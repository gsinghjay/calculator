from typing import List
import logging

# ==============================================================================
# OBSERVER PATTERN FOR TRACKING HISTORY
# ==============================================================================

# Who: The HistoryObserver and CalculatorWithObserver classes.
# What: Allows observers to be notified of changes in the calculation history.
# Why: To promote loose coupling between the calculator and observers, adhering to the Observer Pattern.
# Where: In the calculator's history management.
# When: Whenever a new calculation is performed.
# How: Observers register themselves with the calculator and are notified upon updates.

class HistoryObserver:
    """
    Observer that gets notified whenever a new calculation is added to history.
    Implements the Observer Pattern.
    """
    def update(self, calculation):
        """
        Called when a new calculation is added to the history.
        Parameters:
        - calculation (Calculation): The calculation object that was added.
        """
        # Log the notification at INFO level.
        logging.info(f"Observer: New calculation added -> {calculation}")

class CalculatorWithObserver:
    """
    Calculator class with observer support for tracking calculation history.
    Maintains a list of observers and notifies them of changes.
    """
    def __init__(self):
        self._history: List = []  # List to store calculation history.
        self._observers: List[HistoryObserver] = []  # List of observers.

    def add_observer(self, observer: HistoryObserver):
        """
        Adds an observer to be notified when history is updated.
        Parameters:
        - observer (HistoryObserver): The observer to add.
        """
        self._observers.append(observer)  # Add the observer to the list.
        logging.debug(f"Observer added: {observer}")  # Log the addition.

    def notify_observers(self, calculation):
        """
        Notifies all observers when a new calculation is added.
        Parameters:
        - calculation (Calculation): The calculation object that was added.
        """
        for observer in self._observers:
            observer.update(calculation)  # Call the update method on the observer.
            logging.debug(f"Notified observer about: {calculation}")  # Log the notification.

    def perform_operation(self, operation, a: float, b: float):
        """
        Performs the operation, stores it in history, and notifies observers.
        Parameters:
        - operation: The operation to perform.
        - a (float): The first operand.
        - b (float): The second operand.
        Returns:
        - The result of the operation.
        """
        calculation = operation.calculate(a, b)  # Create a new Calculation object.
        self._history.append(calculation)  # Add the calculation to the history.
        self.notify_observers(calculation)  # Notify observers of the new calculation.
        logging.debug(f"Performed operation: {calculation}")  # Log the operation.
        return calculation  # Return the calculation result.
    
    # Why use the Observer Pattern?
# - Decouples the calculator from the observers, allowing for dynamic addition/removal of observers.
# - Promotes a one-to-many dependency between objects, so when one object changes state, all dependents are notified.