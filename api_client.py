"""External API client for fetching metal prices"""

import logging
import random
from typing import Dict, Optional

import requests

from config import METALS_LIVE_API_URL, TRADING_ECONOMICS_API_URL

logger = logging.getLogger(__name__)


class TradingEconomicsClient:
    """Client for Trading Economics commodity market quotes."""

    source_name = "Trading Economics"

    METAL_NAMES = {
        "Steel HRC": ("Steel", "US Steel"),
        "Iron Ore": ("Iron Ore",),
        "Copper": ("Copper",),
        "Aluminum": ("Aluminum",),
        "Zinc": ("Zinc",),
        "Gold": ("Gold",),
        "Silver": ("Silver",),
        "Platinum": ("Platinum",),
        "Palladium": ("Palladium",),
    }

    def __init__(self, api_key: str, base_url: str = TRADING_ECONOMICS_API_URL):
        self.api_key = api_key.strip()
        self.base_url = base_url
        self.timeout = 15
        self.available = bool(self.api_key)

    def get_commodity_quotes(self) -> Optional[list]:
        """Fetch commodity quotes from Trading Economics."""
        if not self.available:
            return None

        try:
            response = requests.get(
                self.base_url,
                params={"c": self.api_key, "f": "json"},
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, list) else None
        except requests.RequestException as e:
            logger.error(f"Error fetching prices from Trading Economics: {e}")
            return None
        except ValueError as e:
            logger.error(f"Invalid Trading Economics response: {e}")
            return None

    def format_prices(self, raw_data: list) -> list:
        """Normalize Trading Economics quote rows for the app database."""
        if not raw_data:
            return []

        prices = []
        used_names = set()
        for display_name, source_names in self.METAL_NAMES.items():
            for row in raw_data:
                row_name = str(row.get("Name", "")).strip().lower()
                if row_name not in {name.lower() for name in source_names}:
                    continue

                raw_price = row.get("Last") or row.get("Close")
                if raw_price in (None, ""):
                    continue

                unit = str(row.get("unit") or row.get("Unit") or "USD").strip()
                prices.append({
                    "metal": display_name,
                    "price": round(float(raw_price), 2),
                    "currency": unit or "USD",
                    "change_24h": row.get("DailyChange", 0) or 0,
                })
                used_names.add(display_name)
                break

        logger.info("Trading Economics matched commodities: %s", sorted(used_names))
        return prices

    def get_all_prices(self) -> list:
        """Get all configured metal prices available from Trading Economics."""
        raw_data = self.get_commodity_quotes()
        return self.format_prices(raw_data or [])


class YFinanceClient:
    """Client for Yahoo Finance - Real metal prices from futures markets"""

    source_name = "Yahoo Finance Futures"

    # Futures ticker symbols for metals
    METAL_SYMBOLS = {
        'Steel HRC': 'HRC=F',    # CME US Midwest HRC Steel futures
        'Iron Ore': 'TIO=F',     # SGX TSI Iron Ore futures
        'Copper': 'HG=F',        # COMEX Copper futures
        'Aluminum': 'ALI=F',     # CME Aluminum futures
        'Zinc': 'ZNC=F',         # COMEX Zinc futures
        'Gold': 'GC=F',          # COMEX Gold futures
        'Silver': 'SI=F',        # COMEX Silver futures
        'Platinum': 'PL=F',      # NYMEX Platinum futures
        'Palladium': 'PA=F',     # NYMEX Palladium futures
    }

    def __init__(self):
        try:
            import yfinance
            self.yfinance = yfinance
            self.available = True
        except ImportError:
            logger.error("yfinance not installed")
            self.available = False

    def get_all_prices(self) -> list:
        """Fetch real metal prices from Yahoo Finance futures"""
        if not self.available:
            return []

        prices = []
        for metal_name, symbol in self.METAL_SYMBOLS.items():
            try:
                ticker = self.yfinance.Ticker(symbol)
                data = ticker.history(period="5d")

                if not data.empty:
                    latest_price = float(data['Close'].iloc[-1])
                    previous_price = float(data['Close'].iloc[-2]) if len(data) > 1 else latest_price
                    prices.append({
                        'metal': metal_name,
                        'price': round(latest_price, 2),
                        'currency': 'USD',
                        'change_24h': round(latest_price - previous_price, 2)
                    })
                    logger.info(f"{metal_name}: ${latest_price}")
                else:
                    logger.warning(f"{metal_name}: No data available")
            except Exception as e:
                logger.error(f"Error fetching {metal_name}: {e}")

        return prices

class MetalsLiveClient:
    """Client for Metals.live API - Free metal prices"""

    source_name = "Metals.live"

    def __init__(self, base_url: str = METALS_LIVE_API_URL):
        self.base_url = base_url
        self.timeout = 10

    def get_spot_prices(self) -> Optional[Dict]:
        """
        Fetch current spot prices from Metals.live API
        Returns: Dict of metal prices in USD per ounce/ton
        """
        try:
            response = requests.get(self.base_url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching prices from Metals.live: {e}")
            return None

    def format_prices(self, raw_data: Dict) -> list:
        """
        Format raw API response into standardized format
        Returns: List of dicts with 'metal', 'price', 'currency'
        """
        if not raw_data:
            return []

        prices = []
        # metals.live returns data like: {"gold": {...}, "silver": {...}}
        for metal, data in raw_data.items():
            if isinstance(data, dict) and 'usd' in data:
                prices.append({
                    'metal': metal.capitalize(),
                    'price': float(data['usd']),
                    'currency': 'USD',
                    'change_24h': data.get('gdmUsd', 0)
                })
        return prices

    def get_all_prices(self) -> list:
        """Get and format all current metal prices"""
        raw_data = self.get_spot_prices()
        if raw_data:
            return self.format_prices(raw_data)
        return []


class MockMetalsClient:
    """Mock client for testing - returns realistic price data"""

    source_name = "Demo Data"

    def get_all_prices(self) -> list:
        """Return realistic price data for all 4 metals"""
        base_prices = {
            'Steel HRC': {'price': 845.00, 'change': 8.00},
            'Iron Ore': {'price': 105.25, 'change': -1.20},
            'Copper': {'price': 4.72, 'change': 0.04},
            'Aluminum': {'price': 2575.00, 'change': 12.00},
            'Zinc': {'price': 2940.00, 'change': -18.00},
            'Gold': {'price': 2145.50, 'change': 12.25},
            'Silver': {'price': 27.85, 'change': -0.75},
            'Platinum': {'price': 948.20, 'change': 6.50},
            'Palladium': {'price': 918.75, 'change': -14.80},
        }

        prices = []
        for metal, info in base_prices.items():
            variation = random.uniform(0.99, 1.01)
            prices.append({
                'metal': metal,
                'price': round(info['price'] * variation, 2),
                'currency': 'USD',
                'change_24h': info['change']
            })
        return prices
