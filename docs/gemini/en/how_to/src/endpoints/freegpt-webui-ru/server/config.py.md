**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:\n    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:\n

How to Use This Code Block
=========================================================================================

Description
-------------------------
This code defines a dictionary (`models`) containing various GPT models, and another dictionary (`special_instructions`) that provides custom instructions for each model.

Execution Steps
-------------------------
1. Defines a dictionary `models` with keys representing the GPT models and values as the model names.
2. Defines a dictionary `special_instructions` with keys representing the model names and values as lists of instructions for each model.
3. Each instruction within the `special_instructions` list is represented as a dictionary containing `role` (which is always 'user') and `content` (which is the specific instruction for the model).

Usage Example
-------------------------

```python
    # Access a list of models
    print(models)

    # Access instructions for a specific model
    print(special_instructions['gpt-dan-11.0'])

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".