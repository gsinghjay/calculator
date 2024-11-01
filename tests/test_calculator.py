"""Test cases for the calculator functionality."""
import sys
from io import StringIO
import pytest  # type: ignore
from app.calculator import (
    calculator,
    operation_registry,
    register_operation,
    TemplateOperation,
    Addition,
    Subtraction,
    Multiplication,
    Division
)


def run_calculator_with_input(monkeypatch, inputs):
    """
    Simulates user input and captures output from the calculator REPL.

    :param monkeypatch: pytest fixture to simulate user input
    :param inputs: list of inputs to simulate
    :return: captured output as a string
    """
    input_iterator = iter(inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(input_iterator))

    old_stdout = sys.stdout
    captured_output = StringIO()
    sys.stdout = captured_output

    try:
        calculator()
    finally:
        sys.stdout = old_stdout

    return captured_output.getvalue()


def test_operation_registry_overwrite_and_return():
    """Test that registering an operation with the same name
    triggers a warning and returns the class."""
    operation_registry.clear()

    class TestOperation(TemplateOperation):
        """Test operation class."""
        def execute(self, a: float, b: float) -> float:
            """Execute the test operation."""
            return a + b

    class AnotherTestOperation(TemplateOperation):
        """Another test operation class."""
        def execute(self, a: float, b: float) -> float:
            """Execute the test operation."""
            return a + b

    decorator = register_operation("test_op")
    decorated_class = decorator(TestOperation)
    assert decorated_class == TestOperation

    with pytest.warns(UserWarning):
        decorator = register_operation("test_op")
        decorated_class = decorator(AnotherTestOperation)
        assert decorated_class == AnotherTestOperation

    assert operation_registry["test_op"] == AnotherTestOperation


@pytest.mark.parametrize("operation,num1,num2,expected", [
    ("add", 2, 3, 5.0),
    ("add", -1, 1, 0.0),
    ("add", 0.1, 0.2, 0.3),
    ("subtract", 5, 2, 3.0),
    ("subtract", 2, 5, -3.0),
    ("subtract", 0, 0, 0.0),
    ("multiply", 4, 5, 20.0),
    ("multiply", -2, 3, -6.0),
    ("multiply", 0, 5, 0.0),
    ("divide", 10, 2, 5.0),
    ("divide", 0, 5, 0.0),
    ("divide", -6, 2, -3.0),
])
def test_valid_operations(monkeypatch, operation, num1, num2, expected):
    """Test various valid operations with different inputs."""
    inputs = [f"{operation} {num1} {num2}", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert f"Result: {expected}" in output


@pytest.mark.parametrize("test_input,expected_error", [
    ("invalid_op 1 2", "Unknown operation"),
    ("mod 5 2", "Unknown operation"),
    ("add", "Invalid input"),
    ("add 1", "Invalid input"),
    ("add 1 2 3", "Invalid input"),
    ("add abc def", "Invalid input"),
    ("divide 5 0", "Division by zero"),
])
def test_invalid_operations(monkeypatch, test_input, expected_error):
    """Test various invalid operations and inputs."""
    inputs = [test_input, "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert expected_error in output


def test_help_command(monkeypatch):
    """Test that the help command displays the expected information."""
    inputs = ["help", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Available commands:" in output
    assert "add <num1> <num2>" in output
    assert "subtract <num1> <num2>" in output
    assert "multiply <num1> <num2>" in output
    assert "divide <num1> <num2>" in output


def test_exit_command(monkeypatch):
    """Test that the exit command works properly."""
    inputs = ["exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Exiting calculator..." in output


@pytest.fixture(autouse=True)
def setup_operations():
    """Set up operations before each test."""
    operation_registry.clear()

    register_operation('add')(Addition)
    register_operation('subtract')(Subtraction)
    register_operation('multiply')(Multiplication)
    register_operation('divide')(Division)


# Additional Positive and Negative Tests

@pytest.mark.parametrize("operation_class,a,b,expected", [
    (Addition, 1, 2, 3),
    (Addition, -1, -2, -3),
    (Subtraction, 5, 3, 2),
    (Subtraction, 0, 0, 0),
    (Multiplication, 4, 5, 20),
    (Multiplication, -2, 3, -6),
    (Division, 10, 2, 5),
    (Division, -6, 3, -2),
])
def test_operation_execute_positive(operation_class, a, b, expected):
    """Test the execute method of operation classes with valid inputs."""
    operation_instance = operation_class()
    assert operation_instance.execute(a, b) == expected


@pytest.mark.parametrize("operation_class,a,b,expected_exception", [
    (Division, 5, 0, ValueError),
    (Division, -10, 0, ValueError),
])
def test_operation_execute_negative(operation_class, a, b, expected_exception):
    """Test the execute method of operation classes with invalid inputs."""
    operation_instance = operation_class()
    with pytest.raises(expected_exception):
        operation_instance.execute(a, b)
        