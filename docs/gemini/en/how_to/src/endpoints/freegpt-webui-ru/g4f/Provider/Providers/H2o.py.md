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
This code defines a `_create_completion` function that interacts with the H2O GPT-GM API to generate text completions based on a given conversation.

Execution Steps
-------------------------
1. **Prepare conversation**: The code assembles a conversation string from the provided `messages` list, forming a text representation of the conversation.
2. **Initialize session**: A `requests.Session` object is created to handle HTTP requests.
3. **Set headers**: Headers are configured for the HTTP requests, including user agent, origin, and other relevant information.
4. **Perform initial GET request**: A GET request is made to the `https://gpt-gm.h2o.ai/` endpoint to potentially load necessary resources.
5. **Configure settings**: A POST request is sent to `https://gpt-gm.h2o.ai/settings` to send user settings related to the model and preferences.
6. **Create conversation**: A POST request is sent to `https://gpt-gm.h2o.ai/conversation` with the chosen `model` identifier to initiate a conversation with the selected model.
7. **Send completion request**: Another POST request is sent to `https://gpt-gm.h2o.ai/conversation/{conversationId}` with the conversation string, parameters (like temperature, max_new_tokens), and stream settings to trigger the generation of a text completion.
8. **Stream response**: The response is streamed, and each line is processed. If the line contains the `data` field, the corresponding text token is extracted.
9. **Yield tokens**: The extracted tokens are yielded back to the caller, allowing for real-time processing of the generated text.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.freegpt-webui-ru.g4f.Provider.Providers.H2o import _create_completion

messages = [
    {'role': 'user', 'content': 'Hello, how are you?'},
    {'role': 'assistant', 'content': 'I am doing well, thank you for asking.'},
]

for token in _create_completion(model='falcon-40b', messages=messages, stream=True, temperature=0.7):
    print(token, end='')
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".