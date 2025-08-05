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
The code implements a Flask backend API for processing conversations using a large language model (LLM) like ChatGPT. It handles requests, builds conversation contexts, fetches search results, and generates responses based on user input and selected jailbreak instructions.

Execution Steps
-------------------------
1. **Initialization**:
    - The `Backend_Api` class is initialized with a Flask app instance and configuration settings.
    - It defines a route for handling conversation requests (`/backend-api/v2/conversation`).
    - If auto-proxy is enabled, it starts a background thread to update working proxies.
2. **Conversation Processing**:
    - The `_conversation` method handles POST requests to the conversation route.
    - It retrieves user input, jailbreak instructions, and model selection from the request.
    - It builds a conversation context by combining system messages, existing conversation history, search results, and the user prompt.
    - It utilizes the `ChatCompletion` class from `g4f` to generate a response from the selected LLM.
    - It streams the response to the client in text/event-stream format, enabling real-time feedback.
3. **Error Handling**:
    - The code includes error handling using a `try...except` block to catch exceptions and return appropriate error messages to the client.
4. **Conversation Context Building**:
    - The `build_messages` function constructs the conversation context by combining various elements:
        - System messages: Defines the LLM's role, instructions, and current date.
        - Existing conversation history: Retrieves previous messages from the request.
        - Search results: Fetches relevant web results based on the prompt if internet access is enabled.
        - Jailbreak instructions: Adds specific jailbreak instructions based on the selected jailbreak.
        - User prompt: Includes the current user's input.
    - It limits the conversation size to prevent API token quantity errors.
5. **Search Results Retrieval**:
    - The `fetch_search_results` function uses the DDG API to retrieve search results based on the user prompt and formats them for inclusion in the conversation context.
6. **Response Stream Generation**:
    - The `generate_stream` function handles the streaming of the LLM response to the client.
    - It supports jailbreak instructions by checking if the response includes specific patterns indicating a successful jailbreak.
7. **Jailbreak Success/Failure Detection**:
    - The `response_jailbroken_success` and `response_jailbroken_failed` functions check the response content to determine if the jailbreak attempt was successful or failed.
8. **Language Detection and Response**:
    - The `set_response_language` function detects the language of the user's prompt and sets a system message informing the LLM to respond in the same language.
9. **Jailbreak Instruction Retrieval**:
    - The `isJailbreak` function checks the selected jailbreak type and retrieves the corresponding instructions from the `special_instructions` configuration dictionary.

Usage Example
-------------------------

```python
from server.backend import Backend_Api

# Create a Flask app instance
app = Flask(__name__)

# Initialize the backend API
backend = Backend_Api(app, {'use_auto_proxy': True})

# Define the route for conversation requests
@app.route('/backend-api/v2/conversation', methods=['POST'])
def conversation():
    return backend._conversation()

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".