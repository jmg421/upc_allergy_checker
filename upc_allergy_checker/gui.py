# gui.py

import tkinter as tk
from tkinter import messagebox, scrolledtext
import logging
from .api import ProductAPI
from .allergen import AllergenChecker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AllergyCheckerGUI:
    """Graphical User Interface for the UPC Allergy Checker application."""

    def __init__(self, root):
        self.root = root
        self.root.title("UPC Allergy Checker")
        self.api = ProductAPI()
        self.checker = AllergenChecker()

        self.create_widgets()

    def create_widgets(self):
        """Create and arrange GUI widgets."""
        # UPC Input Frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        upc_label = tk.Label(input_frame, text="Scan UPC:")
        upc_label.pack(side=tk.LEFT, padx=5)

        self.upc_entry = tk.Entry(input_frame, width=20, font=('Arial', 14))
        self.upc_entry.pack(side=tk.LEFT, padx=5)
        self.upc_entry.bind("<Return>", self.process_upc)  # Bind Enter key

        # Fetch Button
        fetch_button = tk.Button(self.root, text="Check Product", command=self.process_upc)
        fetch_button.pack(pady=5)

        # Result Display
        self.result_text = scrolledtext.ScrolledText(self.root, width=60, height=20, state='disabled', wrap=tk.WORD)
        self.result_text.pack(pady=10)

    def process_upc(self, event=None):
        """Handle UPC input, fetch product details, and check for allergens."""
        upc = self.upc_entry.get().strip()
        if not upc:
            messagebox.showwarning("Input Error", "Please enter a UPC code.")
            return

        logger.info(f"Fetching product for UPC: {upc}")
        result = self.api.fetch_product(upc)
        if result is None:
            self.display_result(f"Product not found for UPC: {upc}\n")
            messagebox.showerror("Error", "Product not found.")
            return

        product_name, ingredients = result
        logger.info(f"Product found: {product_name}")
        self.display_result(f"Product Name: {product_name}\n\nIngredients: {ingredients}\n\n")

        allergens_found = self.checker.check_allergens(ingredients)
        if allergens_found:
            allergen_msg = "Allergens Detected:\n" + ", ".join(allergens_found)
            self.display_result(allergen_msg)
            messagebox.showerror("Allergen Alert", f"The following allergens were detected: {', '.join(allergens_found)}")
        else:
            self.display_result("No allergens detected.")
            messagebox.showinfo("Safe", "No allergens detected in this product.")

    def display_result(self, text: str):
        """Display text in the result area."""
        self.result_text.config(state='normal')
        self.result_text.insert(tk.END, text + "\n")
        self.result_text.config(state='disabled')
        self.result_text.see(tk.END)  # Auto-scroll to the end

