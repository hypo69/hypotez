# Module for Automatic Documentation Update
## Overview
This module provides the `autodoc` decorator, which automatically updates the documentation string (`docstring`) of a function by adding the time of the last function call. This allows you to keep track of when a function was last executed. The decorator wraps the function, updating its docstring before each call, thus ensuring that the documentation is up-to-date.

## Details
The `autodoc` decorator works by modifying the function's docstring before it's called. The decorator calls the `update_docstring` function to add the current timestamp to the docstring. The `time` library is used to get the current time. The module also provides an example of how to use the `autodoc` decorator with the `example_function`.

## Classes
### `autodoc`
**Description**:  This decorator automatically updates the docstring of a function with the time of its last call. 

**Inherits**:  `functools.wraps`

**Methods**:
- `wrapper(*args, **kwargs)`: Calls the function and updates its docstring before execution.

## Functions
### `autodoc(func)`
**Purpose**: This decorator automatically updates the docstring of a function by adding the time of its last call.

**Parameters**:
- `func`: The function whose docstring will be updated.

**Returns**: 
- `wrapper`: A wrapper function that updates the docstring and then calls the original function.

**Examples**:
```python
@autodoc
def example_function(param1: int, param2: str) -> None:
    """Пример функции.
    Args:
        param1 (int): Первое значение.
        param2 (str): Второе значение.
    """
    print(f"Processing {param1} and {param2}")

example_function(1, "test")
print(example_function.__doc__)
```

**How the Function Works**:
- The `autodoc` decorator calls the `update_docstring` function to add the current timestamp to the function's docstring before executing the wrapped function.

### `update_docstring(func)`
**Purpose**:  Updates the function's docstring by adding the current timestamp.

**Parameters**:
- `func`: The function whose docstring will be updated.

**Returns**:
- `None`

**Examples**:
```python
@autodoc
def example_function(param1: int, param2: str) -> None:
    """Пример функции.
    Args:
        param1 (int): Первое значение.
        param2 (str): Второе значение.
    """
    print(f"Processing {param1} and {param2}")

example_function(1, "test")
print(example_function.__doc__)
```

**How the Function Works**:
- The `update_docstring` function gets the current time using `time.strftime("%Y-%m-%d %H:%M:%S")`. 
- Then it checks if the function already has a docstring. 
- If it does, it appends the current timestamp to the existing docstring. 
- Otherwise, it sets the docstring to the current timestamp. 
- This ensures that the docstring is always updated with the time of the last call.

### `example_function(param1: int, param2: str) -> None`
**Purpose**: This is an example function that demonstrates the use of the `autodoc` decorator. 

**Parameters**:
- `param1 (int)`: The first value.
- `param2 (str)`: The second value.

**Returns**: 
- `None`

**Examples**:
```python
@autodoc
def example_function(param1: int, param2: str) -> None:
    """Пример функции.
    Args:
        param1 (int): Первое значение.
        param2 (str): Второе значение.
    """
    print(f"Processing {param1} and {param2}")

example_function(1, "test")
print(example_function.__doc__)  # Output: "Пример функции.\n\nLast called at: YYYY-MM-DD HH:MM:SS"
```

**How the Function Works**:
- The `example_function` prints the values of `param1` and `param2` to the console. 
- When called, the `autodoc` decorator updates its docstring by adding the current timestamp. 
- The output of the updated docstring will include the current time. 
- This provides a clear timestamp of when the function was last executed.