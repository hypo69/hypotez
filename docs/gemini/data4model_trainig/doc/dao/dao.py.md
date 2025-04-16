# Модуль DAO для работы с базой данных

## Обзор

Модуль `src.endpoints.bots.telegram.digital_market.bot.dao.dao` предоставляет классы DAO (Data Access Object) для работы с базой данных, используя SQLAlchemy.

## Подробней

Модуль содержит классы DAO для работы с моделями `User`, `Purchase`, `Category` и `Product`, предоставляя методы для выполнения операций CRUD (Create, Read, Update, Delete) и других запросов к базе данных.

## Классы

### `UserDAO`

**Описание**: DAO для работы с моделью `User`.

**Наследует**:

*   `BaseDAO[User]`: Базовый класс DAO.

**Атрибуты**:

*   `model` (Type[User]): Модель SQLAlchemy для таблицы `User`.

**Методы**:

*   `get_purchase_statistics(cls, session: AsyncSession, telegram_id: int) -> Optional[Dict[str, int]]`: Получает статистику о покупках пользователя.
*   `get_purchased_products(cls, session: AsyncSession, telegram_id: int) -> Optional[List[Purchase]]`: Получает список покупок пользователя.
*   `get_statistics(cls, session: AsyncSession)`: Получает общую статистику по пользователям.

### `PurchaseDao`

**Описание**: DAO для работы с моделью `Purchase`.

**Наследует**:

*   `BaseDAO[Purchase]`: Базовый класс DAO.

**Атрибуты**:

*   `model` (Type[Purchase]): Модель SQLAlchemy для таблицы `Purchase`.

**Методы**:

*   `get_payment_stats(cls, session: AsyncSession) -> str`: Получает статистику по типам платежей.
*   `get_full_summ(cls, session: AsyncSession) -> int`: Получает общую сумму всех покупок.
*   `get_next_id(cls, session: AsyncSession) -> int`: Возвращает следующий свободный ID для новой записи.

### `CategoryDao`

**Описание**: DAO для работы с моделью `Category`.

**Наследует**:

*   `BaseDAO[Category]`: Базовый класс DAO.

**Атрибуты**:

*   `model` (Type[Category]): Модель SQLAlchemy для таблицы `Category`.

### `ProductDao`

**Описание**: DAO для работы с моделью `Product`.

**Наследует**:

*   `BaseDAO[Product]`: Базовый класс DAO.

**Атрибуты**:

*   `model` (Type[Product]): Модель SQLAlchemy для таблицы `Product`.

## Методы класса `UserDAO`

### `get_purchase_statistics`

```python
@classmethod
async def get_purchase_statistics(cls, session: AsyncSession, telegram_id: int) -> Optional[Dict[str, int]]:
```

**Назначение**: Получает статистику о покупках пользователя.

**Параметры**:

*   `session` (AsyncSession): Асинхронная сессия базы данных.
*   `telegram_id` (int): Telegram ID пользователя.

**Возвращает**:

*   `Optional[Dict[str, int]]`: Словарь со статистикой покупок (общее число покупок и общая сумма) или `None`, если произошла ошибка.

**Как работает функция**:

1.  Выполняет запрос к базе данных, чтобы получить общее число покупок и общую сумму для заданного пользователя.
2.  Возвращает словарь со статистикой или `None` в случае ошибки.

### `get_purchased_products`

```python
@classmethod
async def get_purchased_products(cls, session: AsyncSession, telegram_id: int) -> Optional[List[Purchase]]:
```

**Назначение**: Получает список покупок пользователя.

**Параметры**:

*   `session` (AsyncSession): Асинхронная сессия базы данных.
*   `telegram_id` (int): Telegram ID пользователя.

**Возвращает**:

*   `Optional[List[Purchase]]`: Список покупок пользователя или `None`, если пользователь не найден или произошла ошибка.

**Как работает функция**:

1.  Выполняет запрос к базе данных, чтобы получить пользователя с его покупками.
2.  Возвращает список покупок пользователя или `None`, если пользователь не найден или произошла ошибка.

### `get_statistics`

```python
@classmethod
async def get_statistics(cls, session: AsyncSession):
```

**Назначение**: Получает общую статистику по пользователям.

**Параметры**:

*   `session` (AsyncSession): Асинхронная сессия базы данных.

**Возвращает**:

*   `dict`: Словарь со статистикой (общее количество пользователей, количество новых пользователей за сегодня, неделю и месяц).

**Как работает функция**:

1.  Выполняет запрос к базе данных, чтобы получить общее количество пользователей и количество новых пользователей за сегодня, неделю и месяц.
2.  Возвращает словарь со статистикой.

## Методы класса `PurchaseDao`

### `get_payment_stats`

```python
@classmethod
async def get_payment_stats(cls, session: AsyncSession) -> str:
```

**Назначение**: Получает статистику по типам платежей.

**Параметры**:

*   `session` (AsyncSession): Асинхронная сессия базы данных.

**Возвращает**:

*   `str`: Отформатированная строка со статистикой по типам платежей.

**Как работает функция**:

1.  Выполняет запрос к базе данных для получения статистики по типам платежей и общей сумме для каждого типа.
2.  Формирует строку с отформатированной статистикой.

### `get_full_summ`

```python
@classmethod
async def get_full_summ(cls, session: AsyncSession) -> int:
```

**Назначение**: Получает общую сумму всех покупок.

**Параметры**:

*   `session` (AsyncSession): Асинхронная сессия базы данных.

**Возвращает**:

*   `int`: Общая сумма всех покупок.

**Как работает функция**:

1.  Выполняет запрос к базе данных для получения общей суммы всех покупок.
2.  Возвращает общую сумму.

### `get_next_id`

```python
@classmethod
async def get_next_id(cls, session: AsyncSession) -> int:
```

**Назначение**: Возвращает следующий свободный ID для новой записи.

**Параметры**:

*   `session` (AsyncSession): Асинхронная сессия базы данных.

**Возвращает**:

*   `int`: Следующий свободный ID.

**Как работает функция**:

1.  Выполняет запрос к базе данных для получения максимального ID.
2.  Возвращает максимальный ID + 1 или 1, если таблица пуста.