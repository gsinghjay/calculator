"""Test cases for the template operation classes."""
import logging
import pytest  # type: ignore
from app.template_operation import Addition, Subtraction, Multiplication, Division


def test_addition():
    """Test the Addition operation."""
    operation = Addition()
    assert operation.calculate(1, 2) == 3
    assert operation.calculate(-1, -2) == -3
    assert operation.calculate(0, 0) == 0
    assert operation.calculate(1e10, 1e10) == 2e10  # Edge case with large numbers


def test_subtraction():
    """Test the Subtraction operation."""
    operation = Subtraction()
    assert operation.calculate(5, 3) == 2
    assert operation.calculate(-1, -2) == 1
    assert operation.calculate(0, 0) == 0
    assert operation.calculate(1e10, 1e10) == 0  # Edge case with large numbers


def test_multiplication():
    """Test the Multiplication operation."""
    operation = Multiplication()
    assert operation.calculate(2, 3) == 6
    assert operation.calculate(-1, -2) == 2
    assert operation.calculate(0, 5) == 0
    assert operation.calculate(1e5, 1e5) == 1e10  # Edge case with large numbers


def test_division():
    """Test the Division operation."""
    operation = Division()
    assert operation.calculate(6, 3) == 2
    assert operation.calculate(-6, -3) == 2
    assert operation.calculate(1e10, 1e5) == 1e5  # Edge case with large numbers
    with pytest.raises(ValueError, match="Division by zero is not allowed."):
        operation.calculate(1, 0)


def test_invalid_inputs():
    """Test invalid inputs for the operations."""
    operation = Addition()  # Using Addition to test input validation
    with pytest.raises(ValueError, match="Both inputs must be numbers."):
        operation.calculate("a", 1)
    with pytest.raises(ValueError, match="Both inputs must be numbers."):
        operation.calculate(1, "b")


def test_logging(caplog):
    """Test logging for the Division operation."""
    operation = Division()
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError):
            operation.calculate(1, 0)
    assert "Attempted to divide by zero." in caplog.text
