# DAX Measure Documentation — RetailPulse BI Analytics

> **Important Power BI Validation Notice**: As specified in `AGENTS.md`, AI-generated DAX measures are **not assumed to be validated in Power BI Desktop** until verified inside Power BI Desktop with active visuals. Use this reference alongside [`dax/VALIDATION_CHECKLIST.md`](../dax/VALIDATION_CHECKLIST.md).

---

## Table of Contents
1. [Base Business Measures](#1-base-business-measures)
2. [Time Intelligence Measures](#2-time-intelligence-measures)
3. [Profitability, Contribution & Ranking Measures](#3-profitability-contribution--ranking-measures)

---

## 1. Base Business Measures
Location: `dax/01_base_measures.dax`

### 1.1 `Total Sales`
- **DAX Expression**:
  ```dax
  Total Sales =
  SUMX(
      Sales,
      Sales[Quantity] * Sales[UnitPrice] * (1 - Sales[Discount])
  )
  ```
- **Business Purpose**: Computes net sales revenue realized after line-item discounts.
- **Dependencies**: `Sales[Quantity]`, `Sales[UnitPrice]`, `Sales[Discount]`.
- **Format String**: Currency (`$#,##0.00`).
- **Context Behavior**: Row-by-row iteration across `Sales` within current filter context.

### 1.2 `Total Cost`
- **DAX Expression**:
  ```dax
  Total Cost =
  SUMX(
      Sales,
      Sales[Quantity] * RELATED(Products[CostPrice])
  )
  ```
- **Business Purpose**: Calculates total cost of goods sold (COGS).
- **Dependencies**: `Sales[Quantity]`, `Products[CostPrice]`, Relationship: `Sales[ProductID]` -> `Products[ProductID]`.
- **Format String**: Currency (`$#,##0.00`).
- **Context Behavior**: Uses `RELATED` to pull unit cost from the `Products` dimension table.

### 1.3 `Total Profit`
- **DAX Expression**:
  ```dax
  Total Profit =
  [Total Sales] - [Total Cost]
  ```
- **Business Purpose**: Gross dollar margin generated after deducting COGS from net sales.
- **Dependencies**: `[Total Sales]`, `[Total Cost]`.
- **Format String**: Currency (`$#,##0.00`).

### 1.4 `Profit Margin %`
- **DAX Expression**:
  ```dax
  Profit Margin % =
  DIVIDE(
      [Total Profit],
      [Total Sales],
      0
  )
  ```
- **Business Purpose**: Profitability percentage relative to net revenue. Safe division returns 0 if sales are zero.
- **Dependencies**: `[Total Profit]`, `[Total Sales]`.
- **Format String**: Percentage (`0.0%`).

### 1.5 `Total Orders`
- **DAX Expression**:
  ```dax
  Total Orders =
  DISTINCTCOUNT(Sales[OrderID])
  ```
- **Business Purpose**: Counts unique transaction purchase orders.
- **Dependencies**: `Sales[OrderID]`.
- **Format String**: Whole Number (`#,##0`).

### 1.6 `Total Customers`
- **DAX Expression**:
  ```dax
  Total Customers =
  DISTINCTCOUNT(Sales[CustomerID])
  ```
- **Business Purpose**: Counts distinct transacting customers.
- **Dependencies**: `Sales[CustomerID]`.
- **Format String**: Whole Number (`#,##0`).

### 1.7 `Average Order Value (AOV)`
- **DAX Expression**:
  ```dax
  Average Order Value =
  DIVIDE(
      [Total Sales],
      [Total Orders],
      0
  )
  ```
- **Business Purpose**: Average revenue generated per unique sales order.
- **Dependencies**: `[Total Sales]`, `[Total Orders]`.
- **Format String**: Currency (`$#,##0.00`).

---

## 2. Time Intelligence Measures
Location: `dax/02_time_intelligence.dax`

### 2.1 `Previous Year Sales`
- **DAX Expression**:
  ```dax
  Previous Year Sales =
  CALCULATE(
      [Total Sales],
      SAMEPERIODLASTYEAR(Date[Date])
  )
  ```
- **Business Purpose**: Computes `Total Sales` for the identical calendar period one year prior.
- **Dependencies**: `[Total Sales]`, `Date[Date]`.
- **Format String**: Currency (`$#,##0.00`).

### 2.2 `YoY Sales Growth`
- **DAX Expression**:
  ```dax
  YoY Sales Growth =
  IF(
      ISBLANK([Previous Year Sales]),
      BLANK(),
      [Total Sales] - [Previous Year Sales]
  )
  ```
- **Business Purpose**: Dollar variance between current period sales and previous year sales.
- **Dependencies**: `[Total Sales]`, `[Previous Year Sales]`.
- **Format String**: Currency (`$#,##0.00`).

### 2.3 `YoY Sales Growth %`
- **DAX Expression**:
  ```dax
  YoY Sales Growth % =
  DIVIDE(
      [Total Sales] - [Previous Year Sales],
      [Previous Year Sales],
      BLANK()
  )
  ```
- **Business Purpose**: Relative percentage growth compared to previous year.
- **Dependencies**: `[Total Sales]`, `[Previous Year Sales]`.
- **Format String**: Percentage (`+0.0%;-0.0%;0.0%`).

### 2.4 `Monthly Sales`
- **DAX Expression**:
  ```dax
  Monthly Sales =
  CALCULATE(
      [Total Sales],
      ALLEXCEPT(Date, Date[Year], Date[Month], Date[MonthNumber])
  )
  ```
- **Business Purpose**: Aggregates net sales at the Year-Month grain, ignoring lower-level date filters.
- **Dependencies**: `[Total Sales]`, `Date[Year]`, `Date[Month]`, `Date[MonthNumber]`.

### 2.5 `Quarterly Sales`
- **DAX Expression**:
  ```dax
  Quarterly Sales =
  CALCULATE(
      [Total Sales],
      ALLEXCEPT(Date, Date[Year], Date[Quarter])
  )
  ```
- **Business Purpose**: Aggregates sales at the Year-Quarter level.

### 2.6 `YTD Sales`
- **DAX Expression**:
  ```dax
  YTD Sales =
  TOTALYTD(
      [Total Sales],
      Date[Date]
  )
  ```
- **Business Purpose**: Cumulative year-to-date sales starting January 1st of each calendar year.

---

## 3. Profitability, Contribution & Ranking Measures
Location: `dax/03_profitability_and_rankings.dax`

### 3.1 `Category Profitability`
- **DAX Expression**:
  ```dax
  Category Profitability =
  CALCULATE(
      [Total Profit],
      KEEPFILTERS(Products[Category])
  )
  ```
- **Business Purpose**: Retains active product category filters while evaluating profitability.

### 3.2 `Customer Contribution %`
- **DAX Expression**:
  ```dax
  Customer Contribution % =
  VAR CurrentSales = [Total Sales]
  VAR AllCustomerSales = CALCULATE([Total Sales], ALL(Customers))
  RETURN
      DIVIDE(
          CurrentSales,
          AllCustomerSales,
          0
      )
  ```
- **Business Purpose**: Percentage share of total enterprise revenue generated by the selected customer or segment.
- **Dependencies**: `[Total Sales]`, `Customers` table.
- **Format String**: Percentage (`0.00%`).

### 3.3 `Category Sales Contribution %`
- **DAX Expression**:
  ```dax
  Category Sales Contribution % =
  VAR CategorySales = [Total Sales]
  VAR TotalSalesAllCategories = CALCULATE([Total Sales], ALL(Products[Category]))
  RETURN
      DIVIDE(
          CategorySales,
          TotalSalesAllCategories,
          0
      )
  ```
- **Business Purpose**: Share of total revenue contributed by each product category.
- **Format String**: Percentage (`0.0%`).

### 3.4 `Top Product Rank by Sales`
- **DAX Expression**:
  ```dax
  Top Product Rank by Sales =
  IF(
      ISBLANK([Total Sales]),
      BLANK(),
      RANKX(
          ALLSELECTED(Products[ProductName]),
          [Total Sales],
          ,
          DESC,
          Dense
      )
  )
  ```
- **Business Purpose**: Dynamic dense ranking of products by sales volume within current visual slicers.

### 3.5 `Top Product Rank by Profit`
- **DAX Expression**:
  ```dax
  Top Product Rank by Profit =
  IF(
      ISBLANK([Total Profit]),
      BLANK(),
      RANKX(
          ALLSELECTED(Products[ProductName]),
          [Total Profit],
          ,
          DESC,
          Dense
      )
  )
  ```
- **Business Purpose**: Dynamic dense ranking of products by gross profit.
