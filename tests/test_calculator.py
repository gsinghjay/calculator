""" tests/test_calculator.py """
import sys
import pytest # type: ignore
from io import StringIO
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

# Helper function to capture print statements
def run_calculator_with_input(monkeypatch, inputs):
    """
    Simulates user input and captures output from the calculator REPL.
    
    :param monkeypatch: pytest fixture to simulate user input
    :param inputs: list of inputs to simulate
    :return: captured output as a string
    """
    input_iterator = iter(inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(input_iterator))

    # Capture the output of the calculator
    old_stdout = sys.stdout
    captured_output = StringIO()
    sys.stdout = captured_output
    
    try:
        calculator()
    finally:
        sys.stdout = old_stdout  # Ensure stdout is always restored
    
    return captured_output.getvalue()

def test_operation_registry_overwrite_and_return():
    """Test that registering an operation with the same name triggers a warning and returns the class."""
    # Clear the registry before test
    operation_registry.clear()
    
    # Create test operation classes
    class TestOperation(TemplateOperation):
        def execute(self, a: float, b: float) -> float:
            return a + b
    
    class AnotherTestOperation(TemplateOperation):
        def execute(self, a: float, b: float) -> float:
            return a + b
    
    # Register the first operation and verify the return value
    decorator = register_operation("test_op")
    decorated_class = decorator(TestOperation)
    assert decorated_class == TestOperation  # Verify the decorator returns the class
    
    # Register another operation with the same name
    with pytest.warns(UserWarning):
        decorator = register_operation("test_op")
        decorated_class = decorator(AnotherTestOperation)
        assert decorated_class == AnotherTestOperation  # Verify the decorator returns the class
        
    # Verify that the registry contains the new operation
    assert operation_registry["test_op"] == AnotherTestOperation

# Positive test cases using parametrize
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

# Negative test cases using parametrize
@pytest.mark.parametrize("test_input,expected_error", [
    # Invalid operations
    ("invalid_op 1 2", "Unknown operation"),
    ("mod 5 2", "Unknown operation"),
    
    # Invalid input formats
    ("add", "Invalid input"),
    ("add 1", "Invalid input"),
    ("add 1 2 3", "Invalid input"),
    ("add abc def", "Invalid input"),
    
    # Division by zero
    ("divide 5 0", "Division by zero"),
])
def test_invalid_operations(monkeypatch, test_input, expected_error):
    """Test various invalid operations and inputs."""
    inputs = [test_input, "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert expected_error in output

# Additional test for help command
def test_help_command(monkeypatch):
    """Test that the help command displays the expected information."""
    inputs = ["help", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Available commands:" in output
    assert "add <num1> <num2>" in output
    assert "subtract <num1> <num2>" in output
    assert "multiply <num1> <num2>" in output
    assert "divide <num1> <num2>" in output

# Test for clean exit
def test_exit_command(monkeypatch):
    """Test that the exit command works properly."""
    inputs = ["exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Exiting calculator..." in output

@pytest.fixture(autouse=True)
def setup_operations():
    """Setup operations before each test."""
    # Clear the registry
    operation_registry.clear()
    
    # Re-register the operations
    register_operation('add')(Addition)
    register_operation('subtract')(Subtraction)
    register_operation('multiply')(Multiplication)
    register_operation('divide')(Division)