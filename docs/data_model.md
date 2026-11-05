# Data Model Architecture — RetailPulse BI Analytics

This document details the star-schema data modeling principles and relational architecture implemented for RetailPulse BI Analytics.

---

## 1. Relational Entity Relationship Diagram (ERD)

```text
                  +-----------------------------------+
                  |             Customers             |
                  +-----------------------------------+
                  | PK  CustomerID      VARCHAR(10)   |
                  |     CustomerName    VARCHAR(100)  |
                  |     Segment         VARCHAR(25)   |
                  |     Age             INTEGER       |
                  |     Gender          VARCHAR(15)   |
                  |     City            VARCHAR(50)   |
                  |     State           VARCHAR(50)   |
                  +-----------------+-----------------+
                                    | 1
                                    |
                                    | *
+------------------------------+    |    +------------------------------+
|           Products           |    |    |           Regions            |
+------------------------------+    |    +------------------------------+
| PK  ProductID    VARCHAR(10) |    |    | PK  RegionID    VARCHAR(10)  |
|     ProductName  VARCHAR(150)|    |    |     Region      VARCHAR(25)  |
|     Category     VARCHAR(50) |    |    |     State       VARCHAR(50)  |
|     SubCategory  VARCHAR(50) |    |    |     City        VARCHAR(50)  |
|     Brand        VARCHAR(50) |    |    +--------------+---------------+
|     CostPrice    DECIMAL     |    |                   | 1
+--------------+---------------+    |                   |
               | 1                  |                   |
               |                    |                   |
               | *                  |                   | *
+--------------+--------------------+-------------------+---------------+
|                                 Sales                                 |
+-----------------------------------------------------------------------+
| PK/FK  OrderID       VARCHAR(15)                                      |
| FK     OrderDate     DATE          ---> Date[Date]                    |
| FK     CustomerID    VARCHAR(10)   ---> Customers[CustomerID]         |
| FK     ProductID     VARCHAR(10)   ---> Products[ProductID]           |
| FK     RegionID      VARCHAR(10)   ---> Regions[RegionID]             |
|        Quantity      INTEGER                                          |
|        UnitPrice     DECIMAL(10,2)                                    |
|        Discount      DECIMAL(5,4)                                     |
+-----------------------------------+-----------------------------------+
                                    | *
                                    |
                                    | 1
                  +-----------------+-----------------+
                  |               Date                |
                  +-----------------------------------+
                  | PK  Date            DATE          |
                  |     Year            INTEGER       |
                  |     Quarter         VARCHAR(2)    |
                  |     Month           VARCHAR(20)   |
                  |     MonthNumber     INTEGER       |
                  |     Week            INTEGER       |
                  +-----------------------------------+
```

---

## 2. Table Relationships & Cardinality

| From (Fact / Many) | Foreign Key | To (Dimension / One) | Primary Key | Cardinality | Cross Filter Direction | Active |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Sales` | `OrderDate` | `Date` | `Date` | Many-to-One (`*:1`) | Single (`Date` filters `Sales`) | **Active** |
| `Sales` | `CustomerID` | `Customers` | `CustomerID` | Many-to-One (`*:1`) | Single (`Customers` filters `Sales`) | **Active** |
| `Sales` | `ProductID` | `Products` | `ProductID` | Many-to-One (`*:1`) | Single (`Products` filters `Sales`) | **Active** |
| `Sales` | `RegionID` | `Regions` | `RegionID` | Many-to-One (`*:1`) | Single (`Regions` filters `Sales`) | **Active** |

---

## 3. Modeling Best Practices & Rationale
1. **Pure Star Schema**:
   - Reduces query complexity and memory footprint in Power BI's VertiPaq engine.
   - Eliminates bidirectional cross-filtering ambiguities and performance penalties.
2. **Dedicated Date Dimension**:
   - Spans strictly uninterrupted calendar days from 2022-01-01 to 2024-12-31.
   - Marked as official Date Table to power DAX time-intelligence functions (`SAMEPERIODLASTYEAR`, `TOTALYTD`).
   - Column `Month` is sorted by `MonthNumber` to guarantee proper calendar chronology.
3. **Surrogate Key Integrity**:
   - Standardized alphanumeric IDs (`ORD-`, `CUST-`, `PROD-`, `REG-`).
   - Validated against nulls and orphan keys through automated data-quality pipelines.
4. **Calculated Columns Avoided in Fact Table**:
   - Total sales, costs, and profits are calculated on-the-fly through DAX measures (`SUMX`) rather than calculated columns, optimizing data storage and compression.
