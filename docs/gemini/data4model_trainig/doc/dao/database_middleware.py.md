# Модуль промежуточного слоя для работы с базой данных

## Обзор

Модуль `src.endpoints.bots.telegram.digital_market.bot.dao.database_middleware` предоставляет мидлвари (middleware) для работы с базой данных в Telegram-боте, используя SQLAlchemy.

## Подробней

Модуль содержит классы мидлвари, которые управляют созданием, использованием и закрытием сессий базы данных.

## Классы

### `BaseDatabaseMiddleware`

**Описание**: Базовый класс для мидлвари, работающих с базой данных.

**Атрибуты**:

*   Нет явно определенных атрибутов.

**Методы**:

*   `__call__(self, handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]], event: Message | CallbackQuery, data: Dict[str, Any]) -> Any`: Основной метод мидлвари, вызываемый для обработки события.
*   `set_session(self, data: Dict[str, Any], session) -> None`: Метод для установки сессии в словарь данных (должен быть реализован в подклассах).
*   `after_handler(self, session) -> None`: Метод для выполнения действий после вызова обработчика (например, коммит) (по умолчанию ничего не делает).

### `DatabaseMiddlewareWithoutCommit`

**Описание**: Мидлварь для работы с базой данных без коммита транзакции.

**Наследует**:

*   `BaseDatabaseMiddleware`: Базовый класс для мидлвари, работающих с базой данных.

**Методы**:

*   `set_session(self, data: Dict[str, Any], session) -> None`: Устанавливает сессию базы данных в словарь данных без коммита.

### `DatabaseMiddlewareWithCommit`

**Описание**: Мидлварь для работы с базой данных с коммитом транзакции.

**Наследует**:

*   `BaseDatabaseMiddleware`: Базовый класс для мидлвари, работающих с базой данных.

**Методы**:

*   `set_session(self, data: Dict[str, Any], session) -> None`: Устанавливает сессию базы данных в словарь данных.
*   `after_handler(self, session) -> None`: Выполняет коммит транзакции после вызова обработчика.

## Методы класса `BaseDatabaseMiddleware`

### `__call__`

```python
async def __call__(
    self,
    handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
    event: Message | CallbackQuery,
    data: Dict[str, Any]
) -> Any:
```

**Назначение**: Основной метод мидлвари, вызываемый для обработки события.

**Параметры**:

*   `handler` (Callable): Функция-обработчик, которая будет вызвана.
*   `event` (Message | CallbackQuery): Событие (сообщение или обратный вызов).
*   `data` (Dict[str, Any]): Словарь данных.

**Как работает функция**:

1.  Создает асинхронную сессию базы данных.
2.  Устанавливает сессию в словарь данных, вызывая метод `set_session`.
3.  Вызывает функцию-обработчик, передавая ей событие и данные.
4.  После выполнения обработчика выполняет дополнительные действия, используя метод `after_handler`.
5.  В случае ошибки выполняет откат транзакции с помощью `session.rollback()`.
6.  Закрывает сессию базы данных.

### `set_session`

```python
def set_session(self, data: Dict[str, Any], session) -> None:
```

**Назначение**: Метод для установки сессии в словарь данных (должен быть реализован в подклассах).

**Параметры**:

*   `data` (Dict[str, Any]): Словарь данных.
*   `session`: Сессия базы данных.

**Вызывает исключения**:

*   `NotImplementedError`: Если метод не реализован в подклассе.

### `after_handler`

```python
async def after_handler(self, session) -> None:
```

**Назначение**: Метод для выполнения действий после вызова обработчика (например, коммит).

**Параметры**:

*   `session`: Сессия базы данных.

**Как работает функция**:

В базовом классе метод ничего не делает.

## Методы классов `DatabaseMiddlewareWithoutCommit` и `DatabaseMiddlewareWithCommit`

### `set_session`

**Назначение**: Устанавливает сессию базы данных в словарь данных.

**Параметры**:

*   `data` (Dict[str, Any]): Словарь данных.
*   `session`: Сессия базы данных.

**Как работает функция**:

*   `DatabaseMiddlewareWithoutCommit`: Устанавливает сессию в `data['session_without_commit']`.
*   `DatabaseMiddlewareWithCommit`: Устанавливает сессию в `data['session_with_commit']`.

### `after_handler`

**Назначение**: Выполняет коммит транзакции после вызова обработчика.

**Параметры**:

*   `session`: Сессия базы данных.

**Как работает функция**:

*   `DatabaseMiddlewareWithCommit`: Выполняет коммит транзакции, используя `await session.commit()`.
*    `DatabaseMiddlewareWithoutCommit`: Не выполняет никаких действий.

## Использование

Данный модуль предоставляет механизмы для управления сессиями базы данных в Telegram-боте, обеспечивая автоматическое создание, использование и закрытие сессий для каждого обработчика.

**Пример использования:**

```python
from aiogram import Dispatcher

from bot.dao.database_middleware import DatabaseMiddlewareWithoutCommit, DatabaseMiddlewareWithCommit

dp = Dispatcher()

dp.update.middleware(DatabaseMiddlewareWithoutCommit())
dp.update.middleware(DatabaseMiddlewareWithCommit())