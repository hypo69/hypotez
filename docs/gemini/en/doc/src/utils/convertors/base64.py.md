# Module: src.utils.convertors.base64
## Overview

This module provides functions to convert Base64 encoded content to temporary files. It is used in the `hypotez` project to handle and process data encoded in Base64 format.

## Details

This module provides two main functions:

- **`base64_to_tmpfile`**: This function takes Base64 encoded content and a file name as input. It then decodes the Base64 content and writes it to a temporary file with the same extension as the provided file name. The path to the temporary file is returned.

- **`base64encode`**: This function takes a path to an image file and encodes its content using Base64 encoding. The function then returns the encoded data as a string.

## Table of Contents

- [Classes](#classes)
- [Functions](#functions)
- [Inner Functions](#inner-functions)
- [Parameter Details](#parameter-details)
- [Examples](#examples)


## Functions

### `base64_to_tmpfile`

**Purpose**: Converts Base64 encoded content to a temporary file.

**Parameters**:

- `content` (str): Base64 encoded content to be decoded and written to the file.
- `file_name` (str): Name of the file used to extract the file extension for the temporary file.

**Returns**:

- `str`: Path to the temporary file.

**Raises Exceptions**:

- `None`

**How the Function Works**:

- The function first extracts the file extension from the provided file name using `os.path.splitext`.
- It then creates a temporary file using `tempfile.NamedTemporaryFile` with the extracted extension.
- The Base64 encoded content is decoded using `base64.b64decode` and written to the temporary file.
- The path to the temporary file is returned.

**Examples**:

```python
>>> base64_content = "SGVsbG8gd29ybGQh"  # Base64 encoded content "Hello world!"
>>> file_name = "example.txt"
>>> tmp_file_path = base64_to_tmpfile(base64_content, file_name)
>>> print(f"Temporary file created at: {tmp_file_path}")
Temporary file created at: /tmp/tmpfile.txt
```

### `base64encode`

**Purpose**: Encodes the content of an image file using Base64 encoding.

**Parameters**:

- `image_path` (str): Path to the image file to be encoded.

**Returns**:

- `str`: Base64 encoded content of the image file.

**Raises Exceptions**:

- `None`

**How the Function Works**:

- The function opens the image file in binary read mode (`"rb"`).
- It reads the file content using `image_file.read()`.
- The content is then encoded using `base64.b64encode` and decoded to a UTF-8 string using `decode('utf-8')`.
- The encoded string is returned.

**Examples**:

```python
>>> image_path = "image.jpg"
>>> encoded_content = base64encode(image_path)
>>> print(f"Encoded image content: {encoded_content}")
Encoded image content: /9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAUDBAQEAwUEBAQFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQ...
```