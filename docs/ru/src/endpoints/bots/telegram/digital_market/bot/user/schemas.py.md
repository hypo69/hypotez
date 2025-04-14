# Модуль schemas.py

## Обзор

Модуль `schemas.py` содержит определения Pydantic моделей, используемых для валидации и представления данных, связанных с пользователями Telegram, продуктами и платежами в контексте Telegram-бота для цифрового рынка. Эти модели используются для обеспечения типов данных, валидации входных данных и удобной передачи данных между различными компонентами бота.

## Подробнее

Модуль определяет несколько моделей Pydantic, каждая из которых представляет собой определенный тип данных. `TelegramIDModel` служит базовой моделью для идентификации пользователей по их Telegram ID. `UserModel` расширяет эту модель, добавляя информацию об имени пользователя. Модели `ProductIDModel` и `ProductCategoryIDModel` используются для идентификации продуктов и категорий продуктов, соответственно. `PaymentData` используется для хранения информации о платежах, совершаемых пользователями.

## Классы

### `TelegramIDModel`

**Описание**: Базовая модель для представления идентификатора пользователя Telegram.

**Наследует**: `pydantic.BaseModel`

**Атрибуты**:
- `telegram_id` (int): Уникальный идентификатор пользователя в Telegram.

**Методы**: Нет

**Принцип работы**:
Модель `TelegramIDModel` используется для представления идентификатора пользователя Telegram. Атрибут `telegram_id` содержит уникальный идентификатор пользователя. Конфигурация модели `model_config` позволяет создавать экземпляры модели из атрибутов объектов.

### `UserModel`

**Описание**: Модель для представления информации о пользователе Telegram.

**Наследует**: `TelegramIDModel`

**Атрибуты**:
- `username` (str | None): Имя пользователя в Telegram (может отсутствовать).
- `first_name` (str | None): Имя пользователя (может отсутствовать).
- `last_name` (str | None): Фамилия пользователя (может отсутствовать).

**Методы**: Нет

**Принцип работы**:
Модель `UserModel` расширяет модель `TelegramIDModel`, добавляя информацию об имени пользователя, имени и фамилии. Атрибуты `username`, `first_name` и `last_name` могут отсутствовать.

### `ProductIDModel`

**Описание**: Модель для представления идентификатора продукта.

**Наследует**: `pydantic.BaseModel`

**Атрибуты**:
- `id` (int): Уникальный идентификатор продукта.

**Методы**: Нет

**Принцип работы**:
Модель `ProductIDModel` используется для представления идентификатора продукта. Атрибут `id` содержит уникальный идентификатор продукта.

### `ProductCategoryIDModel`

**Описание**: Модель для представления идентификатора категории продукта.

**Наследует**: `pydantic.BaseModel`

**Атрибуты**:
- `category_id` (int): Уникальный идентификатор категории продукта.

**Методы**: Нет

**Принцип работы**:
Модель `ProductCategoryIDModel` используется для представления идентификатора категории продукта. Атрибут `category_id` содержит уникальный идентификатор категории продукта.

### `PaymentData`

**Описание**: Модель для представления данных о платеже.

**Наследует**: `pydantic.BaseModel`

**Атрибуты**:
- `user_id` (int): ID пользователя Telegram.
- `payment_id` (str): Уникальный ID платежа.
- `price` (int): Сумма платежа в рублях.
- `product_id` (int): ID товара.
- `payment_type` (str): Тип оплаты.

**Методы**: Нет

**Принцип работы**:
Модель `PaymentData` используется для представления данных о платеже. Атрибуты `user_id`, `payment_id`, `price`, `product_id` и `payment_type` содержат информацию о платеже.

## Параметры класса

- `telegram_id` (int): Уникальный идентификатор пользователя в Telegram.
- `username` (str | None): Имя пользователя в Telegram (может отсутствовать).
- `first_name` (str | None): Имя пользователя (может отсутствовать).
- `last_name` (str | None): Фамилия пользователя (может отсутствовать).
- `id` (int): Уникальный идентификатор продукта.
- `category_id` (int): Уникальный идентификатор категории продукта.
- `user_id` (int): ID пользователя Telegram.
- `payment_id` (str): Уникальный ID платежа.
- `price` (int): Сумма платежа в рублях.
- `product_id` (int): ID товара.
- `payment_type` (str): Тип оплаты.

## Примеры

```python
from pydantic import BaseModel, ConfigDict, Field

class TelegramIDModel(BaseModel):
    telegram_id: int

    model_config = ConfigDict(from_attributes=True)

# Пример создания экземпляра класса TelegramIDModel
telegram_id_model = TelegramIDModel(telegram_id=123456789)
print(telegram_id_model)
# Вывод: telegram_id=123456789

class UserModel(TelegramIDModel):
    username: str | None
    first_name: str | None
    last_name: str | None

# Пример создания экземпляра класса UserModel
user_model = UserModel(telegram_id=123456789, username="testuser", first_name="Test", last_name="User")
print(user_model)
# Вывод: telegram_id=123456789 username='testuser' first_name='Test' last_name='User'

class ProductIDModel(BaseModel):
    id: int

# Пример создания экземпляра класса ProductIDModel
product_id_model = ProductIDModel(id=1)
print(product_id_model)
# Вывод: id=1

class ProductCategoryIDModel(BaseModel):
    category_id: int

# Пример создания экземпляра класса ProductCategoryIDModel
product_category_id_model = ProductCategoryIDModel(category_id=1)
print(product_category_id_model)
# Вывод: category_id=1

class PaymentData(BaseModel):
    user_id: int = Field(..., description="ID пользователя Telegram")
    payment_id: str = Field(..., max_length=255, description="Уникальный ID платежа")
    price: int = Field(..., description="Сумма платежа в рублях")
    product_id: int = Field(..., description="ID товара")
    payment_type: str = Field(..., description="Тип оплаты")

# Пример создания экземпляра класса PaymentData
payment_data = PaymentData(user_id=123456789, payment_id="payment123", price=100, product_id=1, payment_type="card")
print(payment_data)
# Вывод: user_id=123456789 payment_id='payment123' price=100 product_id=1 payment_type='card'