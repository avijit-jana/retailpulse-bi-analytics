"""Tests for the comprehensive data-quality validation module.

Covers:
- Primary key uniqueness
- Foreign key integrity
- Null and missing values
- Duplicate transactions
- Invalid dates
- Negative and zero quantities
- Invalid discounts (< 0 or >= 1)
- Invalid prices and costs (<= 0)
- Unexpected categories and segments
- Non-silent failure reporting
"""

import pytest
import pandas as pd
from src.data_generation.generator import generate_all_datasets
from src.validation.validator import DataQualityValidator

@pytest.fixture
def valid_dataset():
    """Generates a small valid dataset for testing."""
    return generate_all_datasets(num_customers=50, num_orders=100, seed=42)

def test_clean_data_passes_all_checks(valid_dataset):
    """Clean generated data should have 0 errors."""
    validator = DataQualityValidator(
        sales_df=valid_dataset["Sales"],
        customers_df=valid_dataset["Customers"],
        products_df=valid_dataset["Products"],
        regions_df=valid_dataset["Regions"],
        date_df=valid_dataset["Date"]
    )
    report = validator.run_all_checks()
    assert not report.has_errors
    assert len(report.issues) == 0
    assert report.total_checks > 0
    assert report.passed_checks == report.total_checks

def test_detects_primary_key_duplicates(valid_dataset):
    """Detects duplicate primary key in dimension tables."""
    cust_df = valid_dataset["Customers"].copy()
    # Duplicate first row's CustomerID into second row
    cust_df.loc[1, "CustomerID"] = cust_df.loc[0, "CustomerID"]

    validator = DataQualityValidator(
        sales_df=valid_dataset["Sales"],
        customers_df=cust_df,
        products_df=valid_dataset["Products"],
        regions_df=valid_dataset["Regions"]
    )
    report = validator.run_all_checks()
    assert report.has_errors
    pk_issues = [i for i in report.issues if i.check_name == "Primary Key Duplicate"]
    assert len(pk_issues) == 1
    assert pk_issues[0].table == "Customers"
    assert pk_issues[0].column == "CustomerID"

def test_detects_foreign_key_violation(valid_dataset):
    """Detects invalid foreign keys in Sales."""
    sales_df = valid_dataset["Sales"].copy()
    # Point first record to non-existent CustomerID
    sales_df.loc[0, "CustomerID"] = "CUST-99999"

    validator = DataQualityValidator(
        sales_df=sales_df,
        customers_df=valid_dataset["Customers"],
        products_df=valid_dataset["Products"],
        regions_df=valid_dataset["Regions"]
    )
    report = validator.run_all_checks()
    assert report.has_errors
    fk_issues = [i for i in report.issues if i.check_name == "FK Integrity" and i.column == "CustomerID"]
    assert len(fk_issues) == 1
    assert fk_issues[0].count == 1

def test_detects_null_values(valid_dataset):
    """Detects null values in mandatory fields."""
    prod_df = valid_dataset["Products"].copy()
    prod_df.loc[0, "CostPrice"] = None

    validator = DataQualityValidator(
        sales_df=valid_dataset["Sales"],
        customers_df=valid_dataset["Customers"],
        products_df=prod_df,
        regions_df=valid_dataset["Regions"]
    )
    report = validator.run_all_checks()
    assert report.has_errors
    null_issues = [i for i in report.issues if i.check_name == "Null Values" and i.column == "CostPrice"]
    assert len(null_issues) == 1

def test_detects_duplicate_transactions(valid_dataset):
    """Detects duplicate transactions with identical OrderID and ProductID."""
    sales_df = valid_dataset["Sales"].copy()
    # Append the first row again
    duplicate_row = sales_df.iloc[[0]]
    sales_df = pd.concat([sales_df, duplicate_row], ignore_index=True)

    validator = DataQualityValidator(
        sales_df=sales_df,
        customers_df=valid_dataset["Customers"],
        products_df=valid_dataset["Products"],
        regions_df=valid_dataset["Regions"]
    )
    report = validator.run_all_checks()
    assert report.has_errors
    dup_issues = [i for i in report.issues if i.check_name == "Duplicate Transaction"]
    assert len(dup_issues) == 1

def test_detects_invalid_dates(valid_dataset):
    """Detects invalid or corrupted date values."""
    sales_df = valid_dataset["Sales"].copy()
    sales_df.loc[0, "OrderDate"] = "not-a-valid-date"

    validator = DataQualityValidator(
        sales_df=sales_df,
        customers_df=valid_dataset["Customers"],
        products_df=valid_dataset["Products"],
        regions_df=valid_dataset["Regions"]
    )
    report = validator.run_all_checks()
    assert report.has_errors
    date_issues = [i for i in report.issues if i.check_name == "Invalid Date Format"]
    assert len(date_issues) == 1

def test_detects_negative_or_zero_quantity(valid_dataset):
    """Detects negative or zero quantities."""
    sales_df = valid_dataset["Sales"].copy()
    sales_df.loc[0, "Quantity"] = 0
    sales_df.loc[1, "Quantity"] = -5

    validator = DataQualityValidator(
        sales_df=sales_df,
        customers_df=valid_dataset["Customers"],
        products_df=valid_dataset["Products"],
        regions_df=valid_dataset["Regions"]
    )
    report = validator.run_all_checks()
    assert report.has_errors
    qty_issues = [i for i in report.issues if i.check_name == "Negative/Zero Quantity"]
    assert len(qty_issues) == 1
    assert qty_issues[0].count == 2

def test_detects_invalid_discounts(valid_dataset):
    """Detects discounts < 0 or >= 1."""
    sales_df = valid_dataset["Sales"].copy()
    sales_df.loc[0, "Discount"] = -0.10
    sales_df.loc[1, "Discount"] = 1.05

    validator = DataQualityValidator(
        sales_df=sales_df,
        customers_df=valid_dataset["Customers"],
        products_df=valid_dataset["Products"],
        regions_df=valid_dataset["Regions"]
    )
    report = validator.run_all_checks()
    assert report.has_errors
    disc_issues = [i for i in report.issues if i.check_name == "Invalid Discount"]
    assert len(disc_issues) == 1
    assert disc_issues[0].count == 2

def test_detects_invalid_prices_and_costs(valid_dataset):
    """Detects prices or costs <= 0."""
    sales_df = valid_dataset["Sales"].copy()
    sales_df.loc[0, "UnitPrice"] = -25.0
    prod_df = valid_dataset["Products"].copy()
    prod_df.loc[0, "CostPrice"] = 0.0

    validator = DataQualityValidator(
        sales_df=sales_df,
        customers_df=valid_dataset["Customers"],
        products_df=prod_df,
        regions_df=valid_dataset["Regions"]
    )
    report = validator.run_all_checks()
    assert report.has_errors
    price_issues = [i for i in report.issues if i.check_name == "Invalid UnitPrice"]
    cost_issues = [i for i in report.issues if i.check_name == "Invalid CostPrice"]
    assert len(price_issues) == 1
    assert len(cost_issues) == 1

def test_detects_unexpected_categories_and_segments(valid_dataset):
    """Detects unknown categories or customer segments."""
    cust_df = valid_dataset["Customers"].copy()
    cust_df.loc[0, "Segment"] = "VIP_Special_Segment"
    prod_df = valid_dataset["Products"].copy()
    prod_df.loc[0, "Category"] = "Automotive"

    validator = DataQualityValidator(
        sales_df=valid_dataset["Sales"],
        customers_df=cust_df,
        products_df=prod_df,
        regions_df=valid_dataset["Regions"]
    )
    report = validator.run_all_checks()
    assert report.has_errors
    seg_issues = [i for i in report.issues if i.check_name == "Unexpected Segment"]
    cat_issues = [i for i in report.issues if i.check_name == "Unexpected Category"]
    assert len(seg_issues) == 1
    assert len(cat_issues) == 1

def test_report_readable_string_output(valid_dataset):
    """Validates human-readable formatting of the report."""
    validator = DataQualityValidator(
        sales_df=valid_dataset["Sales"],
        customers_df=valid_dataset["Customers"],
        products_df=valid_dataset["Products"],
        regions_df=valid_dataset["Regions"]
    )
    report = validator.run_all_checks()
    report_text = report.to_readable_string()
    assert "DATA-QUALITY VALIDATION REPORT" in report_text
    assert "PASSED ✅" in report_text
