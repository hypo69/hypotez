# Module `Replicate.py`

## Overview

Модуль предоставляет асинхронный генератор для взаимодействия с Replicate API. Replicate позволяет запускать различные модели машинного обучения через API. Модуль поддерживает стриминг ответов и требует аутентификации через API ключ.

## More details

Этот модуль является частью проекта `hypotez` и предназначен для интеграции с Replicate API для выполнения задач, требующих машинного обучения. Он включает в себя функции для форматирования запросов, фильтрации параметров и обработки стриминговых ответов от Replicate.

## Classes

### `Replicate`

**Description**: Класс `Replicate` предоставляет асинхронный генератор для взаимодействия с API Replicate.

**Inherits**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Добавляет функциональность для работы с моделями.

**Attributes**:
- `url` (str): URL для доступа к Replicate API.
- `login_url` (str): URL для получения API токена.
- `working` (bool): Указывает, работает ли провайдер.
- `needs_auth` (bool): Указывает, требуется ли аутентификация.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (list): Список поддерживаемых моделей.

**Working principle**:
Класс использует `AsyncGeneratorProvider` для асинхронной генерации ответов от Replicate API. Он также использует `ProviderModelMixin` для управления моделями. При создании асинхронного генератора, класс проверяет наличие API ключа, формирует запрос к API и обрабатывает стриминговые ответы.

## Class Methods

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    api_key: str = None,
    proxy: str = None,
    timeout: int = 180,
    system_prompt: str = None,
    max_tokens: int = None,
    temperature: float = None,
    top_p: float = None,
    top_k: float = None,
    stop: list = None,
    extra_data: dict = {},
    headers: dict = {
        "accept": "application/json",
    },
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для взаимодействия с API Replicate.

    Args:
        cls (Replicate): Класс Replicate.
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        api_key (str, optional): API ключ для аутентификации. По умолчанию `None`.
        proxy (str, optional): Прокси сервер для использования. По умолчанию `None`.
        timeout (int, optional): Время ожидания запроса в секундах. По умолчанию 180.
        system_prompt (str, optional): Системное сообщение для модели. По умолчанию `None`.
        max_tokens (int, optional): Максимальное количество токенов в ответе. По умолчанию `None`.
        temperature (float, optional): Температура для генерации текста. По умолчанию `None`.
        top_p (float, optional): Top P для генерации текста. По умолчанию `None`.
        top_k (float, optional): Top K для генерации текста. По умолчанию `None`.
        stop (list, optional): Список стоп-слов. По умолчанию `None`.
        extra_data (dict, optional): Дополнительные данные для отправки. По умолчанию `{}`.
        headers (dict, optional): Заголовки HTTP запроса. По умолчанию `{"accept": "application/json"}`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор текста.

    Raises:
        MissingAuthError: Если `api_key` отсутствует и требуется аутентификация.
        ResponseError: Если получен некорректный ответ от API.

    How the function works:
    - Функция извлекает модель из входных параметров.
    - Проверяет, требуется ли аутентификация и наличие `api_key`.
    - Формирует заголовки запроса, включая `Authorization`, если предоставлен `api_key`.
    - Создает сессию с использованием `StreamSession` для поддержки стриминга.
    - Формирует данные для запроса, включая `prompt`, `max_new_tokens`, `temperature`, `top_p`, `top_k` и `stop_sequences`.
    - Отправляет POST запрос к API Replicate для получения предсказания.
    - Обрабатывает ответ, проверяя наличие ошибок и извлекая `id` предсказания.
    - Отправляет GET запрос к `stream` URL для получения стриминговых данных.
    - Итерирует по строкам ответа, извлекая данные из событий `output`.
    - Декодирует полученные данные и передает их через `yield`.
    """
    model = cls.get_model(model)
    if cls.needs_auth and api_key is None:
        raise MissingAuthError("api_key is missing")
    if api_key is not None:
        headers["Authorization"] = f"Bearer {api_key}"
        api_base = "https://api.replicate.com/v1/models/"
    else:
        api_base = "https://replicate.com/api/models/"
    async with StreamSession(
        proxy=proxy,
        headers=headers,
        timeout=timeout
    ) as session:
        data = {
            "stream": True,
            "input": {
                "prompt": format_prompt(messages),
                **filter_none(
                    system_prompt=system_prompt,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    top_k=top_k,
                    stop_sequences=",".join(stop) if stop else None
                ),
                **extra_data
            },
        }
        url = f"{api_base.rstrip('/')}/{model}/predictions"
        async with session.post(url, json=data) as response:
            message = "Model not found" if response.status == 404 else None
            await raise_for_status(response, message)
            result = await response.json()
            if "id" not in result:
                raise ResponseError(f"Invalid response: {result}")
            async with session.get(result["urls"]["stream"], headers={"Accept": "text/event-stream"}) as response:
                await raise_for_status(response)
                event = None
                async for line in response.iter_lines():
                    if line.startswith(b"event: "):
                        event = line[7:]
                        if event == b"done":
                            break
                    elif event == b"output":
                        if line.startswith(b"data: "):
                            new_text = line[6:].decode()
                            if new_text:
                                yield new_text
                            else:
                                yield "\\n"
```

### Internal functions: if there are any

Внутри функции `create_async_generator` используются следующие внутренние функции и методы:

- `cls.get_model(model)`: Получает имя модели.
- `format_prompt(messages)`: Форматирует список сообщений в строку для отправки в запросе.
- `filter_none(...)`: Фильтрует параметры, удаляя те, которые имеют значение `None`.
- `session.post(url, json=data)`: Отправляет POST-запрос к API Replicate.
- `response.json()`: Декодирует JSON-ответ.
- `session.get(result["urls"]["stream"], headers={"Accept": "text/event-stream"})`: Отправляет GET-запрос для получения стриминговых данных.
- `response.iter_lines()`: Итерирует по строкам в стриминговом ответе.

**Examples**: # All possible variations of examples of calling the function with different parameters
```python
# Пример вызова create_async_generator с минимальным набором параметров
async def example():
    async for text in Replicate.create_async_generator(model="meta/meta-llama-3-70b-instruct", messages=[{"role": "user", "content": "Hello, Replicate!"}], api_key="YOUR_API_KEY"):
        print(text)

# Пример вызова create_async_generator с дополнительными параметрами
async def example_with_params():
    async for text in Replicate.create_async_generator(
        model="meta/meta-llama-3-70b-instruct",
        messages=[{"role": "user", "content": "Translate to Spanish: Hello, Replicate!"}],
        api_key="YOUR_API_KEY",
        max_tokens=50,
        temperature=0.7,
        stop=["\n"]
    ):
        print(text)