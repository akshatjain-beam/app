# Utility Modules Documentation

This document provides an in-depth overview of the utility modules within the `app.utils` package. The utilities include logging configuration, HTTP request handling with retries and cooldowns, and web scraping functionality.

## Table of Contents

- [Utility Modules Documentation](#utility-modules-documentation)
  - [Table of Contents](#table-of-contents)
  - [Logger Module](#logger-module)
    - [Overview](#overview)
    - [Class: Logger](#class-logger)
      - [Attributes](#attributes)
      - [Methods](#methods)
      - [Usage Example](#usage-example)
  - [Requester Module](#requester-module)
    - [Overview](#overview-1)
    - [Class: Requester](#class-requester)
      - [Attributes](#attributes-1)
      - [Methods](#methods-1)
      - [Cooldown Management Methods](#cooldown-management-methods)
      - [Usage Example](#usage-example-1)
  - [Scraper Module](#scraper-module)
    - [Overview](#overview-2)
    - [Function: scrape\_products](#function-scrape_products)
      - [Arguments](#arguments)
      - [Return Values](#return-values)
      - [Detailed Description](#detailed-description)
      - [Usage Example](#usage-example-2)

---

## Logger Module

### Overview

The `logger.py` module provides a custom logger class for creating and configuring loggers. This ensures consistent and formatted logging across your application.

### Class: Logger

#### Attributes

- **logger (logging.Logger)**: The logger instance initialized with the provided name.

#### Methods

- **`__init__(self, name: str)`**: Initializes the logger with a specified name and configures it to log messages with an INFO level.
  - **Arguments**:
    - `name (str)`: The name of the logger.
  - **Functionality**:
    - Sets the logging level to INFO.
    - Creates a console handler.
    - Defines the log message format.
    - Adds the handler to the logger.

- **`get_logger(self) -> logging.Logger`**: Returns the configured logger instance.

#### Usage Example

```python
from app.utils.logger import Logger

# Initialize a logger instance
logger = Logger(__name__).get_logger()

# Example usage
logger.info("Logging information message")
logger.warning("Logging warning message")
logger.error("Logging error message")
```

---

## Requester Module

### Overview

The `requester.py` module handles HTTP requests with built-in retry mechanisms and cooldown periods. This ensures reliable and controlled request handling, especially when interacting with external APIs that may have rate limits or intermittent availability.

### Class: Requester

#### Attributes

- **logger (Logger)**: Instance of the `Logger` class for logging messages related to request handling.
- **proxy_url (Optional[str])**: Optional proxy URL to use for requests.
- **cooldown_time (int)**: Time interval in seconds for regular cooldown between requests.
- **super_cooldown_time (int)**: Time interval in seconds for extended cooldown between requests.
- **cooldown_start_time (float)**: Timestamp when the regular cooldown started.
- **super_cooldown_start_time (float)**: Timestamp when the extended cooldown started.
- **max_retries (int)**: Maximum number of retry attempts for failed requests.

#### Methods

- **`__init__(self, logger: Logger, proxy_url: Optional[str] = None)`**: Initializes the requester with a logger and an optional proxy URL.
  - **Arguments**:
    - `logger (Logger)`: Logger instance for logging messages.
    - `proxy_url (Optional[str])`: Optional proxy URL for requests.

- **`send_request(self, url: str, method: str = "GET", timeout: int = 10) -> Optional[requests.Response]`**: Sends an HTTP request to the specified URL with retry mechanisms and cooldown handling.
  - **Arguments**:
    - `url (str)`: The URL to send the request to.
    - `method (str)`: The HTTP method to use (GET, POST, etc.). Default is 'GET'.
    - `timeout (int)`: Timeout in seconds for the request. Default is 10 seconds.
  - **Return**:
    - `Optional[requests.Response]`: The response object if successful, None if unsuccessful.

- **`get_result(self, response: Optional[requests.Response]) -> str`**: Extracts the text content from the HTTP response.
  - **Arguments**:
    - `response (Optional[requests.Response])`: The HTTP response object.
  - **Return**:
    - `str`: The text content of the response if available, an empty string otherwise.

#### Cooldown Management Methods

- **`check_cooldown(self) -> bool`**: Checks if the regular cooldown period is in effect.
  - **Return**:
    - `bool`: True if the cooldown period is active, False otherwise.

- **`check_super_cooldown(self) -> bool`**: Checks if the extended super cooldown period is in effect.
  - **Return**:
    - `bool`: True if the super cooldown period is active, False otherwise.

- **`start_cooldown(self) -> None`**: Starts the regular cooldown period.

- **`start_super_cooldown(self) -> None`**: Starts the extended super cooldown period.

- **`reset_cooldown(self) -> None`**: Resets both cooldown periods.

#### Usage Example

```python
from app.utils.requester import Requester
from app.utils.logger import Logger

# Initialize a logger instance
logger = Logger(__name__).get_logger()

# Initialize a requester instance
requester = Requester(logger)

# Example usage
response = requester.send_request("https://example.com")
if response:
    print(requester.get_result(response))
```

---

## Scraper Module

### Overview

The `scraper.py` module scrapes product information from a website and interacts with the database to update or insert product data.

### Function: scrape_products

- **Purpose**: Scrapes product information from a specified number of pages on a website and updates/inserts products into a database.

#### Arguments

- **`max_pages (int)`**: Maximum number of pages to scrape. Default is 119.
- **`proxy_url (Optional[str])`**: Optional proxy URL to use for requests.

#### Return Values

- **`Tuple[Dict[str, Any], int]`**: A tuple containing a dictionary with scraping results and an HTTP status code.

#### Detailed Description

- **Initialization**:
  - Initializes logger and requester instances.
  - Sets up a database session to interact with the database.

- **Scraping Process**:
  - Iterates through the specified number of pages.
  - Sends HTTP requests to fetch the page content.
  - Parses the HTML content using BeautifulSoup.
  - Extracts product information (title, price, image URL).
  - Checks if the product is already cached in the database:
    - If the product is cached and the price has changed, updates the product.
    - If the product is cached and the price has not changed, increments the no changes counter.
    - If the product is not cached, adds a new product to the database.

- **Finalization**:
  - Commits all changes to the database.
  - Logs the results of the scraping process.
  - Returns a dictionary with the results and an HTTP status code.

#### Usage Example

```python
from app.utils.scraper import scrape_products

# Example usage
results, status_code = scrape_products(max_pages=10)
print(results)
```

