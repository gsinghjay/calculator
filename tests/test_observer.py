import unittest
from unittest.mock import MagicMock, patch
from app.observer import HistoryObserver, CalculatorWithObserver
from app.main import Addition, Subtraction, Multiplication, Division

class TestObserverPattern(unittest.TestCase):

   
    def setUp(self):
        self.calculator = CalculatorWithObserver()
        self.mock_observer = HistoryObserver()
        self.calculator.add_observer(self.mock_observer)

    def test_add_observer(self):
        # Ensure the observer is added
        self.assertIn(self.mock_observer, self.calculator._observers)

    def test_notify_observers(self):
        # Mock operation with a calculate method
        mock_operation = MagicMock()
        mock_operation.calculate.return_value = 42  # Mock return value

        # Perform the operation
        result = self.calculator.perform_operation(mock_operation, 1, 2)

        # Verify the result and history update
        self.assertEqual(result, 42)
        self.assertIn(42, self.calculator._history)

    @patch('app.observer.logging.info')
    def test_logging_info_called(self, mock_logging_info):
        # Mock operation with a calculate method
        mock_operation = MagicMock()
        mock_operation.calculate.return_value = 42  # Mock return value

        # Perform the operation
        self.calculator.perform_operation(mock_operation, 1, 2)

        # Check if logging.info was called with the correct message
        mock_logging_info.assert_called_with("Observer: New calculation added -> 42")

    def test_perform_operation_addition(self):
        # Test the perform_operation method with addition
        addition_operation = Addition()
        result = self.calculator.perform_operation(addition_operation, 3, 4)
        self.assertEqual(result, 7)
        self.assertEqual(len(self.calculator._history), 1)

    def test_perform_operation_subtraction(self):
        # Test the perform_operation method with subtraction
        subtraction_operation = Subtraction()
        result = self.calculator.perform_operation(subtraction_operation, 5, 3)
        self.assertEqual(result, 2)
        self.assertEqual(len(self.calculator._history), 1)

    def test_perform_operation_multiplication(self):
        # Test the perform_operation method with multiplication
        multiplication_operation = Multiplication()
        result = self.calculator.perform_operation(multiplication_operation, 2, 3)
        self.assertEqual(result, 6)
        self.assertEqual(len(self.calculator._history), 1)

    def test_perform_operation_division(self):
        # Test the perform_operation method with division
        division_operation = Division()
        result = self.calculator.perform_operation(division_operation, 6, 2)
        self.assertEqual(result, 3)
        self.assertEqual(len(self.calculator._history), 1)

    def test_perform_operation_division_by_zero(self):
        # Test division by zero raises ValueError
        division_operation = Division()
        with self.assertRaises(ValueError):
            self.calculator.perform_operation(division_operation, 6, 0)

if __name__ == '__main__':
    unittest.main()