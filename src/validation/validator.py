"""Data-Quality Validation Engine for RetailPulse BI Analytics.

Validates datasets against:
- Primary key uniqueness
- Foreign key referential integrity
- Null and missing values
- Duplicate transactions
- Invalid dates and date range alignment
- Negative and zero quantities
- Invalid discounts (< 0 or > 1)
- Invalid prices and costs (<= 0)
- Unexpected categories and segments

Produces a detailed, human-readable data-quality report.
Does NOT silently delete invalid records; flags and reports every issue.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
import pandas as pd
from src.config import CUSTOMER_SEGMENTS

@dataclass
class ValidationIssue:
    severity: str  # "ERROR" or "WARNING"
    table: str
    column: Optional[str]
    check_name: str
    message: str
    count: int = 1

@dataclass
class ValidationReport:
    timestamp: str
    tables_checked: List[str]
    issues: List[ValidationIssue] = field(default_factory=list)
    total_checks: int = 0
    passed_checks: int = 0

    @property
    def has_errors(self) -> bool:
        return any(issue.severity == "ERROR" for issue in self.issues)

    def to_readable_string(self) -> str:
        lines = []
        lines.append("=" * 80)
        lines.append("RETAILPULSE BI ANALYTICS — DATA-QUALITY VALIDATION REPORT")
        lines.append("=" * 80)
        lines.append(f"Execution Timestamp : {self.timestamp}")
        lines.append(f"Tables Checked      : {', '.join(self.tables_checked)}")
        lines.append(f"Total Rules Checked : {self.total_checks}")
        lines.append(f"Passed Checks       : {self.passed_checks}")
        lines.append(f"Failed Checks / Issues Found : {len(self.issues)}")
        lines.append(f"Overall Status      : {'FAILED ❌' if self.has_errors else 'PASSED ✅'}")
        lines.append("-" * 80)

        if not self.issues:
            lines.append("No issues found! All data-quality constraints passed successfully.")
        else:
            lines.append(f"{'SEVERITY':<10} | {'TABLE':<12} | {'COLUMN':<14} | {'CHECK NAME':<25} | {'DETAILS'}")
            lines.append("-" * 80)
            for issue in self.issues:
                col = issue.column or "-"
                lines.append(f"{issue.severity:<10} | {issue.table:<12} | {col:<14} | {issue.check_name:<25} | {issue.message} (Count: {issue.count})")

        lines.append("=" * 80)
        return "\n".join(lines)


class DataQualityValidator:
    """Validator class to evaluate retail dataframes against business & relational constraints."""

    def __init__(
        self,
        sales_df: pd.DataFrame,
        customers_df: pd.DataFrame,
        products_df: pd.DataFrame,
        regions_df: pd.DataFrame,
        date_df: Optional[pd.DataFrame] = None
    ):
        self.sales = sales_df.copy()
        self.customers = customers_df.copy()
        self.products = products_df.copy()
        self.regions = regions_df.copy()
        self.date = date_df.copy() if date_df is not None else None
        self.issues: List[ValidationIssue] = []
        self.total_checks = 0
        self.passed_checks = 0

    def _record_check(self, passed: bool, issue: Optional[ValidationIssue] = None):
        self.total_checks += 1
        if passed:
            self.passed_checks += 1
        elif issue:
            self.issues.append(issue)

    def validate_null_values(self):
        """Check 1: Ensure no unexpected missing or null values in mandatory fields."""
        tables = {
            "Sales": (self.sales, ["OrderID", "OrderDate", "CustomerID", "ProductID", "RegionID", "Quantity", "UnitPrice", "Discount"]),
            "Customers": (self.customers, ["CustomerID", "CustomerName", "Segment", "Age", "Gender", "City", "State"]),
            "Products": (self.products, ["ProductID", "ProductName", "Category", "SubCategory", "Brand", "CostPrice"]),
            "Regions": (self.regions, ["RegionID", "Region", "State", "City"]),
        }
        if self.date is not None:
            tables["Date"] = (self.date, ["Date", "Year", "Quarter", "Month", "MonthNumber", "Week"])

        for tbl_name, (df, cols) in tables.items():
            for col in cols:
                if col not in df.columns:
                    self._record_check(False, ValidationIssue(
                        severity="ERROR",
                        table=tbl_name,
                        column=col,
                        check_name="Missing Column",
                        message=f"Mandatory column '{col}' is missing from table '{tbl_name}'"
                    ))
                    continue

                null_count = int(df[col].isnull().sum())
                if null_count > 0:
                    self._record_check(False, ValidationIssue(
                        severity="ERROR",
                        table=tbl_name,
                        column=col,
                        check_name="Null Values",
                        message=f"Column has {null_count} null/missing values",
                        count=null_count
                    ))
                else:
                    self._record_check(True)

    def validate_primary_keys(self):
        """Check 2: Ensure primary keys in dimension tables are strictly unique and non-null."""
        pk_configs = [
            ("Regions", self.regions, "RegionID"),
            ("Customers", self.customers, "CustomerID"),
            ("Products", self.products, "ProductID"),
        ]
        if self.date is not None:
            pk_configs.append(("Date", self.date, "Date"))

        for tbl_name, df, pk_col in pk_configs:
            if pk_col not in df.columns:
                continue
            dups = int(df[pk_col].duplicated().sum())
            if dups > 0:
                self._record_check(False, ValidationIssue(
                    severity="ERROR",
                    table=tbl_name,
                    column=pk_col,
                    check_name="Primary Key Duplicate",
                    message=f"Primary key '{pk_col}' has {dups} duplicate entries",
                    count=dups
                ))
            else:
                self._record_check(True)

    def validate_duplicate_transactions(self):
        """Check 3: Check for exact duplicate order line items (OrderID + ProductID)."""
        if "OrderID" in self.sales.columns and "ProductID" in self.sales.columns:
            dups = int(self.sales.duplicated(subset=["OrderID", "ProductID"]).sum())
            if dups > 0:
                self._record_check(False, ValidationIssue(
                    severity="ERROR",
                    table="Sales",
                    column="OrderID,ProductID",
                    check_name="Duplicate Transaction",
                    message=f"Found {dups} duplicate order lines with identical OrderID and ProductID",
                    count=dups
                ))
            else:
                self._record_check(True)

    def validate_foreign_keys(self):
        """Check 4: Foreign Key Referential Integrity."""
        # 4a. CustomerID in Sales exists in Customers
        if "CustomerID" in self.sales.columns and "CustomerID" in self.customers.columns:
            valid_customers = set(self.customers["CustomerID"])
            orphan_cust = ~self.sales["CustomerID"].isin(valid_customers)
            orphan_count = int(orphan_cust.sum())
            if orphan_count > 0:
                self._record_check(False, ValidationIssue(
                    severity="ERROR",
                    table="Sales",
                    column="CustomerID",
                    check_name="FK Integrity",
                    message=f"Found {orphan_count} sales records referencing non-existent CustomerIDs",
                    count=orphan_count
                ))
            else:
                self._record_check(True)

        # 4b. ProductID in Sales exists in Products
        if "ProductID" in self.sales.columns and "ProductID" in self.products.columns:
            valid_prods = set(self.products["ProductID"])
            orphan_prod = ~self.sales["ProductID"].isin(valid_prods)
            orphan_count = int(orphan_prod.sum())
            if orphan_count > 0:
                self._record_check(False, ValidationIssue(
                    severity="ERROR",
                    table="Sales",
                    column="ProductID",
                    check_name="FK Integrity",
                    message=f"Found {orphan_count} sales records referencing non-existent ProductIDs",
                    count=orphan_count
                ))
            else:
                self._record_check(True)

        # 4c. RegionID in Sales exists in Regions
        if "RegionID" in self.sales.columns and "RegionID" in self.regions.columns:
            valid_regs = set(self.regions["RegionID"])
            orphan_reg = ~self.sales["RegionID"].isin(valid_regs)
            orphan_count = int(orphan_reg.sum())
            if orphan_count > 0:
                self._record_check(False, ValidationIssue(
                    severity="ERROR",
                    table="Sales",
                    column="RegionID",
                    check_name="FK Integrity",
                    message=f"Found {orphan_count} sales records referencing non-existent RegionIDs",
                    count=orphan_count
                ))
            else:
                self._record_check(True)

        # 4d. OrderDate in Sales exists in Date table
        if self.date is not None and "OrderDate" in self.sales.columns and "Date" in self.date.columns:
            valid_dates = set(pd.to_datetime(self.date["Date"]).dt.strftime("%Y-%m-%d"))
            sales_dates = pd.to_datetime(self.sales["OrderDate"], errors="coerce").dt.strftime("%Y-%m-%d")
            orphan_dates = ~sales_dates.isin(valid_dates)
            orphan_count = int(orphan_dates.sum())
            if orphan_count > 0:
                self._record_check(False, ValidationIssue(
                    severity="ERROR",
                    table="Sales",
                    column="OrderDate",
                    check_name="FK Integrity (Date)",
                    message=f"Found {orphan_count} sales dates outside the calendar date dimension",
                    count=orphan_count
                ))
            else:
                self._record_check(True)

    def validate_dates(self):
        """Check 5: Date format and logical validation."""
        if "OrderDate" in self.sales.columns:
            parsed = pd.to_datetime(self.sales["OrderDate"], errors="coerce")
            invalid_dates_count = int(parsed.isna().sum())
            if invalid_dates_count > 0:
                self._record_check(False, ValidationIssue(
                    severity="ERROR",
                    table="Sales",
                    column="OrderDate",
                    check_name="Invalid Date Format",
                    message=f"Found {invalid_dates_count} unparseable or corrupted date values",
                    count=invalid_dates_count
                ))
            else:
                self._record_check(True)

    def validate_numeric_bounds(self):
        """Check 6, 7, 8: Quantities, Discounts, Prices, and Costs."""
        # 6. Quantities > 0
        if "Quantity" in self.sales.columns:
            qty_numeric = pd.to_numeric(self.sales["Quantity"], errors="coerce")
            invalid_qty = (qty_numeric <= 0) | qty_numeric.isna()
            inv_count = int(invalid_qty.sum())
            if inv_count > 0:
                self._record_check(False, ValidationIssue(
                    severity="ERROR",
                    table="Sales",
                    column="Quantity",
                    check_name="Negative/Zero Quantity",
                    message=f"Found {inv_count} records with non-positive or non-numeric Quantity",
                    count=inv_count
                ))
            else:
                self._record_check(True)

        # 7. Discount bounds: 0.0 <= Discount < 1.0 (retail items cannot be 100% free or negative)
        if "Discount" in self.sales.columns:
            disc_numeric = pd.to_numeric(self.sales["Discount"], errors="coerce")
            invalid_disc = (disc_numeric < 0.0) | (disc_numeric >= 1.0) | disc_numeric.isna()
            inv_count = int(invalid_disc.sum())
            if inv_count > 0:
                self._record_check(False, ValidationIssue(
                    severity="ERROR",
                    table="Sales",
                    column="Discount",
                    check_name="Invalid Discount",
                    message=f"Found {inv_count} records with Discount outside allowed range [0.0, 1.0)",
                    count=inv_count
                ))
            else:
                self._record_check(True)

        # 8a. UnitPrice > 0
        if "UnitPrice" in self.sales.columns:
            price_numeric = pd.to_numeric(self.sales["UnitPrice"], errors="coerce")
            invalid_price = (price_numeric <= 0.0) | price_numeric.isna()
            inv_count = int(invalid_price.sum())
            if inv_count > 0:
                self._record_check(False, ValidationIssue(
                    severity="ERROR",
                    table="Sales",
                    column="UnitPrice",
                    check_name="Invalid UnitPrice",
                    message=f"Found {inv_count} records with non-positive UnitPrice",
                    count=inv_count
                ))
            else:
                self._record_check(True)

        # 8b. CostPrice > 0
        if "CostPrice" in self.products.columns:
            cost_numeric = pd.to_numeric(self.products["CostPrice"], errors="coerce")
            invalid_cost = (cost_numeric <= 0.0) | cost_numeric.isna()
            inv_count = int(invalid_cost.sum())
            if inv_count > 0:
                self._record_check(False, ValidationIssue(
                    severity="ERROR",
                    table="Products",
                    column="CostPrice",
                    check_name="Invalid CostPrice",
                    message=f"Found {inv_count} products with non-positive CostPrice",
                    count=inv_count
                ))
            else:
                self._record_check(True)

    def validate_categories_and_segments(self):
        """Check 9: Verify Customer Segments and Product Categories match expected allowed values."""
        # 9a. Segments
        if "Segment" in self.customers.columns:
            allowed_segments = set(CUSTOMER_SEGMENTS)
            invalid_segments = ~self.customers["Segment"].isin(allowed_segments)
            inv_count = int(invalid_segments.sum())
            if inv_count > 0:
                self._record_check(False, ValidationIssue(
                    severity="ERROR",
                    table="Customers",
                    column="Segment",
                    check_name="Unexpected Segment",
                    message=f"Found {inv_count} records with unexpected customer segment value",
                    count=inv_count
                ))
            else:
                self._record_check(True)

        # 9b. Categories
        if "Category" in self.products.columns:
            allowed_categories = {"Technology", "Furniture", "Office Supplies"}
            invalid_cat = ~self.products["Category"].isin(allowed_categories)
            inv_count = int(invalid_cat.sum())
            if inv_count > 0:
                self._record_check(False, ValidationIssue(
                    severity="ERROR",
                    table="Products",
                    column="Category",
                    check_name="Unexpected Category",
                    message=f"Found {inv_count} records with unexpected product category",
                    count=inv_count
                ))
            else:
                self._record_check(True)

    def run_all_checks(self) -> ValidationReport:
        """Runs the complete battery of data quality checks."""
        self.validate_null_values()
        self.validate_primary_keys()
        self.validate_duplicate_transactions()
        self.validate_foreign_keys()
        self.validate_dates()
        self.validate_numeric_bounds()
        self.validate_categories_and_segments()

        tables = ["Sales", "Customers", "Products", "Regions"]
        if self.date is not None:
            tables.append("Date")

        return ValidationReport(
            timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
            tables_checked=tables,
            issues=self.issues,
            total_checks=self.total_checks,
            passed_checks=self.passed_checks
        )
