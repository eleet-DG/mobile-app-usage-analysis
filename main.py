#!/usr/bin/env python3
"""
main.py
=======
Command-line entry point for the Mobile App Usage & User Engagement Analysis.

Author  : Piyush Pal
Adm. No : 2026B01010868

Examples
--------
    python main.py                       # analyse data/24_mobile_app_usage.csv
    python main.py --generate            # (re)create the sample CSV first
    python main.py --feature "Search"    # average duration for one feature
    python main.py --no-plots --quiet    # tables only, minimal console output
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from app_engagement import config as cfg
from app_engagement.data_generator import generate_dataset, save_dataset
from app_engagement.data_loader import DatasetError
from app_engagement.pipeline import run_analysis
from app_engagement.report import (
    format_console_report,
    save_clean_dataset,
    save_console_report,
    save_markdown_report,
    save_tables,
)
from app_engagement.visualization import create_all_figures


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=f"{cfg.PROJECT_TITLE} - {cfg.STUDENT_NAME} ({cfg.ADMISSION_NUMBER})",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--data", type=Path, default=cfg.DEFAULT_DATASET_PATH, help="path to the usage CSV file")
    parser.add_argument("--output", type=Path, default=cfg.OUTPUT_DIR, help="folder for tables, charts and reports")
    parser.add_argument("--generate", action="store_true", help="generate a fresh synthetic dataset at --data first")
    parser.add_argument("--seed", type=int, default=cfg.DEFAULT_SEED, help="random seed for --generate")
    parser.add_argument("--feature", type=str, default=None, help="feature used for the task-12 duration function")
    parser.add_argument("--no-plots", action="store_true", help="skip chart creation")
    parser.add_argument("--quiet", action="store_true", help="do not print the full report to the console")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    # Make sure a dataset exists: generate one when requested or when missing.
    if args.generate or not args.data.exists():
        print(f"[setup] Generating sample dataset at {args.data} (seed={args.seed}) ...")
        save_dataset(generate_dataset(seed=args.seed), args.data)

    try:
        results = run_analysis(args.data, selected_feature=args.feature)
    except DatasetError as error:
        print(f"[error] {error}", file=sys.stderr)
        return 1
    except ValueError as error:
        print(f"[error] {error}", file=sys.stderr)
        return 2

    figure_dir = args.output / "figures"
    table_dir = args.output / "tables"

    figures: list[Path] = []
    if not args.no_plots:
        figures = create_all_figures(
            df=results.clean,
            features=results.features,
            devices=results.devices,
            ages=results.ages,
            ratings=results.ratings,
            hours=results.hours,
            weekdays=results.weekdays,
            heatmap=results.heatmap,
            bounds=results.bounds,
            engagement=results.engagement,
            monthly=results.monthly,
            out_dir=figure_dir,
        )

    tables = save_tables(results, table_dir)
    clean_path = save_clean_dataset(results, args.output)
    text_path = save_console_report(results, args.output)
    md_path = save_markdown_report(results, figures, args.output)

    if not args.quiet:
        print(format_console_report(results))

    print("\n[done] Outputs written:")
    print(f"  - {len(tables)} tables       -> {table_dir}")
    print(f"  - {len(figures)} charts       -> {figure_dir}")
    print(f"  - cleaned dataset    -> {clean_path}")
    print(f"  - text report        -> {text_path}")
    print(f"  - markdown report    -> {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
