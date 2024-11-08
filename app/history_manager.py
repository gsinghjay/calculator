"""Module for managing calculation history."""

import csv
from typing import Optional, Tuple, List, Dict


class HistoryManager:
    """
    Manages calculation history using a list of dictionaries.
    Supports history display, clear, undo, redo, save, and load operations.
    """

    def __init__(self):
        self.history: List[Dict[str, float]] = []
        self.undo_stack: List[Tuple[str, int, Optional[Dict[str, float]]]] = []
        self.redo_stack: List[Tuple[str, int, Optional[Dict[str, float]]]] = []

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
        entry = self._create_new_entry(operation, operand1, operand2, result)
        self.history.append(entry)
        self.undo_stack.append(("add", len(self.history) - 1, None))
        self.redo_stack.clear()

    def show_history(self) -> None:
        """Display the calculation history."""
        if not self.history:
            print("No history available.")
            return

        # Determine column widths for pretty printing
        headers = ["Operation", "Operand1", "Operand2", "Result"]
        col_widths = {header: len(header) for header in headers}

        for entry in self.history:
            for header in headers:
                col_widths[header] = max(col_widths[header], len(str(entry[header])))

        # Create format string
        row_format = "  ".join(
            [f"{{:<{col_widths[header]}}}" for header in headers]
        )

        # Print headers
        print(row_format.format(*headers))

        # Print separator
        print("  ".join(["-" * col_widths[header] for header in headers]))

        # Print each entry
        for entry in self.history:
            print(
                row_format.format(
                    entry["Operation"],
                    entry["Operand1"],
                    entry["Operand2"],
                    entry["Result"],
                )
            )


    def clear_history(self) -> None:
        """Clear the calculation history."""
        # Save current history for undo
        previous_history = self.history.copy()
        self.undo_stack.append(("clear", len(previous_history), previous_history))
        self.history.clear()
        self.redo_stack.clear()
        print("History cleared.")

    def undo(self) -> None:
        """Undo the last operation."""
        if not self.undo_stack:
            print("Nothing to undo.")
            return

        action, index, entry = self.undo_stack.pop()

        if action == "add":
            removed_entry = self.history.pop(index)
            self.redo_stack.append(("add", index, removed_entry))
            print(
                f"Undone: {removed_entry['Operation']} {removed_entry['Operand1']} "
                f"{removed_entry['Operand2']} = {removed_entry['Result']}"
            )
        elif action == "clear":
            print("Undoing clear history operation.")
            # Restore the previous history
            self.history = entry
            self.redo_stack.append(("clear", index, self.history.copy()))
            print("History restored.")
        else:
            print(f"Unknown action '{action}' in undo stack.")


    def redo(self) -> None:
        """Redo the last undone operation."""
        if not self.redo_stack:
            print("Nothing to redo.")
            return

        action, index, entry = self.redo_stack.pop()

        if action == "add" and entry:
            self.history.append(entry)
            self.undo_stack.append(("add", len(self.history) - 1, None))
            print(
                f"Redone: {entry['Operation']} {entry['Operand1']} "
                f"{entry['Operand2']} = {entry['Result']}"
            )

        elif action == "clear":
            # Redoing clear
            print("Redoing clear history operation.")
            self.history.clear()
            self.undo_stack.append(("clear", 0, None))
            print("History cleared.")
        else:
            print(f"Unknown action '{action}' in redo stack.")

    def save_history(self, filename: str) -> None:
        """Save the calculation history to a CSV file.

        Args:
            filename (str): The name of the file to save the history.
        """
        try:
            with open(filename, mode="w", newline="") as csvfile:
                fieldnames = ["Operation", "Operand1", "Operand2", "Result"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for entry in self.history:
                    writer.writerow(entry)
            print(f"History saved to {filename}.")
        except Exception as e:
            print(f"Failed to save history to {filename}: {e}")

    def load_history(self, filename: str) -> None:
        """Load calculation history from a CSV file.

        Args:
            filename (str): The name of the file to load the history from.
        """
        try:
            with open(filename, mode="r", newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                loaded_history = []
                for row in reader:
                    loaded_entry = {
                        "Operation": row["Operation"],
                        "Operand1": float(row["Operand1"]),
                        "Operand2": float(row["Operand2"]),
                        "Result": float(row["Result"]),
                    }
                    loaded_history.append(loaded_entry)

            self.history = loaded_history
            self.undo_stack.clear()
            self.redo_stack.clear()
            print(f"History loaded from {filename}.")
        except FileNotFoundError:
            print(f"File {filename} not found.")
        except Exception as e:
            print(f"Failed to load history from {filename}: {e}")
