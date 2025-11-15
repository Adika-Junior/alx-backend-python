# 0x03. Unittests and Integration Tests

This project focuses on unit testing and integration testing in Python using the `unittest` framework. It covers testing patterns such as mocking, parametrization, and fixtures.

## Learning Objectives

- Understand the difference between unit and integration tests
- Learn common testing patterns such as mocking, parametrizations, and fixtures
- Implement unit tests using `unittest.TestCase`
- Use `unittest.mock` for mocking external dependencies
- Parameterize tests using the `parameterized` library
- Create integration tests with fixtures

## Requirements

- Python 3.7
- All files must end with a new line
- All files must start with `#!/usr/bin/env python3`
- Code must follow `pycodestyle` style (version 2.5)
- All files must be executable
- All modules, classes, and functions must have documentation
- All functions and coroutines must be type-annotated

## Dependencies

- `unittest` - Built-in Python testing framework
- `unittest.mock` - Mocking library for testing
- `parameterized` - Library for parameterized tests

Install dependencies:
```bash
pip install parameterized
```

## Files

- `utils.py` - Utility functions for nested map access, JSON fetching, and memoization
- `client.py` - GitHub API client for fetching organization information
- `fixtures.py` - Test fixtures for integration testing
- `test_utils.py` - Unit tests for the utils module
- `test_client.py` - Unit tests and integration tests for the client module

## Running Tests

Run all tests:
```bash
python -m unittest discover
```

Run specific test file:
```bash
python -m unittest test_utils.py
python -m unittest test_client.py
```

Run specific test class:
```bash
python -m unittest test_utils.TestAccessNestedMap
python -m unittest test_client.TestGithubOrgClient
```

## Testing Patterns Covered

1. **Parameterized Tests** - Using `@parameterized.expand` to test multiple inputs
2. **Mocking** - Using `unittest.mock.patch` to mock external dependencies
3. **Property Mocking** - Using `PropertyMock` to mock properties
4. **Exception Testing** - Using `assertRaises` to test exception handling
5. **Integration Tests** - Testing code paths end-to-end with fixtures
6. **Memoization Testing** - Testing decorator behavior and caching

## Tasks

1. **Task 0-1**: Parameterize unit tests for `access_nested_map` including exception cases
2. **Task 2**: Mock HTTP calls for `get_json` function
3. **Task 3**: Test memoization decorator behavior
4. **Task 4-7**: Test `GithubOrgClient` methods with mocking and parametrization
5. **Task 8**: Integration test with fixtures

