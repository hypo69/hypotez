## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Блок кода представляет собой метод `process_affiliate_products` класса `AliAffiliatedProducts`, который предназначен для обработки списка идентификаторов продуктов AliExpress или URL-адресов и возврата списка продуктов с партнерскими ссылками и сохраненными изображениями.

Шаги выполнения
-------------------------
1. **Получение списка партнерских ссылок**: Метод `get_affiliate_links` из базового класса `AliApi` вызывается для получения списка партнерских ссылок для каждого предоставленного идентификатора продукта или URL-адреса.
2. **Извлечение данных о продукте**: Если найдены партнерские ссылки, метод `retrieve_product_details` вызывается для получения подробных данных о продукте из AliExpress API.
3. **Сохранение изображений и видео**: Для каждого продукта сохраняются изображения и видео (если они есть).
4. **Сохранение данных о продукте**: Данные о продукте, включая партнерские ссылки, сохраненные пути к изображениям и видео, а также другие атрибуты, сохраняются в файл JSON.
5. **Возврат списка обработанных продуктов**: Метод возвращает список обработанных продуктов в формате `SimpleNamespace`.


Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.affiliated_products_generator import AliAffiliatedProducts

# Инициализация объекта AliAffiliatedProducts
affiliated_products = AliAffiliatedProducts(language='EN', currency='USD')

# Список идентификаторов продуктов
prod_ids = ['1000000000', '2000000000', '3000000000']

# Каталог для сохранения данных
category_root = Path('/path/to/category/root')

# Вызов метода process_affiliate_products
products = asyncio.run(affiliated_products.process_affiliate_products(prod_ids, category_root))

# Печать результатов
for product in products:
    print(product.product_title)
    print(product.promotion_link)
    print(product.local_image_path)
    print(product.local_video_path)
```