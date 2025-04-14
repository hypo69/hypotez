# Модуль обновления таблицы покупок

## Обзор

Этот модуль содержит функции для обновления таблицы `purchases` в базе данных с использованием Alembic. Он добавляет столбец `payment_type` и создает уникальное ограничение для столбца `payment_id`.

## Подробней

Модуль предназначен для управления изменениями схемы базы данных. Он использует Alembic для автоматического внесения изменений в схему базы данных, таких как добавление столбцов и ограничений. Это позволяет поддерживать базу данных в актуальном состоянии с минимальным ручным вмешательством.

## Функции

### `upgrade`

```python
def upgrade() -> None:
    """
    Обновляет схему базы данных, добавляя столбец `payment_type` в таблицу `purchases` и создавая уникальное ограничение для столбца `payment_id`.

    Args:
        None

    Returns:
        None

    Raises:
        Нет

    Как работает функция:
    - Использует `op.add_column` для добавления столбца `payment_type` типа `String` в таблицу `purchases`. `nullable=False` означает, что столбец не может содержать `NULL` значения.
    - Использует `op.create_unique_constraint` для создания уникального ограничения для столбца `payment_id` в таблице `purchases`. Это гарантирует, что каждое значение в `payment_id` будет уникальным.
    """
    op.add_column('purchases', sa.Column('payment_type', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'purchases', ['payment_id'])
    # ### end Alembic commands ###
```

### `downgrade`

```python
def downgrade() -> None:
    """
    Откатывает изменения, внесенные функцией `upgrade`, удаляя уникальное ограничение и столбец `payment_type` из таблицы `purchases`.

    Args:
        None

    Returns:
        None

    Raises:
        Нет

    Как работает функция:
    - Использует `op.drop_constraint` для удаления уникального ограничения из таблицы `purchases`.
    - Использует `op.drop_column` для удаления столбца `payment_type` из таблицы `purchases`.
    """
    op.drop_constraint(None, 'purchases', type_='unique')
    op.drop_column('purchases', 'payment_type')
    # ### end Alembic commands ###