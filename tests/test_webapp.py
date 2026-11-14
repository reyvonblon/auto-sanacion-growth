#!/usr/bin/env python3
"""Integration tests for Auto Sanación Funnel, Smart QR Router, School, and CRM."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "webapp"))

import server  # noqa: E402


class TestWebAppIntegration(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp_dir.name) / "test.db"
        os.environ["AUTOSANACION_DB_PATH"] = str(self.db_path)
        os.environ["AUTOSANACION_QUIET"] = "1"
        server.LATEST_OUTPUT_DIR = Path(self.tmp_dir.name) / "latest_cycle"
        self.httpd = server.create_server(host="127.0.0.1", port=0)
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=2)
        os.environ.pop("AUTOSANACION_DB_PATH", None)
        self.tmp_dir.cleanup()

    def _req(self, path: str, method: str = "GET", payload: dict | None = None) -> tuple[int, str]:
        url = f"http://127.0.0.1:{self.port}{path}"
        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        headers = {"Content-Type": "application/json"} if payload is not None else {}
        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(req, timeout=5) as resp:
            return resp.status, resp.read().decode("utf-8")

    def test_full_funnel_qr_school_and_admin_flow(self) -> None:
        # 1. Health & config update
        status, body = self._req("/api/health")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["status"], "ok")

        status, body = self._req(
            "/api/config",
            method="POST",
            payload={
                "whatsapp_number": "+573001112233",
                "asin_paperback": "B0TESTPAPER",
                "amazon_domain": "amazon.com",
            },
        )
        self.assertEqual(status, 200)
        cfg = json.loads(body)
        self.assertIn("/dp/B0TESTPAPER", cfg["amazon_urls"]["paperback_url"])

        # 2. Smart QR scan + context
        status, html = self._req("/qr/cap-1")
        self.assertEqual(status, 200)
        self.assertIn("QR Inteligente", html)

        status, qr_json = self._req("/api/qr/cap-1")
        qr_data = json.loads(qr_json)
        self.assertEqual(qr_data["qr"]["chapter_ref"], "Capítulo 1")
        self.assertIn("573001112233", qr_data["whatsapp_url"])

        # 3. Lead registration & stage update
        status, lead_body = self._req(
            "/api/leads",
            method="POST",
            payload={
                "name": "Laura Gómez",
                "email": "laura@example.com",
                "whatsapp": "+573009998877",
                "source": "qr_cap-1",
            },
        )
        self.assertEqual(status, 201)
        lead_id = json.loads(lead_body)["lead"]["id"]

        status, _ = self._req(
            f"/api/leads/{lead_id}",
            method="PATCH",
            payload={"stage": "leyendo_libro"},
        )
        self.assertEqual(status, 200)

        status, csv_body = self._req("/api/leads/export.csv")
        self.assertEqual(status, 200)
        self.assertIn("Laura Gómez", csv_body)

        # 4. School progress & Francis feedback
        _, school_body = self._req("/api/school")
        modules = json.loads(school_body)["modules"]
        self.assertEqual(len(modules), 6)
        first_lesson_id = modules[0]["lessons"][0]["id"]

        status, _ = self._req(
            "/api/student/progress",
            method="POST",
            payload={
                "email": "laura@example.com",
                "name": "Laura Gómez",
                "lesson_id": first_lesson_id,
                "completed": True,
                "reflection_text": "Sentí mucha paz haciendo la pausa integrativa.",
            },
        )
        self.assertEqual(status, 200)

        _, refs_body = self._req("/api/admin/reflections")
        refs = json.loads(refs_body)["reflections"]
        self.assertEqual(len(refs), 1)
        progress_id = refs[0]["progress_id"]

        status, _ = self._req(
            "/api/admin/reflections/feedback",
            method="POST",
            payload={
                "progress_id": progress_id,
                "feedback": "Qué alegría Laura, sigue practicando cada noche.",
            },
        )
        self.assertEqual(status, 200)

        _, st_prog_body = self._req("/api/student/progress?email=laura@example.com")
        st_prog = json.loads(st_prog_body)
        self.assertEqual(st_prog["items"][0]["francis_feedback"], "Qué alegría Laura, sigue practicando cada noche.")

        # 5. Import KDP + Ads CSVs via admin endpoint
        kdp_csv = "Title,Marketplace,Net Units Sold,KENP Read,Royalty\nAuto Sanación,Amazon.com,10,1200,$42.00\n"
        ads_csv = (
            "Campaign Name,Ad Group Name,Match Type,Customer Search Term,Impressions,Clicks,Spend,7 Day Total Sales,7 Day Total Orders (#)\n"
            "SP Auto,AG1,AUTO,novela gratis,500,10,$6.00,$0.00,0\n"
            "SP Auto,AG1,AUTO,sanacion emocional,800,12,$4.00,$24.00,2\n"
        )
        status, imp_body = self._req(
            "/api/admin/import-reports",
            method="POST",
            payload={"period_label": "Semana Test", "kdp_csv": kdp_csv, "ads_csv": ads_csv},
        )
        self.assertEqual(status, 200)
        imp = json.loads(imp_body)
        self.assertTrue(imp["has_negatives_csv"])
        self.assertEqual(imp["saved_sale"]["units"], 10)

        status, neg_csv = self._req("/api/admin/bulk-negatives.csv")
        self.assertEqual(status, 200)
        self.assertIn("novela gratis", neg_csv)

        _, dash_body = self._req("/api/dashboard")
        metrics = json.loads(dash_body)["metrics"]
        self.assertEqual(metrics["total_units"], 10)
        self.assertEqual(metrics["qr_scans"], 1)
        self.assertEqual(metrics["pending_feedback"], 0)

        # 6. Automated follow-up outbox (2 emails queued on lead signup + social queue)
        status, outbox_body = self._req("/api/admin/outbox")
        self.assertEqual(status, 200)
        outbox = json.loads(outbox_body)
        self.assertEqual(len(outbox["jobs"]), 2)

        status, _ = self._req(
            "/api/admin/outbox/queue-social",
            method="POST",
            payload={"subject": "Reel Día 1", "body": "Descubre cómo tu cuerpo tiene los recursos para sanar."},
        )
        self.assertEqual(status, 201)

        status, disp_body = self._req("/api/admin/outbox/dispatch", method="POST", payload={})
        self.assertEqual(status, 200)
        disp = json.loads(disp_body)
        # Without SMTP/Webhook env vars, Day 0 email + social post are skipped cleanly (Day 3 is scheduled_for_later)
        self.assertEqual(disp["skipped_missing_credentials"], 2)
        self.assertEqual(disp["scheduled_for_later"], 1)

    def test_static_path_traversal_blocked(self) -> None:
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            self._req("/static/../../config/book_profile.json")
        self.assertEqual(ctx.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
