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
This code block defines a set of type annotations for various data structures and objects used within the `gpt4free` module. The annotations ensure type safety and provide clear documentation for developers working with these elements.

Execution Steps
-------------------------
1. **Imports**: The code starts by importing necessary modules and classes, including `sys`, `os`, and `typing`.
2. **Type Aliases**: Several custom type aliases are defined using the `NewType` and `TypedDict` classes. These aliases provide meaningful names for complex types, making the code more readable and maintainable.
    - `SHA256`: Defines a type alias for SHA-256 hashes as strings.
    - `CreateResult`: Represents an iterator that yields either strings or instances of `ResponseType`.
    - `AsyncResult`: Defines an asynchronous iterator for yielding strings or `ResponseType` objects.
    - `Messages`: Defines a list of dictionaries that hold message data.
    - `Cookies`: Represents a dictionary of cookies.
    - `ImageType`: A union type representing different possible image types (string paths, byte streams, file-like objects, PIL.Image instances, or file paths).
    - `MediaListType`: A list of tuples, where each tuple contains an `ImageType` and an optional caption string.
3. **Exposing Types**: The `__all__` variable lists all the type aliases and other types that should be accessible from the module. This ensures that only intended types are imported when other modules use the `gpt4free.g4f.typing` module.

Usage Example
-------------------------
```python
from gpt4free.g4f.typing import SHA256, CreateResult, Messages, ImageType, MediaListType

# Example SHA-256 hash
hash_value: SHA256 = "e594682225e528a547807d647044532c27837f56d45797707a464225d3774712"

# Example message list
messages: Messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I am doing well, thank you for asking!"},
]

# Example image type
image_path: ImageType = "path/to/image.jpg"

# Example media list
media_list: MediaListType = [
    ("path/to/image1.jpg", "Image 1 caption"),
    ("path/to/image2.png", "Image 2 caption"),
]
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".