# Модуль ThrottlingMiddleware

## Обзор

Модуль `ThrottlingMiddleware` предоставляет класс `ThrottlingMiddleware`, который является middleware для aiogram, предназначенным для ограничения частоты обращений пользователей в Telegram-боте. Он использует `TTLCache` для хранения информации о последних запросах от каждого пользователя и предотвращения слишком частых запросов.

## Подробнее

Этот модуль реализует механизм защиты от злоупотреблений ботом, позволяя контролировать количество запросов, которые может сделать пользователь за определенный период времени. Это особенно полезно для предотвращения спама или DDoS-атак на бота.

## Классы

### `ThrottlingMiddleware`

**Описание**: Middleware для aiogram, реализующий ограничение частоты запросов.

**Наследует**:
- `BaseMiddleware` из библиотеки `aiogram`.

**Атрибуты**:
- `limit` (TTLCache): Кэш, хранящий информацию о последних запросах от каждого пользователя.

**Методы**:
- `__init__(self, time_limit: int = 2) -> None`: Инициализирует middleware с заданным временем ограничения.
- `__call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]) -> Any`: Вызывается при каждом входящем сообщении. Проверяет, не превысил ли пользователь лимит запросов.

### `__init__`

```python
def __init__(self, time_limit: int = 2) -> None:
    """
    Инициализирует middleware с заданным временем ограничения.

    Args:
        time_limit (int, optional): Время в секундах, в течение которого пользователь может сделать только один запрос. По умолчанию 2 секунды.
    """
```

**Как работает функция**:

- Функция инициализирует экземпляр класса `ThrottlingMiddleware`.
- Создает кэш `TTLCache` с максимальным размером 10 000 элементов и временем жизни `time_limit` секунд. Этот кэш используется для хранения информации о том, когда последний раз пользователь взаимодействовал с ботом.

### `__call__`

```python
async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
) -> Any:
    """
    Вызывается при каждом входящем сообщении. Проверяет, не превысил ли пользователь лимит запросов.

    Args:
        handler (Callable[[Message, Dict[str, Any]], Awaitable[Any]]): Обработчик сообщения.
        event (Message): Объект сообщения от пользователя.
        data (Dict[str, Any]): Дополнительные данные.

    Returns:
        Any: Результат обработки сообщения.
    """
```

**Как работает функция**:

- Функция `__call__` является точкой входа для middleware. Она вызывается каждый раз, когда aiogram получает сообщение.
- Проверяет, есть ли идентификатор чата пользователя (`event.chat.id`) в кэше `self.limit`.
- Если идентификатор чата уже есть в кэше, это означает, что пользователь недавно отправлял сообщение, и функция немедленно возвращает управление, игнорируя текущий запрос.
- Если идентификатора чата нет в кэше, функция добавляет его в кэш и вызывает обработчик сообщения (`handler`), передавая ему объект сообщения (`event`) и дополнительные данные (`data`).

**Примеры**:

```python
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import F
import asyncio

# Инициализация бота и диспетчера
bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher()

# Подключение middleware
dp.message.middleware(ThrottlingMiddleware(time_limit=3))

# Обработчик команды /start
@dp.message.handler(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет! Как дела?")

# Обработчик текстовых сообщений
@dp.message.handler(F.text)
async def text_handler(message: types.Message):
    await message.answer("Вы отправили: " + message.text)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
```
В этом примере `ThrottlingMiddleware` применяется ко всем сообщениям, обрабатываемым диспетчером. Пользователь не сможет отправлять сообщения чаще, чем раз в 3 секунды.