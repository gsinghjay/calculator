"""Test cases for the observer pattern implementation."""
import unittest
from unittest.mock import MagicMock, patch
from app.observer import HistoryObserver, CalculatorWithObserver
from app.main import Addition, Subtraction, Multiplication, Division


class TestObserverPattern(unittest.TestCase):
    """Test class for the observer pattern."""

    def setUp(self):
        """Set up the test environment."""
        self.calculator = CalculatorWithObserver()
        self.mock_observer = HistoryObserver()
        self.calculator.add_observer(self.mock_observer)

    def test_add_observer(self):
        """Test adding an observer to the calculator."""
        # pylint: disable=protected-access
        self.assertIn(self.mock_observer, self.calculator._observers)

    def test_notify_observers(self):
        """Test notifying observers when an operation is performed."""
        mock_operation = MagicMock()
        mock_operation.calculate.return_value = 42

        result = self.calculator.perform_operation(mock_operation, 1, 2)

        self.assertEqual(result, 42)
        # pylint: disable=protected-access
        self.assertIn(42, self.calculator._history)

    @patch('app.observer.logging.info')
    def test_logging_info_called(self, mock_logging_info):
        """Test that logging.info is called with the correct message."""
        mock_operation = MagicMock()
        mock_operation.calculate.return_value = 42

        self.calculator.perform_operation(mock_operation, 1, 2)

        mock_logging_info.assert_called_with("Observer: New calculation added -> 42")

    def test_perform_operation_addition(self):
        """Test performing an addition operation."""
        addition_operation = Addition()
        result = self.calculator.perform_operation(addition_operation, 3, 4)
        self.assertEqual(result, 7)
        # pylint: disable=protected-access
        self.assertEqual(len(self.calculator._history), 1)

    def test_perform_operation_subtraction(self):
        """Test performing a subtraction operation."""
        subtraction_operation = Subtraction()
        result = self.calculator.perform_operation(subtraction_operation, 5, 3)
        self.assertEqual(result, 2)
        # pylint: disable=protected-access
        self.assertEqual(len(self.calculator._history), 1)

    def test_perform_operation_multiplication(self):
        """Test performing a multiplication operation."""
        multiplication_operation = Multiplication()
        result = self.calculator.perform_operation(multiplication_operation, 2, 3)
        self.assertEqual(result, 6)
        # pylint: disable=protected-access
        self.assertEqual(len(self.calculator._history), 1)

    def test_perform_operation_division(self):
        """Test performing a division operation."""
        division_operation = Division()
        result = self.calculator.perform_operation(division_operation, 6, 2)
        self.assertEqual(result, 3)
        # pylint: disable=protected-access
        self.assertEqual(len(self.calculator._history), 1)

    def test_perform_operation_division_by_zero(self):
        """Test performing a division by zero operation."""
        division_operation = Division()
        with self.assertRaises(ValueError):
            self.calculator.perform_operation(division_operation, 6, 0)


if __name__ == '__main__':
    unittest.main()
