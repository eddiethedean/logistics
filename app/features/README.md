# BDD Testing with Behave

This directory contains BDD (Behavior-Driven Development) feature files and step definitions using the `behave` package.

## Structure

- `*.feature` - Gherkin feature files describing the behavior
- `steps/` - Python step definition files that implement the behavior
- `behave.ini` - Behave configuration file

## Running Tests

To run the BDD tests:

1. Install dependencies:
   ```bash
   pip install -r requirements-bdd.txt
   ```

2. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

3. Run the behave tests:
   ```bash
   behave
   ```

## Current Features

- **Viewer sees map**: Tests the basic functionality of viewing a map in the LogCOP application

## Notes

- The step definitions use Selenium WebDriver for browser automation
- Chrome WebDriver is automatically managed via webdriver-manager
- Tests assume the Streamlit app is running on localhost:8501
- Map selectors may need to be updated based on the actual implementation
