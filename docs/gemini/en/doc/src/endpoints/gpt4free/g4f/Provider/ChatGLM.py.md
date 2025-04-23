# Документация для модуля ChatGLM

## Обзор

Модуль `ChatGLM` предназначен для взаимодействия с API ChatGLM для генерации текста. Он поддерживает асинхронный стриминг ответов и предоставляет возможность использования прокси. Модуль включает в себя классы `ChatGLM`, `AsyncGeneratorProvider` и `ProviderModelMixin`.

## Подробнее

Модуль предоставляет класс `ChatGLM`, который наследуется от `AsyncGeneratorProvider` и `ProviderModelMixin`. Он использует `aiohttp` для выполнения асинхронных HTTP-запросов к API ChatGLM. Модуль поддерживает стриминг ответов, но не поддерживает системные сообщения и историю сообщений.

## Классы

### `ChatGLM`

**Описание**: Класс для взаимодействия с API ChatGLM.

**Наследует**:
- `AsyncGeneratorProvider`: Предоставляет базовый функционал для асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет функционал для работы с моделями.

**Атрибуты**:
- `url` (str): URL сервиса ChatGLM.
- `api_endpoint` (str): URL API для стриминга.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер стриминг.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию (`"glm-4"`).
- `models` (list): Список поддерживаемых моделей (`[default_model]`).

**Методы**:
- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для получения ответов от API ChatGLM.

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
    Создает асинхронный генератор для получения ответов от API ChatGLM.

    Args:
        cls (ChatGLM): Класс ChatGLM.
        model (str): Используемая модель.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий текст от API ChatGLM.
    
    Как работает функция:
    - Генерируется `device_id` в формате UUID.
    - Формируются заголовки запроса, включая `device_id`.
    - Создается асинхронная сессия с использованием `aiohttp.ClientSession`.
    - Формируется JSON-payload с сообщениями для отправки в API.
    - Отправляется POST-запрос к `cls.api_endpoint` с использованием асинхронной сессии.
    - Обрабатывается ответ от API, извлекая данные из каждого чанка.
    - Извлекается контент из JSON-данных и генерируется текст.
    - Если статус ответа `'finish'`, генерируется `FinishReason("stop")`.
    - Обрабатываются ошибки JSON при декодировании.

    """
```

## Примеры

Пример использования класса `ChatGLM`:

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.ChatGLM import ChatGLM
from src.endpoints.gpt4free.g4f.typing import Message

async def main():
    messages: list[Message] = [
        {"role": "user", "content": "Привет, как дела?"}
    ]
    
    async for response in ChatGLM.create_async_generator(model="glm-4", messages=messages):
        print(response, end="")

if __name__ == "__main__":
    asyncio.run(main())