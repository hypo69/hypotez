# Hashnode Provider for GPT4Free

## Overview

This module defines the `Hashnode` class, a provider for GPT4Free that utilizes the Hashnode API to generate responses. 

## Details

This provider utilizes the `Hashnode` API to generate responses. The class inherits from `AsyncGeneratorProvider`, providing an asynchronous generator to stream responses.

## Classes

### `Hashnode`

**Description**: A provider for GPT4Free that utilizes the Hashnode API to generate responses.

**Inherits**: `AsyncGeneratorProvider`

**Attributes**:

- `url` (str): The base URL of the Hashnode API.
- `working` (bool): Indicates if the provider is currently working.
- `supports_message_history` (bool): Indicates if the provider supports message history.
- `supports_gpt_35_turbo` (bool): Indicates if the provider supports GPT-3.5 turbo.
- `_sources` (list): A list of sources used for web searches.

**Methods**:

- `create_async_generator(model: str, messages: Messages, search_type: str = SearchTypes.websearch, proxy: str = None, **kwargs) -> AsyncResult`
- `get_sources() -> list`

## Class Methods

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        search_type: str = SearchTypes.websearch,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для получения ответов от Hashnode API.

        Args:
            model (str): Имя модели (например, "text-davinci-003").
            messages (Messages): Список сообщений в истории чата.
            search_type (str): Тип поиска (например, "quick", "code", "websearch"). По умолчанию "websearch".
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            **kwargs: Дополнительные ключевые аргументы.

        Returns:
            AsyncResult: Асинхронный результат с генератором, который выдает фрагменты ответа.

        Raises:
            Exception: Если произошла ошибка при запросе к API.

        Example:
            >>> from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Hashnode import Hashnode
            >>> from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Hashnode import SearchTypes
            >>> messages = [{"role": "user", "content": "Hello, world!"}]
            >>> async_generator = await Hashnode.create_async_generator(model='gpt-3.5-turbo', messages=messages, search_type=SearchTypes.websearch)
            >>> async for chunk in async_generator:
            ...     print(chunk)
            ...
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
            "Accept": "*/*",
            "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": f"{cls.url}/rix",
            "Content-Type": "application/json",
            "Origin": cls.url,
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "trailers",
        }
        async with ClientSession(headers=headers) as session:
            prompt = messages[-1]["content"]
            cls._sources = []
            if search_type == "websearch":
                async with session.post(
                    f"{cls.url}/api/ai/rix/search",
                    json={"prompt": prompt},
                    proxy=proxy,
                ) as response:
                    response.raise_for_status()
                    cls._sources = (await response.json())["result"]
            data = {
                "chatId": get_random_hex(),
                "history": messages,
                "prompt": prompt,
                "searchType": search_type,
                "urlToScan": None,
                "searchResults": cls._sources,
            }
            async with session.post(
                f"{cls.url}/api/ai/rix/completion",
                json=data,
                proxy=proxy,
            ) as response:
                response.raise_for_status()
                async for chunk in response.content.iter_any():
                    if chunk:
                        yield chunk.decode()
```

**Purpose**: This method creates an asynchronous generator for retrieving responses from the Hashnode API.

**Parameters**:

- `model` (str): The name of the model (e.g., "text-davinci-003").
- `messages` (Messages): A list of messages in the chat history.
- `search_type` (str): The type of search (e.g., "quick", "code", "websearch"). Defaults to "websearch".
- `proxy` (str, optional): A proxy server to use. Defaults to `None`.
- `**kwargs`: Additional keyword arguments.

**Returns**:

- `AsyncResult`: An asynchronous result with a generator that yields chunks of the response.

**Raises Exceptions**:

- `Exception`: If an error occurred during the API request.

**How the Function Works**:

1. The method creates an `aiohttp.ClientSession` with custom headers.
2. It extracts the last message from the `messages` list.
3. If the `search_type` is "websearch", it performs a web search using the Hashnode API.
4. It constructs a JSON payload with the chat history, prompt, search type, and search results.
5. It sends a POST request to the Hashnode API endpoint `/api/ai/rix/completion` with the payload.
6. The method iterates through the response content and yields each chunk of the response.

**Examples**:

```python
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Hashnode import Hashnode
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Hashnode import SearchTypes
>>> messages = [{"role": "user", "content": "Hello, world!"}]
>>> async_generator = await Hashnode.create_async_generator(model='gpt-3.5-turbo', messages=messages, search_type=SearchTypes.websearch)
>>> async for chunk in async_generator:
...     print(chunk)
...
```

### `get_sources`

```python
    @classmethod
    def get_sources(cls) -> list:
        """
        Возвращает список источников для web-поиска.

        Args:
            None

        Returns:
            list: Список словарей с заголовками и URL-адресами источников.

        Example:
            >>> from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Hashnode import Hashnode
            >>> sources = Hashnode.get_sources()
            >>> print(sources)
        """
        return [
            {
                "title": source["name"],
                "url": source["url"]
            } for source in cls._sources
        ]
```

**Purpose**: This method returns a list of sources used for web searches.

**Parameters**:

- `None`: The method does not take any parameters.

**Returns**:

- `list`: A list of dictionaries containing the titles and URLs of the sources.

**Examples**:

```python
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Hashnode import Hashnode
>>> sources = Hashnode.get_sources()
>>> print(sources)
```

## Parameter Details

- `model` (str): The name of the model to use.
- `messages` (Messages): A list of messages in the chat history.
- `search_type` (str): The type of search to perform.
- `proxy` (str, optional): A proxy server to use.

## Examples

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Hashnode import Hashnode
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Hashnode import SearchTypes

messages = [
    {"role": "user", "content": "Hello, world!"},
]

async_generator = await Hashnode.create_async_generator(
    model='gpt-3.5-turbo',
    messages=messages,
    search_type=SearchTypes.websearch
)

async for chunk in async_generator:
    print(chunk)
```