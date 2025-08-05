# Text Completions Demo (Sync)

## Overview

This file demonstrates a synchronous text completion request using the `gpt-4o` model from the `g4f` library. It showcases a basic interaction with the OpenAI API using the `Client` object and a sample conversation with a "helpful assistant" role.

## Details

The code utilizes the `Client` class from the `g4f` library to interact with the OpenAI API. The `client.chat.completions.create()` function allows us to send a prompt (a list of messages) to the `gpt-4o` model. The `messages` list defines the conversation context, including a system message that sets the assistant's role as "helpful" and a user message containing the question. 

The example then prints the content of the assistant's response.

## Classes 

### `Client` 

**Description**: This class represents a client for interacting with the OpenAI API.

**Attributes**: None

**Methods**:

- `chat.completions.create()`: This method initiates a chat completion request to the OpenAI API.

## Functions 

### `main` 

**Purpose**: The `main` function serves as the entry point for the script. It initiates a chat completion request and displays the assistant's response.

**Parameters**: None

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**: 

- Initializes a `Client` object for interacting with the OpenAI API.
- Sends a chat completion request to the `gpt-4o` model using the `client.chat.completions.create()` function.
- The prompt consists of two messages:
    - A system message defining the assistant's role as "helpful."
    - A user message containing the question "how does a court case get to the Supreme Court?"
- Retrieves the assistant's response from the `response.choices[0].message.content` attribute.
- Prints the assistant's response.

**Examples**:

```python
from g4f.client import Client

client = Client()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "how does a court case get to the Supreme Court?"}
    ],
)

print(response.choices[0].message.content)
```