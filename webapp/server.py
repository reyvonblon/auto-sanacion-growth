#!/usr/bin/env python3
"""24/7 HTTP Server for Auto Sanación Sales Funnel, Smart QR Router, School & CRM."""

from __future__ import annotations

import csv
import io
import json
import mimetypes
import os
import re
import sys
import tempfile
import threading
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
STATIC_DIR = Path(__file__).resolve().parent / "static"
LATEST_OUTPUT_DIR = PROJECT_ROOT / "data" / "latest_cycle"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

import autopilot_dispatcher  # noqa: E402
import database  # noqa: E402
import run_weekly_cycle  # noqa: E402


def build_amazon_urls(settings: dict[str, str]) -> dict[str, str]:
    domain = settings.get("amazon_domain", "amazon.com").strip() or "amazon.com"
    title_q = "AUTO+SANACION+Francis+Jaramillo"

    def dp_or_search(asin: str) -> str:
        clean = (asin or "").strip()
        if clean and "PENDIENTE" not in clean.upper() and "REEMPLAZAR" not in clean.upper():
            return f"https://www.{domain}/dp/{clean}"
        return f"https://www.{domain}/s?k={title_q}"

    kindle_asin = settings.get("asin_kindle", "")
    paper_asin = settings.get("asin_paperback", "")
    english_asin = settings.get("asin_english", "")
    audible_asin = settings.get("asin_audible", "")
    review_asin = paper_asin if ("PENDIENTE" not in paper_asin.upper() and paper_asin.strip()) else kindle_asin
    review_url = (
        f"https://www.{domain}/review/create-review/?asin={review_asin.strip()}"
        if review_asin and "PENDIENTE" not in review_asin.upper()
        else f"https://www.{domain}/s?k={title_q}"
    )

    return {
        "kindle_url": dp_or_search(kindle_asin),
        "paperback_url": dp_or_search(paper_asin),
        "english_url": dp_or_search(english_asin),
        "audible_url": dp_or_search(audible_asin),
        "review_url": review_url,
    }


def build_whatsapp_url(number: str, message: str) -> str:
    digits = re.sub(r"[^\d]", "", number or "")
    from urllib.parse import quote

    encoded = quote(message)
    if digits:
        return f"https://wa.me/{digits}?text={encoded}"
    return f"https://wa.me/?text={encoded}"


class AutoSanacionHandler(BaseHTTPRequestHandler):
    server_version = "AutoSanacionStudio/1.0"

    def log_message(self, format: str, *args: Any) -> None:
        # Keep console output concise unless debugging
        if os.environ.get("AUTOSANACION_QUIET") == "1":
            return
        super().log_message(format, *args)

    def _send_json(self, payload: Any, status: int = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_bytes(self, data: bytes, content_type: str, filename: str | None = None) -> None:
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        if filename:
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.end_headers()
        self.wfile.write(data)

    def _serve_static_file(self, rel_path: str) -> None:
        safe_path = (STATIC_DIR / rel_path.lstrip("/")).resolve()
        if not str(safe_path).startswith(str(STATIC_DIR.resolve())) or not safe_path.is_file():
            self._send_json({"error": "Recurso no encontrado"}, status=HTTPStatus.NOT_FOUND)
            return
        mime, _ = mimetypes.guess_type(str(safe_path))
        ctype = f"{mime or 'application/octet-stream'}; charset=utf-8" if (mime or "").startswith("text/") or mime == "application/javascript" else (mime or "application/octet-stream")
        self._send_bytes(safe_path.read_bytes(), ctype)

    def _read_json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            self._serve_static_file("index.html")
            return
        if path in {"/escuela", "/escuela.html"}:
            self._serve_static_file("escuela.html")
            return
        if path in {"/admin", "/admin.html"}:
            self._serve_static_file("admin.html")
            return
        if path.startswith("/qr/"):
            slug = path[len("/qr/"):].strip("/") or "contacto"
            ctx = database.get_qr_context(slug)
            database.log_qr_scan(
                slug=slug,
                chapter_ref=ctx.get("chapter_ref", ""),
                user_agent=self.headers.get("User-Agent", ""),
            )
            self._serve_static_file("qr.html")
            return
        if path.startswith("/static/"):
            self._serve_static_file(path[len("/static/"):])
            return

        if path == "/api/health":
            self._send_json({"status": "ok", "service": "Auto Sanación Studio"})
            return

        if path == "/api/config":
            settings = database.get_settings()
            self._send_json(
                {
                    "settings": settings,
                    "amazon_urls": build_amazon_urls(settings),
                    "whatsapp_direct_url": build_whatsapp_url(
                        settings.get("whatsapp_number", ""),
                        "Hola Francis, vengo desde la página oficial de Auto Sanación y quiero conocer más.",
                    ),
                }
            )
            return

        if path.startswith("/api/qr/"):
            slug = path[len("/api/qr/"):].strip("/") or "contacto"
            ctx = database.get_qr_context(slug)
            settings = database.get_settings()
            msg = (
                f"Hola Francis, acabo de escanear el QR de '{ctx['chapter_ref']}' "
                f"del libro Auto Sanación y quiero continuar mi proceso."
            )
            self._send_json(
                {
                    "qr": ctx,
                    "whatsapp_url": build_whatsapp_url(settings.get("whatsapp_number", ""), msg),
                    "amazon_urls": build_amazon_urls(settings),
                }
            )
            return

        if path == "/api/dashboard":
            metrics = database.get_dashboard_metrics()
            settings = database.get_settings()
            self._send_json({"metrics": metrics, "amazon_urls": build_amazon_urls(settings)})
            return

        if path == "/api/leads":
            search = qs.get("search", [""])[0]
            stage = qs.get("stage", [""])[0]
            leads = database.list_leads(search=search, stage=stage)
            settings = database.get_settings()
            wa_num = settings.get("whatsapp_number", "")
            for item in leads:
                target_num = item.get("whatsapp") or ""
                item["whatsapp_chat_url"] = build_whatsapp_url(
                    target_num,
                    f"Hola {item['name']}, te saluda Francis Jaramillo (Auto Sanación). ¿Cómo vas con tu lectura?",
                ) if target_num else ""
                item["author_whatsapp_configured"] = bool(re.sub(r"[^\d]", "", wa_num))
            self._send_json({"leads": leads})
            return

        if path == "/api/leads/export.csv":
            leads = database.list_leads()
            buf = io.StringIO()
            writer = csv.writer(buf)
            writer.writerow(["ID", "Nombre", "Correo", "WhatsApp", "Origen", "Etapa", "Notas", "Creado", "Actualizado"])
            for l in leads:
                writer.writerow(
                    [l["id"], l["name"], l["email"], l["whatsapp"], l["source"], l["stage"], l["notes"], l["created_at"], l["updated_at"]]
                )
            data = ("\ufeff" + buf.getvalue()).encode("utf-8")
            self._send_bytes(data, "text/csv; charset=utf-8", filename="leads_auto_sanacion.csv")
            return

        if path == "/api/sales":
            self._send_json({"sales": database.list_sales()})
            return

        if path == "/api/school":
            self._send_json({"modules": database.get_school_curriculum()})
            return

        if path == "/api/student/progress":
            email = qs.get("email", [""])[0]
            if not email.strip():
                self._send_json({"error": "Se requiere el parámetro email"}, status=HTTPStatus.BAD_REQUEST)
                return
            self._send_json(database.get_student_progress_by_email(email))
            return

        if path == "/api/admin/reflections":
            self._send_json({"reflections": database.list_student_reflections()})
            return

        if path == "/api/admin/bulk-negatives.csv":
            neg_file = LATEST_OUTPUT_DIR / "bulk_negatives.csv"
            if not neg_file.exists():
                self._send_json({"error": "Aún no se ha generado ningún archivo de negativas."}, status=HTTPStatus.NOT_FOUND)
                return
            self._send_bytes(neg_file.read_bytes(), "text/csv; charset=utf-8", filename="bulk_negatives.csv")
            return

        if path == "/api/admin/outbox":
            self._send_json(
                {
                    "config_status": autopilot_dispatcher.get_autopilot_status(),
                    "jobs": database.list_outbox_jobs(),
                }
            )
            return

        self._send_json({"error": "Ruta no encontrada"}, status=HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path

        try:
            data = self._read_json_body()
        except Exception as exc:
            self._send_json({"error": f"JSON inválido: {exc}"}, status=HTTPStatus.BAD_REQUEST)
            return

        if path == "/api/config":
            allowed_keys = {
                "asin_kindle",
                "asin_paperback",
                "asin_english",
                "asin_audible",
                "amazon_domain",
                "whatsapp_number",
                "school_welcome_message",
            }
            filtered = {k: v for k, v in data.items() if k in allowed_keys}
            updated = database.update_settings(filtered)
            self._send_json({"settings": updated, "amazon_urls": build_amazon_urls(updated)})
            return

        if path == "/api/leads":
            try:
                lead = database.upsert_lead(
                    name=data.get("name", ""),
                    email=data.get("email", ""),
                    whatsapp=data.get("whatsapp", ""),
                    source=data.get("source", "landing"),
                    stage=data.get("stage", "nuevo_lead"),
                    notes=data.get("notes", ""),
                )
            except ValueError as exc:
                self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
                return
            self._send_json({"lead": lead}, status=HTTPStatus.CREATED)
            return

        if path == "/api/sales":
            entry = database.add_sale_entry(
                period_label=data.get("period_label", ""),
                marketplace=data.get("marketplace", "Amazon.com"),
                units=int(data.get("units", 0) or 0),
                kenp=int(data.get("kenp", 0) or 0),
                royalty_usd=float(data.get("royalty_usd", 0.0) or 0.0),
                ad_spend_usd=float(data.get("ad_spend_usd", 0.0) or 0.0),
                orders_ads=int(data.get("orders_ads", 0) or 0),
                source="manual",
            )
            self._send_json({"sale": entry}, status=HTTPStatus.CREATED)
            return

        if path == "/api/student/progress":
            email = (data.get("email") or "").strip()
            name = (data.get("name") or "").strip()
            lesson_id = data.get("lesson_id")
            if not email or not lesson_id:
                self._send_json({"error": "email y lesson_id son obligatorios"}, status=HTTPStatus.BAD_REQUEST)
                return
            res = database.save_student_progress(
                email=email,
                name=name or email.split("@")[0],
                lesson_id=int(lesson_id),
                completed=bool(data.get("completed", True)),
                reflection_text=data.get("reflection_text", ""),
                whatsapp=data.get("whatsapp", ""),
            )
            self._send_json(res)
            return

        if path == "/api/admin/reflections/feedback":
            progress_id = data.get("progress_id")
            feedback = data.get("feedback", "")
            if not progress_id:
                self._send_json({"error": "progress_id es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
                return
            updated = database.save_francis_feedback(int(progress_id), str(feedback))
            if not updated:
                self._send_json({"error": "Registro no encontrado"}, status=HTTPStatus.NOT_FOUND)
                return
            self._send_json({"progress": updated})
            return

        if path == "/api/school/lessons":
            module_id = data.get("module_id")
            title = (data.get("title") or "").strip()
            if not module_id or not title:
                self._send_json({"error": "module_id y title son obligatorios"}, status=HTTPStatus.BAD_REQUEST)
                return
            lesson = database.create_lesson(
                module_id=int(module_id),
                title=title,
                video_url=data.get("video_url", ""),
                reading_guide=data.get("reading_guide", ""),
                exercise_prompt=data.get("exercise_prompt", ""),
                duration_minutes=int(data.get("duration_minutes", 12) or 12),
            )
            self._send_json({"lesson": lesson}, status=HTTPStatus.CREATED)
            return

        if path == "/api/admin/import-reports":
            kdp_csv_text = (data.get("kdp_csv") or "").strip()
            ads_csv_text = (data.get("ads_csv") or "").strip()
            period_label = (data.get("period_label") or "Importación Amazon").strip()
            target_acos = float(data.get("target_acos", 35.0) or 35.0)

            if not kdp_csv_text and not ads_csv_text:
                self._send_json({"error": "Adjunta al menos un archivo CSV de KDP o Amazon Ads."}, status=HTTPStatus.BAD_REQUEST)
                return

            with tempfile.TemporaryDirectory() as tmp:
                tmp_path = Path(tmp)
                kdp_path = None
                ads_path = None
                if kdp_csv_text:
                    kdp_path = tmp_path / "kdp.csv"
                    kdp_path.write_text(kdp_csv_text, encoding="utf-8")
                if ads_csv_text:
                    ads_path = tmp_path / "ads.csv"
                    ads_path.write_text(ads_csv_text, encoding="utf-8")

                result = run_weekly_cycle.run_cycle(
                    out_dir=LATEST_OUTPUT_DIR,
                    kdp_csv=kdp_path,
                    search_terms_csv=ads_path,
                    target_acos=target_acos,
                )

            kdp_sum = result.get("kdp_summary") or {}
            ads_sum = result.get("ads_summary") or {}
            saved_sale = database.add_sale_entry(
                period_label=period_label,
                marketplace="Consolidado Amazon",
                units=int(kdp_sum.get("total_units", 0)),
                kenp=int(kdp_sum.get("total_kenp", 0)),
                royalty_usd=float(kdp_sum.get("total_royalty", 0.0)),
                ad_spend_usd=float(ads_sum.get("spend", 0.0)),
                orders_ads=int(ads_sum.get("orders", 0)),
                source="csv_import",
            )
            self._send_json(
                {
                    "cycle_result": result,
                    "saved_sale": saved_sale,
                    "has_negatives_csv": (LATEST_OUTPUT_DIR / "bulk_negatives.csv").exists(),
                }
            )
            return

        if path == "/api/admin/outbox/dispatch":
            self._send_json(autopilot_dispatcher.dispatch_due_jobs())
            return

        if path == "/api/admin/outbox/queue-social":
            subject = (data.get("subject") or "Publicación automática Auto Sanación").strip()
            body = (data.get("body") or "").strip()
            if not body:
                self._send_json({"error": "El contenido de la publicación es obligatorio."}, status=HTTPStatus.BAD_REQUEST)
                return
            job = database.queue_outbox_job(channel="social_webhook", subject=subject, body=body)
            self._send_json({"job": job}, status=HTTPStatus.CREATED)
            return

        self._send_json({"error": "Ruta POST no encontrada"}, status=HTTPStatus.NOT_FOUND)

    def do_PATCH(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        try:
            data = self._read_json_body()
        except Exception as exc:
            self._send_json({"error": f"JSON inválido: {exc}"}, status=HTTPStatus.BAD_REQUEST)
            return

        if path.startswith("/api/leads/"):
            lead_id_str = path[len("/api/leads/"):].strip("/")
            if not lead_id_str.isdigit():
                self._send_json({"error": "ID inválido"}, status=HTTPStatus.BAD_REQUEST)
                return
            updated = database.update_lead(
                int(lead_id_str),
                stage=data.get("stage"),
                notes=data.get("notes"),
            )
            if not updated:
                self._send_json({"error": "Lead no encontrado"}, status=HTTPStatus.NOT_FOUND)
                return
            self._send_json({"lead": updated})
            return

        if path.startswith("/api/school/lessons/"):
            lesson_id_str = path[len("/api/school/lessons/"):].strip("/")
            if not lesson_id_str.isdigit():
                self._send_json({"error": "ID inválido"}, status=HTTPStatus.BAD_REQUEST)
                return
            updated = database.update_lesson(
                int(lesson_id_str),
                title=data.get("title"),
                video_url=data.get("video_url"),
                reading_guide=data.get("reading_guide"),
                exercise_prompt=data.get("exercise_prompt"),
            )
            if not updated:
                self._send_json({"error": "Lección no encontrada"}, status=HTTPStatus.NOT_FOUND)
                return
            self._send_json({"lesson": updated})
            return

        self._send_json({"error": "Ruta PATCH no encontrada"}, status=HTTPStatus.NOT_FOUND)


def create_server(host: str = "127.0.0.1", port: int = 8795) -> ThreadingHTTPServer:
    database.init_db()
    return ThreadingHTTPServer((host, port), AutoSanacionHandler)


def _start_autopilot_worker(interval_seconds: int) -> threading.Event:
    stop_event = threading.Event()

    def _loop() -> None:
        while not stop_event.wait(interval_seconds):
            try:
                status = autopilot_dispatcher.get_autopilot_status()
                if status.get("smtp_ready") or status.get("social_webhook_ready"):
                    autopilot_dispatcher.dispatch_due_jobs()
            except Exception:
                pass

    thread = threading.Thread(target=_loop, name="autopilot-worker", daemon=True)
    thread.start()
    return stop_event


def main() -> None:
    host = os.environ.get("AUTOSANACION_HOST", "127.0.0.1")
    port = int(os.environ.get("PORT") or os.environ.get("AUTOSANACION_PORT", "8795"))
    server = create_server(host=host, port=port)
    dispatch_interval = int(os.environ.get("AUTOSANACION_DISPATCH_INTERVAL", "60"))
    stop_event = _start_autopilot_worker(dispatch_interval) if dispatch_interval > 0 else None
    print(f"Auto Sanación Studio escuchando en http://{host}:{port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        if stop_event is not None:
            stop_event.set()
        server.server_close()


if __name__ == "__main__":
    main()
