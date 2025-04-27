## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код представляет собой класс `AliexpressApi`, который является оберткой для AliExpress API. Класс предоставляет методы для извлечения информации о продуктах, генерации партнерских ссылок, поиска товаров с высокой комиссией и получения категорий продуктов. 

Шаги выполнения
-------------------------
1. **Инициализация класса:**
    - Для использования API необходимо создать экземпляр класса `AliexpressApi`, передав API ключ, API секрет, код языка, код валюты и необязательный идентификатор отслеживания (tracking_id). 
    - В конструкторе класса устанавливаются необходимые параметры, такие как ключ, секрет, язык, валюта, идентификатор отслеживания и приложение для API.

2. **Извлечение данных о продуктах (retrieve_product_details):**
    - Метод `retrieve_product_details` позволяет получить информацию о продуктах AliExpress по их ID или URL-адресам. 
    - Можно указать поля, которые необходимо включить в результаты, а также страну для фильтрации продуктов. 

3. **Генерация партнерских ссылок (get_affiliate_links):**
    - Метод `get_affiliate_links` генерирует партнерские ссылки для заданных URL-адресов.
    - Можно выбрать тип ссылки: стандартная ссылка или ссылка на популярный продукт. 
    - Для этого необходимо передать параметр `link_type`, который может принимать значение `model_LinkType.NORMAL` или `model_LinkType.HOTLINK`.

4. **Поиск товаров с высокой комиссией (get_hotproducts):**
    - Метод `get_hotproducts` позволяет найти популярные продукты с высокой комиссией. 
    - Метод принимает ряд параметров для фильтрации товаров, таких как идентификаторы категорий, количество дней доставки, диапазон цен, ключевые слова и другие. 

5. **Получение категорий (get_categories):**
    - Метод `get_categories` возвращает список всех доступных категорий, как родительских, так и дочерних. 

6. **Получение родительских категорий (get_parent_categories):**
    - Метод `get_parent_categories` возвращает список всех родительских категорий. 

7. **Получение дочерних категорий (get_child_categories):**
    - Метод `get_child_categories` возвращает список дочерних категорий для конкретной родительской категории.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.api.api import AliexpressApi
from src.suppliers.suppliers_list.aliexpress.api.models import Language, Currency, LinkType

# Создаем экземпляр класса AliexpressApi
api = AliexpressApi(
    key="YOUR_API_KEY",
    secret="YOUR_API_SECRET",
    language=Language.EN,
    currency=Currency.USD,
    tracking_id="YOUR_TRACKING_ID"
)

# Получаем информацию о продукте по ID
product_id = '123456789'
product_details = api.retrieve_product_details(product_id)
print(product_details)

# Создаем партнерскую ссылку
link = 'https://www.aliexpress.com/item/123456789.html'
affiliate_links = api.get_affiliate_links(link)
print(affiliate_links)

# Поиск товаров с высокой комиссией
hotproducts = api.get_hotproducts(
    category_ids='123456789',
    min_sale_price=100,
    max_sale_price=1000,
    keywords='smartwatch'
)
print(hotproducts)

# Получение всех доступных категорий
categories = api.get_categories()
print(categories)

# Получение родительских категорий
parent_categories = api.get_parent_categories()
print(parent_categories)

# Получение дочерних категорий для родительской категории с ID 123456789
child_categories = api.get_child_categories(parent_category_id=123456789)
print(child_categories)
```