Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода определяет базовую настройку для работы с базой данных, используя SQLAlchemy. Он включает создание асинхронного движка базы данных, определение базового класса для моделей (таблиц) базы данных, а также настройку автоматического обновления временных меток (`created_at` и `updated_at`).

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются модули `datetime`, `func`, `TIMESTAMP`, `Integer` из `sqlalchemy`, а также классы для работы с асинхронной базой данных из `sqlalchemy.orm` и `sqlalchemy.ext.asyncio`.
2. **Настройка подключения к базе данных**:
   - `database_url` извлекается из `bot.config` и используется для создания асинхронного движка базы данных с помощью `create_async_engine`.
   - Создается фабрика сессий `async_session_maker` для работы с базой данных в асинхронном режиме.
3. **Определение базового класса Base**:
   - Класс `Base` наследуется от `AsyncAttrs` и `DeclarativeBase` и служит базовым классом для всех моделей базы данных.
   - Определяются общие поля для всех таблиц: `id` (первичный ключ, автоинкремент), `created_at` (дата создания записи) и `updated_at` (дата последнего обновления записи).
   - Поля `created_at` и `updated_at` автоматически заполняются текущим временем при создании и обновлении записи соответственно.
4. **Метод to_dict**:
   -  `to_dict` преобразовывает объект модели в словарь, где ключами являются имена столбцов, а значениями - соответствующие значения атрибутов объекта.
5. **Автоматическое определение имени таблицы**:
   - `__tablename__` автоматически генерирует имя таблицы на основе имени класса модели, приводя его к нижнему регистру и добавляя суффикс 's'.

Пример использования
-------------------------

```python
from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Identity

from bot.dao.database import Base, async_session_maker


class Пользователь(Base):
    """
    Пример класса модели Пользователь, который наследуется от базового класса Base.
    """
    __tablename__ = "users"  # Явное задание имени таблицы

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    username: Mapped[String] = mapped_column(String(32), unique=True)
    email_address: Mapped[String] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.username!r}, email={self.email_address})"


async def main():
    """
    Пример использования модели и создания сессии для работы с базой данных.
    """
    async with async_session_maker() as session:
        # Создание нового пользователя
        new_user = Пользователь(username="example_user", email_address="example@example.com")
        session.add(new_user)
        await session.commit()

        # Запрос пользователя из базы данных
        retrieved_user = await session.get(Пользователь, new_user.id)
        if retrieved_user:
            print(retrieved_user.to_dict())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())