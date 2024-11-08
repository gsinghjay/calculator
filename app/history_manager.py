# app/history_manager.py

"""Module for managing calculation history using pandas DataFrame."""

import os
import pandas as pd
from typing import Optional, Tuple, List, Dict
import logging

logger = logging.getLogger(__name__)

class HistoryManager:
    """
    Manages calculation history using a pandas DataFrame.
    Supports history display, clear, undo, redo, save, and load operations.
    """

    DEFAULT_HISTORY_FILE: str = os.getenv('HISTORY_FILE', 'calculation_history.csv')

    def __init__(self):
        self.history = pd.DataFrame(columns=["Operation", "Operand1", "Operand2", "Result"])
        self.undo_stack: List[Tuple[str, Optional[pd.DataFrame]]] = []
        self.redo_stack: List[Tuple[str, Optional[pd.DataFrame]]] = []
        logger.debug("HistoryManager initialized with empty history.")

    def _create_new_entry(
        self, operation: str, operand1: float, operand2: float, result: float
    ) -> Dict[str, float]:
        """
        Creates a new history entry as a dictionary for the calculation.

        Args:
            operation (str): The operation performed.
            operand1 (float): The first operand.
            operand2 (float): The second operand.
            result (float): The result of the operation.

        Returns:
            Dict[str, float]: A dictionary representing the history entry.
        """
        entry = {
            "Operation": operation,
            "Operand1": operand1,
            "Operand2": operand2,
            "Result": result,
        }
        logger.debug(f"Created new history entry: {entry}")
        return entry

    def add_entry(
        self, operation: str, operand1: float, operand2: float, result: float
    ) -> None:
        """Add a new calculation entry to history.

        Args:
            operation (str): The operation performed.
            operand1 (float): The first operand.
            operand2 (float): The second operand.
            result (float): The result of the operation.
        """
        entry = pd.DataFrame([self._create_new_entry(operation, operand1, operand2, result)])
        if self.history.empty:
            self.history = entry
            logger.debug("Added first history entry.")
        else:
            self.history = pd.concat([self.history, entry], ignore_index=True)
            logger.debug(f"Added history entry: {entry.to_dict(orient='records')}")
        self.undo_stack.append(("add", entry))
        self.redo_stack.clear()
        logger.info(f"History entry added: {operation} {operand1} {operand2} = {result}")
        print(f"Operation '{operation}' {operand1} and {operand2} successful.")  # User-facing message

    def show_history(self) -> None:
        """Display the calculation history."""
        if self.history.empty:
            logger.info("No history available to display.")
            print("No history available.")  # User message
            return

        logger.debug("Displaying calculation history.")
        print(self.history.to_string(index=False))  # User message

    def clear_history(self) -> None:
        """Clear the calculation history."""
        # Save current history for undo
        previous_history = self.history.copy()
        self.undo_stack.append(("clear", previous_history))
        self.history = pd.DataFrame(columns=self.history.columns)
        self.redo_stack.clear()
        logger.info("History cleared.")
        print("History cleared successfully.")  # User message

    def undo(self) -> None:
        """Undo the last operation.

        This method handles undoing the last action performed on the calculation history.
        It separates logging from user messages to maintain clarity and adherence to SOLID principles.

        Logging:
            - Records warnings and errors related to undo operations.
            - Logs informational messages about undo actions.

        User Messages:
            - Provides feedback to the user about the success or failure of undo actions.
        """
        if not self.undo_stack:
            logger.warning("Undo attempted with empty undo stack.")
            print("Nothing to undo.")
            return

        action, data = self.undo_stack.pop()

        if action == "add":
            if self.history.empty:
                logger.warning("Undo attempted to remove from empty history.")
                print("Nothing to undo.")
                return
            removed_entry = self.history.iloc[-1]
            self.history = self.history.iloc[:-1]
            self.redo_stack.append(("add", removed_entry))
            logger.info(f"Undone: {removed_entry['Operation']} {removed_entry['Operand1']} "
                        f"{removed_entry['Operand2']} = {removed_entry['Result']}")
            print(f"Operation '{removed_entry['Operation']}' {removed_entry['Operand1']} and {removed_entry['Operand2']} undone successfully.")
        elif action == "clear":
            logger.info("Undoing clear history operation.")
            self.redo_stack.append(("clear", self.history.copy()))
            self.history = data
            logger.info("History restored after undoing clear.")
            print("History restoration after undo successful.")
        else:
            logger.error(f"Unknown action '{action}' in undo stack.")
            print(f"Unknown action '{action}' in undo stack.")

    def redo(self) -> None:
        """Redo the last undone operation.

        This method handles redoing the last undone action performed on the calculation history.
        It separates logging from user messages to maintain clarity and adherence to SOLID principles.

        Logging:
            - Records warnings and errors related to redo operations.
            - Logs informational messages about redo actions.

        User Messages:
            - Provides feedback to the user about the success or failure of redo actions.
        """
        if not self.redo_stack:
            logger.warning("Redo attempted with empty redo stack.")
            print("Nothing to redo.")
            return

        action, data = self.redo_stack.pop()

        if action == "add":
            self.history = pd.concat([self.history, data.to_frame().T], ignore_index=True)
            self.undo_stack.append(("add", data.to_frame().T))
            logger.info(f"Redone: {data['Operation']} {data['Operand1']} {data['Operand2']} = {data['Result']}")
            print(f"Operation '{data['Operation']}' {data['Operand1']} and {data['Operand2']} redone successfully.")
        elif action == "clear":
            logger.info("Redoing clear history operation.")
            self.undo_stack.append(("clear", self.history.copy()))
            self.history = pd.DataFrame(columns=self.history.columns)
            logger.info("History cleared after redo.")
            print("History cleared successfully.")
        else:
            logger.error(f"Unknown action '{action}' in redo stack.")
            print(f"Unknown action '{action}' in redo stack.")

    def save_history(self, filename: Optional[str] = None) -> None:
        """Save the calculation history to a CSV file.

        Args:
            filename (Optional[str]): The name of the file to save the history.
                                    Defaults to the environment variable or a default value.
        """
        filename = filename or self.DEFAULT_HISTORY_FILE
        try:
            self.history.to_csv(filename, index=False)
            logger.info(f"History saved to {filename}.")
            print(f"History saved to {filename}.")  # User message
        except Exception as e:
            logger.error(f"Failed to save history to {filename}: {e}")
            print(f"Failed to save history to {filename}: {e}")  # User message

    def load_history(self, filename: Optional[str] = None) -> None:
        """Load calculation history from a CSV file.

        Args:
            filename (Optional[str]): The name of the file to load the history from.
                                      Defaults to the environment variable or a default value.
        """
        filename = filename or self.DEFAULT_HISTORY_FILE
        try:
            self.history = pd.read_csv(filename)
            self.undo_stack.clear()
            self.redo_stack.clear()
            logger.info(f"History loaded from {filename}.")
            print(f"History loaded from {filename}.")  # User message
        except FileNotFoundError:
            logger.error(f"File {filename} not found.")
            print(f"File {filename} not found.")  # User message
        except Exception as e:
            logger.error(f"Failed to load history from {filename}: {e}")
            print(f"Failed to load history from {filename}: {e}")  # User message
