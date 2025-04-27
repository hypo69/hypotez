# Модуль `database_middleware.py`

## Обзор

Данный модуль содержит базовый класс `BaseDatabaseMiddleware`, который предоставляет функциональность для управления сессиями базы данных в Telegram-боте. Модуль также включает два класса-наследника: `DatabaseMiddlewareWithoutCommit` и `DatabaseMiddlewareWithCommit`, которые предоставляют разные варианты работы с сессиями базы данных:

- `DatabaseMiddlewareWithoutCommit`: класс, который добавляет сессию базы данных в словарь данных без автоматического коммита изменений.
- `DatabaseMiddlewareWithCommit`: класс, который добавляет сессию базы данных в словарь данных с автоматическим коммитом изменений после завершения обработки хендлера.

## Детали

Модуль `database_middleware.py` представляет собой ядро для управления сессиями базы данных в Telegram-боте. Он реализует базовый класс `BaseDatabaseMiddleware`, который служит основой для создания middleware, взаимодействующих с базой данных. Этот класс предоставляет два ключевых метода:

- `set_session`: устанавливает сессию базы данных в словарь данных.
- `after_handler`: выполняет действия после обработки хендлера (например, коммит изменений).

Классы-наследники `DatabaseMiddlewareWithoutCommit` и `DatabaseMiddlewareWithCommit` реализуют различные стратегии работы с сессиями:

- `DatabaseMiddlewareWithoutCommit`: Этот класс создает сессию базы данных, но не коммитит изменения автоматически. Это позволяет разработчику вручную управлять коммитом изменений.
- `DatabaseMiddlewareWithCommit`: Этот класс автоматически коммитит изменения после успешного завершения обработки хендлера.

Использование `database_middleware.py` позволяет организовать взаимодействие с базой данных в Telegram-боте, гарантируя правильное управление сессиями и коммитом изменений.

## Классы

### `BaseDatabaseMiddleware`

**Описание**: Базовый класс для middleware, работающих с сессиями базы данных.

**Наследует**:  `aiogram.BaseMiddleware`

**Атрибуты**:

**Методы**:

- `__call__`:  Обработчик, который вызывается при обработке событий. Метод устанавливает сессию базы данных, вызывает хендлер и выполняет действия после обработки хендлера.
- `set_session`: Абстрактный метод, который должен быть реализован в подклассах для установки сессии базы данных в словарь данных.
- `after_handler`: Метод для выполнения действий после вызова хендлера (например, коммит).

### `DatabaseMiddlewareWithoutCommit`

**Описание**: Класс, который добавляет сессию базы данных в словарь данных без автоматического коммита изменений.

**Наследует**: `BaseDatabaseMiddleware`

**Атрибуты**:

**Методы**:

- `set_session`: Устанавливает сессию базы данных в словарь данных под ключом `session_without_commit`.

### `DatabaseMiddlewareWithCommit`

**Описание**: Класс, который добавляет сессию базы данных в словарь данных с автоматическим коммитом изменений после завершения обработки хендлера.

**Наследует**: `BaseDatabaseMiddleware`

**Атрибуты**:

**Методы**:

- `set_session`: Устанавливает сессию базы данных в словарь данных под ключом `session_with_commit`.
- `after_handler`: Выполняет коммит изменений в сессии базы данных.

## Функции

## Параметры

## Примеры

**Пример использования `BaseDatabaseMiddleware`:**

```python
from bot.dao.database_middleware import BaseDatabaseMiddleware

class MyDatabaseMiddleware(BaseDatabaseMiddleware):
    def set_session(self, data: Dict[str, Any], session) -> None:
        data['session'] = session

    async def after_handler(self, session) -> None:
        await session.commit()

# Использование в Telegram-боте
dp.middleware.setup(MyDatabaseMiddleware())
```

**Пример использования `DatabaseMiddlewareWithoutCommit`:**

```python
from bot.dao.database_middleware import DatabaseMiddlewareWithoutCommit

# Использование в Telegram-боте
dp.middleware.setup(DatabaseMiddlewareWithoutCommit())
```

**Пример использования `DatabaseMiddlewareWithCommit`:**

```python
from bot.dao.database_middleware import DatabaseMiddlewareWithCommit

# Использование в Telegram-боте
dp.middleware.setup(DatabaseMiddlewareWithCommit())
```

## Как работает `database_middleware.py`

Модуль `database_middleware.py` предоставляет базовый класс `BaseDatabaseMiddleware`, который реализует функциональность для управления сессиями базы данных в Telegram-боте. Этот класс устанавливает сессию базы данных в словарь данных и предоставляет возможность выполнять действия после обработки хендлера.

Классы-наследники `DatabaseMiddlewareWithoutCommit` и `DatabaseMiddlewareWithCommit` реализуют разные варианты работы с сессиями базы данных. `DatabaseMiddlewareWithoutCommit` добавляет сессию базы данных в словарь данных без автоматического коммита изменений, в то время как `DatabaseMiddlewareWithCommit` автоматически коммитит изменения после завершения обработки хендлера.

## Примеры использования `database_middleware.py`

В примерах показано, как использовать модуль `database_middleware.py` в Telegram-боте.

**Пример 1:**

В этом примере создается класс `MyDatabaseMiddleware`, который наследует от `BaseDatabaseMiddleware`. В классе `MyDatabaseMiddleware` реализованы методы `set_session` и `after_handler`, которые устанавливают сессию базы данных и выполняют коммит изменений соответственно.

**Пример 2:**

Этот пример демонстрирует использование `DatabaseMiddlewareWithoutCommit` и `DatabaseMiddlewareWithCommit` для управления сессиями базы данных в Telegram-боте.