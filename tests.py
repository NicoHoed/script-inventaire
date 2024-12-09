import unittest
from inventory_manager import InventoryManager


class TestInventoryManager(unittest.TestCase):
    """Unit tests for the InventoryManager class."""

    def setUp(self):
        self.manager = InventoryManager()
        self.sample_inventory = [
            {"product_name": "Widget A", "quantity": "10", "price": "15.99", "category": "Widgets"},
            {"product_name": "Widget B", "quantity": "5", "price": "25.99", "category": "Widgets"},
        ]
        self.manager.inventory = self.sample_inventory

    def test_import_csv_files(self):
        self.manager.import_csv_files("test_data")
        self.assertGreater(len(self.manager.inventory), 0)

    def test_search_inventory(self):
        results = self.manager.search_inventory("Widget")
        self.assertEqual(len(results), 2)

    def test_generate_report(self):
        output_file = "test_report.csv"
        self.manager.generate_report(output_file)
        with open(output_file, "r") as file:
            content = file.readlines()
        self.assertGreater(len(content), 1)


if __name__ == "__main__":
    unittest.main()
