### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код добавляет новый товар в PrestaShop, используя API PrestaShopAsync. Сначала он получает список родительских категорий для товара, затем преобразует данные товара в формат словаря, необходимый для API PrestaShop. После этого создает новый товар и, если успешно, загружает изображение для этого товара.

Шаги выполнения
-------------------------
1. **Получение родительских категорий**:
   - Вызывается `self.presta_category_async.get_parent_categories_list(f.id_category_default)` для получения списка родительских категорий товара на основе `id_category_default`.

2. **Преобразование данных товара в словарь**:
   - Данные товара, содержащиеся в объекте `f` типа `ProductFields`, преобразуются в словарь с помощью метода `f.to_dict()`.

3. **Создание нового товара в PrestaShop**:
   - Вызывается `self.create('products', presta_product_dict)` для создания нового товара в PrestaShop с использованием API. Если товар не создан, регистрируется ошибка и функция возвращает `None`.

4. **Загрузка изображения товара**:
   - Если товар успешно создан, вызывается `self.create_binary(f'images/products/{new_f.id_product}', f.local_image_path, new_f.id_product)` для загрузки изображения товара. Если загрузка не удалась, регистрируется ошибка и функция возвращает `None`.

Пример использования
-------------------------

```python
    from src.endpoints.prestashop.product_async import PrestaProductAsync
    from src.endpoints.prestashop.product_fields import ProductFields

    async def main():
        # Пример использования
        product = PrestaProductAsync()
        product_fields = ProductFields(
            lang_index = 1,
            name='Test Product Async',
            price=19.99,
            description='This is an asynchronous test product.',
            id_category_default=3  # Добавьте id_category_default
        )
        
        new_product = await product.add_new_product_async(product_fields)
        if new_product:
            print(f'New product id = {new_product.id_product}')
        else:
            print(f'Error add new product')

    if __name__ == '__main__':
        import asyncio
        asyncio.run(main())