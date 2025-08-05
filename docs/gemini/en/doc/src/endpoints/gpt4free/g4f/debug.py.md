# Module for Debugging and Logging in `hypotez`

## Overview

This module provides debugging and logging functionality for the `hypotez` project. It allows developers to track program execution, log errors, and provide useful information for troubleshooting and development purposes.

## Details

The module defines two key functions: `log` and `error`. These functions handle logging messages and errors, respectively. The module also includes several variables to control logging behavior and output.

- `logging` (bool): A boolean variable indicating whether logging is enabled or disabled.
- `version_check` (bool): A boolean variable used for version checks.
- `version` (Optional[str]): A variable to store the version information, if available.
- `log_handler` (Callable): A callable function used to handle logging output.
- `logs` (List[str]): A list to store logged messages for later retrieval.

## Functions

### `log`

**Purpose**: Logs a message if logging is enabled.

**Parameters**:

- `*text` (Any): One or more arguments representing the message to be logged.
- `file` (Optional[Any], optional): An optional file object where the message should be written. Defaults to `None`, which logs to standard output.

**Returns**:
- `None`: The function does not return a value.

**Raises Exceptions**:
- `None`: The function does not raise any exceptions.

**How the Function Works**:

- The function checks the `logging` variable to see if logging is enabled.
- If logging is enabled, the function calls the `log_handler` function with the provided arguments.
- The `log_handler` function is responsible for writing the log message to the desired destination.
- By default, the `log_handler` is set to `print`, which writes log messages to standard output.

**Examples**:

```python
log("This is a log message.")  # Writes the message to standard output if logging is enabled.
log("This is another log message.", file=open("log.txt", "w"))  # Writes the message to "log.txt" if logging is enabled.
```

### `error`

**Purpose**: Logs an error message to stderr.

**Parameters**:

- `*error` (Any): One or more arguments representing the error message(s).
- `name` (Optional[str], optional): An optional string representing the name of the error type. Defaults to `None`.

**Returns**:
- `None`: The function does not return a value.

**Raises Exceptions**:
- `None`: The function does not raise any exceptions.

**How the Function Works**:

- The function converts all error messages to strings.
- It formats the error messages by including the error type (if provided) and the error message itself.
- It calls the `log` function with the formatted error messages, which writes them to stderr.

**Examples**:

```python
error("An error occurred.")  # Logs the message to stderr.
error("A TypeError occurred.", type(TypeError))  # Logs "TypeError: A TypeError occurred." to stderr.
error("An error occurred during processing.", "ProcessingError")  # Logs "ProcessingError: An error occurred during processing." to stderr.
```

## Parameter Details

- `logging` (bool): Enables or disables logging. If set to `True`, all log messages will be printed.
- `version_check` (bool): Used for version checks.
- `version` (Optional[str]): Stores version information, if available.
- `log_handler` (Callable): Handles logging output. By default, it's set to `print`, which writes to standard output.
- `logs` (List[str]): Stores logged messages for later retrieval.

## Examples

```python
logging = True  # Enable logging
log("Starting the application.")

try:
    # Code that might raise an error
    raise ValueError("Something went wrong!")
except ValueError as ex:
    error(f"ValueError: {ex}")

log("Ending the application.")
```

This code demonstrates how to use the `log` and `error` functions to track application execution and log errors. The `logging` variable is set to `True` to enable logging. Messages are logged using the `log` function, and errors are logged using the `error` function. This helps developers understand the application's behavior and troubleshoot any issues that may arise.