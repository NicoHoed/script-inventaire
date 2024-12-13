"""
This module provides a command-line
interface for managing an inventory system.
"""
import argparse
import os
from cmd import Cmd
import pandas as pd
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


def print_error(message):
    """Red error message"""
    print(Fore.RED + message + Style.RESET_ALL)


def print_success(message):
    """Green success message"""
    print(Fore.GREEN + message + Style.RESET_ALL)


def print_info(message):
    """Blue info message"""
    print(Fore.BLUE + message + Style.RESET_ALL)


class InventoryManager(Cmd):
    """
    A command-line interface for loading,
    searching, summarizing, and displaying inventory data.
    """
    intro = ("\nWelcome to the Inventory Manager."
             "Type 'help' or '?' to see available commands.\n")
    prompt = "(inventory) "

    def __init__(self):
        super().__init__()
        self.inventory = pd.DataFrame()

    def do_load(self, folder_path):
        """
        Load CSV files into a unified database.
        Syntax: load <folder_containing_files>
        """
        folder_path = folder_path.strip()
        if not os.path.isdir(folder_path):
            print_error("Folder not found.")
            return

        files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        if not files:
            print_error("No CSV files found in the folder.")
            return

        data_frames = []
        for file in files:
            file_path = os.path.join(folder_path, file)
            try:
                df = pd.read_csv(file_path)
                data_frames.append(df)
                print_success(f"Loaded: {file}")
            except (pd.errors.EmptyDataError, pd.errors.ParserError) as e:
                print_error(f"Error loading {file}: {e}")

        if data_frames:
            self.inventory = pd.concat(data_frames, ignore_index=True)
            print_success("All CSV files have been consolidated.")
        else:
            print_error("No valid files were loaded.")

    def do_search(self, query):
        """
        Search for a product or category.
        Syntax: search <column=value>
        """
        if self.inventory.empty:
            print_error("The database is empty. Load data first.")
            return

        try:
            column, value = query.split('=')
            column, value = column.strip(), value.strip()

            if column not in self.inventory.columns:
                print_error(f"Column '{column}' not found in the data.")
                return

            result = self.inventory[
                self.inventory[column]
                .astype(str)
                .str.contains(value, case=False, na=False)
            ]

            if result.empty:
                print_info("No results found.")
            else:
                print_info(result.to_string())
        except ValueError:
            print_error("Invalid syntax. Use 'search <column=value>'.")

    def do_summary(self, save_path):
        """
        Generate a summary report.
        Syntax: summary
        """
        if self.inventory.empty:
            print_error("The database is empty. Load data first.")
            return

        group_col = 'category'
        quantity_col = 'quantity'
        price_col = 'unit_price'
        required_columns = [group_col, quantity_col, price_col]
        if not all(col in self.inventory.columns for col in required_columns):
            print_error("Required columns are missing for summary.")
            return

        summary = self.inventory.groupby(group_col).agg({
            quantity_col: 'sum',
            price_col: 'mean'
        }).rename(columns={
            quantity_col: 'Total Quantity',
            price_col: 'Average Price'
        })

        print_info(summary.to_string())
        save_path = save_path.strip() or "summary_report.csv"
        summary.to_csv(save_path)
        print_success(f"Summary report exported to {save_path}.")

    def do_show(self, n):
        """
        Display the first rows of the consolidated database.
        Syntax: show <number_of_rows>
        """
        if self.inventory.empty:
            print_error("The database is empty. Load data first.")
            return

        try:
            n = int(n.strip()) if n.strip() else 5
            print_info(self.inventory.head(n).to_string())
        except ValueError:
            print_error("Please provide a valid number of rows.")


def main():
    """Entry point for the Inventory Manager CLI.

    Handles the following actions based on user input:
    - '--load': Load CSV files from a folder.
    - '--search': Search for a product or category (column=value).
    - '--summary': Generate and save a summary report.
    - '--show': Display the first N rows of the inventory.

    If no arguments are provided, starts the interactive mode.
    """

    parser = argparse.ArgumentParser(description="Inventory Manager CLI")
    parser.add_argument(
        "--load",
        help="Load CSV files from a folder"
    )
    parser.add_argument(
        "--search",
        help="Search for a product or category (format: column=value)"
    )
    parser.add_argument(
        "--summary",
        help="Generate a summary report and save to a file"
    )
    parser.add_argument(
        "--show",
        type=int,
        help="Display the first N rows of the inventory"
    )

    args = parser.parse_args()
    manager = InventoryManager()

    if args.load:
        manager.do_load(args.load)
    if args.search:
        manager.do_search(args.search)
    if args.summary:
        manager.do_summary(args.summary)
    if args.show is not None:
        manager.do_show(str(args.show))

    # If no arguments are provided, start the interactive mode
    if not any(vars(args).values()):
        manager.cmdloop()


if __name__ == "__main__":
    main()
