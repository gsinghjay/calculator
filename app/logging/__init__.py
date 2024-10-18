import logging  # Standard Python module for logging events and messages.
# Documentation: https://docs.python.org/3/library/logging.html

def setup_logging():
    """Configure the logging settings for the application."""
    logging.basicConfig(
        filename='calculator.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

# This allows other modules to import the setup_logging function directly
__all__ = ['setup_logging']