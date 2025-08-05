**Instructions for Generating Code Documentation**

How to Use This Code Block
=========================================================================================

Description
-------------------------
This Alembic migration script adds a new column `payment_id` to the `purchases` table in a SQLite database. It ensures uniqueness for the `payment_id` column. If the column already exists, it skips the addition.

Execution Steps
-------------------------
1. **Upgrade:**
    - Checks if the `payment_id` column exists in the `purchases` table.
    - If the column doesn't exist, it adds the `payment_id` column with the `sa.String()` data type and sets it as non-nullable.
    - It creates a unique constraint on the `payment_id` column to ensure that each `payment_id` is unique.
    - If the column already exists, it prints a message indicating that the column already exists.

2. **Downgrade:**
    - Checks if the `payment_id` column exists in the `purchases` table.
    - If the column exists, it drops the unique constraint `uq_purchases_payment_id` and then drops the `payment_id` column.
    - If the column doesn't exist, it prints a message indicating that the column doesn't exist.

Usage Example
-------------------------

```python
from alembic import op
import sqlalchemy as sa

# Example usage:
op.add_column(
    'purchases',
    sa.Column('payment_id', sa.String(), nullable=False),
)
op.create_unique_constraint('uq_purchases_payment_id', 'purchases', ['payment_id'])
```

```python
# Example of how to use the downgrade function:
op.drop_constraint('uq_purchases_payment_id', 'purchases', type_='unique')
op.drop_column('purchases', 'payment_id')
```

```python
# Example of how to use the upgrade function:
conn = op.get_bind()
result = conn.execute(sa.text("PRAGMA table_info('purchases')"))
columns = [row[1] for row in result]
if 'payment_id' not in columns:
    op.add_column('purchases', sa.Column('payment_id', sa.String(), nullable=False))
    op.create_unique_constraint('uq_purchases_payment_id', 'purchases', ['payment_id'])
```