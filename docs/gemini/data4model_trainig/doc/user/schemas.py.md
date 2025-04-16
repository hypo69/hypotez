# Модуль схем для пользовательского интерфейса Telegram-бота

## Обзор

Модуль `src.endpoints.bots.telegram.digital_market.bot.user.schemas` определяет схемы данных, используемые для валидации и представления данных в пользовательском интерфейсе Telegram-бота.

## Подробней

Модуль использует библиотеку `pydantic` для определения моделей данных, которые используются для валидации данных, поступающих от пользователей бота.

## Классы

### `TelegramIDModel`

**Описание**: Модель данных для представления ID пользователя Telegram.

**Наследует**:

*   `BaseModel` из библиотеки `pydantic`.

**Атрибуты**:

*   `telegram_id` (int): Telegram ID пользователя.

### `UserModel`

**Описание**: Модель данных для представления информации о пользователе.

**Наследует**:

*   `TelegramIDModel`: Базовая модель, содержащая Telegram ID пользователя.

**Атрибуты**:

*   `username` (str | None): Имя пользователя (может быть `None`).
*   `first_name` (str | None): Имя пользователя (может быть `None`).
*   `last_name` (str | None): Фамилия пользователя (может быть `None`).

### `ProductIDModel`

**Описание**: Модель данных для представления ID товара.

**Наследует**:

*   `BaseModel` из библиотеки `pydantic`.

**Атрибуты**:

*   `id` (int): ID товара.

### `ProductCategoryIDModel`

**Описание**: Модель данных для представления ID категории товара.

**Наследует**:

*   `BaseModel` из библиотеки `pydantic`.

**Атрибуты**:

*   `category_id` (int): ID категории товара.

### `PaymentData`

**Описание**: Модель данных для представления информации о платеже.

**Наследует**:

*   `BaseModel` из библиотеки `pydantic`.

**Атрибуты**:

*   `user_id` (int): ID пользователя Telegram.
*   `payment_id` (str): Уникальный ID платежа.
*   `price` (int): Сумма платежа в рублях.
*   `product_id` (int): ID товара.
*   `payment_type` (str): Тип оплаты.

## Примеры

Пример использования класса `UserModel`:

```python
from pydantic import ValidationError
from bot.user.schemas import UserModel

try:
    user = UserModel(
        telegram_id=123456789,
        username='testuser',
        first_name='Test',
        last_name='User'
    )
    print(user)
except ValidationError as e:
    print(e)
```