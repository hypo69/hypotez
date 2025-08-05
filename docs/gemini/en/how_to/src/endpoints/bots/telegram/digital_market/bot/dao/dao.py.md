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
[Explanation of what the code does.]

Execution Steps
-------------------------
1. [Description of the first step.]
2. [Description of the second step.]
3. [Continue as needed...]

Usage Example
-------------------------

```python
    [Code usage example]
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".
```

## How to Use the `UserDAO` Class

=========================================================================================

**Description:**

The `UserDAO` class provides methods for interacting with the `User` model in the database. It allows you to retrieve user data, purchase statistics, and information about purchased products.

**Execution Steps:**

**1. Retrieving User Purchase Statistics:**

- The `get_purchase_statistics` method retrieves the total number of purchases and the total amount spent by a user.
- It performs a database query to join the `User` and `Purchase` tables and filter by the user's `telegram_id`.
- The query returns a tuple containing the total number of purchases and the total amount spent.
- The method returns a dictionary containing the `total_purchases` and `total_amount` values.

**2. Retrieving Purchased Products:**

- The `get_purchased_products` method retrieves a list of purchases made by a user.
- It performs a database query to retrieve the `User` object with its associated purchases and products.
- The query uses the `selectinload` option to eager load the related `purchases` and `products` data.
- The method returns a list of `Purchase` objects.

**3. Getting User Statistics:**

- The `get_statistics` method retrieves overall user statistics, including the total number of users and the number of new users registered in the last day, week, and month.
- It performs a database query to count the total number of users and use `case` expressions to count new users within specific timeframes.
- The method returns a dictionary containing the statistics.

**Usage Example:**

```python
from bot.dao.dao import UserDAO
from sqlalchemy.ext.asyncio import AsyncSession

async def main():
    async with AsyncSession() as session:
        # Get purchase statistics for a user with telegram_id 123456789
        stats = await UserDAO.get_purchase_statistics(session, telegram_id=123456789)
        print(f"User purchase statistics: {stats}")

        # Get purchased products for a user with telegram_id 123456789
        purchases = await UserDAO.get_purchased_products(session, telegram_id=123456789)
        print(f"User purchased products: {purchases}")

        # Get overall user statistics
        statistics = await UserDAO.get_statistics(session)
        print(f"Overall user statistics: {statistics}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## How to Use the `PurchaseDao` Class

=========================================================================================

**Description:**

The `PurchaseDao` class provides methods for interacting with the `Purchase` model in the database. It allows you to retrieve payment statistics and the total sum of all purchases.

**Execution Steps:**

**1. Retrieving Payment Statistics:**

- The `get_payment_stats` method retrieves statistics about the total amount spent using different payment methods.
- It performs a database query to group purchases by payment type and calculate the total amount spent for each type.
- The method returns a formatted string displaying the statistics for each payment method.

**2. Retrieving the Total Sum of Purchases:**

- The `get_full_summ` method calculates the total sum of all purchases made.
- It performs a database query to sum the `price` column of all purchases.
- The method returns the total sum as an integer.

**3. Retrieving the Next Free ID:**

- The `get_next_id` method retrieves the next available ID for a new purchase record.
- It performs a database query to find the maximum ID value and increments it by 1.
- The method returns the next available ID.

**Usage Example:**

```python
from bot.dao.dao import PurchaseDao
from sqlalchemy.ext.asyncio import AsyncSession

async def main():
    async with AsyncSession() as session:
        # Get payment statistics
        payment_stats = await PurchaseDao.get_payment_stats(session)
        print(f"Payment statistics:\n{payment_stats}")

        # Get the total sum of purchases
        total_sum = await PurchaseDao.get_full_summ(session)
        print(f"Total sum of purchases: {total_sum}")

        # Get the next free ID for a new purchase
        next_id = await PurchaseDao.get_next_id(session)
        print(f"Next free ID: {next_id}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## How to Use the `CategoryDao` and `ProductDao` Classes

=========================================================================================

**Description:**

The `CategoryDao` and `ProductDao` classes provide basic methods for interacting with the `Category` and `Product` models, respectively. 

**Execution Steps:**

The `CategoryDao` and `ProductDao` classes inherit from the `BaseDAO` class and use generic type parameters to specify the models they work with. They provide basic methods for interacting with the database:

- **`get_all`**: Retrieves all records from the table.
- **`get_by_id`**: Retrieves a single record based on its ID.
- **`create`**: Inserts a new record into the table.
- **`update`**: Updates an existing record.
- **`delete`**: Deletes a record from the table.

**Usage Example:**

```python
from bot.dao.dao import CategoryDao, ProductDao
from sqlalchemy.ext.asyncio import AsyncSession

async def main():
    async with AsyncSession() as session:
        # Get all categories
        categories = await CategoryDao.get_all(session)
        print(f"All categories: {categories}")

        # Get a category by ID
        category = await CategoryDao.get_by_id(session, category_id=1)
        print(f"Category with ID 1: {category}")

        # Create a new product
        new_product = Product(name="New Product", description="Description", category_id=1, price=100)
        await ProductDao.create(session, new_product)
        print(f"New product created: {new_product}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())