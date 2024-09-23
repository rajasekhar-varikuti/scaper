from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str

class ScraperSettings(BaseModel):
    page_limit: int = 5
    proxy: str = None
