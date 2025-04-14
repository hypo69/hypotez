### **Анализ кода модуля `dao.py`**

## \file /hypotez/src/endpoints/bots/telegram/digital_market/bot/dao/dao.py

Модуль содержит Data Access Objects (DAO) для работы с базой данных, используя SQLAlchemy.
DAO используются для абстракции доступа к данным и выполнения операций с таблицами базы данных, такими как `User`, `Purchase`, `Category`, `Product`.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Использование асинхронных сессий SQLAlchemy для неблокирующих операций с базой данных.
    - Абстракция доступа к данным через DAO.
    - Использование `logger` для логирования информации и ошибок.
    - Явное указание типов для параметров и возвращаемых значений.
- **Минусы**:
    - Отсутствуют docstring для классов `CategoryDao` и `ProductDao`.
    - В некоторых блоках `except` используется `print` вместо `logger.error` для логирования ошибок.
    - Использование `e` вместо `ex` в блоках обработки исключений.
    - Отсутствуют комментарии и docstring к некоторым функциям.

**Рекомендации по улучшению:**

1.  **Добавить docstring для всех классов и методов**:
    - Добавить подробные описания для классов `CategoryDao` и `ProductDao`.
    - Улучшить существующие docstring, сделав их более информативными и соответствующими стандарту.

2.  **Заменить `print` на `logger.error` в блоках `except`**:
    - Использовать `logger.error` вместо `print` для логирования ошибок, чтобы обеспечить централизованное и структурированное логирование.

3.  **Использовать `ex` вместо `e` в блоках обработки исключений**:
    - Унифицировать именование переменных исключений, используя `ex` вместо `e`.

4.  **Добавить аннотации типов для переменных, где это необходимо**:
    - Добавить аннотации типов для локальных переменных, чтобы улучшить читаемость и поддерживаемость кода.

5.  **Добавить комментарии к сложной логике**:
    - Добавить комментарии для пояснения сложных запросов SQLAlchemy и логики обработки данных.

6.  **Улучшить обработку ошибок**:
    - Вместо простого возврата `None` при ошибках, можно рассмотреть возможность проброса исключений или возврата специальных объектов ошибок.

7.  **Удалить неиспользуемые импорты**:
    - Проверить и удалить неиспользуемые импорты.

8.  **Использовать одинарные кавычки**
    - Использовать одинарные кавычки (`'`) вместо двойных (`"`) для строковых литералов.

**Оптимизированный код:**

```python
from datetime import datetime, UTC, timedelta
from typing import Optional, List, Dict

from loguru import logger
from sqlalchemy import select, func, case
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from bot.dao.base import BaseDAO
from bot.dao.models import User, Purchase, Category, Product


class UserDAO(BaseDAO[User]):
    """
    DAO для работы с моделью User.
    Предоставляет методы для получения статистики покупок и информации о приобретенных продуктах.
    """
    model = User

    @classmethod
    async def get_purchase_statistics(cls, session: AsyncSession, telegram_id: int) -> Optional[Dict[str, int]]:
        """
        Получает статистику покупок пользователя по telegram_id.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.
            telegram_id (int): Telegram ID пользователя.

        Returns:
            Optional[Dict[str, int]]: Словарь со статистикой покупок пользователя,
            включающий общее количество покупок и общую сумму.
            Возвращает None в случае ошибки или отсутствия данных.
        """
        try:
            # Запрос для получения общего числа покупок и общей суммы
            result = await session.execute(
                select(
                    func.count(Purchase.id).label('total_purchases'),
                    func.sum(Purchase.price).label('total_amount')
                ).join(User).filter(User.telegram_id == telegram_id)
            )
            stats = result.one_or_none()

            if stats is None:
                return None

            total_purchases, total_amount = stats
            return {
                'total_purchases': total_purchases,
                'total_amount': total_amount or 0  # Обработка случая, когда сумма может быть None
            }

        except SQLAlchemyError as ex:
            # Обработка ошибок при работе с базой данных
            logger.error('Ошибка при получении статистики покупок пользователя', ex, exc_info=True)
            return None

    @classmethod
    async def get_purchased_products(cls, session: AsyncSession, telegram_id: int) -> Optional[List[Purchase]]:
        """
        Получает список покупок пользователя по telegram_id.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.
            telegram_id (int): Telegram ID пользователя.

        Returns:
            Optional[List[Purchase]]: Список покупок пользователя.
            Возвращает None в случае ошибки или отсутствия данных.
        """
        try:
            # Запрос для получения пользователя с его покупками и связанными продуктами
            result = await session.execute(
                select(User)
                .options(
                    selectinload(User.purchases).selectinload(Purchase.product)
                )
                .filter(User.telegram_id == telegram_id)
            )
            user = result.scalar_one_or_none()

            if user is None:
                return None

            return user.purchases

        except SQLAlchemyError as ex:
            # Обработка ошибок при работе с базой данных
            logger.error('Ошибка при получении информации о покупках пользователя', ex, exc_info=True)
            return None

    @classmethod
    async def get_statistics(cls, session: AsyncSession) -> Dict[str, int]:
        """
        Получает статистику по пользователям: общее количество, новых за сегодня, за неделю и за месяц.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.

        Returns:
            Dict[str, int]: Словарь со статистикой пользователей.

        Raises:
            SQLAlchemyError: Если возникает ошибка при выполнении запроса к базе данных.
        """
        try:
            now: datetime = datetime.now(UTC)

            query = select(
                func.count().label('total_users'),
                func.sum(case((cls.model.created_at >= now - timedelta(days=1), 1), else_=0)).label('new_today'),
                func.sum(case((cls.model.created_at >= now - timedelta(days=7), 1), else_=0)).label('new_week'),
                func.sum(case((cls.model.created_at >= now - timedelta(days=30), 1), else_=0)).label('new_month')
            )

            result = await session.execute(query)
            stats = result.fetchone()

            statistics: Dict[str, int] = {
                'total_users': stats.total_users,
                'new_today': stats.new_today,
                'new_week': stats.new_week,
                'new_month': stats.new_month
            }

            logger.info(f'Статистика успешно получена: {statistics}')
            return statistics
        except SQLAlchemyError as ex:
            logger.error('Ошибка при получении статистики', ex, exc_info=True)
            raise


class PurchaseDao(BaseDAO[Purchase]):
    """
    DAO для работы с моделью Purchase.
    Предоставляет методы для получения статистики платежей и общей суммы покупок.
    """
    model = Purchase

    @classmethod
    async def get_payment_stats(cls, session: AsyncSession) -> str:
        """
        Получает статистику платежей по типам (yukassa, robocassa, stars).

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.

        Returns:
            str: Отформатированная строка со статистикой платежей.
        """
        query = select(
            cls.model.payment_type,
            func.sum(cls.model.price).label('total_price')
        ).group_by(cls.model.payment_type)

        result = await session.execute(query)
        stats = result.all()

        # Словарь для хранения результатов
        totals: Dict[str, float] = {
            'yukassa': 0,
            'robocassa': 0,
            'stars': 0
        }

        # Заполняем словарь результатами запроса
        for payment_type, total in stats:
            totals[payment_type] = total or 0

        # Форматируем результат
        formatted_stats: str = (
            f'💳 Юкасса: {totals["yukassa"]:.2f} ₽\n'
            f'🤖 Робокасса: {totals["robocassa"]:.2f} ₽\n'
            f'⭐ STARS: {totals["stars"]:.0f}\n\n'
            'Статистика актуальна на данный момент.'
        )

        return formatted_stats

    @classmethod
    async def get_full_summ(cls, session: AsyncSession) -> int:
        """
        Получает полную сумму всех покупок.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.

        Returns:
            int: Полная сумма всех покупок.
        """
        query = select(func.sum(cls.model.price).label('total_price'))
        result = await session.execute(query)
        total_price = result.scalars().one_or_none()
        return total_price if total_price is not None else 0

    @classmethod
    async def get_next_id(cls, session: AsyncSession) -> int:
        """
        Возвращает следующий свободный ID для новой записи.

        Args:
            session: Асинхронная сессия базы данных
        Returns:
            Следующий свободный ID
        """
        query = select(func.coalesce(func.max(cls.model.id) + 1, 1))
        result = await session.execute(query)
        return result.scalar()


class CategoryDao(BaseDAO[Category]):
    """DAO для работы с моделью Category."""
    model = Category


class ProductDao(BaseDAO[Product]):
    """DAO для работы с моделью Product."""
    model = Product