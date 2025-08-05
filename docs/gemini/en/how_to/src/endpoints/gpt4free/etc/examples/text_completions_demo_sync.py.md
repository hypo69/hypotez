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
This code snippet demonstrates how to use the GPT-4 Free API to generate text completions synchronously. It utilizes the `g4f.client` library to interact with the API. 

Execution Steps
-------------------------
1. **Import the `Client` Class**: The code imports the `Client` class from the `g4f.client` library. This class provides methods for interacting with the GPT-4 Free API.
2. **Instantiate a Client Object**: A `Client` object is created to represent a connection to the GPT-4 Free API.
3. **Send a Text Completion Request**: The `chat.completions.create` method is called on the `client` object to send a text completion request.
   - The `model` parameter specifies the GPT model to use. In this case, `gpt-4o` is used, representing a version of the GPT-4 model.
   - The `messages` parameter is a list of message objects that provide context to the completion request. This example includes a system message that defines the chatbot's role as a helpful assistant and a user message containing the question.
4. **Process the Response**: The response received from the API is stored in the `response` variable. This response object contains information about the generated text completion.
5. **Retrieve and Print the Generated Text**: The `choices[0].message.content` attribute of the `response` object is accessed to retrieve the generated text. The text is then printed to the console.

Usage Example
-------------------------

```python
from g4f.client import Client

client = Client()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the meaning of life?"}
    ],
)

print(response.choices[0].message.content)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".