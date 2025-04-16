### **Анализ кода модуля `test_1_murano_glass_scenario.py`**

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код достаточно структурирован и логичен.
    - Используются аннотации типов.
    - Присутствуют комментарии, описывающие некоторые участки кода.
- **Минусы**:
    - Не все функции и классы документированы в соответствии с требуемым форматом.
    - Присутствуют неинформативные комментарии и дублирование платформ.
    - Используется `print` для отладочной информации, вместо `logger`.
    - Есть устаревшие и повторяющиеся комментарии.
    - Не все переменные аннотированы типами.
    - Используется `Union` вместо `|`.

**Рекомендации по улучшению:**

1.  **Документирование кода**:
    *   Добавить docstring к каждой функции, включая внутренние, с подробным описанием аргументов, возвращаемых значений и возможных исключений.
    *   Обеспечить, чтобы все docstring были на русском языке и в формате UTF-8.

2.  **Логирование**:
    *   Заменить все вызовы `print` на использование модуля `logger` для информационных и отладочных сообщений.
    *   При обработке исключений использовать `logger.error` с передачей информации об ошибке (`ex`) и трассировки (`exc_info=True`).

3.  **Типизация**:
    *   Убедиться, что все переменные и параметры функций аннотированы типами.

4.  **Комментарии**:
    *   Удалить устаревшие, повторяющиеся и неинформативные комментарии.
    *   Перефразировать неясные комментарии, используя более точные и понятные формулировки.
    *   Пример: Вместо "Если не вернулся False, значит товар уже в бд" лучше написать: "Если `product_id` не равен `False`, это означает, что товар уже существует в базе данных PrestaShop".

5.  **Обработка строк**:
    *   Использовать f-строки для форматирования строк, где это уместно, чтобы улучшить читаемость.
    *   Избегать многократного вызова методов `strip` для удаления символов, можно использовать один вызов с перечислением всех символов.

6. **Улучшение импортов**:
   *   Убедиться, что все импортированные модули и классы используются в коде.
   *   Удалить неиспользуемые импорты.

7. **Использовать `|` вместо `Union`**
    *   Вместо `Union[str, int]` используйте `str | int`.

**Оптимизированный код:**

```python
## \file /src/suppliers/amazon/_experiments/scenarois/all_scenarios_from_amazon/murano_glass/test_1_murano_glass_scenario.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для Murano Glass сценария на Amazon
==============================================

Модуль содержит логику для извлечения и обработки информации о товарах Murano Glass с сайта Amazon,
а также для добавления или обновления этих товаров в базе данных PrestaShop.
"""

from pathlib import Path
from typing import Union, Optional

from header import logger, pprint
from header import StringNormalizer, StringFormatter
from header import Product, ProductFields, Supplier, Driver
from header import PrestaAPIV1, PrestaAPIV2, upload_image
from header import start_supplier

supplier_prefix: str = 'amazon'
s: Supplier = start_supplier(supplier_prefix)
""" s - на протяжении всего кода означает класс `Supplier` """

logger.info("Начинаем сценарий Murano Glass")

s.current_scenario: dict = {
    "url": "https://amzn.to/3OhRz2g",
    "condition": "new",
    "presta_categories": {
        "default_category": {"11209": "MURANO GLASS"},
        "additional_categories": [""]
    },
    "price_rule": 1
}
l: dict = s.locators.get('product')
d: Driver = s.driver
_: callable = d.execute_locator

# test_url_4 = r"https://www.amazon.com/C%C3%A1-dOro-Hippie-Colored-Murano-Style/dp/B09N53XSQB/ref=sr_1_1_sspa?crid=24Q0ZZYVNOQMP&keywords=Art+Deco+murano+glass&qid=1687277030&sprefix=art+deco+murano+glass%2Caps%2C230&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"
# test_url_5 = r"https://www.amazon.com/Luxury-Lane-Sommerso-Centerpiece-Decoration/dp/B0BSZBF8NJ/ref=sr_1_3_sspa?c=ts&keywords=Vases&qid=1688326048&s=furniture&sr=1-3-spons&ts_id=3745451&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1"

d.get_url(s.current_scenario['url'])

ASIN: str = _(l['ASIN'])

product_reference: str = f"{s.supplier_id}-{ASIN}"
product_id: Union[int, bool] = Product.check_if_product_in_presta_db(product_reference)
logger.info(f"Проверка наличия товара в базе данных PrestaShop. ID товара: {product_id}")

default_image_url: str = _(l['additional_images_urls'])[0]

if not isinstance(product_id, bool):
    """ Если `product_id` не равен `False`, это означает, что товар уже существует в базе данных PrestaShop """
    Product.upload_image2presta(image_url=default_image_url, product_id=product_id)
    ...

else:
    product_fields: ProductFields = Product.grab_product_page(s)

    product_dict: dict = {}
    product_dict['product']: dict = dict(product_fields.fields)
    # product_dict['product']['wholesale_price'] = product_dict['product']['price'] = float(product_dict['product']['wholesale_price'])
    #
    product_name: list[str] = _(l['name'])

    res_product_name: str = ''.join(product_name)
    product_dict['product']['name'] = res_product_name.strip("\'\"\\n")
    pprint(product_dict)
    # pprint(PrestaProduct.add(product_dict))