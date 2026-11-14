#!/usr/bin/env python3
"""Orchestrator CLI runner for weekly Amazon growth cycles of Auto Sanación.

Runs KDP sales aggregation and Amazon Ads Search Term analysis in one command
and produces a consolidated executive summary Markdown report for the Orchestrator.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from ads_analyzer import (
    analyze_search_terms,
    export_bulk_negatives,
    load_search_terms,
    render_markdown_report,
)
from kdp_sales_tracker import analyze_kdp_csv, render_sales_markdown


def run_cycle(
    out_dir: Path,
    kdp_csv: Path | None = None,
    search_terms_csv: Path | None = None,
    target_acos: float = 35.0,
) -> dict:
    """Execute weekly analytics & ads optimization and write consolidated summary."""
    out_dir.mkdir(parents=True, exist_ok=True)
    ads_summary: dict | None = None
    kdp_summary: dict | None = None

    if search_terms_csv and search_terms_csv.exists():
        rows = load_search_terms(search_terms_csv)
        ads_analysis = analyze_search_terms(rows, target_acos=target_acos)
        ads_summary = ads_analysis["summary"]
        (out_dir / "ads_analysis_report.md").write_text(
            render_markdown_report(ads_analysis), encoding="utf-8"
        )
        export_bulk_negatives(ads_analysis["negatives"], out_dir / "bulk_negatives.csv")

    ad_spend = float(ads_summary["spend"]) if ads_summary else 0.0
    if kdp_csv and kdp_csv.exists():
        kdp_summary = analyze_kdp_csv(kdp_csv, ad_spend=ad_spend)
        (out_dir / "resumen_kdp.md").write_text(
            render_sales_markdown(kdp_summary), encoding="utf-8"
        )

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    exec_lines = [
        f"# Ciclo Semanal Orquestado — Auto Sanación ({timestamp})",
        "",
        "## Estado de Fuentes Procesadas",
        f"- **KDP Royalties CSV:** {'Procesado' if kdp_summary else 'Pendiente de proporcionar'}",
        f"- **Amazon Ads Search Terms CSV:** {'Procesado' if ads_summary else 'Pendiente de proporcionar'}",
        "",
    ]
    if kdp_summary:
        exec_lines.extend(
            [
                "## Ventas y Rentabilidad KDP",
                f"- **Unidades vendidas:** {kdp_summary['total_units']}",
                f"- **Páginas KENP leídas:** {kdp_summary['total_kenp']:,}",
                f"- **Regalías totales:** ${kdp_summary['total_royalty']:.2f}",
                f"- **Utilidad neta tras Ads:** ${kdp_summary['net_profit_after_ads']:.2f}",
                "",
            ]
        )
    if ads_summary:
        exec_lines.extend(
            [
                "## Rendimiento Amazon Ads",
                f"- **Gasto:** ${ads_summary['spend']:.2f} | **Ventas Ads:** ${ads_summary['sales']:.2f} | **Pedidos:** {ads_summary['orders']}",
                f"- **ACoS:** {ads_summary['acos_percent']}%" if ads_summary["acos_percent"] is not None else "- **ACoS:** N/A",
                f"- **Gasto recuperable con Negativas generadas:** ${ads_summary['wasted_spend_detected']:.2f}",
                "",
            ]
        )

    exec_path = out_dir / "resumen_ejecutivo.md"
    exec_path.write_text("\n".join(exec_lines) + "\n", encoding="utf-8")

    return {
        "resumen_ejecutivo": str(exec_path),
        "kdp_summary": kdp_summary,
        "ads_summary": ads_summary,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run weekly orchestrated Amazon growth analysis.")
    parser.add_argument("--kdp-csv", type=Path, help="Optional KDP royalties CSV export.")
    parser.add_argument("--search-terms-csv", type=Path, help="Optional Amazon Ads Search Terms CSV.")
    parser.add_argument("--target-acos", type=float, default=35.0, help="Target ACoS percentage.")
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/semanal"), help="Output directory.")
    args = parser.parse_args()

    result = run_cycle(
        out_dir=args.out_dir,
        kdp_csv=args.kdp_csv,
        search_terms_csv=args.search_terms_csv,
        target_acos=args.target_acos,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
