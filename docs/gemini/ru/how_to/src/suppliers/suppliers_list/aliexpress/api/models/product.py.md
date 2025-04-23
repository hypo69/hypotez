### **Как использовать этот блок кода**

=========================================================================================

Описание
-------------------------
Этот блок кода определяет класс `Product`, который представляет модель данных товара с AliExpress. Он содержит атрибуты, описывающие различные характеристики товара, такие как цены, комиссии, изображения, ссылки и категории.

Шаги выполнения
-------------------------
1. **Импорт модуля `List`**: Импортируется модуль `List` из библиотеки `typing` для аннотации типов, указывающей, что атрибут `product_small_image_urls` является списком строк.
2. **Определение класса `Product`**: Определяется класс `Product` без явного конструктора (`__init__`). Это означает, что атрибуты класса будут устанавливаться непосредственно при создании экземпляра класса.
3. **Определение атрибутов класса**: Для каждого атрибута товара определены аннотации типов, такие как `str` для строковых значений и `int` для целочисленных. Атрибуты включают:
    - `app_sale_price` (цена со скидкой в приложении)
    - `app_sale_price_currency` (валюта цены со скидкой в приложении)
    - `commission_rate` (комиссионный процент)
    - `discount` (скидка)
    - `evaluate_rate` (оценка)
    - `first_level_category_id` (ID категории первого уровня)
    - `first_level_category_name` (название категории первого уровня)
    - `lastest_volume` (последний объем)
    - `hot_product_commission_rate` (комиссионный процент для популярных товаров)
    - `original_price` (оригинальная цена)
    - `original_price_currency` (валюта оригинальной цены)
    - `product_detail_url` (URL страницы с деталями товара)
    - `product_id` (ID товара)
    - `product_main_image_url` (URL главного изображения товара)
    - `product_small_image_urls` (список URL маленьких изображений товара)
    - `product_title` (название товара)
    - `product_video_url` (URL видео товара)
    - `promotion_link` (ссылка на акцию)
    - `relevant_market_commission_rate` (комиссионный процент для релевантного рынка)
    - `sale_price` (цена со скидкой)
    - `sale_price_currency` (валюта цены со скидкой)
    - `second_level_category_id` (ID категории второго уровня)
    - `second_level_category_name` (название категории второго уровня)
    - `shop_id` (ID магазина)
    - `shop_url` (URL магазина)
    - `target_app_sale_price` (целевая цена со скидкой в приложении)
    - `target_app_sale_price_currency` (валюта целевой цены со скидкой в приложении)
    - `target_original_price` (целевая оригинальная цена)
    - `target_original_price_currency` (валюта целевой оригинальной цены)
    - `target_sale_price` (целевая цена со скидкой)
    - `target_sale_price_currency` (валюта целевой цены со скидкой)

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.api.models import Product

# Создание экземпляра класса Product
product = Product()
product.product_title = "Awesome Gadget"
product.sale_price = "25.00"
product.sale_price_currency = "USD"
product.product_small_image_urls = ["http://example.com/image1.jpg", "http://example.com/image2.jpg"]

# Доступ к атрибутам экземпляра класса
print(f"Product Title: {product.product_title}")
print(f"Sale Price: {product.sale_price} {product.sale_price_currency}")
print(f"Small Image URLs: {product.product_small_image_urls}")