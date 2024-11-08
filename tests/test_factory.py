"""Test cases for the OperationFactory."""
import pytest # type: ignore
from app.factory import OperationFactory
from app.template_operation import Addition, Subtraction, Multiplication, Division

@pytest.mark.parametrize("operation_name, expected_type", [
    ("add", Addition),
    ("ADD", Addition),
    ("Add", Addition),
    ("subtract", Subtraction),
    ("SUBTRACT", Subtraction),
    ("Subtract", Subtraction),
    ("multiply", Multiplication),
    ("MULTIPLY", Multiplication),
    ("Multiply", Multiplication),
    ("divide", Division),
    ("DIVIDE", Division),
    ("Divide", Division),
])
def test_create_operation_positive(operation_name, expected_type):
    """
    Test that OperationFactory correctly creates operations for valid inputs.
    Tests case-insensitive operation names.
    """
    operation = OperationFactory.create_operation(operation_name)
    assert isinstance(operation, expected_type)

@pytest.mark.parametrize("invalid_operation", [
    "",
    "invalid",
    "plus",
    "minus",
    "times",
    "divided",
    None,
    "123",
    "add ",  # with space
    " add",  # with space
    "ad d",  # with space in middle
])
def test_create_operation_negative(invalid_operation):
    """
    Test that OperationFactory returns None for invalid operations.
    Tests various invalid inputs including empty strings, incorrect operation names,
    and operations with spaces.
    """
    operation = OperationFactory.create_operation(invalid_operation)
    assert operation is None

@pytest.mark.parametrize("operation_name, a, b, expected", [
    ("add", 2, 3, 5),
    ("subtract", 5, 3, 2),
    ("multiply", 4, 3, 12),
    ("divide", 6, 2, 3.0),
])
def test_created_operation_calculation(operation_name, a, b, expected):
    """
    Test that operations created by the factory perform calculations correctly.
    Tests actual calculation results for each operation type.
    """
    operation = OperationFactory.create_operation(operation_name)
    assert operation.calculate(a, b) == expected

def test_division_by_zero():
    """Test that division by zero raises ValueError."""
    operation = OperationFactory.create_operation("divide")
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        operation.calculate(5, 0)

@pytest.mark.parametrize("operation_name, a, b", [
    ("add", 1e308, 1e308),  # Very large numbers
    ("subtract", -1e308, 1e308),
    ("multiply", 1e308, 0),
    ("divide", 1e308, 1e308),
])
def test_operation_edge_cases(operation_name, a, b):
    """
    Test edge cases with very large numbers and extreme values.
    Ensures operations handle edge cases without raising exceptions.
    """
    operation = OperationFactory.create_operation(operation_name)
    try:
        result = operation.calculate(a, b)
        assert isinstance(result, (int, float))
    except OverflowError:
        pytest.skip("Overflow is an acceptable outcome for extreme values")

@pytest.mark.parametrize("operation_name", [
    "add", "subtract", "multiply", "divide"
])
def test_operation_instance_independence(operation_name):
    """
    Test that factory creates independent instances each time.
    Ensures no shared state between instances of the same operation type.
    """
    operation1 = OperationFactory.create_operation(operation_name)
    operation2 = OperationFactory.create_operation(operation_name)
    assert operation1 is not operation2
