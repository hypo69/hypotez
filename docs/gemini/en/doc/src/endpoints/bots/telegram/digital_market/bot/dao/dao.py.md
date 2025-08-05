# DAO for Telegram Digital Market Bot

## Overview

This module contains data access objects (DAO) for interacting with the database related to the Telegram Digital Market bot. It provides functions for retrieving and managing user data, purchase information, product details, and category information.

## Details

The DAO classes in this module use SQLAlchemy to interact with the database. They provide a layer of abstraction over the database operations, simplifying the process of retrieving and manipulating data from the database.

## Classes

### `UserDAO`

**Description**: This class provides methods for interacting with the `User` table in the database. It inherits from the base `BaseDAO` class.

**Inherits**: `BaseDAO[User]`

**Attributes**:

- `model`:  The `User` model class.

**Methods**:

- `get_purchase_statistics(session: AsyncSession, telegram_id: int) -> Optional[Dict[str, int]]`: Retrieves purchase statistics for a user based on their Telegram ID.
- `get_purchased_products(session: AsyncSession, telegram_id: int) -> Optional[List[Purchase]]`: Retrieves a list of purchases made by a user, including product information.
- `get_statistics(session: AsyncSession) -> Dict[str, int]`: Retrieves overall statistics about users, including the total number of users and the number of new users in the last day, week, and month.

### `PurchaseDao`

**Description**: This class provides methods for interacting with the `Purchase` table in the database. It inherits from the base `BaseDAO` class.

**Inherits**: `BaseDAO[Purchase]`

**Attributes**:

- `model`: The `Purchase` model class.

**Methods**:

- `get_payment_stats(session: AsyncSession) -> str`: Retrieves payment statistics, showing the total amount of money paid using different payment methods.
- `get_full_summ(session: AsyncSession) -> int`: Calculates the total amount of money paid for all purchases.
- `get_next_id(session: AsyncSession) -> int`: Retrieves the next available ID for a new purchase record.

### `CategoryDao`

**Description**: This class provides methods for interacting with the `Category` table in the database. It inherits from the base `BaseDAO` class.

**Inherits**: `BaseDAO[Category]`

**Attributes**:

- `model`: The `Category` model class.

### `ProductDao`

**Description**: This class provides methods for interacting with the `Product` table in the database. It inherits from the base `BaseDAO` class.

**Inherits**: `BaseDAO[Product]`

**Attributes**:

- `model`: The `Product` model class.


## Functions

### `get_purchase_statistics(session: AsyncSession, telegram_id: int) -> Optional[Dict[str, int]]`

**Purpose**: Retrieves purchase statistics for a user based on their Telegram ID.

**Parameters**:

- `session` (AsyncSession): An asynchronous database session.
- `telegram_id` (int): The Telegram ID of the user.

**Returns**:

- `Optional[Dict[str, int]]`: A dictionary containing the total number of purchases and the total amount spent, or `None` if no purchases were found.

**Raises Exceptions**:

- `SQLAlchemyError`: If an error occurs while interacting with the database.

**How the Function Works**:

1. The function executes a SQL query to count the number of purchases and sum the prices for a specific user based on their Telegram ID.
2. The result is extracted as a tuple containing the total number of purchases and the total amount spent.
3. The function returns a dictionary containing the extracted statistics.

**Examples**:

```python
# Example usage:
stats = await UserDAO.get_purchase_statistics(session, telegram_id=123456789)
if stats:
    print(f"Total purchases: {stats['total_purchases']}")
    print(f"Total amount spent: {stats['total_amount']}")
else:
    print("User has no purchases.")
```

### `get_purchased_products(session: AsyncSession, telegram_id: int) -> Optional[List[Purchase]]`

**Purpose**: Retrieves a list of purchases made by a user, including product information.

**Parameters**:

- `session` (AsyncSession): An asynchronous database session.
- `telegram_id` (int): The Telegram ID of the user.

**Returns**:

- `Optional[List[Purchase]]`: A list of purchase objects, or `None` if no purchases were found.

**Raises Exceptions**:

- `SQLAlchemyError`: If an error occurs while interacting with the database.

**How the Function Works**:

1. The function executes a SQL query to retrieve the user based on their Telegram ID.
2. The query uses `selectinload` to eagerly load related purchases and products.
3. The function returns the list of purchases associated with the user.

**Examples**:

```python
# Example usage:
purchases = await UserDAO.get_purchased_products(session, telegram_id=123456789)
if purchases:
    for purchase in purchases:
        print(f"Product: {purchase.product.name}")
        print(f"Price: {purchase.price}")
else:
    print("User has no purchases.")
```

### `get_statistics(session: AsyncSession) -> Dict[str, int]`

**Purpose**: Retrieves overall statistics about users, including the total number of users and the number of new users in the last day, week, and month.

**Parameters**:

- `session` (AsyncSession): An asynchronous database session.

**Returns**:

- `Dict[str, int]`: A dictionary containing the overall statistics.

**Raises Exceptions**:

- `SQLAlchemyError`: If an error occurs while interacting with the database.

**How the Function Works**:

1. The function executes a SQL query to count the total number of users and use `CASE` expressions to count the number of users created in the last day, week, and month.
2. The query uses `func.count()` to count the total number of users.
3. The query uses `func.sum()` to calculate the count of users based on the `CASE` expressions.
4. The function returns a dictionary containing the extracted statistics.

**Examples**:

```python
# Example usage:
stats = await UserDAO.get_statistics(session)
print(f"Total users: {stats['total_users']}")
print(f"New users today: {stats['new_today']}")
print(f"New users this week: {stats['new_week']}")
print(f"New users this month: {stats['new_month']}")
```

### `get_payment_stats(session: AsyncSession) -> str`

**Purpose**: Retrieves payment statistics, showing the total amount of money paid using different payment methods.

**Parameters**:

- `session` (AsyncSession): An asynchronous database session.

**Returns**:

- `str`: A formatted string representing the payment statistics.

**Raises Exceptions**:

- `SQLAlchemyError`: If an error occurs while interacting with the database.

**How the Function Works**:

1. The function executes a SQL query to group purchases by payment type and calculate the total price for each type.
2. The result is a list of tuples containing the payment type and the total amount.
3. The function iterates through the results and constructs a formatted string representing the payment statistics.

**Examples**:

```python
# Example usage:
stats = await PurchaseDao.get_payment_stats(session)
print(stats)
```

### `get_full_summ(session: AsyncSession) -> int`

**Purpose**: Calculates the total amount of money paid for all purchases.

**Parameters**:

- `session` (AsyncSession): An asynchronous database session.

**Returns**:

- `int`: The total amount of money paid.

**Raises Exceptions**:

- `SQLAlchemyError`: If an error occurs while interacting with the database.

**How the Function Works**:

1. The function executes a SQL query to sum the prices of all purchases.
2. The result is extracted as a scalar value representing the total price.

**Examples**:

```python
# Example usage:
total_price = await PurchaseDao.get_full_summ(session)
print(f"Total price: {total_price}")
```

### `get_next_id(session: AsyncSession) -> int`

**Purpose**: Retrieves the next available ID for a new purchase record.

**Parameters**:

- `session` (AsyncSession): An asynchronous database session.

**Returns**:

- `int`: The next available ID.

**Raises Exceptions**:

- `SQLAlchemyError`: If an error occurs while interacting with the database.

**How the Function Works**:

1. The function executes a SQL query to find the maximum ID of existing purchase records.
2. If no records exist, the query returns 1.
3. The function returns the maximum ID plus 1, which represents the next available ID.

**Examples**:

```python
# Example usage:
next_id = await PurchaseDao.get_next_id(session)
print(f"Next available ID: {next_id}")
```