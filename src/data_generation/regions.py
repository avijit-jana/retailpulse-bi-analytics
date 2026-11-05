"""Generates the Regions dimension dataset."""

import pandas as pd
from typing import List, Dict
from src.config import REGION_HIERARCHY

def generate_regions(regions_data: List[Dict[str, str]] = None) -> pd.DataFrame:
    """
    Creates the Regions dimension dataframe.
    Schema: RegionID, Region, State, City
    """
    if regions_data is None:
        regions_data = REGION_HIERARCHY

    df = pd.DataFrame(regions_data)
    # Ensure correct column ordering according to AGENTS.md
    df = df[["RegionID", "Region", "State", "City"]]
    return df
