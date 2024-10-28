# allergen.py

from typing import List
import re
from .config import ALLERGENS

class AllergenChecker:
    """Checks for allergens in product ingredients."""

    def __init__(self, allergens: List[str] = ALLERGENS):
        """
        Initialize the AllergenChecker with a list of allergens.

        Args:
            allergens (List[str], optional): List of allergens. Defaults to ALLERGENS from config.
        """
        self.allergens = [allergen.lower() for allergen in allergens]

    def check_allergens(self, ingredients: str) -> List[str]:
        """
        Check if any allergens are present in the ingredients.

        Args:
            ingredients (str): The ingredients text.

        Returns:
            List[str]: List of detected allergens.
        """
        detected = set()
        # Remove punctuation and split ingredients into words
        words = re.findall(r'\b\w+\b', ingredients.lower())
        for allergen in self.allergens:
            if allergen in words:
                detected.add(allergen.capitalize())
        return list(detected)

