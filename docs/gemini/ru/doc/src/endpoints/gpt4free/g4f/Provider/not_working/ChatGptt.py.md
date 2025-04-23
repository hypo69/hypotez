# src.endpoints.gpt4free.g4f.Provider.not_working.ChatGptt

## Обзор

Модуль `ChatGptt` предоставляет асинхронный генератор для взаимодействия с моделью `gpt-4o` через API `chatgptt.me`. Он поддерживает потоковую передачу данных, системные сообщения и историю сообщений. Этот модуль предназначен для интеграции в систему `hypotez` для обеспечения доступа к альтернативным моделям обработки текста.

## Подробней

Модуль предназначен для реализации доступа к API `chatgptt.me` для использования моделей `gpt-4o`, `gpt-4` и `gpt-4o-mini`. Он использует асинхронные запросы через `aiohttp` для получения ответов от API и предоставляет результаты в виде асинхронного генератора. Модуль извлекает необходимые токены аутентификации (nonce и post_id) из HTML-кода главной страницы `chatgptt.me`. Это позволяет обходить ограничения доступа и использовать API для генерации текста.

## Классы

### `ChatGptt`

**Описание**: Класс `ChatGptt` реализует асинхронный генератор для взаимодействия с API `chatgptt.me`. Он наследует функциональность от `AsyncGeneratorProvider` и `ProviderModelMixin`.

**Наследует**:

- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями, такими как `gpt-4`, `gpt-4o` и `gpt-4o-mini`.

**Атрибуты**:

- `url` (str): URL главной страницы `chatgptt.me`.
- `api_endpoint` (str): URL API для отправки запросов.
- `working` (bool): Указывает, работает ли провайдер в данный момент. Всегда `False` в данном коде.
- `supports_stream` (bool): Поддержка потоковой передачи данных. Всегда `True`.
- `supports_system_message` (bool): Поддержка системных сообщений. Всегда `True`.
- `supports_message_history` (bool): Поддержка истории сообщений. Всегда `True`.
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4o`).
- `models` (list): Список поддерживаемых моделей (`gpt-4`, `gpt-4o`, `gpt-4o-mini`).

**Принцип работы**:

Класс использует асинхронные HTTP-запросы для обмена данными с API `chatgptt.me`. Он извлекает токены аутентификации из HTML-кода главной страницы и отправляет POST-запросы с сообщениями для генерации текста. Результаты возвращаются в виде асинхронного генератора.

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
    """Создает асинхронный генератор для получения ответов от API `chatgptt.me`.

    Args:
        cls (ChatGptt): Ссылка на класс `ChatGptt`.
        model (str): Модель для использования (например, `gpt-4`, `gpt-4o`, `gpt-4o-mini`).
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы (не используются).

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от API.

    Raises:
        RuntimeError: Если не удается найти токены аутентификации в HTML-коде страницы.
    """
```

**Назначение**: Создает асинхронный генератор для получения ответов от API `chatgptt.me`.

**Параметры**:

- `cls` (ChatGptt): Ссылка на класс `ChatGptt`.
- `model` (str): Модель для использования (например, `gpt-4`, `gpt-4o`, `gpt-4o-mini`).
- `messages` (Messages): Список сообщений для отправки в API.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы (не используются).

**Возвращает**:

- `AsyncResult`: Асинхронный генератор, возвращающий ответы от API.

**Вызывает исключения**:

- `RuntimeError`: Если не удается найти токены аутентификации в HTML-коде страницы.

**Как работает функция**:

1. **Выбор модели**:
   - Функция вызывает `cls.get_model(model)` для получения имени модели.

2. **Формирование заголовков**:
   - Функция задает заголовоки для HTTP-запроса, включая `authority`, `accept`, `origin`, `referer` и `user-agent`.

3. **Создание сессии**:
   - Используется `aiohttp.ClientSession` для выполнения асинхронных запросов.

4. **Извлечение токенов аутентификации**:
   - Функция отправляет GET-запрос на главную страницу `chatgptt.me`.
   - Извлекает `nonce` и `post_id` из HTML-кода страницы с использованием регулярных выражений.
   - Если токены не найдены, вызывается исключение `RuntimeError`.

5. **Подготовка данных**:
   - Функция подготавливает данные (`payload`) для POST-запроса, включая `_wpnonce`, `post_id`, `url`, `action`, `message`, `bot_id`, `chatbot_identity` и `wpaicg_chat_client_id`.
   - `message` формируется с использованием функции `format_prompt(messages)`.

6. **Отправка запроса и обработка ответа**:
   - Функция отправляет POST-запрос на `cls.api_endpoint` с заголовками и данными.
   - Обрабатывает ответ, извлекая поле `data` из JSON-формата и передавая его в генератор.

**Примеры**:

```python
# Пример использования функции create_async_generator
import asyncio
from src.endpoints.gpt4free.g4f.Provider.not_working.ChatGptt import ChatGptt
from src.typing import Messages

async def main():
    messages: Messages = [{"role": "user", "content": "Hello, how are you?"}]
    model = "gpt-4o"
    proxy = None

    generator = await ChatGptt.create_async_generator(model=model, messages=messages, proxy=proxy)
    async for message in generator:
        print(message)

if __name__ == "__main__":
    asyncio.run(main())