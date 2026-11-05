# Data Dictionary — RetailPulse BI Analytics

This document defines the schema, data types, constraints, and business logic for all tables in the RetailPulse BI Analytics star-schema data model.

> **Dataset Classification**: Synthetic Retail Data (Generated via `src/data_generation/generator.py` with seed=42).

---

## 1. Fact Table: `Sales` (`Sales.csv`)
- **Storage Location**: `data/raw/Sales.csv`, `data/cleaned/Sales.csv`
- **Granularity**: One record per line item per customer order.

| Column Name | Data Type | Key Type | Nullable | Valid Values / Constraints | Business Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `OrderID` | String | Degenerate PK | No | Format: `ORD-XXXXXXX` (e.g., `ORD-0000001`) | Unique identifier for a sales order transaction. Can repeat across multiple items. |
| `OrderDate` | Date (String) | FK -> `Date.Date` | No | ISO 8601 `YYYY-MM-DD` (2022-01-01 to 2024-12-31) | The calendar date on which the order transaction took place. |
| `CustomerID` | String | FK -> `Customers.CustomerID` | No | Format: `CUST-XXXXX` | Identifier of the customer placing the order. |
| `ProductID` | String | FK -> `Products.ProductID` | No | Format: `PROD-XXXX` | Identifier of the purchased product SKU. |
| `RegionID` | String | FK -> `Regions.RegionID` | No | Format: `REG-XXX` | Regional hub where the customer/fulfillment was routed. |
| `Quantity` | Integer | - | No | Integer > 0 (typically 1 to 10) | Number of units purchased for this line item. |
| `UnitPrice` | Decimal (2) | - | No | Decimal > 0.00 | Selling retail price per unit before discount. |
| `Discount` | Decimal (4) | - | No | Decimal in range `[0.00, 1.00)` | Line-item discount percentage applied to UnitPrice. |

---

## 2. Dimension Table: `Customers` (`Customers.csv`)
- **Storage Location**: `data/raw/Customers.csv`, `data/cleaned/Customers.csv`
- **Granularity**: One record per unique registered customer.

| Column Name | Data Type | Key Type | Nullable | Valid Values / Constraints | Business Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `CustomerID` | String | Primary Key | No | Format: `CUST-XXXXX`, Strictly Unique | Unique identifier assigned to each customer. |
| `CustomerName` | String | - | No | Full Name (e.g., "Allison Hill") | Full name of the customer. |
| `Segment` | String | - | No | `Consumer`, `Corporate`, `Home Office` | Customer market segment classification. |
| `Age` | Integer | - | No | Integer between 18 and 75 | Customer age at registration. |
| `Gender` | String | - | No | `Male`, `Female`, `Non-Binary` | Self-reported customer gender. |
| `City` | String | - | No | Valid operational hub city | City where customer resides. |
| `State` | String | - | No | Valid operational hub state | State where customer resides. |

---

## 3. Dimension Table: `Products` (`Products.csv`)
- **Storage Location**: `data/raw/Products.csv`, `data/cleaned/Products.csv`
- **Granularity**: One record per individual product SKU.

| Column Name | Data Type | Key Type | Nullable | Valid Values / Constraints | Business Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ProductID` | String | Primary Key | No | Format: `PROD-XXXX`, Strictly Unique | Unique identifier assigned to each product SKU. |
| `ProductName` | String | - | No | Text (e.g., "TechPro Laptop Model-B10") | Descriptive commercial name of the product SKU. |
| `Category` | String | - | No | `Technology`, `Furniture`, `Office Supplies` | Top-level product category classification. |
| `SubCategory` | String | - | No | e.g., `Laptops`, `Chairs`, `Storage` | Granular product subcategory. |
| `Brand` | String | - | No | e.g., `TechPro`, `ErgoComfort`, `Apex` | Manufacturer or brand name. |
| `CostPrice` | Decimal (2) | - | No | Decimal > 0.00 | Unit manufacturing / acquisition cost to retailer. |

---

## 4. Dimension Table: `Regions` (`Regions.csv`)
- **Storage Location**: `data/raw/Regions.csv`, `data/cleaned/Regions.csv`
- **Granularity**: One record per geographical operational hub.

| Column Name | Data Type | Key Type | Nullable | Valid Values / Constraints | Business Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `RegionID` | String | Primary Key | No | Format: `REG-XXX`, Strictly Unique | Unique identifier assigned to each geographic hub. |
| `Region` | String | - | No | `East`, `West`, `Central`, `South` | Broad geographic territory. |
| `State` | String | - | No | U.S. State Name (e.g., California, New York) | State of the regional operational hub. |
| `City` | String | - | No | U.S. City Name (e.g., Los Angeles, Chicago) | Primary metropolitan hub city. |

---

## 5. Dimension Table: `Date` (`Date.csv`)
- **Storage Location**: `data/raw/Date.csv`, `data/cleaned/Date.csv`
- **Granularity**: One record per contiguous calendar day.

| Column Name | Data Type | Key Type | Nullable | Valid Values / Constraints | Business Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Date` | Date (String) | Primary Key | No | ISO 8601 `YYYY-MM-DD`, Strictly Contiguous | Unique calendar date. |
| `Year` | Integer | - | No | 2022, 2023, 2024 | 4-digit calendar year. |
| `Quarter` | String | - | No | `Q1`, `Q2`, `Q3`, `Q4` | Calendar quarter label. |
| `Month` | String | - | No | `January` through `December` | Full English name of the calendar month. |
| `MonthNumber` | Integer | - | No | Integer from 1 to 12 | Numeric order of the month (used for sorting Month). |
| `Week` | Integer | - | No | Integer from 1 to 53 | ISO calendar week number. |
