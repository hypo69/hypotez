# Module BingCreateImages

## Overview

The `BingCreateImages` module is an asynchronous provider for generating images using Microsoft Designer in Bing. It facilitates the creation of images based on a given prompt and returns a markdown-formatted string containing the generated images. This module is part of the `g4f` package within the `hypotez` project, specifically designed to work with image generation services that require authentication.

## More details

This module leverages the `create_images` and `create_session` functions from the `bing.create_images` module to interact with the Bing image creation service. It handles authentication using cookies, including the "_U" cookie, and supports the use of proxies. The module is designed to be used asynchronously, making it suitable for integration into applications that require non-blocking image generation.

## Classes

### `BingCreateImages`

**Description**: This class is an asynchronous provider for generating images using Microsoft Designer in Bing.

**Inherits**:
- `AsyncGeneratorProvider`: Provides asynchronous generation capabilities.
- `ProviderModelMixin`: Provides a mixin for provider model functionality.

**Attributes**:
- `label` (str): The label of the provider, set to "Microsoft Designer in Bing".
- `url` (str): The URL of the Bing image creation service, set to "https://www.bing.com/images/create".
- `working` (bool): A flag indicating whether the provider is working, set to `True`.
- `needs_auth` (bool): A flag indicating whether the provider needs authentication, set to `True`.
- `image_models` (List[str]): A list of supported image models, set to `["dall-e-3"]`.
- `models` (List[str]): An alias for `image_models`.
- `cookies` (Cookies): Cookies for authentication.
- `proxy` (str): Proxy server address for requests.

**Working principle**:
The `BingCreateImages` class initializes with cookies and a proxy, if provided. The `create_async_generator` method is a class method that creates an instance of `BingCreateImages` and yields the result of the `generate` method. The `generate` method handles the actual image generation process by creating a session with the Bing service, calling the `create_images` function, and returning a markdown-formatted string containing the generated images.

**Methods**:
- `__init__`: Initializes the `BingCreateImages` class.
- `create_async_generator`: Creates an asynchronous generator for image generation.
- `generate`: Generates images based on the prompt.

### `__init__`

```python
def __init__(self, cookies: Cookies = None, proxy: str = None, api_key: str = None) -> None
```

Инициализирует экземпляр класса `BingCreateImages`.

**Parameters**:
- `cookies` (Cookies, optional): Куки для аутентификации. По умолчанию `None`.
- `proxy` (str, optional): Адрес прокси-сервера для запросов. По умолчанию `None`.
- `api_key` (str, optional): Ключ API для аутентификации. Если предоставлен, добавляет его в куки "_U". По умолчанию `None`.

**How the function works**:
Функция инициализирует класс `BingCreateImages`, устанавливая куки и прокси. Если предоставлен `api_key`, он добавляется в куки "_U".

**Examples**:
```python
# Пример инициализации с куки и прокси
cookies = {"_U": "some_api_key"}
bing_images = BingCreateImages(cookies=cookies, proxy="http://proxy.example.com")

# Пример инициализации только с ключом API
bing_images = BingCreateImages(api_key="some_api_key")
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    prompt: str = None,
    api_key: str = None,
    cookies: Cookies = None,
    proxy: str = None,
    **kwargs
) -> AsyncResult
```

Создает асинхронный генератор для генерации изображений.

**Parameters**:
- `cls`: Ссылка на класс.
- `model` (str): Модель для генерации изображений.
- `messages` (Messages): Сообщения для формирования запроса.
- `prompt` (str, optional): Дополнительный запрос для генерации изображений. По умолчанию `None`.
- `api_key` (str, optional): Ключ API для аутентификации. По умолчанию `None`.
- `cookies` (Cookies, optional): Куки для аутентификации. По умолчанию `None`.
- `proxy` (str, optional): Адрес прокси-сервера для запросов. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Returns**:
- `AsyncResult`: Асинхронный генератор, возвращающий результаты генерации изображений.

**How the function works**:
Функция создает экземпляр класса `BingCreateImages` и вызывает метод `generate` для генерации изображений. Результат возвращается в виде асинхронного генератора.

**Examples**:
```python
# Пример создания асинхронного генератора
async for result in BingCreateImages.create_async_generator(
    model="dall-e-3",
    messages=[{"role": "user", "content": "generate a cat image"}],
    api_key="some_api_key"
):
    print(result)
```

### `generate`

```python
async def generate(self, prompt: str) -> ImageResponse
```

Асинхронно создает строку в формате Markdown с изображениями на основе запроса.

**Parameters**:
- `prompt` (str): Запрос для генерации изображений.

**Returns**:
- `ImageResponse`: Объект `ImageResponse`, содержащий сгенерированные изображения и метаданные.

**Raises**:
- `MissingAuthError`: Если отсутствует куки "_U".

**How the function works**:
Функция проверяет наличие куки "_U" и создает сессию с Bing с использованием предоставленных куки и прокси. Затем вызывается функция `create_images` для генерации изображений на основе запроса. Возвращается объект `ImageResponse`, содержащий сгенерированные изображения и URL для предпросмотра.

**Examples**:
```python
# Пример генерации изображений
bing_images = BingCreateImages(cookies={"_U": "some_api_key"})
image_response = await bing_images.generate(prompt="generate a cat image")
print(image_response)
```