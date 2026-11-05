"""Tests for synthetic data generation reproducibility, schema, and referential integrity."""

import pytest
import pandas as pd
from datetime import date
from src.data_generation.generator import generate_all_datasets
from src.data_generation.regions import generate_regions
from src.data_generation.customers import generate_customers
from src.data_generation.products import generate_products
from src.data_generation.dates import generate_dates
from src.data_generation.sales import generate_sales

def test_fixed_seed_reproducibility():
    """Verify that running generation with identical seed yields byte-for-byte identical dataframes."""
    res1 = generate_all_datasets(num_customers=50, num_orders=100, seed=12345)
    res2 = generate_all_datasets(num_customers=50, num_orders=100, seed=12345)

    for table_name in ["Regions", "Customers", "Products", "Date", "Sales"]:
        pd.testing.assert_frame_equal(res1[table_name], res2[table_name])

def test_different_seeds_produce_variation():
    """Verify that different seeds produce different customer names and order assignments."""
    res1 = generate_all_datasets(num_customers=50, num_orders=100, seed=111)
    res2 = generate_all_datasets(num_customers=50, num_orders=100, seed=999)

    assert not res1["Customers"]["CustomerName"].equals(res2["Customers"]["CustomerName"])

def test_date_dimension_coverage():
    """Verify Date dimension accurately spans expected range and schema."""
    start = date(2023, 1, 1)
    end = date(2023, 1, 31)
    df_date = generate_dates(start, end)
    assert len(df_date) == 31
    assert set(df_date.columns) == {"Date", "Year", "Quarter", "Month", "MonthNumber", "Week"}
    assert df_date["Date"].iloc[0] == "2023-01-01"
    assert df_date["Date"].iloc[-1] == "2023-01-31"

def test_sales_referential_integrity():
    """Verify that all foreign keys in Sales reference existing records in dimension tables."""
    datasets = generate_all_datasets(num_customers=50, num_orders=100, seed=42)
    sales = datasets["Sales"]
    cust = datasets["Customers"]
    prod = datasets["Products"]
    reg = datasets["Regions"]

    assert sales["CustomerID"].isin(set(cust["CustomerID"])).all()
    assert sales["ProductID"].isin(set(prod["ProductID"])).all()
    assert sales["RegionID"].isin(set(reg["RegionID"])).all()
