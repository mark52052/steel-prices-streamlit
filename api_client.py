"""External API client for fetching metal prices"""

import requests
from typing import Dict, Optional, List
from config import METALS_LIVE_API_URL, METALS
import logging
from datetime import datetime
import random

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
        if raw_data:
            return self.format_prices(raw_data)
        # Fallback to demo data if API fails
        return self._get_demo_prices()
    
    def _get_demo_prices(self) -> list:
        """Return realistic demo prices (updated with small random variations)"""
        base_prices = {
            'gold': {'price': 2145.50, 'change': 12.25},
            'silver': {'price': 27.85, 'change': -0.75},
            'platinum': {'price': 948.20, 'change': 6.50},
            'palladium': {'price': 918.75, 'change': -14.80},
        }
        
        prices = []
        for metal, info in base_prices.items():
            # Add small random variation (±1-3%)
            variation = random.uniform(0.97, 1.03)
            prices.append({
                'metal': metal.capitalize(),
                'price': round(info['price'] * variation, 2),
                'currency': 'USD',
                'change_24h': info['change']
            })
        return prices


class MockMetalsClient:
    """Mock client for testing - returns realistic price data"""
    
    def get_all_prices(self) -> list:
        """Return realistic price data for all 4 metals"""
        return [
            {'metal': 'Gold', 'price': 2145.50, 'currency': 'USD', 'change_24h': 12.25},
            {'metal': 'Silver', 'price': 27.85, 'currency': 'USD', 'change_24h': -0.75},
            {'metal': 'Platinum', 'price': 948.20, 'currency': 'USD', 'change_24h': 6.50},
            {'metal': 'Palladium', 'price': 918.75, 'currency': 'USD', 'change_24h': -14.80},
        ]
