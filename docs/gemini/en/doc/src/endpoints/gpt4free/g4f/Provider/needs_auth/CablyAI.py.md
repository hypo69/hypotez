# Модуль CablyAI

## Обзор

Модуль `CablyAI` предоставляет класс для взаимодействия с сервисом CablyAI. Он наследуется от класса `OpenaiTemplate` и предназначен для генерации асинхронных результатов.

## Подробнее

Модуль содержит настройки для работы с CablyAI, включая URL, базовый адрес API и поддержку потоковой передачи. Для работы требуется аутентификация.

## Классы

### `CablyAI`

**Описание**: Класс для взаимодействия с сервисом CablyAI.
**Наследует**: `OpenaiTemplate`

**Атрибуты**:
- `url` (str): URL сервиса CablyAI ("https://cablyai.com/chat").
- `login_url` (str): URL для входа в сервис CablyAI ("https://cablyai.com").
- `api_base` (str): Базовый URL API сервиса CablyAI ("https://cablyai.com/v1").
- `working` (bool): Указывает, что сервис работает (True).
- `needs_auth` (bool): Указывает, что для работы требуется аутенентификация (True).
- `supports_stream` (bool): Указывает, что сервис поддерживает потоковую передачу данных (True).
- `supports_system_message` (bool): Указывает, что сервис поддерживает системные сообщения (True).
- `supports_message_history` (bool): Указывает, что сервис поддерживает историю сообщений (True).

**Принцип работы**:
Класс `CablyAI` настраивает параметры подключения к сервису CablyAI. Он также переопределяет метод `create_async_generator` для добавления специфических заголовков запроса, необходимых для аутентификации и взаимодействия с API CablyAI.

## Методы класса

### `create_async_generator`

```python
@classmethod
def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    api_key: str = None,
    stream: bool = False,
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для взаимодействия с API CablyAI.

    Args:
        cls (CablyAI): Класс CablyAI.
        model (str): Модель для генерации.
        messages (Messages): Список сообщений для отправки.
        api_key (str, optional): API ключ для аутентификации. По умолчанию `None`.
        stream (bool, optional): Флаг для включения потоковой передачи. По умолчанию `False`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный результат.

    Как работает функция:
    Функция `create_async_generator` создает заголовки, необходимые для аутентификации и взаимодействия с API CablyAI, включая токен авторизации, тип контента, источник и User-Agent. Затем вызывает метод `create_async_generator` родительского класса `OpenaiTemplate`, передавая необходимые параметры, включая заголовки.

    """
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Origin": cls.url,
        "Referer": f"{cls.url}/chat",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    return super().create_async_generator(
        model=model,
        messages=messages,
        api_key=api_key,
        stream=stream,
        headers=headers,
        **kwargs
    )
```

## Примеры

Пример вызова `create_async_generator`:

```python
# from src.endpoints.gpt4free.g4f.Provider.needs_auth.CablyAI import CablyAI
# from g4f.models import gpt_35_turbo
# from g4f.message import Message
# from typing import List

# messages: List[Message] = [Message(role="user", content="Hello")]
# api_key = "ваш_api_ключ"  # Замените на ваш фактический API ключ
# result = CablyAI.create_async_generator(model=gpt_35_turbo.name, messages=messages, api_key=api_key, stream=False)
# print(result)