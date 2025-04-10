# Модуль Qwen_Qwen_2_5M

## Обзор

Модуль `Qwen_Qwen_2_5M` предоставляет асинхронный генератор для взаимодействия с моделью Qwen-2.5M через Hugging Face Space. Он поддерживает потоковую передачу данных, системные сообщения и предоставляет возможность возвращать JSON-контекст разговора.

## Подробней

Этот модуль используется для асинхронного взаимодействия с моделью Qwen-2.5M, размещенной на Hugging Face Space. Он отправляет запросы к API, обрабатывает ответы в формате JSON и генерирует текст. Модуль поддерживает потоковую передачу данных, что позволяет получать ответы в реальном времени.

## Классы

### `Qwen_Qwen_2_5M`

**Описание**: Класс `Qwen_Qwen_2_5M` реализует асинхронный генератор для взаимодействия с моделью Qwen-2.5M.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера ("Qwen Qwen-2.5M").
- `url` (str): URL Hugging Face Space ("https://qwen-qwen2-5-1m-demo.hf.space").
- `api_endpoint` (str): URL API для отправки запросов (`f"{url}/run/predict?__theme=light"`).
- `working` (bool): Указывает, работает ли провайдер (True).
- `supports_stream` (bool): Поддерживает ли потоковую передачу данных (True).
- `supports_system_message` (bool): Поддерживает ли системные сообщения (True).
- `supports_message_history` (bool): Поддерживает ли историю сообщений (False).
- `default_model` (str): Модель по умолчанию ("qwen-2.5-1m-demo").
- `model_aliases` (dict): Псевдонимы моделей (`{"qwen-2.5-1m": default_model}`).
- `models` (list): Список моделей (ключи `model_aliases`).

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для взаимодействия с моделью.

## Функции

### `create_async_generator`

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
    """
    Создает асинхронный генератор для взаимодействия с моделью Qwen-2.5M.

    Args:
        model (str): Название модели.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        return_conversation (bool, optional): Флаг, указывающий, нужно ли возвращать контекст разговора. По умолчанию `False`.
        conversation (JsonConversation, optional): Объект контекста разговора. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий результаты взаимодействия с моделью.

    Raises:
        aiohttp.ClientError: При ошибках соединения с сервером.
        json.JSONDecodeError: При ошибках декодирования JSON-ответа.

    """
```

**Назначение**: Функция `create_async_generator` создает асинхронный генератор, который взаимодействует с моделью Qwen-2.5M для генерации текста на основе предоставленных сообщений. Она отправляет запросы к API Hugging Face Space и обрабатывает ответы для получения сгенерированного текста.

**Параметры**:
- `cls`: Ссылка на класс `Qwen_Qwen_2_5M`.
- `model` (str): Название используемой модели.
- `messages` (Messages): Список сообщений, используемых для генерации ответа.
- `proxy` (str, optional): URL прокси-сервера для использования при подключении. По умолчанию `None`.
- `return_conversation` (bool, optional): Флаг, указывающий, следует ли возвращать объект `JsonConversation` с информацией о сессии. По умолчанию `False`.
- `conversation` (JsonConversation, optional): Объект `JsonConversation`, содержащий информацию о текущей сессии. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры, которые могут быть переданы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, который выдает текст, сгенерированный моделью.

**Вызывает исключения**:
- `aiohttp.ClientError`: Возникает при проблемах с сетевыми запросами.
- `json.JSONDecodeError`: Возникает, когда не удается декодировать JSON-ответ от сервера.

**Как работает функция**:

1. **Генерация хеша сессии**:
   - Если `conversation` равен `None`, генерируется уникальный хеш сессии.
   - Если `conversation` не равен `None`, используется хеш сессии из объекта `conversation`.
2. **Подготовка запроса**:
   - Формируется `prompt` на основе `messages` (если `conversation` равен `None`) или извлекается последнее сообщение пользователя (если `conversation` не равен `None`).
   - Формируются заголовки (`headers`) для HTTP-запросов.
   - Формируется полезная нагрузка (`payload_predict`) для запроса к API.
3. **Отправка запросов и обработка ответов**:
   - Отправляется POST-запрос к `api_endpoint` для получения данных.
   - Отправляется POST-запрос к `join_url` для присоединения к очереди.
   - Отправляется GET-запрос к `url_data` для получения потока данных.
   - Поток данных обрабатывается построчно, декодируется и извлекается JSON.
   - Из JSON извлекается текст, генерируемый моделью, и передается через `yield`.
   - Обрабатываются сообщения `process_generating` и `process_completed` для извлечения итогового текста.
4. **Обработка ошибок**:
   - Если не удается декодировать JSON, регистрируется ошибка с помощью `debug.log`.

**Внутренние функции**:

#### `generate_session_hash`

```python
def generate_session_hash():
    """Generate a unique session hash."""
    return str(uuid.uuid4()).replace(\'-\', \'\')[:12]
```

**Назначение**: Функция генерирует уникальный хеш сессии.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `str`: Уникальный хеш сессии длиной 12 символов.

**Как работает функция**:
1. Генерирует UUID (Universally Unique Identifier) с помощью `uuid.uuid4()`.
2. Удаляет дефисы из UUID с помощью `replace('-', '')`.
3. Извлекает первые 12 символов из UUID с помощью `[:12]`.
4. Возвращает полученную строку.

```
Генерация UUID --> Удаление дефисов --> Извлечение первых 12 символов --> Возврат хеша сессии
```

**Примеры**:

Пример вызова функции `create_async_generator`:

```python
import asyncio
from typing import AsyncGenerator, List, Dict, Any

from src.endpoints.gpt4free.g4f.Provider.hf_space.Qwen_Qwen_2_5M import Qwen_Qwen_2_5M
from src.endpoints.gpt4free.g4f.typing import Messages, AsyncResult

async def main():
    model: str = "qwen-2.5-1m-demo"
    messages: Messages = [{"role": "user", "content": "Hello, how are you?"}]
    proxy: str = None
    return_conversation: bool = False
    conversation: None = None

    generator: AsyncGenerator = Qwen_Qwen_2_5M.create_async_generator(
        model=model,
        messages=messages,
        proxy=proxy,
        return_conversation=return_conversation,
        conversation=conversation
    )

    async for item in generator:
        print(item)

if __name__ == "__main__":
    asyncio.run(main())
```
```