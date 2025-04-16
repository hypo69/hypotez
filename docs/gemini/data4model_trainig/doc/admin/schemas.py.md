# Модуль схем данных для админ-панели Telegram-бота

## Обзор

Модуль `src.endpoints.bots.telegram.digital_market.bot.admin.schemas` определяет схемы данных, используемые для валидации и управления данными в админ-панели Telegram-бота.

## Подробней

Модуль использует библиотеку `pydantic` для определения моделей данных, которые используются для валидации данных, поступающих от администраторов бота.

## Классы

### `ProductIDModel`

**Описание**: Модель данных для представления ID товара.

**Наследует**:

*   `BaseModel` из библиотеки `pydantic`.

**Атрибуты**:

*   `id` (int): ID товара.

### `ProductModel`

**Описание**: Модель данных для представления информации о товаре.

**Наследует**:

*   `BaseModel` из библиотеки `pydantic`.

**Атрибуты**:

*   `name` (str): Название товара (минимум 5 символов).
*   `description` (str): Описание товара (минимум 5 символов).
*   `price` (int): Цена товара (должна быть больше 0).
*   `category_id` (int): ID категории товара (должен быть больше 0).
*   `file_id` (str | None): ID файла товара (может отсутствовать).
*   `hidden_content` (str): Скрытый контент товара (минимум 5 символов).

## Примеры

Пример использования класса `ProductModel`:

```python
from pydantic import ValidationError
from bot.admin.schemas import ProductModel

try:
    product = ProductModel(
        name='Test Product',
        description='Test description',
        price=100,
        category_id=1,
        file_id=None,
        hidden_content='Hidden content'
    )
    print(product)
except ValidationError as e:
    print(e)
```