# Документация для `throttling.py`

## Обзор

Данный модуль содержит класс `ThrottlingMiddleware`, который используется для ограничения частоты обработки сообщений от пользователей в Telegram-боте. Это позволяет предотвратить злоупотребление ботом и снизить нагрузку на сервер.

## Подробнее

Модуль реализует middleware для aiogram, которое позволяет ограничивать количество запросов от одного и того же чата в течение заданного времени. В основе работы лежит использование кэша `TTLCache` для хранения идентификаторов чатов и времени последнего обращения.

## Классы

### `ThrottlingMiddleware`

**Описание**: Middleware для ограничения частоты обработки сообщений от пользователей.
**Наследует**: `BaseMiddleware` из `aiogram`.

**Атрибуты**:
- `limit` (TTLCache): Кэш для хранения идентификаторов чатов и времени последнего обращения.

**Методы**:
- `__init__`: Инициализирует middleware с заданным временем ограничения.
- `__call__`: Вызывается для каждого входящего сообщения и проверяет, не превышен ли лимит запросов для данного чата.

#### `__init__`

```python
def __init__(self, time_limit: int = 2) -> None:
    """
    Инициализирует middleware с заданным временем ограничения.

    Args:
        time_limit (int, optional): Время в секундах, в течение которого разрешается только один запрос от чата. По умолчанию 2 секунды.

    Returns:
        None
    """
```

#### `__call__`

```python
async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
) -> Any:
    """
    Вызывается для каждого входящего сообщения и проверяет, не превышен ли лимит запросов для данного чата.

    Args:
        handler (Callable[[Message, Dict[str, Any]], Awaitable[Any]]): Функция-обработчик сообщения.
        event (Message): Объект сообщения от Telegram.
        data (Dict[str, Any]): Дополнительные данные.

    Returns:
        Any: Результат обработки сообщения обработчиком.

    Как работает функция:
    - Функция проверяет, есть ли идентификатор чата в кэше `self.limit`.
    - Если идентификатор чата есть в кэше, функция немедленно возвращает управление, предотвращая дальнейшую обработку сообщения.
    - Если идентификатора чата нет в кэше, функция добавляет его в кэш и вызывает функцию-обработчик `handler` для обработки сообщения.
    """
```

## Примеры

Пример использования `ThrottlingMiddleware` для ограничения частоты запросов:

```python
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from src.endpoints.bots.telegram.movie_bot-main.middlewares.throttling import ThrottlingMiddleware
from src.logger import logger

# Инициализация бота и диспетчера
bot = Bot(token="YOUR_TELEGRAM_BOT_TOKEN")
dp = Dispatcher()

# Регистрация middleware
dp.message.middleware(ThrottlingMiddleware(time_limit=2))

# Обработчик команды /start
@dp.message(CommandStart())
async def start_handler(message: Message):
    """
    Обработчик команды /start.

    Args:
        message (Message): Объект сообщения.

    Returns:
        None
    """
    try:
        await message.answer("Привет! Я бот, который ограничивает количество запросов.")
    except Exception as ex:
        logger.error("Ошибка при отправке ответа", ex, exc_info=True)

# Запуск бота
async def main():
    """
    Запускает бота.

    Returns:
        None
    """
    try:
        await dp.start_polling(bot)
    except Exception as ex:
        logger.error("Ошибка при запуске бота", ex, exc_info=True)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())