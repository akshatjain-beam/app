# app.utils.logger.py

import logging
from typing import Any

class Logger:
    """
    A custom logger class for creating and configuring loggers.
    
    Attributes:
        logger (logging.Logger): The logger instance.
    """
    def __init__(self, name: str):
        """
        Initialize a new Logger instance.
        
        Args:
            name (str): The name of the logger.
        """
        self.logger: logging.Logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Create a handler that logs to the console
        handler: logging.Handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)

        # Create a formatter that defines the log message format
        formatter: logging.Formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(handler)

    def get_logger(self) -> logging.Logger:
        """
        Get the configured logger instance.
        
        Returns:
            logging.Logger: The logger instance.
        """
        return self.logger
