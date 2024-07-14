# app.utils.scraper.py

from bs4 import BeautifulSoup
import requests
from typing import Any, Optional, Dict, List, Tuple
from app.utils.requester import Requester
from app.utils.logger import Logger
from app.models.item import Product as ProductDB
from app.schemas.item import Product as ProductSchema
from app.models.database import get_local_session


def scrape_products(
    max_pages: int = 119, proxy_url: Optional[str] = None
) -> Tuple[Dict[str, Any], int]:
    """
    Scrapes product information from a website and updates/inserts into a database.

    Args:
        max_pages (int): Maximum number of pages to scrape. Default is 119.
        proxy_url (Optional[str]): Optional proxy URL to use for requests.

    Returns:
        Tuple[Dict[str, Any], int]: A tuple containing a dictionary with scraping results and an HTTP status code.
    """
    products: List[Dict[str, Any]] = []  # List to store product information
    added_count: int = 0  # Counter for added products
    updated_count: int = 0  # Counter for updated products
    no_changes_count: int = 0  # Counter for products with no changes
    logger: Logger = Logger(__name__).get_logger()  # Logger instance
    requester: Requester = Requester(logger, proxy_url)  # Requester instance
    session = get_local_session()  # Create a session to interact with the database

    logger.info(f"Scraping started with proxy URL: {proxy_url}")

    try:
        for page in range(1, max_pages + 1):
            url: str = f"https://dentalstall.com/shop/page/{page}/"
            response: Optional[requests.Response] = requester.send_request(url)

            if response is None or response.status_code != 200:
                logger.error(f"Failed to reach URL: {url}")
                error_response = {
                    "error": f"Failed to reach URL: {url}",
                }
                return error_response, 500  # Return error response with status code 500

            soup: BeautifulSoup = BeautifulSoup(
                requester.get_result(response), "html.parser"
            )

            for product in soup.find_all("li", class_="product"):
                img_tag = product.find("img", class_="attachment-woocommerce_thumbnail")
                title = img_tag.get("title")
                
                price = product.find(
                    "span", class_="woocommerce-Price-amount"
                ).text.strip()
                price = round(float(price.replace("₹", "")), 2)
                
                img_link = img_tag.get("data-lazy-src")

                # Check if the product is already cached in the database
                cached_product = (
                    session.query(ProductDB).filter_by(product_title=title).first()
                )

                if cached_product:
                    # If the product is cached, check if the price has changed
                    if cached_product.product_price != price:
                        # Update the product price and image link
                        cached_product.product_price = price
                        cached_product.path_to_image = img_link
                        updated_count += 1
                        products.append(
                            {
                                "title": title,
                                "price": price,
                                "image": img_link,
                                "status": "Updated",
                            }
                        )
                    else:
                        # If no changes were made, increment the no_changes_count
                        no_changes_count += 1
                else:
                    product_schema = ProductSchema(product_title=title, product_price=price, path_to_image=img_link)
                    # If the product is not cached, create a new ProductDB object and add it to the session
                    product_obj = ProductDB(
                        product_title=product_schema.product_title, product_price=product_schema.product_price, path_to_image=product_schema.path_to_image
                    )
                    session.add(product_obj)
                    added_count += 1
                    products.append(
                        {
                            "title": title,
                            "price": price,
                            "image": img_link,
                            "status": "Added",
                        }
                    )

        session.commit()  # Commit all changes to the database
        total_count: int = added_count + updated_count + no_changes_count
        response: Dict[str, Any] = {
            "total_products": total_count,
            "added_products": added_count,
            "updated_products": updated_count,
            "no_changes": no_changes_count,
            "updated_or_modified_products": products,
        }

        logger.info(f"Scraping completed with {total_count} products processed")
        return response, 200  # Return success response with status code 200

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        session.rollback()  # Rollback the transaction if an error occurs
        error_response: Dict[str, str] = {
            "error": str(e),
        }
        return error_response, 500  # Return error response with status code 500

    finally:
        session.close()  # Close the session
