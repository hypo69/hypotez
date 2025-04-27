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
This code snippet defines a class called `Hashnode` which extends the `AsyncGeneratorProvider` class. The `Hashnode` class represents an asynchronous provider for the Hashnode API, allowing users to send prompts and receive responses from the Hashnode AI.

Execution Steps
-------------------------
1. The `create_async_generator` class method is called with parameters like `model`, `messages`, `search_type`, and `proxy`.
2. The method sets up headers for the request to the Hashnode API, including User-Agent, Accept, Referer, and Content-Type.
3. It then uses an `aiohttp.ClientSession` to make a POST request to the Hashnode API's `search` endpoint with the prompt as the request body.
4. If `search_type` is set to "websearch", the method retrieves search results from the `search` endpoint and stores them in `cls._sources`.
5. The method constructs a data dictionary containing the chatId, message history, prompt, searchType, and searchResults.
6. It makes another POST request to the Hashnode API's `completion` endpoint with the constructed data dictionary as the request body.
7. The method then iterates over the response content using `response.content.iter_any()`, yielding each chunk of data as it's received.
8. The `get_sources` class method retrieves and returns a list of sources from `cls._sources`.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Hashnode import Hashnode, SearchTypes
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

async def example():
    messages: Messages = [
        {"role": "user", "content": "What is the capital of France?"}
    ]
    async for response_chunk in Hashnode.create_async_generator(model="text-davinci-003", messages=messages, search_type=SearchTypes.websearch):
        print(response_chunk)

```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".