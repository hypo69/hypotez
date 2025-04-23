### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Этот блок кода отвечает за добавление товара в базу данных PrestaShop, если товара еще нет в базе. Он также обрабатывает случай, когда товар уже существует в базе данных, обновляя его изображение.

Шаги выполнения
-------------------------
1. **Определение ASIN и product_reference**: Извлекается ASIN товара со страницы и формируется уникальный идентификатор товара (`product_reference`).
2. **Проверка наличия товара в базе данных**: С использованием `Product.check_if_product_in_presta_db` проверяется, существует ли товар с данным `product_reference` в базе данных PrestaShop. Результат сохраняется в `product_id`.
3. **Обработка случая, когда товар уже существует в базе данных**:
   - Если `product_id` не является `False` (то есть товар найден в базе данных), извлекается URL изображения товара (`default_image_url`).
   - Вызывается метод `Product.upload_image2presta` для обновления изображения товара в PrestaShop.
4. **Обработка случая, когда товара нет в базе данных**:
   - Если `product_id` является `False` (то есть товар не найден в базе данных), вызывается метод `Product.grab_product_page` для сбора информации о товаре со страницы.
   - Формируется словарь `product_dict` с информацией о товаре.
   - Извлекается название товара (`product_name`) и очищается от лишних символов.
   - Название товара присваивается полю `name` в словаре `product_dict`.
   - Выводится словарь `product_dict` для отладки.

Пример использования
-------------------------

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

defaul_image_url = _(l['additional_images_urls'])[0]

if not isinstance(product_id, bool):
    """ Если не вернулся False, значит товар уже в бд, я полуну его id_product
    здесь обработка product_update
    """
    Product.upload_image2presta(image_url = defaul_image_url, product_id = product_id)
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
    product_dict['product']['name'] = res_product_name.strip("\'").strip('\"').strip('\n')
    pprint(product_dict)
    #pprint(PrestaProduct.add(product_dict))