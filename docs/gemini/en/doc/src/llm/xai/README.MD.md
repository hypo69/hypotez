# xAI API Client

## Overview

This module provides a Python client for interacting with the xAI API. The client simplifies the process of making requests to the xAI API, including both standard and streaming requests.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
    - [Initialization](#initialization)
    - [Chat Completion](#chat-completion)
    - [Streaming Chat Completion](#streaming-chat-completion)
- [Example](#example)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

- **Authentication**: Securely authenticate your requests using your xAI API key.
- **Chat Completion**: Generate responses from the xAI models using the `chat_completion` method.
- **Streaming Responses**: Stream responses from the xAI models using the `stream_chat_completion` method.

## Installation

To use this client, you need to have Python installed on your system. You can install the required dependencies using pip:

```bash
pip install requests
```

## Usage

### Initialization

First, initialize the `XAI` class with your API key:

```python
from xai import XAI

api_key = "your_api_key_here"  # Replace with your actual API key
xai = XAI(api_key)
```

### Chat Completion

To generate a response from the xAI model, use the `chat_completion` method:

```python
messages = [
    {
        "role": "system",
        "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."
    },
    {
        "role": "user",
        "content": "What is the answer to life and universe?"
    }
]

completion_response = xai.chat_completion(messages)
print("Non-streaming response:", completion_response)
```

### Streaming Chat Completion

To stream responses from the xAI model, use the `stream_chat_completion` method:

```python
stream_response = xai.stream_chat_completion(messages)
print("Streaming response:")
for line in stream_response:
    if line.strip():
        print(json.loads(line))
```

## Example

Here is a complete example of how to use the `XAI` client:

```python
import json
from xai import XAI

api_key = "your_api_key_here"  # Replace with your actual API key
xai = XAI(api_key)

messages = [
    {
        "role": "system",
        "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."
    },
    {
        "role": "user",
        "content": "What is the answer to life and universe?"
    }
]

# Non-streaming request
completion_response = xai.chat_completion(messages)
print("Non-streaming response:", completion_response)

# Streaming request
stream_response = xai.stream_chat_completion(messages)
print("Streaming response:")
for line in stream_response:
    if line.strip():
        print(json.loads(line))
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you encounter any problems or have suggestions for improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

- Thanks to xAI for providing the API that powers this client.
- Inspired by the need for a simple and efficient way to interact with xAI's powerful models.

---

For more information, please refer to the [xAI API documentation](https://api.x.ai/docs).