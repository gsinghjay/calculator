""" tests/test_operations.py """
import pytest # type: ignore
from app.operations import addition, subtraction, multiplication, division


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 5),
        (0, 0, 0),
        (-1, 1, 0),
        (10, 5, 15),
        (-2, -3, -5),
    ],
)
def test_addition_positive(a, b, expected):
    """Test positive cases for addition."""
    assert addition(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (-2, -3, -5),
        (-1, 0, -1),
    ],
)
def test_addition_negative(a, b, expected):
    """Test negative cases for addition."""
    assert addition(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (5, 3, 2),
        (0, 0, 0),
        (10, 5, 5),
        (-5, -3, -2),
        (3, 5, -2),
    ],
)
def test_subtraction(a, b, expected):
    """Test cases for subtraction."""
    assert subtraction(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 6),
        (0, 10, 0),
        (-2, -3, 6),
        (2, -3, -6),
        (-2, 3, -6),
    ],
)
def test_multiplication(a, b, expected):
    """Test cases for multiplication."""
    assert multiplication(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (6, 3, 2),
        (-6, -3, 2),
        (6, -3, -2),
        (-6, 3, -2),
    ],
)
def test_division(a, b, expected):
    """Test cases for division."""
    assert division(a, b) == expected


def test_division_by_zero():
    """Test division by zero."""
    with pytest.raises(ValueError, match="Division by zero is not allowed."):
        division(1, 0)
