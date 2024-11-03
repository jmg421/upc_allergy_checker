# cli.py

import argparse
import logging
from typing import List
from .api import ProductAPI
from .allergen import AllergenChecker

def main():
    parser = argparse.ArgumentParser(description='UPC Allergy Checker - Command Line Interface')
    parser.add_argument('upc_codes', nargs='*', help='List of UPC codes to check')
    parser.add_argument('-f', '--file', type=str, help='File containing UPC codes, one per line')
    parser.add_argument('-o', '--output', type=str, help='Output file to write the results')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)
    else:
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

    # Collect UPC codes
    upc_codes = args.upc_codes

    # Read UPC codes from file if specified
    if args.file:
        try:
            with open(args.file, 'r') as f:
                file_upc_codes = [line.strip() for line in f if line.strip()]
                upc_codes.extend(file_upc_codes)
        except IOError as e:
            logger.error(f"Unable to read UPC codes from file {args.file}: {e}")
            return

    # Remove duplicates
    upc_codes = list(set(upc_codes))

    if not upc_codes:
        logger.error("No UPC codes provided.")
        parser.print_help()
        return

    api = ProductAPI()
    checker = AllergenChecker()

    results = []

    for upc in upc_codes:
        logger.info(f"Processing UPC: {upc}")
        result = api.fetch_product(upc)
        if result is None:
            logger.warning(f"Product not found for UPC: {upc}")
            results.append({
                'upc': upc,
                'product_name': 'Product not found',
                'allergens': [],
                'status': 'Product not found'
            })
            continue

        product_name, ingredients = result
        allergens_found = checker.check_allergens(ingredients)
        if allergens_found:
            status = f"Allergens detected: {', '.join(allergens_found)}"
        else:
            status = "No allergens detected"

        results.append({
            'upc': upc,
            'product_name': product_name,
            'allergens': allergens_found,
            'status': status
        })

    # Output results
    if args.output:
        try:
            with open(args.output, 'w') as f:
                for r in results:
                    f.write(f"UPC: {r['upc']}\n")
                    f.write(f"Product Name: {r['product_name']}\n")
                    f.write(f"Status: {r['status']}\n")
                    f.write("\n")
            logger.info(f"Results written to {args.output}")
        except IOError as e:
            logger.error(f"Unable to write results to file {args.output}: {e}")
    else:
        for r in results:
            print(f"UPC: {r['upc']}")
            print(f"Product Name: {r['product_name']}")
            print(f"Status: {r['status']}")
            print()

    api.close()

if __name__ == '__main__':
    main()

