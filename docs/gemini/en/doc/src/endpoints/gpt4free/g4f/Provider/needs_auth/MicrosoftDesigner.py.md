# Module MicrosoftDesigner

## Overview

The module `MicrosoftDesigner` implements an asynchronous provider for generating images using the Microsoft Designer service. It supports different image models and handles authentication using HAR files or by fetching an access token and user agent through a browser.

## More details

This module is designed to interact with the Microsoft Designer API to create images from textual prompts. It is used within the `hypotez` project to provide image generation capabilities. The module supports different image models and handles the authentication process, which can involve reading HAR files or using a browser to obtain an access token.

## Classes

### `MicrosoftDesigner`

**Description**: The class `MicrosoftDesigner` is an asynchronous provider for generating images using the Microsoft Designer service.

**Inherits**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Attributes**:
- `label` (str): The label of the provider, set to "Microsoft Designer".
- `url` (str): The URL of the Microsoft Designer service, set to "https://designer.microsoft.com".
- `working` (bool): A flag indicating whether the provider is currently working, set to `True`.
- `use_nodriver` (bool): A flag indicating whether the provider uses a browser-less setup, set to `True`.
- `needs_auth` (bool): A flag indicating whether authentication is required, set to `True`.
- `default_image_model` (str): The default image model, set to "dall-e-3".
- `image_models` (list): A list of supported image models, including "dall-e-3", "1024x1024", "1024x1792", and "1792x1024".
- `models` (list): An alias for `image_models`.

**Working principle**:
The `MicrosoftDesigner` class inherits from `AsyncGeneratorProvider` and `ProviderModelMixin`, providing the structure for asynchronous image generation. It handles authentication, image size selection, and interaction with the Microsoft Designer API.

**Methods**:
- `create_async_generator`: Creates an asynchronous generator for generating images.
- `generate`: Generates images based on a prompt and image size.

## Class Methods

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    prompt: str = None,
    proxy: str = None,
    **kwargs
) -> AsyncResult:
    """ Создает асинхронный генератор для генерации изображений.

    Args:
        cls (MicrosoftDesigner): Класс MicrosoftDesigner.
        model (str): Модель изображения для использования ("dall-e-3", "1024x1024", "1024x1792", "1792x1024").
        messages (Messages): Список сообщений для формирования запроса.
        prompt (str, optional): Текст запроса. По умолчанию `None`.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.

    Returns:
        AsyncResult: Асинхронный результат, который является генератором изображений.
    """
    ...
```

**Purpose**: Creates an asynchronous generator that yields image responses based on the provided model, messages, prompt, and proxy.

**Parameters**:
- `cls` (MicrosoftDesigner): The class `MicrosoftDesigner`.
- `model` (str): The image model to use (e.g., "dall-e-3", "1024x1024").
- `messages` (Messages): A list of messages to format the prompt.
- `prompt` (str, optional): The text prompt. Defaults to `None`.
- `proxy` (str, optional): The proxy server URL. Defaults to `None`.
- `**kwargs`: Additional keyword arguments.

**Returns**:
- `AsyncResult`: An asynchronous result, which is an image generator.

**How the function works**:
The function selects the image size based on the provided model and yields the result of the `generate` method, which performs the actual image generation.

**Examples**:
```python
# Example of calling create_async_generator
model = "1024x1024"
messages = [{"role": "user", "content": "Generate an image of a cat"}]
prompt = "A cat"
proxy = None
generator = await MicrosoftDesigner.create_async_generator(model, messages, prompt, proxy)
```

### `generate`

```python
@classmethod
async def generate(cls, prompt: str, image_size: str, proxy: str = None) -> ImageResponse:
    """ Генерирует изображения на основе запроса и размера изображения.

    Args:
        cls (MicrosoftDesigner): Класс MicrosoftDesigner.
        prompt (str): Текст запроса для генерации изображения.
        image_size (str): Размер изображения ("1024x1024", "1024x1792", "1792x1024").
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.

    Returns:
        ImageResponse: Объект ImageResponse, содержащий сгенерированные изображения.

    Raises:
        NoValidHarFileError: Если не найден действительный HAR-файл.
    """
    ...
```

**Purpose**: Generates images based on the provided prompt and image size.

**Parameters**:
- `cls` (MicrosoftDesigner): The class `MicrosoftDesigner`.
- `prompt` (str): The text prompt for image generation.
- `image_size` (str): The image size (e.g., "1024x1024").
- `proxy` (str, optional): The proxy server URL. Defaults to `None`.

**Returns**:
- `ImageResponse`: An `ImageResponse` object containing the generated images.

**Raises**:
- `NoValidHarFileError`: If no valid HAR file is found.

**How the function works**:
The function first tries to read authentication details from a HAR file. If that fails, it attempts to fetch an access token and user agent using a browser. It then calls the `create_images` function to generate the images and returns an `ImageResponse` object.

**Examples**:
```python
# Example of calling generate
prompt = "A futuristic city"
image_size = "1024x1024"
proxy = None
image_response = await MicrosoftDesigner.generate(prompt, image_size, proxy)
```

## Functions

### `create_images`

```python
async def create_images(prompt: str, access_token: str, user_agent: str, image_size: str, proxy: str = None, seed: int = None):
    """ Создает изображения с использованием API Microsoft Designer.

    Args:
        prompt (str): Текст запроса для генерации изображения.
        access_token (str): Токен доступа для аутентификации.
        user_agent (str): User-Agent для HTTP-запросов.
        image_size (str): Размер изображения ("1024x1024", "1024x1792", "1792x1024").
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        seed (int, optional): Зерно для случайной генерации. По умолчанию `None`.

    Returns:
        list[str]: Список URL-адресов сгенерированных изображений.
    """
    ...
```

**Purpose**: Creates images using the Microsoft Designer API.

**Parameters**:
- `prompt` (str): The text prompt for image generation.
- `access_token` (str): The access token for authentication.
- `user_agent` (str): The User-Agent string for HTTP requests.
- `image_size` (str): The image size (e.g., "1024x1024").
- `proxy` (str, optional): The proxy server URL. Defaults to `None`.
- `seed` (int, optional): The seed for random generation. Defaults to `None`.

**Returns**:
- `list[str]`: A list of generated image URLs.

**How the function works**:
The function constructs a POST request to the Microsoft Designer API with the provided parameters, including the prompt, access token, and image size. It polls the API until the images are generated and returns a list of image URLs.

**Examples**:
```python
# Example of calling create_images
prompt = "A landscape with mountains"
access_token = "example_access_token"
user_agent = "Example User Agent"
image_size = "1024x1024"
proxy = None
images = await create_images(prompt, access_token, user_agent, image_size, proxy)
```

### `readHAR`

```python
def readHAR(url: str) -> tuple[str, str]:
    """ Читает HAR-файлы для извлечения токена доступа и User-Agent.

    Args:
        url (str): URL для поиска в HAR-файлах.

    Returns:
        tuple[str, str]: Кортеж, содержащий токен доступа и User-Agent.

    Raises:
        NoValidHarFileError: Если токен доступа не найден в HAR-файлах.
    """
    ...
```

**Purpose**: Reads HAR files to extract the access token and User-Agent.

**Parameters**:
- `url` (str): The URL to search for in the HAR files.

**Returns**:
- `tuple[str, str]`: A tuple containing the access token and User-Agent.

**Raises**:
- `NoValidHarFileError`: If no access token is found in the HAR files.

**How the function works**:
The function iterates through HAR files, searches for a matching URL, and extracts the access token and User-Agent from the request headers.

**Examples**:
```python
# Example of calling readHAR
url = "https://designerapp.officeapps.live.com"
access_token, user_agent = readHAR(url)
```

### `get_access_token_and_user_agent`

```python
async def get_access_token_and_user_agent(url: str, proxy: str = None):
    """ Получает токен доступа и User-Agent с использованием браузера.

    Args:
        url (str): URL для посещения в браузере.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.

    Returns:
        tuple[str, str]: Кортеж, содержащий токен доступа и User-Agent.
    """
    ...
```

**Purpose**: Gets the access token and User-Agent using a browser.

**Parameters**:
- `url` (str): The URL to visit in the browser.
- `proxy` (str, optional): The proxy server URL. Defaults to `None`.

**Returns**:
- `tuple[str, str]`: A tuple containing the access token and User-Agent.

**How the function works**:
The function launches a browser, navigates to the specified URL, extracts the User-Agent, and retrieves the access token from local storage.

**Examples**:
```python
# Example of calling get_access_token_and_user_agent
url = "https://designer.microsoft.com"
access_token, user_agent = await get_access_token_and_user_agent(url, proxy)
```