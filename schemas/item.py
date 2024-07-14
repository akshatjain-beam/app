# schemas.item.py

from pydantic import BaseModel

class Product(BaseModel):
    """
    Product schema for data validation and serialization.
    
    Attributes:
        product_title (str): The title of the product.
        product_price (float): The price of the product.
        path_to_image (str): The URL or path to the product's image.
    """
    product_title: str
    product_price: float
    path_to_image: str
