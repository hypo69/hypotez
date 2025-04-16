# Модуль для асинхронного взаимодействия с BackendApi

## Обзор

Модуль `BackendApi` предназначен для асинхронного взаимодействия с API, предоставляющим функциональность обработки диалогов и мультимедийного контента. Он использует `StreamSession` для потоковой передачи данных и предоставляет асинхронный генератор для обработки ответов.

## Подробней

Модуль `BackendApi` предоставляет класс `BackendApi`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`. Он предназначен для работы с API, которое принимает сообщения и медиафайлы, обрабатывает их и возвращает ответы в режиме потока. Класс использует `StreamSession` для асинхронной отправки запросов и получения ответов.

## Классы

### `BackendApi`

**Описание**: Класс для асинхронного взаимодействия с API обработки диалогов и мультимедийного контента.
**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:
- `ssl` (None): Параметр для настройки SSL соединения. По умолчанию `None`.
- `headers` (dict): Заголовки HTTP-запроса. По умолчанию пустой словарь `{}`.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для потоковой обработки ответов от API.

### Методы класса

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        media: MediaListType = None,
        api_key: str = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для потоковой обработки ответов от API.

        Args:
            model (str): Идентификатор модели для обработки сообщений.
            messages (Messages): Список сообщений для отправки в API.
            media (MediaListType, optional): Список медиафайлов для отправки в API. По умолчанию `None`.
            api_key (str, optional): Ключ API для аутентификации. По умолчанию `None`.
            **kwargs: Дополнительные параметры для отправки в API.

        Returns:
            AsyncResult: Асинхронный генератор, который выдает ответы от API в режиме потока.
        """
        ...
```

**Назначение**: Метод `create_async_generator` создает асинхронный генератор, который отправляет запросы к API и обрабатывает ответы в режиме потока. Он использует `StreamSession` для асинхронной отправки запросов и получения ответов.

**Как работает функция**:
1. Логирует ключ API с использованием `debug.log`.
2. Преобразует медиафайлы в формат data URI, если они предоставлены.
3. Создает асинхронный `StreamSession` с заданными заголовками.
4. Отправляет POST-запрос к API с использованием `session.post`.
5. Получает ответы от API в режиме потока с использованием `response.iter_lines`.
6. Для каждой строки ответа создает объект `RawResponse` и передает его в генератор.

**Параметры**:
- `cls`: Ссылка на класс `BackendApi`.
- `model` (str): Идентификатор модели для обработки сообщений.
- `messages` (Messages): Список сообщений для отправки в API.
- `media` (MediaListType, optional): Список медиафайлов для отправки в API. По умолчанию `None`.
- `api_key` (str, optional): Ключ API для аутентификации. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры для отправки в API.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, который выдает ответы от API в режиме потока.

**Примеры**:

Пример вызова `create_async_generator`:

```python
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Hello, world!"}]
media = None
api_key = "your_api_key"
kwargs = {}

async def main():
    async for response in BackendApi.create_async_generator(model, messages, media, api_key, **kwargs):
        print(response)

# asyncio.run(main())  # Необходимо запустить в асинхронном контексте
```
В этом примере создается асинхронный генератор для отправки сообщения "Hello, world!" в API с использованием модели "gpt-3.5-turbo".

### `create_async_generator` -> `session.post` -> `response.iter_lines` -> `RawResponse`

```python
        async with StreamSession(
            headers={"Accept": "text/event-stream", **cls.headers},\n        ) as session:
            async with session.post(f"{cls.url}/backend-api/v2/conversation", json={\n                "model": model,\n                "messages": messages,\n                "media": media,\n                "api_key": api_key,\n                **kwargs\n            }, ssl=cls.ssl) as response:
                async for line in response.iter_lines():
                    yield RawResponse(**json.loads(line))
```
**Как работает**:
1. `StreamSession`: Создает асинхронную сессию для потоковой передачи данных.
2. `session.post`: Отправляет POST-запрос к API с использованием указанного URL, заголовков и данных в формате JSON.
3. `response.iter_lines`: Получает ответы от API в режиме потока, разделяя их на строки.
4. `RawResponse`: Для каждой строки ответа создает объект `RawResponse` из JSON и передает его в генератор.

## Параметры класса

- `ssl`: Параметр для настройки SSL соединения.
- `headers`: Заголовки HTTP-запроса.