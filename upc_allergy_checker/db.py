# ./upc_allergy_checker/db.py

import sqlite3
import os
from typing import Optional, Tuple

DB_PATH = os.path.expanduser("~/.upc_allergy_checker.db")

class DatabaseManager:
    """Manages database operations."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()

    def create_tables(self):
        """Create tables if they don't exist."""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                upc TEXT PRIMARY KEY,
                product_name TEXT NOT NULL,
                ingredients TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def get_product(self, upc: str) -> Optional[Tuple[str, str]]:
        """Retrieve product details by UPC from the database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT product_name, ingredients FROM products WHERE upc = ?", (upc,))
        result = cursor.fetchone()
        return result if result else None

    def save_product(self, upc: str, product_name: str, ingredients: str):
        """Save a new product to the database."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO products (upc, product_name, ingredients) VALUES (?, ?, ?)",
            (upc, product_name, ingredients)
        )
        self.conn.commit()

    def close(self):
        """Close the database connection."""
        self.conn.close()

