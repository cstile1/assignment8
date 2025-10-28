# tests/e2e/test_e2e.py

import pytest  # Import the pytest framework for writing and running tests

# The following decorators and functions define E2E tests for the FastAPI calculator application.

from playwright.sync_api import expect

@pytest.mark.e2e
def test_hello_world(page, fastapi_server):
    page.goto("http://localhost:8000")
    expect(page.locator("h1")).to_have_text("Hello World")

@pytest.mark.e2e
def test_calculator_add(page, fastapi_server):
    page.goto("http://localhost:8000")
    page.fill("#a", "10")
    page.fill("#b", "5")
    page.click('button:text("Add")')
    page.wait_for_selector("#result", state="attached", timeout=3000)
    result_text = page.inner_text("#result")
    assert result_text == "Calculation Result: 15", f"Expected 'Calculation Result: 15', got '{result_text}'"

@pytest.mark.e2e
def test_calculator_divide_by_zero(page, fastapi_server):
    page.goto("http://localhost:8000")
    page.fill("#a", "10")
    page.fill("#b", "0")
    page.click('button:text("Divide")')

    # Wait for the error text to appear
    page.wait_for_function(
        """() => document.querySelector('#result') && document.querySelector('#result').innerText.includes('Cannot divide by zero')""",
        timeout=5000
    )

    result_text = page.inner_text("#result")
    assert result_text == "Error: Cannot divide by zero!", f"Expected 'Error: Cannot divide by zero!', got '{result_text}'"
