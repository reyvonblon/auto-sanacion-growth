#!/usr/bin/env python3
"""Automated Email & Social Webhook Dispatcher for Auto Sanación.

Reads pending due jobs from SQLite `outbox_jobs` and sends:
- Emails via SMTP (configured via .env / environment variables)
- Social posts via Webhook (Make / Zapier / n8n / Buffer)

Never fabricates delivery: if credentials are missing, keeps jobs pending and
returns explicit configuration status.
"""

from __future__ import annotations

import argparse
import json
import os
import smtplib
import sys
import urllib.request
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

if str(PROJECT_ROOT / "webapp") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "webapp"))

import database  # noqa: E402


def load_env_file() -> dict[str, str]:
    values: dict[str, str] = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            clean = line.strip()
            if not clean or clean.startswith("#") or "=" not in clean:
                continue
            k, v = clean.split("=", 1)
            values[k.strip()] = v.strip().strip('"').strip("'")
    for k in (
        "SMTP_HOST",
        "SMTP_PORT",
        "SMTP_USER",
        "SMTP_PASS",
        "SMTP_FROM",
        "SOCIAL_WEBHOOK_URL",
    ):
        if os.environ.get(k):
            values[k] = os.environ[k]
    return values


def get_autopilot_status() -> dict[str, bool]:
    cfg = load_env_file()
    smtp_ready = bool(cfg.get("SMTP_HOST") and cfg.get("SMTP_USER") and cfg.get("SMTP_PASS"))
    webhook_ready = bool(cfg.get("SOCIAL_WEBHOOK_URL"))
    return {"smtp_ready": smtp_ready, "social_webhook_ready": webhook_ready}


def send_smtp_email(cfg: dict[str, str], to_addr: str, subject: str, body: str) -> None:
    msg = EmailMessage()
    msg["From"] = cfg.get("SMTP_FROM") or cfg["SMTP_USER"]
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.set_content(body)

    port = int(cfg.get("SMTP_PORT") or "587")
    host = cfg["SMTP_HOST"]
    if port == 465:
        with smtplib.SMTP_SSL(host, port, timeout=15) as smtp:
            smtp.login(cfg["SMTP_USER"], cfg["SMTP_PASS"])
            smtp.send_message(msg)
    else:
        with smtplib.SMTP(host, port, timeout=15) as smtp:
            smtp.starttls()
            smtp.login(cfg["SMTP_USER"], cfg["SMTP_PASS"])
            smtp.send_message(msg)


def send_social_webhook(webhook_url: str, subject: str, body: str) -> None:
    payload = json.dumps(
        {
            "book": "AUTO SANACIÓN — Francis Jaramillo",
            "title": subject,
            "caption": body,
            "timestamp": datetime.now().isoformat(),
        },
        ensure_ascii=False,
    ).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        if resp.status >= 400:
            raise RuntimeError(f"Webhook HTTP {resp.status}")


def dispatch_due_jobs() -> dict:
    database.init_db()
    cfg = load_env_file()
    status = get_autopilot_status()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pending = database.list_outbox_jobs(status="pending")

    sent_count = 0
    skipped_no_creds = 0
    failed_count = 0
    future_count = 0

    for job in pending:
        if job["scheduled_for"] > now_str:
            future_count += 1
            continue
        ch = job["channel"]
        if ch == "email":
            if not status["smtp_ready"]:
                skipped_no_creds += 1
                continue
            try:
                send_smtp_email(cfg, job["recipient"], job["subject"], job["body"])
                database.update_outbox_job(job["id"], "sent")
                sent_count += 1
            except Exception as exc:
                database.update_outbox_job(job["id"], "failed", str(exc))
                failed_count += 1
        elif ch == "social_webhook":
            if not status["social_webhook_ready"]:
                skipped_no_creds += 1
                continue
            try:
                send_social_webhook(cfg["SOCIAL_WEBHOOK_URL"], job["subject"], job["body"])
                database.update_outbox_job(job["id"], "sent")
                sent_count += 1
            except Exception as exc:
                database.update_outbox_job(job["id"], "failed", str(exc))
                failed_count += 1

    return {
        "config_status": status,
        "sent": sent_count,
        "skipped_missing_credentials": skipped_no_creds,
        "failed": failed_count,
        "scheduled_for_later": future_count,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Dispatch due Auto Sanación emails and social posts.")
    parser.add_argument("--status-only", action="store_true", help="Only inspect credentials and pending count.")
    args = parser.parse_args()

    database.init_db()
    if args.status_only:
        print(
            json.dumps(
                {
                    "config_status": get_autopilot_status(),
                    "pending_jobs": len(database.list_outbox_jobs(status="pending")),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return
    print(json.dumps(dispatch_due_jobs(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
