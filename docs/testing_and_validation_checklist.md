# Comprehensive Testing & Validation Checklist — RetailPulse BI Analytics

This document establishes the end-to-end quality assurance and verification gate for RetailPulse BI Analytics.
It clearly distinguishes between **Automated Python Testing** (fully executed in this repository) and **Power BI Desktop Verification** (to be performed when opening the report in Power BI Desktop).

> **Verification Governance Notice**:
> In compliance with `AGENTS.md`, AI agents do not invent real business results or claim that Power BI Desktop visuals have been tested unless formal Power BI Desktop execution evidence exists.

---

## Part 1: Automated Python Data & Code Validation (Completed & Passing)

The automated test suite runs via `pytest -v` and tests against both synthetic raw and cleaned datasets.

### Automated Test Matrix
- [x] **Seed Determinism (`tests/test_generator.py::test_fixed_seed_reproducibility`)**:
  - Confirms running generator with seed 42 produces identical dataframes across all 5 tables.
- [x] **Seed Variation (`tests/test_generator.py::test_different_seeds_produce_variation`)**:
  - Confirms altering random seeds produces statistically distinct variations.
- [x] **Date Dimension Bounds (`tests/test_generator.py::test_date_dimension_coverage`)**:
  - Confirms contiguous daily calendar coverage spanning 2022-01-01 to 2024-12-31 without gaps.
- [x] **Foreign Key Referential Integrity (`tests/test_generator.py::test_sales_referential_integrity`)**:
  - Confirms 100% of foreign keys in `Sales` map directly to `Customers`, `Products`, and `Regions`.
- [x] **Baseline Dataset Quality (`tests/test_validation.py::test_clean_data_passes_all_checks`)**:
  - Confirms generated dataset clears all 47 checks with 0 errors.
- [x] **Primary Key Duplicate Detection (`tests/test_validation.py::test_detects_primary_key_duplicates`)**:
  - Confirms injected duplicates in PK fields trigger explicit `ERROR`.
- [x] **Foreign Key Orphan Detection (`tests/test_validation.py::test_detects_foreign_key_violation`)**:
  - Confirms orphaned foreign keys in transactions trigger explicit `ERROR`.
- [x] **Null Value Detection (`tests/test_validation.py::test_detects_null_values`)**:
  - Confirms nulls in mandatory columns trigger explicit `ERROR`.
- [x] **Duplicate Transaction Detection (`tests/test_validation.py::test_detects_duplicate_transactions`)**:
  - Confirms identical `OrderID` + `ProductID` duplicates trigger explicit `ERROR`.
- [x] **Invalid Date Detection (`tests/test_validation.py::test_detects_invalid_dates`)**:
  - Confirms corrupted or unparseable dates trigger explicit `ERROR`.
- [x] **Negative Quantity Detection (`tests/test_validation.py::test_detects_negative_or_zero_quantity`)**:
  - Confirms non-positive quantities (`<= 0`) trigger explicit `ERROR`.
- [x] **Invalid Discount Detection (`tests/test_validation.py::test_detects_invalid_discounts`)**:
  - Confirms discounts `< 0` or `>= 1` trigger explicit `ERROR`.
- [x] **Invalid Price & Cost Detection (`tests/test_validation.py::test_detects_invalid_prices_and_costs`)**:
  - Confirms prices or costs `<= 0` trigger explicit `ERROR`.
- [x] **Unexpected Domain Values (`tests/test_validation.py::test_detects_unexpected_categories_and_segments`)**:
  - Confirms rogue categories or customer segments trigger explicit `ERROR`.
- [x] **Readable Report String Formatting (`tests/test_validation.py::test_report_readable_string_output`)**:
  - Confirms the report formats as a readable audit table.

---

## Part 2: Power BI Desktop Ingestion & Visual Checklist (For Desktop Developer)

This section must be completed by the developer inside Power BI Desktop.

### 1. Data Connection & ETL Gate
- [ ] Connected to `data/cleaned/` CSVs (Sales, Customers, Products, Regions, Date).
- [ ] No type casting errors or truncated rows in Power Query.
- [ ] Currency, date, and whole number column types set correctly.

### 2. Relational Model Gate
- [ ] Star schema modeled with 4 single-directional 1-to-many relationships pointing to `Sales`.
- [ ] No bidirectional relationships or circular dependencies.
- [ ] `Date` table marked as official Date Table.
- [ ] `Date[Month]` sorted by `Date[MonthNumber]`.

### 3. DAX Metric Accuracy Gate
- [ ] Card visual with `[Total Sales]` matches total net revenue from cleaned data.
- [ ] Card visual with `[Total Cost]` matches line quantity multiplied by related cost price.
- [ ] `[Total Profit]` equals `[Total Sales] - [Total Cost]`.
- [ ] `[Profit Margin %]` renders with 1 decimal percentage (`XX.X%`).
- [ ] Matrix with `Date[Year]` confirms `[Previous Year Sales]` is blank for 2022 and accurately shifts 2022/2023 sales into 2023/2024.
- [ ] Top Product Ranks evaluate dense rankings dynamically under slicer selections.

### 4. Five-Page Report Validation Gate
- [ ] **Page 1 (Executive Overview)**: Renders all 6 KPI cards, monthly trend chart, category donut, regional bars.
- [ ] **Page 2 (Sales Analysis)**: Scatter plot renders discount vs sales; monthly regional stacked column functions.
- [ ] **Page 3 (Customer Analysis)**: Segment matrix shows Consumer/Corporate/Home Office metrics; top 25 customer table populated.
- [ ] **Page 4 (Product Analysis)**: Hierarchy drilldown functions smoothly across Category -> SubCategory -> Product.
- [ ] **Page 5 (Management Insights)**: Margin leakage table highlights discounted low-margin transactions.

### 5. Final Sign-off Evidence
- Status: **Pending manual Power BI Desktop execution**
- Power BI Desktop Version: ______________________
- Tested by: _____________________________________
- Date: __________________________________________
