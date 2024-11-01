import logging
import os
from dotenv import load_dotenv  # type: ignore

load_dotenv()

def setup_logging():
    """Configure the logging settings for the application."""
    log_filename = os.getenv('LOG_FILENAME', 'calculator.log')
    log_level = getattr(logging, os.getenv('LOG_LEVEL', 'DEBUG'))
    log_format = os.getenv('LOG_FORMAT', '%(asctime)s - %(levelname)s - %(message)s')
    
    logging.basicConfig(
        filename=log_filename,
        level=log_level,
        format=log_format
    )
    logging.debug(f"Logging configured with filename={log_filename}, level={log_level}, format={log_format}")

# This allows other modules to import the setup_logging function directly
__all__ = ['setup_logging']