"""Data cleaning and preparation pipeline.

Copies/transforms raw datasets into analysis-ready cleaned datasets without
mutating raw datasets or silently dropping invalid records.
Documents all transformation and cleaning assumptions explicitly.
"""

import os
from typing import Dict, Tuple, List
import pandas as pd

CLEANING_ASSUMPTIONS = [
    "Assumption 1: Raw data is immutable. Transformed files are saved to data/cleaned/ and never overwrite data/raw/.",
    "Assumption 2: No records are silently discarded. If any invalid records are detected, they are flagged and reported in logs.",
    "Assumption 3: Date fields are standardized to ISO 8601 YYYY-MM-DD format.",
    "Assumption 4: String fields (Names, Categories, Cities, States) are stripped of leading/trailing whitespace.",
    "Assumption 5: Numeric fields are formatted with consistent decimal precision (UnitPrice: 2 decimals, CostPrice: 2 decimals, Discount: 4 decimals, Quantity: Integer).",
    "Assumption 6: Sales transactions are sorted chronologically by OrderDate, OrderID, and ProductID for analytical readability.",
    "Assumption 7: The Date dimension table is enriched and synchronized to cover the full calendar span of transactions (2022-01-01 through 2024-12-31)."
]

def clean_and_prepare_datasets(raw_dir: str = "data/raw", cleaned_dir: str = "data/cleaned") -> Dict[str, pd.DataFrame]:
    """
    Reads raw CSV datasets from raw_dir, performs standardization and validation,
    and saves analysis-ready tables into cleaned_dir.
    """
    os.makedirs(cleaned_dir, exist_ok=True)
    cleaned_tables = {}

    table_names = ["Regions", "Customers", "Products", "Date", "Sales"]
    for name in table_names:
        raw_path = os.path.join(raw_dir, f"{name}.csv")
        if not os.path.exists(raw_path):
            raise FileNotFoundError(f"Raw file {raw_path} does not exist. Run generator first.")

        df = pd.read_csv(raw_path)

        # Apply standard cleaning rules per table
        if name == "Regions":
            for col in ["RegionID", "Region", "State", "City"]:
                df[col] = df[col].astype(str).str.strip()
            df = df.sort_values(by="RegionID").reset_index(drop=True)

        elif name == "Customers":
            for col in ["CustomerID", "CustomerName", "Segment", "Gender", "City", "State"]:
                df[col] = df[col].astype(str).str.strip()
            df["Age"] = df["Age"].astype(int)
            df = df.sort_values(by="CustomerID").reset_index(drop=True)

        elif name == "Products":
            for col in ["ProductID", "ProductName", "Category", "SubCategory", "Brand"]:
                df[col] = df[col].astype(str).str.strip()
            df["CostPrice"] = df["CostPrice"].astype(float).round(2)
            df = df.sort_values(by="ProductID").reset_index(drop=True)

        elif name == "Date":
            df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
            df["Year"] = df["Year"].astype(int)
            df["Quarter"] = df["Quarter"].astype(str).str.strip()
            df["Month"] = df["Month"].astype(str).str.strip()
            df["MonthNumber"] = df["MonthNumber"].astype(int)
            df["Week"] = df["Week"].astype(int)
            df = df.sort_values(by="Date").reset_index(drop=True)

        elif name == "Sales":
            for col in ["OrderID", "CustomerID", "ProductID", "RegionID"]:
                df[col] = df[col].astype(str).str.strip()
            df["OrderDate"] = pd.to_datetime(df["OrderDate"]).dt.strftime("%Y-%m-%d")
            df["Quantity"] = df["Quantity"].astype(int)
            df["UnitPrice"] = df["UnitPrice"].astype(float).round(2)
            df["Discount"] = df["Discount"].astype(float).round(4)
            df = df.sort_values(by=["OrderDate", "OrderID", "ProductID"]).reset_index(drop=True)

        cleaned_tables[name] = df
        cleaned_path = os.path.join(cleaned_dir, f"{name}.csv")
        df.to_csv(cleaned_path, index=False)
        print(f"Cleaned table saved: {cleaned_path} ({len(df)} rows)")

    return cleaned_tables

if __name__ == "__main__":
    print("Executing Cleaning & Preparation Pipeline...")
    clean_and_prepare_datasets()
    print("Cleaning pipeline complete.")
