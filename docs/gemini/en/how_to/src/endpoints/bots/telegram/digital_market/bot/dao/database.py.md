**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use This Code Block
=========================================================================================

Description
-------------------------
This code block sets up a basic SQLAlchemy model structure for creating an asynchronous database connection and defining a base model class.

Execution Steps
-------------------------
1. **Imports**:
    - Imports necessary modules from `datetime`, `bot.config`, and `sqlalchemy` for database connection and model definition.
2. **Create Database Engine**:
    - Creates an asynchronous database engine using `create_async_engine` based on the `database_url` specified in the `bot.config` module.
3. **Create Asynchronous Session Maker**:
    - Creates an asynchronous session maker using `async_sessionmaker` associated with the engine for creating database sessions.
4. **Define Base Model Class**:
    - Creates a base model class `Base` that inherits from `AsyncAttrs` and `DeclarativeBase`, providing the foundation for defining specific database models.
5. **Define Common Model Attributes**:
    - Adds common attributes to the `Base` class:
        - `id`: Primary key with auto-incrementing integer value.
        - `created_at`: Timestamp automatically set when the record is created.
        - `updated_at`: Timestamp automatically set when the record is created and updated.
6. **Define Table Name Convention**:
    - Implements `__tablename__` class method to automatically generate table names based on the model class name in lowercase with an "s" suffix.
7. **Define `to_dict` Method**:
    - Adds `to_dict` method to convert model instances into dictionaries, making it easy to serialize data.

Usage Example
-------------------------

```python
from bot.dao.database import Base, engine, async_session_maker
from sqlalchemy import Column, String

class User(Base):
    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Create database tables

    async with async_session_maker() as session:
        new_user = User(name="Alice", email="alice@example.com")
        session.add(new_user)
        await session.commit()

        users = await session.execute(select(User))
        for user in users:
            print(user.to_dict())

if __name__ == "__main__":
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".