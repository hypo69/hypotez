# Qwen Qwen-2.72B Provider

## Overview

This module provides the `Qwen_Qwen_2_72B` class, which is an asynchronous generator provider for the Qwen-2.72B model from Hugging Face Space. This class allows you to interact with the model and receive its responses in a streaming manner. 

## Details

The `Qwen_Qwen_2_72B` class utilizes the Hugging Face Space API for communication. It provides a mechanism for generating responses from the Qwen-2.72B model based on user prompts and messages. The `create_async_generator` method creates an asynchronous generator that streams the model's responses.

## Classes

### `class Qwen_Qwen_2_72B(AsyncGeneratorProvider, ProviderModelMixin)`

**Description**: An asynchronous generator provider for the Qwen-2.72B model. This class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`.

**Attributes**:
- `label` (str): "Qwen Qwen-2.72B".
- `url` (str): "https://qwen-qwen2-72b-instruct.hf.space".
- `api_endpoint` (str): "https://qwen-qwen2-72b-instruct.hf.space/queue/join?".
- `working` (bool): True, indicating the provider is currently operational.
- `supports_stream` (bool): True, indicating support for streaming responses.
- `supports_system_message` (bool): True, indicating support for system messages.
- `supports_message_history` (bool): False, indicating lack of support for message history.
- `default_model` (str): "qwen-qwen2-72b-instruct".
- `model_aliases` (dict): {"qwen-2-72b": "qwen-qwen2-72b-instruct"}.
- `models` (list): List of supported model names.

**Methods**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`:
    - **Purpose**: This method creates an asynchronous generator that interacts with the Qwen-2.72B model to produce responses.
    - **Parameters**:
        - `model` (str): The name of the Qwen-2.72B model to use.
        - `messages` (Messages): A list of messages to be processed by the model.
        - `proxy` (str, optional): A proxy server URL to use for the request. Defaults to None.
    - **Returns**:
        - `AsyncResult`: An object containing the result of the request.
    - **How the Function Works**:
        1. Generates a unique session hash.
        2. Prepares headers for joining the queue.
        3. Formats the prompt based on messages.
        4. Sends a join request to the Hugging Face Space API, providing the formatted prompt and other parameters.
        5. Retrieves the event ID from the join response.
        6. Prepares headers and parameters for the data stream request.
        7. Sends a data stream request to the API, using the event ID and session hash.
        8. Continuously receives data from the API.
        9. Decodes and parses the data as JSON.
        10. Checks for generation stages and completion status.
        11. Yields response fragments as they are generated.
        12. Returns the final, complete response when the process is completed.
    - **Inner Functions**:
        - `generate_session_hash()`:
            - **Purpose**: Generates a unique session hash for the request.
            - **Returns**:
                - `str`: A unique session hash.
    - **Examples**:
        ```python
        from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.Qwen_Qwen_2_72B import Qwen_Qwen_2_72B
        from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

        messages: Messages = [
            {"role": "user", "content": "Hello, world!"}
        ]

        async def main():
            provider = Qwen_Qwen_2_72B()
            async for response in provider.create_async_generator(messages=messages):
                print(response, end="")
            print()

        if __name__ == "__main__":
            import asyncio
            asyncio.run(main())
        ```

## Parameter Details

- `model` (str): The name of the Qwen-2.72B model to use.
- `messages` (Messages): A list of messages to be processed by the model.
- `proxy` (str, optional): A proxy server URL to use for the request. Defaults to None.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.Qwen_Qwen_2_72B import Qwen_Qwen_2_72B
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {"role": "user", "content": "Hello, world!"}
]

async def main():
    provider = Qwen_Qwen_2_72B()
    async for response in provider.create_async_generator(messages=messages):
        print(response, end="")
    print()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```