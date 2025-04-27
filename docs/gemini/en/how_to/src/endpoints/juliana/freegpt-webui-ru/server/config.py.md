**Instructions for Generating Code Documentation**

1. **Analyze the Code**: This code defines a dictionary called `special_instructions` which contains key-value pairs. Each key represents a specific instruction mode for a language model, and the corresponding value is a list of instructions.

2. **Create a Step-by-Step Guide**:

    - **Description**: This code block defines a dictionary called `special_instructions` containing instructions for different language model modes.
    - **Execution Steps**:
        1. The code creates a dictionary called `special_instructions`.
        2. It defines several keys, each representing a specific instruction mode: `default`, `gpt-dan-11.0`, `gpt-dan-2.0`, `gpt-evil`, `gpt-dev-2.0`, `programming-assistant`, `editor`, `midjourney-promt`, and `sd-promt`.
        3. For each key, the code assigns a list of instructions as the value.
        4. Each instruction is a dictionary with a `role` and a `content` key.
        5. The `content` key holds the actual instruction text for the specific mode.

    - **Usage Example**:
    ```python
    # Accessing a specific mode's instructions
    dan_11_instructions = special_instructions['gpt-dan-11.0']

    # Printing the first instruction for the DAN 11.0 mode
    print(dan_11_instructions[0]['content'])
    ```

3. **Example**:

How to Use This Code Block
=========================================================================================

Description
-------------------------
This code block defines a dictionary called `special_instructions` which contains instructions for different language model modes. Each key represents a specific instruction mode for a language model, and the corresponding value is a list of instructions.

Execution Steps
-------------------------
1. The code creates a dictionary called `special_instructions`.
2. It defines several keys, each representing a specific instruction mode: `default`, `gpt-dan-11.0`, `gpt-dan-2.0`, `gpt-evil`, `gpt-dev-2.0`, `programming-assistant`, `editor`, `midjourney-promt`, and `sd-promt`.
3. For each key, the code assigns a list of instructions as the value.
4. Each instruction is a dictionary with a `role` and a `content` key.
5. The `content` key holds the actual instruction text for the specific mode.

Usage Example
-------------------------

```python
    # Accessing a specific mode's instructions
    dan_11_instructions = special_instructions['gpt-dan-11.0']

    # Printing the first instruction for the DAN 11.0 mode
    print(dan_11_instructions[0]['content'])
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".