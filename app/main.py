# Ultimate Guide to OOP Design Patterns: Building a Calculator with Logging and Debugging

# ==============================================================================
# IMPORTING NECESSARY MODULES
# ==============================================================================

from app.logging import setup_logging
import logging  # Standard Python module for logging events and messages.
# Documentation: https://docs.python.org/3/library/logging.html

import pdb  # Python debugger for interactive debugging sessions.
# Documentation: https://docs.python.org/3/library/pdb.html

from abc import ABC, abstractmethod  # For creating abstract base classes (ABCs).
# Documentation: https://docs.python.org/3/library/abc.html

from dataclasses import dataclass  # Provides a decorator and functions for automatically adding special methods to classes.
# Documentation: https://docs.python.org/3/library/dataclasses.html

from typing import List  # Provides support for type hints.
# Documentation: https://docs.python.org/3/library/typing.html

from app.observer import HistoryObserver, CalculatorWithObserver
from app.template_operation import TemplateOperation, Addition, Subtraction, Multiplication, Division
from app.factory import OperationFactory
from app.history_manager import HistoryManager

setup_logging()
logging.debug("Logging has been set up.")

# Initialize HistoryManager
history_manager = HistoryManager()

# ==============================================================================
# FACTORY PATTERN FOR CREATING OPERATIONS
# ==============================================================================

# Who: The OperationFactory class.
# What: Creates instances of operation classes based on a given operation name.
# Why: To encapsulate object creation, promoting loose coupling and adherence to the Open/Closed Principle.
# Where: Used whenever a new operation needs to be created based on user input.
# When: At runtime, during the calculator's execution.
# How: By mapping operation names to their corresponding classes.

class OperationFactory:
    """
    Factory class to create instances of operations based on the operation type.
    Implements the Factory Pattern.
    """
    @staticmethod
    def create_operation(operation: str) -> TemplateOperation:
        """
        Returns an instance of the appropriate Operation subclass based on the operation string.
        Parameters:
        - operation (str): The operation name (e.g., 'add', 'subtract').
        """
        logging.debug(f"Creating operation for: {operation}")
        # Dictionary mapping operation names to their corresponding class instances.
        operations_map = {
            "add": Addition(),
            "subtract": Subtraction(),
            "multiply": Multiplication(),
            "divide": Division(),
        }
        # Log the operation creation request at DEBUG level.
        result = operations_map.get(operation.lower())  # Returns None if the key is not found.
        if result:
            logging.debug(f"Operation '{operation}' created successfully.")
        else:
            logging.debug(f"Operation '{operation}' not found in operations_map.")
        return result

# Why use the Factory Pattern?
# - It provides a way to create objects without specifying the exact class.
# - Enhances flexibility and scalability; new operations can be added without modifying existing code.

# ==============================================================================
# SINGLETON PATTERN FOR ENSURING ONE CALCULATOR INSTANCE
# ==============================================================================

# Who: The SingletonCalculator class.
# What: Ensures only one instance of the calculator exists.
# Why: To have a single shared state (e.g., calculation history) across the application.
# Where: In scenarios where shared resources are needed.
# When: Throughout the application's lifecycle.
# How: By controlling instance creation using the __new__ method.

class SingletonCalculator:
    """
    A calculator using the Singleton pattern to ensure only one instance exists.
    """
    _instance = None  # Class variable to hold the singleton instance.

    def __new__(cls):
        """
        Overrides the __new__ method to control the creation of a new instance.
        Ensures that only one instance is created.
        """
        logging.debug("SingletonCalculator.__new__ called.")
        if cls._instance is None:
            cls._instance = super(SingletonCalculator, cls).__new__(cls)  # Call the superclass __new__ method.
            cls._history = []  # Initialize the shared history.
            logging.info("SingletonCalculator instance created.")
        else:
            logging.debug("SingletonCalculator instance already exists.")
        return cls._instance  # Return the singleton instance.

    def perform_operation(self, operation: TemplateOperation, a: float, b: float) -> float:
        """
        Performs the given operation and stores the calculation in history.
        Parameters:
        - operation (TemplateOperation): The operation to perform.
        - a (float): The first operand.
        - b (float): The second operand.
        Returns:
        - The result of the operation.
        """
        logging.debug("SingletonCalculator.perform_operation called.")
        calculation = Calculation(operation, a, b)  # Create a new Calculation object.
        logging.debug(f"Calculation created: {calculation}")
        self._history.append(calculation)  # Add the calculation to the shared history.
        logging.debug(f"Calculation appended to history: {calculation}")
        self.notify_observers(calculation)  # Notify observers of the new calculation.
        logging.debug(f"Operation performed: {calculation}")
        return calculation  # Return the calculation result.

    def get_history(self):
        """
        Returns the history of calculations.
        Includes a breakpoint for debugging using pdb.
        """
        logging.debug("SingletonCalculator.get_history called.")
        # pdb.set_trace()  # Pause execution here for debugging.
        return self._history  # Return the shared history list.

    def notify_observers(self, calculation):
        """
        Notifies all observers about a new calculation.
        Parameters:
        - calculation (Calculation): The calculation to notify observers about.
        """
        logging.debug(f"Notifying observers about new calculation: {calculation}")
        # Assuming CalculatorWithObserver has a notify_observers method
        # Modify accordingly if different
        # For example:
        # for observer in self._observers:
        #     observer.update(calculation)
        #     logging.debug(f"Notified observer: {observer}")
        pass  # Replace with actual notification logic as needed.

# Why use the Singleton Pattern?
# - To control access to a shared resource.
# - Ensures that there's only one point of interaction with the resource.

# ==============================================================================
# STRATEGY PATTERN FOR OPERATION SELECTION
# ==============================================================================

# Who: The Calculation class.
# What: Represents a calculation using a specific strategy (operation).
# Why: To encapsulate algorithms (operations) and make them interchangeable.
# Where: In the execution of calculations.
# When: When performing operations on operands.
# How: By holding a reference to a strategy object and executing it.

@dataclass  # Decorator to automatically generate special methods like __init__.
class Calculation:
    """
    Represents a single calculation using the Strategy Pattern.
    Holds the operation (strategy) and operands.
    """
    operation: TemplateOperation  # The operation to execute (strategy).
    operand1: float  # The first operand.
    operand2: float  # The second operand.

    def __repr__(self) -> str:
        """
        Official string representation of the Calculation object.
        Used for debugging and logging.
        """
        return f"Calculation({self.operand1}, {self.operation.__class__.__name__.lower()}, {self.operand2})"

    def __str__(self) -> str:
        """
        User-friendly string representation of the calculation and result.
        """
        logging.debug(f"String representation called for Calculation: {self}")
        result = self.operation.calculate(self.operand1, self.operand2)  # Perform the calculation.
        return f"{self.operand1} {self.operation.__class__.__name__.lower()} {self.operand2} = {result}"

# Why use the Strategy Pattern?
# - Allows the algorithm (operation) to vary independently from the clients that use it.
# - Promotes flexibility and reuse of algorithms.

# ==============================================================================
# MAIN CALCULATOR PROGRAM (REPL INTERFACE WITH DEBUGGING)
# ==============================================================================

# Who: The calculator() function.
# What: Provides an interactive command-line interface for users to perform calculations.
# Why: To allow users to interact with the calculator in real-time.
# Where: In the main execution of the program.
# When: When the script is run directly.
# How: By implementing a Read-Eval-Print Loop (REPL).

def calculator():
    """
    Interactive REPL (Read-Eval-Print Loop) for performing calculator operations.
    Provides a command-line interface for users to interact with the calculator.
    """
    logging.debug("Calculator REPL started.")

    # Create an instance of the calculator with observer support.
    calc = CalculatorWithObserver()
    logging.debug("CalculatorWithObserver instance created.")

    # Create an observer to monitor calculation history.
    observer = HistoryObserver()
    logging.debug("HistoryObserver instance created.")

    # Add the observer to the calculator's list of observers.
    calc.add_observer(observer)
    logging.debug("HistoryObserver added to CalculatorWithObserver.")

    print("Welcome to the OOP Calculator! Type 'help' for available commands.")
    logging.info("Displayed welcome message to user.")

    while True:
        user_input = input("Enter a command or operation: ")
        logging.debug(f"User input: '{user_input}'")

        if not user_input.strip():
            continue  # Skip empty input

        parts = user_input.strip().split()

        command = parts[0].lower()

        if command == "help":
            print("\nAvailable commands:")
            print("  add <num1> <num2>       : Add two numbers.")
            print("  subtract <num1> <num2>  : Subtract the second number from the first.")
            print("  multiply <num1> <num2>  : Multiply two numbers.")
            print("  divide <num1> <num2>    : Divide the first number by the second.")
            print("  history                 : Show calculation history.")
            print("  clear                   : Clear calculation history.")
            print("  undo                    : Undo the last operation.")
            print("  redo                    : Redo the last undone operation.")
            print("  save <filename>         : Save history to a CSV file.")
            print("  load <filename>         : Load history from a CSV file.")
            print("  exit                    : Exit the calculator.\n")
            logging.debug("Displayed help information to user.")
            continue

        elif command == "exit":
            print("Exiting calculator...")
            logging.info("Calculator session terminated by user.")
            break

        elif command == "history":
            history_manager.show_history()
            continue

        elif command == "clear":
            history_manager.clear_history()
            continue

        elif command == "undo":
            history_manager.undo()
            continue

        elif command == "redo":
            history_manager.redo()
            continue

        elif command == "save":
            if len(parts) != 2:
                print("Usage: save <filename>")
                continue
            filename = parts[1]
            history_manager.save_history(filename)
            continue

        elif command == "load":
            if len(parts) != 2:
                print("Usage: load <filename>")
                continue
            filename = parts[1]
            history_manager.load_history(filename)
            continue

        # Handle arithmetic operations
        if len(parts) != 3:
            print("Invalid input. Please enter a valid operation and two numbers. Type 'help' for instructions.")
            logging.error("Invalid input format.")
            continue

        operation_name, num1_str, num2_str = parts

        try:
            num1, num2 = float(num1_str), float(num2_str)
            logging.debug(f"Parsed operands: {num1}, {num2}")
        except ValueError:
            print("Invalid numbers. Please enter valid numerical values.")
            logging.error("Invalid number conversion.")
            continue

        operation = OperationFactory.create_operation(operation_name)

        if not operation:
            print(f"Unknown operation '{operation_name}'. Type 'help' for available commands.")
            logging.warning(f"Unknown operation attempted: '{operation_name}'.")
            continue

        try:
            result = calc.perform_operation(operation, num1, num2)
            history_manager.add_entry(operation_name, num1, num2, result)
            print(f"Result: {result}")
            logging.info(f"Performed operation '{operation_name}' with operands {num1} and {num2}: Result {result}")
        except Exception as e:
            print(f"Error: {e}")
            logging.error(f"Error performing operation '{operation_name}': {e}")

# Why use a REPL?
# - Provides an interactive way for users to execute commands and see immediate results.
# - Enhances user experience and allows for real-time feedback.

# ==============================================================================
# RUNNING THE CALCULATOR PROGRAM
# ==============================================================================

if __name__ == "__main__":
    # This block ensures that the calculator runs only when the script is executed directly.
    # It will not run if the script is imported as a module.
    calculator()  # Call the main calculator function to start the REPL.

# General Programming Good Practices Demonstrated:
# - **Modular Design**: The code is organized into classes and functions, making it easier to understand and maintain.
# - **Encapsulation**: Data and methods are encapsulated within classes, promoting data hiding and abstraction.
# - **Inheritance and Polymorphism**: Base classes define common interfaces, and derived classes implement specific behaviors.
# - **Exception Handling**: The code anticipates and handles potential errors gracefully, providing informative feedback.
# - **Logging**: Comprehensive logging is implemented to track the application's behavior and assist in debugging.
# - **Type Hinting**: Type hints improve code readability and help with static analysis tools.
# - **Documentation and Comments**: Detailed comments and docstrings explain the purpose and functionality of code components.
# - **Adherence to PEP 8**: The code follows Python's style guidelines for improved readability.

# Additional Resources and References:
# - **Abstract Base Classes (`abc` module)**:
#   - Reference: https://docs.python.org/3/library/abc.html
# - **Data Classes (`dataclasses` module)**:
#   - Reference: https://docs.python.org/3/library/dataclasses.html
# - **Type Hints (`typing` module)**:
#   - Reference: https://docs.python.org/3/library/typing.html
# - **Logging (`logging` module)**:
#   - Reference: https://docs.python.org/3/library/logging.html
# - **Python Debugger (`pdb` module)**:
#   - Reference: https://docs.python.org/3/library/pdb.html
# - **Design Patterns in Python**:
#   - Reference: https://refactoring.guru/design-patterns/python
# - **PEP 8 - Style Guide for Python Code**:
#   - Reference: https://www.python.org/dev/peps/pep-0008/

# Conclusion:
# This code serves as a comprehensive example of how to implement several key object-oriented design patterns in Python.
# By understanding the who, what, why, where, when, and how of each component, students can gain a deeper appreciation
# for the art and science of OOP. The combination of design patterns, logging, debugging, and good programming practices
# results in code that is robust, maintainable, and scalable.
