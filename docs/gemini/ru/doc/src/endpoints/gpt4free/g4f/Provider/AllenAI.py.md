# Модуль AllenAI

## Обзор

Модуль `AllenAI` предоставляет класс `AllenAI`, который является асинхронным генератором для взаимодействия с API Ai2 Playground. Он позволяет отправлять запросы к различным моделям Ai2 Playground и получать ответы в асинхронном режиме.

## Подробнее

Модуль поддерживает потоковую передачу данных, не требует аутентификации и может быть использован для ведения диалогов с использованием истории сообщений. Он также предоставляет возможность выбора различных моделей, поддерживаемых Ai2 Playground.

## Классы

### `Conversation`

**Описание**: Класс `Conversation` представляет собой структуру для хранения истории диалога с AI-моделью. Он наследуется от `JsonConversation` и добавляет специфичные атрибуты для управления контекстом диалога.

**Наследует**: `JsonConversation`

**Атрибуты**:

-   `parent` (str): Идентификатор родительского сообщения в диалоге.
-   `x_anonymous_user_id` (str): Анонимный идентификатор пользователя.
-   `model` (str):  Имя модели, используемой в диалоге.
-   `messages` (List[dict]): Список сообщений в диалоге, где каждое сообщение представлено в виде словаря.

**Методы**:

-   `__init__(self, model: str)`: Инициализирует новый экземпляр класса `Conversation`.

### `AllenAI`

**Описание**: Класс `AllenAI` является провайдером для взаимодействия с API Ai2 Playground. Он предоставляет методы для создания асинхронных генераторов, отправки запросов и получения ответов от AI-моделей.

**Наследует**: `AsyncGeneratorProvider`, `ProviderModelMixin`

**Атрибуты**:

-   `label` (str): Метка провайдера ("Ai2 Playground").
-   `url` (str): URL Ai2 Playground ("https://playground.allenai.org").
-   `login_url` (str): URL для входа (None).
-   `api_endpoint` (str): URL API Ai2 Playground ("https://olmo-api.allen.ai/v4/message/stream").
-   `working` (bool): Указывает, что провайдер работает (True).
-   `needs_auth` (bool): Указывает, требуется ли аутентификация (False).
-   `use_nodriver` (bool): Указывает, нужно ли использовать драйвер (False).
-   `supports_stream` (bool): Указывает, поддерживает ли потоковую передачу (True).
-   `supports_system_message` (bool): Указывает, поддерживает ли системные сообщения (False).
-   `supports_message_history` (bool): Указывает, поддерживает ли историю сообщений (True).
-   `default_model` (str): Модель по умолчанию ('tulu3-405b').
-   `models` (List[str]): Список поддерживаемых моделей.
-   `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

**Методы**:

-   `create_async_generator(...)`: Создает асинхронный генератор для получения ответов от AI-модели.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    host: str = "inferd",
    private: bool = True,
    top_p: float = None,
    temperature: float = None,
    conversation: Conversation = None,
    return_conversation: bool = False,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для получения ответов от AI-модели.

    Args:
        cls (AllenAI): Класс AllenAI.
        model (str): Имя используемой модели.
        messages (Messages): Список сообщений для отправки в модель.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        host (str, optional): Хост для отправки запроса. По умолчанию "inferd".
        private (bool, optional): Указывает, является ли запрос приватным. По умолчанию `True`.
        top_p (float, optional): Значение top_p для генерации текста. По умолчанию `None`.
        temperature (float, optional): Температура для генерации текста. По умолчанию `None`.
        conversation (Conversation, optional): Объект диалога для поддержания контекста. По умолчанию `None`.
        return_conversation (bool, optional): Указывает, нужно ли возвращать объект диалога. По умолчанию `False`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от AI-модели.

    Raises:
        Exception: Если возникает ошибка при отправке запроса или обработке ответа.

    Как работает функция:
    - Формирует запрос на основе входных параметров.
    - Отправляет запрос к API Ai2 Playground.
    - Получает ответы от AI-модели в асинхронном режиме.
    - Обрабатывает ответы и возвращает их в виде асинхронного генератора.
    - Поддерживает контекст диалога с использованием объекта `Conversation`.

    Внутренние функции:
        отсутствуют
    """
```

## Параметры класса

-   `label` (str): Метка провайдера ("Ai2 Playground").
-   `url` (str): URL Ai2 Playground ("https://playground.allenai.org").
-   `login_url` (str): URL для входа (None).
-   `api_endpoint` (str): URL API Ai2 Playground ("https://olmo-api.allen.ai/v4/message/stream").
-   `working` (bool): Указывает, что провайдер работает (True).
-   `needs_auth` (bool): Указывает, требуется ли аутентификация (False).
-   `use_nodriver` (bool): Указывает, нужно ли использовать драйвер (False).
-   `supports_stream` (bool): Указывает, поддерживает ли потоковую передачу (True).
-   `supports_system_message` (bool): Указывает, поддерживает ли системные сообщения (False).
-   `supports_message_history` (bool): Указывает, поддерживает ли историю сообщений (True).
-   `default_model` (str): Модель по умолчанию ('tulu3-405b').
-   `models` (List[str]): Список поддерживаемых моделей.
-   `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

## Примеры

```python
# Пример использования create_async_generator
import asyncio
from typing import AsyncGenerator, List, Dict

from src.endpoints.gpt4free.g4f.Provider.AllenAI import AllenAI
from src.endpoints.gpt4free.g4f.Provider.AllenAI import Conversation

async def main():
    messages: List[Dict[str, str]] = [{"role": "user", "content": "Hello, how are you?"}]
    model: str = "tulu3-405b"
    conversation = Conversation(model)

    async def stream_response(gen: AsyncGenerator[str, None]):
        async for message in gen:
            print(message)

    generator = await AllenAI.create_async_generator(
        model=model,
        messages=messages,
        conversation=conversation,
        return_conversation=True
    )

    await stream_response(generator)

if __name__ == "__main__":
    asyncio.run(main())