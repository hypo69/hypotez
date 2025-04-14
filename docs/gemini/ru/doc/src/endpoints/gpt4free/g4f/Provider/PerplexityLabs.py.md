# Модуль `PerplexityLabs`

## Обзор

Модуль `PerplexityLabs` предоставляет асинхронный интерфейс для взаимодействия с моделями Perplexity AI Labs. Он позволяет отправлять сообщения к различным моделям, таким как "r1-1776", "sonar-pro" и другие, и получать ответы в виде асинхронного генератора. Модуль использует websockets для обмена данными с сервером Perplexity AI Labs.

## Подробнее

Модуль реализует подключение к API Perplexity AI Labs через websockets, отправляет запросы на генерацию текста и обрабатывает ответы, предоставляя их в виде асинхронного генератора. Он поддерживает различные модели, предоставляемые Perplexity AI Labs, и обеспечивает обработку ошибок при взаимодействии с API.

## Классы

### `PerplexityLabs`

**Описание**: Класс `PerplexityLabs` является асинхронным провайдером для работы с моделями Perplexity AI Labs.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): URL для взаимодействия с Perplexity AI Labs (`https://labs.perplexity.ai`).
- `working` (bool): Указывает, что провайдер в рабочем состоянии (True).
- `default_model` (str): Модель, используемая по умолчанию ("r1-1776").
- `models` (List[str]): Список поддерживаемых моделей.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для взаимодействия с Perplexity AI Labs.

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
        """ Создает асинхронный генератор для взаимодействия с Perplexity AI Labs.
        Args:
            cls (PerplexityLabs): Класс PerplexityLabs.
            model (str): Имя используемой модели.
            messages (Messages): Список сообщений для отправки в модель.
            proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
            **kwargs: Дополнительные параметры.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий результаты от модели.

        Raises:
            ResponseError: При возникновении ошибок при обмене данными с сервером.
            RuntimeError: Если происходит неизвестная ошибка во время обмена данными.

        Как работает функция:
        1.  Функция устанавливает заголовки, необходимые для взаимодействия с API Perplexity AI Labs.
        2.  Создается асинхронная сессия с использованием `StreamSession` для поддержки потоковой передачи данных.
        3.  Выполняется несколько GET и POST запросов для установки соединения через Socket.IO.
        4.  Устанавливается WebSocket соединение для обмена сообщениями в реальном времени.
        5.  Сообщения отправляются в Perplexity AI Labs и обрабатываются ответы, которые передаются через асинхронный генератор.
        6.  Функция обрабатывает ошибки и завершает работу при получении финального сообщения.

        Внутренние функции:
        - Отсутствуют

        """
        ...
```

## Параметры класса

- `url` (str): URL для взаимодействия с Perplexity AI Labs.
- `working` (bool): Указывает, что провайдер в рабочем состоянии.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (List[str]): Список поддерживаемых моделей.

**Примеры**

```python
# Пример использования класса PerplexityLabs для создания асинхронного генератора
import asyncio
from typing import List, Dict, AsyncGenerator

from src.endpoints.gpt4free.g4f.Provider.PerplexityLabs import PerplexityLabs
from src.endpoints.gpt4free.g4f.typing import Messages, AsyncResult

async def main():
    model = "r1-1776"
    messages: Messages = [{"role": "user", "content": "Hello, how are you?"}]

    generator: AsyncGenerator = await PerplexityLabs.create_async_generator(model=model, messages=messages)

    async for message in generator:
        print(message, end="")

if __name__ == "__main__":
    asyncio.run(main())