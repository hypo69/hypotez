# Модуль schemas

## Обзор

Модуль определяет Pydantic модели для представления данных, связанных с пользователями Telegram, товарами и платежами. Модели используются для валидации и сериализации данных, передаваемых между различными компонентами телеграм-бота.

## Подробней

Этот модуль содержит определения схем данных, используемых в телеграм-боте для цифрового рынка. Он определяет структуру данных для идентификации пользователей Telegram, товаров и категорий товаров, а также для обработки платежной информации. Использование Pydantic позволяет обеспечить строгую типизацию и валидацию данных, что повышает надежность и удобство разработки.

## Классы

### `TelegramIDModel`

**Описание**: Базовая модель для представления идентификатора пользователя Telegram.
**Наследует**: `BaseModel` (Pydantic).

**Атрибуты**:
- `telegram_id` (int): Уникальный идентификатор пользователя Telegram.

**Методы**:
- Нет

**Принцип работы**:
Класс определяет структуру данных для хранения идентификатора пользователя Telegram. Атрибут `telegram_id` содержит числовое значение, однозначно идентифицирующее пользователя в системе Telegram. `model_config = ConfigDict(from_attributes=True)` указывает, что модель может быть создана из атрибутов класса.

### `UserModel`

**Описание**: Модель для представления информации о пользователе Telegram.
**Наследует**: `TelegramIDModel`.

**Атрибуты**:
- `username` (str | None): Имя пользователя Telegram (может отсутствовать).
- `first_name` (str | None): Имя пользователя (может отсутствовать).
- `last_name` (str | None): Фамилия пользователя (может отсутствовать).

**Методы**:
- Нет

**Принцип работы**:
Класс расширяет базовую модель `TelegramIDModel`, добавляя атрибуты для хранения имени пользователя, имени и фамилии. Все строковые атрибуты являются необязательными и могут иметь значение `None`. Это позволяет представлять информацию о пользователях, для которых известны только некоторые данные.

### `ProductIDModel`

**Описание**: Модель для представления идентификатора товара.
**Наследует**: `BaseModel` (Pydantic).

**Атрибуты**:
- `id` (int): Уникальный идентификатор товара.

**Методы**:
- Нет

**Принцип работы**:
Класс определяет структуру данных для хранения идентификатора товара. Атрибут `id` содержит числовое значение, однозначно идентифицирующее товар.

### `ProductCategoryIDModel`

**Описание**: Модель для представления идентификатора категории товара.
**Наследует**: `BaseModel` (Pydantic).

**Атрибуты**:
- `category_id` (int): Уникальный идентификатор категории товара.

**Методы**:
- Нет

**Принцип работы**:
Класс определяет структуру данных для хранения идентификатора категории товара. Атрибут `category_id` содержит числовое значение, однозначно идентифицирующее категорию товара.

### `PaymentData`

**Описание**: Модель для представления данных о платеже.
**Наследует**: `BaseModel` (Pydantic).

**Атрибуты**:
- `user_id` (int): ID пользователя Telegram.
- `payment_id` (str): Уникальный ID платежа.
- `price` (int): Сумма платежа в рублях.
- `product_id` (int): ID товара.
- `payment_type` (str): Тип оплаты.

**Методы**:
- Нет

**Принцип работы**:
Класс определяет структуру данных для хранения информации о платеже. Атрибуты содержат ID пользователя, уникальный ID платежа, сумму платежа в рублях, ID товара и тип оплаты. Атрибуты `user_id`, `payment_id`, `price`, и `product_id` являются обязательными и должны быть предоставлены при создании экземпляра класса. Максимальная длина `payment_id` составляет 255 символов.

## Параметры класса

### `TelegramIDModel`

- `telegram_id` (int): Уникальный идентификатор пользователя Telegram.

### `UserModel`

- `username` (str | None): Имя пользователя Telegram (может отсутствовать).
- `first_name` (str | None): Имя пользователя (может отсутствовать).
- `last_name` (str | None): Фамилия пользователя (может отсутствовать).

### `ProductIDModel`

- `id` (int): Уникальный идентификатор товара.

### `ProductCategoryIDModel`

- `category_id` (int): Уникальный идентификатор категории товара.

### `PaymentData`

- `user_id` (int): ID пользователя Telegram.
- `payment_id` (str): Уникальный ID платежа.
- `price` (int): Сумма платежа в рублях.
- `product_id` (int): ID товара.
- `payment_type` (str): Тип оплаты.

## Примеры

### `TelegramIDModel`
```python
from src.endpoints.bots.telegram.digital_market.bot.user.schemas import TelegramIDModel

telegram_id_model = TelegramIDModel(telegram_id=123456789)
print(telegram_id_model.telegram_id)
```

### `UserModel`
```python
from src.endpoints.bots.telegram.digital_market.bot.user.schemas import UserModel

user_model = UserModel(telegram_id=123456789, username="testuser", first_name="Test", last_name="User")
print(user_model.username)
```

### `ProductIDModel`
```python
from src.endpoints.bots.telegram.digital_market.bot.user.schemas import ProductIDModel

product_id_model = ProductIDModel(id=123)
print(product_id_model.id)
```

### `ProductCategoryIDModel`
```python
from src.endpoints.bots.telegram.digital_market.bot.user.schemas import ProductCategoryIDModel

product_category_id_model = ProductCategoryIDModel(category_id=456)
print(product_category_id_model.category_id)
```

### `PaymentData`
```python
from src.endpoints.bots.telegram.digital_market.bot.user.schemas import PaymentData

payment_data = PaymentData(user_id=123456789, payment_id="payment123", price=100, product_id=123, payment_type="card")
print(payment_data.price)
```