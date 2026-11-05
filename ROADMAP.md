# Development Roadmap — RetailPulse BI Analytics

This roadmap establishes the phased engineering lifecycle for RetailPulse BI Analytics.
It aligns strictly with the standards set in `AGENTS.md`.

---

## Phase Overview

| Phase | Title | Status | Deliverables |
| :--- | :--- | :--- | :--- |
| **Phase 1** | **Foundations & Architecture** | **Completed** | Directory structure, .gitignore, requirements.txt, Business Requirements, Data Model |
| **Phase 2** | **Synthetic Data Generator** | **Completed** | Modular generator scripts, fixed random seed (42), multi-year data (2022-2024) |
| **Phase 3** | **Data Validation & Cleaning Pipeline** | **Completed** | Automated data quality module (9 checks), test suite (pytest), clean datasets export |
| **Phase 4** | **DAX Measure Library** | **Completed** | Organized DAX files (base, time intelligence, rankings), Power BI validation checklist |
| **Phase 5** | **Power BI Modeling & Report Build** | **Upcoming** | Ingestion of cleaned CSVs, Star Schema relationships, 5-page report construction in Power BI Desktop |
| **Phase 6** | **Quality Review & Final Deliverables** | **Upcoming** | Visual verification, visual screenshots, user guide, final executive presentation |

---

## Detailed Milestones

### Phase 1: Foundations & Architecture (Completed)
- [x] Establish modular repository structure (`data/raw`, `data/cleaned`, `src/`, `tests/`, `docs/`, `dax/`, `reports/`).
- [x] Configure Python dependencies in `requirements.txt` (pandas, numpy, faker, pytest).
- [x] Configure `.gitignore` to prevent committing generated data and artifacts.
- [x] Author comprehensive `Business_Requirements.md` detailing business questions, KPIs, star schema, and 5 report page layouts.

### Phase 2: Synthetic Data Generator (Completed)
- [x] Build modular generators: `regions.py`, `customers.py`, `products.py`, `dates.py`, `sales.py`.
- [x] Implement fixed random seed (`42`) to guarantee 100% deterministic reproducibility.
- [x] Ensure realistic retail dynamics: multi-line orders, category-specific markups, holiday Q4 seasonality, and discrete discounts.
- [x] Enforce strict referential integrity across all foreign keys.

### Phase 3: Data Quality Validation & Cleaning (Completed)
- [x] Implement `src/validation/validator.py` with 9 comprehensive verification rules:
  - Primary key uniqueness
  - Foreign key referential integrity
  - Null / missing values
  - Duplicate transactions
  - Invalid date parsing & range
  - Negative/zero quantities
  - Invalid discount ranges
  - Invalid prices/costs
  - Unexpected categories and segments
- [x] Implement automated `pytest` suite in `tests/` covering clean generation, corrupted mutations, and edge cases.
- [x] Implement immutable cleaning pipeline `src/utils/clean_data.py` saving datasets to `data/cleaned/`.

### Phase 4: DAX Measure Library (Completed)
- [x] Author core base measures (`dax/01_base_measures.dax`): Total Sales, Total Cost, Total Profit, Profit Margin %, Total Orders, Total Customers, AOV.
- [x] Author time intelligence measures (`dax/02_time_intelligence.dax`): Monthly Sales, Quarterly Sales, Previous Year Sales, YoY Sales Growth %, YTD Sales.
- [x] Author profitability & ranking measures (`dax/03_profitability_and_rankings.dax`): Category Profitability, Customer Contribution %, Top Product Ranks.
- [x] Provide comprehensive `dax/VALIDATION_CHECKLIST.md` for Power BI Desktop ingestion.

### Phase 5: Power BI Desktop Report Construction (Upcoming)
- [ ] Connect Power BI Desktop to `data/cleaned/*.csv`.
- [ ] Verify data types and create Star Schema relationships in Power BI Model View.
- [ ] Mark `Date` table as Date Table.
- [ ] Import and validate DAX measures using the DAX Validation Checklist.
- [ ] Build Page 1: Executive Overview.
- [ ] Build Page 2: Sales Analysis.
- [ ] Build Page 3: Customer Analysis.
- [ ] Build Page 4: Product Analysis.
- [ ] Build Page 5: Management Insights.

### Phase 6: Verification, Documentation & Final Delivery (Upcoming)
- [ ] Visual verification of all 5 report pages in Power BI Desktop.
- [ ] Capture high-resolution visual screenshots into `reports/screenshots/`.
- [ ] Document complete User Guide and End-User walkthrough.
- [ ] Prepare final presentation slide deck summarizing analytical insights.
- [ ] Final compliance check against all `AGENTS.md` guidelines.
