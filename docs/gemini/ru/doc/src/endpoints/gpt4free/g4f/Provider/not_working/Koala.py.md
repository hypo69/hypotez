# Модуль Koala

## Обзор

Модуль `Koala` предоставляет асинхронный интерфейс для взаимодействия с сервисом `koala.sh` для генерации текста с использованием различных моделей, включая `gpt-4o-mini`. Он поддерживает сохранение истории сообщений и использует асинхронные генераторы для обработки данных.

## Подробней

Этот модуль является частью проекта `hypotez` и предназначен для интеграции с другими компонентами, требующими функциональности генерации текста на основе AI. Он использует `aiohttp` для выполнения асинхронных HTTP-запросов и предоставляет удобный интерфейс для отправки сообщений и получения ответов от сервиса `koala.sh`.

## Классы

### `Koala`

**Описание**: Класс `Koala` предоставляет асинхронный интерфейс для взаимодействия с сервисом `koala.sh`.
**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает функциональность асинхронного генератора.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL сервиса `koala.sh`.
- `api_endpoint` (str): URL API для взаимодействия с `koala.sh`.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4o-mini`).

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от сервиса.
- `_parse_event_stream`: Разбирает поток событий, полученный от сервера.

## Методы класса

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: Optional[str] = None,
        connector: Optional[BaseConnector] = None,
        **kwargs: Any
    ) -> AsyncGenerator[Dict[str, Union[str, int, float, List[Dict[str, Any]], None]], None]:
        """Создает асинхронный генератор для получения ответов от сервиса koala.sh.

        Args:
            model (str): Модель для использования.
            messages (Messages): Список сообщений для отправки.
            proxy (Optional[str], optional): Прокси-сервер для использования. По умолчанию `None`.
            connector (Optional[BaseConnector], optional): HTTP-коннектор для использования. По умолчанию `None`.
            **kwargs (Any): Дополнительные аргументы.

        Returns:
            AsyncGenerator[Dict[str, Union[str, int, float, List[Dict[str, Any]], None]], None]: Асинхронный генератор, возвращающий словарь с данными ответа.

        Raises:
            Exception: Если возникает ошибка при выполнении запроса.
        """
        ...
```

**Назначение**: Создает асинхронный генератор для взаимодействия с сервисом `koala.sh` и получения ответов на основе предоставленных сообщений и модели.

**Параметры**:
- `model` (str): Модель для использования при генерации ответа.
- `messages` (Messages): Список сообщений, отправляемых в запросе.
- `proxy` (Optional[str], optional): Прокси-сервер для использования при подключении. По умолчанию `None`.
- `connector` (Optional[BaseConnector], optional): HTTP-коннектор для использования. По умолчанию `None`.
- `**kwargs` (Any): Дополнительные параметры, которые могут быть переданы.

**Возвращает**:
- `AsyncGenerator[Dict[str, Union[str, int, float, List[Dict[str, Any]], None]], None]`: Асинхронный генератор, возвращающий словарь с данными ответа.

**Как работает функция**:
1. Определяет модель для использования, если она не указана, устанавливает `gpt-4o-mini` по умолчанию.
2. Формирует заголовки HTTP-запроса, включая User-Agent, Referer и другие необходимые параметры.
3. Создает асинхронную сессию `aiohttp` с заданными заголовками и коннектором.
4. Подготавливает данные для отправки в запросе, включая входной текст, историю сообщений пользователя и ассистента.
5. Отправляет POST-запрос на `api_endpoint` с данными и заголовками.
6. Обрабатывает поток событий, полученный от сервера, и возвращает каждый чанк данных через асинхронный генератор.

### `_parse_event_stream`

```python
    @staticmethod
    async def _parse_event_stream(response: ClientResponse) -> AsyncGenerator[Dict[str, Any], None]:
        """Разбирает поток событий, полученный от сервера.

        Args:
            response (ClientResponse): Объект HTTP-ответа от сервера.

        Returns:
            AsyncGenerator[Dict[str, Any], None]: Асинхронный генератор, возвращающий словарь с данными из потока событий.

        Raises:
            Exception: Если возникает ошибка при разборе данных.
        """
        ...
```

**Назначение**: Разбирает поток событий, полученный от сервера `koala.sh`, и извлекает данные из каждого чанка.

**Параметры**:
- `response` (ClientResponse): Объект HTTP-ответа от сервера.

**Возвращает**:
- `AsyncGenerator[Dict[str, Any], None]`: Асинхронный генератор, возвращающий словарь с данными из потока событий.

**Как работает функция**:
1. Итерируется по содержимому ответа (`response.content`) асинхронно.
2. Проверяет, начинается ли чанк с префикса `b"data: "`.
3. Если да, извлекает данные, декодирует их из JSON и возвращает через генератор.

## Примеры

Пример использования класса `Koala` для создания асинхронного генератора и получения ответов от сервиса:

```python
import asyncio
from typing import List, Dict

from aiohttp import ClientSession

# from g4f.Provider.Koala import Koala  # Предполагается, что Koala находится в g4f.Provider

async def main():
    messages: List[Dict[str, str]] = [
        {"role": "user", "content": "Hello, Koala!"},
    ]

    async for message in Koala.create_async_generator(model="gpt-4o-mini", messages=messages):
        print(message)

if __name__ == "__main__":
    asyncio.run(main())
```

Этот пример показывает, как создать список сообщений, вызвать `create_async_generator` для получения асинхронного генератора и затем итерироваться по ответам, выводимым на экран.