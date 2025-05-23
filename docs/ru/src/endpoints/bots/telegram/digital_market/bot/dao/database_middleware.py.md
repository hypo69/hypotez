# Модуль middleware для работы с базой данных в Telegram боте

## Обзор

Модуль содержит middleware классы для управления сессиями базы данных при обработке входящих сообщений и callback-запросов от Telegram бота. Он обеспечивает создание, передачу и закрытие сессий, а также обработку транзакций (commit/rollback).

## Подробнее

Этот модуль предоставляет базовый класс `BaseDatabaseMiddleware`, который служит основой для создания middleware, управляющих сессиями базы данных. Он использует `async_session_maker` для создания асинхронных сессий и обеспечивает автоматическое открытие, закрытие и обработку транзакций.
Также определены два производных класса: `DatabaseMiddlewareWithoutCommit` и `DatabaseMiddlewareWithCommit`, которые реализуют специфическое поведение для сессий без и с автоматическим коммитом изменений соответственно.

## Классы

### `BaseDatabaseMiddleware`

**Описание**: Базовый класс middleware для управления сессиями базы данных.

**Методы**:

- `__call__(handler, event, data)`: Асинхронный метод, вызываемый для обработки каждого события (сообщения или callback-запроса).
- `set_session(data, session)`: Метод для установки сессии в словарь данных.
- `after_handler(session)`: Метод для выполнения действий после вызова хендлера (например, коммит).

#### `__call__`

```python
async def __call__(
    self,
    handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
    event: Message | CallbackQuery,
    data: Dict[str, Any]
) -> Any:
    """
    Выполняет middleware обработку для каждого события.

    Args:
        handler (Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]]): Обработчик события.
        event (Message | CallbackQuery): Объект события (сообщение или callback-запрос).
        data (Dict[str, Any]): Словарь данных, передаваемый между middleware и обработчиком.

    Returns:
        Any: Результат выполнения обработчика.

    Raises:
        Exception: Если во время обработки возникает исключение, выполняет откат транзакции.

    
        1. Создает асинхронную сессию базы данных.
        2. Устанавливает сессию в словарь данных `data` с помощью метода `self.set_session`.
        3. Вызывает обработчик `handler` с событием и данными.
        4. После успешного выполнения обработчика вызывает метод `self.after_handler` для выполнения дополнительных действий (например, коммит).
        5. В случае возникновения исключения выполняет откат транзакции.
        6. Закрывает сессию базы данных в блоке `finally`.
    """
    ...
```

#### `set_session`

```python
def set_session(self, data: Dict[str, Any], session) -> None:
    """
    Устанавливает сессию в словарь данных.

    Args:
        data (Dict[str, Any]): Словарь данных, в который нужно установить сессию.
        session: Объект сессии базы данных.

    Raises:
        NotImplementedError: Если метод не переопределен в подклассе.

    
        Вызывает исключение `NotImplementedError`, так как метод должен быть реализован в подклассах для установки сессии в словарь данных.
    """
    ...
```

#### `after_handler`

```python
async def after_handler(self, session) -> None:
    """
    Выполняет действия после вызова хендлера.

    Args:
        session: Объект сессии базы данных.

    
        По умолчанию ничего не делает (`pass`). Может быть переопределен в подклассах для выполнения действий после обработки события (например, коммит транзакции).
    """
    ...
```

### `DatabaseMiddlewareWithoutCommit`

**Описание**: Middleware для работы с базой данных без автоматического коммита.

**Наследует**: `BaseDatabaseMiddleware`

**Методы**:

- `set_session(data, session)`: Устанавливает сессию в словаре данных без автоматического коммита.

#### `set_session`

```python
def set_session(self, data: Dict[str, Any], session) -> None:
    """
    Устанавливает сессию в словарь данных под ключом 'session_without_commit'.

    Args:
        data (Dict[str, Any]): Словарь данных, в который нужно установить сессию.
        session: Объект сессии базы данных.

    
        Устанавливает сессию в словаре `data` по ключу `'session_without_commit'`.
    """
    ...
```

### `DatabaseMiddlewareWithCommit`

**Описание**: Middleware для работы с базой данных с автоматическим коммитом.

**Наследует**: `BaseDatabaseMiddleware`

**Методы**:

- `set_session(data, session)`: Устанавливает сессию в словаре данных для автоматического коммита.
- `after_handler(session)`: Выполняет коммит сессии после обработки события.

#### `set_session`

```python
def set_session(self, data: Dict[str, Any], session) -> None:
    """
    Устанавливает сессию в словарь данных под ключом 'session_with_commit'.

    Args:
        data (Dict[str, Any]): Словарь данных, в который нужно установить сессию.
        session: Объект сессии базы данных.

    
        Устанавливает сессию в словаре `data` по ключу `'session_with_commit'`.
    """
    ...
```

#### `after_handler`

```python
async def after_handler(self, session) -> None:
    """
    Выполняет коммит сессии после обработки хендлера.

    Args:
        session: Объект сессии базы данных.

    
        Выполняет коммит транзакции для данной сессии.
    """
    ...
```