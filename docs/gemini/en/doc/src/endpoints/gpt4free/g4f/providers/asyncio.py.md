# Asyncio Provider for gpt4free
## Overview
This module provides asynchronous utilities for interacting with the gpt4free API. It simplifies the handling of asynchronous operations and ensures compatibility with various event loop implementations.

## Details
The module leverages `asyncio` for asynchronous processing and utilizes libraries like `nest_asyncio` and `uvloop` for enhanced performance and compatibility with different event loop environments. The module aims to make it easier to work with gpt4free's asynchronous API by providing a set of utility functions and classes designed to streamline common operations.

## Functions
### `get_running_loop`
**Purpose**: Retrieves the currently running event loop, optionally patching it for nested event loop scenarios.

**Parameters**:
- `check_nested` (bool): If `True`, raises an exception if the loop is not patched for nested event loops. Defaults to `True`.

**Returns**:
- `Optional[AbstractEventLoop]`: The running event loop or `None` if no loop is running.

**Raises Exceptions**:
- `NestAsyncioError`: If `check_nested` is `True` and the loop is not patched for nested event loops.

**How the Function Works**:
1.  The function attempts to retrieve the running event loop using `asyncio.get_running_loop()`.
2.  If the loop is a `uvloop.Loop`, it's returned directly without patching.
3.  If the loop doesn't have a `_nest_patched` attribute, indicating that it's not patched for nested event loops, the function applies `nest_asyncio.apply()` if `has_nest_asyncio` is `True`.
4.  If `check_nested` is `True` and the loop is not patched, a `NestAsyncioError` is raised, prompting users to install the `nest_asyncio` package.
5.  The patched or unpatched loop is returned.

**Examples**:
```python
# Example 1: Get the running loop and patch if necessary
loop = get_running_loop()  # Returns the running loop

# Example 2: Raise an exception if the loop is not patched
loop = get_running_loop(check_nested=True)
```

### `await_callback`
**Purpose**: Awaits the execution of a given callback function.

**Parameters**:
- `callback` (Callable): The callback function to be executed.

**Returns**:
- The result of the callback function execution.

**How the Function Works**:
- The function simply awaits the execution of the provided callback function using `await callback()`.

**Examples**:
```python
async def my_callback():
    return "Hello, World!"

result = await await_callback(my_callback)  # result will be "Hello, World!"
```

### `async_generator_to_list`
**Purpose**: Converts an asynchronous generator to a list.

**Parameters**:
- `generator` (AsyncIterator): The asynchronous generator to be converted.

**Returns**:
- `list`: A list containing the items yielded by the asynchronous generator.

**How the Function Works**:
- The function uses an asynchronous comprehension to iterate over the asynchronous generator and collect the yielded items into a list.

**Examples**:
```python
async def my_async_generator():
    for i in range(5):
        yield i

my_list = await async_generator_to_list(my_async_generator())  # my_list will be [0, 1, 2, 3, 4]
```

### `to_sync_generator`
**Purpose**: Converts an asynchronous generator to a synchronous generator.

**Parameters**:
- `generator` (AsyncIterator): The asynchronous generator to be converted.
- `stream` (bool): If `True`, the generator will yield items one by one; otherwise, it will yield a list of all items. Defaults to `True`.

**Returns**:
- `Iterator`: A synchronous generator yielding items from the asynchronous generator.

**How the Function Works**:
1.  The function retrieves the running event loop using `get_running_loop()` and checks if it's a `uvloop.Loop`.
2.  If `stream` is `False`, it directly runs the asynchronous generator to list conversion and yields the list.
3.  If `stream` is `True`, the function creates a new event loop if necessary, iterates over the asynchronous generator using the loop's `run_until_complete()` method, and yields each item.
4.  After iterating, the function closes the loop and handles any exceptions gracefully.

**Examples**:
```python
# Example 1: Convert async generator to synchronous generator (stream mode)
async def my_async_generator():
    for i in range(5):
        yield i

for item in to_sync_generator(my_async_generator()):
    print(item)  # Prints 0, 1, 2, 3, 4

# Example 2: Convert async generator to synchronous generator (list mode)
for item in to_sync_generator(my_async_generator(), stream=False):
    print(item)  # Prints [0, 1, 2, 3, 4]
```

### `to_async_iterator`
**Purpose**: Converts a synchronous iterator or coroutine to an asynchronous iterator.

**Parameters**:
- `iterator`: The synchronous iterator or coroutine to be converted.

**Returns**:
- `AsyncIterator`: An asynchronous iterator yielding items from the input iterator.

**How the Function Works**:
- The function checks if the input `iterator` has an `__aiter__` method, indicating that it's already an asynchronous iterator, and yields items directly.
- If the input `iterator` is a coroutine, it awaits its execution and yields the result.
- For other types of iterators, the function iterates over them synchronously and yields each item.

**Examples**:
```python
# Example 1: Convert a list to an async iterator
my_list = [1, 2, 3]
async for item in to_async_iterator(my_list):
    print(item)  # Prints 1, 2, 3

# Example 2: Convert a coroutine to an async iterator
async def my_coroutine():
    return "Hello, World!"

async for item in to_async_iterator(my_coroutine()):
    print(item)  # Prints "Hello, World!"
```