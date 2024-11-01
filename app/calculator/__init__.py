""" app/calculator.py """

import logging
import warnings
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
            warnings.warn(f"Operation '{name}' is already registered. Overwriting.")
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

def calculator():
    """Interactive REPL calculator using registry-based operation lookup."""
    print("Welcome to the calculator REPL! Type 'exit' to quit, or 'help' for commands.")

    while True:
        user_input = input("Enter an operation (add, subtract, multiply, divide) and two numbers, or 'exit' to quit: ").strip()

        if user_input.lower() == "exit":
            print("Exiting calculator...")
            logging.info("Calculator session terminated by user.")
            break

        if user_input.lower() == "help":
            print("\nAvailable commands:")
            print("  add <num1> <num2>       : Add two numbers.")
            print("  subtract <num1> <num2>  : Subtract the second number from the first.")
            print("  multiply <num1> <num2>  : Multiply two numbers.")
            print("  divide <num1> <num2>    : Divide the first number by the second.")
            print("  help                    : Show this help message.")
            print("  exit                    : Exit the calculator.\n")
            continue

        try:
            # Split user input into components
            operation_name, num1_str, num2_str = user_input.split()
            num1, num2 = float(num1_str), float(num2_str)
        except ValueError:
            print("Invalid input. Please follow the format: <operation> <num1> <num2>")
            logging.error("Invalid input format.")
            continue

        # Retrieve the operation class from the registry
        operation_class = operation_registry.get(operation_name.lower())

        if not operation_class:
            print(f"Unknown operation '{operation_name}'. Supported operations: add, subtract, multiply, divide.")
            logging.warning(f"Unknown operation attempted: '{operation_name}'.")
            continue

        try:
            # Instantiate the operation and perform calculation
            operation_instance = operation_class()
            result = operation_instance.calculate(num1, num2)
            print(f"Result: {result}\n")
            logging.info(f"Performed operation '{operation_name}' with operands {num1} and {num2}: Result {result}")
        except Exception as e:
            print(f"Error: {e}")
            logging.error(f"Error performing operation '{operation_name}' with operands {num1} and {num2}: {e}")