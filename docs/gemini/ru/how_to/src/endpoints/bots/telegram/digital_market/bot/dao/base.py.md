### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
`BaseDAO` - это базовый класс для Data Access Objects (DAO), который предоставляет набор методов для выполнения стандартных операций базы данных, таких как создание, чтение, обновление и удаление (CRUD). Он использует SQLAlchemy для взаимодействия с базой данных и предназначен для работы с асинхронными сессиями.

Шаги выполнения
-------------------------
1. **Импортируйте необходимые модули**:
   - `typing` для аннотации типов.
   - `pydantic` для работы с моделями данных.
   - `sqlalchemy` для взаимодействия с базой данных.
   - `loguru` для логирования.
   - `sqlalchemy.ext.asyncio` для асинхронных сессий.
   - `Base` из `bot.dao.database` как базовую модель для DAO.

2. **Определите базовый класс `BaseDAO`**:
   - Используйте `Generic[T]` для указания, что класс является generic-типом, где `T` - это тип модели, с которой работает DAO.
   - Укажите атрибут `model: type[T]`, который будет хранить тип модели.

3. **Реализуйте методы класса `BaseDAO`**:
   - `find_one_or_none_by_id`: Функция выполняет поиск записи в базе данных по её ID.
     - Логирует начало поиска записи.
     - Формирует запрос `select` для поиска записи по ID.
     - Выполняет запрос и извлекает результат.
     - Логирует успешное или неуспешное завершение поиска.
     - Обрабатывает возможные ошибки SQLAlchemy и логирует их.
   - `find_one_or_none`: Функция выполняет поиск одной записи в базе данных по заданным фильтрам.
     - Преобразует фильтры из `BaseModel` в словарь.
     - Логирует начало поиска записи.
     - Формирует запрос `select` с использованием фильтров.
     - Выполняет запрос и извлекает результат.
     - Логирует успешное или неуспешное завершение поиска.
     - Обрабатывает возможные ошибки SQLAlchemy и логирует их.
   - `find_all`: Функция выполняет поиск всех записей в базе данных по заданным фильтрам.
     - Преобразует фильтры из `BaseModel` в словарь.
     - Логирует начало поиска записей.
     - Формирует запрос `select` с использованием фильтров.
     - Выполняет запрос и извлекает результаты.
     - Логирует количество найденных записей.
     - Обрабатывает возможные ошибки SQLAlchemy и логирует их.
   - `add`: Функция добавляет одну запись в базу данных.
     - Преобразует значения из `BaseModel` в словарь.
     - Логирует начало добавления записи.
     - Создает новый экземпляр модели с использованием переданных значений.
     - Добавляет новый экземпляр в сессию.
     - Фиксирует изменения в базе данных.
     - Обрабатывает возможные ошибки SQLAlchemy, выполняет откат транзакции и логирует ошибку.
   - `add_many`: Функция добавляет несколько записей в базу данных.
     - Преобразует список экземпляров `BaseModel` в список словарей.
     - Логирует начало добавления записей.
     - Создает список новых экземпляров моделей с использованием переданных значений.
     - Добавляет все новые экземпляры в сессию.
     - Фиксирует изменения в базе данных.
     - Обрабатывает возможные ошибки SQLAlchemy, выполняет откат транзакции и логирует ошибку.
   - `update`: Функция обновляет записи в базе данных по заданным фильтрам.
     - Преобразует фильтры и значения из `BaseModel` в словари.
     - Логирует начало обновления записей.
     - Формирует запрос `sqlalchemy_update` с использованием фильтров и значений.
     - Выполняет запрос и фиксирует изменения в базе данных.
     - Обрабатывает возможные ошибки SQLAlchemy, выполняет откат транзакции и логирует ошибку.
   - `delete`: Функция удаляет записи из базы данных по заданным фильтрам.
     - Преобразует фильтры из `BaseModel` в словарь.
     - Логирует начало удаления записей.
     - Формирует запрос `sqlalchemy_delete` с использованием фильтров.
     - Выполняет запрос и фиксирует изменения в базе данных.
     - Обрабатывает возможные ошибки SQLAlchemy, выполняет откат транзакции и логирует ошибку.
   - `count`: Функция подсчитывает количество записей в базе данных по заданным фильтрам.
     - Преобразует фильтры из `BaseModel` в словарь.
     - Логирует начало подсчета записей.
     - Формирует запрос `select` с использованием `func.count` для подсчета количества записей.
     - Выполняет запрос и извлекает результат.
     - Логирует количество найденных записей.
     - Обрабатывает возможные ошибки SQLAlchemy и логирует их.
   - `paginate`: Функция выполняет пагинацию записей в базе данных по заданным фильтрам.
     - Преобразует фильтры из `BaseModel` в словарь.
     - Логирует начало пагинации записей.
     - Формирует запрос `select` с использованием фильтров, `offset` и `limit` для пагинации.
     - Выполняет запрос и извлекает результаты.
     - Логирует количество найденных записей на странице.
     - Обрабатывает возможные ошибки SQLAlchemy и логирует их.
   - `find_by_ids`: Функция выполняет поиск нескольких записей в базе данных по списку ID.
     - Логирует начало поиска записей.
     - Формирует запрос `select` с использованием фильтра `in_` для поиска по списку ID.
     - Выполняет запрос и извлекает результаты.
     - Логирует количество найденных записей.
     - Обрабатывает возможные ошибки SQLAlchemy и логирует их.
   - `upsert`: Функция создает новую запись или обновляет существующую запись на основе уникальных полей.
     - Преобразует значения из `BaseModel` в словарь.
     - Создает словарь фильтров на основе уникальных полей.
     - Логирует начало операции upsert.
     - Пытается найти существующую запись с использованием `find_one_or_none`.
     - Если запись существует, обновляет её атрибуты и фиксирует изменения.
     - Если запись не существует, создает новую запись и добавляет её в сессию.
     - Обрабатывает возможные ошибки SQLAlchemy, выполняет откат транзакции и логирует ошибку.
   - `bulk_update`: Функция выполняет массовое обновление записей в базе данных.
     - Логирует начало массового обновления записей.
     - Итерируется по списку записей.
     - Для каждой записи формирует запрос `sqlalchemy_update` для обновления записи по ID.
     - Выполняет запрос и увеличивает счетчик обновленных записей.
     - Фиксирует изменения в базе данных.
     - Обрабатывает возможные ошибки SQLAlchemy, выполняет откат транзакции и логирует ошибку.

Пример использования
-------------------------

```python
from typing import List, Any, TypeVar, Generic
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete, func
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.database import Base

# Объявляем типовой параметр T с ограничением, что это наследник Base
T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    model: type[T]

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int, session: AsyncSession):
        # Найти запись по ID
        logger.info(f"Поиск {cls.model.__name__} с ID: {data_id}")
        try:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            if record:
                logger.info(f"Запись с ID {data_id} найдена.")
            else:
                logger.info(f"Запись с ID {data_id} не найдена.")
            return record
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске записи с ID {data_id}: {e}")
            raise

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, filters: BaseModel):
        # Найти одну запись по фильтрам
        filter_dict = filters.model_dump(exclude_unset=True)
        logger.info(f"Поиск одной записи {cls.model.__name__} по фильтрам: {filter_dict}")
        try:
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            if record:
                logger.info(f"Запись найдена по фильтрам: {filter_dict}")
            else:
                logger.info(f"Запись не найдена по фильтрам: {filter_dict}")
            return record
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске записи по фильтрам {filter_dict}: {e}")
            raise

    @classmethod
    async def find_all(cls, session: AsyncSession, filters: BaseModel | None = None):
        # Найти все записи по фильтрам
        filter_dict = filters.model_dump(exclude_unset=True) if filters else {}
        logger.info(f"Поиск всех записей {cls.model.__name__} по фильтрам: {filter_dict}")
        try:
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query)
            records = result.scalars().all()
            logger.info(f"Найдено {len(records)} записей.")
            return records
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске всех записей по фильтрам {filter_dict}: {e}")
            raise

    @classmethod
    async def add(cls, session: AsyncSession, values: BaseModel):
        # Добавить одну запись
        values_dict = values.model_dump(exclude_unset=True)
        logger.info(f"Добавление записи {cls.model.__name__} с параметрами: {values_dict}")
        new_instance = cls.model(**values_dict)
        session.add(new_instance)
        try:
            await session.flush()
            logger.info(f"Запись {cls.model.__name__} успешно добавлена.")
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при добавлении записи: {e}")
            raise e
        return new_instance

    @classmethod
    async def add_many(cls, session: AsyncSession, instances: List[BaseModel]):
        # Добавить несколько записей
        values_list = [item.model_dump(exclude_unset=True) for item in instances]
        logger.info(f"Добавление нескольких записей {cls.model.__name__}. Количество: {len(values_list)}")
        new_instances = [cls.model(**values) for values in values_list]
        session.add_all(new_instances)
        try:
            await session.flush()
            logger.info(f"Успешно добавлено {len(new_instances)} записей.")
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при добавлении нескольких записей: {e}")
            raise e
        return new_instances

    @classmethod
    async def update(cls, session: AsyncSession, filters: BaseModel, values: BaseModel):
        # Обновить записи по фильтрам
        filter_dict = filters.model_dump(exclude_unset=True)
        values_dict = values.model_dump(exclude_unset=True)
        logger.info(f"Обновление записей {cls.model.__name__} по фильтру: {filter_dict} с параметрами: {values_dict}")
        query = (
            sqlalchemy_update(cls.model)
            .where(*[getattr(cls.model, k) == v for k, v in filter_dict.items()])
            .values(**values_dict)
            .execution_options(synchronize_session="fetch")
        )
        try:
            result = await session.execute(query)
            await session.flush()
            logger.info(f"Обновлено {result.rowcount} записей.")
            return result.rowcount
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при обновлении записей: {e}")
            raise e

    @classmethod
    async def delete(cls, session: AsyncSession, filters: BaseModel):
        # Удалить записи по фильтру
        filter_dict = filters.model_dump(exclude_unset=True)
        logger.info(f"Удаление записей {cls.model.__name__} по фильтру: {filter_dict}")
        if not filter_dict:
            logger.error("Нужен хотя бы один фильтр для удаления.")
            raise ValueError("Нужен хотя бы один фильтр для удаления.")

        query = sqlalchemy_delete(cls.model).filter_by(**filter_dict)
        try:
            result = await session.execute(query)
            await session.flush()
            logger.info(f"Удалено {result.rowcount} записей.")
            return result.rowcount
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при удалении записей: {e}")
            raise e

    @classmethod
    async def count(cls, session: AsyncSession, filters: BaseModel | None = None):
        # Подсчитать количество записей
        filter_dict = filters.model_dump(exclude_unset=True) if filters else {}
        logger.info(f"Подсчет количества записей {cls.model.__name__} по фильтру: {filter_dict}")
        try:
            query = select(func.count(cls.model.id)).filter_by(**filter_dict)
            result = await session.execute(query)
            count = result.scalar()
            logger.info(f"Найдено {count} записей.")
            return count
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при подсчете записей: {e}")
            raise

    @classmethod
    async def paginate(cls, session: AsyncSession, page: int = 1, page_size: int = 10, filters: BaseModel = None):
        # Пагинация записей
        filter_dict = filters.model_dump(exclude_unset=True) if filters else {}
        logger.info(
            f"Пагинация записей {cls.model.__name__} по фильтру: {filter_dict}, страница: {page}, размер страницы: {page_size}")
        try:
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query.offset((page - 1) * page_size).limit(page_size))
            records = result.scalars().all()
            logger.info(f"Найдено {len(records)} записей на странице {page}.")
            return records
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при пагинации записей: {e}")
            raise

    @classmethod
    async def find_by_ids(cls, session: AsyncSession, ids: List[int]) -> List[Any]:
        """Найти несколько записей по списку ID"""
        logger.info(f"Поиск записей {cls.model.__name__} по списку ID: {ids}")
        try:
            query = select(cls.model).filter(cls.model.id.in_(ids))
            result = await session.execute(query)
            records = result.scalars().all()
            logger.info(f"Найдено {len(records)} записей по списку ID.")
            return records
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске записей по списку ID: {e}")
            raise

    @classmethod
    async def upsert(cls, session: AsyncSession, unique_fields: List[str], values: BaseModel):
        """Создать запись или обновить существующую"""
        values_dict = values.model_dump(exclude_unset=True)
        filter_dict = {field: values_dict[field] for field in unique_fields if field in values_dict}

        logger.info(f"Upsert для {cls.model.__name__}")
        try:
            existing = await cls.find_one_or_none(session, BaseModel.construct(**filter_dict))
            if existing:
                # Обновляем существующую запись
                for key, value in values_dict.items():
                    setattr(existing, key, value)
                await session.flush()
                logger.info(f"Обновлена существующая запись {cls.model.__name__}")
                return existing
            else:
                # Создаем новую запись
                new_instance = cls.model(**values_dict)
                session.add(new_instance)
                await session.flush()
                logger.info(f"Создана новая запись {cls.model.__name__}")
                return new_instance
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при upsert: {e}")
            raise

    @classmethod
    async def bulk_update(cls, session: AsyncSession, records: List[BaseModel]) -> int:
        """Массовое обновление записей"""
        logger.info(f"Массовое обновление записей {cls.model.__name__}")
        try:
            updated_count = 0
            for record in records:
                record_dict = record.model_dump(exclude_unset=True)
                if 'id' not in record_dict:
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
            logger.info(f"Обновлено {updated_count} записей")
            return updated_count
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при массовом обновлении: {e}")
            raise