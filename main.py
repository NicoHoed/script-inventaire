"""This module provides a command-line interface for managing an inventory system."""
import os
from cmd import Cmd
import pandas as pd


class InventoryManager(Cmd):
    """
    A command-line interface for loading, searching, summarizing, and displaying inventory data.
    """
    intro = "\nWelcome to the Inventory Manager. Type 'help' or '?' to see available commands.\n"
    prompt = "(inventory) "

    def __init__(self):
        super().__init__()
        self.inventory = pd.DataFrame()

    def do_load(self, args):
        """
        Load CSV files into a unified database.
        Syntax: load <folder_containing_files>
        """
        folder_path = args.strip()
        if not os.path.isdir(folder_path):
            print("Folder not found.")
            return

        files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        if not files:
            print("No CSV files found in the folder.")
            return

        data_frames = []
        for file in files:
            file_path = os.path.join(folder_path, file)
            try:
                df = pd.read_csv(file_path)
                data_frames.append(df)
                print(f"Loaded: {file}")
            except (pd.errors.EmptyDataError, pd.errors.ParserError) as e:
                print(f"Error loading {file}: {e}")

        if data_frames:
            self.inventory = pd.concat(data_frames, ignore_index=True)
            print("All CSV files have been consolidated.")
        else:
            print("No valid files were loaded.")

    def do_search(self, args):
        """
        Search for a product or category.
        Syntax: search <column=value>
        """
        if self.inventory.empty:
            print("The database is empty. Load data first.")
            return

        try:
            column, value = args.split('=')
            column = column.strip()
            value = value.strip()

            if column not in self.inventory.columns:
                print(f"Column '{column}' not found in the data.")
                return

            result = self.inventory[
                self.inventory[column].astype(str).str.contains(value, case=False, na=False)
            ]
            if result.empty:
                print("No results found.")
            else:
                print(result)
        except ValueError:
            print("Invalid syntax. Use 'search <column=value>'.")

    def do_summary(self, args):
        """
        Generate a summary report.
        Syntax: summary
        """
        if self.inventory.empty:
            print("The database is empty. Load data first.")
            return

        try:
            summary = self.inventory.groupby('category').agg({
                'quantity': 'sum',
                'unit_price': 'mean'
            }).rename(columns={
                'quantity': 'Total Quantity',
                'unit_price': 'Average Price'
            })

            print(summary)

            save_path = args.strip() or "summary_report.csv"
            summary.to_csv(save_path)
            print(f"Summary report exported to {save_path}.")
        except KeyError as e:
            print(f"Error generating the report: Missing required column: {e}")

    def do_show(self, args):
        """
        Display the first rows of the consolidated database.
        Syntax: show <number_of_rows>
        """
        if self.inventory.empty:
            print("The database is empty. Load data first.")
            return

        try:
            n = int(args.strip()) if args.strip() else 5
            print(self.inventory.head(n))
        except ValueError:
            print("Please provide a valid number for the number of rows.")

    def do_exit(self, _):
        """
        Exit the application.
        Syntax: exit
        """
        print("Goodbye!")
        return True


if __name__ == "__main__":
    InventoryManager().cmdloop()
