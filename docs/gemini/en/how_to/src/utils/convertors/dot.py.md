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
The `dot2png()` function converts a DOT file (a text-based graph description format) into a PNG image using the Graphviz library. 

Execution Steps
-------------------------
1. **Reads the DOT File**: The function opens the specified DOT file and reads its contents.
2. **Creates a Source Object**: The read DOT content is used to create a `Source` object from the `graphviz` library. This object represents the graph defined in the DOT file.
3. **Renders the Source to a PNG File**: The `Source` object's format is set to 'png', and then it's rendered into a PNG file at the specified path. The `cleanup` parameter is set to `True` to remove temporary files created during the rendering process.
4. **Handles Exceptions**: The code includes `try...except` blocks to handle potential errors, such as `FileNotFoundError` (if the DOT file doesn't exist) and general exceptions (`Exception`) during conversion. 

Usage Example
-------------------------

```python
    from src.utils.convertors.dot import dot2png

    dot2png('example.dot', 'output.png') 
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".