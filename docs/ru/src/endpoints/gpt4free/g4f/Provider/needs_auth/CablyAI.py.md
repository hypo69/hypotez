# Модуль `CablyAI`

## Обзор

Модуль `CablyAI` предоставляет класс `CablyAI`, который является наследником `OpenaiTemplate` и предназначен для взаимодействия с моделью CablyAI. Модуль определяет URL, необходимые для аутентификации и взаимодействия с API CablyAI, а также указывает на поддержку потоковой передачи, системных сообщений и истории сообщений.
## Подробнее

Модуль `CablyAI` является частью проекта `hypotez` и предназначен для обеспечения возможности взаимодействия с сервисом CablyAI. Он содержит информацию о конечных точках API, необходимых для аутентификации и обмена сообщениями. Класс `CablyAI` наследуется от `OpenaiTemplate`, что позволяет использовать общие методы и структуру для работы с API, подобными OpenAI.

## Классы

### `CablyAI`

**Описание**: Класс `CablyAI` предоставляет интерфейс для взаимодействия с моделью CablyAI. Он наследуется от класса `OpenaiTemplate`.

**Наследует**:

- `OpenaiTemplate`: Предоставляет общую структуру и методы для работы с API, подобными OpenAI.

**Атрибуты**:

- `url` (str): URL для взаимодействия с CablyAI (`https://cablyai.com/chat`).
- `login_url` (str): URL для аутентификации (`https://cablyai.com`).
- `api_base` (str): Базовый URL для API CablyAI (`https://cablyai.com/v1`).
- `working` (bool): Указывает, что провайдер работает (True).
- `needs_auth` (bool): Указывает, что требуется аутентификация (True).
- `supports_stream` (bool): Указывает, что поддерживается потоковая передача (True).
- `supports_system_message` (bool): Указывает, что поддерживаются системные сообщения (True).
- `supports_message_history` (bool): Указывает, что поддерживается история сообщений (True).

**Методы**:

- `create_async_generator`: Создает асинхронный генератор для взаимодействия с API CablyAI.

## Функции

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
        """
        Создает асинхронный генератор для взаимодействия с API CablyAI.

        Args:
            model (str): Название модели.
            messages (Messages): Список сообщений для отправки.
            api_key (str, optional): API-ключ для аутентификации. По умолчанию `None`.
            stream (bool, optional): Флаг, указывающий на необходимость потоковой передачи. По умолчанию `False`.
            **kwargs: Дополнительные параметры.

        Returns:
            AsyncResult: Асинхронный результат.

        Raises:
            ModelNotSupportedError: Если указанная модель не поддерживается.

        """
```

**Назначение**:

Метод `create_async_generator` создает асинхронный генератор для взаимодействия с API CablyAI. Он устанавливает необходимые заголовки для запроса и вызывает метод `create_async_generator` родительского класса `OpenaiTemplate` для фактической отправки запроса.

**Параметры**:

- `cls` (type): Ссылка на класс.
- `model` (str): Название модели.
- `messages` (Messages): Список сообщений для отправки.
- `api_key` (str, optional): API-ключ для аутентификации. По умолчанию `None`.
- `stream` (bool, optional): Флаг, указывающий на необходимость потоковой передачи. По умолчанию `False`.
- `**kwargs`: Дополнительные параметры, передаваемые в родительский класс.

**Возвращает**:

- `AsyncResult`: Асинхронный результат.

**Вызывает исключения**:

- `ModelNotSupportedError`: Если указанная модель не поддерживается.

**Как работает функция**:

1. **Установка заголовков**:
   - Функция создает словарь `headers`, содержащий необходимые HTTP-заголовки для взаимодействия с API CablyAI.
   - В заголовки включаются `Accept`, `Accept-Language`, `Authorization` (с использованием предоставленного `api_key`), `Content-Type`, `Origin`, `Referer` и `User-Agent`.

2. **Вызов родительского метода**:
   - Функция вызывает метод `create_async_generator` родительского класса `OpenaiTemplate`, передавая все параметры, включая установленные заголовки.

3. **Возврат результата**:
   - Функция возвращает результат, полученный от вызова родительского метода.

**Примеры**:

Пример создания асинхронного генератора:

```python
from typing import List, Dict, Optional

class Messages:
    def __init__(self, messages: List[Dict]):
        self.messages = messages

messages = Messages([
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
])

api_key = "your_api_key"
model = "default"

async_result = CablyAI.create_async_generator(
    model=model,
    messages=messages,
    api_key=api_key,
    stream=False
)