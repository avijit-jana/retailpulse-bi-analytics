# RetailPulse BI Analytics — Business Requirements Document

## 1. Executive Summary & Project Purpose
RetailPulse BI Analytics is an end-to-end retail sales intelligence solution engineered using Power BI, Power Query, DAX, and Python.

The primary objective is to transform transactional retail sales data into actionable, high-impact business intelligence. The solution enables executive leadership, sales directors, inventory managers, and regional leads to monitor revenue performance, diagnose profitability leakages, evaluate customer segment dynamics, and optimize product mix and discounting strategies.

> **Integrity & Disclosure Notice**: As mandated by `AGENTS.md`, all transactional and dimension datasets in this repository are **strictly synthetic** and generated for modeling, prototyping, and analytical demonstration. No real business results or proprietary company numbers are simulated or claimed.

---

## 2. Core Business Questions
The BI solution addresses key questions across 5 core operational domains:

1. **Revenue & Growth**:
   - What is the overall sales trajectory across the 3-year historical window (2022–2024)?
   - How does Year-over-Year (YoY) revenue compare across quarters and months?
   - What are the seasonal peaks and troughs in demand?
2. **Profitability & Margin Health**:
   - Which product categories and sub-categories drive gross profit vs. which erode margin?
   - Are excessive discounts diluting net profits on high-volume items?
3. **Customer Segmentation & Value**:
   - How are revenue and transaction volume split across Consumer, Corporate, and Home Office segments?
   - What is the Average Order Value (AOV) per segment and region?
   - Which customer segments exhibit the highest lifetime value and purchasing frequency?
4. **Product Catalog & Brand Performance**:
   - What are the top 10 products by sales volume vs. top 10 products by profit contribution?
   - Are certain brands over-indexed on discounts to generate sales?
5. **Regional & Geographic Distribution**:
   - How does performance vary across geographic regions (East, West, Central, South)?
   - Are regional disparities driven by product mix, order frequency, or discounting policies?

---

## 3. Core KPIs & Mathematical Formulations

| KPI Name | DAX Measure / Formula | Business Interpretation |
| :--- | :--- | :--- |
| **Total Sales** | `SUMX(Sales, Quantity * UnitPrice * (1 - Discount))` | Net sales revenue generated across all completed orders after line discounts. |
| **Total Cost** | `SUMX(Sales, Quantity * RELATED(Products[CostPrice]))` | Total cost of goods sold (COGS) based on product catalog unit costs. |
| **Total Profit** | `[Total Sales] - [Total Cost]` | Gross dollar profit after product cost of goods sold. |
| **Profit Margin %** | `DIVIDE([Total Profit], [Total Sales], 0)` | Overall profitability efficiency percentage. |
| **Total Orders** | `DISTINCTCOUNT(Sales[OrderID])` | Total unique purchase transactions executed. |
| **Total Customers** | `DISTINCTCOUNT(Sales[CustomerID])` | Unique transacting customer count. |
| **Average Order Value (AOV)** | `DIVIDE([Total Sales], [Total Orders], 0)` | Average net revenue earned per order transaction. |
| **YoY Sales Growth %** | `DIVIDE([Total Sales] - [Previous Year Sales], [Previous Year Sales], BLANK())` | Relative percentage growth in net revenue compared to the identical period last year. |

---

## 4. Star-Schema Data Model Specification

The data architecture adheres to an enterprise star-schema design centered on `FactSales` with 1-to-many (`1:*`), single-direction relationships from surrounding dimension tables.

```text
       +--------------------+          +--------------------+
       |    DimCustomers    |          |    DimProducts     |
       |--------------------|          |--------------------|
       | PK CustomerID      |          | PK ProductID       |
       |    CustomerName    |          |    ProductName     |
       |    Segment         |          |    Category        |
       |    Age, Gender     |          |    SubCategory     |
       |    City, State     |          |    Brand, CostPrice|
       +---------+----------+          +---------+----------+
                 | 1                             | 1
                 |                               |
                 | *                           * |
            +----+-------------------------------+----+
            |                  FactSales              |
            |-----------------------------------------|
            | OrderID, OrderDate                      |
            | FK CustomerID                           |
            | FK ProductID                            |
            | FK RegionID                             |
            | Quantity, UnitPrice, Discount           |
            +----+-------------------------------+----+
                 | *                           * |
                 |                               |
                 | 1                             | 1
       +---------+----------+          +---------+----------+
       |     DimRegions     |          |      DimDate       |
       |--------------------|          |--------------------|
       | PK RegionID        |          | PK Date            |
       |    Region          |          |    Year, Quarter   |
       |    State           |          |    Month           |
       |    City            |          |    MonthNumber     |
       |                    |          |    Week            |
       +--------------------+          +--------------------+
```

### Table Definitions

#### FactSales (`Sales.csv`)
- **Grain**: One record per line item per order.
- **Keys**: `OrderID` (degenerate key), `OrderDate` (FK -> DimDate), `CustomerID` (FK -> DimCustomers), `ProductID` (FK -> DimProducts), `RegionID` (FK -> DimRegions).
- **Measures**: `Quantity` (integer > 0), `UnitPrice` (decimal > 0), `Discount` (decimal [0.00, 1.00)).

#### DimCustomers (`Customers.csv`)
- **Grain**: One record per unique customer.
- **Attributes**: `CustomerID` (PK), `CustomerName`, `Segment` (`Consumer`, `Corporate`, `Home Office`), `Age`, `Gender`, `City`, `State`.

#### DimProducts (`Products.csv`)
- **Grain**: One record per product SKU.
- **Attributes**: `ProductID` (PK), `ProductName`, `Category` (`Technology`, `Furniture`, `Office Supplies`), `SubCategory`, `Brand`, `CostPrice`.

#### DimRegions (`Regions.csv`)
- **Grain**: One record per designated geographical operational hub.
- **Attributes**: `RegionID` (PK), `Region` (`East`, `West`, `Central`, `South`), `State`, `City`.

#### DimDate (`Date.csv`)
- **Grain**: One record per contiguous calendar day (2022-01-01 to 2024-12-31).
- **Attributes**: `Date` (PK), `Year`, `Quarter`, `Month`, `MonthNumber`, `Week`.

---

## 5. Power BI Five-Page Report Specifications

### Page 1: Executive Overview
- **Objective**: High-level corporate health scorecard for C-suite executives and board members.
- **Target Audience**: CEO, CFO, VP of Sales.
- **Visuals**:
  1. *KPI Cards Row*: Total Sales, Total Profit, Profit Margin %, Total Orders, AOV, YoY Sales Growth %.
  2. *Sales & Profit Trend (Line & Clustered Column Chart)*: Monthly Sales vs. Monthly Profit over time.
  3. *Sales by Category (Donut / Bar Chart)*: Share of revenue across Technology, Furniture, and Office Supplies.
  4. *Regional Performance (Map / Horizontal Bar Chart)*: Net Sales & Margin % split by Region.
  5. *Global Slicers*: Year, Quarter, Region.

### Page 2: Sales Analysis
- **Objective**: Detailed examination of revenue drivers, discount depth, and volume dynamics.
- **Target Audience**: Sales Directors, Revenue Operations, Commercial Leads.
- **Visuals**:
  1. *Monthly & Quarterly Revenue Waterfall*: Variance analysis comparing current month/quarter vs previous periods.
  2. *Discount vs. Sales Scatter Plot*: Correlation analysis evaluating if higher discounting drove proportional volume or caused margin degradation.
  3. *Sales by Channel/Region (Stacked Column Chart)*: Monthly sales stacked by region.
  4. *Transactions Table*: Granular order ledger with OrderID, Date, Customer, Product, Quantity, Net Sales, and Discount %.

### Page 3: Customer Analysis
- **Objective**: Customer segment profiling, purchasing behavior, and demographic analysis.
- **Target Audience**: CMO, Customer Retention Leads, Account Managers.
- **Visuals**:
  1. *Segment Contribution Matrix*: Sales, Profit, Order Count, and AOV by Customer Segment (`Consumer`, `Corporate`, `Home Office`).
  2. *Customer Age & Gender Demographics (Clustered Bar Chart)*: Distribution of sales by age brackets (18-30, 31-45, 46-60, 60+) and gender.
  3. *Top 20 Customers by Revenue (Table / Ranked Visual)*: Customer Name, Segment, City, Lifetime Orders, Total Revenue, Customer Contribution %.
  4. *Segment Slicers*: Segment, State, Gender.

### Page 4: Product Analysis
- **Objective**: Portfolio performance, SKU-level profitability, brand rankings, and catalog rationalization.
- **Target Audience**: Merchandising Managers, Supply Chain Directors, Category Leads.
- **Visuals**:
  1. *Category & SubCategory Profitability Matrix*: Sales, Cost, Gross Profit, and Profit Margin % by Category and SubCategory.
  2. *Brand Performance Matrix*: Sales and average discount rate by Brand.
  3. *Top 10 vs Bottom 10 Products by Profit*: Visual ranking identifying best-sellers and loss-leaders.
  4. *Product Category / SubCategory Drill-down Matrix*.

### Page 5: Management Insights
- **Objective**: Actionable operational decision support, risk detection, and growth opportunities.
- **Target Audience**: COO, Regional General Managers, Operations Review Committee.
- **Visuals**:
  1. *Margin Leakage Diagnostic Visual*: Highlights orders/products where high discounts resulted in sub-optimal or negative margin contribution.
  2. *Regional Disparity Decomposition*: Compares Average Order Value against Profit Margin across East, West, Central, and South hubs.
  3. *Executive Opportunity Callouts*: Ranked recommendations (e.g. discount policy caps, inventory priority for top-margin SKUs).
  4. *What-If / Parameter Scenario Visual*: Sensitivity simulation of adjusting average discount rates by +/- 2-5%.
