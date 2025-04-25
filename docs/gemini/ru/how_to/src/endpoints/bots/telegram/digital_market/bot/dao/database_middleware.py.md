## Как использовать этот блок кода
=========================================================================================

### Описание
-------------------------
Блок кода представляет собой базовый класс `BaseDatabaseMiddleware` для работы с базой данных в телеграм-боте, а также два подкласса: `DatabaseMiddlewareWithoutCommit` и `DatabaseMiddlewareWithCommit`.

`BaseDatabaseMiddleware`  -  базовый класс, который обеспечивает работу с базой данных в телеграм-боте. Он использует `async_session_maker` для создания асинхронной сессии, добавляет сессию в контекст данных `data` и обрабатывает исключения.

`DatabaseMiddlewareWithoutCommit` - подкласс базового класса, который не совершает коммиты в базу данных после успешного выполнения хендлера. 

`DatabaseMiddlewareWithCommit` - подкласс базового класса, который совершает коммиты в базу данных после успешного выполнения хендлера.

### Шаги выполнения
-------------------------
1. **Создание сессии:** При вызове обработчика `__call__`  в `BaseDatabaseMiddleware` создается асинхронная сессия с помощью `async_session_maker`.
2. **Установка сессии в контекст данных:** Сессия устанавливается в контекст данных `data`  с помощью метода `set_session`, который должен быть реализован в подклассах.
3. **Вызов обработчика:** Вызывается обработчик `handler` с переданным контекстом данных `data`.
4. **Обработка исключений:**  При возникновении исключения выполняется откат транзакции `session.rollback()`.
5. **Закрытие сессии:**  После завершения обработки, сессия закрывается.

### Пример использования
-------------------------
```python
from bot.dao.database_middleware import DatabaseMiddlewareWithCommit

# ...

# Создаем объект DatabaseMiddlewareWithCommit
db_middleware = DatabaseMiddlewareWithCommit()

# Регистрируем middleware в dispatcher
dp.middleware.setup(db_middleware)

# ...

# В хендлере доступна сессия
@dp.message_handler(commands=['start'])
async def start_handler(message: Message, data: Dict[str, Any]):
    session = data['session_with_commit']
    # ...
```

В примере мы создаем объект `DatabaseMiddlewareWithCommit` и регистрируем его в диспетчере. В обработчике `start_handler`  доступна сессия через контекст данных `data` по ключу `'session_with_commit'`.