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
This code block initializes the command-line interface (CLI) for the GPT4Free API. It defines the parser for CLI arguments, parses the arguments provided by the user, sets the default value for the `gui` argument, and finally executes the API with the parsed arguments.

Execution Steps
-------------------------
1. Imports necessary modules, including `get_api_parser` and `run_api_args` from the `.cli` module.
2. Defines the parser using `get_api_parser()`.
3. Parses the command-line arguments using `parser.parse_args()`.
4. Sets the default value for the `gui` argument to `True` if it's not provided.
5. Executes the API with the parsed arguments using `run_api_args(args)`.

Usage Example
-------------------------

```python
from g4f.__main__ import run_api_args

# Example usage with GUI enabled
args = {'gui': True}
run_api_args(args)

# Example usage with GUI disabled
args = {'gui': False}
run_api_args(args)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".