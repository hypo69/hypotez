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
This code defines a set of SQL Alchemy models for a Telegram bot selling digital products. 

Execution Steps
-------------------------
1. The code imports necessary libraries including `typing`, `sqlalchemy.orm`, and `sqlalchemy`.
2. It defines a base class `Base` to inherit from.
3. The code defines four classes representing different entities:
    - `User`: Represents a Telegram user with their ID, username, and purchase history.
    - `Category`: Represents a category for products.
    - `Product`: Represents a digital product with its name, description, price, file ID, category, hidden content, and purchase history.
    - `Purchase`: Represents a purchase made by a user for a specific product with information about payment.
4. Each class maps attributes to database columns using `mapped_column` and defines relationships between different classes using `relationship` (one-to-many and many-to-many).
5. The `__repr__` method of each class provides a string representation of the object.

Usage Example
-------------------------

```python
from bot.dao.models import User, Product, Purchase, Category

# Create a new user
user = User(telegram_id=123456789, username='johndoe')

# Create a new category
category = Category(category_name='Books')

# Create a new product
product = Product(
    name='The Hitchhiker's Guide to the Galaxy',
    description='A humorous science fiction novel',
    price=10,
    category=category,
)

# Create a new purchase
purchase = Purchase(
    user=user,
    product=product,
    price=product.price,
    payment_type='Card',
    payment_id='1234567890',
)

# Save the entities to the database
from bot.dao.database import engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()
session.add_all([user, category, product, purchase])
session.commit()
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".