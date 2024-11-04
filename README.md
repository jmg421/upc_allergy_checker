# UPC Allergy Checker

A Python application that scans UPC barcodes, retrieves product information, and flags any allergens based on the user's sensitivity profile. Can be used with a variety of standard UPC scanners, e.g., the Tera Barcode Scanner at https://tera-digital.com/products/2d-barcode-scanner-hw0002.

<img width="443" alt="image" src="https://github.com/user-attachments/assets/90275689-4360-4de9-b385-2f0c3729b0b0">
<img height="443" alt="image" src="https://github.com/user-attachments/assets/bb5e184e-fa13-456b-9d31-513777270aea">

## Features

- **Continuous Scanning**: Scan multiple UPC codes in succession without pop-up interruptions.
- **Allergen Detection**: Automatically checks for allergens and displays results in the GUI.
- **Product Lookup**: Fetches product details and ingredients from the Open Food Facts API.
- **Results Display**: Displays all results in the GUI's result area for easy review.
- **Results Saved to Database**: All scanned data is stored in an SQLite3 database (`~/.upc_allergy_checker.db` by default).

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/upc_allergy_checker.git
   cd upc_allergy_checker
   ```

2. **Create a Virtual Environment**

   It's recommended to use a virtual environment to manage dependencies.

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   Alternatively, install the package with pip:

   ```bash
   pip install .
   ```

## Usage

Run the application using:

```bash
python -m upc_allergy_checker
```

Alternatively, if installed via pip, you can run:

```bash
allergy_checker
```

**Scanning UPC Codes:**

- Ensure your cursor is focused on the "Scan UPC" entry field.
- Use a barcode scanner to scan the UPC code, or manually enter it.
- The application will automatically process the UPC code, display the results, and be ready for the next scan without any additional input.

## Configuration

The list of allergens can be modified in the `config.py` file within the `upc_allergy_checker` package.

## Troubleshooting

If you encounter issues with the GUI not displaying or `tkinter` not working:

- Ensure that you are running the script with the correct Python interpreter.
  - Run `which python` (Unix) or `where python` (Windows) to check the path.
  - Use `python -c "import sys; print(sys.executable)"` to see which Python is being used.

- Verify that `tkinter` is installed for your Python installation.
  - On Ubuntu/Debian, you may need to install it using:
    ```bash
    sudo apt-get install python3-tk
    ```

- If you're using a virtual environment, ensure that `tkinter` is installed in the global Python environment since it's part of the standard library.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

