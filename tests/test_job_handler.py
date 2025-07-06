import pytest
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.job_handler import *

# Test the math handler
def test_handle_add(capsys):
    payload = {"a": 5, "b": 3,"c": 6,"d": 9}
    handle_add(payload)

    # Capture stdout
    captured = capsys.readouterr()
    assert "➕ 5 + 3 + 6 + 9 = 23" in captured.out

# Test the math handler
def test_handle_add_zero(capsys):
    payload = {"a": 5}
    handle_add(payload)

    # Capture stdout
    captured = capsys.readouterr()
    assert "➕ 5 + 0 = 5" in captured.out

# Test the print_message handler
def test_handle_print_message(capsys):
    payload = {"message": "Hello, test!"}
    handle_print_message(payload)

    captured = capsys.readouterr()
    assert "📝 Hello, test!" in captured.out

# Test the reverse string handler
def test_handle_reverse_string(capsys):
    payload = {"text": "Meta"}
    handle_reverse_string(payload)

    captured = capsys.readouterr()
    assert "🔁 Meta → ateM" in captured.out

# Test the handler dispatcher
def test_get_handler_valid():
    assert get_handler("add") == handle_add
    assert get_handler("print_message") == handle_print_message
    assert get_handler("reverse_string") == handle_reverse_string

def test_get_handler_invalid():
    assert get_handler("nonexistent") is None

