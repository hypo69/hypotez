### Как использовать класс `AliexpressApi`
=========================================================================================

Описание
-------------------------
Класс `AliexpressApi` предоставляет интерфейс для взаимодействия с API AliExpress, позволяя получать информацию о товарах, категориях и создавать партнерские ссылки.

Шаги выполнения
-------------------------
1. **Инициализация класса**: Создайте экземпляр класса `AliexpressApi`, передав необходимые параметры аутентификации и настройки.
2. **Получение информации о товарах**: Вызовите метод `retrieve_product_details` для получения детальной информации о товарах по их ID.
3. **Создание партнерских ссылок**: Используйте метод `get_affiliate_links` для генерации партнерских ссылок на товары.
4. **Получение списка горячих товаров**: Вызовите метод `get_hotproducts` для поиска товаров с высокой комиссией.
5. **Получение категорий**: Используйте методы `get_categories`, `get_parent_categories` и `get_child_categories` для получения списка категорий товаров.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.api.api import AliexpressApi
from src.suppliers.suppliers_list.aliexpress.api.models import Language, Currency, LinkType

# Параметры аутентификации и настройки
api_key = "your_api_key"
api_secret = "your_api_secret"
language = Language.RU  # или другой поддерживаемый язык
currency = Currency.RUB  # или другая поддерживаемая валюта
tracking_id = "your_tracking_id"  # Обязателен для создания партнерских ссылок

# Инициализация API
aliexpress_api = AliexpressApi(
    key=api_key,
    secret=api_secret,
    language=language,
    currency=currency,
    tracking_id=tracking_id
)

# Получение информации о товарах
product_ids = ["1234567890", "0987654321"]
products = aliexpress_api.retrieve_product_details(product_ids=product_ids)
if products:
    print(f"Информация о товарах: {products}")

# Создание партнерских ссылок
links = ["https://aliexpress.com/item/1234567890.html", "https://aliexpress.com/item/0987654321.html"]
affiliate_links = aliexpress_api.get_affiliate_links(links=links, link_type=LinkType.HOTLINK)
if affiliate_links:
    print(f"Партнерские ссылки: {affiliate_links}")

# Получение списка горячих товаров
hot_products = aliexpress_api.get_hotproducts(category_ids=["200000348"])
if hot_products:
    print(f"Список горячих товаров: {hot_products.products}")

# Получение категорий
categories = aliexpress_api.get_categories()
if categories:
    print(f"Список категорий: {categories}")

# Получение родительских категорий
parent_categories = aliexpress_api.get_parent_categories()
if parent_categories:
    print(f"Родительские категории: {parent_categories}")

# Получение дочерних категорий для родительской категории с ID 2
child_categories = aliexpress_api.get_child_categories(parent_category_id=2)
if child_categories:
    print(f"Дочерние категории: {child_categories}")