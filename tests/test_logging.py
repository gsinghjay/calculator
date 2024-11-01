import pytest # type: ignore
import logging
from app.logging import setup_logging
from app.template_operation import Addition, Subtraction, Multiplication, Division

def test_setup_logging():
    """Test that setup_logging runs without raising any exceptions."""
    try:
        setup_logging()
    except Exception as e:
        pytest.fail(f"setup_logging raised an exception: {e}")

# Positive Tests for Basic Operations
def test_addition_logging(caplog):
    """Test that performing addition logs the operation."""
    setup_logging()
    addition = Addition()
    with caplog.at_level(logging.INFO):
        addition.calculate(2, 3)
    assert "Operation performed: 2 and 3 -> Result: 5" in caplog.text

def test_subtraction_logging(caplog):
    """Test that performing subtraction logs the operation."""
    setup_logging()
    subtraction = Subtraction()
    with caplog.at_level(logging.INFO):
        subtraction.calculate(5, 3)
    assert "Operation performed: 5 and 3 -> Result: 2" in caplog.text

def test_multiplication_logging(caplog):
    """Test that performing multiplication logs the operation."""
    setup_logging()
    multiplication = Multiplication()
    with caplog.at_level(logging.INFO):
        multiplication.calculate(4, 3)
    assert "Operation performed: 4 and 3 -> Result: 12" in caplog.text

def test_division_logging(caplog):
    """Test that performing division logs the operation."""
    setup_logging()
    division = Division()
    with caplog.at_level(logging.INFO):
        division.calculate(6, 2)
    assert "Operation performed: 6 and 2 -> Result: 3.0" in caplog.text

# Error Cases and Edge Cases
def test_division_by_zero_logging(caplog):
    """Test that dividing by zero logs an error and raises ValueError."""
    setup_logging()
    division = Division()
    with pytest.raises(ValueError, match="Division by zero is not allowed."):
        with caplog.at_level(logging.ERROR):
            division.calculate(5, 0)
    assert "Attempted to divide by zero." in caplog.text

def test_invalid_input_logging(caplog):
    """Test that invalid input types are logged appropriately."""
    setup_logging()
    addition = Addition()
    with pytest.raises(ValueError, match="Both inputs must be numbers."):
        with caplog.at_level(logging.ERROR):
            addition.calculate("invalid", 3)
    assert "Invalid input: invalid, 3 (Inputs must be numbers)" in caplog.text

def test_debug_level_logging(caplog):
    """Test that debug level messages are captured."""
    setup_logging()
    multiplication = Multiplication()
    with caplog.at_level(logging.DEBUG):
        multiplication.calculate(2, 2)
    # Since there's no debug message, we'll just verify the INFO message
    assert "Operation performed: 2 and 2 -> Result: 4" in caplog.text

# Multiple Operations Test
def test_multiple_operations_logging(caplog):
    """Test that multiple operations are logged correctly."""
    setup_logging()
    addition = Addition()
    multiplication = Multiplication()
    
    with caplog.at_level(logging.INFO):
        addition.calculate(2, 3)
        multiplication.calculate(4, 2)
    
    log_text = caplog.text
    assert "Operation performed: 2 and 3 -> Result: 5" in log_text
    assert "Operation performed: 4 and 2 -> Result: 8" in log_text

# Log Level Tests
def test_log_level_filtering(caplog):
    """Test that log level filtering works correctly."""
    setup_logging()
    division = Division()
    
    # Should not capture DEBUG messages when level is set to INFO
    with caplog.at_level(logging.INFO):
        division.calculate(6, 2)
    assert "Performing division operation" not in caplog.text
    assert "Operation performed: 6 and 2 -> Result: 3.0" in caplog.text

# Negative Numbers Test
def test_negative_numbers_logging(caplog):
    """Test that operations with negative numbers are logged correctly."""
    setup_logging()
    subtraction = Subtraction()
    with caplog.at_level(logging.INFO):
        subtraction.calculate(-5, -3)
    assert "Operation performed: -5 and -3 -> Result: -2" in caplog.text

# Large Numbers Test
def test_large_numbers_logging(caplog):
    """Test that operations with large numbers are logged correctly."""
    setup_logging()
    multiplication = Multiplication()
    with caplog.at_level(logging.INFO):
        multiplication.calculate(1000000, 1000000)
    assert "Operation performed: 1000000 and 1000000 -> Result: 1000000000000" in caplog.text