# Items Router (`routers.items.py`) Documentation

This module defines an API router using FastAPI for scraping products from a website, incorporating authorization and input validation capabilities.

## Table of Contents

- [Items Router (`routers.items.py`) Documentation](#items-router-routersitemspy-documentation)
  - [Table of Contents](#table-of-contents)
  - [Endpoint](#endpoint)
    - [Endpoint: `/scrape_products`](#endpoint-scrape_products)
      - [Method](#method)
      - [Description](#description)
      - [Authorization](#authorization)
      - [Request Body](#request-body)
      - [Request Headers](#request-headers)
      - [Response Format](#response-format)
  - [Functionality](#functionality)
    - [Authorization Check](#authorization-check)
    - [Input Validation](#input-validation)
    - [Scraping Process](#scraping-process)
  - [Dependencies](#dependencies)
    - [External Dependencies](#external-dependencies)
    - [Internal Dependencies](#internal-dependencies)
  - [Example Usage](#example-usage)

---

## Endpoint

### Endpoint: `/scrape_products`

#### Method

- **POST**

#### Description

- This endpoint scrapes products from a specified website, returning the results in a structured JSON format.

#### Authorization

- The endpoint requires a static token for authorization.
- **Authorization Header**:
  - `Bearer my_secret_token`

#### Request Body

- **JSON Format**:
  ```json
  {
    "max_pages": 10,
    "use_auto_proxy": "auto", // [optional] must be one of 'auto', 'manual', or null
    "proxy_url": "http://example-proxy.com"  // Required only when using manual proxy
  }
  ```

#### Request Headers

- **Authorization Header**: Must be `Bearer my_secret_token` for authorization.
- **Content-Type**: `application/json`

#### Response Format

- **JSON Format**:
  ```json
  {
    "status_code": 200,
    "response": {
      // Scraped product data or error messages
    }
  }
  ```

## Functionality

### Authorization Check

- Validates the Authorization header to ensure only authorized requests are processed.
- Checks if the `Authorization` header matches the static token `Bearer my_secret_token`.

### Input Validation

- **Function**: `validate_input_data(data: Dict[str, Any]) -> Union[Tuple[int, Optional[str]], Dict[str, str]]`
  - **Purpose**: Validates and parses input data for scraping products.
  - **Validation Rules**:
    - `max_pages`: Must be a positive integer.
    - `use_auto_proxy`: Must be one of `"auto"`, `"manual"`, or `None`.
    - `proxy_url`: Required and validated when `use_auto_proxy` is `"manual"`.

### Scraping Process

- **Function**: `scrape_products_endpoint(request: Request) -> JSONResponse`
  - **Purpose**: Handles the scraping process based on the input parameters.
  - **Process**:
    - Parses the JSON request body.
    - Validates input data using `validate_input_data()`.
    - Calls the `scrape_products(max_pages, proxy_url)` function from the `scraper` module to perform the scraping.
    - Returns a JSON response with the scraping results or error messages.

## Dependencies

### External Dependencies

- **FastAPI**: Framework for building APIs with Python.
- **fp.fp**: Library for fetching free proxies (`FreeProxy`).

### Internal Dependencies

- **app.utils.scraper**: Module containing the `scrape_products` function that performs the actual scraping logic.

## Example Usage

Here is an example of how to use the `/scrape_products` endpoint:

```python
import requests

# Define the URL of the endpoint
url = "http://localhost:8000/scrape_products"

# Define the headers, including the authorization token
headers = {
    "Authorization": "Bearer my_secret_token",
}

# Define the request data
data = {
    "max_pages": 10,
    "use_auto_proxy": "auto"
}

# Make the POST request
response = requests.post(url, headers=headers, json=data)

# Print the JSON response
print(response.json())
```
