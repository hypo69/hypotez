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
This code block defines a function `_create_completion` that interacts with the You.com API to generate text completions.

Execution Steps
-------------------------
1. **Imports Required Modules**: Imports necessary libraries like `os`, `json`, `time`, `subprocess`, and type hints.
2. **Defines API Details**: Sets the base URL (`url`) for the You.com API and the desired model (`model`) for text generation.
3. **Defines Function `_create_completion`**:
    - Takes the `model`, `messages`, and `stream` parameters.
    - Retrieves the path to the `you.py` helper script located within the current directory.
    - Creates a configuration dictionary (`config`) that includes the user messages.
    - Constructs a command (`cmd`) to execute the `you.py` script with the `config` as an argument.
    - Spawns a subprocess (`p`) to execute the command and captures both standard output and error streams.
    - Iterates through each line of output from the subprocess, decodes it to UTF-8, and yields the decoded line as a string.

Usage Example
-------------------------

```python
    messages = [
        {'role': 'user', 'content': 'Hello, world!'},
    ]
    completion = _create_completion(model='gpt-3.5-turbo', messages=messages, stream=True)
    for line in completion:
        print(line, end='')
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".