#!/usr/bin/env python3
"""KDP Sales, KENP & TACoS Tracker for Auto Sanación.

Parses KDP Royalties/Sales CSV exports (English or Spanish headers), aggregates
by marketplace and format, and optionally combines with Amazon Ads spend to
compute TACoS (Total Advertising Cost of Sales) and net royalty profit.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

from ads_analyzer import parse_number

KDP_ALIASES = {
    "title": ["title", "título", "titulo"],
    "marketplace": ["marketplace", "tienda"],
    "format": ["transaction type", "tipo de transacción", "tipo de transaccion", "format", "formato"],
    "units": ["net units sold", "units sold", "unidades netas vendidas", "unidades vendidas"],
    "kenp": ["kenp read", "páginas leídas de kenp", "paginas leidas de kenp"],
    "royalty": ["royalty", "regalías", "regalias", "estimated earnings", "ganancias estimadas"],
    "currency": ["currency", "moneda"],
}


def resolve_kdp_headers(fieldnames: list[str]) -> dict[str, str]:
    lower_map = {h.strip().lower(): h for h in fieldnames}
    resolved: dict[str, str] = {}
    for key, aliases in KDP_ALIASES.items():
        for alias in aliases:
            if alias in lower_map:
                resolved[key] = lower_map[alias]
                break
    return resolved


def analyze_kdp_csv(csv_path: Path, ad_spend: float = 0.0) -> dict:
    """Aggregate KDP sales/KENP metrics and compute TACoS & net profit."""
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            return {"total_units": 0, "total_kenp": 0, "total_royalty": 0.0, "by_marketplace": {}}
        headers = resolve_kdp_headers(list(reader.fieldnames))

        total_units = 0
        total_kenp = 0
        total_royalty = 0.0
        by_marketplace: dict[str, dict[str, float | int]] = defaultdict(
            lambda: {"units": 0, "kenp": 0, "royalty": 0.0}
        )

        for row in reader:
            units = int(parse_number(row.get(headers.get("units", ""))))
            kenp = int(parse_number(row.get(headers.get("kenp", ""))))
            royalty = parse_number(row.get(headers.get("royalty", "")))
            mkt = (row.get(headers.get("marketplace", ""), "") or "Unknown").strip()

            total_units += units
            total_kenp += kenp
            total_royalty += royalty

            by_marketplace[mkt]["units"] += units
            by_marketplace[mkt]["kenp"] += kenp
            by_marketplace[mkt]["royalty"] = round(float(by_marketplace[mkt]["royalty"]) + royalty, 2)

    tacos_on_royalty = round((ad_spend / total_royalty * 100.0), 2) if total_royalty > 0 else None
    net_profit = round(total_royalty - ad_spend, 2)

    return {
        "total_units": total_units,
        "total_kenp": total_kenp,
        "total_royalty": round(total_royalty, 2),
        "ad_spend": round(ad_spend, 2),
        "tacos_on_royalty_percent": tacos_on_royalty,
        "net_profit_after_ads": net_profit,
        "by_marketplace": dict(by_marketplace),
    }


def render_sales_markdown(summary: dict) -> str:
    lines = [
        "# Reporte Semanal de Ventas KDP & Rentabilidad — Auto Sanación",
        "",
        "## Métricas Consolidadas",
        f"- **Unidades netas vendidas:** {summary['total_units']}",
        f"- **Páginas leídas (Kindle Unlimited KENP):** {summary['total_kenp']:,}",
        f"- **Regalías totales brutas:** ${summary['total_royalty']:.2f}",
        f"- **Inversión en Amazon Ads:** ${summary['ad_spend']:.2f}",
        f"- **TACoS (Gasto Ads / Regalías):** {summary['tacos_on_royalty_percent']}%"
        if summary["tacos_on_royalty_percent"] is not None
        else "- **TACoS (Gasto Ads / Regalías):** N/A",
        f"- **Utilidad neta después de Ads:** ${summary['net_profit_after_ads']:.2f}",
        "",
        "## Desglose por Tienda (Marketplace)",
        "| Tienda | Unidades | KENP | Regalías |",
        "| :--- | ---: | ---: | ---: |",
    ]
    for mkt, vals in sorted(summary["by_marketplace"].items()):
        lines.append(f"| {mkt} | {vals['units']} | {vals['kenp']:,} | ${vals['royalty']:.2f} |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Track KDP royalties, KENP, and TACoS.")
    parser.add_argument("--kdp-csv", type=Path, required=True, help="Path to KDP royalties/orders CSV.")
    parser.add_argument("--ad-spend", type=float, default=0.0, help="Total ad spend for the period.")
    parser.add_argument("--out-md", type=Path, help="Optional Markdown report output path.")
    args = parser.parse_args()

    summary = analyze_kdp_csv(args.kdp_csv, ad_spend=args.ad_spend)
    if args.out_md:
        args.out_md.parent.mkdir(parents=True, exist_ok=True)
        args.out_md.write_text(render_sales_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
