# UPC Allergy Checker

A Python application that scans UPC barcodes, retrieves product information, and flags any allergens based on the user's sensitivity profile.

<img width="443" alt="image" src="https://github.com/user-attachments/assets/90275689-4360-4de9-b385-2f0c3729b0b0">

## Features

- **UPC Scanning**: Input UPC codes via a barcode scanner or manually.
- **Product Lookup**: Fetches product details and ingredients from the Open Food Facts API.
- **Allergen Detection**: Flags products containing allergens the user is sensitive to.
- **User-Friendly GUI**: Simple interface built with `tkinter`.
- **Results Saved to Database**: All data that is scanned and looked up is stored in a Sqlite3 database (~/.upc_allergy_checker.db by default)

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

