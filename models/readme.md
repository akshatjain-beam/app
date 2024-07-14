# Models Folder Structure and Usage

This README provides an overview of the `models` folder structure and how to use its components for database modeling and interaction using SQLAlchemy in Python.

## Table of Contents

- [Models Folder Structure and Usage](#models-folder-structure-and-usage)
  - [Table of Contents](#table-of-contents)
  - [Database Configuration and Session Management (`models.database.py`)](#database-configuration-and-session-management-modelsdatabasepy)
    - [Database Configuration](#database-configuration)
    - [Engine and Session Management](#engine-and-session-management)
    - [Function `get_local_session()`](#function-get_local_session)
    - [Base Declaration](#base-declaration)
  - [Product Model (`models.item.py`)](#product-model-modelsitempy)
    - [Product Class (Model)](#product-class-model)
    - [Table Definition](#table-definition)
  - [Usage Example](#usage-example)
    - [Interacting with the Database](#interacting-with-the-database)
  - [Dependencies](#dependencies)

---

## Database Configuration and Session Management (`models.database.py`)

### Database Configuration

- **DATABASE_URL**:
  - Defines the SQLite database URL (`sqlite:///products.db`) where data is stored locally.

### Engine and Session Management

- **Engine Creation**:
  - Uses SQLAlchemy's `create_engine` function to create an engine that connects to the SQLite database specified by `DATABASE_URL`.

    ```python
    from sqlalchemy import create_engine

    # Database URL for SQLite
    DATABASE_URL = "sqlite:///products.db"

    # Create an engine that stores data in the local directory's products.db file.
    engine = create_engine(DATABASE_URL)
    ```

- **Session Management**:
  - `SessionLocal` is defined using `sessionmaker(bind=engine)` to manage database sessions. This session factory can be used to create new database sessions.

    ```python
    from sqlalchemy.orm import sessionmaker

    # Create a configured "Session" class
    SessionLocal = sessionmaker(bind=engine)
    ```

### Function `get_local_session()`

- **Purpose**:
  - Creates and returns a new SQLAlchemy session (`Session`) for database interactions.

- **Usage**:
  - Call `get_local_session()` to obtain a new session instance whenever a database session is needed within your application.

    ```python
    from sqlalchemy.orm import Session

    def get_local_session() -> Session:
        """
        Create and return a new SQLAlchemy session.
        
        Returns:
            db (Session): A new SQLAlchemy database session.
        """
        db = SessionLocal()
        return db
    ```

### Base Declaration

- **Purpose**:
  - `Base` is declared using `declarative_base()` from SQLAlchemy. It serves as a base class for all model definitions in the application.

    ```python
    from sqlalchemy.ext.declarative import declarative_base

    # Create a base class for our classes definitions
    Base = declarative_base()
    ```

## Product Model (`models.item.py`)

### Product Class (Model)

- **Purpose**:
  - Represents the `products` table in the database, defining its structure and relationships.

- **Attributes**:
  - **id**: Primary key for identifying each product (`Integer`, `primary_key=True`).
  - **product_title**: Title of the product (`String`, `nullable=False`).
  - **product_price**: Price of the product (`Float`, `nullable=False`).
  - **path_to_image**: URL or path to the product's image (`String`, `nullable=True`).

```python
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
```

### Table Definition

- **Table Name**:
  - `__tablename__ = "products"` explicitly sets the table name in the database.

## Usage Example

### Interacting with the Database

- **Example Code**:
  - Demonstrates how to use the defined models and database session to interact with the `products` table.

```python
from app.models.database import Base, get_local_session
from app.models.item import Product

# Create a session
db = get_local_session()

# Querying products
products = db.query(Product).all()

# Adding a new product
new_product = Product(product_title="New Product", product_price=19.99, path_to_image="example.com/image.jpg")
db.add(new_product)
db.commit()

# Closing the session
db.close()
```

## Dependencies

- **SQLAlchemy**:
  - Required for object-relational mapping (ORM) capabilities and database interaction in Python.

    ```bash
    pip install sqlalchemy
    ```
