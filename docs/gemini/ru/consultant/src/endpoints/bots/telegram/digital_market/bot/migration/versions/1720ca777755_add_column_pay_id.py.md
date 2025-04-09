### **Анализ кода модуля `1720ca777755_add_column_pay_id.py`**

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код содержит проверки существования столбца перед добавлением или удалением, что предотвращает ошибки.
    - Используются `alembic` для управления миграциями базы данных и `sqlalchemy` для определения типов данных.
- **Минусы**:
    - Отсутствует логирование действий, что затрудняет отслеживание изменений в базе данных.
    - Используется `print` для вывода сообщений, что не соответствует стандартам логирования проекта.
    - Нет документации функций.

**Рекомендации по улучшению:**

1.  **Добавить логирование**:
    - Заменить `print` на `logger.info` или `logger.warning` для логирования сообщений о добавлении или удалении столбца.
    - Логировать ошибки, которые могут возникнуть при выполнении миграции.

2.  **Добавить документацию**:
    - Добавить docstring к функциям `upgrade` и `downgrade` для описания их назначения и параметров.

3.  **Использовать константы**:
    - Заменить строковые литералы `'purchases'` и `'payment_id'` на константы для повышения читаемости и предотвращения опечаток.

4. **Улучшить обработку ошибок**:
    - В случае возникновения ошибки при выполнении `op.add_column` или `op.drop_column`, необходимо логировать ошибку и, возможно, вызывать исключение, чтобы остановить процесс миграции.

**Оптимизированный код:**

```python
"""add column pay id

Revision ID: 1720ca777755
Revises: 1b95d36c8908
Create Date: 2024-12-20 21:59:03.848433

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from src.logger import logger  # Добавлен импорт logger


# revision identifiers, used by Alembic.
revision: str = '1720ca777755'
down_revision: Union[str, None] = '1b95d36c8908'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAME: str = 'purchases'  # Добавлена константа для имени таблицы
COLUMN_NAME: str = 'payment_id'  # Добавлена константа для имени столбца


def upgrade() -> None:
    """
    Добавляет столбец 'payment_id' в таблицу 'purchases', если он не существует.
    Создает уникальный constraint для нового столбца.
    """
    try:
        conn = op.get_bind()
        result = conn.execute(
            sa.text(f"PRAGMA table_info('{TABLE_NAME}')")
        )
        columns = [row[1] for row in result]  # Индекс 1 — это имя колонки в результатах PRAGMA
        if COLUMN_NAME not in columns:
            op.add_column(TABLE_NAME, sa.Column(COLUMN_NAME, sa.String(), nullable=False))
            op.create_unique_constraint(f'uq_{TABLE_NAME}_{COLUMN_NAME}', TABLE_NAME, [COLUMN_NAME])
            logger.info(f"Столбец '{COLUMN_NAME}' успешно добавлен в таблицу '{TABLE_NAME}'.")
        else:
            logger.warning(f"Столбец '{COLUMN_NAME}' уже существует в таблице '{TABLE_NAME}', пропускаем добавление.")
    except Exception as ex:
        logger.error(f"Ошибка при добавлении столбца '{COLUMN_NAME}' в таблицу '{TABLE_NAME}'.", ex, exc_info=True)


def downgrade() -> None:
    """
    Удаляет столбец 'payment_id' из таблицы 'purchases', если он существует.
    Удаляет уникальный constraint для этого столбца.
    """
    try:
        conn = op.get_bind()
        result = conn.execute(
            sa.text(f"PRAGMA table_info('{TABLE_NAME}')")
        )
        columns = [row[1] for row in result]  # Индекс 1 — это имя колонки в результатах PRAGMA
        if COLUMN_NAME in columns:
            op.drop_constraint(f'uq_{TABLE_NAME}_{COLUMN_NAME}', TABLE_NAME, type_='unique')
            op.drop_column(TABLE_NAME, COLUMN_NAME)
            logger.info(f"Столбец '{COLUMN_NAME}' успешно удален из таблицы '{TABLE_NAME}'.")
        else:
            logger.warning(f"Столбец '{COLUMN_NAME}' не существует в таблице '{TABLE_NAME}', пропускаем удаление.")
    except Exception as ex:
        logger.error(f"Ошибка при удалении столбца '{COLUMN_NAME}' из таблицы '{TABLE_NAME}'.", ex, exc_info=True)