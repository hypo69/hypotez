# Модуль ThrottlingMiddleware

## Обзор

Модуль `ThrottlingMiddleware` реализует класс `ThrottlingMiddleware`, который является промежуточным слоем (middleware) для aiogram, предназначенным для ограничения частоты обработки сообщений от одного и того же чата. Это позволяет предотвратить злоупотребления и защитить бота от перегрузки.

## Подробней

Данный модуль используется для контроля за интенсивностью запросов к Telegram боту, предотвращая отправку большого количества сообщений за короткий промежуток времени. Он использует кэш `TTLCache` для хранения идентификаторов чатов и времени последнего обращения, чтобы определить, следует ли обрабатывать входящее сообщение или отклонить его.

## Классы

### `ThrottlingMiddleware`

**Описание**:
Класс `ThrottlingMiddleware` является промежуточным слоем для aiogram, который ограничивает частоту обработки сообщений от одного и того же чата.

**Наследует**:
`BaseMiddleware` из библиотеки `aiogram`.

**Атрибуты**:
- `limit` (TTLCache): Кэш для хранения идентификаторов чатов и времени последнего обращения.

**Методы**:
- `__init__(self, time_limit: int = 2) -> None`: Конструктор класса.
- `__call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]) -> Any`: Асинхронный метод, вызываемый при каждом входящем сообщении.

### `__init__(self, time_limit: int = 2) -> None`

**Назначение**:
Инициализирует объект `ThrottlingMiddleware`.

**Параметры**:
- `time_limit` (int, optional): Время в секундах, в течение которого сообщения от одного и того же чата будут ограничены. По умолчанию `2`.

**Как работает функция**:
- Инициализирует кэш `self.limit` с максимальным размером 10 000 элементов и временем жизни `time_limit`.

```python
    def __init__(self, time_limit: int = 2) -> None:
        self.limit = TTLCache(maxsize=10_000, ttl=time_limit)
```

### `__call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]) -> Any`

**Назначение**:
Асинхронный метод, вызываемый при каждом входящем сообщении. Определяет, следует ли обрабатывать сообщение или отклонить его на основе ограничений по времени.

**Параметры**:
- `handler` (Callable[[Message, Dict[str, Any]], Awaitable[Any]]): Функция-обработчик сообщения.
- `event` (Message): Объект сообщения от Telegram.
- `data` (Dict[str, Any]): Дополнительные данные, переданные в обработчик.

**Возвращает**:
- `Any`: Результат выполнения обработчика сообщения, если сообщение не было отклонено. В противном случае - `None`.

**Как работает функция**:
- Проверяет, находится ли идентификатор чата (`event.chat.id`) в кэше `self.limit`.
- Если идентификатор чата уже есть в кэше, функция немедленно завершается, и сообщение не обрабатывается.
- Если идентификатора чата нет в кэше, он добавляется в кэш, и вызывается функция-обработчик сообщения (`handler`).

**Примеры**:

Пример использования `ThrottlingMiddleware` в aiogram:

```python
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from src.endpoints.bots.telegram.movie_bot-main.middlewares.throttling import ThrottlingMiddleware
import asyncio

# Инициализация бота и диспетчера
bot = Bot(token="YOUR_TELEGRAM_BOT_TOKEN")
dp = Dispatcher()

# Регистрация промежуточного слоя ThrottlingMiddleware
dp.message.middleware(ThrottlingMiddleware(time_limit=2))

# Обработчик команды /start
@dp.message.handler(CommandStart())
async def start_command(message: Message):
    await message.answer("Привет! Я бот, который ограничивает частоту сообщений.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
```

## Параметры класса

- `limit` (TTLCache): Кэш, хранящий идентификаторы чатов и время последнего обращения. Используется для определения, следует ли обрабатывать входящее сообщение.
- `time_limit` (int): Время в секундах, в течение которого сообщения от одного и того же чата будут ограничены. Используется при инициализации `TTLCache`.