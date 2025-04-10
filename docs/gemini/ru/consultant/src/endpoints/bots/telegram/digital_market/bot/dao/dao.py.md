### **Анализ кода модуля `dao.py`**

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Использование асинхронных сессий SQLAlchemy для работы с базой данных.
  - Применение `selectinload` для оптимизации запросов и избежания N+1 проблемы.
  - Использование `logger` для логирования операций и ошибок.
  - Четкая структура DAO классов для каждой модели.
- **Минусы**:
  - Не везде используется `logger.error` с передачей исключения (например, в `UserDAO`).
  - В некоторых местах используются `print` вместо `logger`.
  - Отсутствуют docstring для некоторых методов (например, `get_next_id` в `PurchaseDao`).
  - В блоках `except` используется переменная `e` вместо `ex`.
  - Не все переменные аннотированы типами.

**Рекомендации по улучшению**:

1.  **Документирование кода**:
    - Добавить docstring для метода `get_next_id` в классе `PurchaseDao`.
    - Убедиться, что все методы и классы имеют docstring, описывающие их назначение, аргументы, возвращаемые значения и возможные исключения.
2.  **Обработка исключений**:
    - Использовать `logger.error` вместо `print` для логирования ошибок, передавая исключение `ex` и `exc_info=True`.
    - Переименовать переменную исключения `e` в `ex` в блоках `except`.
3.  **Логирование**:
    - Добавить логирование в методы, где оно отсутствует.
4.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных, где они отсутствуют.
5.  **Использование одинарных кавычек**:
    - Заменить двойные кавычки на одинарные там, где это необходимо.
6. **Использовать вебдрайвер**
    - В данном коде не используются функции вебдрайвера. В связи с этим советовать тут нечего

**Оптимизированный код**:

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
    model = User

    @classmethod
    async def get_purchase_statistics(
        cls, session: AsyncSession, telegram_id: int
    ) -> Optional[Dict[str, int]]:
        """
        Получает статистику покупок пользователя.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.
            telegram_id (int): Telegram ID пользователя.

        Returns:
            Optional[Dict[str, int]]: Словарь со статистикой покупок пользователя или None в случае ошибки.
        """
        try:
            # Запрос для получения общего числа покупок и общей суммы
            result = await session.execute(
                select(
                    func.count(Purchase.id).label('total_purchases'),
                    func.sum(Purchase.price).label('total_amount'),
                )
                .join(User)
                .filter(User.telegram_id == telegram_id)
            )
            stats = result.one_or_none()

            if stats is None:
                return None

            total_purchases, total_amount = stats
            return {
                'total_purchases': total_purchases,
                'total_amount': total_amount or 0,  # Обработка случая, когда сумма может быть None
            }

        except SQLAlchemyError as ex:
            # Обработка ошибок при работе с базой данных
            logger.error(
                'Ошибка при получении статистики покупок пользователя', ex, exc_info=True
            )
            return None

    @classmethod
    async def get_purchased_products(
        cls, session: AsyncSession, telegram_id: int
    ) -> Optional[List[Purchase]]:
        """
        Получает список покупок пользователя.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.
            telegram_id (int): Telegram ID пользователя.

        Returns:
            Optional[List[Purchase]]: Список покупок пользователя или None в случае ошибки.
        """
        try:
            # Запрос для получения пользователя с его покупками и связанными продуктами
            result = await session.execute(
                select(User)
                .options(selectinload(User.purchases).selectinload(Purchase.product))
                .filter(User.telegram_id == telegram_id)
            )
            user = result.scalar_one_or_none()

            if user is None:
                return None

            return user.purchases

        except SQLAlchemyError as ex:
            # Обработка ошибок при работе с базой данных
            logger.error(
                'Ошибка при получении информации о покупках пользователя',
                ex,
                exc_info=True,
            )
            return None

    @classmethod
    async def get_statistics(cls, session: AsyncSession) -> Dict[str, Optional[int]]:
        """
        Получает общую статистику пользователей.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.

        Returns:
            Dict[str, Optional[int]]: Словарь с общей статистикой пользователей.
        """
        try:
            now: datetime = datetime.now(UTC)

            query = select(
                func.count().label('total_users'),
                func.sum(
                    case((cls.model.created_at >= now - timedelta(days=1), 1), else_=0)
                ).label('new_today'),
                func.sum(
                    case((cls.model.created_at >= now - timedelta(days=7), 1), else_=0)
                ).label('new_week'),
                func.sum(
                    case((cls.model.created_at >= now - timedelta(days=30), 1), else_=0)
                ).label('new_month'),
            )

            result = await session.execute(query)
            stats = result.fetchone()

            statistics: Dict[str, Optional[int]] = {
                'total_users': stats.total_users,
                'new_today': stats.new_today,
                'new_week': stats.new_week,
                'new_month': stats.new_month,
            }

            logger.info(f'Статистика успешно получена: {statistics}')
            return statistics
        except SQLAlchemyError as ex:
            logger.error('Ошибка при получении статистики', ex, exc_info=True)
            raise


class PurchaseDao(BaseDAO[Purchase]):
    model = Purchase

    @classmethod
    async def get_payment_stats(cls, session: AsyncSession) -> str:
        """
        Получает статистику по типам оплат.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.

        Returns:
            str: Форматированная строка со статистикой по типам оплат.
        """
        query = select(
            cls.model.payment_type, func.sum(cls.model.price).label('total_price')
        ).group_by(cls.model.payment_type)

        result = await session.execute(query)
        stats = result.all()

        # Словарь для хранения результатов
        totals: Dict[str, float] = {'yukassa': 0, 'robocassa': 0, 'stars': 0}

        # Заполняем словарь результатами запроса
        for payment_type, total in stats:
            totals[payment_type] = total or 0

        # Форматируем результат
        formatted_stats: str = (
            f'💳 Юкасса: {totals["yukassa"]:.2f} ₽\n'
            f'🤖 Робокасса: {totals["robocassa"]:.2f} ₽\n'
            f'⭐ STARS: {totals["stars"]:.0f}\n\n'
            f'Статистика актуальна на данный момент.'
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
        total_price: Optional[float] = result.scalars().one_or_none()
        return int(total_price) if total_price is not None else 0

    @classmethod
    async def get_next_id(cls, session: AsyncSession) -> int:
        """
        Возвращает следующий свободный ID для новой записи.

        Args:
            session: Асинхронная сессия базы данных
        Returns: Следующий свободный ID
        """
        query = select(func.coalesce(func.max(cls.model.id) + 1, 1))
        result: Any = await session.execute(query)
        return result.scalar()


class CategoryDao(BaseDAO[Category]):
    model = Category


class ProductDao(BaseDAO[Product]):
    model = Product