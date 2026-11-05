# Power BI Development Instructions — RetailPulse BI Analytics

This guide provides end-to-end, reproducible instructions for building the Power BI report using the validated datasets and DAX library in this repository.

> **Verification Notice**: In strict accordance with `AGENTS.md`, AI agents cannot interact directly with the Power BI Desktop GUI. Therefore, visual verification and rendering must be performed by the developer in Power BI Desktop following the instructions below.

---

## Step 1: Connecting Data via Power Query

1. Open **Power BI Desktop**.
2. Select **Get Data** -> **Text/CSV**.
3. Ingest each of the following 5 CSV files from the repository directory `data/cleaned/`:
   - `data/cleaned/Customers.csv`
   - `data/cleaned/Products.csv`
   - `data/cleaned/Regions.csv`
   - `data/cleaned/Date.csv`
   - `data/cleaned/Sales.csv`
4. In the Power Query Editor, verify data types:
   - **Sales**:
     - `OrderID`: Text
     - `OrderDate`: Date
     - `CustomerID`: Text
     - `ProductID`: Text
     - `RegionID`: Text
     - `Quantity`: Whole Number
     - `UnitPrice`: Fixed Decimal Number ($)
     - `Discount`: Percentage / Decimal Number
   - **Customers**:
     - `CustomerID`: Text
     - `Age`: Whole Number
     - `CustomerName`, `Segment`, `Gender`, `City`, `State`: Text
   - **Products**:
     - `ProductID`: Text
     - `CostPrice`: Fixed Decimal Number ($)
     - `ProductName`, `Category`, `SubCategory`, `Brand`: Text
   - **Regions**:
     - `RegionID`, `Region`, `State`, `City`: Text
   - **Date**:
     - `Date`: Date
     - `Year`, `MonthNumber`, `Week`: Whole Number
     - `Quarter`, `Month`: Text
5. Click **Close & Apply**.

---

## Step 2: Star-Schema Data Modeling & Relationships

1. Navigate to the **Model View** tab in Power BI Desktop.
2. Arrange tables in a star schema with `Sales` (fact) in the center, flanked by `Date`, `Customers`, `Products`, and `Regions`.
3. Configure the following 4 relationships:
   - `Date[Date]` 1 -> * `Sales[OrderDate]` (Single direction, Active)
   - `Customers[CustomerID]` 1 -> * `Sales[CustomerID]` (Single direction, Active)
   - `Products[ProductID]` 1 -> * `Sales[ProductID]` (Single direction, Active)
   - `Regions[RegionID]` 1 -> * `Sales[RegionID]` (Single direction, Active)
4. Right-click the `Date` table -> select **Mark as Date Table** -> Select `Date[Date]` as the date column.
5. In the `Date` table, select column `Month` -> under **Column Tools**, click **Sort by column** -> select `MonthNumber`.

---

## Step 3: DAX Measures Creation

Create a dedicated empty table named `_Measures` to house all business metrics:
1. Under **Home** tab -> Click **Enter Data** -> Name table `_Measures` -> Load.
2. Add the DAX measures from the repository files:
   - From `dax/01_base_measures.dax`:
     - `Total Sales`
     - `Total Cost`
     - `Total Profit`
     - `Profit Margin %`
     - `Total Orders`
     - `Total Customers`
     - `Average Order Value`
   - From `dax/02_time_intelligence.dax`:
     - `Monthly Sales`
     - `Quarterly Sales`
     - `Previous Year Sales`
     - `YoY Sales Growth`
     - `YoY Sales Growth %`
     - `YTD Sales`
   - From `dax/03_profitability_and_rankings.dax`:
     - `Category Profitability`
     - `Customer Contribution %`
     - `Category Sales Contribution %`
     - `Top Product Rank by Sales`
     - `Top Product Rank by Profit`
3. Format each measure accordingly (Currency for Sales/Profit/Cost, Percentage for Margins/Growths, Whole Number for Counts).

---

## Step 4: Constructing the Five Report Pages

### Page 1: Executive Overview
- **Canvas Size**: 16:9 (1280x720)
- **Top Slicer Bar**: Year (`Date[Year]`), Quarter (`Date[Quarter]`), Region (`Regions[Region]`).
- **Top Card Visuals**:
  - Card 1: `[Total Sales]`
  - Card 2: `[Total Profit]`
  - Card 3: `[Profit Margin %]`
  - Card 4: `[Total Orders]`
  - Card 5: `[Average Order Value]`
  - Card 6: `[YoY Sales Growth %]`
- **Main Visual (Center Left)**: Line and Clustered Column Chart:
  - Shared Axis: `Date[Month]` (sorted by `MonthNumber`)
  - Column Values: `[Total Sales]`
  - Line Values: `[Total Profit]`
- **Secondary Visual (Center Right)**: Donut Chart:
  - Legend: `Products[Category]`
  - Values: `[Total Sales]`
- **Bottom Visual**: Clustered Bar Chart:
  - Y-Axis: `Regions[Region]`
  - X-Axis: `[Total Sales]`, `[Total Profit]`

### Page 2: Sales Analysis
- **Top Metrics**: `[Total Sales]`, `[Total Orders]`, `[YoY Sales Growth %]`.
- **Visual 1**: Scatter Plot:
  - X-Axis: `Sales[Discount]`
  - Y-Axis: `[Total Sales]`
  - Legend / Details: `Products[Category]`
  - Size: `Sales[Quantity]`
- **Visual 2**: Stacked Column Chart:
  - X-Axis: `Date[Month]`
  - Legend: `Regions[Region]`
  - Values: `[Total Sales]`
- **Visual 3**: Detailed Drill-through Table:
  - Columns: `Sales[OrderID]`, `Sales[OrderDate]`, `Customers[CustomerName]`, `Products[ProductName]`, `Sales[Quantity]`, `[Total Sales]`, `Sales[Discount]`.

### Page 3: Customer Analysis
- **Top Metrics**: `[Total Customers]`, `[Average Order Value]`.
- **Visual 1**: Matrix by Segment:
  - Rows: `Customers[Segment]`
  - Values: `[Total Sales]`, `[Total Profit]`, `[Profit Margin %]`, `[Total Orders]`, `[Average Order Value]`.
- **Visual 2**: Clustered Column Chart:
  - X-Axis: `Customers[Gender]`
  - Values: `[Total Sales]`
  - Tooltips: `[Total Customers]`
- **Visual 3**: Ranked Customer Table:
  - Columns: `Customers[CustomerName]`, `Customers[Segment]`, `Customers[City]`, `Customers[State]`, `[Total Sales]`, `[Customer Contribution %]`.
  - Visual Filter: Top 25 Customers by `[Total Sales]`.

### Page 4: Product Analysis
- **Top Metrics**: Count of Products, `[Total Profit]`, Overall `[Profit Margin %]`.
- **Visual 1**: Matrix Hierarchical Breakdown:
  - Rows: `Products[Category]` -> `Products[SubCategory]` -> `Products[ProductName]`
  - Values: `[Total Sales]`, `[Total Cost]`, `[Total Profit]`, `[Profit Margin %]`.
- **Visual 2**: Horizontal Bar Chart:
  - Y-Axis: `Products[Brand]`
  - X-Axis: `[Total Sales]`
  - Data Color: Highlight by Category.
- **Visual 3**: Top 10 Products by Profit:
  - Y-Axis: `Products[ProductName]`
  - X-Axis: `[Total Profit]`
  - Visual Filter: Top 10 by `[Total Profit]`.

### Page 5: Management Insights
- **Top Callout Summary Cards**: Discount Leakage Flag, Regional Margin Spread.
- **Visual 1**: Margin Leakage Table:
  - Filter: Discount > 15%
  - Columns: `Products[ProductName]`, `Products[Category]`, `[Total Sales]`, `[Total Profit]`, `[Profit Margin %]`.
- **Visual 2**: Regional Disparity Decomposition Matrix:
  - Rows: `Regions[Region]`
  - Columns: `Date[Year]`
  - Values: `[Total Sales]`, `[Profit Margin %]`.
- **Visual 3**: Strategic Takeaway Text Cards / Callouts:
  - Document key takeaways and operational guidance.

---

## Step 5: Verification & Capture

1. Execute the verification steps in [`dax/VALIDATION_CHECKLIST.md`](../dax/VALIDATION_CHECKLIST.md).
2. Save the Power BI project file as `reports/RetailPulse_Analytics.pbix`.
3. Capture high-resolution PNG screenshots of each of the 5 report pages into `reports/screenshots/`:
   - `01_executive_overview.png`
   - `02_sales_analysis.png`
   - `03_customer_analysis.png`
   - `04_product_analysis.png`
   - `05_management_insights.png`
