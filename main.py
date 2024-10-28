# main.py

import tkinter as tk
from .gui import AllergyCheckerGUI

def main():
    root = tk.Tk()
    app = AllergyCheckerGUI(root)
    root.mainloop()

