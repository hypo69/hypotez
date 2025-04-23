### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет несколько моделей данных (схем) для использования в Telegram-боте цифрового магазина. Он использует библиотеку `pydantic` для объявления моделей данных с валидацией типов и конфигурациями.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Из библиотеки `pydantic` импортируются классы `BaseModel`, `ConfigDict` и `Field`. `BaseModel` используется как базовый класс для создания моделей данных. `ConfigDict` позволяет настроить поведение модели. `Field` используется для определения дополнительных параметров полей модели.

2. **Определение модели `TelegramIDModel`**:
   - Создается класс `TelegramIDModel`, наследующийся от `BaseModel`.
   - Определяется поле `telegram_id` типа `int`, представляющее идентификатор пользователя в Telegram.
   - Устанавливается конфигурация модели `model_config` с `from_attributes=True`, что позволяет создавать экземпляры модели из атрибутов объекта.

3. **Определение модели `UserModel`**:
   - Создается класс `UserModel`, наследующийся от `TelegramIDModel`.
   - Добавляются поля `username`, `first_name` и `last_name`, представляющие имя пользователя, имя и фамилию соответственно. Все поля являются необязательными (типа `str | None`).

4. **Определение модели `ProductIDModel`**:
   - Создается класс `ProductIDModel`, наследующийся от `BaseModel`.
   - Определяется поле `id` типа `int`, представляющее идентификатор товара.

5. **Определение модели `ProductCategoryIDModel`**:
   - Создается класс `ProductCategoryIDModel`, наследующийся от `BaseModel`.
   - Определяется поле `category_id` типа `int`, представляющее идентификатор категории товара.

6. **Определение модели `PaymentData`**:
   - Создается класс `PaymentData`, наследующийся от `BaseModel`.
   - Определяются следующие поля:
     - `user_id` типа `int` с описанием "ID пользователя Telegram".
     - `payment_id` типа `str` с максимальной длиной 255 символов и описанием "Уникальный ID платежа".
     - `price` типа `int` с описанием "Сумма платежа в рублях".
     - `product_id` типа `int` с описанием "ID товара".
     - `payment_type` типа `str` с описанием "Тип оплаты".
   - Поле `user_id` объявлено как обязательное с использованием `Field(..., description="ID пользователя Telegram")`.

Пример использования
-------------------------

```python
from pydantic import BaseModel, ConfigDict, Field


class TelegramIDModel(BaseModel):
    telegram_id: int

    model_config = ConfigDict(from_attributes=True)


class UserModel(TelegramIDModel):
    username: str | None
    first_name: str | None
    last_name: str | None


class ProductIDModel(BaseModel):
    id: int


class ProductCategoryIDModel(BaseModel):
    category_id: int


class PaymentData(BaseModel):
    user_id: int = Field(..., description="ID пользователя Telegram")
    payment_id: str = Field(..., max_length=255, description="Уникальный ID платежа")
    price: int = Field(..., description="Сумма платежа в рублях")
    product_id: int = Field(..., description="ID товара")
    payment_type: str = Field(..., description="Тип оплаты")


# Пример создания экземпляра модели UserModel
user_data = {
    "telegram_id": 123456789,
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
}

user = UserModel(**user_data)
print(f"Username: {user.username}")

# Пример создания экземпляра модели PaymentData
payment_data = {
    "user_id": 987654321,
    "payment_id": "PAY_12345",
    "price": 1000,
    "product_id": 101,
    "payment_type": "credit_card",
}

payment = PaymentData(**payment_data)
print(f"Payment ID: {payment.payment_id}")