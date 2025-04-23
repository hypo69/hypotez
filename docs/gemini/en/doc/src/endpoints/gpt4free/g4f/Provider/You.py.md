# Модуль `You.py`

## Обзор

Модуль `You.py` предназначен для взаимодействия с сервисом You.com. Он предоставляет асинхронный генератор для обработки текстовых и визуальных запросов с использованием различных моделей, включая `gpt-4o-mini`, `dall-e` и другие. Модуль поддерживает потоковую передачу данных, загрузку изображений и управление cookie для обеспечения стабильной работы с API You.com.

## Детали

Модуль содержит класс `You`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`. Он обеспечивает асинхронную генерацию ответов на основе предоставленных сообщений и моделей. Класс также поддерживает загрузку изображений и управление cookie для взаимодействия с API You.com.

## Классы

### `You`

**Описание**: Класс для взаимодействия с сервисом You.com.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера ("You.com").
- `url` (str): URL сервиса You.com ("https://you.com").
- `working` (bool): Флаг, указывающий на работоспособность провайдера (True).
- `default_model` (str): Модель, используемая по умолчанию ("gpt-4o-mini").
- `default_vision_model` (str): Модель для обработки изображений по умолчанию ("agent").
- `image_models` (List[str]): Список поддерживаемых моделей для работы с изображениями (["dall-e"]).
- `models` (List[str]): Список всех поддерживаемых моделей.
- `_cookies` (Optional[Cookies]): Cookie для работы с сервисом.
- `_cookies_used` (int): Счетчик использованных cookie.
- `_telemetry_ids` (List[Any]): Список идентификаторов телеметрии.

**Принцип работы**:
Класс `You` предоставляет интерфейс для отправки запросов к сервису You.com и получения ответов в асинхронном режиме. Он поддерживает различные режимы работы, включая текстовые запросы, запросы с изображениями и генерацию изображений. Класс также управляет cookie для обеспечения стабильного соединения с сервисом.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от сервиса You.com.
- `upload_file`: Загружает файл на сервис You.com.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    stream: bool = True,
    image: ImageType = None,
    image_name: str = None,
    proxy: str = None,
    timeout: int = 240,
    chat_mode: str = "default",
    cookies: Cookies = None,
    **kwargs,
) -> AsyncResult:
    """
    Создает асинхронный генератор для получения ответов от сервиса You.com.

    Args:
        cls (You): Класс `You`.
        model (str): Используемая модель.
        messages (Messages): Список сообщений для отправки.
        stream (bool): Флаг для потоковой передачи данных (по умолчанию True).
        image (ImageType): Изображение для отправки (по умолчанию None).
        image_name (str): Имя файла изображения (по умолчанию None).
        proxy (str): Прокси-сервер для использования (по умолчанию None).
        timeout (int): Время ожидания ответа в секундах (по умолчанию 240).
        chat_mode (str): Режим чата ("default", "agent", "create", "custom").
        cookies (Cookies): Cookie для использования (по умолчанию None).
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от сервиса You.com.

    Raises:
        MissingRequirementsError: Если отсутствуют необходимые cookie и не удается получить их автоматически.
        ResponseError: Если получен ответ с ошибкой от сервиса You.com.

    Как работает функция:
    - Определяет режим чата в зависимости от наличия изображения и выбранной модели.
    - Получает cookie, если они не предоставлены и режим чата не "default".
    - Создает сессию с использованием `StreamSession` для асинхронного взаимодействия с сервисом.
    - Загружает изображение, если оно предоставлено.
    - Формирует заголовки и данные для запроса.
    - Отправляет запрос к API `streamingSearch` и обрабатывает ответы, возвращая их через генератор.
    """
    ...
```

### `upload_file`

```python
@classmethod
async def upload_file(cls, client: StreamSession, cookies: Cookies, file: bytes, filename: str = None) -> dict:
    """
    Загружает файл на сервис You.com.

    Args:
        cls (You): Класс `You`.
        client (StreamSession): Асинхронная сессия для отправки запросов.
        cookies (Cookies): Cookie для использования.
        file (bytes): Файл для загрузки в виде байтов.
        filename (str): Имя файла (по умолчанию None).

    Returns:
        dict: Словарь с результатами загрузки файла.

    Raises:
        ResponseError: Если получен ответ с ошибкой от сервиса You.com.

    Как работает функция:
    - Получает nonce для загрузки файла.
    - Формирует данные формы для загрузки файла.
    - Отправляет POST-запрос к API `upload` с файлом и заголовками.
    - Обрабатывает ответ и возвращает результаты.
    """
    ...
```

## Параметры класса

- `label` (str): Метка провайдера ("You.com").
- `url` (str): URL сервиса You.com ("https://you.com").
- `working` (bool): Флаг, указывающий на работоспособность провайдера (True).
- `default_model` (str): Модель, используемая по умолчанию ("gpt-4o-mini").
- `default_vision_model` (str): Модель для обработки изображений по умолчанию ("agent").
- `image_models` (List[str]): Список поддерживаемых моделей для работы с изображениями (["dall-e"]).
- `models` (List[str]): Список всех поддерживаемых моделей.
- `_cookies` (Optional[Cookies]): Cookie для работы с сервисом.
- `_cookies_used` (int): Счетчик использованных cookie.
- `_telemetry_ids` (List[Any]): Список идентификаторов телеметрии.

## Примеры

Пример использования класса `You` для создания асинхронного генератора:

```python
from src.endpoints.gpt4free.g4f.Provider.You import You
from src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [{"role": "user", "content": "Hello, world!"}]
model = "gpt-4o-mini"

async def main():
    generator = await You.create_async_generator(model=model, messages=messages)
    async for message in generator:
        print(message)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

Пример загрузки изображения с использованием класса `You`:

```python
from src.endpoints.gpt4free.g4f.Provider.You import You
from src.endpoints.gpt4free.g4f.requests import StreamSession
from src.endpoints.gpt4free.g4f.typing import Cookies

async def main():
    client = StreamSession()
    cookies: Cookies = {}
    file = b"example image data"
    filename = "image.jpg"
    result = await You.upload_file(client=client, cookies=cookies, file=file, filename=filename)
    print(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```