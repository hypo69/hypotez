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
This code block defines custom exception classes for handling specific errors related to Mega.

Execution Steps
-------------------------
1. The `MegaException` class is defined as a base exception class for all Mega-related errors.
2. The `MegaIncorrectPasswordExcetion` class inherits from `MegaException` and represents an error occurring when an incorrect password or email is provided.
3. The `MegaRequestException` class inherits from `MegaException` and indicates an error in the request made to the Mega API.

Usage Example
-------------------------

```python
    try:
        # Code that interacts with the Mega API
        # ...
    except MegaIncorrectPasswordExcetion as e:
        print(f"Incorrect password or email: {e}")
    except MegaRequestException as e:
        print(f"Error in the request: {e}")
    except MegaException as e:
        print(f"General Mega error: {e}")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".