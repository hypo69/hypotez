## Как использовать этот блок кода
=========================================================================================

### Описание
-------------------------
Данный блок кода представляет собой миграцию базы данных, которая добавляет колонку `payment_id` в таблицу `purchases`, если она еще не существует, и создает уникальный индекс для этой колонки. 

### Шаги выполнения
-------------------------
1. **Проверка наличия колонки:** Проверяется, существует ли уже колонка `payment_id` в таблице `purchases` с использованием SQL запроса `PRAGMA table_info('purchases')`.
2. **Добавление колонки (если отсутствует):** Если колонки `payment_id` нет, выполняется добавление новой колонки `payment_id` типа `sa.String()` с атрибутом `nullable=False`. Также создается уникальный индекс `uq_purchases_payment_id` для колонки `payment_id`.
3. **Обработка существующей колонки:** Если колонка `payment_id` уже существует, выводится сообщение о том, что добавление пропускается.
4. **Удаление колонки (при откатке):** Аналогично, при откатке миграции проверяется наличие колонки `payment_id`.
5. **Удаление колонки (если существует):** Если колонка `payment_id` существует, удаляется уникальный индекс `uq_purchases_payment_id`, а затем сама колонка `payment_id`.
6. **Обработка несуществующей колонки:** Если колонка `payment_id` отсутствует при откатке, выводится сообщение о том, что удаление пропускается.

### Пример использования
-------------------------

```python
# Пример использования кода в качестве миграции базы данных
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1720ca777755'
down_revision: Union[str, None] = '1b95d36c8908'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


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

```