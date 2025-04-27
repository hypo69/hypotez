# Streaming Text Completions with GPT-4

## Overview

This module demonstrates how to use GPT-4's text completion API with streaming functionality, enabling real-time display of the model's response as it generates text. It provides two methods for streaming: synchronous and asynchronous.

## Details

The code showcases how to utilize the `g4f` library for interacting with GPT-4. The primary focus is on leveraging the `stream=True` parameter in the `chat.completions.create` method to enable streaming text completions. This allows the application to progressively display the generated text as it's produced by the model, offering a more interactive and engaging user experience.

## Functions

### `sync_stream`

**Purpose**: This function demonstrates synchronous streaming of text completions from GPT-4. 

**How the Function Works**:
- Initializes a `Client` object from the `g4f` library.
- Sends a text completion request to GPT-4 with the `stream=True` parameter enabled.
- Iterates through the received stream chunks and prints each chunk's content to the console.

**Example**:
```python
>>> sync_stream()
Hey! How can I recursively list all files in a directory in Python?

```python
import os
def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))
```

### `async_stream`

**Purpose**: This function demonstrates asynchronous streaming of text completions from GPT-4.

**How the Function Works**:
- Initializes an `AsyncClient` object from the `g4f` library.
- Sends a text completion request to GPT-4 with the `stream=True` parameter enabled.
- Uses an `async for` loop to iteratively process the stream chunks and print each chunk's content to the console.

**Example**:
```python
>>> asyncio.run(async_stream())
Hey! How can I recursively list all files in a directory in Python?

```python
import os
def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))
```

### `main`

**Purpose**: This function orchestrates the execution of both synchronous and asynchronous streaming functions, showcasing the differences in their implementation.

**How the Function Works**:
- Calls the `sync_stream` function to demonstrate synchronous streaming.
- Uses `asyncio.run` to execute the `async_stream` function, showcasing asynchronous streaming.

**Example**:
```python
>>> main()
Synchronous Stream:
Hey! How can I recursively list all files in a directory in Python?

```python
import os
def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))


Asynchronous Stream:
Hey! How can I recursively list all files in a directory in Python?

```python
import os
def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))
```

## Parameter Details

- **`model`**:  (str, optional) The GPT-4 model to use. Defaults to "gpt-4".
- **`messages`**: (List[Dict[str, str]], optional) A list of messages to send to the model. Defaults to `[{"role": "user", "content": question}]`.
- **`stream`**: (bool, optional) If True, return a stream of tokens. Defaults to `True`.

## Examples

```python
>>> sync_stream()
Hey! How can I recursively list all files in a directory in Python?

```python
import os
def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))
```
```python
>>> asyncio.run(async_stream())
Hey! How can I recursively list all files in a directory in Python?

```python
import os
def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))
```
```python
>>> main()
Synchronous Stream:
Hey! How can I recursively list all files in a directory in Python?

```python
import os
def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))


Asynchronous Stream:
Hey! How can I recursively list all files in a directory in Python?

```python
import os
def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))
```