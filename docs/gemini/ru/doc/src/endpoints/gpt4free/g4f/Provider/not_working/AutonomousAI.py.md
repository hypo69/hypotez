# Модуль `AutonomousAI`

## Обзор

Модуль `AutonomousAI` предоставляет асинхронный интерфейс для взаимодействия с различными AI-моделями через API сервиса Autonomous AI. Поддерживает потоковую передачу данных и системные сообщения.

## Подробней

Этот модуль предназначен для интеграции с сервисом Autonomous AI, позволяя использовать разные модели, такие как `llama`, `qwen_coder`, `hermes`, `vision` и `summary`. Он обеспечивает асинхронный обмен сообщениями, что позволяет эффективно обрабатывать запросы и ответы в реальном времени. Модуль также поддерживает передачу истории сообщений, что полезно для контекстных взаимодействий с AI.

## Классы

### `AutonomousAI`

**Описание**: Класс предоставляет асинхронный интерфейс для работы с AI-моделями через API Autonomous AI.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Добавляет функциональность выбора и управления моделями.

**Атрибуты**:
- `url` (str): Базовый URL сервиса Autonomous AI.
- `api_endpoints` (dict): Словарь с конечными точками API для различных моделей.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (list): Список поддерживаемых моделей.
- `model_aliases` (dict): Словарь с псевдонимами моделей.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для взаимодействия с AI-моделью.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    stream: bool = False,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для взаимодействия с AI-моделью.

    Args:
        cls (Type[AutonomousAI]): Класс `AutonomousAI`.
        model (str): Название используемой модели.
        messages (Messages): Список сообщений для отправки.
        proxy (Optional[str]): Прокси-сервер для использования. По умолчанию `None`.
        stream (bool): Флаг, указывающий на необходимость потоковой передачи данных. По умолчанию `False`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий данные от AI-модели.

    Raises:
        Exception: Если возникает ошибка при взаимодействии с API.

    Как работает функция:
    - Определяет конечную точку API для выбранной модели.
    - Формирует заголовки запроса.
    - Кодирует сообщения в формат JSON и Base64.
    - Отправляет POST-запрос к API с закодированными сообщениями.
    - Получает данные от API и преобразует их в асинхронный поток.
    - Обрабатывает чанки данных, извлекая полезную информацию.
    - Возвращает асинхронный генератор, предоставляющий данные.

    Внутренние функции: Отсутствуют

    """
    ...
```

## Параметры класса

- `cls`: Ссылка на класс `AutonomousAI`.
- `model` (str): Название используемой модели.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (Optional[str]): Прокси-сервер для использования. По умолчанию `None`.
- `stream` (bool): Флаг, указывающий на необходимость потоковой передачи данных. По умолчанию `False`.
- `**kwargs`: Дополнительные аргументы.

## Примеры

```python
# Пример использования create_async_generator
import asyncio
from typing import List, Dict, AsyncGenerator

from src.endpoints.gpt4free.g4f.Provider.not_working.AutonomousAI import AutonomousAI

async def main():
    model = "llama"
    messages: List[Dict[str, str]] = [{"role": "user", "content": "Hello, how are you?"}]
    proxy = None
    stream = True

    generator: AsyncGenerator[str, None] = await AutonomousAI.create_async_generator(
        model=model, messages=messages, proxy=proxy, stream=stream
    )

    async for message in generator:
        print(message, end="")

if __name__ == "__main__":
    asyncio.run(main())