**Instructions for Generating Code Documentation**

How to Use This Code Block
=========================================================================================

Description
-------------------------
The code block defines a class called `Qwen_Qwen_2_72B` which implements an asynchronous generator provider for the Qwen-2.72B language model hosted on Hugging Face. 

Execution Steps
-------------------------
1. The `create_async_generator` class method is used to generate an asynchronous generator that produces responses from the Qwen-2.72B model.
2. The method first generates a unique session hash to identify the interaction.
3. It prepares a prompt by formatting the provided messages and extracting a system message if present.
4. The method sends a "join" request to the Qwen-2.72B API endpoint with the prompt and session hash.
5. The API responds with an event ID, which is used to initiate a data stream request.
6. The method sends a data stream request to the API endpoint with the session hash.
7. The API responds with a stream of data representing the generated response.
8. The `create_async_generator` method parses the data stream line by line, checking for generation stages and completion signals.
9. If the message indicates "process_generating", the method yields the generated fragments.
10. If the message indicates "process_completed", the method yields the remaining part of the final response and breaks the loop.

Usage Example
-------------------------

```python
    from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space import Qwen_Qwen_2_72B
    from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

    messages: Messages = [
        {"role": "user", "content": "What is the meaning of life?"},
    ]

    async def main():
        provider = Qwen_Qwen_2_72B()
        async for response in provider.create_async_generator(model="qwen-2-72b", messages=messages):
            print(response)

    if __name__ == "__main__":
        import asyncio
        asyncio.run(main())
```

```python
                from __future__ import annotations

import aiohttp
import json
import uuid
import re

from ...typing import AsyncResult, Messages
from ..base_provider import AsyncGeneratorProvider, ProviderModelMixin
from ..helper import format_prompt
from ... import debug

class Qwen_Qwen_2_72B(AsyncGeneratorProvider, ProviderModelMixin):
    label = "Qwen Qwen-2.72B"
    url = "https://qwen-qwen2-72b-instruct.hf.space"
    api_endpoint = "https://qwen-qwen2-72b-instruct.hf.space/queue/join?"
    
    working = True
    supports_stream = True
    supports_system_message = True
    supports_message_history = False
    
    default_model = "qwen-qwen2-72b-instruct"
    model_aliases = {"qwen-2-72b": default_model}
    models = list(model_aliases.keys())

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        def generate_session_hash():
            """Generate a unique session hash."""
            return str(uuid.uuid4()).replace(\'-\', \'\')[:12]

        # Generate a unique session hash
        session_hash = generate_session_hash()

        headers_join = {
            \'accept\': \'*/*\',\n            \'accept-language\': \'en-US,en;q=0.9\',\n            \'content-type\': \'application/json\',\n            \'origin\': f\'{cls.url}\',\n            \'referer\': f\'{cls.url}/\',\n            \'user-agent\': \'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\'\n        }

        # Prepare the prompt
        system_prompt = "\\n".join([message["content"] for message in messages if message["role"] == "system"])
        messages = [message for message in messages if message["role"] != "system"]
        prompt = format_prompt(messages)

        payload_join = {
            "data": [prompt, [], system_prompt],
            "event_data": None,
            "fn_index": 0,
            "trigger_id": 11,
            "session_hash": session_hash
        }

        async with aiohttp.ClientSession() as session:
            # Send join request
            async with session.post(cls.api_endpoint, headers=headers_join, json=payload_join) as response:
                event_id = (await response.json())[\'event_id\']

            # Prepare data stream request
            url_data = f\'{cls.url}/queue/data\'\n\n            headers_data = {\n                \'accept\': \'text/event-stream\',\n                \'accept-language\': \'en-US,en;q=0.9\',\n                \'referer\': f\'{cls.url}/\',\n                \'user-agent\': \'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\'\n            }

            params_data = {\n                \'session_hash\': session_hash\n            }

            # Send data stream request
            async with session.get(url_data, headers=headers_data, params=params_data) as response:
                full_response = ""
                final_full_response = ""
                async for line in response.content:
                    decoded_line = line.decode(\'utf-8\')
                    if decoded_line.startswith(\'data: \'):
                        try:
                            json_data = json.loads(decoded_line[6:])

                            # Look for generation stages
                            if json_data.get(\'msg\') == \'process_generating\':
                                if \'output\' in json_data and \'data\' in json_data[\'output\']:\n                                    output_data = json_data[\'output\'][\'data\']\n                                    if len(output_data) > 1 and len(output_data[1]) > 0:\n                                        for item in output_data[1]:\n                                            if isinstance(item, list) and len(item) > 1:\n                                                fragment = str(item[1])\n                                                # Ignore [0, 1] type fragments and duplicates\n                                                if not re.match(r\'^\\[.*\\]$\', fragment) and not full_response.endswith(fragment):\n                                                    full_response += fragment\n                                                    yield fragment\n\n                            # Check for completion\n                            if json_data.get(\'msg\') == \'process_completed\':\n                                # Final check to ensure we get the complete response\n                                if \'output\' in json_data and \'data\' in json_data[\'output\']:\n                                    output_data = json_data[\'output\'][\'data\']\n                                    if len(output_data) > 1 and len(output_data[1]) > 0:\n                                        final_full_response = output_data[1][0][1]\n                                        \n                                        # Clean up the final response\n                                        if final_full_response.startswith(full_response):\n                                            final_full_response = final_full_response[len(full_response):]\n                                        \n                                        # Yield the remaining part of the final response\n                                        if final_full_response:\n                                            yield final_full_response\n                                break\n\n                        except json.JSONDecodeError:\n                            debug.log("Could not parse JSON:", decoded_line)\n\n                ```