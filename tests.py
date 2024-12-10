import unittest
from inventory_manager import InventoryManager


class TestInventoryManager(unittest.TestCase):

    def setUp(self):
        """Initialisation avant chaque test."""
        self.manager = InventoryManager()

    def test_import_csv_files(self):
        """Test l'importation de fichiers CSV."""
        self.manager.import_csv_files('test_data')  # Assurez-vous d'avoir un dossier test_data avec des CSV valides
        self.assertGreater(len(self.manager.inventory), 0)  # Vérifie qu'il y a des éléments importés

    def test_search_inventory(self):
        """Test de la fonctionnalité de recherche."""
        self.manager.import_csv_files('test_data')
        self.manager.search_inventory('Electronics')
        # Vérifiez que les éléments de la catégorie "Electronics" sont bien retrouvés.

    def test_generate_report(self):
        """Test de la génération du rapport."""
        self.manager.import_csv_files('test_data')
        self.manager.generate_report('test_report.csv')
        # Vérifiez si le fichier 'test_report.csv' a été créé et contient des données
        with open('test_report.csv', 'r') as f:
            content = f.read()
            self.assertIn('Category', content)


if __name__ == "__main__":
    unittest.main()
