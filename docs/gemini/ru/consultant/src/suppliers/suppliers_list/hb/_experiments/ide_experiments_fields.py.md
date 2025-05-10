### **Анализ кода модуля `ide_experiments_fields.py`**

**Расположение файла в проекте:** `/src/suppliers/hb/_experiments/ide_experiments_fields.py`

**Назначение модуля:** Файл предназначен для экспериментов по наполнению полей товара (`product_fields`) для поставщика HB. Он собирает данные о товаре со страницы и преобразует их в формат, пригодный для добавления или обновления информации о товаре в системе PrestaShop.

**Качество кода:**
- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код структурирован по функциям, что облегчает понимание и поддержку.
    - Используются аннотации типов, что улучшает читаемость и помогает в отладке.
    - Присутствуют комментарии, объясняющие назначение отдельных блоков кода.
- **Минусы**:
    - Много устаревших и неинформативных комментариев, таких как `@details`.
    - Некоторые функции содержат много логики и требуют рефакторинга для улучшения читаемости.
    - Не все функции имеют docstring, что затрудняет понимание их назначения и использования.
    - Использование `global` переменных может привести к проблемам с состоянием и усложняет отладку.
    - Смешаны стили форматирования (использование `Union` вместо `|`).

**Рекомендации по улучшению:**

1. **Общее**:
    - Добавить docstring ко всем функциям, чтобы объяснить их назначение, параметры и возвращаемые значения.
    - Избегать использования `global` переменных. Вместо этого передавать необходимые параметры функциям.
    - Заменить `Union` на `|` в аннотациях типов.
    - Убрать все лишние и неинформативные комментарии, такие как `@details`.
    - Привести код в соответствие со стандартами PEP8.
    - Добавить обработку исключений с логированием ошибок через `logger.error`.

2. **`grab_product_page`**:
    - Разбить функцию на более мелкие, чтобы каждая выполняла одну конкретную задачу.
    - Убрать `global` переменные `s`, `p`, `f`, `l` и передавать их как аргументы в вызываемые функции.
    - Добавить обработку ошибок при выполнении локаторов.

3. **`product_reference_and_volume_and_price_for_100`**:
    - Добавить обработку случая, когда ни одно из условий `if/elif` не выполняется.
    - Улучшить читаемость, вынеся логику из цикла `for` в отдельные функции.
    - Заменить `print` на `logger.info` для логирования цены за единицу товара.

4. **Функции для полей**:
    - Добавить docstring для каждой функции, чтобы объяснить, какое поле она заполняет и какие данные ожидает.
    - Унифицировать стиль возвращаемых значений (например, всегда возвращать строку или число, а не `WebElement`).

5. **`get_price`**:
    - Убрать `asyncio.run` и использовать `await` для асинхронного выполнения локатора, если это необходимо.
    - Улучшить обработку исключений, чтобы логировать конкретную ошибку.

**Оптимизированный код:**

```python
## \file /src/suppliers/hb/_experiments/ide_experiments_fields.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для экспериментов по наполнению полей товара для поставщика HB.
=======================================================================

Модуль собирает данные о товаре со страницы и преобразует их в формат,
пригодный для добавления или обновления информации о товаре в системе PrestaShop.

.. module:: src.suppliers.hb._experiments
"""

import os
import sys
from pathlib import Path
from typing import List, Union, Dict, Optional

from selenium.webdriver.remote.webelement import WebElement

# Добавление корневой директории позволяет мне плясать от печки
dir_root: Path = Path(os.getcwd()[:os.getcwd().rfind("hypotez") + 7])
sys.path.append(str(dir_root))  # Adding the root folder to sys.path
dir_src = Path(dir_root, 'src')
sys.path.append(str(dir_root))

from src.webdriver import executor
# Добавление корневой директории позволяет мне плясать от печки.
from src import gs
from src.product import Product, ProductFields
from src.logger.logger import logger
from src.webdriver.driver import Driver
from src.utils import StringFormatter, StringNormalizer
from src.supplier import Supplier


def grab_product_page(supplier: Supplier, async_run: bool = True) -> ProductFields:
    """
    Собирает со страницы товара значения веб-элементов и приводит их к полям ProductFields.

    Args:
        supplier (Supplier): Класс поставщика. Веб-драйвер должен быть установлен на странице товара.
        async_run (bool): Флаг для асинхронного запуска.

    Returns:
        ProductFields: Заполненные поля товара.
    """
    s: Supplier = supplier
    p: Product = Product(s)
    f: ProductFields = ProductFields(s)
    d: Driver = s.driver
    l: Dict = s.locators["product"]

    s.current_scenario: Dict = {
        "url": "https://hbdeadsea.co.il/product-category/bodyspa/feet-hand-treatment/",
        "name": "טיפוח כפות ידיים ורגליים",
        "condition": "new",
        "presta_categories": {
            "default_category": 11259,
            "additional_categories": []
        }
    }

    d.get_url(s.current_scenario['url'])
    d.wait(5)
    d.execute_locator(l["close_banner"])  # Закрываю баннер
    d.scroll()  # Прокручиваю страницу товара, чтобы захватить области, которые подгружаются через AJAX

    def product_reference_and_volume_and_price_for_100(driver: Driver, locators: Dict, product_fields: ProductFields) -> None:
        """
        Извлекает объем, артикул поставщика и цену за единицу товара.

        Args:
            driver (Driver): Инстанс веб-драйвера.
            locators (Dict): Локаторы элементов на странице.
            product_fields (ProductFields): Объект для хранения полей товара.
        """
        webelements: List[WebElement] = driver.execute_locator(locators["product_reference_and_volume_and_price_for_100"])

        for webelement in webelements:
            text: str = webelement.text
            if 'Fl.oz' in text and 'מ"ל' in text:
                # Объем
                product_fields.volume = text
            elif 'מחיר ל100 מ"ל' in text:
                # Цена за единицу товара
                price_per_unit: str = text
                logger.info(f'Цена за единицу товара: {price_per_unit}')
            elif 'מקט' in text:
                # Артикул поставщика
                product_fields.supplier_reference = StringNormalizer.get_numbers_only(text)

    def set_references(supplier_id: int, supplier_reference: str, product_fields: ProductFields) -> None:
        """
        Устанавливает идентификаторы товара.

        Args:
            supplier_id (int): ID поставщика.
            supplier_reference (str): Артикул поставщика.
            product_fields (ProductFields): Объект для хранения полей товара.
        """
        product_fields.id_supplier = int(supplier_id)
        product_fields.reference = f'{supplier_id}-{supplier_reference}'

    product_reference_and_volume_and_price_for_100(d, l, f)
    set_references(s.supplier_id, f.supplier_reference, f)

    f.additional_shipping_cost = field_additional_shipping_cost(d, l)
    f.affiliate_short_link = field_affiliate_short_link(d)
    f.available_for_order = f.active = field_available_for_order(d, l, f)
    f.condition = field_condition(d, l)

    _images_urls: list = d.execute_locator(l["additional_images_urls"])
    if len(_images_urls) > 0:
        f.assist_fields_dict['default_image_url'] = _images_urls[0]
    if len(_images_urls) > 1:
        f.assist_fields_dict['images_urls'] = _images_urls[1::]

    f.description_short = f.description = field_description(d, l)
    f.how_to_use = field_how_to_use(d, l)
    f.id_category_default = field_id_category_default(s)
    f.id_manufacturer = field_id_manufacturer(d, l)
    f.ingredients = field_ingredients(d, l)

    _name: list = d.execute_locator(l["name"])  # Чтобы два раза не бегать, Я получаю значение локатора в _name
    f.name = field_name(_name[0])  # А потом использую для f.name
    f.link_rewrite = field_link_rewrite(_name[0])  # И для f.link_rewrite

    f.on_sale = field_on_sale(d, l)
    f.price = field_price(d, l)
    f.visibility = field_visibility(d, l)

    return f


def field_additional_shipping_cost(driver: Driver, locators: Dict) -> str:
    """
    Возвращает стоимость доставки.
    """
    return driver.execute_locator(locators["additional_shipping_cost"])


def field_delivery_in_stock(driver: Driver, locators: Dict) -> str:
    """
    Возвращает информацию о доставке, когда товар в наличии.
    """
    return str(driver.execute_locator(locators["delivery_in_stock"]))


def field_active(product_fields: ProductFields) -> int:
    """
    Возвращает активность товара. Зависит от delivery_out_stock.
    """
    return product_fields.active


def field_affiliate_short_link(driver: Driver) -> str:
    """
    Возвращает короткую партнерскую ссылку.
    """
    return driver.current_url


def field_available_for_order(driver: Driver, locators: Dict, product_fields: ProductFields) -> int:
    """
    Определяет, доступен ли товар для заказа.
    Если вернулся веб-элемент, это флаг, что товара нет в наличии.
    """
    available_for_order = driver.execute_locator(locators["available_for_order"])

    if available_for_order is None:
        product_fields.available_for_order = 1
    else:
        product_fields.available_for_order = 0
        product_fields.active = 0

    return product_fields.available_for_order


def field_condition(driver: Driver, locators: Dict) -> str:
    """
    Возвращает состояние товара.
    """
    return driver.execute_locator(locators["condition"])


def field_description(driver: Driver, locators: Dict) -> str:
    """
    Возвращает полное описание товара.
    """
    description_element: list = driver.execute_locator(locators["description"])
    if description_element:
        return description_element[0].text
    return ""


def field_id_category_default(supplier: Supplier) -> int:
    """
    Возвращает главную категорию товара. Берется из сценария.
    """
    return supplier.current_scenario["presta_categories"]["default_category"]


def field_how_to_use(driver: Driver, locators: Dict) -> str:
    """
    Возвращает информацию о том, как использовать товар.
    """
    how_to_use_elements: list = driver.execute_locator(locators["how_to_use"])
    if how_to_use_elements:
        return how_to_use_elements[0].text
    return ""


def field_id_manufacturer(driver: Driver, locators: Dict) -> str:
    """
    Возвращает ID бренда. Может быть и названием бренда - престашоп сам разберется.
    """
    return driver.execute_locator(locators["id_manufacturer"])


def field_ingredients(driver: Driver, locators: Dict) -> str:
    """
    Возвращает состав товара. Забираю с сайта HTML с картинками ингредиентов.
    """
    ingredients_elements: list = driver.execute_locator(locators["ingredients"])
    if ingredients_elements:
        return ingredients_elements[0].text
    return ""


def field_link_rewrite(product_name: str) -> str:
    """
    Создает ссылку перезаписи из названия товара.
    """
    return StringNormalizer.normalize_link_rewrite(product_name)


def field_name(name: str) -> str:
    """
    Возвращает название товара, очищенное от лишних параметров.
    """
    return StringNormalizer.normalize_product_name(name)


def field_online_only(driver: Driver, locators: Dict) -> str:
    """
    Возвращает флаг, указывающий, что товар доступен только в интернет-магазине.
    """
    return driver.execute_locator(locators['online_only'])


def field_on_sale(driver: Driver, locators: Dict) -> str:
    """
    Возвращает флаг, указывающий, что товар на распродаже.
    """
    return driver.execute_locator(locators['on_sale'])


def field_out_of_stock(driver: Driver, locators: Dict) -> str:
    """
    Возвращает флаг, указывающий, что товара нет в наличии.
    """
    return driver.execute_locator(locators["out_of_stock"])


def field_price(driver: Driver, locators: Dict) -> str:
    """
    Возвращает цену товара.
    """
    price_elements: list = driver.execute_locator(locators["price"])
    if price_elements:
        return StringNormalizer.normalize_price(price_elements[0])
    return ""


def field_visibility(driver: Driver, locators: Dict) -> str:
    """
    Возвращает видимость товара.
    """
    return driver.execute_locator(locators["visibility"])


async def get_price(_d: Driver, _l: Dict) -> str | float | None:
    """
    Извлекает и нормализует цену товара.

    Args:
        _d (Driver): Инстанс веб-драйвера.
        _l (Dict): Локаторы элементов на странице.

    Returns:
        str | float | None: Нормализованная цена товара или None в случае ошибки.
    """
    try:
        # raw_price = asyncio.run ( _d.execute_locator ( _l ["price"]["new"] )[0])
        raw_price = await _d.execute_locator(_l["price"]["new"]) if gs.async_run else _d.execute_locator(_l["price"]["new"])[0]
        ''' raw_price получаю в таком виде:
        ILS382.00\nILS382\n.\n00
        '''
        raw_price = str(raw_price).split('\n')[0]
        return StringNormalizer.normalize_price(raw_price)
    except Exception as ex:
        logger.error('Ошибка при получении цены товара', ex, exc_info=True)
        return None


def specification():
    f["product_specification"] = f["description"]


def summary():
    f["summary"] = f["description"]


def delivery():
    shipping_price = _d.execute_locator(_l["shipping_price_locator"])
    if 'Free Shipping' in shipping_price:
        f["shipping price"] = 0
        return True
    f["shipping price"] = StringFormatter.clear_price(shipping_price)
    return True


def link():
    f["link_to_product"] = _d.current_url.split('?')[0]


def images():
    _http_server = f'''http://davidka.esy.es/supplier_imgs/{s.supplier_prefix}'''
    _img_name = f'''{f["sku"]}.png'''
    f["img url"] = f'''{_http_server}/{_img_name}'''
    screenshot = _d.execute_locator(_l["main_image_locator"])
    s.save_and_send_viaftp({_img_name: screenshot})


def qty():
    try:
        _qty = _d.execute_locator(_l["qty_locator"])[0]
        f["qty"] = StringFormatter.clear_price(_qty)
        f["tavit im bemlay"] = f["qty"]
        return True
    except Exception as ex:
        logger.error('Ошибка при получении количества товара', ex, exc_info=True)
        return None


def byer_protection():
    try:
        f["product_byer_protection"] = str(_d.execute_locator(_l["byer_protection_locator"]))
        return True
    except Exception as ex:
        f["product_byer_protection"] = None
        logger.error('Ошибка при получении информации о защите покупателя', ex, exc_info=True)
        return None


def customer_reviews():
    try:
        f["product_customer_reviews"] = _d.execute_locator(_l["customer_reviews_locator"])
    except Exception as ex:
        f["product_customer_reviews"] = None
        logger.error('Ошибка при получении отзывов клиентов', ex, exc_info=True)
        return None


def rewritted_URL():
    f["Rewritten URL"] = f["id"]


# Далее идет использование функций для сбора и обработки информации о товаре
# s: Supplier = Supplier(supplier_prefix='hb')
# p: Product = Product(s)
# l: Dict = s.locators["product"]
# d: Driver = s.driver
# f: ProductFields = ProductFields(s)
s: Supplier = Supplier(supplier_prefix='hb')
product_fields: ProductFields = grab_product_page(s)

presta_fields_dict: Dict = {key: value for key, value in product_fields.presta_fields_dict.items() if value}
# Убираю пустые ключи из словаря

if 'quantity' in presta_fields_dict:
    del presta_fields_dict['quantity']
# `quantity` нельзя задавать при добавлении нового товара

assist_fields_dict: Dict = product_fields.assist_fields_dict

# Для `V3` Я могу передать фильтр, как строку `filter[id] = [5]` и как словарь `{\'filter[id]\':\'[5]\'}`
reference: str = presta_fields_dict["reference"]
search_filter_str: str = f'filter[reference] = [{reference}]'
search_filter_dict: Dict = {'filter[reference]': '[' + reference + ']'}
p: Product = Product(s)
ret = p.get(search_filter=search_filter_dict, PrestaAPIV='V3')

if ret is False or not ret or len(ret) == 0:
    # Новый товар
    p.add(presta_fields_dict, 'JSON', 'V3')