# Модуль database_middleware.py

## Обзор

Этот модуль предоставляет middleware для интеграции базы данных с ботом Telegram. Он содержит базовый класс `BaseDatabaseMiddleware` и его подклассы `DatabaseMiddlewareWithoutCommit` и `DatabaseMiddlewareWithCommit`, которые управляют сессиями базы данных и транзакциями.

## Подробности

Этот код обеспечивает интеграцию базы данных в обработчики aiogram, гарантируя, что каждая операция выполняется в контексте сессии базы данных. Он также включает обработку транзакций, позволяя откатывать изменения в случае ошибок.

## Классы

### `BaseDatabaseMiddleware`

**Описание**: Базовый класс middleware для управления сессиями базы данных.

**Наследует**: `aiogram.BaseMiddleware`

**Атрибуты**:
- Нет специфических атрибутов, кроме тех, что предоставляются базовым классом `aiogram.BaseMiddleware`.

**Методы**:

- `__call__(self, handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]], event: Message | CallbackQuery, data: Dict[str, Any]) -> Any`
- `set_session(self, data: Dict[str, Any], session) -> None`
- `after_handler(self, session) -> None`

### `BaseDatabaseMiddleware.__call__`

```python
async def __call__(
    self,
    handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
    event: Message | CallbackQuery,
    data: Dict[str, Any]
) -> Any:
    """
    Выполняет middleware, управляя сессией базы данных.

    Args:
        handler (Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]]): Обработчик события.
        event (Message | CallbackQuery): Событие (сообщение или callback-запрос).
        data (Dict[str, Any]): Словарь данных, передаваемый между middleware и обработчиком.

    Returns:
        Any: Результат выполнения обработчика.

    Raises:
        Exception: Если в процессе выполнения обработчика возникает исключение, транзакция откатывается.

    Как работает:
    - Создает асинхронную сессию базы данных.
    - Устанавливает сессию в словаре данных.
    - Вызывает обработчик события.
    - Выполняет действия после вызова обработчика (например, коммит).
    - В случае исключения откатывает транзакцию.
    - Закрывает сессию.

    Пример:
        # Пример использования middleware
        async def my_handler(event: Message, data: Dict[str, Any]):
            session = data['session']
            # ... логика обработчика ...
            return ...
    """
```

### `BaseDatabaseMiddleware.set_session`

```python
def set_session(self, data: Dict[str, Any], session) -> None:
    """
    Устанавливает сессию в словарь данных.

    Args:
        data (Dict[str, Any]): Словарь данных, в который нужно установить сессию.
        session: Сессия базы данных.

    Raises:
        NotImplementedError: Если метод не реализован в подклассе.

    Как работает:
    - Этот метод должен быть переопределен в подклассах для установки сессии в словаре данных.
    """
```

### `BaseDatabaseMiddleware.after_handler`

```python
async def after_handler(self, session) -> None:
    """
    Выполняет действия после вызова обработчика (например, коммит).

    Args:
        session: Сессия базы данных.

    Как работает:
    - Этот метод может быть переопределен в подклассах для выполнения действий после вызова обработчика.
    """
```

### `DatabaseMiddlewareWithoutCommit`

**Описание**: Middleware для работы с базой данных без автоматического коммита транзакций.

**Наследует**: `BaseDatabaseMiddleware`

**Методы**:
- `set_session(self, data: Dict[str, Any], session) -> None`

### `DatabaseMiddlewareWithoutCommit.set_session`

```python
def set_session(self, data: Dict[str, Any], session) -> None:
    """
    Устанавливает сессию в словарь данных под ключом 'session_without_commit'.

    Args:
        data (Dict[str, Any]): Словарь данных, в который нужно установить сессию.
        session: Сессия базы данных.

    Как работает:
    - Устанавливает сессию базы данных в словаре данных под ключом 'session_without_commit'.
    """
```

### `DatabaseMiddlewareWithCommit`

**Описание**: Middleware для работы с базой данных с автоматическим коммитом транзакций после обработки.

**Наследует**: `BaseDatabaseMiddleware`

**Методы**:
- `set_session(self, data: Dict[str, Any], session) -> None`
- `after_handler(self, session) -> None`

### `DatabaseMiddlewareWithCommit.set_session`

```python
def set_session(self, data: Dict[str, Any], session) -> None:
    """
    Устанавливает сессию в словарь данных под ключом 'session_with_commit'.

    Args:
        data (Dict[str, Any]): Словарь данных, в который нужно установить сессию.
        session: Сессия базы данных.

    Как работает:
    - Устанавливает сессию базы данных в словаре данных под ключом 'session_with_commit'.
    """
```

### `DatabaseMiddlewareWithCommit.after_handler`

```python
async def after_handler(self, session) -> None:
    """
    Выполняет коммит транзакции после вызова обработчика.

    Args:
        session: Сессия базы данных.

    Как работает:
    - Выполняет коммит транзакции, сохраняя изменения в базе данных.
    """
```