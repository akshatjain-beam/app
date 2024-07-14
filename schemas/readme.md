# Schemas Folder Structure and Usage

This README provides an overview of the `schemas` folder structure and how to use its components for data validation and serialization using Pydantic in Python.

## `schemas.item.py`

### Product Class (Schema)

- **Purpose**:
  - Defines the schema for product data using Pydantic's `BaseModel` for data validation and serialization.

- **Attributes**:
  - **product_title**: The title of the product (`str`).
  - **product_price**: The price of the product (`float`).
  - **path_to_image**: The URL or path to the product's image (`str`).

  ```python
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
  ```

### Data Validation

- **Purpose**:
  - Ensures that the data conforms to the expected types and constraints.

- **Example**:
  - When creating a new product or updating an existing one, the data must match the schema.

  ```python
  product_data = {
      "product_title": "Example Product",
      "product_price": 29.99,
      "path_to_image": "https://example.com/image.jpg"
  }

  product = Product(**product_data)
  print(product)
  ```

### Data Serialization

- **Purpose**:
  - Converts Pydantic models to various formats (e.g., JSON) for easy transmission and storage.

- **Example**:
  - Convert a product schema to JSON format.

  ```python
  product_json = product.json()
  print(product_json)
  ```

## Usage Example

### Validating and Serializing Data

- **Example Code**:
  - Demonstrates how to validate and serialize product data using the defined schema.

  ```python
  from schemas.item import Product

  # Valid product data
  valid_data = {
      "product_title": "Valid Product",
      "product_price": 19.99,
      "path_to_image": "https://example.com/valid_image.jpg"
  }

  # Create a Product instance
  valid_product = Product(**valid_data)
  print(valid_product)

  # Serialize the Product instance to JSON
  product_json = valid_product.json()
  print(product_json)

  # Invalid product data (raises ValidationError)
  try:
      invalid_data = {
          "product_title": "Invalid Product",
          "product_price": "invalid_price",  # Invalid type
          "path_to_image": "https://example.com/invalid_image.jpg"
      }
      invalid_product = Product(**invalid_data)
  except ValueError as e:
      print(f"Validation error: {e}")
  ```

## Dependencies

- **Pydantic**:
  - Required for data validation and serialization.

  ```bash
  pip install pydantic
  ```
