# Poe Provider

## Overview

This module defines the `Poe` class, a provider class for interacting with the Poe platform and its available AI models. 

## Details

The `Poe` class inherits from the `AbstractProvider` class and provides functionality for generating text completions using various AI models available on Poe. It supports both streaming and non-streaming responses.

## Classes

### `class Poe(AbstractProvider)`

**Description**: This class represents the `Poe` provider for accessing AI models on the Poe platform.

**Inherits**: `AbstractProvider`

**Attributes**:

- `url` (str): Base URL for the Poe platform.
- `working` (bool): Flag indicating whether the provider is currently working.
- `needs_auth` (bool): Flag indicating whether the provider requires authentication.
- `supports_stream` (bool): Flag indicating whether the provider supports streaming responses.
- `models` (set): Set of supported models on the Poe platform.

**Methods**:

- `create_completion(model: str, messages: Messages, stream: bool, proxy: str = None, webdriver: WebDriver = None, user_data_dir: str = None, headless: bool = True, **kwargs) -> CreateResult`

## Class Methods

### `create_completion`

```python
    @classmethod
    def create_completion(
        cls,
        model: str,
        messages: Messages,
        stream: bool,
        proxy: str = None,
        webdriver: WebDriver = None,
        user_data_dir: str = None,
        headless: bool = True,
        **kwargs
    ) -> CreateResult:
        """
        Создает завершение с помощью модели Poe.

        Args:
            model (str): Имя модели, которую нужно использовать для создания завершения.
            messages (Messages): Список сообщений, которые необходимо передать в качестве контекста для модели.
            stream (bool): Флаг, указывающий, нужно ли использовать потоковую передачу ответов.
            proxy (str, optional): Прокси-сервер для использования при подключении к Poe. Defaults to `None`.
            webdriver (WebDriver, optional): Экземпляр веб-драйвера для взаимодействия с Poe. Defaults to `None`.
            user_data_dir (str, optional): Путь к каталогу с пользовательскими данными для веб-драйвера. Defaults to `None`.
            headless (bool, optional): Флаг, указывающий, нужно ли запускать веб-драйвер в безголовом режиме. Defaults to `True`.

        Returns:
            CreateResult: Результат создания завершения.

        Raises:
            ValueError: Если модель не поддерживается.
            RuntimeError: Если не удается найти поле ввода запроса.

        Example:
            >>> from hypotez.src.endpoints.gpt4free.g4f.Provider.Poe import Poe
            >>> from hypotez.src.endpoints.gpt4free.g4f.Provider.helper import Messages
            >>> model = 'gpt-3.5-turbo'
            >>> messages = Messages([{'role': 'user', 'content': 'Hello, world!'}]
            >>> result = Poe.create_completion(model=model, messages=messages, stream=False)
            >>> print(result.content)
            Hello, world!
        """
        ...
```

**Purpose**: This method handles the process of generating text completions using the selected model on Poe.

**Parameters**:

- `model` (str): The name of the AI model to be used for text generation.
- `messages` (Messages): A list of messages representing the conversation context.
- `stream` (bool): Flag indicating whether to stream the responses.
- `proxy` (str, optional): Proxy server for connecting to Poe. Defaults to `None`.
- `webdriver` (WebDriver, optional): Webdriver instance for interacting with Poe. Defaults to `None`.
- `user_data_dir` (str, optional): Path to user data directory for the webdriver. Defaults to `None`.
- `headless` (bool, optional): Flag indicating whether to run the webdriver in headless mode. Defaults to `True`.

**Returns**:

- `CreateResult`: The result of creating the completion, including the generated text and other metadata.

**Raises Exceptions**:

- `ValueError`: If the specified model is not supported by Poe.
- `RuntimeError`: If the prompt textarea cannot be found on the Poe website.

**How the Function Works**:

1.  It validates the provided `model` and checks if it is supported.
2.  It formats the `messages` into a prompt string.
3.  It initializes a `WebDriverSession` object to handle web interactions.
4.  It opens the Poe website and navigates to the page of the chosen model.
5.  It waits for the prompt textarea to become visible.
6.  It types the formatted prompt into the textarea and clicks the send button.
7.  It uses JavaScript to monitor the response and yields chunks of text as they become available.

**Examples**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.Poe import Poe
from hypotez.src.endpoints.gpt4free.g4f.Provider.helper import Messages

# Example 1: Generating a completion with GPT-3.5-turbo
model = 'gpt-3.5-turbo'
messages = Messages([{'role': 'user', 'content': 'Hello, world!'}]
result = Poe.create_completion(model=model, messages=messages, stream=False)
print(result.content)

# Example 2: Generating a streaming completion with Llama-2-7b
model = 'meta-llama/Llama-2-7b-chat-hf'
messages = Messages([{'role': 'user', 'content': 'Write a poem about a cat.'}]
for chunk in Poe.create_completion(model=model, messages=messages, stream=True):
    print(chunk, end='')
```