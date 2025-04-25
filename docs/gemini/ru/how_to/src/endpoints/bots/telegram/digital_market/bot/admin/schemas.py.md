## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет две модели данных (schemas) для представления информации о товаре в Telegram-боте: `ProductIDModel` и `ProductModel`.

Шаги выполнения
-------------------------
1. **Определение модели `ProductIDModel`:** 
    - Определяется модель `ProductIDModel` с помощью класса `BaseModel` из библиотеки `pydantic`.
    - Модель имеет единственное поле `id` типа `int`, которое представляет собой идентификатор товара.

2. **Определение модели `ProductModel`:** 
    - Определяется модель `ProductModel` с помощью класса `BaseModel` из библиотеки `pydantic`.
    - Модель имеет следующие поля:
        - `name` (строка): Название товара (не менее 5 символов).
        - `description` (строка): Описание товара (не менее 5 символов).
        - `price` (целое число): Цена товара (больше 0).
        - `category_id` (целое число): Идентификатор категории товара (больше 0).
        - `file_id` (строка, опционально): Идентификатор файла с изображением товара (может быть None).
        - `hidden_content` (строка): Скрытое содержимое (не менее 5 символов).

Пример использования
-------------------------

```python
from hypotez.src.endpoints.bots.telegram.digital_market.bot.admin.schemas import ProductIDModel, ProductModel

# Создание экземпляра модели ProductIDModel
product_id = ProductIDModel(id=123)

# Создание экземпляра модели ProductModel
product = ProductModel(
    name="Ноутбук Acer", 
    description="Ноутбук Acer Aspire 5 A515-45-R74Z",
    price=50000,
    category_id=1,
    file_id="AgADAgADZPEAAvG4Gw",
    hidden_content="Скидка 10% при покупке до конца месяца"
)

# Вывод данных модели
print(product_id)  # Output: ProductIDModel(id=123)
print(product)  # Output: ProductModel(name='Ноутбук Acer', description='Ноутбук Acer Aspire 5 A515-45-R74Z', price=50000, category_id=1, file_id='AgADAgADZPEAAvG4Gw', hidden_content='Скидка 10% при покупке до конца месяца')
```