## Как использовать класс `PrestaProductAsync`
=========================================================================================

Описание
-------------------------
Класс `PrestaProductAsync`  предназначен для взаимодействия с товарами в PrestaShop. Он наследуется от класса `PrestaShopAsync` и предоставляет методы для добавления новых товаров, а также для получения информации о товарах.

Шаги выполнения
-------------------------
1. **Инициализация класса**: Создайте экземпляр класса `PrestaProductAsync`. В конструктор класса передайте необходимые параметры, такие как URL-адрес PrestaShop, учетные данные API и т.д.
2. **Добавление нового товара**: Используйте метод `add_new_product_async` для добавления нового товара в PrestaShop. Передайте в метод объект `ProductFields`, содержащий информацию о товаре.
3. **Получение информации о товаре**: Используйте методы, унаследованные от класса `PrestaShopAsync`, для получения информации о товарах, таких как `get_products` и `get_product`.

Пример использования
-------------------------

```python
from src.endpoints.prestashop.product_async import PrestaProductAsync
from src.endpoints.prestashop.product_fields import ProductFields

async def main():
    # Создаем экземпляр класса PrestaProductAsync
    product = PrestaProductAsync()

    # Создаем объект ProductFields с данными о товаре
    product_fields = ProductFields(
        lang_index=1,
        name='Test Product Async',
        price=19.99,
        description='This is an asynchronous test product.',
    )

    # Получаем список родительских категорий для id_category=3
    parent_categories = await product.presta_category_async.get_parent_categories_list(id_category=3)
    print(f'Parent categories: {parent_categories}')

    # Добавляем новый товар в PrestaShop
    new_product = await product.add_new_product_async(product_fields)
    if new_product:
        print(f'New product id = {new_product.id_product}')
    else:
        print(f'Error add new product')

    # Вызываем метод fetch_data_async() для получения данных о товарах
    await product.fetch_data_async()

if __name__ == '__main__':
    asyncio.run(main())
```