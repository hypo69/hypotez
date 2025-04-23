### **Как использовать этот блок кода**

=========================================================================================

Описание
-------------------------
Этот блок кода представляет собой скрипт миграции базы данных, используемый Alembic для внесения изменений в схему базы данных. В частности, он добавляет столбец `payment_type` в таблицу `purchases` и создает уникальное ограничение для столбца `payment_id`.

Шаги выполнения
-------------------------
1. **Добавление столбца `payment_type`**: Функция `upgrade` добавляет новый столбец с именем `payment_type` в таблицу `purchases`. Тип данных столбца — `String`, и установлено ограничение `nullable=False`, что означает, что столбец не может содержать `NULL` значения.
2. **Создание уникального ограничения**: Функция `upgrade` создает уникальное ограничение для столбца `payment_id` в таблице `purchases`. Это гарантирует, что каждое значение в столбце `payment_id` будет уникальным.
3. **Удаление столбца `payment_type`**: Функция `downgrade` удаляет столбец `payment_type` из таблицы `purchases`.
4. **Удаление уникального ограничения**: Функция `downgrade` удаляет уникальное ограничение, созданное для столбца `payment_id` в таблице `purchases`.

Пример использования
-------------------------

```python
from alembic import op
import sqlalchemy as sa


def upgrade() -> None:
    # Добавление столбца 'payment_type' в таблицу 'purchases'
    op.add_column('purchases', sa.Column('payment_type', sa.String(), nullable=False))
    # Создание уникального ограничения для столбца 'payment_id'
    op.create_unique_constraint(None, 'purchases', ['payment_id'])


def downgrade() -> None:
    # Удаление уникального ограничения для столбца 'payment_id'
    op.drop_constraint(None, 'purchases', type_='unique')
    # Удаление столбца 'payment_type' из таблицы 'purchases'
    op.drop_column('purchases', 'payment_type')
```