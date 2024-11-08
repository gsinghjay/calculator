"""Factory module for creating operation instances."""
import logging
from typing import Optional
from app.template_operation import (
    TemplateOperation,
    Addition,
    Subtraction,
    Multiplication,
    Division
)

class OperationFactory:
    """
    Factory class to create instances of operations based on the operation type.
    Implements the Factory Pattern.
    """
    @staticmethod
    def create_operation(operation: Optional[str]) -> Optional[TemplateOperation]:
        """
        Returns an instance of the appropriate Operation subclass based on the operation string.
        
        Parameters:
        - operation (Optional[str]): The operation name (e.g., 'add', 'subtract')
        
        Returns:
        - TemplateOperation: Instance of the appropriate operation class
        - None: If operation is not found or invalid
        """
        logging.debug(f"Creating operation for: {operation}")
        
        if not isinstance(operation, str):
            logging.debug(f"Invalid operation type: {type(operation)}")
            return None
            
        # Dictionary mapping operation names to their corresponding class instances
        operations_map = {
            "add": Addition(),
            "subtract": Subtraction(),
            "multiply": Multiplication(),
            "divide": Division(),
        }
        
        result = operations_map.get(operation.lower())
        if result:
            logging.debug(f"Operation '{operation}' created successfully.")
        else:
            logging.debug(f"Operation '{operation}' not found in operations_map.")
        return result