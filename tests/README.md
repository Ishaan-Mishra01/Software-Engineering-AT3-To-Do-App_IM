# To-Do App Test Suite

This directory contains comprehensive tests for the To-Do application.

## Test Structure

- **test_unit.py** - Unit tests for individual functions
- **test_integration.py** - Integration tests for API endpoints
- **test_frontend.py** - Frontend rendering and static file tests
- **test_security.py** - Security vulnerability tests
- **test_performance.py** - Performance and scalability tests
- **test_app.py** - Original API functionality tests
- **test_ui.html** - Manual UI testing interface
- **TEST_RESULTS.md** - Test results documentation

## Running Tests

### Run All Tests
```bash
python3 run_tests.py
```

### Run Individual Test Suites
```bash
# Unit tests only
python3 -m unittest tests.test_unit

# Integration tests only
python3 -m unittest tests.test_integration

# Frontend tests only
python3 -m unittest tests.test_frontend

# Security tests only
python3 -m unittest tests.test_security

# Performance tests only
python3 -m unittest tests.test_performance

# API tests only
python3 tests/test_app.py
```

## Test Coverage

### Unit Tests (test_unit.py)
- Data loading and saving functions
- Empty file handling
- Session management
- Data validation

### Integration Tests (test_integration.py)
- Complete user registration flow
- Login with correct/incorrect credentials
- Full task CRUD operations
- Multi-user isolation
- Authentication requirements

### Frontend Tests (test_frontend.py)
- HTML element rendering
- CSS file content and styles
- JavaScript functionality
- Form validation attributes
- Responsive design elements
- Static file serving

### Security Tests (test_security.py)
- Session security
- SQL injection protection
- XSS protection
- Authentication enforcement
- Password exposure prevention
- Directory traversal protection

### Performance Tests (test_performance.py)
- Page load times
- Multiple task handling
- Concurrent user simulation
- Static file caching
- Data file growth
- Memory stability

## Prerequisites

1. Install dependencies:
```bash
pip3 install -r requirements.txt
pip3 install requests  # For API tests
```

2. Ensure Flask server can run on port 5001

## Test Results

The test runner provides:
- Coloured output for easy reading
- Individual test results
- Suite summaries
- Overall pass/fail status
- Execution time metrics

## Adding New Tests

To add new tests:

1. Create a new test file in the tests directory
2. Follow the naming convention: `test_*.py`
3. Import unittest and inherit from `unittest.TestCase`
4. Add the test module to `run_tests.py`

Example:
```python
import unittest

class TestNewFeature(unittest.TestCase):
    def test_something(self):
        self.assertTrue(True)
```

## Continuous Integration

The test suite can be integrated with CI/CD pipelines:
- Exit code 0 on all tests passing
- Exit code 1 on any test failure
- Detailed output for debugging