# Module for Measuring Execution Time
## Overview

This module provides functions for measuring the execution time of various methods. It offers three distinct functions: `log_time_async`, `log_time_yield`, and `log_time`, each tailored for different scenarios.

## Details

This module is used within the `hypotez` project to track and log the execution time of functions or methods. It provides a convenient way to understand how long different parts of the code take to execute, aiding in performance analysis and optimization.

## Functions

### `log_time_async`

**Purpose**: This function measures the execution time of asynchronous methods (methods marked with `async`).

**Parameters**:

- `method` (`callable`): The asynchronous method whose execution time needs to be measured.
- `**kwargs` (`dict`):  Additional keyword arguments to be passed to the asynchronous method.

**Returns**:

- `str`: A string containing the result of the asynchronous method execution (if any) followed by the execution time in seconds (e.g., "Result 1.23 secs" or "1.23 secs").

**Raises Exceptions**:

- `Exception`: If an error occurs during the execution of the asynchronous method.

**How the Function Works**:

1. Records the start time using the `time()` function.
2. Executes the asynchronous method using `await`.
3. Calculates the elapsed time in seconds.
4. Formats the result string based on whether the method returned a value or not.

**Examples**:

```python
from hypotez.src.endpoints.gpt4free.etc.testing.log_time import log_time_async

async def my_async_method(param1: str, param2: int) -> str:
    # ... (Asynchronous operation)
    return f"Result: {param1} {param2}"

result = await log_time_async(my_async_method, param1="Hello", param2=10)
print(result) # Output: "Result: Hello 10 1.23 secs"
```

### `log_time_yield`

**Purpose**: This function measures the execution time of generator methods (methods using `yield`).

**Parameters**:

- `method` (`callable`): The generator method whose execution time needs to be measured.
- `**kwargs` (`dict`):  Additional keyword arguments to be passed to the generator method.

**Returns**:

- `Generator`: A generator that yields the results of the generator method followed by the execution time in seconds.

**Raises Exceptions**:

- `Exception`: If an error occurs during the execution of the generator method.

**How the Function Works**:

1. Records the start time using the `time()` function.
2. Executes the generator method using `yield from`.
3. Calculates the elapsed time in seconds.
4. Yields the results of the generator method and then yields the execution time.

**Examples**:

```python
from hypotez.src.endpoints.gpt4free.etc.testing.log_time import log_time_yield

def my_generator_method(param1: str, param2: int) -> Generator[str, None, None]:
    # ... (Generator operations)
    yield f"Result: {param1} {param2}"

for result in log_time_yield(my_generator_method, param1="Hello", param2=10):
    print(result) # Output: "Result: Hello 10 1.23 secs"
```

### `log_time`

**Purpose**: This function measures the execution time of standard (non-asynchronous or generator) methods.

**Parameters**:

- `method` (`callable`): The method whose execution time needs to be measured.
- `**kwargs` (`dict`):  Additional keyword arguments to be passed to the method.

**Returns**:

- `str`: A string containing the result of the method execution (if any) followed by the execution time in seconds (e.g., "Result 1.23 secs" or "1.23 secs").

**Raises Exceptions**:

- `Exception`: If an error occurs during the execution of the method.

**How the Function Works**:

1. Records the start time using the `time()` function.
2. Executes the method.
3. Calculates the elapsed time in seconds.
4. Formats the result string based on whether the method returned a value or not.

**Examples**:

```python
from hypotez.src.endpoints.gpt4free.etc.testing.log_time import log_time

def my_method(param1: str, param2: int) -> str:
    # ... (Method operations)
    return f"Result: {param1} {param2}"

result = log_time(my_method, param1="Hello", param2=10)
print(result) # Output: "Result: Hello 10 1.23 secs"
```

## Parameter Details

- `method` (`callable`): The method to be timed. This can be any function or method.
- `**kwargs` (`dict`):  Additional keyword arguments to be passed to the method.

## Examples

```python
# Example using log_time_async
async def my_async_function(param1: str, param2: int) -> str:
    return f"Result: {param1} {param2}"

result = await log_time_async(my_async_function, param1="Hello", param2=10)
print(result)

# Example using log_time_yield
def my_generator_function(param1: str, param2: int) -> Generator[str, None, None]:
    yield f"Result: {param1} {param2}"

for result in log_time_yield(my_generator_function, param1="Hello", param2=10):
    print(result)

# Example using log_time
def my_function(param1: str, param2: int) -> str:
    return f"Result: {param1} {param2}"

result = log_time(my_function, param1="Hello", param2=10)
print(result)
```