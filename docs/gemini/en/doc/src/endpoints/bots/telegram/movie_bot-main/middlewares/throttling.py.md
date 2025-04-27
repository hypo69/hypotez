# Throttling Middleware

## Overview

This module defines the `ThrottlingMiddleware` class, which implements a simple throttling mechanism for Telegram bot messages. It prevents users from sending too many messages within a specified time interval.

## Details

The `ThrottlingMiddleware` is used to manage the rate at which messages are processed by the Telegram bot. This middleware helps prevent spamming and resource exhaustion by limiting the number of messages a user can send within a given time period.

The middleware uses a cache to track the last time a user sent a message. If a user tries to send another message before the specified time limit has elapsed, the middleware blocks the message and does not pass it to the handler.

## Classes

### `ThrottlingMiddleware`

**Description**: Класс, реализующий простую механику ограничения частоты отправки сообщений в Telegram боте. 

**Inherits**:  `aiogram.BaseMiddleware`

**Attributes**:

- `limit (TTLCache)`: Кэш для отслеживания последнего времени отправки сообщения пользователем.

**Methods**:

- `__call__`
    - **Purpose**: Метод, вызываемый при обработке сообщения ботом. Проверяет, не превышено ли ограничение по частоте отправки сообщений.

    - **Parameters**:
        - `handler (Callable[[Message, Dict[str, Any]], Awaitable[Any]])`: Обработчик сообщения.
        - `event (Message)`: Объект, представляющий сообщение пользователя.
        - `data (Dict[str, Any])`: Данные, передаваемые в обработчик.

    - **Returns**:
        - `Any`: Возвращает результат выполнения обработчика или `None`, если ограничение по частоте отправки сообщений превышено.

    - **How the Function Works**:
        - Метод проверяет, есть ли идентификатор чата пользователя в кэше. Если есть, значит сообщение было отправлено недавно, и метод возвращает `None`, блокируя его обработку.
        - Если идентификатора нет в кэше, значит прошло достаточно времени с момента последнего сообщения, и метод добавляет идентификатор чата в кэш.
        - После этого метод вызывает обработчик `handler` и возвращает результат его выполнения.

    - **Examples**:

```python
        from aiogram.types import Message
        from typing import Dict

        async def handler(event: Message, data: Dict[str, Any]) -> str:
            return "Message received!"

        middleware = ThrottlingMiddleware(time_limit=2)  # Создаем экземпляр класса

        event = Message(chat={'id': 123456789})  # Создаем пример сообщения
        data = {}  # Создаем пример данных

        result = await middleware(handler, event, data)  # Вызываем метод `__call__`

        if result is None:
            print("Message blocked due to throttling")
        else:
            print(result)  # Выводим результат выполнения обработчика
```