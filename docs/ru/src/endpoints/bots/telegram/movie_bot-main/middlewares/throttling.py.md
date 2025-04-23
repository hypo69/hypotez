# Модуль ThrottlingMiddleware

## Обзор

Модуль `ThrottlingMiddleware` предоставляет класс `ThrottlingMiddleware`, который используется для ограничения частоты обработки сообщений от пользователей в Telegram-боте. Это позволяет предотвратить злоупотребления и защитить бота от перегрузки.

## Подробней

Этот модуль реализует middleware для aiogram, которое позволяет ограничивать количество запросов от одного и того же пользователя в течение определенного времени. Middleware использует `TTLCache` для хранения информации о пользователях и времени их последних запросов.

## Классы

### `ThrottlingMiddleware`

**Описание**: Класс `ThrottlingMiddleware` реализует middleware для ограничения частоты запросов от пользователей.

**Атрибуты**:

- `limit` (TTLCache): Кэш, хранящий информацию о пользователях и времени их последних запросов.

**Методы**:

- `__init__(self, time_limit: int = 2) -> None`: Инициализирует middleware с заданным временем ограничения.
- `__call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]) -> Any`: Выполняет middleware, проверяя, не превысил ли пользователь лимит запросов.

## Методы класса

### `__init__`

```python
def __init__(self, time_limit: int = 2) -> None:
    """
    Инициализирует middleware ThrottlingMiddleware.

    Args:
        time_limit (int, optional): Время в секундах, в течение которого пользователь может отправлять сообщения. По умолчанию 2 секунды.

    Returns:
        None
    """
```

**Назначение**: Инициализирует middleware `ThrottlingMiddleware` с заданным временем ограничения.

**Параметры**:

- `time_limit` (int, optional): Время в секундах, в течение которого пользователь может отправлять сообщения. По умолчанию 2 секунды.

**Как работает функция**:

- Функция инициализирует атрибут `limit` как экземпляр класса `TTLCache` с максимальным размером 10 000 и временем жизни (`ttl`), равным `time_limit`. `TTLCache` используется для хранения идентификаторов пользователей и автоматического удаления их из кэша по истечении времени `time_limit`.

**Примеры**:

```python
# Инициализация ThrottlingMiddleware с ограничением в 5 секунд
middleware = ThrottlingMiddleware(time_limit=5)
```

### `__call__`

```python
async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
) -> Any:
    """
    Выполняет middleware, проверяя, не превысил ли пользователь лимит запросов.

    Args:
        handler (Callable[[Message, Dict[str, Any]], Awaitable[Any]]): Функция-обработчик сообщения.
        event (Message): Объект сообщения Telegram.
        data (Dict[str, Any]): Дополнительные данные.

    Returns:
        Any: Результат работы обработчика.
    """
```

**Назначение**: Выполняет middleware, проверяя, не превысил ли пользователь лимит запросов.

**Параметры**:

- `handler` (Callable[[Message, Dict[str, Any]], Awaitable[Any]]): Функция-обработчик сообщения.
- `event` (Message): Объект сообщения Telegram.
- `data` (Dict[str, Any]): Дополнительные данные.

**Как работает функция**:

1.  Функция проверяет, находится ли идентификатор чата (`event.chat.id`) в кэше `self.limit`.
2.  Если идентификатор чата уже есть в кэше, это означает, что пользователь превысил лимит запросов, и функция не выполняет никаких действий (возвращает `None`).
3.  Если идентификатора чата нет в кэше, функция добавляет его в кэш, устанавливая значение `None`, и вызывает функцию-обработчик `handler` с объектом сообщения `event` и дополнительными данными `data`.

**Примеры**:

```python
# Пример использования ThrottlingMiddleware
async def my_handler(message: Message, data: Dict[str, Any]) -> None:
    print(f"Received message: {message.text}")

# Создание инстанса ThrottlingMiddleware
throttling_middleware = ThrottlingMiddleware(time_limit=3)

# Вызов middleware
# await throttling_middleware(my_handler, message, {})
```

## Параметры класса

- `time_limit` (int, optional): Время в секундах, в течение которого пользователь может отправлять сообщения. По умолчанию 2 секунды.
- `handler` (Callable[[Message, Dict[str, Any]], Awaitable[Any]]): Функция-обработчик сообщения.
- `event` (Message): Объект сообщения Telegram.
- `data` (Dict[str, Any]): Дополнительные данные.

## Примеры

```python
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
import asyncio

# Токен вашего бота
BOT_TOKEN = "YOUR_BOT_TOKEN"

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создание инстанса ThrottlingMiddleware
throttling_middleware = ThrottlingMiddleware(time_limit=3)

# Подключение middleware к диспетчеру
dp.message.middleware(throttling_middleware)

# Обработчик команды /start
@dp.message.handler(CommandStart())
async def start_handler(message: Message):
    await message.answer("Hello! How can I help you?")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())