# pylint: disable=redefined-outer-name
# pylint: disable=protected-access
# tests/test_history_manager.py

"""Test cases for the HistoryManager class."""

from unittest.mock import patch
import pandas as pd
import pytest  # type: ignore
from app.history_manager import HistoryManager


@pytest.fixture
def history_mgr():
    """Fixture to create a new HistoryManager instance for each test."""
    return HistoryManager()


def test_initialization(history_mgr):
    """Test that HistoryManager initializes with empty history and stacks."""
    assert history_mgr.history.empty
    assert history_mgr.undo_stack == []
    assert history_mgr.redo_stack == []


def test_create_new_entry(history_mgr):
    """Test the _create_new_entry method creates the correct dictionary."""
    operation = "add"
    operand1 = 5.0
    operand2 = 3.0
    result = 8.0
    expected_entry = {
        "Operation": operation,
        "Operand1": operand1,
        "Operand2": operand2,
        "Result": result,
    }
    entry = history_mgr._create_new_entry(operation, operand1, operand2, result)
    assert entry == expected_entry


def test_add_entry(history_mgr):
    """Test adding a new entry updates history and undo stack correctly."""
    history_mgr.add_entry("multiply", 2.0, 4.0, 8.0)
    assert len(history_mgr.history) == 1
    assert history_mgr.history.iloc[0].to_dict() == {
        "Operation": "multiply",
        "Operand1": 2.0,
        "Operand2": 4.0,
        "Result": 8.0,
    }
    assert len(history_mgr.undo_stack) == 1
    assert history_mgr.undo_stack[-1][0] == "add"
    assert history_mgr.redo_stack == []


def test_show_history_empty(history_mgr, capsys):
    """Test show_history displays the correct message when history is empty."""
    history_mgr.show_history()
    captured = capsys.readouterr()
    assert captured.out.strip() == "No history available."


def test_show_history_non_empty(history_mgr, capsys):
    """Test show_history displays the correct table when history has entries."""
    history_mgr.add_entry("add", 1.0, 2.0, 3.0)
    history_mgr.add_entry("subtract", 5.0, 3.0, 2.0)
    history_mgr.show_history()
    captured = capsys.readouterr()

    output = captured.out.strip()
    assert "add" in output
    assert "1.0" in output
    assert "2.0" in output
    assert "3.0" in output
    assert "subtract" in output
    assert "5.0" in output
    assert "3.0" in output
    assert "2.0" in output


def test_clear_history(history_mgr, capsys):
    """Test clear_history clears the history and updates stacks."""
    history_mgr.add_entry("add", 1.0, 2.0, 3.0)
    history_mgr.clear_history()
    assert history_mgr.history.empty
    assert len(history_mgr.undo_stack) == 2  # One for add and one for clear
    assert history_mgr.redo_stack == []
    captured = capsys.readouterr()
    assert "Operation 'add' added successfully." in captured.out
    assert "History cleared successfully." in captured.out


def test_undo_add(history_mgr, capsys):
    """Test undoing an 'add' operation."""
    history_mgr.add_entry("add", 1.0, 2.0, 3.0)
    history_mgr.undo()
    assert history_mgr.history.empty
    assert len(history_mgr.redo_stack) == 1
    assert history_mgr.redo_stack[-1][0] == "add"
    captured = capsys.readouterr()
    expected_output = "Operation 'add' added successfully.\nOperation 'add' undone successfully."
    assert captured.out.strip() == expected_output


def test_undo_clear(history_mgr, capsys):
    """Test undoing a 'clear' operation."""
    history_mgr.add_entry("add", 1.0, 2.0, 3.0)
    history_mgr.clear_history()
    history_mgr.undo()
    captured = capsys.readouterr()
    assert "History restoration after undo successful." in captured.out

def test_undo_nothing(history_mgr, capsys):
    """Test undo when there is nothing to undo."""
    history_mgr.undo()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Nothing to undo."


def test_redo_add(history_mgr, capsys):
    """Test redoing an 'add' operation."""
    history_mgr.add_entry("add", 1.0, 2.0, 3.0)
    history_mgr.undo()
    history_mgr.redo()
    assert len(history_mgr.history) == 1
    assert history_mgr.history.iloc[0]["Result"] == 3.0
    assert len(history_mgr.undo_stack) == 1
    assert history_mgr.redo_stack == []
    captured = capsys.readouterr()
    expected_output = (
        "Operation 'add' added successfully.\n"
        "Operation 'add' undone successfully.\n"
        "Operation 'add' redone successfully."
    )
    assert captured.out.strip() == expected_output


def test_redo_clear(history_mgr, capsys):
    """Test redoing a 'clear' operation."""
    history_mgr.add_entry("add", 1.0, 2.0, 3.0)
    history_mgr.clear_history()
    history_mgr.undo()
    history_mgr.redo()
    assert history_mgr.history.empty
    assert len(history_mgr.undo_stack) == 2
    captured = capsys.readouterr()
    assert "History cleared successfully." in captured.out


def test_redo_nothing(history_mgr, capsys):
    """Test redo when there is nothing to redo."""
    history_mgr.redo()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Nothing to redo."


def test_save_history_success(history_mgr):
    """Test saving history to a CSV file successfully."""
    history_mgr.add_entry("add", 1.0, 2.0, 3.0)
    history_mgr.add_entry("multiply", 2.0, 4.0, 8.0)
    with patch("pandas.DataFrame.to_csv") as mock_to_csv:
        history_mgr.save_history("test_history.csv")
        mock_to_csv.assert_called_once_with("test_history.csv", index=False)


def test_save_history_failure(history_mgr, capsys):
    """Test saving history to a CSV file fails."""
    history_mgr.add_entry("add", 1.0, 2.0, 3.0)
    with patch("pandas.DataFrame.to_csv", side_effect=Exception("Write error")):
        history_mgr.save_history("test_history.csv")
    captured = capsys.readouterr()
    expected_output = (
        "Operation 'add' added successfully.\n"
        "Failed to save history to test_history.csv: Write error"
    )
    assert captured.out.strip() == expected_output


def test_load_history_success(history_mgr):
    """Test loading history from a CSV file successfully."""
    mock_data = pd.DataFrame({
        "Operation": ["add", "multiply"],
        "Operand1": [1.0, 2.0],
        "Operand2": [2.0, 4.0],
        "Result": [3.0, 8.0],
    })
    with patch("pandas.read_csv", return_value=mock_data):
        history_mgr.load_history("test_history.csv")
        pd.testing.assert_frame_equal(history_mgr.history, mock_data)
        assert history_mgr.undo_stack == []
        assert history_mgr.redo_stack == []


def test_load_history_file_not_found(history_mgr, capsys):
    """Test loading history from a non-existent CSV file."""
    with patch("pandas.read_csv", side_effect=FileNotFoundError):
        history_mgr.load_history("non_existent.csv")
    captured = capsys.readouterr()
    assert captured.out.strip() == "File non_existent.csv not found."


def test_load_history_failure(history_mgr, capsys):
    """Test loading history from a CSV file fails due to invalid format."""
    with patch("pandas.read_csv", side_effect=Exception("Read error")):
        history_mgr.load_history("invalid_history.csv")
    captured = capsys.readouterr()
    assert "Failed to load history from invalid_history.csv: Read error" in captured.out


def test_undo_add_multiple(history_mgr, capsys):
    """Test undoing multiple 'add' operations."""
    history_mgr.add_entry("add", 1.0, 2.0, 3.0)
    history_mgr.add_entry("add", 4.0, 5.0, 9.0)
    history_mgr.undo()
    history_mgr.undo()
    assert history_mgr.history.empty
    assert len(history_mgr.redo_stack) == 2
    captured = capsys.readouterr()
    expected_output = (
        "Operation 'add' added successfully.\n"
        "Operation 'add' added successfully.\n"
        "Operation 'add' undone successfully.\n"
        "Operation 'add' undone successfully."
    )
    assert captured.out.strip() == expected_output


    history_mgr.undo()


def test_undo_unknown_action(history_mgr, capsys):
    """Test undo with an unknown action."""
    # Inject an invalid action into the undo stack
    history_mgr.undo_stack.append(("unknown_action", None))
    history_mgr.undo()
    captured = capsys.readouterr()
    assert "Unknown action 'unknown_action' in undo stack." in captured.out


def test_redo_unknown_action(history_mgr, capsys):
    """Test redo with an unknown action."""
    # Inject an invalid action into the redo stack
    history_mgr.redo_stack.append(("unknown_action", None))
    history_mgr.redo()
    captured = capsys.readouterr()
    assert "Unknown action 'unknown_action' in redo stack." in captured.out

def test_undo_add_when_history_empty(history_mgr, capsys):
    """Test undoing an 'add' operation when history is empty."""
    # Add an entry to the history
    history_mgr.add_entry("add", 1.0, 2.0, 3.0)
    # Manually clear the history without updating the undo stack
    history_mgr.history = pd.DataFrame(columns=history_mgr.history.columns)
    # Now, attempt to undo the 'add' operation
    history_mgr.undo()
    captured = capsys.readouterr()
    expected_output = "Operation 'add' added successfully.\nNothing to undo."
    assert captured.out.strip() == expected_output
