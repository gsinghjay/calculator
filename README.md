# Ultimate Guide to OOP Design Patterns: Building a Calculator with Logging and Debugging

![Python Versions](https://img.shields.io/badge/python-3.8%2C%203.9%2C%203.10-blue)
![Build Status](https://github.com/gsinghjay/calculator/actions/workflows/tests.yml/badge.svg)
![License](https://img.shields.io/github/license/gsinghjay/calculator)
![Coverage Status](https://img.shields.io/coveralls/github/gsinghjay/calculator)
![GitHub Last Commit](https://img.shields.io/github/last-commit/gsinghjay/calculator)

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Architecture](#architecture)
   - [Design Patterns Implemented](#design-patterns-implemented)
4. [Setup and Installation](#setup-and-installation)
5. [Usage](#usage)
6. [Logging and Debugging](#logging-and-debugging)
7. [Testing](#testing)
8. [Contributing](#contributing)
9. [License](#license)
10. [Acknowledgements](#acknowledgements)

---

## Introduction

Welcome to the **Ultimate Guide to OOP Design Patterns**, where we build a fully functional calculator in Python. This project demonstrates several key Object-Oriented Programming (OOP) design patterns, including:

- **Command Pattern**
- **Template Method Pattern**
- **Factory Pattern**
- **Observer Pattern**
- **Singleton Pattern**
- **Strategy Pattern**

Additionally, we've incorporated comprehensive logging and debugging techniques to ensure effective tracking and troubleshooting of the application's behavior.

This guide is tailored for students and developers aiming to deepen their understanding of OOP design patterns through practical implementation.

---

## Features

- **Modular Design:** Organized codebase with clear separation of concerns.
- **Design Patterns:** Implementation of multiple OOP design patterns for scalable and maintainable code.
- **Observer Support:** Tracks calculation history with observer notifications.
- **Interactive REPL:** User-friendly command-line interface for performing calculations.
- **Logging:** Detailed logging for monitoring and debugging.
- **Unit Testing:** Comprehensive test suite ensuring code reliability.
- **Continuous Integration:** Automated testing using GitHub Actions.

---

## Architecture

The calculator application is structured into several modules, each responsible for specific functionality:

```
├── app
│   ├── calculator
│   │   └── __init__.py
│   ├── logging
│   │   └── __init__.py
│   ├── operations
│   │   └── __init__.py
│   ├── observer
│   │   └── __init__.py
│   └── template_operation
│       └── __init__.py
├── tests
│   ├── conftest.py
│   ├── test_calculator.py
│   ├── test_logging.py
│   ├── test_observer.py
│   └── test_operations.py
├── .coveragerc
├── .gitignore
├── .github
│   └── workflows
│       └── tests.yml
├── pytest.ini
├── requirements.txt
└── README.md
```

### Design Patterns Implemented

#### 1. **Factory Pattern**

- **Purpose:** To create objects without specifying the exact class of the object to be created.
- **Implementation:** Located in `app/calculator/__init__.py`, the `OperationFactory` class maps operation names to their corresponding classes.

```python:app/calculator/__init__.py
class OperationFactory:
    @staticmethod
    def create_operation(operation: str) -> TemplateOperation:
        operations_map = {
            "add": Addition(),
            "subtract": Subtraction(),
            "multiply": Multiplication(),
            "divide": Division(),
        }
        return operations_map.get(operation.lower())
```

#### 2. **Observer Pattern**

- **Purpose:** To allow an object (subject) to notify other objects (observers) about changes in its state.
- **Implementation:** Defined in `app/observer/__init__.py`, the `HistoryObserver` and `CalculatorWithObserver` classes manage observer subscriptions and notifications.

```python:app/observer/__init__.py
class HistoryObserver:
    def update(self, calculation):
        logging.info(f"Observer: New calculation added -> {calculation}")

class CalculatorWithObserver:
    def __init__(self):
        self._history: List = []
        self._observers: List[HistoryObserver] = []

    def add_observer(self, observer: HistoryObserver):
        self._observers.append(observer)

    def notify_observers(self, calculation):
        for observer in self._observers:
            observer.update(calculation)
```

#### 3. **Template Method Pattern**

- **Purpose:** Defines the skeleton of an algorithm in a method, deferring some steps to subclasses.
- **Implementation:** Located in `app/template_operation/__init__.py`, the `TemplateOperation` abstract base class outlines the steps for performing operations.

```python:app/template_operation/__init__.py
class TemplateOperation(ABC):
    def calculate(self, a: float, b: float) -> float:
        self.validate_inputs(a, b)
        result = self.execute(a, b)
        self.log_result(a, b, result)
        return result

    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        pass
```

#### 4. **Singleton Pattern**

- **Purpose:** Ensures a class has only one instance and provides a global point of access to it.
- **Implementation:** Present in `app/calculator/__init__.py`, the `SingletonCalculator` class restricts instantiation to a single object.

```python:app/calculator/__init__.py
class SingletonCalculator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonCalculator, cls).__new__(cls)
            cls._history = []
        return cls._instance
```

#### 5. **Strategy Pattern**

- **Purpose:** Enables selecting an algorithm's behavior at runtime.
- **Implementation:** Implemented through the `Calculation` dataclass in `app/template_operation/__init__.py`, which holds a reference to a `TemplateOperation`.

```python:app/template_operation/__init__.py
@dataclass
class Calculation:
    operation: TemplateOperation
    operand1: float
    operand2: float

    def __str__(self) -> str:
        result = self.operation.calculate(self.operand1, self.operand2)
        return f"{self.operand1} {self.operation.__class__.__name__.lower()} {self.operand2} = {result}"
```

---

## Setup and Installation

### Prerequisites

- **Python 3.8 or higher**

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Setup Environment Variables**

   Create a `.env` file in the root directory and specify the following variables:

   ```
   LOG_FILENAME=calculator.log
   LOG_LEVEL=DEBUG
   LOG_FORMAT=%(asctime)s - %(levelname)s - %(message)s
   ```

---

## Usage

### Running the Calculator

Execute the main program using:

```bash
python app/main.py
```

### Interactive Commands

Once the calculator is running, you can use the following commands:

- **add \<num1> \<num2>**: Add two numbers.
- **subtract \<num1> \<num2>**: Subtract the second number from the first.
- **multiply \<num1> \<num2>**: Multiply two numbers.
- **divide \<num1> \<num2>**: Divide the first number by the second.
- **list**: Display calculation history.
- **clear**: Clear the calculation history.
- **help**: Show available commands.
- **exit**: Exit the calculator.

#### Example Session

```bash
Welcome to the OOP Calculator! Type 'help' for available commands.
Enter an operation and two numbers, or a command: add 10 5
Result: 15.0
Enter an operation and two numbers, or a command: multiply 3 4
Result: 12.0
Enter an operation and two numbers, or a command: list
10.0 addition 5.0 = 15.0
3.0 multiplication 4.0 = 12.0
Enter an operation and two numbers, or a command: exit
Exiting calculator...
```

---

## Logging and Debugging

### Logging

Logging is configured in `app/logging/__init__.py` using Python's built-in `logging` module. Logs are stored in the file specified by the `LOG_FILENAME` environment variable (default is `calculator.log`).

**Key Features:**

- **Debugging Information:** Detailed logs for tracking the flow of execution.
- **Error Logging:** Captures and logs errors for troubleshooting.
- **Info Logs:** Records significant events like operation executions and observer notifications.

```python:app/logging/__init__.py
def setup_logging():
    ...
    logging.basicConfig(
        filename=log_filename,
        level=log_level,
        format=log_format
    )
```

### Debugging

The application uses Python's `pdb` module for debugging. Breakpoints can be set in the code to inspect variables and the execution flow.

**Example:**

```python:app/calculator/__init__.py
def get_history(self):
    import pdb; pdb.set_trace()
    return self._history
```

---

## Testing

### Running Tests

Tests are written using `pytest` and can be executed with the following command:

```bash
pytest
```

### Test Coverage

To generate a coverage report, run:

```bash
pytest --cov=app
```

### Continuous Integration

GitHub Actions are set up to run tests automatically on every push or pull request to the `main` branch. Configuration can be found in `.github/workflows/tests.yml`.

```yaml:.github/workflows/tests.yml
name: Run Tests on Push or Pull Request to Main

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    ...
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add your feature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

Please ensure your code follows the project's coding standards and includes appropriate tests and documentation.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgements

- **Python Documentation:** [https://docs.python.org/3/](https://docs.python.org/3/)
- **Refactoring Guru:** [https://refactoring.guru/design-patterns/python](https://refactoring.guru/design-patterns/python)
- **Pytest Documentation:** [https://docs.pytest.org/](https://docs.pytest.org/)
- **GitHub Actions Documentation:** [https://docs.github.com/actions](https://docs.github.com/actions)

---