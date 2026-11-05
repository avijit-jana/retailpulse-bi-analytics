# Data-Quality Report Template & Execution Guide

This document defines the standardized data-quality reporting template and verification procedures used across RetailPulse BI Analytics.

The automated validation tool can write directly to this format using:
```bash
python3 -m src.validation.validate_data --data-dir data/cleaned --report-file docs/latest_data_quality_report.txt
```

---

## 1. Data-Quality Report Format

```text
================================================================================
RETAILPULSE BI ANALYTICS — DATA-QUALITY VALIDATION REPORT
================================================================================
Execution Timestamp : [YYYY-MM-DD HH:MM:SS UTC]
Target Directory    : [e.g., data/cleaned or data/raw]
Environment / Host  : [Python Version / Execution Environment]
Tables Checked      : Sales, Customers, Products, Regions, Date
Total Rules Checked : [Integer count of individual column/table assertions]
Passed Checks       : [Integer count of successful assertions]
Failed Checks / Issues Found : [Integer count of failed assertions]
Overall Status      : [PASSED ✅ / FAILED ❌]
--------------------------------------------------------------------------------

[If Passed]:
No issues found! All data-quality constraints passed successfully.

[If Failed]:
SEVERITY   | TABLE        | COLUMN         | CHECK NAME                | DETAILS
--------------------------------------------------------------------------------
ERROR      | Sales        | CustomerID     | FK Integrity              | Found 1 sales records referencing non-existent CustomerIDs (Count: 1)
ERROR      | Products     | CostPrice      | Null Values               | Column has 1 null/missing values (Count: 1)
ERROR      | Sales        | Discount       | Invalid Discount          | Found 2 records with Discount outside allowed range [0.0, 1.0) (Count: 2)
================================================================================
```

---

## 2. Standardized Audit Checklist

| Check Category | Target Table | Target Column(s) | Business Rule / Assertion | Severity |
| :--- | :--- | :--- | :--- | :--- |
| **PK Uniqueness** | `Customers` | `CustomerID` | Must be strictly unique across all rows. | `ERROR` |
| **PK Uniqueness** | `Products` | `ProductID` | Must be strictly unique across all rows. | `ERROR` |
| **PK Uniqueness** | `Regions` | `RegionID` | Must be strictly unique across all rows. | `ERROR` |
| **PK Uniqueness** | `Date` | `Date` | Must be strictly contiguous, unique dates. | `ERROR` |
| **FK Integrity** | `Sales` | `CustomerID` | Must match a valid `CustomerID` in `Customers`. | `ERROR` |
| **FK Integrity** | `Sales` | `ProductID` | Must match a valid `ProductID` in `Products`. | `ERROR` |
| **FK Integrity** | `Sales` | `RegionID` | Must match a valid `RegionID` in `Regions`. | `ERROR` |
| **FK Integrity** | `Sales` | `OrderDate` | Must match an existing date in `Date` table. | `ERROR` |
| **Completeness** | All Tables | All Mandatory Columns | 0% null or NaN values allowed. | `ERROR` |
| **Deduplication**| `Sales` | `OrderID`, `ProductID` | No duplicate product lines within the same order. | `ERROR` |
| **Date Validity**| `Sales` | `OrderDate` | Must parse to ISO 8601 `YYYY-MM-DD` between 2022-01-01 and 2024-12-31. | `ERROR` |
| **Quantity** | `Sales` | `Quantity` | Must be integer >= 1. Negative or zero quantities strictly forbidden. | `ERROR` |
| **Discount** | `Sales` | `Discount` | Must be decimal in range `[0.00, 1.00)`. | `ERROR` |
| **Price** | `Sales` | `UnitPrice` | Must be numeric > 0.00. | `ERROR` |
| **Cost** | `Products` | `CostPrice` | Must be numeric > 0.00. | `ERROR` |
| **Domain Integrity** | `Customers` | `Segment` | Must belong to: `{'Consumer', 'Corporate', 'Home Office'}`. | `ERROR` |
| **Domain Integrity** | `Products` | `Category` | Must belong to: `{'Technology', 'Furniture', 'Office Supplies'}`. | `ERROR` |

---

## 3. Policy on Handling Quality Issues
In accordance with `AGENTS.md` and repository standards:
1. **Never Silently Discard Data**: The validator outputs every offending row count, table, and column. Records are never dropped in the background.
2. **Raw Immutability**: Faulty raw files must never be directly overwritten. Root-cause issues must be remediated in the generator configuration or transformation logic.
3. **Automated CI/CD Barrier**: A non-zero exit code is triggered on any `ERROR`, blocking deployment until data integrity is restored.
