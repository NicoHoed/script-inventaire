import argparse
from inventory_manager import InventoryManager

def print_help():
    """Custom help function."""
    print("""
    Inventory Management Tool

    Usage:
    ./main.py --import-data <directory> --output <file>    Import inventory data and save it to a file.
    ./main.py --search <keyword>                            Search for items in the inventory by product name or category.
    ./main.py --report <filename>                           Generate a summary report of the inventory.

    Example usage:
    ./main.py --import-data test_data --output inventory.csv
    ./main.py --search Electronics
    ./main.py --report summary_report.csv

    Options:
    --help              Show this help message.
    --import-data       Directory containing CSV files to import.
    --search            Search for a product or category.
    --output            File to save the inventory report.
    --report            Generate a report and save it to a specified file.
    """)

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Inventory management tool for importing, searching, and reporting inventory data."
    )

    # Add arguments
    parser.add_argument(
        "--import-data",
        help="Directory containing CSV files to import. Example: --import-data test_data",
        type=str
    )

    parser.add_argument(
        "--search",
        help="Search for a product or category in the inventory. Example: --search Electronics",
        type=str
    )

    parser.add_argument(
        "--output",
        help="File to save the inventory report. Example: --output inventory.csv",
        type=str
    )

    parser.add_argument(
        "--report",
        help="Generate a report and save it to a specified file. Example: --report report.csv",
        type=str
    )

    parser.add_argument(
        "help",
        help="Show help message.",
        nargs="?",
        default=False
    )

    return parser.parse_args()

def main():
    """Main function to handle the logic for importing data, searching, and generating reports."""
    args = parse_args()

    # Show custom help if 'help' is passed as an argument
    if args.help:
        print_help()
        return

    manager = InventoryManager()

    # Import data
    if args.import_data:
        print(f"Importing data from: {args.import_data}")
        manager.import_csv_files(args.import_data)
        manager.save_inventory(args.output or "inventory.csv")
        print(f"Inventory written to {args.output or 'inventory.csv'}.")

    # Search functionality
    if args.search:
        print(f"Searching for: {args.search}")
        manager.search_inventory(args.search)

    # Generate report
    if args.report:
        print(f"Generating report...")
        manager.generate_report(args.report)
        print(f"Report generated at {args.report}.")

if __name__ == "__main__":
    main()
