### **Анализ кода модуля `database_middleware.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Четкая структура middleware для управления сессиями базы данных.
  - Использование `async with` для управления сессией.
  - Разделение middleware на два типа: с коммитом и без.
- **Минусы**:
  - Не все методы документированы в соответствии с требуемым форматом.
  - Отсутствует обработка конкретных исключений, что может затруднить отладку.
  - Не используется `logger` для логирования ошибок.
  - Не указаны типы для `session` в методах `set_session` и `after_handler`.

#### **Рекомендации по улучшению**:
1. **Документирование методов**:
   - Добавить docstring к методам `set_session` и `after_handler` в базовом классе `BaseDatabaseMiddleware` и в подклассах `DatabaseMiddlewareWithoutCommit` и `DatabaseMiddlewareWithCommit`.
2. **Обработка исключений**:
   - Логировать исключения с использованием `logger.error` с передачей информации об ошибке (`ex`) и трассировки (`exc_info=True`).
3. **Типизация**:
   - Указать тип для параметра `session` в методах `set_session` и `after_handler`.
4. **Комментарии**:
   - Добавить комментарии, объясняющие назначение каждого блока кода, особенно в методах `set_session` и `after_handler`.
5. **Использовать одинарные кавычки**:
   - Заменить двойные кавычки на одинарные.

#### **Оптимизированный код**:

```python
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.database import async_session_maker
from src.logger import logger


class BaseDatabaseMiddleware(BaseMiddleware):
    """
    Базовый класс middleware для управления сессиями базы данных.
    """

    async def __call__(
            self,
            handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        """
        Выполняет middleware.

        Args:
            handler (Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]]): Обработчик события.
            event (Message | CallbackQuery): Событие (сообщение или callback-запрос).
            data (Dict[str, Any]): Дополнительные данные.

        Returns:
            Any: Результат обработки события.

        Raises:
            Exception: Если при выполнении обработчика или коммита возникает ошибка, выполняется откат сессии.
        """
        async with async_session_maker() as session:
            self.set_session(data, session)
            try:
                result = await handler(event, data) # Вызов обработчика события
                await self.after_handler(session) # Выполнение действий после обработчика
                return result
            except Exception as ex: # Обработка исключений
                logger.error('Error during handler execution or commit', ex, exc_info=True)
                await session.rollback() # Откат изменений в случае ошибки
                raise ex
            finally:
                await session.close() # Закрытие сессии

    def set_session(self, data: Dict[str, Any], session: AsyncSession) -> None:
        """
        Устанавливает сессию в словарь данных.

        Args:
            data (Dict[str, Any]): Словарь данных, в который будет добавлена сессия.
            session (AsyncSession): Сессия базы данных.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError('Этот метод должен быть реализован в подклассах.')

    async def after_handler(self, session: AsyncSession) -> None:
        """
        Выполняет действия после вызова хендлера (например, коммит).

        Args:
            session (AsyncSession): Сессия базы данных.
        """
        pass


class DatabaseMiddlewareWithoutCommit(BaseDatabaseMiddleware):
    """
    Middleware для работы с базой данных без автоматического коммита.
    """

    def set_session(self, data: Dict[str, Any], session: AsyncSession) -> None:
        """
        Устанавливает сессию без коммита в словарь данных.

        Args:
            data (Dict[str, Any]): Словарь данных, в который будет добавлена сессия.
            session (AsyncSession): Сессия базы данных.
        """
        data['session_without_commit'] = session


class DatabaseMiddlewareWithCommit(BaseDatabaseMiddleware):
    """
    Middleware для работы с базой данных с автоматическим коммитом.
    """

    def set_session(self, data: Dict[str, Any], session: AsyncSession) -> None:
        """
        Устанавливает сессию с коммитом в словарь данных.

        Args:
            data (Dict[str, Any]): Словарь данных, в который будет добавлена сессия.
            session (AsyncSession): Сессия базы данных.
        """
        data['session_with_commit'] = session

    async def after_handler(self, session: AsyncSession) -> None:
        """
        Выполняет коммит сессии после вызова хендлера.

        Args:
            session (AsyncSession): Сессия базы данных.
        """
        await session.commit()