"""External API client for fetching metal prices"""

import requests
from typing import Dict, Optional
from config import METALS_LIVE_API_URL, METALS
import logging

logger = logging.getLogger(__name__)

class MetalsLiveClient:
    """Client for Metals.live API - Free metal prices"""
    
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
        return self.format_prices(raw_data) if raw_data else []


class MockMetalsClient:
    """Mock client for testing (when API is unavailable)"""
    
    def get_all_prices(self) -> list:
        """Return mock price data"""
        return [
            {'metal': 'Gold', 'price': 2150.50, 'currency': 'USD', 'change_24h': 15.25},
            {'metal': 'Silver', 'price': 28.30, 'currency': 'USD', 'change_24h': -0.50},
            {'metal': 'Copper', 'price': 4.25, 'currency': 'USD', 'change_24h': 0.10},
            {'metal': 'Aluminum', 'price': 2750.00, 'currency': 'USD', 'change_24h': -5.00},
            {'metal': 'Zinc', 'price': 2650.00, 'currency': 'USD', 'change_24h': 20.00},
        ]
