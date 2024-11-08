# app/history_manager.py

"""Module for managing calculation history using pandas DataFrame."""

import pandas as pd
from typing import Optional, Tuple, List, Dict


class HistoryManager:
    """
    Manages calculation history using a pandas DataFrame.
    Supports history display, clear, undo, redo, save, and load operations.
    """

    def __init__(self):
        self.history = pd.DataFrame(columns=["Operation", "Operand1", "Operand2", "Result"])
        self.undo_stack: List[Tuple[str, Optional[pd.DataFrame]]] = []
        self.redo_stack: List[Tuple[str, Optional[pd.DataFrame]]] = []

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
        return {
            "Operation": operation,
            "Operand1": operand1,
            "Operand2": operand2,
            "Result": result,
        }

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
        else:
            self.history = pd.concat([self.history, entry], ignore_index=True)
        self.undo_stack.append(("add", entry))
        self.redo_stack.clear()

    def show_history(self) -> None:
        """Display the calculation history."""
        if self.history.empty:
            print("No history available.")
            return

        print(self.history.to_string(index=False))

    def clear_history(self) -> None:
        """Clear the calculation history."""
        # Save current history for undo
        previous_history = self.history.copy()
        self.undo_stack.append(("clear", previous_history))
        self.history = pd.DataFrame(columns=self.history.columns)
        self.redo_stack.clear()
        print("History cleared.")

    def undo(self) -> None:
        """Undo the last operation."""
        if not self.undo_stack:
            print("Nothing to undo.")
            return

        action, data = self.undo_stack.pop()

        if action == "add":
            if self.history.empty:
                print("Nothing to undo.")
                return
            removed_entry = self.history.iloc[-1]
            self.history = self.history.iloc[:-1]
            self.redo_stack.append(("add", removed_entry))
            print(
                f"Undone: {removed_entry['Operation']} {removed_entry['Operand1']} "
                f"{removed_entry['Operand2']} = {removed_entry['Result']}"
            )
        elif action == "clear":
            print("Undoing clear history operation.")
            self.redo_stack.append(("clear", self.history.copy()))
            self.history = data
            print("History restored.")
        else:
            print(f"Unknown action '{action}' in undo stack.")

    def redo(self) -> None:
        """Redo the last undone operation."""
        if not self.redo_stack:
            print("Nothing to redo.")
            return

        action, data = self.redo_stack.pop()

        if action == "add":
            self.history = pd.concat([self.history, data.to_frame().T], ignore_index=True)
            self.undo_stack.append(("add", data.to_frame().T))
            print(
                f"Redone: {data['Operation']} {data['Operand1']} "
                f"{data['Operand2']} = {data['Result']}"
            )
        elif action == "clear":
            print("Redoing clear history operation.")
            self.undo_stack.append(("clear", self.history.copy()))
            self.history = pd.DataFrame(columns=self.history.columns)
            print("History cleared.")
        else:
            print(f"Unknown action '{action}' in redo stack.")

    def save_history(self, filename: str) -> None:
        """Save the calculation history to a CSV file.

        Args:
            filename (str): The name of the file to save the history.
        """
        try:
            self.history.to_csv(filename, index=False)
            print(f"History saved to {filename}.")
        except Exception as e:
            print(f"Failed to save history to {filename}: {e}")

    def load_history(self, filename: str) -> None:
        """Load calculation history from a CSV file.

        Args:
            filename (str): The name of the file to load the history from.
        """
        try:
            self.history = pd.read_csv(filename)
            self.undo_stack.clear()
            self.redo_stack.clear()
            print(f"History loaded from {filename}.")
        except FileNotFoundError:
            print(f"File {filename} not found.")
        except Exception as e:
            print(f"Failed to load history from {filename}: {e}")
