# Документация для модуля `ChatGptEs`

## Обзор

Модуль `ChatGptEs` предоставляет асинхронный генератор для взаимодействия с сервисом ChatGpt.es. Он использует библиотеку `curl_cffi` для выполнения HTTP-запросов и обходит защиту Cloudflare. Модуль поддерживает потоковую передачу данных и предоставляет несколько моделей, включая `gpt-4` и `gpt-4o`.

## Детали

Модуль предназначен для использования в проектах, требующих взаимодействия с ChatGpt.es для генерации текста на основе предоставленных сообщений. Он автоматически обрабатывает получение nonce и post_id, необходимых для запросов к API.

## Классы

### `ChatGptEs`

**Описание**: Класс для взаимодействия с ChatGpt.es через асинхронный генератор.

**Наследует**:
- `AsyncGeneratorProvider`: Предоставляет базовую функциональность для асинхронных генераторов.
- `ProviderModelMixin`: Позволяет использовать общие методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL сервиса ChatGpt.es (`"https://chatgpt.es"`).
- `api_endpoint` (str): URL API для отправки сообщений (`"https://chatgpt.es/wp-admin/admin-ajax.php"`).
- `working` (bool): Флаг, указывающий, что провайдер работает (`True`).
- `supports_stream` (bool): Флаг, указывающий, что поддерживается потоковая передача (`True`).
- `supports_system_message` (bool): Флаг, указывающий, что поддерживаются системные сообщения (`False`).
- `supports_message_history` (bool): Флаг, указывающий, что поддерживается история сообщений (`False`).
- `default_model` (str): Модель, используемая по умолчанию (`'gpt-4o'`).
- `models` (List[str]): Список поддерживаемых моделей (`['gpt-4', default_model, 'gpt-4o-mini']`).
- `SYSTEM_PROMPT` (str): Системное сообщение, используемое для форматирования запросов (`"Your default language is English. Always respond in English unless the user\'s message is in a different language. If the user\'s message is not in English, respond in the language of the user\'s message. Maintain this language behavior throughout the conversation unless explicitly instructed otherwise. User input:"`).

## Методы класса

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
    Создает асинхронный генератор для взаимодействия с ChatGpt.es.

    Args:
        model (str): Используемая модель.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий результаты от ChatGpt.es.

    Raises:
        MissingRequirementsError: Если не установлена библиотека `curl_cffi`.
        ValueError: Если получен неожиданный статус ответа или формат данных.

    Как работает функция:
    - Проверяет наличие библиотеки `curl_cffi`. Если её нет, вызывает исключение `MissingRequirementsError`.
    - Получает модель, используя метод `get_model`.
    - Форматирует запрос, добавляя системное сообщение и сообщения пользователя.
    - Создает сессию `curl_cffi.requests.Session` для выполнения запросов.
    - Обновляет заголовки сессии, добавляя `user-agent`, `referer`, `origin`, `accept`, `accept-language` и `content-type`.
    - Если указан прокси, устанавливает его для сессии.
    - Выполняет первый GET-запрос для получения `nonce` и `post_id`.
    - Извлекает `nonce` и `post_id` из HTML-ответа, используя регулярные выражения.
    - Генерирует случайный `client_id`.
    - Подготавливает данные для POST-запроса, включая `_wpnonce`, `post_id`, `url`, `action`, `message`, `bot_id`, `chatbot_identity` и `wpaicg_chat_client_id`.
    - Выполняет POST-запрос к `api_endpoint` с использованием сессии.
    - Обрабатывает ответ, проверяя статус код и формат данных.
    - Генерирует данные из ответа, если они присутствуют в формате JSON.

    """
    ...
```

## Примеры

```python
# Пример использования create_async_generator
import asyncio
from src.endpoints.gpt4free.g4f.Provider.ChatGptEs import ChatGptEs
from src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    messages: Messages = [{"role": "user", "content": "Hello, how are you?"}]
    model = "gpt-4o"
    
    try:
        async for message in ChatGptEs.create_async_generator(model=model, messages=messages):
            print(message)
    except Exception as ex:
        print(f"Error: {ex}")

if __name__ == "__main__":
    asyncio.run(main())