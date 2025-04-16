# Модуль для работы с ChatGLM
===========================

Модуль предоставляет класс `ChatGLM`, который используется для взаимодействия с API ChatGLM для генерации текста.

## Обзор

Этот модуль является частью проекта `hypotez` и предназначен для обеспечения взаимодействия с моделью ChatGLM. Он позволяет отправлять запросы к API ChatGLM и получать сгенерированный текст в асинхронном режиме. Модуль поддерживает потоковую передачу данных, что позволяет получать результаты по частям.

## Подробнее

Модуль содержит класс `ChatGLM`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`. Он определяет параметры подключения к API ChatGLM, такие как URL и заголовки запросов. Класс также реализует метод `create_async_generator`, который отправляет запрос к API и возвращает асинхронный генератор для получения сгенерированного текста.

## Классы

### `ChatGLM`

**Описание**: Класс для взаимодействия с API ChatGLM.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL для доступа к ChatGLM.
- `api_endpoint` (str): URL API для отправки запросов.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (List[str]): Список поддерживаемых моделей.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения сгенерированного текста.

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
    """ Создает асинхронный генератор для получения сгенерированного текста от API ChatGLM.
    Args:
        cls (ChatGLM): Класс ChatGLM.
        model (str): Название используемой модели.
        messages (Messages): Список сообщений для отправки в API.
        proxy (Optional[str], optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий сгенерированный текст.

    Raises:
        Exception: Если возникает ошибка при отправке запроса или обработке ответа.

    """
```

**Назначение**: Создает асинхронный генератор для получения сгенерированного текста от API ChatGLM.

**Параметры**:
- `cls` (ChatGLM): Класс ChatGLM.
- `model` (str): Название используемой модели.
- `messages` (Messages): Список сообщений для отправки в API.
- `proxy` (Optional[str], optional): URL прокси-сервера. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий сгенерированный текст.

**Как работает функция**:
- Генерируется уникальный `device_id`.
- Определяются заголовки запроса, включая `device_id`.
- Создается сессия `aiohttp.ClientSession` с заданными заголовками.
- Формируется полезная нагрузка `data` для запроса, включающая `assistant_id`, `conversation_id`, `meta_data` и список сообщений.
- Отправляется POST-запрос к `cls.api_endpoint` с использованием `session.post`.
- Обрабатывается ответ от API в асинхронном режиме, извлекая и передавая сгенерированный текст по частям.
- Если статус ответа `finish`, передается `FinishReason("stop")`.
- Обрабатываются исключения `json.JSONDecodeError`, которые могут возникнуть при разборе JSON.

```python
async with ClientSession(headers=headers) as session:
    data = {
        "assistant_id": "65940acff94777010aa6b796",
        "conversation_id": "",
        "meta_data": {
            "if_plus_model": False,
            "is_test": False,
            "input_question_type": "xxxx",
            "channel": "",
            "draft_id": "",
            "quote_log_id": "",
            "platform": "pc"
        },
        "messages": [
            {
                "role": message["role"],
                "content": [
                    {
                        "type": "text",
                        "text": message["content"]
                    }
                ]
            }
            for message in messages
        ]
    }

    yield_text = 0
    async with session.post(cls.api_endpoint, json=data, proxy=proxy) as response:
        await raise_for_status(response)
        async for chunk in response.content:
            if chunk:
                decoded_chunk = chunk.decode('utf-8')
                if decoded_chunk.startswith('data: '):
                    try:
                        json_data = json.loads(decoded_chunk[6:])
                        parts = json_data.get('parts', [])
                        if parts:
                            content = parts[0].get('content', [])
                            if content:
                                text_content = content[0].get('text', '')
                                text = text_content[yield_text:]
                                if text:
                                    yield text
                                    yield_text += len(text)
                        # Yield FinishReason when status is 'finish'
                        if json_data.get('status') == 'finish':
                            yield FinishReason("stop")
                    except json.JSONDecodeError:
                        pass
```

**Примеры**:

```python
# Пример использования create_async_generator
messages = [{"role": "user", "content": "Hello, ChatGLM!"}]
async def example():
    async for text in ChatGLM.create_async_generator(model="glm-4", messages=messages):
        print(text)

# Запуск примера (требуется асинхронная среда)
# await example()
```

## Параметры класса

- `url` (str): URL для доступа к ChatGLM.
- `api_endpoint` (str): URL API для отправки запросов.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (List[str]): Список поддерживаемых моделей.