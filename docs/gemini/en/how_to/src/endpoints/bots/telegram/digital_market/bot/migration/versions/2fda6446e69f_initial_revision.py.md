**Instructions for Generating Code Documentation**

1. **Analyze the Code**: The code block implements an Alembic migration script that creates the initial database schema for a Telegram bot.
2. **Create a Step-by-Step Guide**:
    - **Description**: This script creates tables for users, categories, products, and purchases within a database using SQLAlchemy. 
    - **Execution Steps**:
        1. The script defines the tables "categories", "users", "products", and "purchases".
        2. Each table has columns for relevant data like category name, user's Telegram ID, product details, and purchase information.
        3. The script uses "op.create_table" to create tables and specifies columns with their data types.
        4. Foreign key constraints are set up to link related tables (like products to categories and purchases to users and products).
        5. "sa.TIMESTAMP" with server_default "(CURRENT_TIMESTAMP)" ensures automatic creation and update timestamps.
    - **Usage Example**: 
        This script is automatically used by Alembic during the migration process. It is not meant to be directly executed in the codebase. To run the migration, use the `alembic upgrade head` command.
3. **Example**:

How to Use This Code Block
=========================================================================================

Description
-------------------------
This Alembic migration script creates the initial database schema for a Telegram bot. The script defines tables for users, categories, products, and purchases. It sets up relationships between tables through foreign key constraints and automatically adds timestamps for creation and update events. 

Execution Steps
-------------------------
1. Define tables: The script starts by defining the `categories`, `users`, `products`, and `purchases` tables using SQLAlchemy.
2. Define columns: Each table is assigned columns with specific data types, including `sa.Text`, `sa.Integer`, and `sa.TIMESTAMP`.
3. Create tables: The `op.create_table` function is used to create each table in the database. 
4. Set up foreign key constraints: Relationships between tables are established with `sa.ForeignKeyConstraint` to link related data, ensuring data integrity.
5. Auto-generate timestamps: `sa.TIMESTAMP` with server_default `sa.text("(CURRENT_TIMESTAMP)")` automatically adds creation and update timestamps for each record.

Usage Example
-------------------------

```python
# This is a sample usage example of the migration script:
# Create a new migration:
#   alembic revision --autogenerate -m "Initial database schema"
# Apply the migration:
#   alembic upgrade head
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".