# Image Chat with Reka

## Overview

This Python script demonstrates how to use the `g4f` library to interact with the Reka AI model for image-based chat. It leverages the Reka model to analyze an image and provide a textual description of its contents.

## Details

This script utilizes the `g4f` library, which provides a convenient interface for interacting with various AI models, including Reka. The code showcases the following steps:

1. **Initialization**:
   - Creates a `Client` object from the `g4f` library, specifying the `provider` as `Reka`.
2. **Image Chat Request**:
   - Uses the `chat.completions.create` method to initiate a chat conversation with the `reka-core` model.
   - Provides the following parameters:
     - `model`: Specifies the model to use (`reka-core` in this case).
     - `messages`: Defines the initial user prompt, which is "What can you see in the image?".
     - `stream`: Enables streaming of the response, allowing for real-time output.
     - `image`: Opens the specified image file ("docs/images/cat.jpeg" in this example) as a file object and provides it to the model.
3. **Response Processing**:
   - Iterates through the streamed responses from the model (`completion`).
   - Prints the content of each message, effectively displaying the Reka model's description of the image.

##  Code Breakdown

```python
                # Image Chat with Reca
# !! YOU NEED COOKIES / BE LOGGED IN TO chat.reka.ai
# download an image and save it as test.png in the same folder

from g4f.client import Client
from g4f.Provider import Reka

client = Client(
    provider = Reka # Optional if you set model name to reka-core
)

completion = client.chat.completions.create(
    model = "reka-core",
    messages = [
        {
            "role": "user",
            "content": "What can you see in the image ?"
        }
    ],
    stream = True,
    image = open("docs/images/cat.jpeg", "rb") # open("path", "rb"), do not use .read(), etc. it must be a file object
)

for message in completion:
    print(message.choices[0].delta.content or "")
    
    # >>> In the image there is ...

```

##  How it works

The script utilizes the `g4f` library, specifically its `Client` object, to interact with the Reka AI model. The `chat.completions.create` method is called to initiate a chat conversation, providing the model name, initial user prompt, and image data. The `stream` parameter enables streaming of the response, allowing for incremental output. The script then iterates through the streamed responses, printing each message to the console.

##  Examples

```python
# Example Usage
from g4f.client import Client
from g4f.Provider import Reka

# Initialize the client
client = Client(provider=Reka)

# Define the user prompt
user_prompt = "What can you see in the image?"

# Specify the image path
image_path = "docs/images/cat.jpeg"

# Initiate the chat with the Reka model
completion = client.chat.completions.create(
    model="reka-core",
    messages=[{"role": "user", "content": user_prompt}],
    stream=True,
    image=open(image_path, "rb"),
)

# Process and print the streamed responses
for message in completion:
    print(message.choices[0].delta.content or "")

```

##  Parameter Details

- `provider`: Specifies the AI model provider (in this case, Reka).
- `model`: Indicates the specific AI model to use (`reka-core`).
- `messages`: Defines the messages exchanged in the chat conversation.
- `stream`: Enables streaming of the response, allowing for incremental output.
- `image`: Provides the image data for analysis.

##  Important Notes

- You need to have cookies or be logged in to chat.reka.ai.
- The image file must be opened as a file object using `open("path", "rb")`. Do not use `.read()` or other methods that read the entire file into memory.

This script offers a basic example of how to use the Reka model for image-based chat. You can extend this script to incorporate additional features, such as user input, image processing, and more complex AI interactions.