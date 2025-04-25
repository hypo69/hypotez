# Модуль схемы данных для Telegram-бота

## Обзор

Модуль содержит схемы данных, используемые в Telegram-боте для обработки запросов и ответов. 

## Классы

### `TelegramIDModel`

**Описание**: Базовая схема для хранения Telegram ID пользователя.

**Атрибуты**:

- `telegram_id` (int): Telegram ID пользователя.

### `UserModel`

**Описание**:  Схема для хранения информации о пользователе Telegram. 

**Наследует**: `TelegramIDModel`

**Атрибуты**:

- `telegram_id` (int): Telegram ID пользователя.
- `username` (str | None): Имя пользователя в Telegram (может быть `None`).
- `first_name` (str | None): Имя пользователя (может быть `None`).
- `last_name` (str | None): Фамилия пользователя (может быть `None`).

### `ProductIDModel`

**Описание**: Схема для хранения ID товара.

**Атрибуты**:

- `id` (int): ID товара.

### `ProductCategoryIDModel`

**Описание**: Схема для хранения ID категории товара.

**Атрибуты**:

- `category_id` (int): ID категории товара.

### `PaymentData`

**Описание**: Схема для хранения данных о платеже.

**Атрибуты**:

- `user_id` (int): ID пользователя Telegram.
- `payment_id` (str): Уникальный ID платежа.
- `price` (int): Сумма платежа в рублях.
- `product_id` (int): ID товара.
- `payment_type` (str): Тип оплаты.

## Примеры

**Пример использования `UserModel`**:

```python
from hypotez.src.endpoints.bots.telegram.digital_market.bot.user.schemas import UserModel

user_data = {
    "telegram_id": 123456789,
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe"
}

user = UserModel(**user_data)

print(user.telegram_id)  # Вывод: 123456789
print(user.username)     # Вывод: johndoe
```
```markdown