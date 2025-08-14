# # \file /src/utils/autodoc.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

""".. Module :: src.utils 
   : Platform: Windows, Unix
   : synopsis: DocString automatic update demonstration.

Description:
    The module contains the `Autodoc` decorator, which updates the line of functioning of the function with the addition of the last call of the function.
    The decorator is used in order to automatically update the Docstring function when calling it.

    The decorator wraps the function by updating its doCstring before calling, adding a line with the current time to it.
    To receive the current time, the `Time` library is used.

Example of use:
    An example of the `Example_Function` function, which uses the decorator` autodoc`. Each time it is called, its doCstring is updated, and information about the time of the last call of the function is added to it.
    
    Code example:
    `` `python
    @autodoc
    Def Example_function (Param1: Int, Param2: Str) -> None:
        "\" "An example of a function.
    
        Args:
            Param1 (int): first meaning.
            Param2 (str): second value.
        "\" "
        Print (F "Processing {param1} and {param2}")
    
    Example_function (1, "Test")
    Print (Example_function .__ Doc__) # conclusion of the updated docstring
    Example_function (2, "Another Test")
    Print (Example_function .__ Doc__) # conclusion of the updated docstring
    `` `"""



import functools
import time

def autodoc(func):
    """Decorator for automatic updating Docstring Functions."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Update doCstring before calling the function
        update_docstring(func)
        return func(*args, **kwargs)

    return wrapper

def update_docstring(func):
    """Updates Docstring function."""
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Checking whether there is a doCstring
    if func.__doc__:
        # Add information about the last call time
        func.__doc__ += f"\n\nLast called at: {current_time}"
    else:
        func.__doc__ = f"Last called at: {current_time}"

# An example of using the decorator
@autodoc
def example_function(param1: int, param2: str) -> None:
    """An example of a function.

    Args:
        Param1 (int): first meaning.
        Param2 (str): second value."""
    print(f"Processing {param1} and {param2}")

# Function testing
example_function(1, "test")
print(example_function.__doc__)  # Conclusion of updated doCstring
example_function(2, "another test")
print(example_function.__doc__)  # Conclusion of updated doCstring
