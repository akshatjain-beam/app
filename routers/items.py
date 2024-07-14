# routers.items.py

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fp.fp import FreeProxy
from app.utils.scraper import scrape_products
from typing import Optional, Dict, Any, Tuple, Union

# Create a new APIRouter instance
router = APIRouter()

# Static token for simple authorization
STATIC_TOKEN = "my_secret_token"  # Replace with your static token


@router.post("/scrape_products")
async def scrape_products_endpoint(request: Request) -> JSONResponse:
    """
    Endpoint to scrape products from a website.

    Args:
        request (Request): The incoming request object.

    Returns:
        JSONResponse: The JSON response containing the scrape results or error messages.
    """
    # Get the Authorization header
    auth_header: str = request.headers.get("Authorization")

    # Check if the Authorization header is valid
    if auth_header != f"Bearer {STATIC_TOKEN}":
        content: Dict[str, Any] = {
            "status_code": 401,
            "response": {"error": "Unauthorized"},
        }
        return JSONResponse(content=content, status_code=401)

    # Parse the request JSON body
    data: Dict[str, Any] = await request.json()

    # Validate the input data
    validation_result = validate_input_data(data)
    if "error" in validation_result:
        content: Dict[str, Any] = {"status_code": 400, "response": validation_result}
        return JSONResponse(content=content, status_code=400)

    # Extract the validated data
    max_pages, proxy_url = validation_result

    # Call the scrape_products function and get the response and status code
    response, status_code = scrape_products(max_pages, proxy_url)
    content: Dict[str, Any] = {"status_code": status_code, "response": response}
    return JSONResponse(content=content, status_code=status_code)


def validate_input_data(
    data: Dict[str, Any]
) -> Union[Tuple[int, Optional[str]], Dict[str, str]]:
    """
    Validate the input data for scraping products.

    Args:
        data (Dict[str, Any]): The input data dictionary.

    Returns:
        Union[Tuple[int, Optional[str]], Dict[str, str]]: A tuple with max_pages and proxy_url if valid, or an error dictionary.
    """
    # Get max_pages from the input data, default to 119
    max_pages: int = data.get("max_pages", 119)
    proxy_type: Optional[str] = data.get("use_auto_proxy", None)
    proxy_url: Optional[str] = None

    # Validate max_pages
    if max_pages is None or not isinstance(max_pages, int):
        return {"error": "max_pages must be an integer"}
    if max_pages <= 0:
        return {"error": "max_pages must be a positive integer"}

    # Validate proxy_type
    if not (isinstance(proxy_type, str) or proxy_type is None):
        return {"error": "proxy_type must be a string or None"}
    if proxy_type not in ["auto", "manual", None]:
        return {"error": "proxy_type must be one of 'auto', 'manual', or None"}

    # Determine the proxy URL based on the proxy type
    if proxy_type == "auto":
        proxy_url = FreeProxy(https=True).get()
    elif proxy_type == "manual":
        proxy_url = data.get("proxy_url")
        if not proxy_url:
            return {"error": "Proxy URL is required when using manual proxy"}
    else:
        proxy_url = None

    return max_pages, proxy_url
