# Модуль миграции базы данных: initial_revision

## Обзор

Модуль содержит Alembic migration script для начальной ревизии базы данных. Он создает таблицы `categories`, `users`, `products` и `purchases` и определяет их схемы. Также предоставляет функцию `upgrade` для применения изменений и функцию `downgrade` для отката изменений.

## Подробней

Этот файл является частью системы миграции Alembic, которая используется для управления изменениями схемы базы данных.  Он определяет операции создания таблиц и связей между ними. Скрипт предназначен для автоматического создания структуры базы данных при развертывании приложения или обновлении существующей базы данных до последней версии.

## Переменные

- `revision` (str): Идентификатор текущей ревизии миграции.
- `down_revision` (Union[str, None]): Идентификатор предыдущей ревизии миграции. Может быть `None`, если это первая миграция.
- `branch_labels` (Union[str, Sequence[str], None]): Метки ветвей для миграции.
- `depends_on` (Union[str, Sequence[str], None]): Список ревизий, от которых зависит данная миграция.

## Функции

### `upgrade`

```python
def upgrade() -> None:
    """
    Применяет изменения, определенные в данной миграции.
    Создает таблицы: 'categories', 'users', 'products', 'purchases'.

    Args:
        None

    Returns:
        None

    """
    # ### commands auto generated by Alembic - please adjust! ###
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
    # ### end Alembic commands ###

### `downgrade`

```python
def downgrade() -> None:
    """
    Отменяет изменения, внесенные данной миграцией.
    Удаляет таблицы: 'purchases', 'products', 'users', 'categories'.

    Args:
        None

    Returns:
        None

    """
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('purchases')
    op.drop_table('products')
    op.drop_table('users')
    op.drop_table('categories')
    # ### end Alembic commands ###