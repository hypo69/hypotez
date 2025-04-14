### **Анализ кода модуля `add_column_pay_id.py`**

## \file /hypotez/src/endpoints/bots/telegram/digital_market/bot/migration/versions/1720ca777755_add_column_pay_id.py

Модуль содержит функции для миграции базы данных, добавляющие и удаляющие колонку `payment_id` в таблице `purchases`.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код выполняет проверку существования колонки перед добавлением и удалением, что предотвращает ошибки.
  - Используется `alembic` для управления миграциями базы данных.
- **Минусы**:
  - Отсутствует обработка исключений.
  - Используется `print` вместо `logger` для вывода информации.
  - Не хватает docstring для функций `upgrade` и `downgrade`.

**Рекомендации по улучшению:**

1.  **Добавить docstring**: Добавить docstring для функций `upgrade` и `downgrade` с описанием их назначения, аргументов и возвращаемых значений.
2.  **Использовать логирование**: Заменить `print` на `logger` для логирования информации о процессе миграции.
3.  **Обработка исключений**: Добавить блоки `try...except` для обработки возможных исключений при работе с базой данных.

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
from src.logger import logger # Импорт модуля logger

# revision identifiers, used by Alembic.
revision: str = '1720ca777755'
down_revision: Union[str, None] = '1b95d36c8908'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Добавляет колонку 'payment_id' в таблицу 'purchases', если она не существует.
    Создает уникальный constraint 'uq_purchases_payment_id' для колонки 'payment_id'.

    Raises:
        Exception: В случае ошибки при выполнении операций с базой данных.
    """
    try:
        conn = op.get_bind()
        result = conn.execute(sa.text('PRAGMA table_info(\'purchases\')'))
        columns = [row[1] for row in result]  # Индекс 1 — это имя колонки в результатах PRAGMA

        if 'payment_id' not in columns:
            op.add_column('purchases', sa.Column('payment_id', sa.String(), nullable=False))
            op.create_unique_constraint('uq_purchases_payment_id', 'purchases', ['payment_id'])
            logger.info('Колонка \'payment_id\' успешно добавлена в таблицу \'purchases\'.') # Логирование
        else:
            logger.info('Колонка \'payment_id\' уже существует, пропускаем добавление.') # Логирование
    except Exception as ex:
        logger.error('Ошибка при добавлении колонки \'payment_id\'', ex, exc_info=True) # Логирование ошибки


def downgrade() -> None:
    """
    Удаляет колонку 'payment_id' из таблицы 'purchases', если она существует.
    Удаляет уникальный constraint 'uq_purchases_payment_id' для колонки 'payment_id'.

    Raises:
        Exception: В случае ошибки при выполнении операций с базой данных.
    """
    try:
        conn = op.get_bind()
        result = conn.execute(sa.text('PRAGMA table_info(\'purchases\')'))
        columns = [row[1] for row in result]  # Индекс 1 — это имя колонки в результатах PRAGMA

        if 'payment_id' in columns:
            op.drop_constraint('uq_purchases_payment_id', 'purchases', type_='unique')
            op.drop_column('purchases', 'payment_id')
            logger.info('Колонка \'payment_id\' успешно удалена из таблицы \'purchases\'.') # Логирование
        else:
            logger.info('Колонка \'payment_id\' не существует, пропускаем удаление.') # Логирование
    except Exception as ex:
        logger.error('Ошибка при удалении колонки \'payment_id\'', ex, exc_info=True) # Логирование ошибки