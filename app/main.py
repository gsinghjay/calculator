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

setup_logging()

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
        # Dictionary mapping operation names to their corresponding class instances.
        operations_map = {
            "add": Addition(),
            "subtract": Subtraction(),
            "multiply": Multiplication(),
            "divide": Division(),
        }
        # Log the operation creation request at DEBUG level.
        logging.debug(f"Creating operation for: {operation}")
        # Retrieve the operation instance from the map.
        return operations_map.get(operation.lower())  # Returns None if the key is not found.

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
        if cls._instance is None:
            cls._instance = super(SingletonCalculator, cls).__new__(cls)  # Call the superclass __new__ method.
            cls._history = []  # Initialize the shared history.
            logging.info("SingletonCalculator instance created.")  # Log the creation.
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
        calculation = Calculation(operation, a, b)  # Create a new Calculation object.
        self._history.append(calculation)  # Add the calculation to the shared history.
        logging.debug(f"SingletonCalculator: Performed operation -> {calculation}")  # Log the operation.
        return operation.calculate(a, b)  # Execute the calculation and return the result.

    def get_history(self):
        """
        Returns the history of calculations.
        Includes a breakpoint for debugging using pdb.
        """
       # pdb.set_trace()  # Pause execution here for debugging.
        return self._history  # Return the shared history list.

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
    import pdb  # Import pdb module for debugging.

    # Create an instance of the calculator with observer support.
    calc = CalculatorWithObserver()

    # Create an observer to monitor calculation history.
    observer = HistoryObserver()

    # Add the observer to the calculator's list of observers.
    calc.add_observer(observer)

    # Display a welcome message and instructions.
    print("Welcome to the OOP Calculator! Type 'help' for available commands.")

    # Start the REPL loop.
    while True:
        # Prompt the user for input.
        user_input = input("Enter an operation and two numbers, or a command: ")

        # Handle the 'help' command.
        if user_input.lower() == "help":
            print("\nAvailable commands:")
            print("  add <num1> <num2>       : Add two numbers.")
            print("  subtract <num1> <num2>  : Subtract the second number from the first.")
            print("  multiply <num1> <num2>  : Multiply two numbers.")
            print("  divide <num1> <num2>    : Divide the first number by the second.")
            print("  list                    : Show the calculation history.")
            print("  clear                   : Clear the calculation history.")
            print("  exit                    : Exit the calculator.\n")
            continue  # Return to the start of the loop.

        # Handle the 'exit' command.
        if user_input.lower() == "exit":
            print("Exiting calculator...")
            break  # Exit the loop and end the program.

        # Handle the 'list' command to display calculation history.
        if user_input.lower() == "list":
            if not calc._history:
                print("No calculations in history.")
            else:
                for calc_item in calc._history:
                    print(calc_item)  # Calls __str__ method of Calculation.
            continue  # Return to the start of the loop.

        # Handle the 'clear' command to clear the history.
        if user_input.lower() == "clear":
            calc._history.clear()  # Clear the history list.
            logging.info("History cleared.")  # Log the action.
            print("History cleared.")
            continue  # Return to the start of the loop.

        # Attempt to parse and execute the user's command.
        try:
            # Set a breakpoint for debugging.
            # pdb.set_trace()  # Execution will pause here, allowing inspection of variables.

            # Split the user input into components.
            operation_str, num1_str, num2_str = user_input.split()  # May raise ValueError.

            # Convert the operand strings to float.
            num1, num2 = float(num1_str), float(num2_str)  # May raise ValueError.

            # Use the factory to create the appropriate operation object.
            operation = OperationFactory.create_operation(operation_str)

            if operation:
                # Perform the operation using the calculator.
                result = calc.perform_operation(operation, num1, num2)
                # Display the result to the user.
                print(f"Result: {result}")
            else:
                # Handle unknown operation names.
                print(f"Unknown operation '{operation_str}'. Type 'help' for available commands.")

        except ValueError as e:
            # Handle errors such as incorrect input format or invalid numbers.
            logging.error(f"Invalid input or error: {e}")  # Log the error.
            print("Invalid input. Please enter a valid operation and two numbers. Type 'help' for instructions.")

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
