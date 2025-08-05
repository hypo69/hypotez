**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use This Code Block
=========================================================================================

Description
-------------------------
This code block defines three functions (`log_time_async`, `log_time_yield`, and `log_time`) that measure the execution time of a given function. Each function takes a callable (the function to be timed) and keyword arguments as input.

Execution Steps
-------------------------
1. **Initialization:** The functions start by recording the current time using the `time()` function.
2. **Execution:**  The functions call the provided `method` with the given `kwargs`.
3. **Time Calculation:**  The functions calculate the elapsed time by subtracting the initial time from the current time.
4. **Result Formatting:** The functions format the elapsed time string in seconds with two decimal places.
5. **Return Value:**
    - **`log_time_async`:** The function returns a string containing the result of the method and the elapsed time. If the method doesn't return a result, it returns only the time.
    - **`log_time_yield`:** The function uses a generator to yield the results of the method, followed by the elapsed time.
    - **`log_time`:** The function returns a string containing the result of the method and the elapsed time. If the method doesn't return a result, it returns only the time.


Usage Example
-------------------------

```python
    async def my_async_function():
        # ... some asynchronous operation ...
        return 'My asynchronous result'

    def my_function():
        # ... some synchronous operation ...
        return 'My synchronous result'

    result = await log_time_async(my_async_function)
    print(f'Result: {result}')

    result = log_time(my_function)
    print(f'Result: {result}')

    for item in log_time_yield(my_function):
        print(f'Result: {item}')
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".