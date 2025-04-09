### **Анализ кода модуля `dao.py`**

## \file /hypotez/src/endpoints/bots/telegram/digital_market/bot/dao/dao.py

#### **1. Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Использование асинхронных сессий SQLAlchemy для работы с базой данных.
    - Применение `selectinload` для оптимизации запросов и избежания N+1 проблемы.
    - Обработка исключений `SQLAlchemyError` для обеспечения стабильности работы с базой данных.
    - Использование `logger` для логирования информации и ошибок.
    - Аннотации типов.

- **Минусы**:
    - Отсутствует docstring в некоторых методах.
    - Не все ошибки логируются с использованием `logger.error`.
    - Использование `print` вместо `logger.error` для логирования ошибок в некоторых блоках `except`.
    - Не везде обрабатываются ситуации, когда возвращается `None` из базы данных.

#### **2. Рекомендации по улучшению:**

1.  **Добавить docstring к методам**:
    - Добавить docstring к методам `get_payment_stats`, `get_full_summ`, `get_next_id` классов `PurchaseDao`, чтобы описать их назначение, аргументы и возвращаемые значения.

2.  **Заменить `print` на `logger.error`**:
    - Заменить `print(f"Ошибка при получении статистики покупок пользователя: {e}")` и `print(f"Ошибка при получении информации о покупках пользователя: {e}")` на `logger.error(f"Ошибка при получении статистики покупок пользователя", e, exc_info=True)` и `logger.error(f"Ошибка при получении информации о покупках пользователя", e, exc_info=True)` соответственно, чтобы использовать стандартизированный подход к логированию ошибок.

3.  **Обработка `None` значений**:
    - В методе `get_purchase_statistics` добавить явную проверку на `None` для `total_amount` перед присваиванием значения.

4.  **Улучшить docstring для `get_next_id`**:
    - Добавить пример использования в docstring для `get_next_id`.

5. **Использовать одинарные кавычки**:
    - Заменить двойные кавычки на одинарные в строках форматирования `f"..."`

6.  **Добавить аннотации типа**:
    - Добавить аннотации типа для локальных переменных, где это необходимо, чтобы повысить читаемость кода.

#### **3. Оптимизированный код:**

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
    async def get_purchase_statistics(cls, session: AsyncSession, telegram_id: int) -> Optional[Dict[str, int]]:
        """
        Получает статистику покупок пользователя.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.
            telegram_id (int): Telegram ID пользователя.

        Returns:
            Optional[Dict[str, int]]: Словарь со статистикой покупок пользователя (общее число покупок и общая сумма)
            или None в случае ошибки.
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
        Получает общую статистику пользователей.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.

        Returns:
            Dict[str, int]: Словарь со статистикой пользователей (общее количество, новые за сегодня, за неделю, за месяц).

        Raises:
            SQLAlchemyError: Если возникает ошибка при работе с базой данных.
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

            if stats is None:
                # Обработка случая, когда статистика не найдена
                return {
                    'total_users': 0,
                    'new_today': 0,
                    'new_week': 0,
                    'new_month': 0
                }

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
    model = Purchase

    @classmethod
    async def get_payment_stats(cls, session: AsyncSession) -> str:
        """
        Получает статистику по типам оплат.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.

        Returns:
            str: Отформатированная строка со статистикой по типам оплат.
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
            session (AsyncSession): Асинхронная сессия базы данных

        Returns:
            int: Следующий свободный ID

        Example:
            >>> session = ...  #  Подставьте свою асинхронную сессию SQLAlchemy
            >>> next_id = await PurchaseDao.get_next_id(session)
            >>> print(next_id)
            1
        """
        query = select(func.coalesce(func.max(cls.model.id) + 1, 1))
        result = await session.execute(query)
        return result.scalar()


class CategoryDao(BaseDAO[Category]):
    model = Category


class ProductDao(BaseDAO[Product]):
    model = Product