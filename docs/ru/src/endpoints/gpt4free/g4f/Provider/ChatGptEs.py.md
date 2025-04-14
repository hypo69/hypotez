# Модуль для взаимодействия с ChatGptEs через API

## Обзор

Модуль `ChatGptEs` предоставляет асинхронный интерфейс для взаимодействия с сервисом ChatGptEs через его API. Он позволяет генерировать ответы на основе предоставленных сообщений, используя различные модели, поддерживаемые сервисом. Модуль использует библиотеку `curl_cffi` для выполнения HTTP-запросов и обхода защиты Cloudflare.

## Подробнее

Модуль предназначен для интеграции с другими частями проекта, где требуется генерация текста на основе моделей GPT. Он обеспечивает асинхронное взаимодействие, что позволяет избежать блокировки основного потока выполнения. Для работы модуля требуется установленная библиотека `curl_cffi`.

## Классы

### `ChatGptEs`

**Описание**: Класс `ChatGptEs` реализует асинхронный генератор для взаимодействия с ChatGptEs.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность асинхронного провайдера генератора.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL сервиса ChatGptEs.
- `api_endpoint` (str): URL API-endpoint для отправки сообщений.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4o`).
- `models` (List[str]): Список поддерживаемых моделей (`gpt-4`, `gpt-4o`, `gpt-4o-mini`).
- `SYSTEM_PROMPT` (str): Системное сообщение, используемое для форматирования запроса.

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для получения ответов от ChatGptEs.
- `get_model()`: Возвращает модель.

## Функции

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
    """Создает асинхронный генератор для получения ответов от ChatGptEs.

    Args:
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от ChatGptEs.

    Raises:
        MissingRequirementsError: Если не установлена библиотека `curl_cffi`.
        ValueError: Если возникает ошибка при выполнении запроса или неожиданный формат ответа.

    """
```

**Назначение**: Создает асинхронный генератор для получения ответов от ChatGptEs.

**Параметры**:
- `cls` (ChatGptEs): Класс ChatGptEs.
- `model` (str): Модель для использования.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий ответы от ChatGptEs.

**Вызывает исключения**:
- `MissingRequirementsError`: Если не установлена библиотека `curl_cffi`.
- `ValueError`: Если возникает ошибка при выполнении запроса или неожиданный формат ответа.

**Как работает функция**:

1. **Проверка зависимостей**:
   - Проверяется наличие библиотеки `curl_cffi`. Если она не установлена, вызывается исключение `MissingRequirementsError`.
2. **Подготовка запроса**:
   - Извлекается имя модели с помощью `cls.get_model(model)`.
   - Формируется prompt (запрос) путем объединения `cls.SYSTEM_PROMPT` и сообщений, отформатированных функцией `format_prompt(messages)`.
3. **Создание сессии**:
   - Инициализируется сессия `curl_cffi.requests.Session`.
   - Устанавливаются заголовки сессии, включая `user-agent`, `referer`, `origin`, `accept`, `accept-language`, `content-type` и `x-requested-with`.
   - Если указан прокси, он добавляется в сессию.
4. **Получение `nonce` и `post_id`**:
   - Выполняется GET-запрос к `cls.url` для получения `nonce` и `post_id` из HTML-кода страницы.
   - Используются регулярные выражения для поиска `nonce` в HTML-коде. Если `nonce` не найден, используется значение по умолчанию `"8cf9917be2"`.
   - Используются регулярные выражения для поиска `post_id` в HTML-коде. Если `post_id` не найден, используется значение по умолчанию `"106"`.
5. **Подготовка данных для POST-запроса**:
   - Генерируется случайный `client_id`.
   - Формируются данные для POST-запроса, включая `_wpnonce`, `post_id`, `url`, `action`, `message`, `bot_id`, `chatbot_identity`, `wpaicg_chat_client_id` и `wpaicg_chat_history`.
6. **Выполнение POST-запроса**:
   - Выполняется POST-запрос к `cls.api_endpoint` с подготовленными данными.
   - Проверяется статус код ответа. Если статус код не равен 200, вызывается исключение `ValueError`.
7. **Обработка ответа**:
   - Преобразуется ответ в формат JSON.
   - Извлекается значение из ключа `data` в ответе.
   - Если значение `data` является строкой и содержит `"Du musst das Kästchen anklicken!"`, вызывается исключение `ValueError`.
   - Возвращается значение `data` через `yield`.
   - Если формат ответа не соответствует ожидаемому, вызывается исключение `ValueError`.

**ASCII flowchart**:

```
A: Проверка зависимостей (curl_cffi)
|
B: Подготовка запроса (model, prompt)
|
C: Создание сессии (headers, proxy)
|
D: Получение nonce и post_id (GET-запрос, regex)
|
E: Подготовка данных для POST-запроса (client_id, data)
|
F: Выполнение POST-запроса (api_endpoint, data)
|
G: Обработка ответа (status_code, JSON, data)
|
H: Генерация результата (yield data)
```

**Примеры**:

```python
# Пример использования create_async_generator
import asyncio
from typing import List, Dict, AsyncGenerator

async def main():
    model: str = "gpt-4o"
    messages: List[Dict[str, str]] = [{"role": "user", "content": "Hello, how are you?"}]
    proxy: str = None

    generator: AsyncGenerator[str, None] = await ChatGptEs.create_async_generator(model=model, messages=messages, proxy=proxy)

    async for message in generator:
        print(message)

if __name__ == "__main__":
    asyncio.run(main())