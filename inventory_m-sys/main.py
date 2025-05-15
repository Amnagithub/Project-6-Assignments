from abc import ABC, abstractmethod
from datetime import datetime
import json

# ===== Abstract Base Class =====
class Product(ABC):
    def __init__(self, product_id, name, price, quantity_in_stock):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._quantity_in_stock = quantity_in_stock

    @abstractmethod
    def restock(self, amount):
        pass

    @abstractmethod
    def sell(self, quantity):
        pass

    def get_total_value(self):
        return self._price * self._quantity_in_stock

    @abstractmethod
    def __str__(self):
        pass

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "product_id": self._product_id,
            "name": self._name,
            "price": self._price,
            "quantity_in_stock": self._quantity_in_stock
        }

# ===== Subclass: Electronics =====
class Electronics(Product):
    def __init__(self, product_id, name, price, quantity_in_stock, brand, warranty_years):
        super().__init__(product_id, name, price, quantity_in_stock)
        self.brand = brand
        self.warranty_years = warranty_years

    def restock(self, amount):
        self._quantity_in_stock += amount

    def sell(self, quantity):
        if quantity > self._quantity_in_stock:
            raise ValueError("Not enough stock to sell.")
        self._quantity_in_stock -= quantity

    def __str__(self):
        return (f"[Electronics] ID: {self._product_id}, Name: {self._name}, Price: ${self._price}, "
                f"Stock: {self._quantity_in_stock}, Brand: {self.brand}, Warranty: {self.warranty_years} yrs")

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "brand": self.brand,
            "warranty_years": self.warranty_years
        })
        return data

# ===== Subclass: Grocery =====
class Grocery(Product):
    def __init__(self, product_id, name, price, quantity_in_stock, expiry_date):
        super().__init__(product_id, name, price, quantity_in_stock)
        self.expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d")

    def is_expired(self):
        return datetime.now() > self.expiry_date

    def restock(self, amount):
        self._quantity_in_stock += amount

    def sell(self, quantity):
        if self.is_expired():
            raise ValueError("Cannot sell expired product.")
        if quantity > self._quantity_in_stock:
            raise ValueError("Not enough stock to sell.")
        self._quantity_in_stock -= quantity

    def __str__(self):
        status = "Expired" if self.is_expired() else "Fresh"
        return (f"[Grocery] ID: {self._product_id}, Name: {self._name}, Price: ${self._price}, "
                f"Stock: {self._quantity_in_stock}, Expiry: {self.expiry_date.date()}, Status: {status}")

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "expiry_date": self.expiry_date.strftime("%Y-%m-%d")
        })
        return data

# ===== Subclass: Clothing =====
class Clothing(Product):
    def __init__(self, product_id, name, price, quantity_in_stock, size, material):
        super().__init__(product_id, name, price, quantity_in_stock)
        self.size = size
        self.material = material

    def restock(self, amount):
        self._quantity_in_stock += amount

    def sell(self, quantity):
        if quantity > self._quantity_in_stock:
            raise ValueError("Not enough stock to sell.")
        self._quantity_in_stock -= quantity

    def __str__(self):
        return (f"[Clothing] ID: {self._product_id}, Name: {self._name}, Price: ${self._price}, "
                f"Stock: {self._quantity_in_stock}, Size: {self.size}, Material: {self.material}")

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "size": self.size,
            "material": self.material
        })
        return data

# ===== Inventory Class =====
class Inventory:
    def __init__(self):
        self._products = {}

    def add_product(self, product: Product):
        if product._product_id in self._products:
            raise ValueError(f"Product ID '{product._product_id}' already exists.")
        self._products[product._product_id] = product

    def remove_product(self, product_id):
        if product_id in self._products:
            del self._products[product_id]
        else:
            raise ValueError(f"Product ID '{product_id}' not found.")

    def search_by_name(self, name):
        return [p for p in self._products.values() if p._name.lower() == name.lower()]

    def search_by_type(self, product_type):
        return [p for p in self._products.values() if p.__class__.__name__.lower() == product_type.lower()]

    def list_all_products(self):
        for product in self._products.values():
            print(product)

    def sell_product(self, product_id, quantity):
        if product_id not in self._products:
            raise ValueError(f"Product ID '{product_id}' not found.")
        self._products[product_id].sell(quantity)

    def restock_product(self, product_id, quantity):
        if product_id not in self._products:
            raise ValueError(f"Product ID '{product_id}' not found.")
        self._products[product_id].restock(quantity)

    def total_inventory_value(self):
        return sum(p.get_total_value() for p in self._products.values())

    def remove_expired_products(self):
        to_remove = [pid for pid, p in self._products.items()
                     if isinstance(p, Grocery) and p.is_expired()]
        for pid in to_remove:
            del self._products[pid]

    def save_to_file(self, filename):
        data = [product.to_dict() for product in self._products.values()]
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)

        self._products.clear()

        for item in data:
            product_type = item.pop("type")
            if product_type == "Electronics":
                product = Electronics(**item)
            elif product_type == "Grocery":
                product = Grocery(**item)
            elif product_type == "Clothing":
                product = Clothing(**item)
            else:
                raise ValueError(f"Unknown product type: {product_type}")

            self._products[product._product_id] = product

# ===== CLI Menu =====
def main():
    inventory = Inventory()

    while True:
        print("\n--- Inventory Management Menu ---")
        print("1. Add Product")
        print("2. Sell Product")
        print("3. Restock Product")
        print("4. List All Products")
        print("5. Search by Name")
        print("6. Search by Type")
        print("7. Remove Expired Products")
        print("8. Show Total Inventory Value")
        print("9. Save Inventory to File")
        print("10. Load Inventory from File")
        print("0. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                product_type = input("Enter product type (Electronics/Grocery/Clothing): ").strip().lower()
                pid = input("ID: ")
                name = input("Name: ")
                price = float(input("Price: "))
                quantity = int(input("Quantity in stock: "))

                if product_type == "electronics":
                    brand = input("Brand: ")
                    warranty = int(input("Warranty (years): "))
                    p = Electronics(pid, name, price, quantity, brand, warranty)

                elif product_type == "grocery":
                    expiry = input("Expiry date (YYYY-MM-DD): ")
                    p = Grocery(pid, name, price, quantity, expiry)

                elif product_type == "clothing":
                    size = input("Size: ")
                    material = input("Material: ")
                    p = Clothing(pid, name, price, quantity, size, material)

                else:
                    print("Invalid product type.")
                    continue

                inventory.add_product(p)
                print("Product added successfully!")

            elif choice == "2":
                pid = input("Enter Product ID to sell: ")
                qty = int(input("Quantity to sell: "))
                inventory.sell_product(pid, qty)
                print("Product sold!")

            elif choice == "3":
                pid = input("Enter Product ID to restock: ")
                qty = int(input("Quantity to add: "))
                inventory.restock_product(pid, qty)
                print("Product restocked!")

            elif choice == "4":
                inventory.list_all_products()

            elif choice == "5":
                name = input("Enter product name: ")
                results = inventory.search_by_name(name)
                for r in results:
                    print(r)

            elif choice == "6":
                ptype = input("Enter product type: ")
                results = inventory.search_by_type(ptype)
                for r in results:
                    print(r)

            elif choice == "7":
                inventory.remove_expired_products()
                print("Expired groceries removed.")

            elif choice == "8":
                print(f"Total Inventory Value: ${inventory.total_inventory_value():.2f}")

            elif choice == "9":
                filename = input("Filename to save (e.g., data.json): ")
                inventory.save_to_file(filename)
                print("Inventory saved!")

            elif choice == "10":
                filename = input("Filename to load (e.g., data.json): ")
                inventory.load_from_file(filename)
                print("Inventory loaded!")

            elif choice == "0":
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
