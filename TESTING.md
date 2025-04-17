# Testing Guide

This document provides guidelines for running and writing tests for the Personal Dashboard application.

## Running Tests

### Running All Tests

To run all tests in the project:

```bash
python manage.py test
```

### Running Tests for a Specific App

To run tests for a specific app (e.g., tasks):

```bash
python manage.py test tasks
```

### Running a Specific Test Class

To run a specific test class:

```bash
python manage.py test tasks.tests.TaskModelTest
```

### Running a Specific Test Method

To run a specific test method:

```bash
python manage.py test tasks.tests.TaskModelTest.test_task_creation
```

## Test Coverage

To check test coverage, you'll need to install coverage:

```bash
pip install coverage
```

Then run:

```bash
coverage run --source='.' manage.py test
coverage report
```

For a more detailed HTML report:

```bash
coverage html
```

Then open `htmlcov/index.html` in your browser.

## Test Structure

The project follows the standard Django testing approach:

1. **Models**: Test data integrity, validations, and method behavior
2. **Forms**: Test form validation with both valid and invalid data
3. **Views**: Test HTTP responses, template rendering, and view logic
4. **Integration**: Test interactions between different components

## Writing Tests

When writing new tests, follow these guidelines:

1. Create a new test class for each model, form, or view
2. Use descriptive method names that explain what is being tested
3. Include docstrings to document test purpose
4. Set up test data in the `setUp` method
5. Test both expected behavior and edge cases
6. Verify that errors are raised when expected

### Example Test Structure

```python
class ExampleModelTest(TestCase):
    def setUp(self):
        # Set up test data
        self.user = User.objects.create_user(...)
        
    def test_expected_behavior(self):
        """Test that the model behaves as expected under normal conditions"""
        # Test code here
        
    def test_edge_case(self):
        """Test behavior in edge cases"""
        # Test code here
```

## Test Best Practices

1. Keep tests simple and focused on a single behavior
2. Use descriptive assertions to make failure messages clear
3. Don't test third-party code or the framework itself
4. Test both positive scenarios (things working correctly) and negative scenarios (error handling)
5. Maintain test independence (tests should not depend on each other)
6. Use factories or fixtures for complex test data setup
7. Clean up after tests if they create files or external resources