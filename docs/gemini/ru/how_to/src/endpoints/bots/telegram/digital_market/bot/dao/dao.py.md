### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода содержит Data Access Objects (DAO) для работы с базой данных, используя SQLAlchemy. Он включает классы для выполнения операций CRUD (создание, чтение, обновление, удаление) с таблицами `User`, `Purchase`, `Category` и `Product`. Также содержит методы для получения статистики, связанной с пользователями и покупками.

Шаги выполнения
-------------------------
1. **Инициализация DAO**:
   - Создаются классы DAO (`UserDAO`, `PurchaseDao`, `CategoryDao`, `ProductDao`), каждый из которых связан с соответствующей моделью SQLAlchemy.

2. **Получение статистики пользователя (`UserDAO.get_purchase_statistics`)**:
   - Метод выполняет запрос к базе данных для получения общего числа покупок и общей суммы, потраченной пользователем.
   - Использует `func.count` и `func.sum` для агрегации данных.
   - Обрабатывает возможные ошибки при работе с базой данных, логируя их.

3. **Получение списка покупок пользователя (`UserDAO.get_purchased_products`)**:
   - Метод извлекает пользователя по `telegram_id` и все его покупки с информацией о продуктах.
   - Использует `selectinload` для оптимизации запроса и избежания "N+1" проблемы.

4. **Получение общей статистики (`UserDAO.get_statistics`)**:
   - Метод получает общую статистику по пользователям, включая общее количество, новых пользователей за сегодня, за неделю и за месяц.
   - Использует `func.count` и `func.sum` с условными выражениями (`case`) для подсчета новых пользователей.
   - Логирует полученную статистику.

5. **Получение статистики платежей (`PurchaseDao.get_payment_stats`)**:
   - Метод извлекает статистику по типам платежей и общей сумме для каждого типа.
   - Использует `func.sum` и `group_by` для агрегации данных по типам платежей.
   - Форматирует результат в виде строки.

6. **Получение общей суммы покупок (`PurchaseDao.get_full_summ`)**:
   - Метод извлекает общую сумму всех покупок.
   - Использует `func.sum` для агрегации данных.

7. **Получение следующего свободного ID (`PurchaseDao.get_next_id`)**:
   - Метод определяет следующий доступный ID для новой записи в таблице `Purchase`.
   - Использует `func.coalesce` и `func.max` для определения максимального существующего ID и возвращает следующий.

Пример использования
-------------------------

```python
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
import asyncio

#  Строка подключения к базе данных
DATABASE_URL = "postgresql+asyncpg://user:password@host:port/database"

#  Создание асинхронного движка
engine = create_async_engine(DATABASE_URL, echo=True)

#  Создание фабрики сессий
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def main():
    async with async_session() as session:
        #  Пример использования UserDAO.get_purchase_statistics
        user_stats = await UserDAO.get_purchase_statistics(session, telegram_id=12345)
        print(f"Статистика покупок пользователя: {user_stats}")

        #  Пример использования UserDAO.get_purchased_products
        user_purchases = await UserDAO.get_purchased_products(session, telegram_id=12345)
        if user_purchases:
            print(f"Покупки пользователя: {[purchase.id for purchase in user_purchases]}")

        #  Пример использования UserDAO.get_statistics
        total_stats = await UserDAO.get_statistics(session)
        print(f"Общая статистика: {total_stats}")

        #  Пример использования PurchaseDao.get_payment_stats
        payment_stats = await PurchaseDao.get_payment_stats(session)
        print(f"Статистика платежей:\n{payment_stats}")

        #  Пример использования PurchaseDao.get_full_summ
        full_summ = await PurchaseDao.get_full_summ(session)
        print(f"Общая сумма покупок: {full_summ}")

        #  Пример использования PurchaseDao.get_next_id
        next_id = await PurchaseDao.get_next_id(session)
        print(f"Следующий ID для покупки: {next_id}")

if __name__ == "__main__":
    asyncio.run(main())