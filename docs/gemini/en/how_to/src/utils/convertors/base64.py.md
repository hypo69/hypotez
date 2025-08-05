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
This code block contains two functions related to Base64 encoding and decoding. The first function, `base64_to_tmpfile`, decodes Base64 encoded content and writes it to a temporary file. The second function, `base64encode`, encodes the content of an image file into Base64 format.

Execution Steps
-------------------------
**For `base64_to_tmpfile` function:**
1. The function receives Base64 encoded content and the name of a file.
2. It extracts the file extension from the provided file name.
3. A temporary file is created with the extracted extension.
4. The Base64 encoded content is decoded and written to the temporary file.
5. The path to the temporary file is returned.

**For `base64encode` function:**
1. The function receives the path to an image file.
2. The image file is opened in binary read mode.
3. The image file content is read and encoded into Base64 format.
4. The encoded content is returned as a string.

Usage Example
-------------------------

```python
    # Base64 decode and write to temporary file
    base64_content = "SGVsbG8gd29ybGQh"  # Base64 encoded content "Hello world!"
    file_name = "example.txt"
    tmp_file_path = base64_to_tmpfile(base64_content, file_name)
    print(f"Temporary file created at: {tmp_file_path}")

    # Base64 encode image file
    image_path = "path/to/image.jpg"
    base64_encoded_image = base64encode(image_path)
    print(f"Base64 encoded image: {base64_encoded_image}")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".