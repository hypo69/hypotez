# Модуль AiChatOnline

## Обзор

Модуль `AiChatOnline` предоставляет асинхронный интерфейс для взаимодействия с сервисом AiChatOnline. Он позволяет генерировать ответы на основе предоставленных сообщений, используя асинхронные генераторы. Модуль использует `aiohttp` для выполнения HTTP-запросов и предоставляет функциональность для получения токена и форматирования запросов.

## Подробней

Этот модуль предназначен для работы с сервисом AiChatOnline через его API. Он включает в себя функции для получения уникального идентификатора пользователя (`grab_token`) и создания асинхронного генератора (`create_async_generator`) для получения ответов от модели.

## Классы

### `AiChatOnline`

**Описание**: Класс `AiChatOnline` является подклассом `AsyncGeneratorProvider` и `ProviderModelMixin`. Он предоставляет методы для взаимодействия с API AiChatOnline и получения ответов в асинхронном режиме.

**Принцип работы**:
Класс использует асинхронные запросы для взаимодействия с API AiChatOnline. Он получает уникальный идентификатор пользователя, формирует запрос с использованием предоставленных сообщений и возвращает асинхронный генератор, который выдает чанки ответа.

**Атрибуты**:
- `site_url` (str): URL сайта AiChatOnline.
- `url` (str): URL API AiChatOnline.
- `api_endpoint` (str): Endpoint API для чата.
- `working` (bool): Указывает, работает ли провайдер.
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4o-mini`).

**Методы**:
- `grab_token`: Получает уникальный идентификатор пользователя.
- `create_async_generator`: Создает асинхронный генератор для получения ответов от модели.

## Функции

### `grab_token`

```python
    @classmethod
    async def grab_token(
        cls,
        session: ClientSession,
        proxy: str
    ) -> str:
        """
        Асинхронно получает уникальный идентификатор пользователя от AiChatOnline.

        Args:
            cls (AiChatOnline): Ссылка на класс.
            session (ClientSession): Асинхронная HTTP-сессия для выполнения запросов.
            proxy (str): URL прокси-сервера для использования при запросе.

        Returns:
            str: Уникальный идентификатор пользователя, полученный из ответа API.

        Raises:
            aiohttp.ClientResponseError: Если HTTP-запрос завершается с ошибкой.

        Пример:
            >>> async with aiohttp.ClientSession() as session:
            ...     token = await AiChatOnline.grab_token(session, 'http://proxy:8080')
            ...     print(token)
            'unique_id'
        """
```

**Назначение**: Функция `grab_token` асинхронно получает уникальный идентификатор пользователя, необходимый для взаимодействия с API AiChatOnline.

**Параметры**:
- `cls` (AiChatOnline): Ссылка на класс.
- `session` (ClientSession): Асинхронная HTTP-сессия для выполнения запросов.
- `proxy` (str): URL прокси-сервера для использования при запросе.

**Возвращает**:
- `str`: Уникальный идентификатор пользователя, полученный из ответа API.

**Вызывает исключения**:
- `aiohttp.ClientResponseError`: Если HTTP-запрос завершается с ошибкой.

**Как работает функция**:

1. Функция отправляет GET-запрос к API AiChatOnline для получения уникального идентификатора пользователя.
2. Проверяет статус ответа и вызывает исключение `aiohttp.ClientResponseError` в случае ошибки.
3. Извлекает идентификатор пользователя из JSON-ответа и возвращает его.

```
A: Отправка GET-запроса к API AiChatOnline
|
B: Проверка статуса ответа
|
C: Извлечение идентификатора пользователя из JSON-ответа
|
D: Возврат идентификатора пользователя
```

**Примеры**:

```python
async with aiohttp.ClientSession() as session:
    token = await AiChatOnline.grab_token(session, 'http://proxy:8080')
    print(token)
# => 'unique_id'
```

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
        Создает асинхронный генератор для получения ответов от модели AiChatOnline.

        Args:
            cls (AiChatOnline): Ссылка на класс.
            model (str): Название модели для использования.
            messages (Messages): Список сообщений для отправки в API.
            proxy (str, optional): URL прокси-сервера для использования при запросе. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, выдающий чанки ответа от модели.

        Raises:
            aiohttp.ClientResponseError: Если HTTP-запрос завершается с ошибкой.

        Пример:
            >>> messages = [{'role': 'user', 'content': 'Hello, world!'}]
            >>> async for chunk in AiChatOnline.create_async_generator('gpt-4o-mini', messages, proxy='http://proxy:8080'):
            ...     print(chunk)
            'Hello'
            ', '
            'world'
            '!'
        """
```

**Назначение**: Функция `create_async_generator` создает асинхронный генератор для получения ответов от модели AiChatOnline.

**Параметры**:
- `cls` (AiChatOnline): Ссылка на класс.
- `model` (str): Название модели для использования.
- `messages` (Messages): Список сообщений для отправки в API.
- `proxy` (str, optional): URL прокси-сервера для использования при запросе. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, выдающий чанки ответа от модели.

**Вызывает исключения**:
- `aiohttp.ClientResponseError`: Если HTTP-запрос завершается с ошибкой.

**Внутренние функции**:
Внутри функции `create_async_generator` нет внутренних функций.

**Как работает функция**:

1. Функция формирует заголовки HTTP-запроса, включая User-Agent, Referer и Content-Type.
2. Создает асинхронную HTTP-сессию с заданными заголовками.
3. Формирует данные запроса, включая идентификатор разговора и отформатированный промпт.
4. Получает уникальный идентификатор пользователя с помощью `grab_token`.
5. Отправляет POST-запрос к API AiChatOnline с заголовками и данными.
6. Получает ответ и итерируется по его содержимому, извлекая чанки ответа из JSON-формата.
7. Преобразует полученные чанки и передает их через `yield`, формируя асинхронный генератор.

```
A: Формирование заголовков HTTP-запроса
|
B: Создание асинхронной HTTP-сессии
|
C: Формирование данных запроса (conversationId, prompt)
|
D: Получение уникального идентификатора пользователя (grab_token)
|
E: Отправка POST-запроса к API AiChatOnline
|
F: Итерация по содержимому ответа и извлечение чанков
|
G: Преобразование чанков и передача через yield
```

**Примеры**:

```python
messages = [{'role': 'user', 'content': 'Hello, world!'}]
async for chunk in AiChatOnline.create_async_generator('gpt-4o-mini', messages, proxy='http://proxy:8080'):
    print(chunk)
# => 'Hello'
# => ', '
# => 'world'
# => '!'