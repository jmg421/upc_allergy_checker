# UPC Allergy Checker

A Python application that scans UPC barcodes, retrieves product information, and flags any allergens based on the user's sensitivity profile. Can be used with a variety of standard UPC scanners, e.g., the Tera Barcode Scanner at https://tera-digital.com/products/2d-barcode-scanner-hw0002.

<img width="443" alt="image" src="https://github.com/user-attachments/assets/90275689-4360-4de9-b385-2f0c3729b0b0">
<img height="443" alt="image" src="https://github.com/user-attachments/assets/bb5e184e-fa13-456b-9d31-513777270aea">

## Features

- **Graphical User Interface (GUI)**: User-friendly interface for scanning and checking products.
- **Command Line Interface (CLI)**: Check products directly from the terminal.
- **Continuous Scanning**: Scan multiple UPC codes in succession without pop-up interruptions.
- **Allergen Detection**: Automatically checks for allergens and displays results.
- **Product Lookup**: Fetches product details and ingredients from the Open Food Facts API.
- **Results Display**: Displays all results in the GUI's result area or outputs to the terminal for review.
- **Results Saved to Database**: All scanned data is stored in an SQLite3 database (`~/upc_allergy_checker.db` by default).

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/jmg421/upc_allergy_checker.git
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

### Graphical User Interface (GUI)

Run the GUI application using:

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

### Command Line Interface (CLI)

The UPC Allergy Checker also includes a command line interface (CLI) that allows you to check products directly from the terminal.

Run the CLI application using:

```bash
python -m upc_allergy_checker.cli [options] [upc_codes ...]
```

Alternatively, if installed via pip, you can run:

```bash
allergy_checker_cli [options] [upc_codes ...]
```

#### Options

```bash
$ python -m upc_allergy_checker.cli -h

usage: cli.py [-h] [-f FILE] [-o OUTPUT] [-v] [upc_codes ...]

UPC Allergy Checker - Command Line Interface

positional arguments:
  upc_codes            List of UPC codes or "UPC,Product Name" pairs to check

options:
  -h, --help           show this help message and exit
  -f FILE, --file FILE
                       File containing "UPC,Product Name" pairs, one per line
  -o OUTPUT, --output OUTPUT
                       Output file to write the results
  -v, --verbose        Enable verbose output
```

#### Examples

**Check a Single UPC Code:**

```bash
python -m upc_allergy_checker.cli 012345678905
```

**Check Multiple UPC Codes:**

```bash
python -m upc_allergy_checker.cli 012345678905 012345678906 012345678907
```

**Check UPC Codes from a File:**

Create a text file `upc_list.txt` with one UPC code per line or "UPC,Product Name" pairs:

```
012345678905,Product A
012345678906,Product B
012345678907
```

Run the CLI with the file:

```bash
python -m upc_allergy_checker.cli -f upc_list.txt
```

**Save Output to a File:**

```bash
python -m upc_allergy_checker.cli 012345678905 -o results.txt
```

**Enable Verbose Output:**

```bash
python -m upc_allergy_checker.cli 012345678905 -v
```

## Configuration

The list of allergens can be modified in the `config.py` file within the `upc_allergy_checker` package.

```python
# config.py

# Open Food Facts API base URL
API_BASE_URL = "https://world.openfoodfacts.org/api/v0/product/{}.json"

# List of allergens the user is sensitive to
ALLERGENS = [
    "garlic",
    "peanut",
    "pecan",
    "walnut",
    "sesame",
    "cashew",
    "almond",
    "hazelnut",
    "pistachio",
    "soybean",
    "soy",   # Common alternative
    "soya",  # Common alternative
]
```

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

