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
This code block defines Pydantic models used to represent data related to users, products, and payments within the Telegram bot application.

Execution Steps
-------------------------
1. **Defines `TelegramIDModel`**: This model represents a Telegram user's ID, defining a single field `telegram_id` of type `int`.
2. **Defines `UserModel`**: This model extends `TelegramIDModel`, adding fields for the user's username, first name, and last name. 
3. **Defines `ProductIDModel`**: This model represents a product's ID, defining a single field `id` of type `int`.
4. **Defines `ProductCategoryIDModel`**: This model represents a product category's ID, defining a single field `category_id` of type `int`.
5. **Defines `PaymentData`**: This model represents payment data, defining fields for user ID, payment ID, price, product ID, and payment type.

Usage Example
-------------------------

```python
from hypotez.src.endpoints.bots.telegram.digital_market.bot.user.schemas import PaymentData

# Create a PaymentData instance
payment_data = PaymentData(
    user_id=123456789,
    payment_id="unique_payment_id",
    price=1000,
    product_id=1,
    payment_type="card"
)

# Access payment data attributes
print(payment_data.user_id)  # Output: 123456789
print(payment_data.payment_id)  # Output: unique_payment_id
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".