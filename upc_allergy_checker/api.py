# api.py

import requests
from typing import Optional, Tuple
import logging
from .config import API_BASE_URL
from .db import DatabaseManager

logger = logging.getLogger(__name__)

class ProductAPI:
    """Handles interactions with the Open Food Facts API and local database."""

    def __init__(self):
        self.db_manager = DatabaseManager()

    def close(self):
        self.db_manager.close()

    def fetch_product(self, upc: str) -> Optional[Tuple[str, str]]:
        """
        Fetch product details using UPC code. Checks the local database first,
        then the API if not found locally.
        """
        # Check the database first
        product = self.db_manager.get_product(upc)
        if product:
            logger.info(f"Product found in local database for UPC: {upc}")
            return product

        # Fetch from API if not found in database
        url = API_BASE_URL.format(upc)
        try:
            logger.info(f"Requesting URL: {url}")
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            if data.get("status") == 1:
                product_data = data.get("product", {})
                product_name = product_data.get("product_name", "N/A")
                ingredients_text = product_data.get("ingredients_text", "")
                if not ingredients_text:
                    # Try alternative field
                    ingredients_text = product_data.get("ingredients_text_en", "")
                logger.debug(f"Product name: {product_name}, Ingredients: {ingredients_text}")

                # Save to database
                self.db_manager.save_product(upc, product_name, ingredients_text)
                logger.info(f"Product saved to local database for UPC: {upc}")
                return product_name, ingredients_text
            else:
                logger.warning(f"Product not found in API for UPC: {upc}")
                return None
        except requests.RequestException as e:
            logger.error(f"Error fetching product from API: {e}")
            return None

