# Модуль `You.py`

## Обзор

Модуль предоставляет асинхронный генератор для взаимодействия с сервисом You.com, включая поддержку текстовых и визуальных запросов. Он содержит класс `You`, который позволяет отправлять запросы к различным моделям, включая GPT-4o, Claude 3 и другие, а также генерировать изображения с использованием DALL-E.

## Подробней

Этот модуль является частью проекта `hypotez` и предназначен для интеграции с сервисом You.com. Он обеспечивает возможность отправки текстовых и визуальных запросов к различным моделям, поддерживаемым You.com, таким как GPT-4o, Claude 3 и DALL-E. Модуль использует асинхронные запросы для обеспечения высокой производительности и поддерживает потоковую передачу данных для обработки больших объемов информации.

## Классы

### `You`

**Описание**: Класс для взаимодействия с сервисом You.com. Поддерживает текстовые и визуальные запросы к различным моделям.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию результатов.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера ("You.com").
- `url` (str): URL сервиса You.com ("https://you.com").
- `working` (bool): Указывает, что провайдер работает (True).
- `default_model` (str): Модель, используемая по умолчанию ("gpt-4o-mini").
- `default_vision_model` (str): Модель для обработки изображений по умолчанию ("agent").
- `image_models` (list[str]): Список моделей для генерации изображений (["dall-e"]).
- `models` (list[str]): Список поддерживаемых моделей.
- `_cookies` (None): Куки, используемые для запросов.
- `_cookies_used` (int): Количество использованных куки.
- `_telemetry_ids` (list): Список идентификаторов телеметрии.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для отправки запросов.
- `upload_file`: Загружает файл на сервер You.com.

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
        """Создает асинхронный генератор для отправки запросов к сервису You.com.

        Args:
            model (str): Модель для использования.
            messages (Messages): Список сообщений для отправки.
            stream (bool, optional): Использовать ли потоковую передачу данных. По умолчанию True.
            image (ImageType, optional): Изображение для отправки. По умолчанию None.
            image_name (str, optional): Имя файла изображения. По умолчанию None.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию None.
            timeout (int, optional): Время ожидания запроса в секундах. По умолчанию 240.
            chat_mode (str, optional): Режим чата. По умолчанию "default".
            cookies (Cookies, optional): Куки для использования. По умолчанию None.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор для получения результатов.

        Raises:
            ResponseError: Если возникает ошибка при получении ответа от сервера.
        """
        ...
```

**Назначение**: Создает асинхронный генератор для отправки запросов к сервису You.com.

**Параметры**:
- `cls`: Ссылка на класс.
- `model` (str): Модель для использования.
- `messages` (Messages): Список сообщений для отправки.
- `stream` (bool, optional): Использовать ли потоковую передачу данных. По умолчанию `True`.
- `image` (ImageType, optional): Изображение для отправки. По умолчанию `None`.
- `image_name` (str, optional): Имя файла изображения. По умолчанию `None`.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `timeout` (int, optional): Время ожидания запроса в секундах. По умолчанию `240`.
- `chat_mode` (str, optional): Режим чата. По умолчанию `"default"`.
- `cookies` (Cookies, optional): Куки для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор для получения результатов.

**Как работает функция**:
1. Определяет режим чата в зависимости от наличия изображения и выбранной модели.
2. Получает куки из файла или с помощью веб-драйвера, если они не предоставлены.
3. Создает сессию с использованием `StreamSession` и отправляет запрос к сервису You.com.
4. Обрабатывает ответ от сервера, извлекая данные и генерируя результаты.
5. В случае ошибок поднимает исключение `ResponseError`.

**Примеры**:

```python
# Пример использования create_async_generator
messages = [{"role": "user", "content": "Hello, how are you?"}]
generator = await You.create_async_generator(model="gpt-4o-mini", messages=messages)
async for message in generator:
    print(message)
```

### `upload_file`

```python
    @classmethod
    async def upload_file(cls, client: StreamSession, cookies: Cookies, file: bytes, filename: str = None) -> dict:
        """Загружает файл на сервер You.com.

        Args:
            client (StreamSession): Клиент для отправки запросов.
            cookies (Cookies): Куки для использования.
            file (bytes): Файл для загрузки в виде байтов.
            filename (str, optional): Имя файла. По умолчанию None.

        Returns:
            dict: Результат загрузки файла.

        Raises:
            ResponseError: Если возникает ошибка при загрузке файла.
        """
        ...
```

**Назначение**: Загружает файл на сервер You.com.

**Параметры**:
- `cls`: Ссылка на класс.
- `client` (StreamSession): Клиент для отправки запросов.
- `cookies` (Cookies): Куки для использования.
- `file` (bytes): Файл для загрузки в виде байтов.
- `filename` (str, optional): Имя файла. По умолчанию `None`.

**Возвращает**:
- `dict`: Результат загрузки файла.

**Как работает функция**:
1. Получает nonce (одноразовый код) для загрузки файла.
2. Формирует данные для отправки файла, включая имя файла и тип контента.
3. Отправляет POST-запрос на сервер You.com с файлом и nonce.
4. Обрабатывает ответ от сервера и возвращает результат загрузки.
5. В случае ошибок поднимает исключение `ResponseError`.

**Примеры**:

```python
# Пример использования upload_file
import asyncio
from aiohttp import ClientSession

async def main():
    file_path = "image.png"
    with open(file_path, "rb") as f:
        file_bytes = f.read()

    async with ClientSession() as session:
        result = await You.upload_file(session, {}, file_bytes, filename=file_path)
        print(result)

if __name__ == "__main__":
    asyncio.run(main())