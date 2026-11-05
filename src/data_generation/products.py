"""Generates the Products dimension dataset."""

import numpy as np
import pandas as pd
from typing import List, Dict
from src.config import PRODUCT_CATALOG

def generate_products(catalog_config: List[Dict] = None, seed: int = 42) -> pd.DataFrame:
    """
    Generates synthetic product catalog.
    Schema: ProductID, ProductName, Category, SubCategory, Brand, CostPrice
    """
    if catalog_config is None:
        catalog_config = PRODUCT_CATALOG

    rng = np.random.default_rng(seed)
    products = []
    prod_counter = 1

    for item in catalog_config:
        category = item["Category"]
        subcat = item["SubCategory"]
        brand = item["Brand"]
        min_cost = item["MinCost"]
        max_cost = item["MaxCost"]
        count = item["Count"]

        for i in range(1, count + 1):
            product_id = f"PROD-{prod_counter:04d}"
            product_name = f"{brand} {subcat.rstrip('s')} Model-{chr(65 + (i % 26))}{i*10}"
            # Realistic cost price with standard rounding
            cost_price = round(float(rng.uniform(min_cost, max_cost)), 2)

            products.append({
                "ProductID": product_id,
                "ProductName": product_name,
                "Category": category,
                "SubCategory": subcat,
                "Brand": brand,
                "CostPrice": cost_price
            })
            prod_counter += 1

    df = pd.DataFrame(products)
    return df[["ProductID", "ProductName", "Category", "SubCategory", "Brand", "CostPrice"]]
