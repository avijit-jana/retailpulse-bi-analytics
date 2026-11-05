"""CLI script for running automated data quality validation on retail datasets."""

import argparse
import os
import sys
import pandas as pd
from src.validation.validator import DataQualityValidator

def load_table(directory: str, filename: str) -> pd.DataFrame:
    filepath = os.path.join(directory, filename)
    if not os.path.exists(filepath):
        print(f"Error: Missing required file: {filepath}", file=sys.stderr)
        sys.exit(1)
    return pd.read_csv(filepath)

def main():
    parser = argparse.ArgumentParser(description="Validate retail datasets.")
    parser.add_argument("--data-dir", type=str, default="data/cleaned", help="Path to data directory (e.g. data/raw or data/cleaned)")
    parser.add_argument("--report-file", type=str, default=None, help="Optional output path to write validation report file")
    args = parser.parse_args()

    print(f"Loading datasets from '{args.data_dir}'...")
    sales_df = load_table(args.data_dir, "Sales.csv")
    customers_df = load_table(args.data_dir, "Customers.csv")
    products_df = load_table(args.data_dir, "Products.csv")
    regions_df = load_table(args.data_dir, "Regions.csv")

    date_df = None
    date_path = os.path.join(args.data_dir, "Date.csv")
    if os.path.exists(date_path):
        date_df = pd.read_csv(date_path)

    print("Running data-quality validation rules...")
    validator = DataQualityValidator(
        sales_df=sales_df,
        customers_df=customers_df,
        products_df=products_df,
        regions_df=regions_df,
        date_df=date_df
    )

    report = validator.run_all_checks()
    report_text = report.to_readable_string()
    print("\n" + report_text)

    if args.report_file:
        os.makedirs(os.path.dirname(os.path.abspath(args.report_file)), exist_ok=True)
        with open(args.report_file, "w") as f:
            f.write(report_text)
        print(f"\nReport written to: {args.report_file}")

    if report.has_errors:
        print("\n❌ Validation finished with errors.", file=sys.stderr)
        sys.exit(1)
    else:
        print("\n✅ All validation rules passed successfully.")
        sys.exit(0)

if __name__ == "__main__":
    main()
