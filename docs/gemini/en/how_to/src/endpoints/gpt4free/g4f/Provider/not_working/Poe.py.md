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
This code block defines a `Poe` class that implements the `AbstractProvider` interface, providing functionality for interacting with the Poe.com platform. 

Execution Steps
-------------------------
1. **Import necessary modules**: Imports modules related to time, typing, and Selenium WebDriver, along with custom helper functions.
2. **Define model mappings**: Creates a dictionary `models` mapping model names to their corresponding display names.
3. **Define `Poe` class**: Creates the `Poe` class with the following attributes:
    - `url`: The base URL for Poe.com.
    - `working`: Set to `False` as the provider is not fully functional.
    - `needs_auth`: Set to `True` as authentication is required.
    - `supports_stream`: Set to `True` to indicate stream support.
    - `models`: A list of supported models.
4. **`create_completion` method**:
    - **Validates the model**: Checks if the provided model is supported.
    - **Formats the prompt**: Uses the `format_prompt` helper function to format the prompt message.
    - **Initializes WebDriver**: Creates a `WebDriverSession` object for interacting with the browser.
    - **Injects custom script**: Injects a script into the browser to capture messages from the Poe.com interface.
    - **Navigates to the model page**: Opens the specified model page on Poe.com.
    - **Sends the prompt**: Finds the input textarea element and sends the formatted prompt.
    - **Initiates response capture**: Uses a while loop to capture and yield response chunks from the Poe.com interface.


Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.Poe import Poe
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.helper import Messages

# Create a Poe instance
poe_provider = Poe()

# Define messages for the conversation
messages = Messages(
    [
        {
            "role": "user",
            "content": "What is the meaning of life?",
        },
    ]
)

# Call the create_completion method to generate a response
response = poe_provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=True)

# Iterate through the response chunks
for chunk in response:
    print(chunk)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".