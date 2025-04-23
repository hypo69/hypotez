# Модуль `Qwen_Qwen_2_5M`

## Обзор

Модуль `Qwen_Qwen_2_5M` предоставляет асинхронный интерфейс для взаимодействия с моделью Qwen Qwen-2.5M через Hugging Face Space. Он поддерживает потоковую передачу ответов и может использоваться для генерации текста на основе предоставленных сообщений.

## Детали

Модуль реализует класс `Qwen_Qwen_2_5M`, который является подклассом `AsyncGeneratorProvider` и `ProviderModelMixin`. Он использует `aiohttp` для выполнения асинхронных HTTP-запросов к API Hugging Face Space. Модуль также включает функции для форматирования входных сообщений и обработки ответов API.

## Классы

### `Qwen_Qwen_2_5M`

**Описание**:
Класс `Qwen_Qwen_2_5M` предоставляет интерфейс для взаимодействия с моделью Qwen Qwen-2.5M через Hugging Face Space.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет общие функции для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера, "Qwen Qwen-2.5M".
- `url` (str): URL Hugging Face Space, "https://qwen-qwen2-5-1m-demo.hf.space".
- `api_endpoint` (str): URL API для выполнения запросов, формируется из `url`.
- `working` (bool): Указывает, работает ли провайдер, `True`.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу, `True`.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения, `True`.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений, `False`.
- `default_model` (str): Модель по умолчанию, "qwen-2.5-1m-demo".
- `model_aliases` (dict): Псевдонимы моделей, `{"qwen-2.5-1m": default_model}`.
- `models` (list): Список моделей, извлеченный из `model_aliases.keys()`.

**Принцип работы**:
Класс использует асинхронные HTTP-запросы для взаимодействия с API Hugging Face Space. Он форматирует входные сообщения, отправляет их в API и обрабатывает ответы для генерации текста. Поддерживается потоковая передача ответов, что позволяет получать текст по частям.

```python
from __future__ import annotations

import aiohttp
import json
import uuid

from ...typing import AsyncResult, Messages
from ..base_provider import AsyncGeneratorProvider, ProviderModelMixin
from ..helper import format_prompt
from ...providers.response import JsonConversation, Reasoning
from ..helper import get_last_user_message
from ... import debug

class Qwen_Qwen_2_5M(AsyncGeneratorProvider, ProviderModelMixin):
    label = "Qwen Qwen-2.5M"
    url = "https://qwen-qwen2-5-1m-demo.hf.space"
    api_endpoint = f"{url}/run/predict?__theme=light"

    working = True
    supports_stream = True
    supports_system_message = True
    supports_message_history = False

    default_model = "qwen-2.5-1m-demo"
    model_aliases = {"qwen-2.5-1m": default_model}
    models = list(model_aliases.keys())
```

### Методы класса

#### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    return_conversation: bool = False,
    conversation: JsonConversation = None,
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для взаимодействия с моделью Qwen Qwen-2.5M.

    Args:
        cls (Qwen_Qwen_2_5M): Ссылка на класс.
        model (str): Название модели для использования.
        messages (Messages): Список сообщений для отправки в модель.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        return_conversation (bool, optional): Возвращать ли объект `JsonConversation`. По умолчанию `False`.
        conversation (JsonConversation, optional): Объект `JsonConversation` для поддержания состояния разговора. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий результаты взаимодействия с моделью.

    Raises:
        aiohttp.ClientError: Если возникает ошибка при выполнении HTTP-запроса.
        json.JSONDecodeError: Если не удается декодировать JSON-ответ.
    """
```

**Внутренние функции**:

- `generate_session_hash()`
```python
        def generate_session_hash():
            """Генерирует уникальный хэш сессии."""
            return str(uuid.uuid4()).replace('-', '')[:12]
```
   **Как работает**:
    - Функция генерирует уникальный идентификатор сессии, используя UUID и удаляя дефисы.

**Как работает**:

1. **Генерация хэша сессии**: Если объект `conversation` не передан, генерируется уникальный хэш сессии с помощью функции `generate_session_hash`. Если `conversation` передан, используется хэш сессии из этого объекта.
2. **Возврат объекта `JsonConversation`**: Если `return_conversation` имеет значение `True`, первым возвращается объект `JsonConversation` с хэшем сессии.
3. **Форматирование запроса**: Если объект `conversation` не передан, формируется запрос на основе списка сообщений `messages` с использованием функции `format_prompt`. Если `conversation` передан, извлекается последнее сообщение пользователя из `messages` с помощью функции `get_last_user_message`.
4. **Подготовка заголовков**: Определяются заголовки HTTP-запроса, включая `accept`, `content-type`, `origin`, `referer` и `user-agent`.
5. **Подготовка полезной нагрузки**: Формируется полезная нагрузка (payload) для отправки данных в API. Включает текст запроса, идентификатор функции (`fn_index`), идентификатор триггера (`trigger_id`) и хэш сессии.
6. **Отправка запроса и обработка ответа**:
   - Создается асинхронная сессия с использованием `aiohttp.ClientSession`.
   - Отправляется POST-запрос к `cls.api_endpoint` с заголовками и полезной нагрузкой.
   - Извлекаются данные из JSON-ответа.
7. **Отправка запроса на присоединение к очереди и получение event_id**:
   - Формируется URL для присоединения к очереди.
   - Формируется полезная нагрузка для запроса на присоединение к очереди.
   - Отправляется POST-запрос к `join_url` с заголовками и полезной нагрузкой.
   - Извлекается `event_id` из JSON-ответа.
8. **Подготовка запроса потока данных**:
   - Формируется URL для получения потока данных.
   - Определяются заголовки для запроса потока данных.
9. **Отправка запроса потока данных и обработка ответа**:
   - Отправляется GET-запрос к `url_data` с заголовками.
   - Асинхронно обрабатываются строки ответа:
     - Декодируется каждая строка.
     - Если строка начинается с `data: `, извлекается JSON-данные.
     - Если `msg` имеет значение `process_generating`, извлекается текст из `output_data` и возвращается.
     - Если `msg` имеет значение `process_completed`, извлекается текст из `output_data` и возвращается.
     - В случае ошибки декодирования JSON, регистрируется сообщение об ошибке.

**Примеры**:

```python
# Пример использования create_async_generator
messages = [{"role": "user", "content": "Hello, Qwen!"}]
async for response in Qwen_Qwen_2_5M.create_async_generator(model="qwen-2.5-1m-demo", messages=messages):
    print(response)
```

## Параметры класса

- `label` (str): "Qwen Qwen-2.5M" - Метка, идентифицирующая провайдера.
- `url` (str): "https://qwen-qwen2-5-1m-demo.hf.space" - URL, используемый для доступа к Hugging Face Space.
- `api_endpoint` (str): Конечная точка API, используемая для выполнения запросов.
- `working` (bool): `True` - Указывает, что провайдер в настоящее время работает.
- `supports_stream` (bool): `True` - Указывает, что провайдер поддерживает потоковую передачу данных.
- `supports_system_message` (bool): `True` - Указывает, что провайдер поддерживает системные сообщения.
- `supports_message_history` (bool): `False` - Указывает, что провайдер не поддерживает историю сообщений.
- `default_model` (str): "qwen-2.5-1m-demo" - Модель, используемая по умолчанию.
- `model_aliases` (dict): `{"qwen-2.5-1m": default_model}` - Псевдонимы для моделей.
- `models` (list): `list(model_aliases.keys())` - Список доступных моделей.