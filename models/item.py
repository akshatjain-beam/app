# models.item.py

from sqlalchemy import Column, Integer, String, Float
from app.models.database import Base

class Product(Base):
    """
    The Product class represents the products table in the database.
    
    Attributes:
        id (int): The primary key of the product.
        product_title (str): The title of the product.
        product_price (float): The price of the product.
        path_to_image (str): The URL or path to the product's image.
    """
    
    # Define the name of the table in the database
    __tablename__ = "products"

    # Define the columns in the table
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_title = Column(String, nullable=False)
    product_price = Column(Float, nullable=False)
    path_to_image = Column(String, nullable=True)

