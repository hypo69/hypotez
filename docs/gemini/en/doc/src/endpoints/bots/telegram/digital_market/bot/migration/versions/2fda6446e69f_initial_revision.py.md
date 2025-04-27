# Модуль `hypotez/src/endpoints/bots/telegram/digital_market/bot/migration/versions/2fda6446e69f_initial_revision.py`

## Обзор

Этот модуль представляет собой миграцию базы данных для телеграм-бота цифрового рынка. В нем создаются таблицы для хранения категорий, пользователей, товаров и покупок.

## Детали

Модуль `2fda6446e69f_initial_revision.py` содержит функции `upgrade()` и `downgrade()`. 

-  `upgrade()`  создает таблицы  `categories`,  `users`,  `products`  и  `purchases`  в базе данных. 
-  `downgrade()`  удаляет эти таблицы.

## Функции

### `upgrade()`

**Описание**: Эта функция создает таблицы базы данных, необходимые для телеграм-бота цифрового рынка.

**Параметры**:

- Нет.

**Возвращает**:

- Нет.

**Пример**:

```python
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    op.create_table('categories',
    sa.Column('category_name', sa.Text(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('telegram_id', sa.BigInteger(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('telegram_id')
    )
    op.create_table('products',
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('file_id', sa.Text(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('purchases',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

```

**Как работает функция**:

-  `upgrade()`  использует библиотеку  `alembic`  для создания таблиц в базе данных.
-  Каждая таблица создается с помощью  `op.create_table()`. 
-  `sa.Column()`  определяет столбцы таблицы, включая тип данных,  `nullable`,  и ограничения.
-  `sa.PrimaryKeyConstraint()`  устанавливает первичный ключ для таблицы. 
-  `sa.UniqueConstraint()`  устанавливает ограничение уникальности для столбца  `telegram_id`  в таблице  `users`. 
-  `sa.ForeignKeyConstraint()`  устанавливает внешние ключи для таблиц  `products`  и  `purchases`,  ссылаясь на соответствующие первичные ключи в других таблицах.

### `downgrade()`

**Описание**: Эта функция удаляет таблицы базы данных, созданные функцией `upgrade()`.

**Параметры**:

- Нет.

**Возвращает**:

- Нет.

**Пример**:

```python
def downgrade() -> None:
    op.drop_table('purchases')
    op.drop_table('products')
    op.drop_table('users')
    op.drop_table('categories')
```

**Как работает функция**:

-  `downgrade()`  использует `alembic`  для удаления таблиц.
-  `op.drop_table()`  удаляет каждую таблицу, созданную  `upgrade()`.

## Таблицы

### `categories`

-  **Описание**: Эта таблица хранит информацию о категориях товаров, доступных в цифровом рынке.
-  **Столбцы**:
    -  `category_name`  (sa.Text(), nullable=False): Имя категории.
    -  `id`  (sa.Integer(), autoincrement=True, nullable=False): Идентификатор категории.
    -  `created_at`  (sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False): Дата и время создания записи.
    -  `updated_at`  (sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False): Дата и время последнего обновления записи.

### `users`

-  **Описание**: Эта таблица хранит информацию о пользователях телеграм-бота.
-  **Столбцы**:
    -  `telegram_id`  (sa.BigInteger(), nullable=False): ID пользователя в Telegram.
    -  `username`  (sa.String(), nullable=True): Имя пользователя в Telegram.
    -  `first_name`  (sa.String(), nullable=True): Имя пользователя.
    -  `last_name`  (sa.String(), nullable=True): Фамилия пользователя.
    -  `id`  (sa.Integer(), autoincrement=True, nullable=False): ID пользователя в базе данных.
    -  `created_at`  (sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False): Дата и время создания записи.
    -  `updated_at`  (sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False): Дата и время последнего обновления записи.

### `products`

-  **Описание**: Эта таблица хранит информацию о товарах, доступных в цифровом рынке.
-  **Столбцы**:
    -  `name`  (sa.Text(), nullable=False): Название товара.
    -  `description`  (sa.Text(), nullable=False): Описание товара.
    -  `price`  (sa.Integer(), nullable=False): Цена товара.
    -  `file_id`  (sa.Text(), nullable=True): ID файла, связанного с товаром (например, файл с описанием).
    -  `category_id`  (sa.Integer(), nullable=False): ID категории, к которой принадлежит товар.
    -  `id`  (sa.Integer(), autoincrement=True, nullable=False): ID товара в базе данных.
    -  `created_at`  (sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False): Дата и время создания записи.
    -  `updated_at`  (sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False): Дата и время последнего обновления записи.

### `purchases`

-  **Описание**: Эта таблица хранит информацию о покупках, совершенных пользователями в цифровом рынке.
-  **Столбцы**:
    -  `user_id`  (sa.Integer(), nullable=False): ID пользователя, совершившего покупку.
    -  `product_id`  (sa.Integer(), nullable=False): ID купленного товара.
    -  `price`  (sa.Integer(), nullable=False): Цена товара.
    -  `id`  (sa.Integer(), autoincrement=True, nullable=False): ID покупки в базе данных.
    -  `created_at`  (sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False): Дата и время создания записи.
    -  `updated_at`  (sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False): Дата и время последнего обновления записи.

## Пример

```python
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    op.create_table('categories',
    sa.Column('category_name', sa.Text(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('telegram_id', sa.BigInteger(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('telegram_id')
    )
    op.create_table('products',
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('file_id', sa.Text(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('purchases',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
```