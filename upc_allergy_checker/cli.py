# cli.py

import argparse
import logging
from upc_allergy_checker.api import ProductAPI
from upc_allergy_checker.allergen import AllergenChecker

def main():
    parser = argparse.ArgumentParser(description='UPC Allergy Checker - Command Line Interface')
    parser.add_argument('upc_codes', nargs='*', help='List of UPC codes or "UPC,Product Name" pairs to check')
    parser.add_argument('-f', '--file', type=str, help='File containing "UPC,Product Name" pairs, one per line')
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

    records = []

    # Process UPC codes from command line arguments
    for item in args.upc_codes:
        if not item.strip():
            continue
        upc, *product_name = item.strip().split(',', 1)
        upc = upc.strip()
        product_name = product_name[0].strip() if product_name else ''
        records.append({'upc': upc, 'product_name': product_name})

    # Read UPC codes from file if specified
    if args.file:
        try:
            with open(args.file, 'r') as f:
                for line in f:
                    if not line.strip():
                        continue
                    upc, *product_name = line.strip().split(',', 1)
                    upc = upc.strip()
                    product_name = product_name[0].strip() if product_name else ''
                    records.append({'upc': upc, 'product_name': product_name})
        except IOError as e:
            logger.error(f"Unable to read UPC codes from file {args.file}: {e}")
            return

    if not records:
        logger.error("No UPC codes provided.")
        parser.print_help()
        return

    # Remove duplicates by UPC, keeping the first occurrence
    unique_records = {}
    for record in records:
        upc = record['upc']
        if upc not in unique_records:
            unique_records[upc] = record
        else:
            # If existing record has no product_name, update it
            if not unique_records[upc]['product_name'] and record['product_name']:
                unique_records[upc]['product_name'] = record['product_name']

    records = list(unique_records.values())

    api = ProductAPI()
    checker = AllergenChecker()

    results = []

    for record in records:
        upc = record['upc']
        provided_product_name = record['product_name']
        logger.info(f"Processing UPC: {upc}")

        result = api.fetch_product(upc)
        if result is None:
            logger.warning(f"Product not found for UPC: {upc}")
            product_name = provided_product_name if provided_product_name else 'Product not found'
            results.append({
                'upc': upc,
                'product_name': product_name,
                'allergens': [],
                'status': 'Product not found'
            })
            continue

        fetched_product_name, ingredients = result
        # Use provided product name if available, else use fetched product name
        product_name = provided_product_name if provided_product_name else fetched_product_name

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

