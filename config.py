"""Configuration for Metal Prices Streamlit App"""

# API Configuration
METALS_LIVE_API_URL = "https://api.metals.live/v1/spot/metals"

# Metals to track
METALS = {
    "Steel (HRC)": "steel",
    "Copper": "copper",
    "Zinc": "zinc",
    "Aluminum": "aluminum",
    "Nickel": "nickel",
    "Iron Ore": "iron_ore",
}

# Display settings
CURRENCY = "USD"
PRICE_UPDATE_INTERVAL = 300  # seconds (5 minutes)
CHART_DAYS = 30  # Show last 30 days of data

# Database
DB_FILE = "prices.db"
