"""Main orchestrator for generating synthetic retail datasets."""

import argparse
import os
import sys
from datetime import date
from typing import Dict
import pandas as pd

from src.config import (
    DEFAULT_RANDOM_SEED,
    DEFAULT_START_DATE,
    DEFAULT_END_DATE,
    DEFAULT_NUM_CUSTOMERS,
    DEFAULT_NUM_ORDERS,
)
from src.data_generation.regions import generate_regions
from src.data_generation.customers import generate_customers
from src.data_generation.products import generate_products
from src.data_generation.dates import generate_dates
from src.data_generation.sales import generate_sales

def generate_all_datasets(
    num_customers: int = DEFAULT_NUM_CUSTOMERS,
    num_orders: int = DEFAULT_NUM_ORDERS,
    start_date: date = DEFAULT_START_DATE,
    end_date: date = DEFAULT_END_DATE,
    seed: int = DEFAULT_RANDOM_SEED
) -> Dict[str, pd.DataFrame]:
    """
    Generates all core retail datasets with strict referential integrity.
    Returns dictionary with keys: 'regions', 'customers', 'products', 'dates', 'sales'
    """
    print(f"Generating synthetic retail datasets with seed={seed}...")

    # 1. Regions
    regions_df = generate_regions()
    print(f"  Generated Regions: {len(regions_df)} records")

    # 2. Customers
    customers_df = generate_customers(num_customers=num_customers, regions_df=regions_df, seed=seed)
    print(f"  Generated Customers: {len(customers_df)} records")

    # 3. Products
    products_df = generate_products(seed=seed)
    print(f"  Generated Products: {len(products_df)} records")

    # 4. Dates
    dates_df = generate_dates(start_date=start_date, end_date=end_date)
    print(f"  Generated Date dimension: {len(dates_df)} days ({start_date} to {end_date})")

    # 5. Sales
    sales_df = generate_sales(
        num_orders=num_orders,
        customers_df=customers_df,
        products_df=products_df,
        regions_df=regions_df,
        start_date=start_date,
        end_date=end_date,
        seed=seed
    )
    print(f"  Generated Sales: {len(sales_df)} transaction line items across {num_orders} orders")

    return {
        "Regions": regions_df,
        "Customers": customers_df,
        "Products": products_df,
        "Date": dates_df,
        "Sales": sales_df
    }

def save_datasets(datasets: Dict[str, pd.DataFrame], output_dir: str):
    """Saves dataframes to CSV in target directory."""
    os.makedirs(output_dir, exist_ok=True)
    for name, df in datasets.items():
        filepath = os.path.join(output_dir, f"{name}.csv")
        df.to_csv(filepath, index=False)
        print(f"  Saved {name}.csv ({len(df)} rows) -> {filepath}")

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic retail dataset.")
    parser.add_argument("--customers", type=int, default=DEFAULT_NUM_CUSTOMERS, help="Number of customers")
    parser.add_argument("--orders", type=int, default=DEFAULT_NUM_ORDERS, help="Number of orders")
    parser.add_argument("--seed", type=int, default=DEFAULT_RANDOM_SEED, help="Random seed for reproducibility")
    parser.add_argument("--output-dir", type=str, default="data/raw", help="Target directory for raw data")
    args = parser.parse_args()

    datasets = generate_all_datasets(
        num_customers=args.customers,
        num_orders=args.orders,
        seed=args.seed
    )
    save_datasets(datasets, args.output_dir)
    print("\nGeneration successfully completed.")

if __name__ == "__main__":
    main()
