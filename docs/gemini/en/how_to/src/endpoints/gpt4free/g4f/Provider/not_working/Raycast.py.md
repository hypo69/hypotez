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
## \file /hypotez/src/endpoints/gpt4free/g4f/Provider/not_working/Raycast.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module::  hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.Raycast
:platform: Windows, Unix
:synopsis: Implements the Raycast provider for GPT4Free.

This module provides a class named `Raycast` that implements the `AbstractProvider` interface for the GPT4Free library. 
The `Raycast` class utilizes the Raycast API to generate text completions using the GPT-3.5-turbo and GPT-4 models.
"""

from __future__ import annotations

import json

import requests

from ...typing import CreateResult, Messages
from ..base_provider import AbstractProvider


class Raycast(AbstractProvider):
    """
    The Raycast provider for GPT4Free.

    This class implements the `AbstractProvider` interface to provide access to the Raycast API for text completion generation. 
    It supports both GPT-3.5-turbo and GPT-4 models.

    :param url: The base URL for the Raycast API.
    :param supports_stream: Indicates if the provider supports streaming responses.
    :param needs_auth: Indicates if the provider requires authentication.
    :param working: Indicates if the provider is currently working.
    :param models: A list of supported models.
    """
    url                     = "https://raycast.com"
    supports_stream         = True
    needs_auth              = True
    working                 = False

    models = [
        "gpt-3.5-turbo",
        "gpt-4"
    ]

    @staticmethod
    def create_completion(
        model: str,
        messages: Messages,
        stream: bool,
        proxy: str = None,
        **kwargs,
    ) -> CreateResult:
        """
        Generates a text completion using the Raycast API.

        This method sends a request to the Raycast API to generate a text completion based on the provided parameters. 
        It supports streaming responses and requires an authentication token passed via the `auth` parameter.

        :param model: The name of the language model to use (e.g., "gpt-3.5-turbo", "gpt-4").
        :param messages: A list of messages representing the conversation history.
        :param stream: Indicates if the response should be streamed.
        :param proxy: An optional proxy server to use for the request.
        :param kwargs: Additional keyword arguments, including `auth` for the authentication token.
        :return: A generator yielding text completion chunks or a single completion string, depending on the `stream` parameter.

        :raises: ValueError if the `auth` parameter is missing.

        :example:
            >>> from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.Raycast import Raycast
            >>> messages = [
            ...     {'role': 'user', 'content': 'Hello, how are you?'},
            ...     {'role': 'assistant', 'content': 'I am doing well, thanks for asking.'},
            ... ]
            >>> auth_token = 'your_raycast_auth_token'
            >>> response = Raycast.create_completion(model='gpt-3.5-turbo', messages=messages, stream=True, auth=auth_token)
            >>> for chunk in response:
            ...     print(chunk)
            ...
            I'm doing well, thanks for asking. What about you?
        """
        auth = kwargs.get('auth')
        if not auth:
            raise ValueError("Raycast needs an auth token, pass it with the `auth` parameter")

        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Authorization': f'Bearer {auth}',
            'Content-Type': 'application/json',
            'User-Agent': 'Raycast/0 CFNetwork/1410.0.3 Darwin/22.6.0',
        }
        parsed_messages = [
            {'author': message['role'], 'content': {'text': message['content']}}
            for message in messages
        ]
        data = {
            "debug": False,
            "locale": "en-CN",
            "messages": parsed_messages,
            "model": model,
            "provider": "openai",
            "source": "ai_chat",
            "system_instruction": "markdown",
            "temperature": 0.5
        }
        response = requests.post(
            "https://backend.raycast.com/api/v1/ai/chat_completions",
            headers=headers,
            json=data,
            stream=True,
            proxies={"https": proxy}
        )
        for token in response.iter_lines():
            if b'data: ' not in token:
                continue
            completion_chunk = json.loads(token.decode().replace('data: ', ''))
            token = completion_chunk['text']
            if token != None:
                yield token