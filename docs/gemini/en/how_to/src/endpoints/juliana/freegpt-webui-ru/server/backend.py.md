**Instructions for Generating Code Documentation**

How to Use the `Backend_Api` Class
=========================================================================================

Description
-------------------------
The `Backend_Api` class handles backend API requests for the FreeGPT web UI. It defines routes and functions for processing conversations with the language model.

Execution Steps
-------------------------
1. **Initialization:**
   - The constructor (`__init__`) takes the Flask app instance (`app`) and a configuration dictionary (`config`) as arguments.
   - It initializes the `use_auto_proxy` flag based on the configuration.
   - It defines routes and their corresponding functions:
     - `/backend-api/v2/conversation`: This route is handled by the `_conversation` function.
   - If auto-proxy is enabled, a thread is started to update working proxies in the background.

2. **Conversation Processing:**
   - The `_conversation` function handles POST requests to the `/backend-api/v2/conversation` route.
   - It retrieves parameters from the request (streaming, jailbreak, model) and builds a conversation message list (`messages`) using the `build_messages` function.
   - It generates a response using the OpenAI ChatCompletion API (`ChatCompletion.create`).
   - It returns the response as a server-sent event stream (`text/event-stream`) using Flask's `response_class`.

3. **Error Handling:**
   - The `_conversation` function includes a try-except block to handle exceptions that might occur during processing.
   - If an exception occurs, it logs the error and returns an error response.

4. **Message Building:**
   - The `build_messages` function builds a list of conversation messages.
   - It retrieves existing conversation messages, web search results (if internet access is enabled), and jailbreak instructions (if applicable) from the request.
   - It adds a system message to the conversation, providing context for the language model.
   - It appends the prompt to the conversation.
   - It limits the conversation size to avoid API token quantity errors.

5. **Jailbreak Handling:**
   - The `isJailbreak` function checks if the `jailbreak` parameter indicates a specific jailbreak instruction set.
   - If a jailbreak is specified, it retrieves the corresponding instructions from the `special_instructions` configuration.

6. **Search Results Fetching:**
   - The `fetch_search_results` function retrieves search results from a DuckDuckGo API.
   - It constructs a list of system messages containing the snippets and URLs of the search results.

7. **Response Stream Handling:**
   - The `generate_stream` function yields responses from the language model in a stream.
   - It handles jailbreak responses by checking for specific keywords (ACT:).

Usage Example
-------------------------

```python
from server.backend import Backend_Api

# Initialize the Backend_Api class
backend_api = Backend_Api(app, config)

# Send a conversation request
response = backend_api.app.test_client().post(
    '/backend-api/v2/conversation',
    json={
        'stream': True,
        'jailbreak': 'Default',
        'model': 'gpt-3.5-turbo',
        'meta': {
            'content': {
                'conversation': [],
                'internet_access': True,
                'parts': [{'content': 'Hello, how are you?'}]
            }
        }
    }
)

# Process the response
print(response.data.decode('utf-8'))
```