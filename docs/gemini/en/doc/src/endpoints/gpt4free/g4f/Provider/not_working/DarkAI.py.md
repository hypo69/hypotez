# Module DarkAI

## Overview

Модуль `DarkAI` представляет собой асинхронный провайдер для работы с API DarkAI. Он позволяет генерировать текст на основе предоставленных сообщений, используя различные модели, такие как `gpt-4o`, `gpt-3.5-turbo` и `llama-3-70b`. Модуль поддерживает потоковую передачу данных и использует `aiohttp` для асинхронных HTTP-запросов.

## More details

Модуль предназначен для интеграции с другими частями проекта `hypotez`, где требуется взаимодействие с API DarkAI для генерации текста. Он обеспечивает асинхронное взаимодействие, что позволяет избежать блокировки основного потока выполнения.

## Classes

### `DarkAI`

**Description**: Класс `DarkAI` является асинхронным провайдером и реализует методы для взаимодействия с API DarkAI.

**Inherits**:
- `AsyncGeneratorProvider`: Обеспечивает поддержку асинхронной генерации данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями провайдера.

**Attributes**:
- `url` (str): URL API DarkAI.
- `api_endpoint` (str): Конечная точка API DarkAI для отправки запросов.
- `working` (bool): Указывает, работает ли провайдер в данный момент.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных.
- `default_model` (str): Модель, используемая по умолчанию (llama-3-70b).
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

**Working principle**:
Класс `DarkAI` использует `aiohttp` для отправки асинхронных POST-запросов к API DarkAI. Он форматирует входные сообщения в формат, ожидаемый API, и обрабатывает потоковый ответ, генерируя текст по частям.

**Methods**:
- `create_async_generator`: Создает асинхронный генератор для получения текста от API DarkAI.

## Class Methods

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
    """Создает асинхронный генератор для получения текста от API DarkAI.

    Args:
        cls (DarkAI): Ссылка на класс.
        model (str): Имя модели для использования.
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий текст от API.

    How the function works:
    - Функция принимает модель, сообщения и прокси (опционально).
    - Извлекает имя модели с помощью `cls.get_model(model)`.
    - Форматирует сообщения с помощью `format_prompt(messages)`.
    - Создает заголовок запроса, содержащий `accept`, `content-type` и `user-agent`.
    - Создает асинхронную сессию с `ClientSession` с заданными заголовками и таймаутом.
    - Отправляет POST-запрос к `cls.api_endpoint` с форматированными сообщениями и моделью.
    - Читает ответ по частям и декодирует его, извлекая текстовые фрагменты.
    - Генерирует текстовые фрагменты, полученные от API.

    Internal functions:
    - Отсутствуют.

    """
```

## Class Parameters

- `cls`: Ссылка на класс `DarkAI`. Используется для доступа к атрибутам класса, таким как `api_endpoint` и `get_model`.
- `model` (str): Имя модели, которую необходимо использовать для генерации текста. Это значение передается в API DarkAI для указания, какая модель должна быть использована для генерации ответа.
- `messages` (Messages): Список сообщений, которые будут отправлены в API DarkAI. Эти сообщения содержат контекст и запрос, на основе которого API должен сгенерировать текст.
- `proxy` (str, optional): Адрес прокси-сервера, который будет использоваться для отправки запроса. Если прокси не указан, запрос будет отправлен напрямую.
- `**kwargs`: Дополнительные параметры, которые могут быть переданы в API.

## Examples

```python
# Пример использования create_async_generator
import asyncio
from src.endpoints.gpt4free.g4f.Provider.not_working.DarkAI import DarkAI

async def main():
    model = "gpt-3.5-turbo"
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    async for chunk in DarkAI.create_async_generator(model=model, messages=messages):
        print(chunk, end="")

if __name__ == "__main__":
    asyncio.run(main())