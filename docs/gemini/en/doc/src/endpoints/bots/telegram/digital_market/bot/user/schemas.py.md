# Schemas for Telegram User, Product, and Payment Data

## Overview

This module defines Pydantic models for representing user data, product information, and payment details within the context of a Telegram bot. Pydantic models provide a structured way to define data schemas and ensure type validation.

## Details

These schemas are essential for processing and validating user data, product information, and payment details within the Telegram bot's functionality. They ensure consistency and data integrity, enabling secure and reliable data handling.

## Classes

### `TelegramIDModel`

**Description**: Base model for representing a Telegram user's ID.

**Attributes**:

- `telegram_id` (int): The unique Telegram ID of the user.

### `UserModel`

**Description**: Model for representing a Telegram user. Inherits from `TelegramIDModel`.

**Attributes**:

- `telegram_id` (int): The unique Telegram ID of the user.
- `username` (str | None): The user's Telegram username, if available.
- `first_name` (str | None): The user's first name.
- `last_name` (str | None): The user's last name.

### `ProductIDModel`

**Description**: Model for representing a product ID.

**Attributes**:

- `id` (int): The unique ID of the product.

### `ProductCategoryIDModel`

**Description**: Model for representing a product category ID.

**Attributes**:

- `category_id` (int): The unique ID of the product category.

### `PaymentData`

**Description**: Model for representing payment data.

**Attributes**:

- `user_id` (int): The ID of the Telegram user making the payment.
- `payment_id` (str): The unique ID of the payment.
- `price` (int): The price of the product in rubles.
- `product_id` (int): The ID of the product being purchased.
- `payment_type` (str): The type of payment method used.

## Examples

```python
from hypotez.src.endpoints.bots.telegram.digital_market.bot.user.schemas import (
    TelegramIDModel,
    UserModel,
    ProductIDModel,
    ProductCategoryIDModel,
    PaymentData,
)

# Example usage:
user_data = UserModel(
    telegram_id=123456789,
    username="@username",
    first_name="John",
    last_name="Doe",
)

product_id = ProductIDModel(id=100)

payment_details = PaymentData(
    user_id=user_data.telegram_id,
    payment_id="unique_payment_id",
    price=1000,
    product_id=product_id.id,
    payment_type="card",
)
```