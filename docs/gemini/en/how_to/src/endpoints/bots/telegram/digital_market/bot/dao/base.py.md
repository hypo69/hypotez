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
This code snippet defines a base class (`BaseDAO`) for working with database records in a Telegram bot project. 
It provides common functionalities for interacting with a database, including finding, creating, updating, deleting, 
and counting records.

Execution Steps
-------------------------
1. The `BaseDAO` class is initialized with a model class representing the database table. 
2. It provides various class methods:
    - `find_one_or_none_by_id`: Finds a record by its ID.
    - `find_one_or_none`: Finds a record based on given filter criteria.
    - `find_all`: Retrieves all records based on optional filters.
    - `add`: Inserts a new record into the database.
    - `add_many`: Inserts multiple records into the database.
    - `update`: Updates records matching the provided filter criteria.
    - `delete`: Deletes records matching the provided filter criteria.
    - `count`: Counts the number of records matching the optional filters.
    - `paginate`: Fetches records in pages based on filters, page number, and page size.
    - `find_by_ids`: Retrieves multiple records by their IDs.
    - `upsert`: Creates a record if it doesn't exist or updates an existing one based on unique fields.
    - `bulk_update`: Updates multiple records in bulk.

Usage Example
-------------------------

```python
from bot.dao.database import Base
from sqlalchemy.ext.asyncio import AsyncSession
from bot.dao.base import BaseDAO

class MyModel(Base):
    # Define model fields...

class MyDAO(BaseDAO[MyModel]):
    model = MyModel

async def main():
    async with AsyncSession() as session:
        # Find a record by ID
        record = await MyDAO.find_one_or_none_by_id(1, session)

        # Create a new record
        new_record = await MyDAO.add(session, MyModel(field1="value1", field2="value2"))

        # Update a record
        updated_count = await MyDAO.update(session, MyModel(field1="value1"), MyModel(field2="new_value"))

        # Delete records
        deleted_count = await MyDAO.delete(session, MyModel(field1="value1"))

        # Count records
        total_count = await MyDAO.count(session)

        # Paginate records
        records_page1 = await MyDAO.paginate(session, page=1)

        # Find by IDs
        records_by_ids = await MyDAO.find_by_ids(session, [1, 2, 3])

        # Upsert a record
        upsert_record = await MyDAO.upsert(session, ["field1"], MyModel(field1="value1", field2="value2"))

        # Bulk update records
        updated_count = await MyDAO.bulk_update(session, [MyModel(id=1, field2="new_value"), MyModel(id=2, field3="new_value")])

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".