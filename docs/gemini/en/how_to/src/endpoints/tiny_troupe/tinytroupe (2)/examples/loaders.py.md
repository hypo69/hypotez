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
The code defines functions for loading and listing example agent and fragment specifications from JSON files.

Execution Steps
-------------------------
1. **`load_example_agent_specification(name:str)`:** This function reads an agent specification file from the `agents` directory based on the provided `name`. It uses `json.load` to parse the JSON content and returns the parsed dictionary.
2. **`load_example_fragment_specification(name:str)`:** This function reads a fragment specification file from the `fragments` directory based on the provided `name`. It uses `json.load` to parse the JSON content and returns the parsed dictionary.
3. **`list_example_agents()`:** This function retrieves a list of available example agents by listing files in the `agents` directory and extracting the file names without the extension.
4. **`list_example_fragments()`:** This function retrieves a list of available example fragments by listing files in the `fragments` directory and extracting the file names without the extension.

Usage Example
-------------------------

```python
    # Load an example agent specification
    agent_spec = load_example_agent_specification('example_agent')

    # Load an example fragment specification
    fragment_spec = load_example_fragment_specification('example_fragment')

    # List available example agents
    agents = list_example_agents()

    # List available example fragments
    fragments = list_example_fragments()
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".