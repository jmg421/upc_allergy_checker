# gui.py

import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import simpledialog
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

        # Bind window close event to ensure database connection is closed
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

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

        # Automatically focus on the UPC entry field
        self.upc_entry.focus()

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
            self.display_result("Input Error: Please enter a UPC code.\n")
            self.upc_entry.focus()
            return

        logger.info(f"Fetching product for UPC: {upc}")
        result = self.api.fetch_product(upc)
        if result is None:
            # Prompt the user to enter product name and ingredients
            self.display_result(f"Product not found for UPC: {upc}\n")
            logger.info(f"Prompting user to enter details for UPC: {upc}")
            self.prompt_for_product_info(upc)
            return

        product_name, ingredients = result
        logger.info(f"Product found: {product_name}")
        self.display_result(f"Product Name: {product_name}\n\nIngredients: {ingredients}\n\n")
        allergens_found = self.checker.check_allergens(ingredients)
        if allergens_found:
            allergen_msg = "Allergens Detected:\n" + ", ".join(allergens_found)
            self.display_result(allergen_msg + "\n")
            logger.info(f"Allergens detected: {', '.join(allergens_found)}")
        else:
            self.display_result("No allergens detected.\n")
            logger.info("No allergens detected in this product.")

        # Clear the UPC entry field
        self.upc_entry.delete(0, tk.END)
        self.upc_entry.focus()

    def prompt_for_product_info(self, upc):
        """Prompt the user to enter product name and ingredients for a given UPC."""
        # Create a new window
        self.input_window = tk.Toplevel(self.root)
        self.input_window.title("Enter Product Details")

        # Product Name Label and Entry
        product_name_label = tk.Label(self.input_window, text="Product Name:")
        product_name_label.pack(pady=(10, 0))
        self.product_name_entry = tk.Entry(self.input_window, width=50)
        self.product_name_entry.pack(pady=5)
        self.product_name_entry.focus()

        # Ingredients Label and Text
        ingredients_label = tk.Label(self.input_window, text="Ingredients:")
        ingredients_label.pack(pady=(10, 0))
        self.ingredients_text = scrolledtext.ScrolledText(self.input_window, width=40, height=10)
        self.ingredients_text.pack(pady=5)

        # Save Button
        save_button = tk.Button(self.input_window, text="Save", command=lambda: self.save_product_info(upc))
        save_button.pack(pady=10)

        # Cancel Button
        cancel_button = tk.Button(self.input_window, text="Cancel", command=self.close_input_window)
        cancel_button.pack()

        # Bind the Enter key to the save function
        self.input_window.bind('<Return>', lambda event: self.save_product_info(upc))

    def save_product_info(self, upc):
        """Save user-entered product name and ingredients to the database."""
        product_name = self.product_name_entry.get().strip()
        ingredients = self.ingredients_text.get("1.0", tk.END).strip()

        if not product_name or not ingredients:
            messagebox.showerror("Input Error", "Please enter both Product Name and Ingredients.")
            return

        # Save to the database
        self.api.db_manager.save_product(upc, product_name, ingredients)
        logger.info(f"Product saved to local database for UPC: {upc}")

        # Close the input window
        self.close_input_window()

        # Display the product and check for allergens
        self.display_result(f"Product Name: {product_name}\n\nIngredients: {ingredients}\n\n")
        allergens_found = self.checker.check_allergens(ingredients)
        if allergens_found:
            allergen_msg = "Allergens Detected:\n" + ", ".join(allergens_found)
            self.display_result(allergen_msg + "\n")
            logger.info(f"Allergens detected: {', '.join(allergens_found)}")
        else:
            self.display_result("No allergens detected.\n")
            logger.info("No allergens detected in this product.")

        # Clear the UPC entry field
        self.upc_entry.delete(0, tk.END)
        self.upc_entry.focus()

    def close_input_window(self):
        """Close the product info input window."""
        if self.input_window:
            self.input_window.destroy()
            self.input_window = None
        # Clear the UPC entry field
        self.upc_entry.delete(0, tk.END)
        self.upc_entry.focus()

    def display_result(self, text: str):
        """Display text in the result area."""
        self.result_text.config(state='normal')
        self.result_text.insert(tk.END, text + "\n")
        self.result_text.config(state='disabled')
        self.result_text.see(tk.END)  # Auto-scroll to the end

    def on_closing(self):
        """Handle window closing event to clean up resources."""
        self.api.close()  # Close the database connection
        self.root.destroy()

