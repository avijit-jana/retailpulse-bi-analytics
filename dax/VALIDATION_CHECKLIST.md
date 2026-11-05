# DAX Validation Checklist for Power BI Desktop

> **Notice per AGENTS.md**: AI-generated DAX measures must not be assumed to be validated in Power BI Desktop automatically. Visual validation and formula verification must be formally executed inside Power BI Desktop. Use this checklist during model ingestion.

---

## 1. Prerequisites in Power BI Desktop
- [ ] **Data Model Schema**: Verify star-schema structure with 1-to-many single-direction relationships:
  - `Date[Date]` 1:* `Sales[OrderDate]`
  - `Customers[CustomerID]` 1:* `Sales[CustomerID]`
  - `Products[ProductID]` 1:* `Sales[ProductID]`
  - `Regions[RegionID]` 1:* `Sales[RegionID]`
- [ ] **Mark as Date Table**: Right-click `Date` table -> *Mark as Date Table* -> Select `Date[Date]` as primary key column.
- [ ] **Data Types**:
  - `Sales[Quantity]`: Whole Number
  - `Sales[UnitPrice]`: Fixed Decimal Number / Currency
  - `Sales[Discount]`: Decimal Number (Formatted as Percentage)
  - `Products[CostPrice]`: Fixed Decimal Number / Currency
  - `Date[Date]`: Date
  - `Sales[OrderDate]`: Date

---

## 2. Base Measures Validation (`dax/01_base_measures.dax`)
- [ ] **[Total Sales]**:
  - Add to a Card visual. Verify value matches sum of line net revenue (`Quantity * UnitPrice * (1 - Discount)`).
  - Test slice by `Products[Category]` and `Customers[Segment]`.
- [ ] **[Total Cost]**:
  - Verify `RELATED(Products[CostPrice])` works across active relationship `Sales[ProductID] -> Products[ProductID]`.
  - Add to Table visual alongside `[Total Sales]`.
- [ ] **[Total Profit]**:
  - Verify `[Total Profit] = [Total Sales] - [Total Cost]`.
- [ ] **[Profit Margin %]**:
  - Format measure as Percentage (`0.0%`).
  - Verify division by zero yields 0 instead of NaN / Infinity.
- [ ] **[Total Orders]** & **[Total Customers]**:
  - Verify distinct count logic matches expected order volume and customer counts.
- [ ] **[Average Order Value]**:
  - Verify `[Total Sales] / [Total Orders]` produces sensible average dollar value per order.

---

## 3. Time Intelligence Validation (`dax/02_time_intelligence.dax`)
- [ ] **[Previous Year Sales]**:
  - Place `Date[Year]`, `[Total Sales]`, and `[Previous Year Sales]` into a Matrix.
  - Verify 2022 `[Previous Year Sales]` is BLANK.
  - Verify 2023 `[Previous Year Sales]` matches 2022 `[Total Sales]`.
  - Verify 2024 `[Previous Year Sales]` matches 2023 `[Total Sales]`.
- [ ] **[YoY Sales Growth %]**:
  - Format measure as Percentage (`0.0%`).
  - Verify that when `[Previous Year Sales]` is blank, the growth % returns blank.
- [ ] **[Monthly Sales] & [Quarterly Sales]**:
  - Verify monthly trend lines and quarterly aggregates calculate correctly across filter selections.
- [ ] **[YTD Sales]**:
  - Verify cumulative accumulation resets at the start of each fiscal/calendar year.

---

## 4. Profitability, Contribution & Rankings Validation (`dax/03_profitability_and_rankings.dax`)
- [ ] **[Customer Contribution %]**:
  - Create table with `Customers[CustomerName]`, `[Total Sales]`, and `[Customer Contribution %]`.
  - Confirm sum of contribution equals 100% when no customer slicer is applied.
- [ ] **[Category Sales Contribution %]**:
  - Add Category bar chart. Confirm categories sum to 1.0 (100%).
- [ ] **[Top Product Rank by Sales] & [Top Product Rank by Profit]**:
  - Verify rankings evaluate dynamically without gaps (Dense ranking).
  - Test with Top N visual filters (e.g. Top 10 products by sales).

---

## 5. Review & Acceptance Sign-off
- Verified by: ___________________________________
- Date verified: _________________________________
- Power BI Desktop Version: ______________________
- Notes / Deviations: ____________________________
