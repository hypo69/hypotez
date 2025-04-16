# Модуль `Berlin`

## Обзор

Модуль `Berlin` представляет собой асинхронный провайдер для взаимодействия с API сервиса ai.berlin4h.top. Он позволяет генерировать ответы на основе предоставленных сообщений, используя модель GPT-3.5 Turbo. Модуль предназначен для использования в асинхронных приложениях и поддерживает работу через прокси.

## Подробнее

Модуль предоставляет класс `Berlin`, который наследуется от `AsyncGeneratorProvider`. Он использует `aiohttp` для выполнения асинхронных HTTP-запросов к API. Для работы с API требуется токен, который получается при логине. Модуль поддерживает форматирование запросов и обработку ответов в формате JSON.

## Классы

### `Berlin`

**Описание**: Класс `Berlin` является асинхронным провайдером для взаимодействия с API сервиса ai.berlin4h.top.
**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL API сервиса (https://ai.berlin4h.top).
- `working` (bool): Флаг, указывающий на работоспособность провайдера (по умолчанию `False`).
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели GPT-3.5 Turbo (по умолчанию `True`).
- `_token` (str | None): Токен авторизации для доступа к API (изначально `None`).

**Методы**:
- `create_async_generator`: Асинхронный генератор для получения ответов от API.

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
    Создает асинхронный генератор для получения ответов от API.

    Args:
        model (str): Название модели для использования.
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные параметры для передачи в API.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от API.

    Raises:
        RuntimeError: Если возникает ошибка при обработке ответа от API.

    """
```

**Назначение**: Создает асинхронный генератор для получения ответов от API сервиса ai.berlin4h.top.

**Параметры**:
- `cls` (Berlin): Ссылка на класс `Berlin`.
- `model` (str): Название модели для использования. Если не указано, используется "gpt-3.5-turbo".
- `messages` (Messages): Список сообщений для отправки в API.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры для передачи в API.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий ответы от API.

**Вызывает исключения**:
- `RuntimeError`: Если возникает ошибка при обработке ответа от API.

**Как работает функция**:
1. Проверяет наличие токена авторизации. Если токен отсутствует, выполняет запрос на получение токена, используя учетные данные для бесплатного доступа.
2. Формирует заголовки запроса, включая токен авторизации.
3. Форматирует сообщения для отправки в API.
4. Формирует данные запроса, включая prompt, model, temperature, presence_penalty, frequency_penalty, max_tokens и другие параметры.
5. Выполняет POST-запрос к API сервиса ai.berlin4h.top.
6. Получает ответ от API и обрабатывает его по частям (chunks).
7. Извлекает содержимое из каждого чанка и возвращает его через генератор.
8. В случае ошибки при обработке ответа, вызывает исключение `RuntimeError`.

**Примеры**:

```python
import asyncio
from typing import AsyncGenerator, List, Dict

from g4f.Provider import Berlin

async def main():
    messages: List[Dict[str, str]] = [
        {"role": "user", "content": "Привет, как дела?"}
    ]

    async for message in Berlin.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(message, end="")

if __name__ == "__main__":
    asyncio.run(main())
```

## Параметры класса

- `url` (str): URL API сервиса (https://ai.berlin4h.top).
- `working` (bool): Флаг, указывающий на работоспособность провайдера (по умолчанию `False`).
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели GPT-3.5 Turbo (по умолчанию `True`).
- `_token` (str | None): Токен авторизации для доступа к API (изначально `None`).

**Примеры**:

```python
# Пример создания экземпляра класса Berlin
berlin_provider = Berlin()
print(f"URL: {berlin_provider.url}")
print(f"Supports GPT-3.5 Turbo: {berlin_provider.supports_gpt_35_turbo}")
```