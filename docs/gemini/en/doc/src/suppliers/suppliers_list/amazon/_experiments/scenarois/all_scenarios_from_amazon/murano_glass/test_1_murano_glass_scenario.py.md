# Тестовый сценарий для товара из Murano glass на Amazon

## Обзор

Этот модуль содержит тестовый сценарий для извлечения данных о товаре из Murano glass на Amazon. 
Сценарий демонстрирует процесс получения информации о товаре, его загрузку в базу данных PrestaShop 
и последующую обработку.

## Детали

Сценарий использует класс `Supplier` для работы с Amazon. В коде используются методы `driver.execute_locator` 
для получения данных с помощью Selenium и `Product.grab_product_page` для извлечения информации о товаре. 
Затем данные обрабатываются и сохраняются в словарь `product_dict`, который в дальнейшем используется для 
загрузки товара в PrestaShop.

## Классы

### `Supplier`

**Описание**: Класс `Supplier` предоставляет функциональность для работы с конкретным поставщиком 
(в данном случае Amazon). 

**Атрибуты**:

- `supplier_id` (str): Идентификатор поставщика.
- `current_scenario` (dict): Текущий сценарий для поставщика.
- `locators` (dict): Словарь с локаторами для элементов веб-страницы.
- `driver` (Driver): Экземпляр класса `Driver`, который используется для взаимодействия с браузером.

**Методы**:

- `start_supplier()`:  Функция для создания экземпляра класса `Supplier` и установки необходимых параметров.
- `get_url()`:  Функция для открытия URL-адреса в браузере.
- `execute_locator()`:  Функция для получения данных по локатору с помощью Selenium.


### `Product`

**Описание**: Класс `Product` предоставляет функциональность для работы с товарами.

**Атрибуты**:

- `product_id` (int | bool): Идентификатор товара в базе данных PrestaShop, `False` если товар отсутствует.

**Методы**:

- `check_if_product_in_presta_db()`:  Функция для проверки наличия товара в базе данных PrestaShop по идентификатору.
- `grab_product_page()`:  Функция для извлечения информации о товаре с веб-страницы.
- `upload_image2presta()`:  Функция для загрузки изображения товара в PrestaShop.

## Функции

### `start_supplier`

**Цель**: Создание экземпляра класса `Supplier` и инициализация его атрибутов.

**Параметры**:

- `supplier_prefix` (str): Префикс идентификатора поставщика.

**Возвращает**:

- `Supplier`: Экземпляр класса `Supplier`.

**Пример**:

```python
supplier_prefix = 'amazon'
s = start_supplier(supplier_prefix)
```


## Пример кода

```python
from pathlib import Path
from typing import Union

import header
from header import logger,   pprint
from header import StringNormalizer, StringFormatter
from header import Product, ProductFields, Supplier, Driver
from header import PrestaAPIV1,PrestaAPIV2, PrestaAPIV2, upload_image
from header import start_supplier
supplier_prefix = 'amazon'
s = start_supplier(supplier_prefix)
""" s - на протяжении всего кода означает класс `Supplier` """

print(" Можно продолжать ")

s.current_scenario: dict = {
      "url": "https://amzn.to/3OhRz2g",
      "condition": "new",
      "presta_categories": {
        "default_category": { "11209": "MURANO GLASS" },
        "additional_categories": [ "" ]
      },
      "price_rule": 1
    }
l = s.locators.get('product')
d = s.driver
_ = d.execute_locator

# test_url_4 = r"https://www.amazon.com/C%C3%A1-dOro-Hippie-Colored-Murano-Style/dp/B09N53XSQB/ref=sr_1_1_sspa?crid=24Q0ZZYVNOQMP&keywords=Art+Deco+murano+glass&qid=1687277030&sprefix=art+deco+murano+glass%2Caps%2C230&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"
# test_url_5 = r"https://www.amazon.com/Luxury-Lane-Sommerso-Centerpiece-Decoration/dp/B0BSZBF8NJ/ref=sr_1_3_sspa?c=ts&keywords=Vases&qid=1688326048&s=furniture&sr=1-3-spons&ts_id=3745451&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1"

d.get_url(s.current_scenario['url'])



ASIN = _(l['ASIN'])


product_reference = f"{s.supplier_id}-{ASIN}"
product_id = Product.check_if_product_in_presta_db(product_reference)
print(f' Если товар в бд получу id_product, иначе False. Получил: {product_id}')

default_image_url = _(l['additional_images_urls'])[0]

if not isinstance(product_id, bool):
    """ Если не вернулся False, значит товар уже в бд, я полуну его id_product
    здесь обработка product_update
    """
    Product.upload_image2presta(image_url = default_image_url, product_id = product_id)
    ...

else:
    product_fields: ProductFields = Product.grab_product_page(s)

   
    product_dict: dict = {}
    product_dict['product']: dict = dict(product_fields.fields)
    #product_dict['product']['wholesale_price'] = product_dict['product']['price'] = float(product_dict['product']['wholesale_price'] )
    #
    product_name = _(l['name'])[0]
    
    res_product_name = ''
    for n in product_name:
        res_product_name += n
    product_dict['product']['name'] = res_product_name.strip("\'").strip('\'"\').strip('\n')
    pprint(product_dict)
    #pprint(PrestaProduct.add(product_dict))
```