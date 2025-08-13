"""add column pay id

Revision ID: 1720ca777755
Revises: 1b95d36c8908
Create Date: 2024-12-20 21:59:03.848433"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1720ca777755'
down_revision: Union[str, None] = '1b95d36c8908'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Check whether the column exists before adding
    conn = op.get_bind()
    result = conn.execute(
        sa.text("PRAGMA table_info('purchases')")
    )
    columns = [row[1] for row in result]  # Index 1 - this is the name of the column in the results of Pragma
    if 'payment_id' not in columns:
        op.add_column('purchases', sa.Column('payment_id', sa.String(), nullable=False))
        op.create_unique_constraint('uq_purchases_payment_id', 'purchases', ['payment_id'])
    else:
        print("Колонка 'payment_id' уже существует, Пропуск добавление")


def downgrade() -> None:
    # Check whether the column exists before removal
    conn = op.get_bind()
    result = conn.execute(
        sa.text("PRAGMA table_info('purchases')")
    )
    columns = [row[1] for row in result]  # Index 1 - this is the name of the column in the results of Pragma
    if 'payment_id' in columns:
        op.drop_constraint('uq_purchases_payment_id', 'purchases', type_='unique')
        op.drop_column('purchases', 'payment_id')
    else:
        print("Колонка 'payment_id' не существует, Пропуск удаление")
