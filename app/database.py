import json
import os
from typing import List
from models import Product

class Database:
    def __init__(self, filename='products.json'):
        self.filename = filename
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.products = json.load(f)
        else:
            self.products = []

    def save_data(self):
        with open(self.filename, 'w') as f:
            json.dump(self.products, f, indent=4)

    def add_product(self, product: Product):
        if not any(p['product_title'] == product.product_title for p in self.products):
            self.products.append(product.dict())
            self.save_data()

    def get_products(self) -> List[Product]:
        return [Product(**p) for p in self.products]
