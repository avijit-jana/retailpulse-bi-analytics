"""Generates the Date dimension dataset."""

from datetime import date
import pandas as pd

def generate_dates(start_date: date, end_date: date) -> pd.DataFrame:
    """
    Generates Date dimension table.
    Schema according to AGENTS.md:
    Date, Year, Quarter, Month, MonthNumber, Week
    """
    date_range = pd.date_range(start=start_date, end=end_date, freq="D")

    df = pd.DataFrame({"Date": date_range})
    df["Year"] = df["Date"].dt.year
    df["Quarter"] = "Q" + df["Date"].dt.quarter.astype(str)
    df["Month"] = df["Date"].dt.strftime("%B")
    df["MonthNumber"] = df["Date"].dt.month
    df["Week"] = df["Date"].dt.isocalendar().week.astype(int)

    # Format Date as YYYY-MM-DD string for clean serialization
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

    return df[["Date", "Year", "Quarter", "Month", "MonthNumber", "Week"]]
