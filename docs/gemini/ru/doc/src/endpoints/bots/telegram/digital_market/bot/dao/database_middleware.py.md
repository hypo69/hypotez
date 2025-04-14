# Модуль для работы с middleware базы данных
=================================================

Модуль содержит классы для создания middleware, обеспечивающих интеграцию с базой данных при обработке сообщений и callback-запросов в Telegram боте.

## Обзор

Этот модуль предоставляет базовые классы middleware для работы с базой данных асинхронно, используя `aiogram`. Он определяет абстрактный класс `BaseDatabaseMiddleware`, который управляет сессией базы данных, и два подкласса: `DatabaseMiddlewareWithoutCommit` и `DatabaseMiddlewareWithCommit`, которые определяют, следует ли автоматически применять изменения к базе данных после обработки запроса.

## Подробнее

Основное назначение модуля - упростить интеграцию с базой данных в обработчиках `aiogram`. `BaseDatabaseMiddleware` создает сессию, передает ее в обработчик и автоматически закрывает сессию после завершения обработчика. Подклассы определяют, следует ли автоматически фиксировать изменения (commit) в базе данных.

## Классы

### `BaseDatabaseMiddleware`

**Описание**: Базовый класс middleware для работы с базой данных. Обеспечивает создание, передачу и закрытие сессии базы данных.

**Наследует**: `aiogram.BaseMiddleware`

**Атрибуты**:
- Нет предопределенных атрибутов, но использует атрибут `data` для передачи сессии базы данных обработчикам.

**Методы**:
- `__call__`: Асинхронный метод, вызываемый при обработке события.
- `set_session`: Метод для установки сессии в словарь данных.
- `after_handler`: Метод для выполнения действий после вызова хендлера (например, коммит).

**Принцип работы**:
1. При получении события `__call__` создает асинхронную сессию базы данных с помощью `async_session_maker()`.
2. Вызывает метод `set_session` для передачи сессии в словарь `data`, который будет доступен обработчику.
3. Вызывает обработчик `handler` с событием `event` и данными `data`.
4. После завершения обработчика вызывает метод `after_handler` для выполнения дополнительных действий (например, коммит).
5. В случае возникновения исключения выполняет откат изменений (rollback) и повторно выбрасывает исключение.
6. В блоке `finally` закрывает сессию базы данных.

### `DatabaseMiddlewareWithoutCommit`

**Описание**: Middleware для работы с базой данных без автоматического применения изменений.

**Наследует**: `BaseDatabaseMiddleware`

**Методы**:
- `set_session`: Устанавливает сессию базы данных в словаре `data` под ключом `'session_without_commit'`.

**Принцип работы**:
- При вызове метода `set_session` сохраняет сессию базы данных в словаре `data` под ключом `'session_without_commit'`, чтобы обработчик мог использовать эту сессию для выполнения операций с базой данных, но не фиксирует изменения автоматически.

### `DatabaseMiddlewareWithCommit`

**Описание**: Middleware для работы с базой данных с автоматическим применением изменений.

**Наследует**: `BaseDatabaseMiddleware`

**Методы**:
- `set_session`: Устанавливает сессию базы данных в словаре `data` под ключом `'session_with_commit'`.
- `after_handler`: Применяет изменения к базе данных после вызова обработчика, вызывая метод `session.commit()`.

**Принцип работы**:
- При вызове метода `set_session` сохраняет сессию базы данных в словаре `data` под ключом `'session_with_commit'`, чтобы обработчик мог использовать эту сессию для выполнения операций с базой данных.
- После успешного завершения обработчика метод `after_handler` автоматически применяет изменения к базе данных, вызывая метод `session.commit()`.

## Методы класса

### `BaseDatabaseMiddleware`

#### `__call__`

```python
async def __call__(
    self,
    handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
    event: Message | CallbackQuery,
    data: Dict[str, Any]
) -> Any:
    """
    Асинхронный метод, вызываемый при обработке события.

    Args:
        handler (Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]]):
            Функция-обработчик, которая будет вызвана для обработки события.
        event (Message | CallbackQuery): Объект события (сообщение или callback-запрос).
        data (Dict[str, Any]): Словарь данных, передаваемый обработчику.

    Returns:
        Any: Результат выполнения обработчика.

    Raises:
        Exception: Если во время обработки произошла ошибка, выполняет откат изменений и пробрасывает исключение.

    Как работает функция:
    - Создает асинхронную сессию базы данных.
    - Устанавливает сессию в словаре данных.
    - Вызывает обработчик.
    - Выполняет действия после обработчика.
    - Обрабатывает исключения и закрывает сессию.
    """
    ...
```

#### `set_session`

```python
def set_session(self, data: Dict[str, Any], session) -> None:
    """
    Метод для установки сессии в словарь данных.

    Args:
        data (Dict[str, Any]): Словарь данных, в который будет установлена сессия.
        session: Объект сессии базы данных.

    Raises:
        NotImplementedError: Если метод не реализован в подклассе.

    Как работает функция:
    - Выбрасывает исключение `NotImplementedError`, указывая, что метод должен быть реализован в подклассах.
    """
    ...
```

#### `after_handler`

```python
async def after_handler(self, session) -> None:
    """
    Метод для выполнения действий после вызова хендлера (например, коммит).

    Args:
        session: Объект сессии базы данных.

    Как работает функция:
    - Ничего не делает, предназначен для переопределения в подклассах.
    """
    ...
```

### `DatabaseMiddlewareWithoutCommit`

#### `set_session`

```python
def set_session(self, data: Dict[str, Any], session) -> None:
    """
    Устанавливает сессию базы данных в словаре `data` под ключом `'session_without_commit'`.

    Args:
        data (Dict[str, Any]): Словарь данных, в который будет установлена сессия.
        session: Объект сессии базы данных.

    Как работает функция:
    - Сохраняет сессию базы данных в словаре `data` под ключом `'session_without_commit'`.
    """
    ...
```

### `DatabaseMiddlewareWithCommit`

#### `set_session`

```python
def set_session(self, data: Dict[str, Any], session) -> None:
    """
    Устанавливает сессию базы данных в словаре `data` под ключом `'session_with_commit'`.

    Args:
        data (Dict[str, Any]): Словарь данных, в который будет установлена сессия.
        session: Объект сессии базы данных.

    Как работает функция:
    - Сохраняет сессию базы данных в словаре `data` под ключом `'session_with_commit'`.
    """
    ...
```

#### `after_handler`

```python
async def after_handler(self, session) -> None:
    """
    Применяет изменения к базе данных после вызова обработчика, вызывая метод `session.commit()`.

    Args:
        session: Объект сессии базы данных.

    Как работает функция:
    - Вызывает метод `session.commit()` для применения изменений к базе данных.
    """
    ...
```

## Параметры класса

### `BaseDatabaseMiddleware`

- `handler` (Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]]): Функция-обработчик, которая будет вызвана для обработки события.
- `event` (Message | CallbackQuery): Объект события (сообщение или callback-запрос).
- `data` (Dict[str, Any]): Словарь данных, передаваемый обработчику.
- `session`: Объект сессии базы данных.

### `DatabaseMiddlewareWithoutCommit`

- `data` (Dict[str, Any]): Словарь данных, в который будет установлена сессия.
- `session`: Объект сессии базы данных.

### `DatabaseMiddlewareWithCommit`

- `data` (Dict[str, Any]): Словарь данных, в который будет установлена сессия.
- `session`: Объект сессии базы данных.

## Примеры

**Пример использования `DatabaseMiddlewareWithoutCommit`:**

```python
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from bot.dao.database import async_session_maker
from bot.dao.database_middleware import DatabaseMiddlewareWithoutCommit

# Инициализация бота и диспетчера
bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher()

# Регистрация middleware
dp.message.middleware(DatabaseMiddlewareWithoutCommit())

# Пример обработчика
@dp.message(CommandStart())
async def start_handler(message: types.Message, session_without_commit):
    # Используйте сессию для выполнения операций с базой данных
    # session_without_commit.add(...)
    await message.answer("Hello, without commit!")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

**Пример использования `DatabaseMiddlewareWithCommit`:**

```python
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from bot.dao.database import async_session_maker
from bot.dao.database_middleware import DatabaseMiddlewareWithCommit

# Инициализация бота и диспетчера
bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher()

# Регистрация middleware
dp.message.middleware(DatabaseMiddlewareWithCommit())

# Пример обработчика
@dp.message(CommandStart())
async def start_handler(message: types.Message, session_with_commit):
    # Используйте сессию для выполнения операций с базой данных
    # session_with_commit.add(...)
    await message.answer("Hello, with commit!")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```