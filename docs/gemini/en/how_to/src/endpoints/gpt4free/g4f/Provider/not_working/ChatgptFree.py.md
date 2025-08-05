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
[Explanation of what the code does.]

Execution Steps
-------------------------
1. [Description of the first step.]
2. [Description of the second step.]
3. [Continue as needed...]

Usage Example
-------------------------

```python
    [Code usage example]
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".
```

## How to Use This Code Block
=========================================================================================

### Description
The `ChatgptFree` class provides an asynchronous generator for interacting with the chatgptfree.ai API. It inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`, providing basic functionality for asynchronous generation and model handling.

### Execution Steps
1. **Initialization**:
   - The `ChatgptFree` class is initialized with default values for URL, model, and other configuration parameters.
   - The class is marked as "not working" ( `working = False`).

2. **Asynchronous Generator Creation**:
   - The `create_async_generator` class method is called to create an asynchronous generator for a specific model (`model`) and input messages (`messages`).
   - Optional parameters such as `proxy`, `timeout`, and `cookies` can be provided.

3. **Request Setup**:
   - The code sets up the `StreamSession` for handling the API requests.
   - Headers and cookies are configured.

4. **Fetching Nonce and Post ID**:
   - If the nonce (`_nonce`) and post ID (`_post_id`) haven't been retrieved, the code makes a GET request to the chatgptfree.ai homepage to extract these values.

5. **Formatting Prompt**:
   - The input messages (`messages`) are formatted into a prompt using the `format_prompt` helper function.

6. **Sending API Request**:
   - A POST request is sent to the chatgptfree.ai API endpoint (`/wp-admin/admin-ajax.php`) with the formatted prompt, nonce, post ID, and other necessary data.

7. **Processing Responses**:
   - The response is processed line by line.
   - If the line starts with "data: ", the data is decoded as JSON and the content is yielded to the asynchronous generator.
   - If the line does not start with "data: ", it is accumulated in a buffer until a final JSON response is received.

8. **Handling Errors**:
   - The code handles errors such as `json.JSONDecodeError` if decoding the JSON response fails.
   - The `raise_for_status` function is used to raise an exception if the API request fails.

### Usage Example

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.ChatgptFree import ChatgptFree

async def chat_with_chatgptfree(messages: Messages):
    """
    Asynchronously sends messages to the chatgptfree.ai API and yields the responses.
    """
    async for response in ChatgptFree.create_async_generator(model="gpt-4o-mini-2024-07-18", messages=messages):
        print(response)

if __name__ == '__main__':
    messages = [
        {"role": "user", "content": "Hello, how are you?"},
    ]
    asyncio.run(chat_with_chatgptfree(messages))