"""Generates the Fact Sales transactions dataset."""

from datetime import date
import numpy as np
import pandas as pd
from typing import List, Dict
from src.config import DISCOUNT_CHOICES, DISCOUNT_WEIGHTS

def generate_sales(
    num_orders: int,
    customers_df: pd.DataFrame,
    products_df: pd.DataFrame,
    regions_df: pd.DataFrame,
    start_date: date,
    end_date: date,
    seed: int = 42
) -> pd.DataFrame:
    """
    Generates realistic retail sales transactions.
    Schema according to AGENTS.md:
    OrderID, OrderDate, CustomerID, ProductID, RegionID, Quantity, UnitPrice, Discount

    Key characteristics:
    - Multi-line item orders (1-4 line items per order) sharing OrderID, OrderDate, CustomerID, RegionID.
    - Full referential integrity against customers_df, products_df, regions_df.
    - Category-sensitive markups (Technology ~20-50%, Furniture ~30-65%, Office Supplies ~40-80%).
    - Discrete discount tiers (0% to 30%).
    - Seasonal trends (Q4 holiday ramp-up and YoY business growth).
    """
    rng = np.random.default_rng(seed)

    # Pre-build lookup maps for performance and data consistency
    # Map Customer to their home RegionID via City & State match
    geo_to_region = {}
    for _, reg_row in regions_df.iterrows():
        geo_to_region[(reg_row["State"], reg_row["City"])] = reg_row["RegionID"]

    cust_to_region = {}
    for _, cust_row in customers_df.iterrows():
        geo_key = (cust_row["State"], cust_row["City"])
        cust_to_region[cust_row["CustomerID"]] = geo_to_region.get(geo_key, regions_df.iloc[0]["RegionID"])

    # Product attributes lookup
    prod_lookup = {}
    for _, prod_row in products_df.iterrows():
        prod_lookup[prod_row["ProductID"]] = {
            "Category": prod_row["Category"],
            "CostPrice": float(prod_row["CostPrice"])
        }

    customer_ids = customers_df["CustomerID"].values
    product_ids = products_df["ProductID"].values

    # Generate dates across the span with weighted seasonality (Q4 boost, year-over-year growth)
    all_dates = pd.date_range(start=start_date, end=end_date, freq="D")

    # Seasonality weights: base weight + Q4 boost + weekend boost + yearly growth
    date_weights = []
    for d in all_dates:
        w = 1.0
        # Yearly growth (e.g. 2022: 1.0, 2023: 1.15, 2024: 1.30)
        year_offset = d.year - start_date.year
        w *= (1.0 + 0.15 * year_offset)
        # Q4 boost (Oct-Dec)
        if d.month in [10, 11, 12]:
            w *= 1.45
        # Weekend slight boost
        if d.weekday() in [5, 6]:
            w *= 1.2
        date_weights.append(w)

    date_weights = np.array(date_weights)
    date_weights /= date_weights.sum()

    # Sample order dates
    selected_date_indices = rng.choice(len(all_dates), size=num_orders, p=date_weights)
    order_dates = [all_dates[idx].strftime("%Y-%m-%d") for idx in selected_date_indices]

    # Assign customers to orders (Pareto-like customer frequency: some repeat buyers)
    # Using Dirichlet or power-law distribution over customer indices
    cust_weights = rng.pareto(a=2.0, size=len(customer_ids)) + 0.1
    cust_weights /= cust_weights.sum()
    order_customers = rng.choice(customer_ids, size=num_orders, p=cust_weights)

    records = []
    for order_idx in range(num_orders):
        order_id = f"ORD-{order_idx + 1:07d}"
        order_date = order_dates[order_idx]
        cust_id = order_customers[order_idx]
        reg_id = cust_to_region[cust_id]

        # Determine number of items in this order (1 to 4 items)
        num_items = rng.choice([1, 2, 3, 4], p=[0.60, 0.25, 0.10, 0.05])

        # Sample distinct products for this order
        chosen_prods = rng.choice(product_ids, size=num_items, replace=False)

        for prod_id in chosen_prods:
            prod_info = prod_lookup[prod_id]
            cost_price = prod_info["CostPrice"]
            cat = prod_info["Category"]

            # Category-based markup
            if cat == "Technology":
                markup = rng.uniform(0.20, 0.45)
            elif cat == "Furniture":
                markup = rng.uniform(0.30, 0.60)
            else: # Office Supplies
                markup = rng.uniform(0.40, 0.85)

            unit_price = round(cost_price * (1.0 + markup), 2)

            # Order quantity: 1 to 5 units standard, occasional bulk
            quantity = int(rng.choice([1, 2, 3, 4, 5, 8, 10], p=[0.45, 0.25, 0.15, 0.08, 0.05, 0.01, 0.01]))

            # Discount
            discount = float(rng.choice(DISCOUNT_CHOICES, p=DISCOUNT_WEIGHTS))

            records.append({
                "OrderID": order_id,
                "OrderDate": order_date,
                "CustomerID": cust_id,
                "ProductID": prod_id,
                "RegionID": reg_id,
                "Quantity": quantity,
                "UnitPrice": unit_price,
                "Discount": discount
            })

    sales_df = pd.DataFrame(records)
    # Sort chronologically by OrderDate and OrderID
    sales_df = sales_df.sort_values(by=["OrderDate", "OrderID"]).reset_index(drop=True)
    return sales_df[["OrderID", "OrderDate", "CustomerID", "ProductID", "RegionID", "Quantity", "UnitPrice", "Discount"]]
