## Как использовать класс UserDAO
=========================================================================================

Описание
-------------------------
Класс `UserDAO` предоставляет методы для работы с данными о пользователях в базе данных. В нем реализованы операции для получения информации о пользователях, их покупках, а также общей статистики.

Шаги выполнения
-------------------------
1. **Инициализация сессии**: Создайте асинхронную сессию базы данных `session` с помощью `AsyncSession`.
2. **Использование методов**: Вызывайте необходимые методы класса для получения данных:
   - `get_purchase_statistics(session: AsyncSession, telegram_id: int)`: Возвращает словарь со статистикой покупок пользователя (общее количество покупок и общая сумма).
   - `get_purchased_products(session: AsyncSession, telegram_id: int)`: Возвращает список покупок пользователя с информацией о приобретенных товарах.
   - `get_statistics(session: AsyncSession)`: Возвращает словарь с общей статистикой пользователей (количество всех пользователей, новых пользователей за день, неделю и месяц).

Пример использования
-------------------------

```python
from bot.dao.models import User
from bot.dao.dao import UserDAO
from sqlalchemy.ext.asyncio import AsyncSession  # импорт из sqlalchemy


async def main():
    async with AsyncSession() as session:  # создание асинхронной сессии
        # Получение статистики покупок пользователя
        purchase_stats = await UserDAO.get_purchase_statistics(session, telegram_id=12345)

        # Получение списка покупок пользователя
        user_purchases = await UserDAO.get_purchased_products(session, telegram_id=12345)

        # Получение общей статистики пользователей
        user_stats = await UserDAO.get_statistics(session)

        print(f"Статистика покупок: {purchase_stats}")
        print(f"Список покупок: {user_purchases}")
        print(f"Общая статистика: {user_stats}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Как использовать класс PurchaseDao
=========================================================================================

Описание
-------------------------
Класс `PurchaseDao` предоставляет методы для работы с данными о покупках в базе данных. В нем реализованы операции для получения информации о покупках, общей суммы покупок и статистики по типам платежей.

Шаги выполнения
-------------------------
1. **Инициализация сессии**: Создайте асинхронную сессию базы данных `session` с помощью `AsyncSession`.
2. **Использование методов**: Вызывайте необходимые методы класса для получения данных:
   - `get_payment_stats(session: AsyncSession)`: Возвращает отформатированную строку с информацией о сумме платежей по различным типам (Юкасса, Робокасса, STARS).
   - `get_full_summ(session: AsyncSession)`: Возвращает общую сумму всех покупок.
   - `get_next_id(session: AsyncSession)`: Возвращает следующий свободный ID для новой записи.

Пример использования
-------------------------

```python
from bot.dao.models import Purchase
from bot.dao.dao import PurchaseDao
from sqlalchemy.ext.asyncio import AsyncSession  # импорт из sqlalchemy


async def main():
    async with AsyncSession() as session:  # создание асинхронной сессии
        # Получение статистики по типам платежей
        payment_stats = await PurchaseDao.get_payment_stats(session)

        # Получение общей суммы покупок
        full_summ = await PurchaseDao.get_full_summ(session)

        # Получение следующего свободного ID для новой записи
        next_id = await PurchaseDao.get_next_id(session)

        print(f"Статистика по типам платежей: {payment_stats}")
        print(f"Общая сумма покупок: {full_summ}")
        print(f"Следующий свободный ID: {next_id}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Как использовать классы CategoryDao и ProductDao
=========================================================================================

Описание
-------------------------
Классы `CategoryDao` и `ProductDao`  предоставляют методы для работы с данными о категориях и товарах в базе данных. Они реализуют базовые операции CRUD для соответствующих моделей.

Шаги выполнения
-------------------------
1. **Инициализация сессии**: Создайте асинхронную сессию базы данных `session` с помощью `AsyncSession`.
2. **Использование методов**: Вызывайте необходимые методы для работы с данными:
    - `get_all(session: AsyncSession)`: Возвращает список всех записей для соответствующей модели.
    - `get_by_id(session: AsyncSession, id: int)`: Возвращает запись по её ID.
    - `create(session: AsyncSession, **kwargs)`: Создает новую запись.
    - `update(session: AsyncSession, id: int, **kwargs)`: Обновляет запись по ID.
    - `delete(session: AsyncSession, id: int)`: Удаляет запись по ID.

Пример использования
-------------------------

```python
from bot.dao.models import Category, Product
from bot.dao.dao import CategoryDao, ProductDao
from sqlalchemy.ext.asyncio import AsyncSession  # импорт из sqlalchemy


async def main():
    async with AsyncSession() as session:  # создание асинхронной сессии
        # Получение списка всех категорий
        categories = await CategoryDao.get_all(session)

        # Получение категории по ID
        category = await CategoryDao.get_by_id(session, id=1)

        # Создание новой категории
        new_category = await CategoryDao.create(session, name="Новая категория")

        # Обновление категории
        updated_category = await CategoryDao.update(session, id=1, name="Обновленная категория")

        # Удаление категории
        await CategoryDao.delete(session, id=1)


        # ... аналогично для работы с товарами (ProductDao) ...

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```