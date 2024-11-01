""" app/calculator.py """

import logging
from app.template_operation import TemplateOperation
from typing import Callable, Dict, Type

# Setup logging
logging.basicConfig(
    filename='calculator.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Registry to hold operation name to class mappings
operation_registry: Dict[str, Type[TemplateOperation]] = {}

def register_operation(name: str):
    """
    Decorator to register an operation class with a given name.
    
    Parameters:
    - name (str): The name of the operation (e.g., 'add', 'subtract').
    """
    def decorator(cls: Type[TemplateOperation]):
        if name in operation_registry:
            logging.warning(f"Operation '{name}' is already registered. Overwriting.")
        operation_registry[name] = cls
        logging.debug(f"Registered operation '{name}' with class '{cls.__name__}'.")
        return cls
    return decorator

@register_operation('add')
class Addition(TemplateOperation):
    """Class to represent the addition operation."""

    def execute(self, a: float, b: float) -> float:
        """Return the sum of two numbers."""
        return a + b

@register_operation('subtract')
class Subtraction(TemplateOperation):
    """Class to represent the subtraction operation."""

    def execute(self, a: float, b: float) -> float:
        """Return the difference between two numbers."""
        return a - b

@register_operation('multiply')
class Multiplication(TemplateOperation):
    """Class to represent the multiplication operation."""

    def execute(self, a: float, b: float) -> float:
        """Return the product of two numbers."""
        return a * b

@register_operation('divide')
class Division(TemplateOperation):
    """Class to represent the division operation."""

    def execute(self, a: float, b: float) -> float:
        """Return the quotient of two numbers. Raise an error if dividing by zero."""
        if b == 0:
            logging.error("Attempted to divide by zero.")
            raise ValueError("Division by zero is not allowed.")
        return a / b
