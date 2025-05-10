# Модуль DAO для бота Telegram

## Обзор

Данный модуль предоставляет набор классов для взаимодействия с базой данных бота Telegram. 
Он реализует абстрактный класс `BaseDAO` и конкретные реализации DAO для различных сущностей, таких как пользователи (`UserDAO`), покупки (`PurchaseDao`), категории (`CategoryDao`) и товары (`ProductDao`).

## Подробнее

Этот модуль используется для выполнения операций CRUD (создание, чтение, обновление, удаление) над сущностями, хранящимися в базе данных. Он обеспечивает абстракцию над SQL-запросами, упрощая работу с базой данных для бота.

## Классы

### `BaseDAO`

**Описание**: Базовый класс для всех DAO, предоставляющий общие методы для работы с сущностями.

**Атрибуты**:

- `model`: Модель SQLAlchemy, с которой работает DAO.

**Методы**:

- `get_by_id(session: AsyncSession, id: int) -> Optional[Model]`: Извлекает запись по ее ID.
- `get_all(session: AsyncSession) -> List[Model]`: Возвращает список всех записей.
- `create(session: AsyncSession, **kwargs) -> Model`: Создает новую запись.
- `update(session: AsyncSession, id: int, **kwargs) -> Model`: Обновляет существующую запись.
- `delete(session: AsyncSession, id: int) -> None`: Удаляет запись по ее ID.

### `UserDAO`

**Описание**: Класс для работы с сущностью `User`.

**Наследует**: `BaseDAO`

**Методы**:

- `get_purchase_statistics(session: AsyncSession, telegram_id: int) -> Optional[Dict[str, int]]`: Получает статистику покупок пользователя по его `telegram_id`.
- `get_purchased_products(session: AsyncSession, telegram_id: int) -> Optional[List[Purchase]]`: Возвращает список покупок пользователя с информацией о товарах.
- `get_statistics(session: AsyncSession) -> Dict[str, int]`: Получает общую статистику пользователей.

### `PurchaseDao`

**Описание**: Класс для работы с сущностью `Purchase`.

**Наследует**: `BaseDAO`

**Методы**:

- `get_payment_stats(session: AsyncSession) -> str`: Возвращает отформатированную строку со статистикой платежей.
- `get_full_summ(session: AsyncSession) -> int`: Возвращает общую сумму покупок.
- `get_next_id(session: AsyncSession) -> int`: Возвращает следующий свободный ID для новой покупки.

### `CategoryDao`

**Описание**: Класс для работы с сущностью `Category`.

**Наследует**: `BaseDAO`

### `ProductDao`

**Описание**: Класс для работы с сущностью `Product`.

**Наследует**: `BaseDAO`


## Примеры

### Пример использования `UserDAO`

```python
from bot.dao.dao import UserDAO

async def get_user_stats(telegram_id: int):
    async with session_maker() as session:  # Предполагается, что `session_maker` уже определен 
        user_dao = UserDAO(session)
        stats = await user_dao.get_purchase_statistics(telegram_id)
        if stats is not None:
            print(f"Статистика покупок пользователя {telegram_id}: {stats}")
        else:
            print(f"Пользователь с ID {telegram_id} не найден")
```

### Пример использования `PurchaseDao`

```python
from bot.dao.dao import PurchaseDao

async def get_payment_summary():
    async with session_maker() as session:
        purchase_dao = PurchaseDao(session)
        stats = await purchase_dao.get_payment_stats()
        print(stats)