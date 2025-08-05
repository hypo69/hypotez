# AIUncensored Provider

## Overview

This module provides the `AIUncensored` class, which is a provider for the `hypotez` project, implementing the `AsyncGeneratorProvider` interface. It allows interaction with the AIUncensored API for generating text and code.

## Details

The `AIUncensored` provider utilizes the AIUncensored API to generate text and code using a variety of models, including "hermes3-70b". It supports streaming responses, system messages, and message history.

## Classes

### `AIUncensored`

**Description**: This class implements an asynchronous generator provider for interacting with the AIUncensored API. It inherits from `AsyncGeneratorProvider` and `ProviderModelMixin` to provide consistent API behavior.

**Inherits**:
  - `AsyncGeneratorProvider`
  - `ProviderModelMixin`

**Attributes**:

  - `url` (str): The base URL of the AIUncensored API.
  - `api_key` (str): The API key for accessing the service.
  - `working` (bool): Indicates whether the provider is currently working.
  - `supports_stream` (bool): Indicates whether the provider supports streaming responses.
  - `supports_system_message` (bool): Indicates whether the provider supports system messages.
  - `supports_message_history` (bool): Indicates whether the provider supports message history.
  - `default_model` (str): The default model used by the provider.
  - `models` (list): A list of supported models.
  - `model_aliases` (dict): A mapping of model aliases to their actual names.

**Methods**:

  - `calculate_signature(timestamp: str, json_dict: dict) -> str`: Calculates the signature for an API request using HMAC-SHA256.
  - `get_server_url() -> str`: Retrieves a random server URL from a list of available servers.
  - `create_async_generator(model: str, messages: Messages, stream: bool = False, proxy: str = None, api_key: str = None, **kwargs) -> AsyncResult`: Creates an asynchronous generator for generating text from the AIUncensored API.

## Class Methods

### `calculate_signature`

```python
    @staticmethod
    def calculate_signature(timestamp: str, json_dict: dict) -> str:
        """ 
        Вычисляет сигнатуру для запроса API с помощью HMAC-SHA256.

        Args:
            timestamp (str):  Время создания запроса в формате UTC (в секундах).
            json_dict (dict): JSON-объект запроса.

        Returns:
            str:  Шестнадцатеричная строка, представляющая сигнатуру.

        """
        message = f"{timestamp}{json.dumps(json_dict)}"
        secret_key = b'your-super-secret-key-replace-in-production'
        signature = hmac.new(
            secret_key,
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
```

**Purpose**: This method calculates the signature for an API request using HMAC-SHA256.

**Parameters**:

 - `timestamp` (str): Time of request creation in UTC (seconds).
 - `json_dict` (dict): JSON object of the request.

**Returns**:

 - `str`: Hexadecimal string representing the signature.

**How the Function Works**:

 - The function combines the timestamp and JSON-encoded request data into a single message string.
 - It then calculates the HMAC-SHA256 hash of the message string using the secret key.
 - The calculated hash is returned as a hexadecimal string.

**Examples**:

 - `AIUncensored.calculate_signature('1694926901', {'messages': [{'role': 'user', 'content': 'Hello, world!'}]})`


### `get_server_url`

```python
    @staticmethod
    def get_server_url() -> str:
        """ 
        Возвращает случайный URL-адрес сервера из списка доступных серверов.

        Returns:
            str:  URL-адрес сервера.
        """
        servers = [
            "https://llm-server-nov24-ibak.onrender.com",
            "https://llm-server-nov24-qv2w.onrender.com", 
            "https://llm-server-nov24.onrender.com"
        ]
        return random.choice(servers)
```

**Purpose**: This method returns a random server URL from a list of available servers.

**Parameters**: None

**Returns**:

 - `str`: Server URL.

**How the Function Works**:

 - The function maintains a list of available server URLs.
 - It randomly selects one server URL from the list and returns it.

**Examples**:

 - `AIUncensored.get_server_url()`


### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        stream: bool = False,
        proxy: str = None,
        api_key: str = None,
        **kwargs
    ) -> AsyncResult:      
        """ 
        Создает асинхронный генератор для генерации текста с помощью AIUncensored API.

        Args:
            model (str): Название модели для использования.
            messages (Messages):  Список сообщений для передачи модели.
            stream (bool, optional): Указывает, следует ли использовать потоковый режим. По умолчанию `False`.
            proxy (str, optional):  Прокси-сервер для использования. По умолчанию `None`.
            api_key (str, optional):  API-ключ для доступа к сервису. По умолчанию `None`.
            **kwargs:  Дополнительные аргументы для передачи в API.

        Returns:
            AsyncResult:  Объект `AsyncResult`, который представляет собой асинхронный генератор.

        """
        model = cls.get_model(model)
        
        timestamp = str(int(time.time()))
        
        json_dict = {
            "messages": [{"role": "user", "content": format_prompt(messages)}],
            "model": model,
            "stream": stream
        }
        
        signature = cls.calculate_signature(timestamp, json_dict)
        
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://www.aiuncensored.info',
            'referer': 'https://www.aiuncensored.info/',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'x-api-key': cls.api_key,
            'x-timestamp': timestamp,
            'x-signature': signature
        }
        
        url = f"{cls.get_server_url()}/api/chat"
        
        async with ClientSession(headers=headers) as session:
            async with session.post(url, json=json_dict, proxy=proxy) as response:
                await raise_for_status(response)
                
                if stream:
                    full_response = ""
                    async for line in response.content:
                        if line:
                            try:
                                line_text = line.decode('utf-8')
                                if line_text.startswith(''):
                                    data = line_text[6:]
                                    if data == '[DONE]':
                                        yield FinishReason("stop")
                                        break
                                    try:
                                        json_data = json.loads(data)
                                        if 'data' in json_data:
                                            yield json_data['data']
                                            full_response += json_data['data']
                                    except json.JSONDecodeError:
                                        continue
                            except UnicodeDecodeError:
                                continue
                    if full_response:
                        yield FinishReason("length")
                else:
                    response_json = await response.json()
                    if 'content' in response_json:
                        yield response_json['content']
                        yield FinishReason("length")
```

**Purpose**: This method creates an asynchronous generator for generating text from the AIUncensored API.

**Parameters**:

 - `model` (str): The name of the model to use.
 - `messages` (Messages): List of messages to pass to the model.
 - `stream` (bool, optional): Indicates whether to use streaming mode. Defaults to `False`.
 - `proxy` (str, optional): Proxy server to use. Defaults to `None`.
 - `api_key` (str, optional): API key to access the service. Defaults to `None`.
 - `**kwargs`: Additional arguments to pass to the API.

**Returns**:

 - `AsyncResult`:  `AsyncResult` object which is an asynchronous generator.

**How the Function Works**:

 - The function first validates the specified model, ensuring it is supported.
 - It creates a JSON payload containing the model, messages, and streaming flag.
 - The function calculates a signature for the request using the `calculate_signature` method.
 - It sets up HTTP headers for the request, including API key, timestamp, and signature.
 - The function then sends a POST request to the AIUncensored API with the JSON payload and headers.
 - In streaming mode, the function iterates over the response content, decoding each line and yielding the generated text.
 - In non-streaming mode, the function waits for the full response, decodes it as JSON, and yields the generated text.

**Examples**:

 - `AIUncensored.create_async_generator('hermes3-70b', [{'role': 'user', 'content': 'Hello, world!'}]})`

## Parameter Details

 - `model` (str): The name of the model to use for generating text.
 - `messages` (Messages): A list of messages to be passed to the model, including user messages and assistant responses.
 - `stream` (bool, optional): If `True`, the response will be streamed, yielding text chunks as they become available. Defaults to `False`.
 - `proxy` (str, optional): A proxy server address to use for making API requests. Defaults to `None`.
 - `api_key` (str, optional): An API key for accessing the AIUncensored service. Defaults to `None`.
 - `**kwargs`: Additional keyword arguments that can be passed to the AIUncensored API.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.AIUncensored import AIUncensored

# Example 1: Simple text generation
async def generate_text():
    provider = AIUncensored()
    messages = [{'role': 'user', 'content': 'Hello, world!'}]
    async for response_chunk in provider.create_async_generator('hermes3-70b', messages):
        print(response_chunk)

# Example 2: Streaming mode
async def stream_response():
    provider = AIUncensored()
    messages = [{'role': 'user', 'content': 'Write a short story about a cat.'}]
    async for response_chunk in provider.create_async_generator('hermes3-70b', messages, stream=True):
        print(response_chunk, end='')

# Example 3: Using a custom API key
async def use_api_key():
    provider = AIUncensored()
    messages = [{'role': 'user', 'content': 'What is the meaning of life?'}]
    async for response_chunk in provider.create_async_generator('hermes3-70b', messages, api_key='your_api_key'):
        print(response_chunk)
```