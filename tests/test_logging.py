import pytest
from app.logging import setup_logging

def test_setup_logging():
    """Test that setup_logging runs without raising any exceptions."""
    try:
        setup_logging()
    except Exception as e:
        pytest.fail(f"setup_logging raised an exception: {e}")