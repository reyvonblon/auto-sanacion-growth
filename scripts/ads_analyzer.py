#!/usr/bin/env python3
"""Amazon Ads (PPC) Search Term Analyzer & Bulk Sheet Generator for Books.

Supports English and Spanish Amazon Ads CSV exports, detects wasted ad spend
(negative keyword candidates), identifies profitable terms to promote to Exact
Match campaigns, and exports actionable reports + Amazon Ads Bulk CSVs.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path

COLUMN_ALIASES = {
    "campaign": ["campaign name", "nombre de la campaña", "nombre de campana"],
    "ad_group": ["ad group name", "nombre del grupo de anuncios"],
    "targeting": ["targeting", "segmentación", "segmentacion", "keyword"],
    "match_type": ["match type", "tipo de concordancia"],
    "search_term": [
        "customer search term",
        "término de búsqueda del cliente",
        "termino de busqueda del cliente",
        "search term",
    ],
    "impressions": ["impressions", "impresiones"],
    "clicks": ["clicks", "clics"],
    "spend": ["spend", "gasto", "cost"],
    "sales": [
        "7 day total sales",
        "14 day total sales",
        "ventas totales de 7 días",
        "ventas totales de 7 dias",
        "sales",
    ],
    "orders": [
        "7 day total orders (#)",
        "14 day total orders (#)",
        "pedidos totales de 7 días (#)",
        "pedidos totales de 7 dias (#)",
        "orders",
    ],
}


def parse_number(value: str | float | int | None) -> float:
    """Parse numeric values with currency symbols, commas, or percentages."""
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    cleaned = str(value).strip()
    if not cleaned or cleaned in {"-", "--", "N/A"}:
        return 0.0
    cleaned = re.sub(r"[^\d,.\-]", "", cleaned)
    # Handle European decimal comma if no dot is present
    if "," in cleaned and "." not in cleaned:
        parts = cleaned.split(",")
        if len(parts[-1]) <= 2:
            cleaned = cleaned.replace(",", ".")
        else:
            cleaned = cleaned.replace(",", "")
    else:
        cleaned = cleaned.replace(",", "")
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def map_headers(fieldnames: list[str]) -> dict[str, str]:
    """Map canonical keys to the actual CSV header names."""
    lower_map = {h.strip().lower(): h for h in fieldnames}
    resolved: dict[str, str] = {}
    for canonical, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in lower_map:
                resolved[canonical] = lower_map[alias]
                break
    return resolved


@dataclass
class SearchTermMetric:
    campaign: str
    ad_group: str
    match_type: str
    search_term: str
    impressions: int
    clicks: int
    spend: float
    sales: float
    orders: int

    @property
    def ctr(self) -> float:
        return (self.clicks / self.impressions * 100.0) if self.impressions else 0.0

    @property
    def cpc(self) -> float:
        return (self.spend / self.clicks) if self.clicks else 0.0

    @property
    def acos(self) -> float | None:
        return (self.spend / self.sales * 100.0) if self.sales > 0 else None

    @property
    def is_asin(self) -> bool:
        return bool(re.fullmatch(r"b0[a-z0-9]{8}", self.search_term.strip().lower()))


def load_search_terms(csv_path: Path) -> list[SearchTermMetric]:
    """Load and aggregate search term rows from an Amazon Ads CSV export."""
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            return []
        headers = map_headers(list(reader.fieldnames))
        if "search_term" not in headers:
            raise ValueError(f"Could not find search term column in {csv_path}")

        rows: list[SearchTermMetric] = []
        for row in reader:
            term = (row.get(headers["search_term"]) or "").strip()
            if not term:
                continue
            rows.append(
                SearchTermMetric(
                    campaign=(row.get(headers.get("campaign", ""), "") or "").strip(),
                    ad_group=(row.get(headers.get("ad_group", ""), "") or "").strip(),
                    match_type=(row.get(headers.get("match_type", ""), "") or "").strip(),
                    search_term=term,
                    impressions=int(parse_number(row.get(headers.get("impressions", "")))),
                    clicks=int(parse_number(row.get(headers.get("clicks", "")))),
                    spend=parse_number(row.get(headers.get("spend", ""))),
                    sales=parse_number(row.get(headers.get("sales", ""))),
                    orders=int(parse_number(row.get(headers.get("orders", "")))),
                )
            )
    return rows


def analyze_search_terms(
    rows: list[SearchTermMetric],
    target_acos: float = 35.0,
    min_bleeder_clicks: int = 8,
    max_bleeder_spend: float = 5.0,
) -> dict:
    """Classify search terms into Scale, Optimize, Negative Exact, and Watch."""
    scale: list[SearchTermMetric] = []
    optimize: list[SearchTermMetric] = []
    negatives: list[SearchTermMetric] = []
    watch: list[SearchTermMetric] = []

    for r in rows:
        if r.orders == 0 and (r.clicks >= min_bleeder_clicks or r.spend >= max_bleeder_spend):
            negatives.append(r)
        elif r.orders >= 2 and r.acos is not None and r.acos <= target_acos:
            scale.append(r)
        elif r.orders >= 1:
            optimize.append(r)
        else:
            watch.append(r)

    total_impr = sum(r.impressions for r in rows)
    total_clicks = sum(r.clicks for r in rows)
    total_spend = sum(r.spend for r in rows)
    total_sales = sum(r.sales for r in rows)
    total_orders = sum(r.orders for r in rows)

    summary = {
        "total_terms": len(rows),
        "impressions": total_impr,
        "clicks": total_clicks,
        "spend": round(total_spend, 2),
        "sales": round(total_sales, 2),
        "orders": total_orders,
        "ctr_percent": round((total_clicks / total_impr * 100.0) if total_impr else 0.0, 2),
        "cpc": round((total_spend / total_clicks) if total_clicks else 0.0, 2),
        "cvr_percent": round((total_orders / total_clicks * 100.0) if total_clicks else 0.0, 2),
        "acos_percent": round((total_spend / total_sales * 100.0), 2) if total_sales > 0 else None,
        "wasted_spend_detected": round(sum(r.spend for r in negatives), 2),
    }

    return {
        "summary": summary,
        "scale": sorted(scale, key=lambda x: (-x.orders, x.acos or 999)),
        "optimize": sorted(optimize, key=lambda x: (-x.orders, x.spend)),
        "negatives": sorted(negatives, key=lambda x: -x.spend),
        "watch_count": len(watch),
    }


def export_bulk_negatives(negatives: list[SearchTermMetric], output_csv: Path) -> None:
    """Write Amazon Ads Bulk Operations CSV for Negative Exact keywords and ASINs."""
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "Product",
                "Entity",
                "Operation",
                "Campaign Name",
                "Ad Group Name",
                "Keyword Text",
                "Product Targeting Expression",
                "Match Type",
                "State",
            ]
        )
        for item in negatives:
            if item.is_asin:
                writer.writerow(
                    [
                        "Sponsored Products",
                        "Negative Product Targeting",
                        "Create",
                        item.campaign,
                        item.ad_group,
                        "",
                        f'asin="{item.search_term.upper()}"',
                        "",
                        "enabled",
                    ]
                )
            else:
                writer.writerow(
                    [
                        "Sponsored Products",
                        "Negative Keyword",
                        "Create",
                        item.campaign,
                        item.ad_group,
                        item.search_term,
                        "",
                        "negativeExact",
                        "enabled",
                    ]
                )


def render_markdown_report(analysis: dict) -> str:
    """Format analysis metrics and actions as a concise Markdown report."""
    s = analysis["summary"]
    acos_display = f"{s['acos_percent']}%" if s["acos_percent"] is not None else "N/A"
    lines = [
        "# Reporte de Optimización Amazon Ads — Auto Sanación",
        "",
        "## Resumen Global",
        f"- **Términos analizados:** {s['total_terms']}",
        f"- **Impresiones:** {s['impressions']:,} | **Clics:** {s['clicks']:,} (CTR: {s['ctr_percent']}%)",
        f"- **Gasto:** ${s['spend']:.2f} | **Ventas:** ${s['sales']:.2f} | **Pedidos:** {s['orders']}",
        f"- **CPC promedio:** ${s['cpc']:.2f} | **Conversión (CVR):** {s['cvr_percent']}%",
        f"- **ACoS:** {acos_display}",
        f"- **Gasto desperdiciado recuperable (Negativas):** ${s['wasted_spend_detected']:.2f}",
        "",
        "## 1. Términos Ganadores para Escalar a Exact Match",
    ]
    if analysis["scale"]:
        lines.append("| Término / ASIN | Campaña | Pedidos | Gasto | Ventas | ACoS |")
        lines.append("| :--- | :--- | ---: | ---: | ---: | ---: |")
        for item in analysis["scale"]:
            acos_str = f"{item.acos:.1f}%" if item.acos is not None else "N/A"
            lines.append(
                f"| `{item.search_term}` | {item.campaign} | {item.orders} | ${item.spend:.2f} | ${item.sales:.2f} | {acos_str} |"
            )
    else:
        lines.append("_Sin términos con >=2 pedidos debajo del ACoS objetivo todavía._")

    lines.extend(["", "## 2. Candidatos a Palabra Clave Negativa Exacta (0 pedidos)"])
    if analysis["negatives"]:
        lines.append("| Término / ASIN | Campaña | Clics | Gasto |")
        lines.append("| :--- | :--- | ---: | ---: |")
        for item in analysis["negatives"]:
            lines.append(
                f"| `{item.search_term}` | {item.campaign} | {item.clicks} | ${item.spend:.2f} |"
            )
    else:
        lines.append("_No se detectaron fugas críticas de presupuesto bajo los umbrales actuales._")

    return "\n".join(lines) + "\n"


def generate_starter_bulk_csv(spec_json: Path, output_csv: Path) -> int:
    """Generate a Sponsored Products Bulk Operations CSV from a campaign JSON spec."""
    spec = json.loads(spec_json.read_text(encoding="utf-8"))
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    rows_written = 0

    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "Product",
                "Entity",
                "Operation",
                "Campaign ID",
                "Ad Group ID",
                "Campaign Name",
                "Ad Group Name",
                "Start Date",
                "Targeting Type",
                "State",
                "Daily Budget",
                "Bid",
                "SKU",
                "ASIN",
                "Keyword Text",
                "Match Type",
                "Product Targeting Expression",
            ]
        )
        for camp in spec.get("campaigns", []):
            cid = camp["name"]
            writer.writerow(
                [
                    "Sponsored Products",
                    "Campaign",
                    "Create",
                    cid,
                    "",
                    camp["name"],
                    "",
                    camp.get("start_date", ""),
                    camp.get("targeting_type", "MANUAL"),
                    camp.get("state", "enabled"),
                    camp.get("daily_budget", 5.0),
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                ]
            )
            rows_written += 1

            for ag in camp.get("ad_groups", []):
                agid = f"{cid}::{ag['name']}"
                writer.writerow(
                    [
                        "Sponsored Products",
                        "Ad Group",
                        "Create",
                        cid,
                        agid,
                        camp["name"],
                        ag["name"],
                        "",
                        "",
                        "enabled",
                        "",
                        ag.get("default_bid", 0.35),
                        "",
                        "",
                        "",
                        "",
                        "",
                    ]
                )
                rows_written += 1

                for asin in ag.get("product_ad_asins", []):
                    writer.writerow(
                        [
                            "Sponsored Products",
                            "Product Ad",
                            "Create",
                            cid,
                            agid,
                            camp["name"],
                            ag["name"],
                            "",
                            "",
                            "enabled",
                            "",
                            "",
                            "",
                            asin,
                            "",
                            "",
                            "",
                        ]
                    )
                    rows_written += 1

                for kw in ag.get("keywords", []):
                    writer.writerow(
                        [
                            "Sponsored Products",
                            "Keyword",
                            "Create",
                            cid,
                            agid,
                            camp["name"],
                            ag["name"],
                            "",
                            "",
                            "enabled",
                            "",
                            kw.get("bid", ag.get("default_bid", 0.35)),
                            "",
                            "",
                            kw["text"],
                            kw.get("match_type", "exact"),
                            "",
                        ]
                    )
                    rows_written += 1

                for pt in ag.get("product_targets", []):
                    writer.writerow(
                        [
                            "Sponsored Products",
                            "Product Targeting",
                            "Create",
                            cid,
                            agid,
                            camp["name"],
                            ag["name"],
                            "",
                            "",
                            "enabled",
                            "",
                            pt.get("bid", ag.get("default_bid", 0.30)),
                            "",
                            "",
                            "",
                            "",
                            pt["expression"],
                        ]
                    )
                    rows_written += 1
    return rows_written


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze Amazon Ads reports or generate Bulk CSVs.")
    parser.add_argument("--search-terms-csv", type=Path, help="Path to exported Search Term Report CSV.")
    parser.add_argument("--target-acos", type=float, default=35.0, help="Target ACoS percentage.")
    parser.add_argument("--min-bleeder-clicks", type=int, default=8, help="Min clicks w/ 0 orders to flag negative.")
    parser.add_argument("--max-bleeder-spend", type=float, default=5.0, help="Max spend w/ 0 orders to flag negative.")
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/ads"), help="Output directory.")
    parser.add_argument("--starter-spec-json", type=Path, help="JSON spec to build starter Bulk CSV.")
    args = parser.parse_args()

    if args.starter_spec_json:
        out_bulk = args.out_dir / "starter_bulk_campaigns.csv"
        count = generate_starter_bulk_csv(args.starter_spec_json, out_bulk)
        print(json.dumps({"starter_bulk_csv": str(out_bulk), "rows": count}, indent=2))

    if args.search_terms_csv:
        rows = load_search_terms(args.search_terms_csv)
        analysis = analyze_search_terms(
            rows,
            target_acos=args.target_acos,
            min_bleeder_clicks=args.min_bleeder_clicks,
            max_bleeder_spend=args.max_bleeder_spend,
        )
        args.out_dir.mkdir(parents=True, exist_ok=True)
        report_path = args.out_dir / "ads_analysis_report.md"
        report_path.write_text(render_markdown_report(analysis), encoding="utf-8")
        neg_csv = args.out_dir / "bulk_negatives.csv"
        export_bulk_negatives(analysis["negatives"], neg_csv)
        print(
            json.dumps(
                {
                    "summary": analysis["summary"],
                    "report_path": str(report_path),
                    "negatives_csv": str(neg_csv),
                },
                ensure_ascii=False,
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
