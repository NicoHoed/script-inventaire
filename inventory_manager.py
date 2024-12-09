import os
import csv


class InventoryManager:
    def __init__(self):
        self.inventory = []

    def import_data(self, data_dir: str, output_file: str) -> None:
        """Imports CSV data from the provided directory and consolidates into a single CSV."""
        self.inventory.clear()  # Clear any existing inventory
        records_imported = 0

        for filename in os.listdir(data_dir):
            if filename.endswith(".csv"):
                filepath = os.path.join(data_dir, filename)
                category = filename.split('.')[0]  # Category name derived from the filename

                try:
                    with open(filepath, newline='', encoding="utf-8") as csvfile:
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                            row['category'] = category
                            self.inventory.append(row)
                            records_imported += 1
                except Exception as e:
                    print(f"Error processing file {filename}: {e}")

        # Write the combined inventory into the output file
        self.write_inventory_to_csv(output_file)

        print(f"Imported data from {records_imported} records.")
        print(f"Inventory saved to {output_file}")

    def write_inventory_to_csv(self, output_file: str) -> None:
        """Write the current inventory to a CSV file."""
        if not self.inventory:
            print("No inventory data to write.")
            return

        fieldnames = ['product_name', 'quantity', 'unit_price', 'category']
        try:
            with open(output_file, mode='w', newline='', encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.inventory)
            print(f"Inventory written to {output_file}.")
        except Exception as e:
            print(f"Error writing to file {output_file}: {e}")

    def search_inventory(self, query: str, inventory_file: str) -> None:
        """Searches the inventory CSV file for a given query."""
        results = []
        query_lower = query.strip().lower()

        try:
            with open(inventory_file, mode='r', newline='', encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Search for exact match in 'category' or 'product_name'
                    if query_lower in row['product_name'].lower() or query_lower in row['category'].lower():
                        results.append(row)
        except Exception as e:
            print(f"Error reading file {inventory_file}: {e}")

        if results:
            print(f"Found {len(results)} matching items:")
            for result in results:
                print(result)
        else:
            print("No matching items found.")
