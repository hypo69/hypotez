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
The `spinning_cursor()` function generates a sequence of symbols `| / - \\` to create a spinning cursor animation in the console. The `show_spinner()` function utilizes the `spinning_cursor()` generator to display the spinning cursor for a specified duration with a customizable delay between each symbol change.

Execution Steps
-------------------------
1. **`spinning_cursor()`:**
   - The function continuously loops, iterating through the `| / - \\` symbols.
   - For each symbol, it yields the current symbol, effectively returning the symbol to the caller. 

2. **`show_spinner()`:**
   - It initializes a `spinning_cursor()` generator to handle the cursor animation.
   - It calculates the end time based on the provided `duration`.
   - It enters a loop that runs until the current time reaches the `end_time`.
   - Inside the loop, it:
     - Prints the next symbol from the `spinner` generator.
     - Flushes the output to the console immediately using `sys.stdout.flush()`.
     - Pauses for the specified `delay` using `time.sleep()`.
     - Moves the cursor back one position using `sys.stdout.write('\b')` to overwrite the previous symbol. 

Usage Example
-------------------------

```python
    # Example usage of the spinner in a script
    print("Spinner for 5 seconds:")
    show_spinner(duration=5.0, delay=0.1)
    print("\nDone!")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".