**Instructions for Generating Code Documentation**

How to Use The `ToolSupportProvider` Class
=========================================================================================

Description
-------------------------
The `ToolSupportProvider` class is a subclass of `AsyncGeneratorProvider` that provides support for using tools with OpenAI models. It allows you to specify a tool and its parameters, which the model can then use to generate responses.

Execution Steps
-------------------------
1. **Initialize the Provider**: The `create_async_generator` class method creates an asynchronous generator object that handles the communication with the OpenAI API.
2. **Validate Inputs**: The code checks if the provided model has a tool specified and if the response format is correct.
3. **Prepare Tool Information**: It extracts the tool's function name and its parameters from the provided tool configuration.
4. **Prepare Prompt**: It constructs a prompt that includes information about the tool and its parameters.
5. **Invoke the Provider**: It calls the `get_async_create_function` method of the underlying provider to handle the communication with the OpenAI API, passing the prompt, tool information, and other parameters.
6. **Process Responses**: The code iterates through the responses from the API, handling different types of responses (e.g., text chunks, usage information, and finish reason).
7. **Yield Responses**: The generator yields the processed responses to the caller.
8. **Process Tool Calls**: If a tool is specified, it constructs a tool call object and yields it to the caller.
9. **Yield Final Response**: It yields the final generated response to the caller.
10. **Yield Finish Reason**: It yields the finish reason for the generation, if available.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.providers.tool_support import ToolSupportProvider

# Define the tool configuration
tool_config = {
    "function": {
        "name": "my_tool",
        "parameters": {
            "properties": {
                "param1": {"type": "string"},
                "param2": {"type": "integer"}
            }
        }
    }
}

# Define the prompt
messages = [{"role": "user", "content": "Please use the `my_tool` to calculate the sum of 2 and 3."}]

# Create an instance of ToolSupportProvider
provider = ToolSupportProvider()

# Generate response using the tool
async for response in provider.create_async_generator(
    model="gpt-3.5-turbo:tool_support",
    messages=messages,
    tools=[tool_config],
    response_format={"type": "json"}
):
    print(response)
```

```python
from __future__ import annotations

import json

from ..typing import AsyncResult, Messages, MediaListType
from ..client.service import get_model_and_provider
from ..client.helper import filter_json
from .base_provider import AsyncGeneratorProvider
from .response import ToolCalls, FinishReason, Usage

class ToolSupportProvider(AsyncGeneratorProvider):
    working = True

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        stream: bool = True,
        media: MediaListType = None,
        tools: list[str] = None,
        response_format: dict = None,
        **kwargs
    ) -> AsyncResult:
        provider = None
        if ":" in model:
            provider, model = model.split(":", 1)
        model, provider = get_model_and_provider(
            model, provider,
            stream, logging=False,
            has_images=media is not None
        )
        if tools is not None:
            if len(tools) > 1:
                raise ValueError("Only one tool is supported.")
            if response_format is None:
                response_format = {"type": "json"}
            tools = tools.pop()
            lines = ["Respone in JSON format."]
            properties = tools["function"]["parameters"]["properties"]
            properties = {key: value["type"] for key, value in properties.items()}
            lines.append(f"Response format: {json.dumps(properties, indent=2)}")
            messages = [{"role": "user", "content": "\\n".join(lines)}] + messages

        finish = None
        chunks = []
        has_usage = False
        async for chunk in provider.get_async_create_function()(\
            model,
            messages,
            stream=stream,
            media=media,
            response_format=response_format,
            **kwargs
        ):
            if isinstance(chunk, str):
                chunks.append(chunk)
            elif isinstance(chunk, Usage):
                yield chunk
                has_usage = True
            elif isinstance(chunk, FinishReason):
                finish = chunk
                break
            else:
                yield chunk

        if not has_usage:
            yield Usage(completion_tokens=len(chunks), total_tokens=len(chunks))

        chunks = "".join(chunks)
        if tools is not None:
            yield ToolCalls([{\
                "id": "",
                "type": "function",
                "function": {\
                    "name": tools["function"]["name"],
                    "arguments": filter_json(chunks)\
                }\
            }])
        yield chunks

        if finish is not None:
            yield finish