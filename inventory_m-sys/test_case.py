
import unittest
from datetime import datetime, timedelta
from main import Electronics, Grocery, Clothing, Inventory

class TestInventorySystem(unittest.TestCase):

    def setUp(self):
        self.inv = Inventory()
        self.elec = Electronics("E001", "Phone", 500.0, 10, "Samsung", 2)
        self.groc = Grocery("G001", "Milk", 2.5, 20, (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"))
        self.cloth = Clothing("C001", "Shirt", 25.0, 15, "M", "Cotton")

    def test_add_product(self):
        self.inv.add_product(self.elec)
        self.assertIn("E001", self.inv._products)

    def test_sell_product(self):
        self.inv.add_product(self.cloth)
        self.inv.sell_product("C001", 5)
        self.assertEqual(self.cloth._quantity_in_stock, 10)

    def test_restock_product(self):
        self.inv.add_product(self.elec)
        self.inv.restock_product("E001", 5)
        self.assertEqual(self.elec._quantity_in_stock, 15)

    def test_expired_grocery_removal(self):
        expired = Grocery("G002", "Old Milk", 2.0, 5, (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"))
        self.inv.add_product(expired)
        self.inv.remove_expired_products()
        self.assertNotIn("G002", self.inv._products)

    def test_total_inventory_value(self):
        self.inv.add_product(self.elec)
        self.inv.add_product(self.cloth)
        total = self.elec.get_total_value() + self.cloth.get_total_value()
        self.assertAlmostEqual(self.inv.total_inventory_value(), total)

if __name__ == "__main__":
    unittest.main()
