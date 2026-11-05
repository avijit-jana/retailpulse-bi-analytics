# RetailPulse BI Analytics

> **End-to-End Retail Sales & Business Intelligence Analytics Solution**
> Built with **Power BI**, **Power Query**, **DAX**, and **Python**.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Data Quality Tests](https://img.shields.io/badge/tests-15%20passed-brightgreen.svg)](tests/)
[![Architecture](https://img.shields.io/badge/schema-Star%20Schema-orange.svg)](docs/data_model.md)
[![Dataset Notice](https://img.shields.io/badge/dataset-100%25%20synthetic-yellow.svg)](#dataset-classification-and-synthetic-notice)

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Dataset Classification and Synthetic Notice](#dataset-classification-and-synthetic-notice)
3. [Repository Directory Structure](#repository-directory-structure)
4. [Data Generation & Assumptions](#data-generation--assumptions)
5. [Data Quality Validation Framework](#data-quality-validation-framework)
6. [Data Model & Star Schema Architecture](#data-model--star-schema-architecture)
7. [DAX Measure Library](#dax-measure-library)
8. [Power BI Report Architecture (5 Pages)](#power-bi-report-architecture-5-pages)
9. [Installation & Quick Start](#installation--quick-start)
10. [Running Automated Tests](#running-automated-tests)
11. [Development Roadmap](#development-roadmap)

---

## Project Overview
RetailPulse BI Analytics is an enterprise-grade retail intelligence platform designed to transform raw transactional retail data into high-impact operational and executive insights.

The platform provides granular visibility into:
- **Revenue & Growth**: Multi-year trend analysis (2022–2024), seasonal fluctuations, and YoY performance.
- **Profitability & Margin Health**: Category and product-level gross margin analysis, discounting leakage.
- **Customer Segmentation**: Behavior across Consumer, Corporate, and Home Office tiers, demographic distributions, and retention.
- **Product Merchandising**: Best-selling vs. loss-leader identification, category mix, and brand performance.
- **Regional Operations**: Geographic distribution across East, West, Central, and South hubs.

---

## Dataset Classification and Synthetic Notice
In strict compliance with project governance guidelines (`AGENTS.md`):
- **100% Synthetic Data**: All customer, transaction, pricing, product, and regional data in this project are programmatically generated and entirely synthetic.
- **No Real Results Claimed**: No real-world business results or proprietary company numbers are simulated or claimed.
- **Reproducibility**: The data generator uses a fixed random seed (`42`), ensuring deterministic byte-for-byte reproducibility across runs.

---

## Repository Directory Structure

```text
RetailPulse-BI-Analytics/
├── .gitignore                      # Git ignore rules for Python, data files, and Power BI temp files
├── AGENTS.md                       # Core project instructions and architectural guidelines
├── Business_Requirements.md        # Comprehensive business questions, KPIs, and report page specs
├── README.md                       # Main project documentation (this document)
├── ROADMAP.md                      # Phased development roadmap
├── requirements.txt                # Python dependencies (pandas, numpy, faker, pytest)
├── data/
│   ├── raw/                        # Pure generated raw synthetic datasets (Sales, Customers, Products, Regions, Date)
│   └── cleaned/                    # Standardized, analysis-ready datasets (source data is never overwritten)
├── dax/
│   ├── 01_base_measures.dax        # Core DAX KPIs (Total Sales, Total Cost, Profit, Margin, AOV, etc.)
│   ├── 02_time_intelligence.dax    # Monthly, Quarterly, YoY Growth, YTD sales measures
│   ├── 03_profitability_and_rankings.dax # Customer contribution, category profitability, top rankings
│   └── VALIDATION_CHECKLIST.md     # Power BI Desktop manual verification checklist
├── docs/
│   ├── data_dictionary.md          # Complete field definitions, data types, and business rules
│   └── data_model.md               # Star-schema architecture and relationship definitions
├── reports/
│   └── screenshots/                # Directory for Power BI report visual captures and templates
├── src/
│   ├── __init__.py
│   ├── config.py                   # Configuration constants, random seed, product catalogs, geo hubs
│   ├── data_generation/            # Modular synthetic data generators
│   │   ├── __init__.py
│   │   ├── generator.py            # Orchestrator CLI for synthetic generation
│   │   ├── regions.py              # DimRegions generator
│   │   ├── customers.py            # DimCustomers generator (realistic names, segments, geo-matching)
│   │   ├── products.py             # DimProducts generator (Technology, Furniture, Office Supplies)
│   │   ├── dates.py                # DimDate calendar generator (2022-01-01 to 2024-12-31)
│   │   └── sales.py                # FactSales generator (multi-line orders, seasonality, discounts)
│   ├── utils/
│   │   ├── __init__.py
│   │   └── clean_data.py           # Immutability-preserving cleaning pipeline to data/cleaned/
│   └── validation/
│       ├── __init__.py
│       ├── validator.py            # Automated data-quality validator engine
│       └── validate_data.py        # CLI data quality reporting tool
└── tests/
    ├── __init__.py
    ├── test_generator.py           # Tests for seed reproducibility and generation schema
    └── test_validation.py          # Comprehensive pytest suite testing all 9 validation rules
```

---

## Data Generation & Assumptions

Data generation is executed via `src/data_generation/generator.py` using a fixed random seed (`seed=42`).

### Generation Assumptions & Parameters
1. **Time Horizon**: Unbroken calendar span of 3 years (January 1, 2022 – December 31, 2024), yielding 1,096 days for comprehensive multi-year trend and YoY analysis.
2. **Seasonality & Growth**:
   - 15% annual YoY transaction volume growth.
   - Q4 holiday surge factor (+45% volume increase in October, November, December).
   - Weekend boost factor (+20% volume on Saturdays and Sundays).
3. **Transaction Structure**:
   - ~15,000 distinct orders generating ~24,000 transaction line items (1 to 4 items per order).
   - Multi-item orders share consistent `OrderID`, `OrderDate`, `CustomerID`, and `RegionID`.
4. **Pricing & Margin Logic**:
   - `CostPrice` defined realistically per SKU.
   - Category markups: Technology (20%–45%), Furniture (30%–60%), Office Supplies (40%–85%).
   - Selling `UnitPrice` computed as `CostPrice * (1 + markup)` with 2 decimal precision.
   - Net Line Revenue: `Quantity * UnitPrice * (1 - Discount)`.
5. **Discount Policy**:
   - Discrete discount brackets: `0% (45%), 5% (18%), 10% (15%), 15% (10%), 20% (7%), 25% (3%), 30% (2%)`.
   - Never exceeds 30% and never negative.
6. **Customer Pareto Dynamics**:
   - Customer ordering frequency follows a Pareto-like distribution, reflecting realistic repeat buyer behavior.

---

## Data Quality Validation Framework

The validation engine in `src/validation/` rigorously tests data against 9 business and relational constraints:

| # | Validation Rule | Implementation & Check Description |
| :- | :--- | :--- |
| **1** | **Primary Key Uniqueness** | Ensures `CustomerID`, `ProductID`, `RegionID`, and `Date` have zero duplicates. |
| **2** | **Foreign Key Integrity** | Verifies 100% of `CustomerID`, `ProductID`, `RegionID`, and `OrderDate` in Sales exist in dimensions. |
| **3** | **Null & Missing Values** | Asserts 0 null or NaN entries across all mandatory columns in all tables. |
| **4** | **Duplicate Transactions** | Checks for duplicate order line items sharing identical `OrderID` and `ProductID`. |
| **5** | **Invalid Dates** | Validates date parsing, chronological validity, and calendar range alignment. |
| **6** | **Negative/Zero Quantities** | Flags any order lines where `Quantity <= 0`. |
| **7** | **Invalid Discounts** | Verifies `0.00 <= Discount < 1.00`. |
| **8** | **Invalid Prices and Costs** | Asserts `UnitPrice > 0.00` and `CostPrice > 0.00`. |
| **9** | **Unexpected Categories/Segments** | Validates categories against allowed set (`Technology`, `Furniture`, `Office Supplies`) and segments (`Consumer`, `Corporate`, `Home Office`). |

> **Important**: The validation module does **not** silently drop or delete invalid records. It compiles and displays a human-readable diagnostic report detailing table, column, rule, and error count.

---

## Data Model & Star Schema Architecture

A clean star-schema model is established around `FactSales`:

- **Fact Table**: `Sales` (`Sales.csv`)
- **Dimension Tables**:
  - `Customers` (`Customers.csv`): 1 to Many relationship with `Sales` on `CustomerID`.
  - `Products` (`Products.csv`): 1 to Many relationship with `Sales` on `ProductID`.
  - `Regions` (`Regions.csv`): 1 to Many relationship with `Sales` on `RegionID`.
  - `Date` (`Date.csv`): 1 to Many relationship with `Sales` on `OrderDate`.

Detailed schema specifications and ERD diagrams are documented in [`docs/data_model.md`](docs/data_model.md) and [`docs/data_dictionary.md`](docs/data_dictionary.md).

---

## DAX Measure Library

The DAX library is organized into three modular script files located in `dax/`:

1. **`01_base_measures.dax`**:
   - `Total Sales`, `Total Cost`, `Total Profit`, `Profit Margin %`, `Total Orders`, `Total Customers`, `Average Order Value (AOV)`.
2. **`02_time_intelligence.dax`**:
   - `Monthly Sales`, `Quarterly Sales`, `Previous Year Sales`, `YoY Sales Growth`, `YoY Sales Growth %`, `YTD Sales`.
3. **`03_profitability_and_rankings.dax`**:
   - `Category Profitability`, `Customer Contribution %`, `Category Sales Contribution %`, `Top Product Rank by Sales`, `Top Product Rank by Profit`.

### Verification Notice
Per `AGENTS.md`, AI-generated DAX measures are not assumed to have been verified in Power BI Desktop automatically. Refer to [`dax/VALIDATION_CHECKLIST.md`](dax/VALIDATION_CHECKLIST.md) for step-by-step verification instructions inside Power BI Desktop.

---

## Power BI Report Architecture (5 Pages)

Detailed in [`Business_Requirements.md`](Business_Requirements.md):
1. **Executive Overview**: High-level KPI summary cards, monthly sales & profit trends, category revenue breakdown, and regional performance.
2. **Sales Analysis**: Sales volume analysis, discount vs. sales scatter plot, regional sales distribution, and order transaction ledger.
3. **Customer Analysis**: Customer segment contribution, age & gender demographic profiling, and top customer value rankings.
4. **Product Analysis**: Product category & subcategory profitability matrix, brand performance, and top/bottom 10 product rankings.
5. **Management Insights**: Discount leakage analysis, regional margin disparity decomposition, and strategic management recommendations.

---

## Installation & Quick Start

### 1. Prerequisites
- Python 3.10 or higher.
- Git.

### 2. Install Dependencies
```bash
python3 -m pip install -r requirements.txt
```

### 3. Generate Synthetic Data
To generate raw datasets with the default seed (`42`):
```bash
python3 -m src.data_generation.generator --output-dir data/raw
```

### 4. Run Cleaning Pipeline
To prepare clean datasets for Power BI:
```bash
python3 -m src.utils.clean_data
```

### 5. Run Data Quality Validation
Run the automated validator to inspect the dataset:
```bash
python3 -m src.validation.validate_data --data-dir data/cleaned
```

---

## Running Automated Tests

Run the complete test suite with `pytest`:
```bash
pytest -v
```

All 15 automated tests covering seed reproducibility, schema validity, referential integrity, and every data validation rule will execute.

---

## Development Roadmap
See [`ROADMAP.md`](ROADMAP.md) for the active milestone breakdown, current delivery status, and upcoming phases.
