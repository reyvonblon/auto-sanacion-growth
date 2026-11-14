#!/usr/bin/env python3
"""Unit tests for the Auto Sanación Amazon growth automation toolkit."""

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import ads_analyzer  # noqa: E402
import kdp_sales_tracker  # noqa: E402
import kdp_seo_optimizer  # noqa: E402
import run_weekly_cycle  # noqa: E402


class TestKdpSeoOptimizer(unittest.TestCase):
    def test_utf8_byte_limit_spanish_accents(self) -> None:
        # "sanación" is 8 chars but 9 UTF-8 bytes
        self.assertEqual(kdp_seo_optimizer.utf8_bytes("sanación"), 9)

        phrases = [
            "psicología integrativa bienestar emocional",
            "sanación cuerpo mente alma",
            "libro gratis amazon bestseller",  # should be skipped (prohibited)
            "superar cáncer embarazo resiliencia",
            "psiconeuroinmunología salud holística",
            "terapia familiar duelo ansiedad estrés",
            "medicina natural esperanza transformación",
        ]
        packed = kdp_seo_optimizer.pack_keyword_boxes(
            phrases,
            title_text="AUTO SANACIÓN: Descubre como tu cuerpo tiene los recursos para sanar",
            author_text="Francis Jaramillo",
        )
        self.assertEqual(len(packed["boxes"]), 7)
        self.assertTrue(all(b["valid"] for b in packed["boxes"]))
        self.assertTrue(all(b["utf8_bytes"] <= 50 for b in packed["boxes"]))
        self.assertEqual(len(packed["skipped_prohibited"]), 1)

    def test_html_description_validation(self) -> None:
        valid_html = "<h4>Título</h4><p>Texto <b>negrita</b> y <i>cursiva</i>.</p><ul><li>Punto 1</li></ul>"
        res_ok = kdp_seo_optimizer.validate_kdp_description_html(valid_html)
        self.assertTrue(res_ok["valid"])

        invalid_html = "<div>No permitido</div><script>bad()</script>"
        res_bad = kdp_seo_optimizer.validate_kdp_description_html(invalid_html)
        self.assertFalse(res_bad["valid"])
        self.assertIn("div", res_bad["unsupported_tags"])
        self.assertIn("script", res_bad["unsupported_tags"])


class TestAdsAnalyzer(unittest.TestCase):
    def test_analyze_search_terms_and_export_bulk(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            csv_file = tmp_path / "search_terms.csv"
            with csv_file.open("w", encoding="utf-8", newline="") as f:
                w = csv.writer(f)
                w.writerow(
                    [
                        "Campaign Name",
                        "Ad Group Name",
                        "Match Type",
                        "Customer Search Term",
                        "Impressions",
                        "Clicks",
                        "Spend",
                        "7 Day Total Sales",
                        "7 Day Total Orders (#)",
                    ]
                )
                w.writerow(["SP Auto", "Auto AG", "AUTO", "sanacion emocional libro", "1200", "15", "$4.50", "$29.98", "2"])
                w.writerow(["SP Auto", "Auto AG", "AUTO", "novela romantica gratis", "900", "12", "$6.20", "$0.00", "0"])
                w.writerow(["SP Auto", "Auto AG", "AUTO", "b08xyz1234", "500", "10", "$5.50", "$0.00", "0"])

            rows = ads_analyzer.load_search_terms(csv_file)
            analysis = ads_analyzer.analyze_search_terms(rows, target_acos=35.0)
            self.assertEqual(len(analysis["scale"]), 1)
            self.assertEqual(analysis["scale"][0].search_term, "sanacion emocional libro")
            self.assertEqual(len(analysis["negatives"]), 2)
            self.assertAlmostEqual(analysis["summary"]["wasted_spend_detected"], 11.70)

            neg_csv = tmp_path / "negatives.csv"
            ads_analyzer.export_bulk_negatives(analysis["negatives"], neg_csv)
            with neg_csv.open("r", encoding="utf-8") as nf:
                neg_rows = list(csv.DictReader(nf))
            self.assertEqual(len(neg_rows), 2)
            entities = {r["Entity"] for r in neg_rows}
            self.assertEqual(entities, {"Negative Keyword", "Negative Product Targeting"})

    def test_starter_bulk_generation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            spec_path = tmp_path / "spec.json"
            spec_path.write_text(
                json.dumps(
                    {
                        "campaigns": [
                            {
                                "name": "SP_Exact_ES",
                                "targeting_type": "MANUAL",
                                "daily_budget": 10.0,
                                "ad_groups": [
                                    {
                                        "name": "Core_Keywords",
                                        "default_bid": 0.35,
                                        "product_ad_asins": ["B0TEST1234"],
                                        "keywords": [{"text": "autosanacion emocional", "match_type": "exact", "bid": 0.40}],
                                    }
                                ],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            out_csv = tmp_path / "bulk.csv"
            count = ads_analyzer.generate_starter_bulk_csv(spec_path, out_csv)
            self.assertEqual(count, 4)
            self.assertTrue(out_csv.exists())


class TestKdpSalesTracker(unittest.TestCase):
    def test_kdp_sales_aggregation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_file = Path(tmp) / "kdp.csv"
            with csv_file.open("w", encoding="utf-8", newline="") as f:
                w = csv.writer(f)
                w.writerow(["Title", "Marketplace", "Transaction Type", "Net Units Sold", "KENP Read", "Royalty"])
                w.writerow(["Auto Sanación", "Amazon.com", "Standard", "12", "0", "$48.00"])
                w.writerow(["Auto Sanación", "Amazon.es", "KENP", "0", "3500", "$15.40"])

            summary = kdp_sales_tracker.analyze_kdp_csv(csv_file, ad_spend=20.0)
            self.assertEqual(summary["total_units"], 12)
            self.assertEqual(summary["total_kenp"], 3500)
            self.assertAlmostEqual(summary["total_royalty"], 63.40)
            self.assertAlmostEqual(summary["net_profit_after_ads"], 43.40)
            self.assertEqual(len(summary["by_marketplace"]), 2)


class TestWeeklyOrchestrator(unittest.TestCase):
    def test_run_cycle_combined(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            kdp_csv = tmp_path / "kdp.csv"
            with kdp_csv.open("w", encoding="utf-8", newline="") as f:
                w = csv.writer(f)
                w.writerow(["Title", "Marketplace", "Net Units Sold", "KENP Read", "Royalty"])
                w.writerow(["Auto Sanación", "Amazon.com", "10", "1000", "$45.00"])

            ads_csv = tmp_path / "ads.csv"
            with ads_csv.open("w", encoding="utf-8", newline="") as f:
                w = csv.writer(f)
                w.writerow(["Campaign Name", "Ad Group Name", "Match Type", "Customer Search Term", "Impressions", "Clicks", "Spend", "7 Day Total Sales", "7 Day Total Orders (#)"])
                w.writerow(["SP_Auto", "AG1", "AUTO", "sanacion", "500", "10", "$5.00", "$20.00", "2"])

            out_dir = tmp_path / "weekly_out"
            res = run_weekly_cycle.run_cycle(out_dir=out_dir, kdp_csv=kdp_csv, search_terms_csv=ads_csv)
            self.assertTrue((out_dir / "resumen_ejecutivo.md").exists())
            self.assertTrue((out_dir / "resumen_kdp.md").exists())
            self.assertTrue((out_dir / "ads_analysis_report.md").exists())
            self.assertTrue((out_dir / "bulk_negatives.csv").exists())
            self.assertAlmostEqual(res["kdp_summary"]["net_profit_after_ads"], 40.00)


if __name__ == "__main__":
    unittest.main()
