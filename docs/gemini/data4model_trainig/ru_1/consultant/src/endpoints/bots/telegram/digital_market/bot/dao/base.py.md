### **Анализ кода модуля `base.py`**

#### **Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Использование асинхронности для работы с базой данных.
    - Применение `BaseModel` из `pydantic` для валидации данных.
    - Использование логирования для отслеживания операций с базой данных.
    - Применение обобщений (`Generic`) для обеспечения типовой безопасности.
    - Обработка исключений `SQLAlchemyError` с логированием ошибок.
- **Минусы**:
    - Отсутствует подробная документация модуля.
    - Некоторые комментарии можно улучшить, сделав их более конкретными.
    - Использование `e` вместо `ex` в блоках обработки исключений.
    - Нет обработки кейса, если `filter_dict` пустой при удалении.

#### **Рекомендации по улучшению:**

1.  **Документация модуля**:
    - Добавить заголовок и общее описание модуля.

2.  **Комментарии и документация**:
    - Добавить docstring к классу `BaseDAO`, описывающий его назначение.
    - Улучшить docstring для каждой функции, сделав описания более конкретными и информативными.

3.  **Обработка исключений**:
    - Использовать `ex` вместо `e` в блоках `except`.
    - В методе `delete` добавить более информативное сообщение об ошибке, если `filter_dict` пуст.

4.  **Использование `logger`**:
    - Убедиться, что все ошибки логируются с использованием `logger.error` и передачей исключения `ex` в качестве второго аргумента.

5.  **Аннотации типов**:
    - Все параметры и возвращаемые значения должны быть аннотированы типами.

6.  **Удаление записей**:
    - В методе `delete` можно добавить проверку, что фильтры не пустые, чтобы избежать случайного удаления всех записей.

7.  **Обновление записей**:
    - В методе `bulk_update` добавить проверку, что `id` присутствует в `record_dict`.

#### **Оптимизированный код:**

```python
from typing import List, Any, TypeVar, Generic
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete, func
from src.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.database import Base

# Объявляем типовой параметр T с ограничением, что это наследник Base
T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    """
    Базовый класс для DAO (Data Access Object), предоставляющий общие методы для работы с базой данных.
    """
    model: type[T]

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int, session: AsyncSession) -> T | None:
        """
        Найти запись по ID.

        Args:
            data_id (int): ID записи.
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            T | None: Найденная запись или None, если запись не найдена.

        Raises:
            SQLAlchemyError: При возникновении ошибки при выполнении запроса к базе данных.
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
        except SQLAlchemyError as ex:
            logger.error(f'Ошибка при поиске записи с ID {data_id}: {ex}', exc_info=True)
            raise

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, filters: BaseModel) -> T | None:
        """
        Найти одну запись по фильтрам.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            filters (BaseModel): Фильтры для поиска записи.

        Returns:
            T | None: Найденная запись или None, если запись не найдена.

        Raises:
            SQLAlchemyError: При возникновении ошибки при выполнении запроса к базе данных.
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
        except SQLAlchemyError as ex:
            logger.error(f'Ошибка при поиске записи по фильтрам {filter_dict}: {ex}', exc_info=True)
            raise

    @classmethod
    async def find_all(cls, session: AsyncSession, filters: BaseModel | None = None) -> List[T]:
        """
        Найти все записи по фильтрам.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            filters (BaseModel | None, optional): Фильтры для поиска записей. Defaults to None.

        Returns:
            List[T]: Список найденных записей.

        Raises:
            SQLAlchemyError: При возникновении ошибки при выполнении запроса к базе данных.
        """
        filter_dict = filters.model_dump(exclude_unset=True) if filters else {}
        logger.info(f'Поиск всех записей {cls.model.__name__} по фильтрам: {filter_dict}')
        try:
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query)
            records = result.scalars().all()
            logger.info(f'Найдено {len(records)} записей.')
            return records
        except SQLAlchemyError as ex:
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
            T: Созданная запись.

        Raises:
            SQLAlchemyError: При возникновении ошибки при выполнении запроса к базе данных.
        """
        values_dict = values.model_dump(exclude_unset=True)
        logger.info(f'Добавление записи {cls.model.__name__} с параметрами: {values_dict}')
        new_instance = cls.model(**values_dict)
        session.add(new_instance)
        try:
            await session.flush()
            logger.info(f'Запись {cls.model.__name__} успешно добавлена.')
        except SQLAlchemyError as ex:
            await session.rollback()
            logger.error(f'Ошибка при добавлении записи: {ex}', exc_info=True)
            raise ex
        return new_instance

    @classmethod
    async def add_many(cls, session: AsyncSession, instances: List[BaseModel]) -> List[T]:
        """
        Добавить несколько записей.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            instances (List[BaseModel]): Список экземпляров для добавления.

        Returns:
            List[T]: Список созданных записей.

        Raises:
            SQLAlchemyError: При возникновении ошибки при выполнении запроса к базе данных.
        """
        values_list = [item.model_dump(exclude_unset=True) for item in instances]
        logger.info(f'Добавление нескольких записей {cls.model.__name__}. Количество: {len(values_list)}')
        new_instances = [cls.model(**values) for values in values_list]
        session.add_all(new_instances)
        try:
            await session.flush()
            logger.info(f'Успешно добавлено {len(new_instances)} записей.')
        except SQLAlchemyError as ex:
            await session.rollback()
            logger.error(f'Ошибка при добавлении нескольких записей: {ex}', exc_info=True)
            raise ex
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
            SQLAlchemyError: При возникновении ошибки при выполнении запроса к базе данных.
        """
        filter_dict = filters.model_dump(exclude_unset=True)
        values_dict = values.model_dump(exclude_unset=True)
        logger.info(f'Обновление записей {cls.model.__name__} по фильтру: {filter_dict} с параметрами: {values_dict}')
        query = (
            sqlalchemy_update(cls.model)
            .where(*[getattr(cls.model, k) == v for k, v in filter_dict.items()])
            .values(**values_dict)
            .execution_options(synchronize_session="fetch")
        )
        try:
            result = await session.execute(query)
            await session.flush()
            logger.info(f'Обновлено {result.rowcount} записей.')
            return result.rowcount
        except SQLAlchemyError as ex:
            await session.rollback()
            logger.error(f'Ошибка при обновлении записей: {ex}', exc_info=True)
            raise ex

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
            ValueError: Если не указаны фильтры для удаления.
            SQLAlchemyError: При возникновении ошибки при выполнении запроса к базе данных.
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
        except SQLAlchemyError as ex:
            await session.rollback()
            logger.error(f'Ошибка при удалении записей: {ex}', exc_info=True)
            raise ex

    @classmethod
    async def count(cls, session: AsyncSession, filters: BaseModel | None = None) -> int:
        """
        Подсчитать количество записей.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            filters (BaseModel | None, optional): Фильтры для подсчета записей. Defaults to None.

        Returns:
            int: Количество записей.

        Raises:
            SQLAlchemyError: При возникновении ошибки при выполнении запроса к базе данных.
        """
        filter_dict = filters.model_dump(exclude_unset=True) if filters else {}
        logger.info(f'Подсчет количества записей {cls.model.__name__} по фильтру: {filter_dict}')
        try:
            query = select(func.count(cls.model.id)).filter_by(**filter_dict)
            result = await session.execute(query)
            count = result.scalar()
            logger.info(f'Найдено {count} записей.')
            return count
        except SQLAlchemyError as ex:
            logger.error(f'Ошибка при подсчете записей: {ex}', exc_info=True)
            raise

    @classmethod
    async def paginate(cls, session: AsyncSession, page: int = 1, page_size: int = 10, filters: BaseModel | None = None) -> List[T]:
        """
        Пагинация записей.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            page (int, optional): Номер страницы. Defaults to 1.
            page_size (int, optional): Размер страницы. Defaults to 10.
            filters (BaseModel | None, optional): Фильтры для пагинации. Defaults to None.

        Returns:
            List[T]: Список записей на странице.

        Raises:
            SQLAlchemyError: При возникновении ошибки при выполнении запроса к базе данных.
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
        except SQLAlchemyError as ex:
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
            SQLAlchemyError: При возникновении ошибки при выполнении запроса к базе данных.
        """
        logger.info(f'Поиск записей {cls.model.__name__} по списку ID: {ids}')
        try:
            query = select(cls.model).filter(cls.model.id.in_(ids))
            result = await session.execute(query)
            records = result.scalars().all()
            logger.info(f'Найдено {len(records)} записей по списку ID.')
            return records
        except SQLAlchemyError as ex:
            logger.error(f'Ошибка при поиске записей по списку ID: {ex}', exc_info=True)
            raise

    @classmethod
    async def upsert(cls, session: AsyncSession, unique_fields: List[str], values: BaseModel) -> T:
        """
        Создать запись или обновить существующую на основе уникальных полей.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            unique_fields (List[str]): Список уникальных полей для поиска существующей записи.
            values (BaseModel): Значения для создания или обновления записи.

        Returns:
            T: Созданная или обновленная запись.

        Raises:
            SQLAlchemyError: При возникновении ошибки при выполнении запроса к базе данных.
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
        except SQLAlchemyError as ex:
            await session.rollback()
            logger.error(f'Ошибка при upsert: {ex}', exc_info=True)
            raise

    @classmethod
    async def bulk_update(cls, session: AsyncSession, records: List[BaseModel]) -> int:
        """
        Массовое обновление записей.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            records (List[BaseModel]): Список экземпляров с данными для обновления.

        Returns:
            int: Количество обновленных записей.

        Raises:
            SQLAlchemyError: При возникновении ошибки при выполнении запроса к базе данных.
        """
        logger.info(f'Массовое обновление записей {cls.model.__name__}')
        try:
            updated_count = 0
            for record in records:
                record_dict = record.model_dump(exclude_unset=True)
                if 'id' not in record_dict:
                    logger.warning(f'Пропущена запись, так как отсутствует id: {record_dict}')
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
        except SQLAlchemyError as ex:
            await session.rollback()
            logger.error(f'Ошибка при массовом обновлении: {ex}', exc_info=True)
            raise