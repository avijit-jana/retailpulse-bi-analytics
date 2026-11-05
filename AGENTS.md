# AGENTS.md — RetailPulse BI Analytics

## Project Overview
Build an end-to-end Retail Sales and Business Intelligence Analytics solution using Power BI, Power Query, DAX and Python.

The objective is to transform retail transaction data into an analytical solution that supports revenue, profitability, customer, product and regional performance analysis.

## Business Requirements
The final Power BI report must contain five pages:

1. Executive Overview
2. Sales Analysis
3. Customer Analysis
4. Product Analysis
5. Management Insights

## Data Model
Use a star-schema architecture.

### Fact Table
Sales:
- OrderID
- OrderDate
- CustomerID
- ProductID
- RegionID
- Quantity
- UnitPrice
- Discount

### Dimension Tables
Customers:
- CustomerID
- CustomerName
- Segment
- Age
- Gender
- City
- State

Products:
- ProductID
- ProductName
- Category
- SubCategory
- Brand
- CostPrice

Regions:
- RegionID
- Region
- State
- City

Date:
- Date
- Year
- Quarter
- Month
- MonthNumber
- Week

## Technology Stack
- Python for synthetic data generation and automated data validation.
- Power Query for data transformation.
- Power BI Desktop for modeling and report development.
- DAX for business measures and KPIs.
- GitHub for version control and documentation.

## Development Guidelines
1. Work in small, independently reviewable tasks.
2. Never invent real business results.
3. Label generated datasets as synthetic.
4. Maintain consistent primary and foreign keys.
5. Validate all generated data.
6. Document assumptions and transformations.
7. Keep Python code modular and reusable.
8. Add tests for important calculations and data-quality rules.
9. Do not commit credentials or secrets.
10. Never overwrite source datasets with transformed data.

## Core KPIs
- Total Sales
- Total Cost
- Total Profit
- Profit Margin
- Total Orders
- Total Customers
- Average Order Value
- Year-over-Year Sales Growth

## Important Constraints
Power BI Desktop report construction and visual validation must be performed and verified in Power BI Desktop.

AI-generated DAX, code, insights and documentation must be reviewed before acceptance.

## Expected Deliverables
- Reproducible data generation scripts
- Raw and cleaned datasets
- Data-quality tests
- DAX measures
- Data dictionary
- Data model documentation
- Power BI report
- Screenshots
- User guide
- Final presentation
