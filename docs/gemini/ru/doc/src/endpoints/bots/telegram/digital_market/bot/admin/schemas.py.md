# Модуль `schemas`

## Обзор

Этот модуль содержит схемы Pydantic для работы с данными о товарах.

## Подробнее

Модуль `schemas.py` предоставляет модели Pydantic для валидации и сериализации данных о товарах. 
Он используется для взаимодействия с API телеграм-бота, который управляет цифровым маркетом.

## Классы

### `ProductIDModel`

**Описание**: Модель для представления идентификатора товара.
**Наследует**: `pydantic.BaseModel`

**Атрибуты**:
- `id` (int): Идентификатор товара (целое число).

**Методы**: 
-  Отсутствуют

### `ProductModel`

**Описание**: Модель для представления товара.
**Наследует**: `pydantic.BaseModel`

**Атрибуты**:
- `name` (str): Название товара (строка, не менее 5 символов).
- `description` (str): Описание товара (строка, не менее 5 символов).
- `price` (int): Цена товара (целое число, больше 0).
- `category_id` (int): Идентификатор категории товара (целое число, больше 0).
- `file_id` (str | None): Идентификатор файла с изображением товара (строка или None).
- `hidden_content` (str): Скрытый контент для товара (строка, не менее 5 символов).

**Методы**: 
-  Отсутствуют


## Примеры

```python
from hypotez.src.endpoints.bots.telegram.digital_market.bot.admin.schemas import ProductModel

# Создание объекта ProductModel
product = ProductModel(
    name='Товар 1',
    description='Описание товара 1',
    price=1000,
    category_id=1,
    file_id='1234567890',
    hidden_content='Скрытый контент для товара 1',
)

# Вывод данных о товаре
print(product)
```
```python
from hypotez.src.endpoints.bots.telegram.digital_market.bot.admin.schemas import ProductIDModel

# Создание объекта ProductIDModel
product_id = ProductIDModel(
    id=1
)

# Вывод данных о товаре
print(product_id)