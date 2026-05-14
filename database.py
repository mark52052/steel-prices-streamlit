"""Database operations for storing price history"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
from config import DB_FILE
import os

class PriceDatabase:
    def __init__(self, db_file: str = DB_FILE):
        self.db_file = db_file
        self.init_db()

    def init_db(self):
        """Initialize database with prices table"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metal_name TEXT NOT NULL,
                    price_usd REAL NOT NULL,
                    currency TEXT DEFAULT 'USD',
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_metal_time 
                ON prices (metal_name, timestamp)
            """)
            conn.commit()

    def insert_price(self, metal_name: str, price_usd: float, currency: str = "USD"):
        """Insert a price record"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO prices (metal_name, price_usd, currency)
                VALUES (?, ?, ?)
            """, (metal_name, price_usd, currency))
            conn.commit()

    def insert_batch_prices(self, prices: List[Dict]):
        """Insert multiple price records"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            for item in prices:
                cursor.execute("""
                    INSERT INTO prices (metal_name, price_usd, currency)
                    VALUES (?, ?, ?)
                """, (item['metal'], item['price'], item.get('currency', 'USD')))
            conn.commit()

    def get_latest_prices(self) -> Dict[str, Dict]:
        """Get latest price for each metal"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT metal_name, price_usd, currency, timestamp
                FROM prices
                WHERE (metal_name, timestamp) IN (
                    SELECT metal_name, MAX(timestamp)
                    FROM prices
                    GROUP BY metal_name
                )
                ORDER BY metal_name
            """)
            results = cursor.fetchall()
            return {
                row[0]: {'price': row[1], 'currency': row[2], 'timestamp': row[3]}
                for row in results
            }

    def get_price_history(self, metal_name: str, days: int = 30) -> List[Dict]:
        """Get price history for a metal"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT metal_name, price_usd, currency, timestamp
                FROM prices
                WHERE metal_name = ? 
                AND timestamp >= datetime('now', '-' || ? || ' days')
                ORDER BY timestamp ASC
            """, (metal_name, days))
            results = cursor.fetchall()
            return [
                {'metal': row[0], 'price': row[1], 'currency': row[2], 'timestamp': row[3]}
                for row in results
            ]

    def clear_old_data(self, days: int = 90):
        """Delete price data older than specified days"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM prices
                WHERE timestamp < datetime('now', '-' || ? || ' days')
            """, (days,))
            conn.commit()
