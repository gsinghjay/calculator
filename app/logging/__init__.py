# app/logging/__init__.py

import logging
import os
from dotenv import load_dotenv  # type: ignore
from logging.handlers import RotatingFileHandler

load_dotenv()

def setup_logging() -> None:
    """Configure the logging settings for the application."""
    log_filename: str = os.getenv('LOG_FILENAME', 'calculator20.log')  # Use a consistent default
    log_level_str: str = os.getenv('LOG_LEVEL', 'DEBUG').upper()
    log_format: str = os.getenv('LOG_FORMAT', '%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    max_bytes: int = int(os.getenv('LOG_MAX_BYTES', 5 * 1024 * 1024))  # 5 MB
    backup_count: int = int(os.getenv('LOG_BACKUP_COUNT', 5))  # Keep 5 backup files
    
    # Convert log level string to logging level
    log_level = getattr(logging, log_level_str, logging.DEBUG)
    
    # Create a rotating file handler
    handler = RotatingFileHandler(
        filename=log_filename,
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    handler.setLevel(log_level)
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    
    # Get the root logger and configure it
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(handler)
    
    logger = logging.getLogger(__name__)
    logger.debug(f"Logging configured with filename='{log_filename}', level='{log_level_str}', format='{log_format}', max_bytes={max_bytes}, backup_count={backup_count}")

__all__ = ['setup_logging']
