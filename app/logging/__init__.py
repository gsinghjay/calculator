# app/logging/__init__.py
import logging
import os
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

# Corrected path to the .env file
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../.env'))
load_dotenv(dotenv_path)

def setup_logging() -> None:
    """Configure the logging settings for the application."""
    log_filename: str = os.getenv('LOG_FILENAME', 'calculator_rename.log')  # Use a consistent default
    log_level_str: str = os.getenv('LOG_LEVEL', 'DEBUG').upper()
    log_format: str = os.getenv('LOG_FORMAT', '%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    max_bytes: int = int(os.getenv('LOG_MAX_BYTES', 5 * 1024 * 1024)) 
    backup_count: int = int(os.getenv('LOG_BACKUP_COUNT', 5))
    
    # Convert log level string to logging level
    log_level = getattr(logging, log_level_str, logging.DEBUG)
    
    # Create a rotating file handler
    handler = RotatingFileHandler(log_filename, maxBytes=max_bytes, backupCount=backup_count)
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    
    # Configure the root logger
    logging.getLogger().setLevel(log_level)
    logging.getLogger().addHandler(handler)
    
    logging.debug(f"Logging initialized with filename={log_filename}, level={log_level_str}")

__all__ = ['setup_logging']
