**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the `autodoc` Decorator
=========================================================================================

Description
-------------------------
The `autodoc` decorator dynamically updates the docstring of a function by adding the time of its last call. This is useful for tracking when functions were last used.

Execution Steps
-------------------------
1. **Import `functools` and `time`**: These modules are required for the decorator and time handling.
2. **Define the `autodoc` decorator**:
    - The `autodoc` function takes a function as input and returns a wrapped version of it.
    - The `@functools.wraps` decorator ensures that the wrapped function retains the original function's metadata.
3. **Define the `wrapper` function**:
    - This is the function that gets executed when the decorated function is called.
    - It calls the `update_docstring` function to add the current time to the function's docstring.
    - Then, it calls the original function and returns its result.
4. **Define the `update_docstring` function**:
    - It retrieves the current time using `time.strftime`.
    - It checks if the function has a docstring and, if so, appends the current time to it. If not, it sets the docstring to the current time.
5. **Apply the `autodoc` decorator**:
    - The `@autodoc` decorator is applied to the `example_function` to automatically update its docstring on each call.

Usage Example
-------------------------

```python
from src.utils.autodoc import autodoc

@autodoc
def example_function(param1: int, param2: str) -> None:
    """Пример функции.

    Args:
        param1 (int): Первое значение.
        param2 (str): Второе значение.
    """
    print(f"Processing {param1} and {param2}")

# Call the function and print its docstring
example_function(1, "test")
print(example_function.__doc__)  # Output: Updated docstring with last call time
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".