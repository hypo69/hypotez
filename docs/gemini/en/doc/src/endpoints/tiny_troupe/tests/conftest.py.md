# hypotez/src/endpoints/tiny_troupe/tests/conftest.py

## Overview

This module provides configuration and setup options for running pytest tests for the `tiny_troupe` endpoint. It includes functions for managing global testing options, such as refreshing the API cache, using the cache, and running test examples.

## Details

This file is used to configure the pytest framework for testing the functionality of the `tiny_troupe` endpoint. It provides a mechanism to control how tests are run based on specific command-line arguments. This helps ensure that tests can be run efficiently and with different configurations depending on the needs of the test scenario.

## Functions

### `pytest_addoption`

**Purpose**: This function defines command-line options that can be used to customize the pytest testing process. It allows users to control whether to refresh the API cache, use the cache, or run test examples.

**Parameters**:

- `parser`: A parser object provided by the `pytest` framework.

**Returns**: None.

**How the Function Works**:

- The function adds three command-line options to the pytest parser using `parser.addoption`:
    - `--refresh_cache`: Refreshes the API cache for the tests, ensuring the latest data is used.
    - `--use_cache`: Uses the API cache for the tests, reducing the number of actual API calls.
    - `--test_examples`: Reruns all examples to make sure they still work, potentially increasing test time.

**Examples**:

- To refresh the API cache before running tests, execute the following command:
    ```bash
    pytest --refresh_cache
    ```
- To use the API cache for the tests, execute the following command:
    ```bash
    pytest --use_cache
    ```
- To run all test examples, execute the following command:
    ```bash
    pytest --test_examples
    ```


### `pytest_generate_tests`

**Purpose**: This function processes global testing options set via command-line arguments and provides information about the current test case to the user.

**Parameters**:

- `metafunc`: A `Metafunc` object provided by the `pytest` framework, containing information about the current test function.

**Returns**: None.

**How the Function Works**:

- The function retrieves the values of the command-line options ( `--refresh_cache`, `--use_cache`, `--test_examples`) from the pytest configuration using `metafunc.config.getoption`.
- It then retrieves the name of the current test function using `metafunc.function.__name__` and prints information about the test case, including the name of the test, the values of the global testing options, and a separating line for better readability.

**Examples**:

- When a test function is being executed, this function will print information about the test case, including the values of the global testing options, to the console. For example:

    ```bash
    Test case: test_api_call
      - refresh_cache: False
      - use_cache: True
      - test_examples: False

    ```

## Parameter Details

- `refresh_cache`:  This option is used to control whether to refresh the API cache before running the tests. It allows for using the most recent data.
- `use_cache`: This option controls whether the tests should use the API cache to improve efficiency by reducing the number of actual API calls.
- `test_examples`: This option allows you to rerun all examples within the test suite to ensure they still function correctly. However, it can significantly increase test time.

## Examples
- Running tests without using cache or refreshing it
    ```bash
    pytest
    ```
- Running tests with cache enabled
    ```bash
    pytest --use_cache
    ```
- Running tests with cache disabled and examples enabled
    ```bash
    pytest --refresh_cache --test_examples
    ```