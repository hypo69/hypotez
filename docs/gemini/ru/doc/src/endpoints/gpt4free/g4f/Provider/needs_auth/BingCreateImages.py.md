# Модуль для создания изображений Bing

## Обзор

Модуль `BingCreateImages.py` предоставляет функциональность для создания изображений с использованием Microsoft Designer в Bing. Он позволяет генерировать изображения на основе текстового запроса (prompt) и возвращает результат в виде markdown-форматированной строки с изображениями. Этот модуль является частью проекта `hypotez` и предназначен для интеграции с другими компонентами, требующими генерации изображений.

## Подробнее

Модуль использует асинхронный подход для создания изображений, что позволяет не блокировать выполнение других задач во время ожидания ответа от сервиса Bing. Он также поддерживает использование cookies и прокси для аутентификации и обхода ограничений сети.

## Классы

### `BingCreateImages`

**Описание**: Класс предоставляет функциональность для создания изображений с использованием Microsoft Designer в Bing.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Добавляет поддержку выбора модели.

**Атрибуты**:
- `label` (str): Метка провайдера ("Microsoft Designer in Bing").
- `url` (str): URL для создания изображений ("https://www.bing.com/images/create").
- `working` (bool): Флаг, указывающий, что провайдер работает (True).
- `needs_auth` (bool): Флаг, указывающий, что требуется аутентификация (True).
- `image_models` (List[str]): Список поддерживаемых моделей изображений (["dall-e-3"]).
- `models` (List[str]): Псевдоним для `image_models`.
- `cookies` (Cookies): Cookies для аутентификации.
- `proxy` (str): Прокси-сервер для использования.
**Параметры**:
   - `cookies` (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
   - `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
   - `api_key` (str, optional): API ключ для аутентификации. По умолчанию `None`.

**Принцип работы**:
1.  При инициализации класса проверяется наличие `api_key`. Если он предоставлен, то он добавляется в cookies под ключом "_U".
2.  Метод `create_async_generator` создает экземпляр класса `BingCreateImages` и вызывает метод `generate` для генерации изображений на основе запроса.
3.  Метод `generate` проверяет наличие cookies и вызывает `create_images` для получения изображений от сервиса Bing.
4.  Результат возвращается в виде объекта `ImageResponse`.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `BingCreateImages`.
- `create_async_generator`: Создает асинхронный генератор для создания изображений.
- `generate`: Генерирует изображения на основе текстового запроса.

## Методы класса

### `__init__`

```python
def __init__(self, cookies: Cookies = None, proxy: str = None, api_key: str = None) -> None
```

**Назначение**: Инициализирует экземпляр класса `BingCreateImages`.

**Параметры**:
- `cookies` (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `api_key` (str, optional): API ключ для аутентификации. Если предоставлен, добавляется в cookies под ключом "_U". По умолчанию `None`.

**Как работает функция**:
- Если передан `api_key`, он добавляется в словарь `cookies` под ключом `_U`. Это необходимо для аутентификации в сервисе Bing.
- Сохраняет переданные значения `cookies` и `proxy` в атрибутах экземпляра класса.

**Примеры**:

```python
from typing import Dict, Optional

# Пример 1: Инициализация без cookies и прокси
bing_images = BingCreateImages()

# Пример 2: Инициализация с cookies
cookies: Dict[str, str] = {"_U": "some_api_key"}
bing_images_with_cookies = BingCreateImages(cookies=cookies)

# Пример 3: Инициализация с прокси
bing_images_with_proxy = BingCreateImages(proxy="http://proxy.example.com")

# Пример 4: Инициализация с api_key
bing_images_with_api_key = BingCreateImages(api_key="some_api_key")

# Пример 5: Инициализация с cookies и прокси
bing_images_with_cookies_and_proxy = BingCreateImages(cookies=cookies, proxy="http://proxy.example.com")
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

**Назначение**: Создает асинхронный генератор для генерации изображений.

**Параметры**:
- `cls` (BingCreateImages): Ссылка на класс.
- `model` (str): Модель для генерации изображений.
- `messages` (Messages): Список сообщений для формирования запроса.
- `prompt` (str, optional): Текстовый запрос для генерации изображений. По умолчанию `None`.
- `api_key` (str, optional): API ключ для аутентификации. По умолчанию `None`.
- `cookies` (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий результаты генерации изображений.

**Как работает функция**:
1.  Создает экземпляр класса `BingCreateImages` с переданными параметрами `cookies`, `proxy` и `api_key`.
2.  Форматирует текстовый запрос, используя функцию `format_image_prompt`.
3.  Вызывает метод `generate` для генерации изображений на основе запроса.
4.  Возвращает асинхронный генератор, который возвращает результат генерации изображений.

**Примеры**:

```python
from typing import List, Dict, AsyncGenerator
from src.endpoints.gpt4free.g4f.typing import Message

# Пример 1: Создание асинхронного генератора с минимальным набором параметров
messages: List[Message] = [{"role": "user", "content": "generate a cat image"}]
async def create_generator():
    generator: AsyncGenerator = BingCreateImages.create_async_generator(
        model="dall-e-3",
        messages=messages
    )
    async for item in generator:
        print(item)
# Пример 2: Создание асинхронного генератора с cookies
cookies: Dict[str, str] = {"_U": "some_api_key"}
async def create_generator_with_cookies():
    generator: AsyncGenerator = BingCreateImages.create_async_generator(
        model="dall-e-3",
        messages=messages,
        cookies=cookies
    )
    async for item in generator:
        print(item)

# Пример 3: Создание асинхронного генератора с prompt и api_key
async def create_generator_with_prompt_and_api_key():
    generator: AsyncGenerator = BingCreateImages.create_async_generator(
        model="dall-e-3",
        messages=messages,
        prompt="A cat with sunglasses",
        api_key="some_api_key"
    )
    async for item in generator:
        print(item)

# Пример 4: Создание асинхронного генератора с proxy
async def create_generator_with_proxy():
    generator: AsyncGenerator = BingCreateImages.create_async_generator(
        model="dall-e-3",
        messages=messages,
        proxy="http://proxy.example.com"
    )
    async for item in generator:
        print(item)

# Пример 5: Создание асинхронного генератора со всеми параметрами
async def create_generator_with_all_params():
    generator: AsyncGenerator = BingCreateImages.create_async_generator(
        model="dall-e-3",
        messages=messages,
        prompt="A cat with sunglasses",
        api_key="some_api_key",
        cookies=cookies,
        proxy="http://proxy.example.com"
    )
    async for item in generator:
        print(item)
```

### `generate`

```python
async def generate(self, prompt: str) -> ImageResponse
```

**Назначение**: Асинхронно создает markdown-форматированную строку с изображениями на основе запроса.

**Параметры**:
- `prompt` (str): Текстовый запрос для генерации изображений.

**Возвращает**:
- `ImageResponse`: Объект, содержащий markdown-форматированную строку с изображениями.

**Вызывает исключения**:
- `MissingAuthError`: Если отсутствует cookie "_U".

**Как работает функция**:
1.  Проверяет наличие cookies в атрибуте `self.cookies`. Если cookies отсутствуют, пытается получить их для домена ".bing.com".
2.  Проверяет наличие cookie "_U" в cookies. Если cookie отсутствует, вызывает исключение `MissingAuthError`.
3.  Создает асинхронную сессию с использованием `create_session` и переданными cookies и прокси.
4.  Вызывает функцию `create_images` для получения изображений от сервиса Bing.
5.  Возвращает объект `ImageResponse`, содержащий изображения и информацию о запросе.

**Примеры**:

```python
import asyncio
from typing import Dict
from src.endpoints.gpt4free.g4f.errors import MissingAuthError

# Пример 1: Генерация изображений с использованием cookies
async def generate_images_with_cookies():
    cookies: Dict[str, str] = {"_U": "some_api_key"}
    bing_images = BingCreateImages(cookies=cookies)
    try:
        image_response = await bing_images.generate(prompt="A cat with sunglasses")
        print(image_response)
    except MissingAuthError as ex:
        print(f"Error: {ex}")

# Пример 2: Генерация изображений с использованием прокси
async def generate_images_with_proxy():
    bing_images = BingCreateImages(proxy="http://proxy.example.com")
    try:
        image_response = await bing_images.generate(prompt="A dog playing guitar")
        print(image_response)
    except MissingAuthError as ex:
        print(f"Error: {ex}")

# Пример 3: Обработка ошибки MissingAuthError
async def generate_images_missing_auth():
    bing_images = BingCreateImages()
    try:
        image_response = await bing_images.generate(prompt="A bird singing a song")
        print(image_response)
    except MissingAuthError as ex:
        print(f"Error: {ex}")

# Запуск асинхронных функций
#asyncio.run(generate_images_with_cookies())
#asyncio.run(generate_images_with_proxy())
#asyncio.run(generate_images_missing_auth())