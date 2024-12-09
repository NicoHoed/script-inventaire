import csv
import os


class InventoryManager:
    def __init__(self):
        self.inventory = []

    def import_csv_files(self, directory):
        """Imports all CSV files from the specified directory."""
        if not os.path.isdir(directory):
            print(f"Error: {directory} is not a valid directory.")
            return

        print(f"Importing data from: {directory}")
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                filepath = os.path.join(directory, filename)
                self._import_csv(filepath)

    def _import_csv(self, filepath):
        """Helper method to import a CSV file into the inventory."""
        print(f"Importing {filepath}...")
        try:
            with open(filepath, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Ensure that all the necessary fields exist
                    if 'product_name' in row and 'quantity' in row and 'unit_price' in row and 'category' in row:
                        self.inventory.append({
                            'product_name': row['product_name'],
                            'quantity': row['quantity'],
                            'unit_price': row['unit_price'],
                            'category': row['category']
                        })
                    else:
                        print(f"Skipping row due to missing data: {row}")
        except Exception as e:
            print(f"Error reading {filepath}: {e}")

    def search_inventory(self, search_term):
        """Search the inventory for items that match the search term."""
        # Normalize the search term for case-insensitive search
        search_term = search_term.lower()

        found_items = [item for item in self.inventory if
                       search_term in item['product_name'].lower() or search_term in item['category'].lower()]

        if found_items:
            print(f"Found {len(found_items)} matching item(s):")
            for item in found_items:
                print(item)
        else:
            print("No matching items found.")

    def generate_report(self, output_file):
        """Generates a report summary of the inventory and writes it to a file."""
        category_counts = {}
        for item in self.inventory:
            category = item['category']
            category_counts[category] = category_counts.get(category, 0) + 1

        with open(output_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Category", "Count"])
            for category, count in category_counts.items():
                writer.writerow([category, count])
        print(f"Report generated at {output_file}")

    def save_inventory(self, output_file):
        """Saves the current inventory to a CSV file."""
        with open(output_file, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ['product_name', 'quantity', 'unit_price', 'category']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.inventory)
        print(f"Inventory saved to {output_file}")
