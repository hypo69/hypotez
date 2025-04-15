### **Анализ кода модуля `database_middleware.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Использование `async` для асинхронных операций.
    - Наличие базового класса `BaseDatabaseMiddleware` для упрощения создания middleware для работы с БД.
    - Использование `async_session_maker` для создания асинхронных сессий.
    - Обработка исключений с rollback сессии.
- **Минусы**:
    - Отсутствует полное документирование классов и методов.
    - Используется `e` вместо `ex` в блоке обработки исключений.
    - Не используется logger для логирования ошибок.
    - Не все переменные аннотированы типами (например, `session` в методах `set_session` и `after_handler`).
    - Docstring на английском языке

#### **Рекомендации по улучшению**:

1.  **Документирование**:
    - Добавить docstring для каждого класса и метода, описывающий его назначение, аргументы и возвращаемые значения.
    - Перевести docstring на русский язык.
2.  **Обработка исключений**:
    - Использовать `ex` вместо `e` в блоках `except`.
    - Добавить логирование ошибок с использованием `logger` из `src.logger`.
3.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных, где это необходимо.
    - Явно указать тип переменной `session` в методах `set_session` и `after_handler`.
4.  **Комментарии**:
    - Добавить комментарии, объясняющие логику работы наиболее важных частей кода.
5.  **Именование переменных**:
    - Убедиться, что имена переменных отражают их назначение и соответствуют общепринятым стандартам.

#### **Оптимизированный код**:

```python
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.logger import logger # Импорт модуля логирования
from bot.dao.database import async_session_maker


class BaseDatabaseMiddleware(BaseMiddleware):
    """
    Базовый класс middleware для работы с базой данных.

    Этот класс обеспечивает создание и закрытие сессии базы данных для каждого обработчика.
    Подклассы должны реализовывать метод `set_session` для установки сессии в словарь данных.
    """
    async def __call__(
            self,
            handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        """
        Выполняет middleware.

        Создает асинхронную сессию базы данных, вызывает обработчик и выполняет необходимые действия после обработки.

        Args:
            handler (Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]]): Обработчик события.
            event (Message | CallbackQuery): Событие (сообщение или callback query).
            data (Dict[str, Any]): Словарь данных.

        Returns:
            Any: Результат выполнения обработчика.
        """
        async with async_session_maker() as session: # Создание асинхронной сессии
            self.set_session(data, session) # Установка сессии в словарь данных
            try:
                result = await handler(event, data) # Вызов обработчика
                await self.after_handler(session) # Выполнение действий после обработчика
                return result
            except Exception as ex: # Обработка исключений
                logger.error('Ошибка при обработке запроса', ex, exc_info=True) # Логирование ошибки
                await session.rollback() # Откат сессии
                raise ex
            finally:
                await session.close() # Закрытие сессии

    def set_session(self, data: Dict[str, Any], session: AsyncSession) -> None:
        """
        Устанавливает сессию в словарь данных.

        Этот метод должен быть реализован в подклассах для установки сессии базы данных в словарь данных,
        чтобы она была доступна обработчикам.

        Args:
            data (Dict[str, Any]): Словарь данных.
            session (AsyncSession): Сессия базы данных.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError('Этот метод должен быть реализован в подклассах.')

    async def after_handler(self, session: AsyncSession) -> None:
        """
        Выполняет действия после вызова обработчика (например, коммит).

        Этот метод может быть переопределен в подклассах для выполнения дополнительных действий после вызова обработчика,
        например, для выполнения коммита сессии.

        Args:
            session (AsyncSession): Сессия базы данных.
        """
        pass # Действия после обработчика (по умолчанию ничего не делает)


class DatabaseMiddlewareWithoutCommit(BaseDatabaseMiddleware):
    """
    Middleware для работы с базой данных без коммита.

    Этот класс устанавливает сессию базы данных в словарь данных без автоматического выполнения коммита.
    """
    def set_session(self, data: Dict[str, Any], session: AsyncSession) -> None:
        """
        Устанавливает сессию в словарь данных.

        Args:
            data (Dict[str, Any]): Словарь данных.
            session (AsyncSession): Сессия базы данных.
        """
        data['session_without_commit'] = session # Установка сессии без коммита


class DatabaseMiddlewareWithCommit(BaseDatabaseMiddleware):
    """
    Middleware для работы с базой данных с автоматическим коммитом.

    Этот класс устанавливает сессию базы данных в словарь данных и автоматически выполняет коммит после вызова обработчика.
    """
    def set_session(self, data: Dict[str, Any], session: AsyncSession) -> None:
        """
        Устанавливает сессию в словарь данных.

        Args:
            data (Dict[str, Any]): Словарь данных.
            session (AsyncSession): Сессия базы данных.
        """
        data['session_with_commit'] = session # Установка сессии с коммитом

    async def after_handler(self, session: AsyncSession) -> None:
        """
        Выполняет коммит сессии после вызова обработчика.

        Args:
            session (AsyncSession): Сессия базы данных.
        """
        await session.commit() # Выполнение коммита