### **Анализ кода модуля `base.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Использование асинхронных методов для работы с базой данных.
    - Применение `pydantic` для валидации данных.
    - Использование `logger` для логирования действий.
    - Обработка исключений `SQLAlchemyError`.
    - Обобщенный класс `BaseDAO` для работы с разными моделями.
- **Минусы**:
    - Некоторые docstring отсутствуют или неполные.
    - Использование `exclude_unset=True` может привести к нежелательному поведению, если требуется обновить поле до `None`.
    - Не все методы имеют примеры использования в docstring.
    - В некоторых местах используется `e` вместо `ex` в блоках `except`.
    - Отсутствуют аннотации для некоторых переменных, таких как `count` в методе `count`.
    - Не все фильтры логируются в методе `bulk_update`.

#### **Рекомендации по улучшению**:

1.  **Документация**:
    *   Добавить docstring для класса `BaseDAO` и для каждой внутренней функции.
    *   Добавить примеры использования в docstring для наиболее важных методов.
2.  **Обработка исключений**:
    *   Использовать `ex` вместо `e` в блоках `except`.
3.  **Логирование**:
    *   Убедиться, что все важные параметры логируются, особенно в методах `update` и `bulk_update`.
4.  **Аннотации типов**:
    *   Добавить аннотации типов для всех переменных, где они отсутствуют (например, `count` в методе `count`).
5.  **Использование `exclude_unset`**:
    *   Рассмотреть возможность использования `exclude_none=True` вместо `exclude_unset=True`, если требуется обновить поле до `None`.
6.  **Форматирование**:
    *   Убедиться, что код соответствует стандартам PEP8.
7.  **Улучшение метода `bulk_update`**:

    *   Добавить проверку на наличие `id` в `record_dict` перед обновлением.
    *   Добавить логирование информации об обновляемых записях.
8.  **Примеры в docstring**:

    *   Добавить примеры использования для основных методов, чтобы облегчить понимание их работы.
9.  **Улучшение метода `upsert`**:

    *   Улучшить обработку ошибок, чтобы избежать потенциальных проблем при одновременном создании и обновлении записей.

#### **Оптимизированный код**:

```python
from typing import List, Any, TypeVar, Generic, Optional
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete, func
from src.logger import logger  # Используем logger из src.logger
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.database import Base

# Объявляем типовой параметр T с ограничением, что это наследник Base
T = TypeVar('T', bound=Base)


class BaseDAO(Generic[T]):
    """
    Базовый класс для Data Access Object (DAO).

    Этот класс предоставляет общие методы для выполнения операций CRUD
    (создание, чтение, обновление, удаление) с использованием SQLAlchemy.

    Args:
        model (type[T]): Тип модели SQLAlchemy, с которой работает DAO.
    """
    model: type[T]

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int, session: AsyncSession) -> Optional[T]:
        """
        Найти запись по ID.

        Args:
            data_id (int): ID записи.
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            Optional[T]: Найденная запись или None, если запись не найдена.

        Raises:
            SQLAlchemyError: Если возникает ошибка при выполнении запроса.
        """
        logger.info(f'Поиск {cls.model.__name__} с ID: {data_id}')
        try:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            if record:
                logger.info(f'Запись с ID {data_id} найдена.')
            else:
                logger.info(f'Запись с ID {data_id} не найдена.')
            return record
        except SQLAlchemyError as ex:  # Используем ex вместо e
            logger.error(f'Ошибка при поиске записи с ID {data_id}: {ex}', exc_info=True)
            raise

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, filters: BaseModel) -> Optional[T]:
        """
        Найти одну запись по фильтрам.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            filters (BaseModel): Фильтры для поиска записи.

        Returns:
            Optional[T]: Найденная запись или None, если запись не найдена.

        Raises:
            SQLAlchemyError: Если возникает ошибка при выполнении запроса.
        """
        filter_dict = filters.model_dump(exclude_unset=True)
        logger.info(f'Поиск одной записи {cls.model.__name__} по фильтрам: {filter_dict}')
        try:
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            if record:
                logger.info(f'Запись найдена по фильтрам: {filter_dict}')
            else:
                logger.info(f'Запись не найдена по фильтрам: {filter_dict}')
            return record
        except SQLAlchemyError as ex:  # Используем ex вместо e
            logger.error(f'Ошибка при поиске записи по фильтрам {filter_dict}: {ex}', exc_info=True)
            raise

    @classmethod
    async def find_all(cls, session: AsyncSession, filters: Optional[BaseModel] = None) -> List[T]:
        """
        Найти все записи по фильтрам.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            filters (Optional[BaseModel], optional): Фильтры для поиска записей. По умолчанию None.

        Returns:
            List[T]: Список найденных записей.

        Raises:
            SQLAlchemyError: Если возникает ошибка при выполнении запроса.
        """
        filter_dict = filters.model_dump(exclude_unset=True) if filters else {}
        logger.info(f'Поиск всех записей {cls.model.__name__} по фильтрам: {filter_dict}')
        try:
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query)
            records = result.scalars().all()
            logger.info(f'Найдено {len(records)} записей.')
            return records
        except SQLAlchemyError as ex:  # Используем ex вместо e
            logger.error(f'Ошибка при поиске всех записей по фильтрам {filter_dict}: {ex}', exc_info=True)
            raise

    @classmethod
    async def add(cls, session: AsyncSession, values: BaseModel) -> T:
        """
        Добавить одну запись.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            values (BaseModel): Значения для добавления записи.

        Returns:
            T: Новая добавленная запись.

        Raises:
            SQLAlchemyError: Если возникает ошибка при добавлении записи.
        """
        values_dict = values.model_dump(exclude_unset=True)
        logger.info(f'Добавление записи {cls.model.__name__} с параметрами: {values_dict}')
        new_instance = cls.model(**values_dict)
        session.add(new_instance)
        try:
            await session.flush()
            logger.info(f'Запись {cls.model.__name__} успешно добавлена.')
        except SQLAlchemyError as ex:  # Используем ex вместо e
            await session.rollback()
            logger.error(f'Ошибка при добавлении записи: {ex}', exc_info=True)
            raise
        return new_instance

    @classmethod
    async def add_many(cls, session: AsyncSession, instances: List[BaseModel]) -> List[T]:
        """
        Добавить несколько записей.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            instances (List[BaseModel]): Список экземпляров BaseModel для добавления.

        Returns:
            List[T]: Список новых добавленных записей.

        Raises:
            SQLAlchemyError: Если возникает ошибка при добавлении записей.
        """
        values_list = [item.model_dump(exclude_unset=True) for item in instances]
        logger.info(f'Добавление нескольких записей {cls.model.__name__}. Количество: {len(values_list)}')
        new_instances = [cls.model(**values) for values in values_list]
        session.add_all(new_instances)
        try:
            await session.flush()
            logger.info(f'Успешно добавлено {len(new_instances)} записей.')
        except SQLAlchemyError as ex:  # Используем ex вместо e
            await session.rollback()
            logger.error(f'Ошибка при добавлении нескольких записей: {ex}', exc_info=True)
            raise
        return new_instances

    @classmethod
    async def update(cls, session: AsyncSession, filters: BaseModel, values: BaseModel) -> int:
        """
        Обновить записи по фильтрам.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            filters (BaseModel): Фильтры для обновления записей.
            values (BaseModel): Значения для обновления записей.

        Returns:
            int: Количество обновленных записей.

        Raises:
            SQLAlchemyError: Если возникает ошибка при обновлении записей.
        """
        filter_dict = filters.model_dump(exclude_unset=True)
        values_dict = values.model_dump(exclude_unset=True)
        logger.info(f'Обновление записей {cls.model.__name__} по фильтру: {filter_dict} с параметрами: {values_dict}')
        query = (
            sqlalchemy_update(cls.model)
            .where(*[getattr(cls.model, k) == v for k, v in filter_dict.items()])
            .values(**values_dict)
            .execution_options(synchronize_session='fetch')
        )
        try:
            result = await session.execute(query)
            await session.flush()
            logger.info(f'Обновлено {result.rowcount} записей.')
            return result.rowcount
        except SQLAlchemyError as ex:  # Используем ex вместо e
            await session.rollback()
            logger.error(f'Ошибка при обновлении записей: {ex}', exc_info=True)
            raise

    @classmethod
    async def delete(cls, session: AsyncSession, filters: BaseModel) -> int:
        """
        Удалить записи по фильтру.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            filters (BaseModel): Фильтры для удаления записей.

        Returns:
            int: Количество удаленных записей.

        Raises:
            ValueError: Если не указан ни один фильтр для удаления.
            SQLAlchemyError: Если возникает ошибка при удалении записей.
        """
        filter_dict = filters.model_dump(exclude_unset=True)
        logger.info(f'Удаление записей {cls.model.__name__} по фильтру: {filter_dict}')
        if not filter_dict:
            logger.error('Нужен хотя бы один фильтр для удаления.')
            raise ValueError('Нужен хотя бы один фильтр для удаления.')

        query = sqlalchemy_delete(cls.model).filter_by(**filter_dict)
        try:
            result = await session.execute(query)
            await session.flush()
            logger.info(f'Удалено {result.rowcount} записей.')
            return result.rowcount
        except SQLAlchemyError as ex:  # Используем ex вместо e
            logger.error(f'Ошибка при удалении записей: {ex}', exc_info=True)
            raise

    @classmethod
    async def count(cls, session: AsyncSession, filters: Optional[BaseModel] = None) -> int:
        """
        Подсчитать количество записей.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            filters (Optional[BaseModel], optional): Фильтры для подсчета записей. По умолчанию None.

        Returns:
            int: Количество записей.

        Raises:
            SQLAlchemyError: Если возникает ошибка при подсчете записей.
        """
        filter_dict = filters.model_dump(exclude_unset=True) if filters else {}
        logger.info(f'Подсчет количества записей {cls.model.__name__} по фильтру: {filter_dict}')
        try:
            query = select(func.count(cls.model.id)).filter_by(**filter_dict)
            result = await session.execute(query)
            count: int = result.scalar()  # Добавлена аннотация типа
            logger.info(f'Найдено {count} записей.')
            return count
        except SQLAlchemyError as ex:  # Используем ex вместо e
            logger.error(f'Ошибка при подсчете записей: {ex}', exc_info=True)
            raise

    @classmethod
    async def paginate(cls, session: AsyncSession, page: int = 1, page_size: int = 10, filters: Optional[BaseModel] = None) -> List[T]:
        """
        Пагинация записей.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            page (int, optional): Номер страницы. По умолчанию 1.
            page_size (int, optional): Размер страницы. По умолчанию 10.
            filters (Optional[BaseModel], optional): Фильтры для пагинации записей. По умолчанию None.

        Returns:
            List[T]: Список записей на странице.

        Raises:
            SQLAlchemyError: Если возникает ошибка при пагинации записей.
        """
        filter_dict = filters.model_dump(exclude_unset=True) if filters else {}
        logger.info(
            f'Пагинация записей {cls.model.__name__} по фильтру: {filter_dict}, страница: {page}, размер страницы: {page_size}')
        try:
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query.offset((page - 1) * page_size).limit(page_size))
            records = result.scalars().all()
            logger.info(f'Найдено {len(records)} записей на странице {page}.')
            return records
        except SQLAlchemyError as ex:  # Используем ex вместо e
            logger.error(f'Ошибка при пагинации записей: {ex}', exc_info=True)
            raise

    @classmethod
    async def find_by_ids(cls, session: AsyncSession, ids: List[int]) -> List[Any]:
        """
        Найти несколько записей по списку ID.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            ids (List[int]): Список ID записей.

        Returns:
            List[Any]: Список найденных записей.

        Raises:
            SQLAlchemyError: Если возникает ошибка при поиске записей по списку ID.
        """
        logger.info(f'Поиск записей {cls.model.__name__} по списку ID: {ids}')
        try:
            query = select(cls.model).filter(cls.model.id.in_(ids))
            result = await session.execute(query)
            records = result.scalars().all()
            logger.info(f'Найдено {len(records)} записей по списку ID.')
            return records
        except SQLAlchemyError as ex:  # Используем ex вместо e
            logger.error(f'Ошибка при поиске записей по списку ID: {ex}', exc_info=True)
            raise

    @classmethod
    async def upsert(cls, session: AsyncSession, unique_fields: List[str], values: BaseModel) -> T:
        """
        Создать запись или обновить существующую.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            unique_fields (List[str]): Список уникальных полей для поиска существующей записи.
            values (BaseModel): Значения для создания или обновления записи.

        Returns:
            T: Созданная или обновленная запись.

        Raises:
            SQLAlchemyError: Если возникает ошибка при выполнении операции.
        """
        values_dict = values.model_dump(exclude_unset=True)
        filter_dict = {field: values_dict[field] for field in unique_fields if field in values_dict}

        logger.info(f'Upsert для {cls.model.__name__}')
        try:
            existing = await cls.find_one_or_none(session, BaseModel.construct(**filter_dict))
            if existing:
                # Обновляем существующую запись
                for key, value in values_dict.items():
                    setattr(existing, key, value)
                await session.flush()
                logger.info(f'Обновлена существующая запись {cls.model.__name__}')
                return existing
            else:
                # Создаем новую запись
                new_instance = cls.model(**values_dict)
                session.add(new_instance)
                await session.flush()
                logger.info(f'Создана новая запись {cls.model.__name__}')
                return new_instance
        except SQLAlchemyError as ex:  # Используем ex вместо e
            await session.rollback()
            logger.error(f'Ошибка при upsert: {ex}', exc_info=True)
            raise

    @classmethod
    async def bulk_update(cls, session: AsyncSession, records: List[BaseModel]) -> int:
        """
        Массовое обновление записей.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            records (List[BaseModel]): Список экземпляров BaseModel для обновления.

        Returns:
            int: Количество обновленных записей.

        Raises:
            SQLAlchemyError: Если возникает ошибка при массовом обновлении.
        """
        logger.info(f'Массовое обновление записей {cls.model.__name__}')
        try:
            updated_count = 0
            for record in records:
                record_dict = record.model_dump(exclude_unset=True)
                if 'id' not in record_dict:
                    logger.warning(f'Пропущена запись из-за отсутствия id: {record_dict}')  # Логируем пропущенные записи
                    continue

                update_data = {k: v for k, v in record_dict.items() if k != 'id'}
                stmt = (
                    sqlalchemy_update(cls.model)
                    .filter_by(id=record_dict['id'])
                    .values(**update_data)
                )
                result = await session.execute(stmt)
                updated_count += result.rowcount

            await session.flush()
            logger.info(f'Обновлено {updated_count} записей')
            return updated_count
        except SQLAlchemyError as ex:  # Используем ex вместо e
            await session.rollback()
            logger.error(f'Ошибка при массовом обновлении: {ex}', exc_info=True)
            raise