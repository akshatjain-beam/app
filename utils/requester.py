# app.utils.requester.py

import requests
import time
from typing import Optional
from app.utils.logger import Logger


class Requester:
    """
    A class to handle HTTP requests with built-in retry mechanisms and cooldown periods.

    Attributes:
        logger (Logger): An instance of the Logger class for logging messages.
        proxy_url (Optional[str]): Optional proxy URL to use for requests.
        cooldown_time (int): Time interval in seconds for regular cooldown between requests.
        super_cooldown_time (int): Time interval in seconds for extended cooldown between requests.
        cooldown_start_time (float): Timestamp when the regular cooldown started.
        super_cooldown_start_time (float): Timestamp when the extended cooldown started.
        max_retries (int): Maximum number of retry attempts for failed requests.
    """

    def __init__(self, logger: Logger, proxy_url: Optional[str] = None):
        """
        Initialize a new Requester instance.

        Args:
            logger (Logger): An instance of the Logger class for logging messages.
            proxy_url (Optional[str]): Optional proxy URL to use for requests. Default is None.
        """
        self.logger: Logger = logger
        self.proxy_url: Optional[str] = proxy_url
        self.cooldown_time: int = 5  # Increased cooldown time to 5 seconds
        self.super_cooldown_time: int = (
            30  # Increased super cooldown time to 30 seconds
        )
        self.cooldown_start_time: float = 0
        self.super_cooldown_start_time: float = 0
        self.max_retries: int = 3  # Added max_retries attribute

    def send_request(
        self, url: str, method: str = "GET", timeout: int = 10
    ) -> Optional[requests.Response]:
        """
        Send an HTTP request to the specified URL with retry mechanisms.

        Args:
            url (str): The URL to send the request to.
            method (str): The HTTP method to use (GET, POST, PUT, etc.). Default is 'GET'.
            timeout (int): Timeout in seconds for the request. Default is 10 seconds.

        Returns:
            Optional[requests.Response]: The response object if successful, None if unsuccessful.
        """
        attempts: int = 0
        while attempts < self.max_retries:
            if self.check_cooldown():
                self.logger.info(
                    f"Cooldown in effect. Waiting for {self.cooldown_time} seconds..."
                )
                time.sleep(self.cooldown_time)
            if self.check_super_cooldown():
                self.logger.info(
                    f"Super cooldown in effect. Waiting for {self.super_cooldown_time} seconds..."
                )
                time.sleep(self.super_cooldown_time)
            try:
                if self.proxy_url:
                    response: requests.Response = requests.request(
                        method,
                        url,
                        proxies={"http": self.proxy_url, "https": self.proxy_url},
                    )
                else:
                    response: requests.Response = requests.request(method, url)
                response.raise_for_status()
                self.reset_cooldown()
                return response
            except requests.RequestException as e:
                attempts += 1
                self.logger.warning(
                    f"Request failed on attempt {attempts}/{self.max_retries}. Reason: {e}"
                )
                wait_time: float = timeout

                if self.check_cooldown():
                    wait_time = self.cooldown_time - (
                        time.time() - self.cooldown_start_time
                    )
                    self.logger.info(
                        f"Cooldown in effect. Waiting for {wait_time:.2f} seconds before next attempt..."
                    )
                elif self.check_super_cooldown():
                    wait_time = self.super_cooldown_time - (
                        time.time() - self.super_cooldown_start_time
                    )
                    self.logger.info(
                        f"Super cooldown in effect. Waiting for {wait_time:.2f} seconds before next attempt..."
                    )
                else:
                    self.logger.info(
                        f"Retrying in {wait_time:.2f} seconds for next attempt..."
                    )

                time.sleep(wait_time)

                if (
                    attempts == self.max_retries // 2
                ):  # start cooldown after half of the max retries
                    self.start_cooldown()
                if (
                    attempts == self.max_retries - 1
                ):  # start super cooldown before the last retry
                    self.start_super_cooldown()

        self.logger.error(f"Request failed after {self.max_retries} attempts.")
        return None

    def get_result(self, response: Optional[requests.Response]) -> str:
        """
        Extract the text content from the HTTP response.

        Args:
            response (Optional[requests.Response]): The HTTP response object.

        Returns:
            str: The text content of the response if available, an empty string otherwise.
        """
        if response is None:
            return ""
        return response.text

    def check_cooldown(self) -> bool:
        """
        Check if the regular cooldown period is in effect.

        Returns:
            bool: True if the cooldown period is active, False otherwise.
        """
        if self.cooldown_start_time + self.cooldown_time > time.time():
            return True
        return False

    def check_super_cooldown(self) -> bool:
        """
        Check if the extended super cooldown period is in effect.

        Returns:
            bool: True if the super cooldown period is active, False otherwise.
        """
        if self.super_cooldown_start_time + self.super_cooldown_time > time.time():
            return True
        return False

    def start_cooldown(self) -> None:
        """
        Start the regular cooldown period.
        """
        self.cooldown_start_time = time.time()
        self.logger.info("Cooldown started.")

    def start_super_cooldown(self) -> None:
        """
        Start the extended super cooldown period.
        """
        self.super_cooldown_start_time = time.time()
        self.logger.info("Super cooldown started.")

    def reset_cooldown(self) -> None:
        """
        Reset both cooldown periods.
        """
        self.cooldown_start_time = 0
        self.super_cooldown_start_time = 0
        self.logger.info("Cooldown reset.")
