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
This code block defines a function called `get_relative_path` that extracts a relative path from a full path.

Execution Steps
-------------------------
1. The function takes two arguments: a full path (`full_path`) and a segment of that path (`relative_from`).
2. It converts the input strings to `Path` objects.
3. It finds the index of the `relative_from` segment in the `parts` of the path.
4. If the segment is found, it creates a relative path starting from the specified segment and returns it.
5. If the segment is not found, the function returns `None`.

Usage Example
-------------------------

```python
    from src.utils.path import get_relative_path

    full_path = '/home/user/project/src/utils/path.py'
    relative_from = 'src'

    relative_path = get_relative_path(full_path, relative_from)

    print(relative_path)  # Output: src/utils/path.py
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".