# Initial revision

Начальная редакция

Revision ID: 2fda6446e69f
Revises: 47f559ec82bb
Create Date: 2024-12-20 10:59:08.896379

```rst
.. module:: src.endpoints.bots.telegram.digital_market.bot.migration.versions.2fda6446e69f_initial_revision
```

## Обзор

Модуль представляет собой скрипт начальной миграции Alembic, создающий таблицы `users`, `categories`, `products` и `purchases`.

## Подробней

Модуль содержит функции `upgrade` и `downgrade` для выполнения и отката миграции.

## Переменные

*   `revision` (str): ID ревизии (значение: `'2fda6446e69f'`).
*   `down_revision` (str | None): ID предыдущей ревизии (значение: `'47f559ec82bb'`).
*   `branch_labels` (str | Sequence[str] | None): Метки ветвей (значение: `None`).
*   `depends_on` (str | Sequence[str] | None): Зависимости (значение: `None`).

## Функции

### `upgrade`

```python
def upgrade() -> None:
```

**Назначение**: Выполняет миграцию (создает таблицы `users`, `categories`, `products` и `purchases`).

**Как работает функция**:

1.  Создает таблицу `categories` со следующими столбцами:

    *   `category_name` (Text, nullable=False)
    *   `id` (Integer, autoincrement=True, primary\_key=True)
    *   `created_at` (TIMESTAMP, server\_default=sa.text('(CURRENT\_TIMESTAMP)'), nullable=False)
    *   `updated_at` (TIMESTAMP, server\_default=sa.text('(CURRENT\_TIMESTAMP)'), nullable=False)
2.  Создает таблицу `users` со следующими столбцами:

    *   `telegram_id` (BigInteger, unique=True, nullable=False)
    *   `username` (String, nullable=True)
    *   `first_name` (String, nullable=True)
    *   `last_name` (String, nullable=True)
    *   `id` (Integer, autoincrement=True, primary\_key=True)
    *   `created_at` (TIMESTAMP, server\_default=sa.text('(CURRENT\_TIMESTAMP)'), nullable=False)
    *   `updated_at` (TIMESTAMP, server\_default=sa.text('(CURRENT\_TIMESTAMP)'), nullable=False)
3.  Создает таблицу `products` со следующими столбцами:

    *   `name` (Text, nullable=False)
    *   `description` (Text, nullable=False)
    *   `price` (Integer, nullable=False)
    *   `file_id` (Text, nullable=True)
    *   `category_id` (Integer, ForeignKey('categories.id'), nullable=False)
    *   `id` (Integer, autoincrement=True, primary\_key=True)
    *   `created_at` (TIMESTAMP, server\_default=sa.text('(CURRENT\_TIMESTAMP)'), nullable=False)
    *   `updated_at` (TIMESTAMP, server\_default=sa.text('(CURRENT\_TIMESTAMP)'), nullable=False)
4.  Создает таблицу `purchases` со следующими столбцами:

    *   `user_id` (Integer, ForeignKey('users.id'), nullable=False)
    *   `product_id` (Integer, ForeignKey('products.id'), nullable=False)
    *   `price` (Integer, nullable=False)
    *   `id` (Integer, autoincrement=True, primary\_key=True)
    *   `created_at` (TIMESTAMP, server\_default=sa.text('(CURRENT\_TIMESTAMP)'), nullable=False)
    *   `updated_at` (TIMESTAMP, server\_default=sa.text('(CURRENT\_TIMESTAMP)'), nullable=False)

### `downgrade`

```python
def downgrade() -> None:
```

**Назначение**: Откатывает миграцию (удаляет таблицы `purchases`, `products`, `users` и `categories`).

**Как работает функция**:

1.  Удаляет таблицы `purchases`, `products`, `users` и `categories` в обратном порядке.