# api.py

import requests
from typing import Optional, Tuple
import logging
from .config import API_BASE_URL

logger = logging.getLogger(__name__)

class ProductAPI:
    """Handles interactions with the Open Food Facts API."""

    @staticmethod
    def fetch_product(upc: str) -> Optional[Tuple[str, str]]:
        """
        Fetch product details using UPC code.

        Args:
            upc (str): The UPC code of the product.

        Returns:
            Optional[Tuple[str, str]]: Returns a tuple of (product_name, ingredients_text) if found, else None.
        """
        url = API_BASE_URL.format(upc)
        try:
            logger.info(f"Requesting URL: {url}")
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Raise HTTPError for bad responses
            data = response.json()
            if data.get("status") == 1:
                product = data.get("product", {})
                product_name = product.get("product_name", "N/A")
                ingredients_text = product.get("ingredients_text", "")
                if not ingredients_text:
                    # Try alternative field
                    ingredients_text = product.get("ingredients_text_en", "")
                logger.debug(f"Product name: {product_name}, Ingredients: {ingredients_text}")
                return product_name, ingredients_text
            else:
                logger.warning(f"Product not found for UPC: {upc}")
                return None
        except requests.RequestException as e:
            logger.error(f"Error fetching product: {e}")
            return None

