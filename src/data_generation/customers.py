"""Generates the Customers dimension dataset."""

import numpy as np
import pandas as pd
from faker import Faker
from src.config import CUSTOMER_SEGMENTS, SEGMENT_WEIGHTS

def generate_customers(num_customers: int, regions_df: pd.DataFrame, seed: int = 42) -> pd.DataFrame:
    """
    Generates realistic synthetic customers.
    Schema: CustomerID, CustomerName, Segment, Age, Gender, City, State
    Ensures City and State map consistently to valid geography from regions_df.
    """
    fake = Faker()
    Faker.seed(seed)
    rng = np.random.default_rng(seed)

    # Distinct city-state combinations from regions_df to ensure geographical alignment
    geo_locations = regions_df[["State", "City"]].drop_duplicates().to_dict("records")

    customers = []
    customer_ids = [f"CUST-{i:05d}" for i in range(1, num_customers + 1)]
    segments = rng.choice(CUSTOMER_SEGMENTS, size=num_customers, p=SEGMENT_WEIGHTS)
    ages = rng.integers(18, 76, size=num_customers)
    genders = rng.choice(["Male", "Female", "Non-Binary"], size=num_customers, p=[0.49, 0.49, 0.02])

    for i in range(num_customers):
        cust_id = customer_ids[i]
        gender = genders[i]
        if gender == "Male":
            name = fake.name_male()
        elif gender == "Female":
            name = fake.name_female()
        else:
            name = fake.name()

        # Pick realistic geo matching region
        geo = geo_locations[rng.integers(0, len(geo_locations))]

        customers.append({
            "CustomerID": cust_id,
            "CustomerName": name,
            "Segment": segments[i],
            "Age": int(ages[i]),
            "Gender": gender,
            "City": geo["City"],
            "State": geo["State"]
        })

    df = pd.DataFrame(customers)
    return df[["CustomerID", "CustomerName", "Segment", "Age", "Gender", "City", "State"]]
