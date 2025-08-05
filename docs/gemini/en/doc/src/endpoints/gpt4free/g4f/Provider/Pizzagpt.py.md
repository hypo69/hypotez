# Pizzagpt Provider

## Overview

This module implements the `Pizzagpt` class, which represents a provider for the Pizzagpt API. 

## Details

The `Pizzagpt` class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`, enabling it to work with asynchronous generators and to manage different models.

Pizzagpt API:

* `url`: Base URL for Pizzagpt API endpoint.
* `api_endpoint`: Endpoint for chat completion requests. 
* `models`: A list of supported models, including the default `gpt-4o-mini`.

The `create_async_generator` class method is responsible for generating asynchronous responses from the API. It constructs the API request based on provided messages and a chosen model.

## Classes

### `Pizzagpt`

**Description**: This class represents a provider for the Pizzagpt API.

**Inherits**: 
* `AsyncGeneratorProvider`: Base class for providers that work with asynchronous generators.
* `ProviderModelMixin`: Base class for managing models.

**Attributes**:
* `url`: Base URL for Pizzagpt API endpoint.
* `api_endpoint`: Endpoint for chat completion requests.
* `working`: A flag indicating whether the provider is currently working.
* `default_model`: Default model to use if none is specified.
* `models`: A list of supported models.

**Methods**:
* `create_async_generator()`: Creates an asynchronous generator that yields responses from the Pizzagpt API.


## Class Methods

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор, который выдает ответы от Pizzagpt API.

        Args:
            model (str): Имя модели (например, 'gpt-4o-mini').
            messages (Messages): Сообщения, которые необходимо отправить в API.
            proxy (str, optional): Прокси-сервер для API запроса. Defaults to None.
            kwargs: Дополнительные аргументы для API запроса.

        Returns:
            AsyncResult: Асинхронный результат.

        Raises:
            ValueError: Если в ответе API обнаружится ошибка.
        """
        headers = {
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": cls.url,
            "referer": f"{cls.url}/en",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "x-secret": "Marinara"
        }
        async with ClientSession(headers=headers) as session:
            prompt = format_prompt(messages)
            data = {
                "question": prompt
            }
            async with session.post(f"{cls.url}{cls.api_endpoint}", json=data, proxy=proxy) as response:
                response.raise_for_status()
                response_json = await response.json()
                content = response_json.get("answer", response_json).get("content")
                if content:
                    if "Misuse detected. please get in touch" in content:
                        raise ValueError(content)
                    yield content
                    yield FinishReason("stop")
```

**Purpose**: This method handles the asynchronous interaction with the Pizzagpt API.

**Parameters**:

* `model` (str): Name of the model to use for the request.
* `messages` (Messages): Messages to send to the API.
* `proxy` (str, optional): Proxy server for the API request. Defaults to None.
* `kwargs`: Additional arguments for the API request.

**Returns**:

* `AsyncResult`: Asynchronous result object.

**Raises Exceptions**:

* `ValueError`: If there is an error in the API response.

**How the Function Works**:

1. Constructs the API request headers.
2. Creates a client session with the specified headers.
3. Formats the prompt from the messages provided.
4. Sends a POST request to the Pizzagpt API with the formatted prompt and additional data.
5. Raises an exception if the API request fails.
6. Retrieves the response content from the JSON response.
7. Checks for errors in the API response.
8. Yields the response content and `FinishReason` for stopping the generator.

**Examples**:

```python
async def example_usage():
    # Example messages for the API request
    messages = [
        {"role": "user", "content": "Hello, world!"},
    ]

    # Create an asynchronous generator for the Pizzagpt API
    async_generator = await Pizzagpt.create_async_generator(model='gpt-4o-mini', messages=messages)

    # Iterate over the generator and print the responses
    async for response in async_generator:
        print(f"API Response: {response}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage())