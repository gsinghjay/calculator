# app/operations/__init__.py

import logging

# Initialize a module-specific logger
logger = logging.getLogger(__name__)

def addition(a: float, b: float) -> float:
    """Returns the sum of two numbers."""
    logger.debug(f"Performing addition: {a} + {b}")
    return a + b

def subtraction(a: float, b: float) -> float:
    """Returns the difference between two numbers."""
    logger.debug(f"Performing subtraction: {a} - {b}")
    return a - b

def multiplication(a: float, b: float) -> float:
    """Returns the product of two numbers."""
    logger.debug(f"Performing multiplication: {a} * {b}")
    return a * b

def division(a: float, b: float) -> float:
    """Returns the quotient of two numbers. Raises ValueError on division by zero."""
    logger.debug(f"Performing division: {a} / {b}")
    if b == 0:
        logger.error("Attempted to divide by zero.")
        raise ValueError("Division by zero is not allowed.")
    return a / b
