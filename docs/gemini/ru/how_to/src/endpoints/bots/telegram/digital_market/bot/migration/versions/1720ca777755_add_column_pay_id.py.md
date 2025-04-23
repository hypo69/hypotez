### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код представляет собой миграцию базы данных, использующую Alembic. Он добавляет столбец `payment_id` в таблицу `purchases`, если он еще не существует, и удаляет его при откате миграции, если он существует.

Шаги выполнения
-------------------------
1. **Подключение к базе данных**: Функция `op.get_bind()` получает соединение с базой данных, которое будет использоваться для выполнения операций.
2. **Проверка существования столбца**:
   - Выполняется запрос `PRAGMA table_info('purchases')`, чтобы получить информацию о структуре таблицы `purchases`.
   - Извлекаются имена всех столбцов из результата запроса.
   - Проверяется, существует ли столбец `payment_id` в списке столбцов.
3. **Добавление столбца (upgrade)**:
   - Если столбца `payment_id` не существует, он добавляется в таблицу `purchases` с использованием `op.add_column()`.
   - Устанавливается ограничение уникальности для столбца `payment_id` с использованием `op.create_unique_constraint()`.
   - Если столбец `payment_id` уже существует, выводится сообщение в консоль, и добавление пропускается.
4. **Удаление столбца (downgrade)**:
   - Если столбец `payment_id` существует, ограничение уникальности для этого столбца удаляется с использованием `op.drop_constraint()`.
   - Затем столбец `payment_id` удаляется из таблицы `purchases` с использованием `op.drop_column()`.
   - Если столбца `payment_id` не существует, выводится сообщение в консоль, и удаление пропускается.

Пример использования
-------------------------

```python
from alembic import op
import sqlalchemy as sa


def upgrade() -> None:
    # Проверяем, существует ли колонка перед добавлением
    conn = op.get_bind()
    result = conn.execute(
        sa.text("PRAGMA table_info('purchases')")
    )
    columns = [row[1] for row in result]  # Индекс 1 — это имя колонки в результатах PRAGMA
    if 'payment_id' not in columns:
        op.add_column('purchases', sa.Column('payment_id', sa.String(), nullable=False))
        op.create_unique_constraint('uq_purchases_payment_id', 'purchases', ['payment_id'])
    else:
        print("Колонка 'payment_id' уже существует, пропускаем добавление")


def downgrade() -> None:
    # Проверяем, существует ли колонка перед удалением
    conn = op.get_bind()
    result = conn.execute(
        sa.text("PRAGMA table_info('purchases')")
    )
    columns = [row[1] for row in result]  # Индекс 1 — это имя колонки в результатах PRAGMA
    if 'payment_id' in columns:
        op.drop_constraint('uq_purchases_payment_id', 'purchases', type_='unique')
        op.drop_column('purchases', 'payment_id')
    else:
        print("Колонка 'payment_id' не существует, пропускаем удаление")