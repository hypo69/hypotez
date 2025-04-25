## Как использовать класс BaseDAO
=========================================================================================

Описание
-------------------------
Класс `BaseDAO` предоставляет набор базовых операций для взаимодействия с базой данных через SQLAlchemy. Он использует генерические типы для обеспечения универсальности и поддерживает такие операции, как:
- Поиск одной записи по ID
- Поиск одной записи по заданным фильтрам
- Поиск всех записей по заданным фильтрам
- Добавление новой записи
- Добавление нескольких записей
- Обновление записей по заданным фильтрам
- Удаление записей по заданным фильтрам
- Подсчет количества записей
- Пагинация записей
- Поиск нескольких записей по списку ID
- Upsert (создание или обновление записи)
- Массовое обновление записей

Шаги выполнения
-------------------------
1. **Создайте класс наследник BaseDAO**  и определите атрибут `model`, указывающий на модель SQLAlchemy, с которой будет работать DAO. 
2. **Используйте методы класса BaseDAO** для взаимодействия с базой данных. 
3. **Передайте сессию SQLAlchemy** (`session: AsyncSession`) в качестве первого аргумента каждого метода.
4. **Передайте фильтры** (`filters: BaseModel`) для всех операций, которые требуют фильтрации.
5. **Передайте данные** (`values: BaseModel`) для добавления, обновления или upsert.
6. **Используйте методы `find_one_or_none_by_id`, `find_one_or_none`, `find_all`, `add`, `add_many`, `update`, `delete`, `count`, `paginate`, `find_by_ids`, `upsert`, `bulk_update`** для соответствующих операций.

Пример использования
-------------------------

```python
from bot.dao.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from bot.dao.base import BaseDAO

engine = create_async_engine("postgresql://user:password@host:port/database")
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)

class UserDAO(BaseDAO[User]):
    model = User

async def main():
    async with async_session() as session:
        # Добавление новой записи
        new_user = await UserDAO.add(session, values={'username': 'JohnDoe'})
        print(f'Новый пользователь добавлен: {new_user}')

        # Поиск пользователя по ID
        user = await UserDAO.find_one_or_none_by_id(session, data_id=new_user.id)
        if user:
            print(f'Найден пользователь: {user}')

        # Обновление имени пользователя
        await UserDAO.update(session, filters={'id': new_user.id}, values={'username': 'JaneDoe'})

        # Удаление пользователя
        await UserDAO.delete(session, filters={'id': new_user.id})

        # Подсчет количества пользователей
        count = await UserDAO.count(session)
        print(f'Количество пользователей: {count}')

        # Пагинация пользователей
        users = await UserDAO.paginate(session, page=1, page_size=10)
        print(f'Пользователи на странице 1: {users}')

        # Upsert (создание или обновление) записи
        result = await UserDAO.upsert(session, unique_fields=['id'], values={'id': 1, 'username': 'TestUser'})
        print(f'Upsert result: {result}')

        # Массовое обновление записей
        records = [
            {'id': 1, 'username': 'UpdatedUser1'},
            {'id': 2, 'username': 'UpdatedUser2'},
        ]
        updated_count = await UserDAO.bulk_update(session, records)
        print(f'Обновлено записей: {updated_count}')

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

**Важно:**
- Класс `BaseDAO` предоставляет базовые операции, которые могут быть расширены для более специфичных задач.
- Используйте `logger.info` для вывода информационных сообщений о выполняемых операциях.
- Используйте `logger.error` для вывода ошибок, возникающих во время взаимодействия с базой данных.
- Всегда обрабатывайте исключения `SQLAlchemyError`, чтобы обеспечить устойчивость к ошибкам.
- Передайте соответствующие аргументы в методы `BaseDAO` для выполнения необходимых операций.