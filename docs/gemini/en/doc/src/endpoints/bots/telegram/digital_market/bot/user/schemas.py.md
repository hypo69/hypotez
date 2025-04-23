# Module Name

## Overview

This module defines Pydantic models for representing data related to users, products, categories, and payments in a Telegram bot context. It includes models for Telegram IDs, user information, product IDs, category IDs, and payment data.

## More details

This module provides a structured way to handle data within the Telegram bot, ensuring type safety and data validation. The models are used to represent data received from and sent to the Telegram API, as well as to store information about users, products, and payments.

## Classes

### `TelegramIDModel`

**Description**: Базовая модель для представления ID пользователя Telegram.
**Inherits**:
**Attributes**:
- `telegram_id` (int): ID пользователя в Telegram.

**Working principle**:
Модель `TelegramIDModel` является базовой и служит для представления ID пользователя в Telegram. Она включает поле `telegram_id` типа `int`, которое хранит уникальный идентификатор пользователя. Конфигурация модели `model_config` указывает, что модель может быть создана из атрибутов.

### `UserModel`

**Description**: Модель для представления информации о пользователе Telegram.
**Inherits**:
- `TelegramIDModel`: Наследует поле `telegram_id` от базовой модели.
**Attributes**:
- `username` (str | None): Имя пользователя в Telegram (может отсутствовать).
- `first_name` (str | None): Имя пользователя (может отсутствовать).
- `last_name` (str | None): Фамилия пользователя (может отсутствовать).

**Working principle**:
Модель `UserModel` расширяет `TelegramIDModel`, добавляя поля для хранения имени пользователя, имени и фамилии. Все строковые поля являются необязательными и могут иметь значение `None`. Это позволяет хранить неполную информацию о пользователях, если какие-то данные отсутствуют.

### `ProductIDModel`

**Description**: Модель для представления ID товара.
**Inherits**:
**Attributes**:
- `id` (int): ID товара.

**Working principle**:
Модель `ProductIDModel` предназначена для представления ID товара. Она содержит поле `id` типа `int`, которое хранит уникальный идентификатор товара.

### `ProductCategoryIDModel`

**Description**: Модель для представления ID категории товара.
**Inherits**:
**Attributes**:
- `category_id` (int): ID категории товара.

**Working principle**:
Модель `ProductCategoryIDModel` предназначена для представления ID категории товара. Она содержит поле `category_id` типа `int`, которое хранит уникальный идентификатор категории.

### `PaymentData`

**Description**: Модель для представления данных о платеже.
**Inherits**:
**Attributes**:
- `user_id` (int): ID пользователя Telegram.
- `payment_id` (str): Уникальный ID платежа.
- `price` (int): Сумма платежа в рублях.
- `product_id` (int): ID товара.
- `payment_type` (str): Тип оплаты.

**Working principle**:
Модель `PaymentData` используется для хранения информации о платежах, совершаемых пользователями. Она включает поля для ID пользователя, уникального ID платежа, суммы платежа, ID товара и типа оплаты. Модель обеспечивает структурированное представление данных о платежах и упрощает их обработку.

## Class Methods

### `TelegramIDModel`

#### `model_config`

```python
model_config = ConfigDict(from_attributes=True)
```

**Purpose**: Конфигурирует модель для создания экземпляров из атрибутов.

**Parameters**:
- Нет

**Returns**:
- Нет

**Raises**:
- Нет

**How the function works**:
Конфигурация `model_config` задает настройку `from_attributes=True`, что позволяет создавать экземпляры модели `TelegramIDModel` из атрибутов, например, из объектов базы данных.

**Examples**:
```python
from pydantic import BaseModel, ConfigDict

class MyModel(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

data = {"id": 1, "name": "Example"}
model_instance = MyModel(**data)
print(model_instance)
```

### `PaymentData`

#### `__init__`

```python
def __init__(self, user_id: int = Field(..., description="ID пользователя Telegram"),
                 payment_id: str = Field(..., max_length=255, description="Уникальный ID платежа"),
                 price: int = Field(..., description="Сумма платежа в рублях"),
                 product_id: int = Field(..., description="ID товара"),
                 payment_type: str = Field(..., description="Тип оплаты")):
    """
    Инициализирует модель данных платежа.
    Args:
        user_id (int): ID пользователя Telegram.
        payment_id (str): Уникальный ID платежа.
        price (int): Сумма платежа в рублях.
        product_id (int): ID товара.
        payment_type (str): Тип оплаты.
    """
```

**Purpose**: Инициализация экземпляра класса `PaymentData`.

**Parameters**:
- `user_id` (int): ID пользователя Telegram.
- `payment_id` (str): Уникальный ID платежа.
- `price` (int): Сумма платежа в рублях.
- `product_id` (int): ID товара.
- `payment_type` (str): Тип оплаты.

**Returns**:
- Нет

**Raises**:
- Нет

**How the function works**:
Метод `__init__` инициализирует экземпляр класса `PaymentData` с заданными параметрами.

**Examples**:
```python
from pydantic import BaseModel, Field

class PaymentData(BaseModel):
    user_id: int = Field(..., description="ID пользователя Telegram")
    payment_id: str = Field(..., max_length=255, description="Уникальный ID платежа")
    price: int = Field(..., description="Сумма платежа в рублях")
    product_id: int = Field(..., description="ID товара")
    payment_type: str = Field(..., description="Тип оплаты")

payment_data = PaymentData(user_id=123, payment_id="abc", price=100, product_id=1, payment_type="card")
print(payment_data)
```
## Class Parameters

- `telegram_id` (int): Уникальный идентификатор пользователя в Telegram.
- `username` (str | None): Имя пользователя в Telegram (может быть `None`).
- `first_name` (str | None): Имя пользователя (может быть `None`).
- `last_name` (str | None): Фамилия пользователя (может быть `None`).
- `id` (int): Уникальный идентификатор товара.
- `category_id` (int): Уникальный идентификатор категории товара.
- `user_id` (int): ID пользователя Telegram.
- `payment_id` (str): Уникальный ID платежа.
- `price` (int): Сумма платежа в рублях.
- `product_id` (int): ID товара.
- `payment_type` (str): Тип оплаты.