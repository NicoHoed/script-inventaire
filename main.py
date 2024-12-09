import argparse
from inventory_manager import InventoryManager

def main():
    parser = argparse.ArgumentParser(description="Manage inventory data.")
    parser.add_argument("--import-data", type=str, help="Directory of CSV files to import data from")
    parser.add_argument("--search", type=str, help="Search for an item in the inventory")
    parser.add_argument("--output", type=str, default="inventory.csv", help="Output CSV file to store the consolidated inventory")

    args = parser.parse_args()

    manager = InventoryManager()

    if args.import_data:
        directory = args.import_data
        output_file = args.output
        manager.import_data(directory, output_file)

    if args.search:
        query = args.search
        output_file = args.output
        manager.search_inventory(query, output_file)

if __name__ == "__main__":
    main()
