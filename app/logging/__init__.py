import logging
import os
from dotenv import load_dotenv

load_dotenv()

def setup_logging():
    """Configure the logging settings for the application."""
    logging.basicConfig(
        filename=os.getenv('LOG_FILENAME', 'calculator.log'),
        level=getattr(logging, os.getenv('LOG_LEVEL', 'DEBUG')),
        format=os.getenv('LOG_FORMAT', '%(asctime)s - %(levelname)s - %(message)s')
    )

# This allows other modules to import the setup_logging function directly
__all__ = ['setup_logging']