# pylint: disable=redefined-outer-name
# pylint: disable=protected-access


"""Test cases for the HistoryManager class."""

from unittest.mock import mock_open, patch
import pytest  # type: ignore
from app.history_manager import HistoryManager


@pytest.fixture
def history_mgr():
    """Fixture to create a new HistoryManager instance for each test."""
    return HistoryManager()


def test_initialization(history_mgr):
    """Test that HistoryManager initializes with empty history and stacks."""
    assert history_mgr.history == []
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
    assert history_mgr.history[0] == {
        "Operation": "multiply",
        "Operand1": 2.0,
        "Operand2": 4.0,
        "Result": 8.0,
    }
    assert len(history_mgr.undo_stack) == 1
    assert history_mgr.undo_stack[-1] == ("add", 0, None)
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

    # Split the output into lines
    output_lines = captured.out.strip().split('\n')
    # The first two lines are headers and separator
    data_lines = output_lines[2:]

    # Extract data from each line
    history_output = []
    for line in data_lines:
        # Split the line based on whitespace
        columns = line.strip().split()
        history_output.append(columns)

    expected_history = [
        ["add", "1.0", "2.0", "3.0"],
        ["subtract", "5.0", "3.0", "2.0"],
    ]

    # Compare the output data with expected data
    assert history_output == expected_history


def test_clear_history(history_mgr, capsys):
    """Test clear_history clears the history and updates stacks."""
    history_mgr.add_entry("add", 1.0, 2.0, 3.0)
    history_mgr.clear_history()
    assert history_mgr.history == []
    assert len(history_mgr.undo_stack) == 2  # One for add and one for clear

    # Since we now store the previous history in the undo_stack, update the assertion
    expected_previous_history = [
        {"Operation": "add", "Operand1": 1.0, "Operand2": 2.0, "Result": 3.0}
    ]
    assert history_mgr.undo_stack[-1] == ("clear", 1, expected_previous_history)
    assert history_mgr.redo_stack == []
    captured = capsys.readouterr()
    assert captured.out.strip() == "History cleared."



def test_undo_add(history_mgr, capsys):
    """Test undoing an 'add' operation."""
    history_mgr.add_entry("add", 1.0, 2.0, 3.0)
    history_mgr.undo()
    assert history_mgr.history == []
    assert len(history_mgr.redo_stack) == 1
    assert history_mgr.redo_stack[-1] == (
        "add",
        0,
        {
            "Operation": "add",
            "Operand1": 1.0,
            "Operand2": 2.0,
            "Result": 3.0,
        },
    )
    captured = capsys.readouterr()
    assert captured.out.strip() == "Undone: add 1.0 2.0 = 3.0"


def test_undo_clear(history_mgr, capsys):
    """Test undoing a 'clear' operation."""
    history_mgr.add_entry("add", 1.0, 2.0, 3.0)
    history_mgr.clear_history()
    history_mgr.undo()
    captured = capsys.readouterr()
    assert "Undoing clear history operation." in captured.out
    assert "History restored." in captured.out
    # After undoing clear, the history should be restored
    assert history_mgr.history == [
        {"Operation": "add", "Operand1": 1.0, "Operand2": 2.0, "Result": 3.0}
    ]


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
    assert history_mgr.history[0] == {
        "Operation": "add",
        "Operand1": 1.0,
        "Operand2": 2.0,
        "Result": 3.0,
    }
    assert history_mgr.undo_stack == [("add", 0, None)]
    assert history_mgr.redo_stack == []
    captured = capsys.readouterr()
    assert captured.out.strip() == "Undone: add 1.0 2.0 = 3.0\nRedone: add 1.0 2.0 = 3.0"


def test_redo_clear(history_mgr, capsys):
    """Test redoing a 'clear' operation."""
    history_mgr.add_entry("add", 1.0, 2.0, 3.0)
    history_mgr.clear_history()
    history_mgr.undo()
    history_mgr.redo()
    assert history_mgr.history == []
    assert len(history_mgr.undo_stack) == 2
    assert history_mgr.undo_stack[-1] == ("clear", 0, None)
    captured = capsys.readouterr()
    assert "History cleared." in captured.out


def test_redo_nothing(history_mgr, capsys):
    """Test redo when there is nothing to redo."""
    history_mgr.redo()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Nothing to redo."


def test_save_history_success(history_mgr):
    """Test saving history to a CSV file successfully."""
    history_mgr.add_entry("add", 1.0, 2.0, 3.0)
    history_mgr.add_entry("multiply", 2.0, 4.0, 8.0)
    mock = mock_open()
    with patch("builtins.open", mock):
        history_mgr.save_history("test_history.csv")
        mock.assert_called_with("test_history.csv", mode="w", newline="")
        handle = mock()
        handle.write.assert_any_call("Operation,Operand1,Operand2,Result\r\n")
        handle.write.assert_any_call("add,1.0,2.0,3.0\r\n")
        handle.write.assert_any_call("multiply,2.0,4.0,8.0\r\n")


def test_save_history_failure(history_mgr, capsys):
    """Test saving history to a CSV file fails."""
    history_mgr.add_entry("add", 1.0, 2.0, 3.0)
    with patch("builtins.open", side_effect=Exception("Write error")):
        history_mgr.save_history("test_history.csv")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Failed to save history to test_history.csv: Write error"


def test_load_history_success(history_mgr):
    """Test loading history from a CSV file successfully."""
    mock_data = "Operation,Operand1,Operand2,Result\r\nadd,1.0,2.0,3.0\r\nmultiply,2.0,4.0,8.0\r\n"
    mock = mock_open(read_data=mock_data)
    with patch("builtins.open", mock):
        history_mgr.load_history("test_history.csv")
        assert history_mgr.history == [
            {"Operation": "add", "Operand1": 1.0, "Operand2": 2.0, "Result": 3.0},
            {"Operation": "multiply", "Operand1": 2.0, "Operand2": 4.0, "Result": 8.0},
        ]
        assert history_mgr.undo_stack == []
        assert history_mgr.redo_stack == []


def test_load_history_file_not_found(history_mgr, capsys):
    """Test loading history from a non-existent CSV file."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        history_mgr.load_history("non_existent.csv")
    captured = capsys.readouterr()
    assert captured.out.strip() == "File non_existent.csv not found."


def test_load_history_failure(history_mgr, capsys):
    """Test loading history from a CSV file fails due to invalid format."""
    mock_data = "Operation,Operand1,Operand2,Result\r\nadd,1.0,invalid,3.0\r\n"
    mock = mock_open(read_data=mock_data)
    with patch("builtins.open", mock):
        history_mgr.load_history("invalid_history.csv")
    captured = capsys.readouterr()
    assert "Failed to load history from invalid_history.csv:" in captured.out


def test_undo_add_multiple(history_mgr, capsys):
    """Test undoing multiple 'add' operations."""
    history_mgr.add_entry("add", 1.0, 2.0, 3.0)
    history_mgr.add_entry("add", 4.0, 5.0, 9.0)
    history_mgr.undo()
    history_mgr.undo()
    assert history_mgr.history == []
    assert len(history_mgr.redo_stack) == 2
    assert history_mgr.redo_stack[0][0] == "add"
    assert history_mgr.redo_stack[1][0] == "add"
    captured = capsys.readouterr()
    expected_output = (
        "Undone: add 4.0 5.0 = 9.0\n"
        "Undone: add 1.0 2.0 = 3.0"
    )
    assert captured.out.strip() == expected_output


def test_redo_add_multiple(history_mgr, capsys):
    """Test redoing multiple 'add' operations."""
    history_mgr.add_entry("add", 1.0, 2.0, 3.0)
    history_mgr.add_entry("add", 4.0, 5.0, 9.0)
    history_mgr.undo()
    history_mgr.undo()
    history_mgr.redo()
    history_mgr.redo()
    assert len(history_mgr.history) == 2
    assert history_mgr.history[0]["Result"] == 3.0
    assert history_mgr.history[1]["Result"] == 9.0
    assert history_mgr.undo_stack == [("add", 0, None), ("add", 1, None)]
    assert history_mgr.redo_stack == []
    captured = capsys.readouterr()
    assert captured.out.strip() == (
        "Undone: add 4.0 5.0 = 9.0\n"
        "Undone: add 1.0 2.0 = 3.0\n"
        "Redone: add 1.0 2.0 = 3.0\n"
        "Redone: add 4.0 5.0 = 9.0"
    )


def test_undo_unknown_action(history_mgr, capsys):
    """Test undo with an unknown action."""
    # Inject an invalid action into the undo stack
    history_mgr.undo_stack.append(("unknown_action", 0, None))
    history_mgr.undo()
    captured = capsys.readouterr()
    assert "Unknown action 'unknown_action' in undo stack." in captured.out


def test_redo_unknown_action(history_mgr, capsys):
    """Test redo with an unknown action."""
    # Inject an invalid action into the redo stack
    history_mgr.redo_stack.append(("unknown_action", 0, None))
    history_mgr.redo()
    captured = capsys.readouterr()
    assert "Unknown action 'unknown_action' in redo stack." in captured.out
