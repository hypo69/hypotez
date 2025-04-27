## Как использовать класс `Aliexpress`
=========================================================================================

Описание
-------------------------
Класс `Aliexpress` объединяет в себе функциональность классов `Supplier`, `AliRequests` и `AliApi` для работы с AliExpress. Он предоставляет удобный интерфейс для взаимодействия с AliExpress, позволяя использовать различные режимы: 
- без веб-драйвера (по умолчанию), 
- с веб-драйвером (Chrome, Mozilla, Edge, default), 
- в режиме `Requests`.

Шаги выполнения
-------------------------
1. **Инициализация класса `Aliexpress`**:
    - При создании экземпляра класса `Aliexpress` можно указать режим работы:
        - `webdriver = False`: без веб-драйвера.
        - `webdriver = 'chrome'`: использование веб-драйвера Chrome.
        - `webdriver = 'mozilla'`: использование веб-драйвера Mozilla.
        - `webdriver = 'edge'`: использование веб-драйвера Edge.
        - `webdriver = 'default'`: использование системного веб-драйвера по умолчанию.
        - `requests = True`: использование режима `Requests` для работы с API.
    - Установка языка и валюты:
        - `locale = {'EN': 'USD'}` - язык английский, валюта - доллар США. Можно использовать словарь или строку, например: `locale = 'EN'`.
2. **Использование методов**:
    - После инициализации объекта `Aliexpress` можно использовать методы, наследуемые от `Supplier`, `AliRequests` и `AliApi`, например:
        - `search_products()`: поиск товаров.
        - `get_product_details()`: получение информации о товаре.
        - `get_product_reviews()`: получение отзывов о товаре.
        - `get_product_images()`: получение изображений товара.
        - `get_product_variations()`: получение вариаций товара.
        - `get_product_shipping()`: получение информации о доставке товара.
        - `get_product_price()`: получение цены товара.
        - `get_product_availability()`: получение информации о наличии товара.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.aliexpress import Aliexpress

# Run without a webdriver
a = Aliexpress()

# Webdriver Chrome
a = Aliexpress(webdriver='chrome')

# Requests mode
a = Aliexpress(requests=True)

# Search for products
results = a.search_products(query='iphone', page=1)

# Get product details
product = a.get_product_details(product_id='1234567890')

# Get product reviews
reviews = a.get_product_reviews(product_id='1234567890', page=1)

# Print results
print(results)
print(product)
print(reviews)
```