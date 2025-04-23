# Документация модуля `H2o`

## Обзор

Модуль `H2o` предоставляет асинхронный генератор для взаимодействия с моделью `h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1` через API `gpt-gm.h2o.ai`. Он позволяет отправлять запросы к модели и получать ответы в виде асинхронного генератора. Модуль использует библиотеку `aiohttp` для асинхронных HTTP-запросов.

## Подробнее

Модуль предназначен для интеграции с другими частями проекта `hypotez`, где требуется взаимодействие с большими языковыми моделями (LLM) через асинхронные запросы. Он предоставляет удобный интерфейс для форматирования запросов и получения ответов в виде генератора, что позволяет эффективно обрабатывать большие объемы данных.

## Классы

### `H2o(AsyncGeneratorProvider)`

**Описание**: Класс `H2o` является провайдером асинхронного генератора, который взаимодействует с API `gpt-gm.h2o.ai`.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL-адрес API `gpt-gm.h2o.ai`.
- `model` (str): Название модели, используемой по умолчанию: `h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1`.

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для получения ответов от модели.

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
        """Создает асинхронный генератор для получения ответов от модели.

        Args:
            model (str): Название модели для использования. Если не указано, используется значение по умолчанию `cls.model`.
            messages (Messages): Список сообщений для отправки в модель.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            **kwargs: Дополнительные параметры, которые будут переданы в запрос.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий текст от модели.

        Raises:
            aiohttp.ClientResponseError: Если возникает ошибка при выполнении HTTP-запроса.

        Как работает функция:
        - Функция принимает модель, список сообщений и дополнительные параметры.
        - Устанавливает заголовки, включая Referer.
        - Создает асинхронную сессию с использованием `aiohttp.ClientSession`.
        - Отправляет POST-запрос к `/settings` для принятия условий использования.
        - Отправляет POST-запрос к `/conversation` для создания нового диалога.
        - Форматирует входные сообщения с помощью `format_prompt`.
        - Отправляет POST-запрос к `/conversation/{conversationId}` с данными для получения ответа от модели.
        - Получает ответ в виде потока и извлекает текстовые токены.
        - Отправляет DELETE-запрос к `/conversation/{conversationId}` для завершения диалога.

        Примеры:
            >>> model_name = "h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1"
            >>> messages = [{"role": "user", "content": "Hello, how are you?"}]
            >>> async def run():
            ...     async for token in H2o.create_async_generator(model=model_name, messages=messages):
            ...         print(token, end="")
            >>> import asyncio
            >>> asyncio.run(run())
            I am doing well, thank you for asking. How can I assist you today?
        """
```

## Параметры класса

- `url` (str): URL-адрес API `gpt-gm.h2o.ai`.
- `model` (str): Название модели, используемой по умолчанию: `h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1`.

## Примеры

Пример использования класса `H2o` для получения ответа от модели:

```python
import asyncio
from src.endpoints.gpt4free.g4f.Provider.deprecated import H2o

async def main():
    messages = [{"role": "user", "content": "Напиши небольшой стих о Python."}]
    async for token in H2o.create_async_generator(model="h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1", messages=messages):
        print(token, end="")

if __name__ == "__main__":
    asyncio.run(main())