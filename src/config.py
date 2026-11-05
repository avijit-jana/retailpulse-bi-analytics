"""Configuration settings and constants for synthetic data generation and validation."""

from datetime import date

# Random seed for full reproducibility
DEFAULT_RANDOM_SEED = 42

# Analytical date range (multi-year coverage: 2022-01-01 to 2024-12-31)
DEFAULT_START_DATE = date(2022, 1, 1)
DEFAULT_END_DATE = date(2024, 12, 31)

# Default generation counts
DEFAULT_NUM_CUSTOMERS = 1000
DEFAULT_NUM_ORDERS = 15000  # Will yield ~25,000+ line items with multi-item orders

# Customer Segments
CUSTOMER_SEGMENTS = ["Consumer", "Corporate", "Home Office"]
SEGMENT_WEIGHTS = [0.52, 0.30, 0.18]

# Regions, States, and Cities
REGION_HIERARCHY = [
    # East
    {"RegionID": "REG-101", "Region": "East", "State": "New York", "City": "New York City"},
    {"RegionID": "REG-102", "Region": "East", "State": "Pennsylvania", "City": "Philadelphia"},
    {"RegionID": "REG-103", "Region": "East", "State": "Massachusetts", "City": "Boston"},
    # West
    {"RegionID": "REG-201", "Region": "West", "State": "California", "City": "Los Angeles"},
    {"RegionID": "REG-202", "Region": "West", "State": "California", "City": "San Francisco"},
    {"RegionID": "REG-203", "Region": "West", "State": "Washington", "City": "Seattle"},
    # Central
    {"RegionID": "REG-301", "Region": "Central", "State": "Illinois", "City": "Chicago"},
    {"RegionID": "REG-302", "Region": "Central", "State": "Texas", "City": "Dallas"},
    {"RegionID": "REG-303", "Region": "Central", "State": "Texas", "City": "Houston"},
    # South
    {"RegionID": "REG-401", "Region": "South", "State": "Florida", "City": "Miami"},
    {"RegionID": "REG-402", "Region": "South", "State": "Georgia", "City": "Atlanta"},
    {"RegionID": "REG-403", "Region": "South", "State": "North Carolina", "City": "Charlotte"},
]

# Product Catalog Definition (Category -> SubCategory -> Brands with typical cost ranges)
PRODUCT_CATALOG = [
    # Technology
    {"Category": "Technology", "SubCategory": "Laptops", "Brand": "TechPro", "MinCost": 400.0, "MaxCost": 1200.0, "Count": 12},
    {"Category": "Technology", "SubCategory": "Smartphones", "Brand": "Apex", "MinCost": 250.0, "MaxCost": 800.0, "Count": 10},
    {"Category": "Technology", "SubCategory": "Accessories", "Brand": "CableCraft", "MinCost": 12.0, "MaxCost": 60.0, "Count": 15},
    {"Category": "Technology", "SubCategory": "Printers", "Brand": "PrintMaster", "MinCost": 90.0, "MaxCost": 350.0, "Count": 8},
    # Furniture
    {"Category": "Furniture", "SubCategory": "Chairs", "Brand": "ErgoComfort", "MinCost": 60.0, "MaxCost": 280.0, "Count": 12},
    {"Category": "Furniture", "SubCategory": "Desks", "Brand": "WoodWork", "MinCost": 120.0, "MaxCost": 500.0, "Count": 10},
    {"Category": "Furniture", "SubCategory": "Bookcases", "Brand": "OakLine", "MinCost": 80.0, "MaxCost": 320.0, "Count": 8},
    {"Category": "Furniture", "SubCategory": "Furnishings", "Brand": "DecoStyle", "MinCost": 15.0, "MaxCost": 90.0, "Count": 12},
    # Office Supplies
    {"Category": "Office Supplies", "SubCategory": "Storage", "Brand": "StoreIt", "MinCost": 18.0, "MaxCost": 95.0, "Count": 12},
    {"Category": "Office Supplies", "SubCategory": "Paper", "Brand": "PureSheet", "MinCost": 8.0, "MaxCost": 35.0, "Count": 10},
    {"Category": "Office Supplies", "SubCategory": "Binders", "Brand": "SecureBind", "MinCost": 5.0, "MaxCost": 22.0, "Count": 10},
    {"Category": "Office Supplies", "SubCategory": "Art", "Brand": "ColorCraft", "MinCost": 6.0, "MaxCost": 45.0, "Count": 10},
    {"Category": "Office Supplies", "SubCategory": "Appliances", "Brand": "OfficeVolt", "MinCost": 35.0, "MaxCost": 160.0, "Count": 8},
]

# Standard Discount Brackets
DISCOUNT_CHOICES = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
DISCOUNT_WEIGHTS = [0.45, 0.18, 0.15, 0.10, 0.07, 0.03, 0.02]
