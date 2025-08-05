# Модуль Acytoo

## Обзор

Модуль `Acytoo` предоставляет асинхронный генератор для взаимодействия с сервисом чата Acytoo. Он позволяет отправлять сообщения и получать ответы в режиме реального времени, поддерживая историю сообщений и модель `gpt-3.5-turbo`.

## Подробней

Модуль предназначен для интеграции с сервисом Acytoo через его API. Он использует `aiohttp` для асинхронных запросов и предоставляет класс `Acytoo` для удобного взаимодействия. Класс `Acytoo` является подклассом `AsyncGeneratorProvider` и реализует метод `create_async_generator` для создания асинхронного генератора, который отправляет запросы к API Acytoo и возвращает ответы.

## Классы

### `Acytoo`

**Описание**: Класс `Acytoo` предоставляет интерфейс для взаимодействия с сервисом чата Acytoo.

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:
- `url` (str): URL-адрес сервиса Acytoo.
- `working` (bool): Флаг, указывающий, работает ли сервис.
- `supports_message_history` (bool): Флаг, указывающий, поддерживается ли история сообщений.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий, поддерживается ли модель `gpt-3.5-turbo`.

**Методы**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для отправки сообщений и получения ответов от сервиса Acytoo.

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
    """Создает асинхронный генератор для отправки сообщений и получения ответов от сервиса Acytoo.

    Args:
        cls (Acytoo): Класс Acytoo.
        model (str): Модель для использования.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от сервиса Acytoo.

    Raises:
        aiohttp.ClientResponseError: Если возникает ошибка при отправке запроса.

    
    - Создает сессию клиента aiohttp с заголовками, полученными из функции `_create_header()`.
    - Отправляет POST-запрос к API Acytoo с использованием URL-адреса, прокси и JSON-данных, полученных из функции `_create_payload()`.
    - Проверяет статус ответа и вызывает исключение, если произошла ошибка.
    - Итерируется по содержимому ответа в виде потока байтов.
    - Декодирует каждый чанк байтов и возвращает его через генератор.

    Внутренние функции:
        Отсутствуют
    """
    ...
```

**Примеры**:
```python
# Пример использования create_async_generator
import asyncio
from typing import List, Dict, AsyncGenerator, Any

from aiohttp import ClientSession

# messages: Messages = [{"role": "user", "content": "Hello, Acytoo!"}]
# async def main():
#     async for response in Acytoo.create_async_generator(model="gpt-3.5-turbo", messages=messages):
#         print(response, end="")

# if __name__ == "__main__":
#     asyncio.run(main())
```

## Функции

### `_create_header`

```python
def _create_header():
    """Создает словарь с заголовками для HTTP-запроса.

    Args:
        Отсутствуют

    Returns:
        dict: Словарь с заголовками 'accept' и 'content-type'.

    
    - Функция создает и возвращает словарь, содержащий заголовки, необходимые для выполнения HTTP-запроса к API Acytoo.
    - Заголовок 'accept' указывает, что клиент принимает любой тип контента ('*/*').
    - Заголовок 'content-type' указывает, что тело запроса имеет формат JSON ('application/json').

    Внутренние функции:
        Отсутствуют
    """
    ...
```

### `_create_payload`

```python
def _create_payload(messages: Messages, temperature: float = 0.5, **kwargs):
    """Создает словарь с полезной нагрузкой (payload) для отправки в HTTP-запросе.

    Args:
        messages (Messages): Список сообщений для отправки.
        temperature (float, optional): Температура модели. По умолчанию 0.5.
        **kwargs: Дополнительные аргументы.

    Returns:
        dict: Словарь с данными для отправки в теле запроса.

    
    - Функция создает и возвращает словарь, содержащий полезную нагрузку для отправки в теле HTTP-запроса к API Acytoo.
    - Ключ 'key' содержит пустую строку.
    - Ключ 'model' содержит имя модели ('gpt-3.5-turbo').
    - Ключ 'messages' содержит список сообщений.
    - Ключ 'temperature' содержит значение температуры модели.
    - Ключ 'password' содержит пустую строку.

    Внутренние функции:
        Отсутствуют
    """
    ...
```

**Примеры**:

```python
# Пример использования _create_payload
messages: Messages = [{"role": "user", "content": "Hello, Acytoo!"}]
payload = _create_payload(messages=messages, temperature=0.7)
print(payload)
# {'key': '', 'model': 'gpt-3.5-turbo', 'messages': [{'role': 'user', 'content': 'Hello, Acytoo!'}], 'temperature': 0.7, 'password': ''}