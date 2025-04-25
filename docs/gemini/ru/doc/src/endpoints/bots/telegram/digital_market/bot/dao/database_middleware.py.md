# Модуль для работы с базой данных в Телеграм боте
=====================================================

Этот модуль предоставляет базовые классы для работы с базой данных в Телеграм боте, используя `aiogram` и `sqlalchemy.ext.asyncio`. 

## Обзор

Модуль предоставляет два основных класса:

- `BaseDatabaseMiddleware`: Базовый класс для работы с базой данных в Телеграм боте.
- `DatabaseMiddlewareWithCommit`:  Класс для работы с базой данных, где изменения в сессии автоматически коммитятся после выполнения обработчика.
- `DatabaseMiddlewareWithoutCommit`: Класс для работы с базой данных, где изменения в сессии не коммитятся автоматически.

## Классы

### `BaseDatabaseMiddleware`

**Описание**: Базовый класс для работы с базой данных в Телеграм боте.

**Наследует**: `aiogram.BaseMiddleware`

**Атрибуты**:  Нет

**Методы**:

- `__call__`:  Метод для вызова обработчика (handler) с использованием сессии базы данных.
- `set_session`:  Метод для установки сессии в словарь данных. 
- `after_handler`: Метод для выполнения действий после вызова обработчика (например, коммит).


**Как работает**:

- Метод `__call__` создает сессию с помощью `async_session_maker` и устанавливает ее в словарь данных (`data`) с помощью метода `set_session`. 
- После выполнения обработчика (`handler`) вызывается метод `after_handler`, где можно выполнить дополнительные действия, например, коммит сессии. 
- В случае возникновения исключения, сессия откатывается (`session.rollback()`). 
- В блоке `finally` сессия закрывается (`session.close()`). 

**Примеры**:

```python
# Пример использования BaseDatabaseMiddleware
from bot.dao.database import async_session_maker

class MyMiddleware(BaseDatabaseMiddleware):
    def set_session(self, data: Dict[str, Any], session) -> None:
        data['session'] = session

    async def after_handler(self, session) -> None:
        await session.commit() 

async def handler(event: Message | CallbackQuery, data: Dict[str, Any]):
    session = data['session'] # Получаем сессию из словаря данных
    # Выполняем операции с сессией
    await session.commit() 
    return ...

middleware = MyMiddleware()

# Пример использования MyMiddleware
# В примере используется MyMiddleware, который наследует BaseDatabaseMiddleware
middleware(handler, event, data) 

```


### `DatabaseMiddlewareWithoutCommit`

**Описание**: Класс для работы с базой данных, где изменения в сессии не коммитятся автоматически.

**Наследует**: `BaseDatabaseMiddleware`

**Атрибуты**:  Нет

**Методы**:

- `set_session`: Метод для установки сессии в словарь данных (`data`). 

**Как работает**:

-  Класс `DatabaseMiddlewareWithoutCommit`  наследует базовый класс `BaseDatabaseMiddleware`. 
-  Метод `set_session`  устанавливает сессию в словарь данных (`data`) с ключом `'session_without_commit'`. 
-  Изменения в сессии не коммитятся автоматически, что позволяет разработчику вручную управлять коммитом сессии в обработчике.

**Примеры**:

```python
# Пример использования DatabaseMiddlewareWithoutCommit
from bot.dao.database import async_session_maker

async def handler(event: Message | CallbackQuery, data: Dict[str, Any]):
    session = data['session_without_commit'] # Получаем сессию из словаря данных
    # Выполняем операции с сессией
    await session.commit() # Коммит сессии вручную
    return ...

middleware = DatabaseMiddlewareWithoutCommit()

# Пример использования MyMiddleware
# В примере используется DatabaseMiddlewareWithoutCommit, который наследует BaseDatabaseMiddleware
middleware(handler, event, data) 

```

### `DatabaseMiddlewareWithCommit`

**Описание**:  Класс для работы с базой данных, где изменения в сессии автоматически коммитятся после выполнения обработчика.

**Наследует**: `BaseDatabaseMiddleware`

**Атрибуты**:  Нет

**Методы**:

- `set_session`: Метод для установки сессии в словарь данных (`data`).
- `after_handler`: Метод для выполнения действий после вызова обработчика (`handler`).

**Как работает**:

-  Класс `DatabaseMiddlewareWithCommit`  наследует базовый класс `BaseDatabaseMiddleware`. 
-  Метод `set_session`  устанавливает сессию в словарь данных (`data`) с ключом `'session_with_commit'`.
-  Метод `after_handler`  автоматически коммитит изменения в сессии после выполнения обработчика.

**Примеры**:

```python
# Пример использования DatabaseMiddlewareWithCommit
from bot.dao.database import async_session_maker

async def handler(event: Message | CallbackQuery, data: Dict[str, Any]):
    session = data['session_with_commit'] # Получаем сессию из словаря данных
    # Выполняем операции с сессией
    return ...

middleware = DatabaseMiddlewareWithCommit()

# Пример использования MyMiddleware
# В примере используется DatabaseMiddlewareWithCommit, который наследует BaseDatabaseMiddleware
middleware(handler, event, data) 

```

## Параметры класса

- Нет

## Примеры

```python
# Пример использования middleware
from bot.dao.database import async_session_maker
from bot.dao.database_middleware import DatabaseMiddlewareWithCommit
from aiogram import Dispatcher

# Создание middleware
db_middleware = DatabaseMiddlewareWithCommit()

# Регистрация middleware в Dispatcher
dp = Dispatcher(...)
dp.middleware.setup(db_middleware)

# Пример обработчика
async def handler(message: Message, data: Dict[str, Any]):
    session = data['session_with_commit']
    # Используем сессию для взаимодействия с базой данных
    # ...
    return ...

# Регистрация обработчика
dp.register_message_handler(handler)

# Запуск бота
if __name__ == "__main__":
    from bot import bot 
    bot.run_polling()
```

## Внутренние функции

- Нет

## Как работает

Модуль `database_middleware.py` обеспечивает взаимодействие с базой данных в Телеграм боте, используя `aiogram` и `sqlalchemy.ext.asyncio`.

- Он реализует базовую мидлвар `BaseDatabaseMiddleware`, которая создает сессию базы данных перед обработкой каждого события.
- Дочерние классы `DatabaseMiddlewareWithoutCommit` и `DatabaseMiddlewareWithCommit`  наследуют  `BaseDatabaseMiddleware` и реализуют разные стратегии для коммита сессии: без коммита и с автоматическим коммитом.

## Дополнительные сведения

- Все три класса предоставляют возможность разработчику управлять сессией базы данных в обработчике.
-  `DatabaseMiddlewareWithCommit`  обеспечивает удобство в тех случаях, когда необходимо автоматически коммитить изменения после каждого обработчика.
-  `DatabaseMiddlewareWithoutCommit`  позволяет разработчику управлять коммитом сессии вручную, что может быть необходимо в некоторых случаях.