# Модуль schemas.py

## Обзор

Модуль содержит Pydantic-схемы для представления данных, связанных с пользователями Telegram, продуктами, категориями продуктов и платежами. Эти схемы используются для валидации и сериализации данных при взаимодействии с Telegram ботом цифрового рынка.

## Подробней

Этот модуль определяет структуры данных, используемые для обработки информации о пользователях Telegram, идентификаторах продуктов и категорий, а также данных об оплате.  Схемы `TelegramIDModel`, `UserModel`, `ProductIDModel`, `ProductCategoryIDModel` и `PaymentData` служат для стандартизации и проверки типов данных, передаваемых между различными компонентами приложения.

## Классы

### `TelegramIDModel`

**Описание**: Базовая модель для представления идентификатора пользователя Telegram.

**Атрибуты**:

- `telegram_id` (int): Уникальный идентификатор пользователя в Telegram.

**Принцип работы**:

Класс `TelegramIDModel` является базовой моделью, используемой для представления идентификатора пользователя в Telegram. Он содержит поле `telegram_id`, которое должно быть целым числом. `model_config = ConfigDict(from_attributes=True)` позволяет создавать экземпляры класса из атрибутов объектов.

### `UserModel`

**Описание**: Модель для представления информации о пользователе Telegram.

**Наследует**:

- `TelegramIDModel`: Наследует поле `telegram_id` от базовой модели.

**Атрибуты**:

- `username` (str | None): Имя пользователя в Telegram (может отсутствовать).
- `first_name` (str | None): Имя пользователя (может отсутствовать).
- `last_name` (str | None): Фамилия пользователя (может отсутствовать).

**Принцип работы**:

Класс `UserModel` расширяет `TelegramIDModel`, добавляя поля для хранения имени пользователя, имени и фамилии пользователя Telegram. Поля `username`, `first_name` и `last_name` могут быть `None`, если информация о пользователе недоступна.

### `ProductIDModel`

**Описание**: Модель для представления идентификатора продукта.

**Атрибуты**:

- `id` (int): Уникальный идентификатор продукта.

**Принцип работы**:

Класс `ProductIDModel` представляет идентификатор продукта. Он содержит поле `id`, которое должно быть целым числом.

### `ProductCategoryIDModel`

**Описание**: Модель для представления идентификатора категории продукта.

**Атрибуты**:

- `category_id` (int): Уникальный идентификатор категории продукта.

**Принцип работы**:

Класс `ProductCategoryIDModel` представляет идентификатор категории продукта. Он содержит поле `category_id`, которое должно быть целым числом.

### `PaymentData`

**Описание**: Модель для представления данных об оплате.

**Атрибуты**:

-   `user_id` (int): ID пользователя Telegram
-   `payment_id` (str): Уникальный ID платежа
-   `price` (int): Сумма платежа в рублях
-   `product_id` (int): ID товара
-   `payment_type` (str): Тип оплаты

**Принцип работы**:

Класс `PaymentData` используется для представления данных об оплате. Он содержит поля для хранения ID пользователя, ID платежа, суммы платежа, ID товара и типа оплаты.

## Методы класса

В данном файле отсутствуют методы классов.

## Параметры класса

### `TelegramIDModel`

- `telegram_id` (int): Уникальный идентификатор пользователя в Telegram.

### `UserModel`

- `username` (str | None): Имя пользователя в Telegram (может отсутствовать).
- `first_name` (str | None): Имя пользователя (может отсутствовать).
- `last_name` (str | None): Фамилия пользователя (может отсутствовать).

### `ProductIDModel`

- `id` (int): Уникальный идентификатор продукта.

### `ProductCategoryIDModel`

- `category_id` (int): Уникальный идентификатор категории продукта.

### `PaymentData`

-   `user_id` (int): ID пользователя Telegram
-   `payment_id` (str): Уникальный ID платежа
-   `price` (int): Сумма платежа в рублях
-   `product_id` (int): ID товара
-   `payment_type` (str): Тип оплаты

## Примеры

### `TelegramIDModel`

```python
from pydantic import BaseModel, ConfigDict

class TelegramIDModel(BaseModel):
    telegram_id: int
    model_config = ConfigDict(from_attributes=True)

# Пример создания экземпляра класса
telegram_id_model = TelegramIDModel(telegram_id=123456789)
print(telegram_id_model)
```

### `UserModel`

```python
from pydantic import BaseModel, ConfigDict

class TelegramIDModel(BaseModel):
    telegram_id: int
    model_config = ConfigDict(from_attributes=True)

class UserModel(TelegramIDModel):
    username: str | None
    first_name: str | None
    last_name: str | None

# Пример создания экземпляра класса
user_model = UserModel(telegram_id=123456789, username='testuser', first_name='Иван', last_name='Иванов')
print(user_model)
```

### `ProductIDModel`

```python
from pydantic import BaseModel

class ProductIDModel(BaseModel):
    id: int

# Пример создания экземпляра класса
product_id_model = ProductIDModel(id=123)
print(product_id_model)
```

### `ProductCategoryIDModel`

```python
from pydantic import BaseModel

class ProductCategoryIDModel(BaseModel):
    category_id: int

# Пример создания экземпляра класса
product_category_id_model = ProductCategoryIDModel(category_id=456)
print(product_category_id_model)
```

### `PaymentData`

```python
from pydantic import BaseModel, Field

class PaymentData(BaseModel):
    user_id: int = Field(..., description="ID пользователя Telegram")
    payment_id: str = Field(..., max_length=255, description="Уникальный ID платежа")
    price: int = Field(..., description="Сумма платежа в рублях")
    product_id: int = Field(..., description="ID товара")
    payment_type: str = Field(..., description="Тип оплаты")

# Пример создания экземпляра класса
payment_data = PaymentData(user_id=123456789, payment_id='payment123', price=1000, product_id=123, payment_type='card')
print(payment_data)