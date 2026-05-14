"""Configuration for Metal Prices Streamlit App"""

import os

# API Configuration
METALS_LIVE_API_URL = "https://api.metals.live/v1/spot/metals"
TRADING_ECONOMICS_API_URL = "https://api.tradingeconomics.com/markets/commodities"
TRADING_ECONOMICS_API_KEY = os.getenv("TRADING_ECONOMICS_API_KEY", "")

# Metals to track. Not every provider supports every market; clients return
# the subset they can fetch and the UI keeps the full watchlist available.
METALS = {
    "Steel HRC": "steel",
    "Iron Ore": "iron-ore",
    "Copper": "copper",
    "Aluminum": "aluminum",
    "Zinc": "zinc",
    "Gold": "gold",
    "Silver": "silver",
    "Platinum": "platinum",
    "Palladium": "palladium",
}

# Display settings
CURRENCY = "USD"
PRICE_UPDATE_INTERVAL = 300  # seconds (5 minutes)
CHART_DAYS = 30  # Show last 30 days of data

# Database
DB_FILE = "prices.db"
