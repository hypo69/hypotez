### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код представляет собой скрипт миграции базы данных, используемый инструментом Alembic. Он определяет, какие изменения следует внести в схему базы данных при обновлении (upgrade) и как откатить эти изменения при необходимости (downgrade). В данном случае, скрипт создает четыре таблицы: `categories`, `users`, `products` и `purchases`, а также определяет их структуру, типы данных и связи между ними.

Шаги выполнения
-------------------------
1. **Определение метаданных миграции**:
   - В начале скрипта определяются метаданные миграции, такие как `revision`, `down_revision`, `branch_labels` и `depends_on`. Эти переменные используются Alembic для отслеживания и управления миграциями.

2. **Функция `upgrade()`**:
   - Функция `upgrade()` содержит последовательность команд, которые выполняются при обновлении базы данных до этой версии.
   - `op.create_table('categories', ...)`: Создает таблицу `categories` со столбцами `category_name`, `id`, `created_at` и `updated_at`. Определяет `id` как первичный ключ.
   - `op.create_table('users', ...)`: Создает таблицу `users` со столбцами `telegram_id`, `username`, `first_name`, `last_name`, `id`, `created_at` и `updated_at`. Определяет `id` как первичный ключ и `telegram_id` как уникальное ограничение.
   - `op.create_table('products', ...)`: Создает таблицу `products` со столбцами `name`, `description`, `price`, `file_id`, `category_id`, `id`, `created_at` и `updated_at`. Определяет `id` как первичный ключ и внешний ключ `category_id`, связанный с таблицей `categories`.
   - `op.create_table('purchases', ...)`: Создает таблицу `purchases` со столбцами `user_id`, `product_id`, `price`, `id`, `created_at` и `updated_at`. Определяет `id` как первичный ключ и внешние ключи `user_id` и `product_id`, связанные с таблицами `users` и `products` соответственно.

3. **Функция `downgrade()`**:
   - Функция `downgrade()` содержит команды для отката изменений, внесенных функцией `upgrade()`.
   - `op.drop_table('purchases')`: Удаляет таблицу `purchases`.
   - `op.drop_table('products')`: Удаляет таблицу `products`.
   - `op.drop_table('users')`: Удаляет таблицу `users`.
   - `op.drop_table('categories')`: Удаляет таблицу `categories`.

Пример использования
-------------------------

```python
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    # Создание таблицы categories
    op.create_table(
        'categories',
        sa.Column('category_name', sa.Text(), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    # Удаление таблицы categories
    op.drop_table('categories')