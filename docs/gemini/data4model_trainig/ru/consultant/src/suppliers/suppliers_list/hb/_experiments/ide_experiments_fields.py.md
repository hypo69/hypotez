### **Анализ кода модуля `ide_experiments_fields.py`**

**Качество кода**:
- **Соответствие стандартам**: 5/10
- **Плюсы**:
    - Код содержит много полезной функциональности для сбора данных о товарах.
    - Используются аннотации типов.
- **Минусы**:
    - Очень много закомментированного кода, что затрудняет чтение и понимание логики.
    - Отсутствует единый стиль форматирования, что снижает читаемость.
    - Слишком много глобальных переменных.
    - Не все функции содержат docstring.
    - Многие docstring написаны не по стандарту (отсутствует описание аргументов, возвращаемых значений и т.д.).
    - Некоторые комментарии неинформативны и не объясняют, что делает код.
    - Присутствуют магические строки и числа.
    - Не везде используется логирование ошибок.
    - Не используется `j_loads` для загрузки `json` файлов
    - В импортах используется `Union[]`.

**Рекомендации по улучшению**:

1.  **Удалить или пересмотреть закомментированный код**: Если код больше не нужен, его следует удалить. Если он может понадобиться в будущем, необходимо перенести его в другое место (например, в систему контроля версий) или объяснить, почему он закомментирован.
2.  **Унифицировать стиль форматирования**: Использовать autopep8 или black для автоматического форматирования кода в соответствии со стандартами PEP8.
3.  **Избавиться от глобальных переменных**: Передавать необходимые объекты (например, `Supplier`, `Product`, `ProductFields`, `Driver`) в функции в качестве аргументов.
4.  **Добавить docstring для всех функций**: Описать назначение каждой функции, ее аргументы и возвращаемое значение. Использовать единый стиль для docstring.
5.  **Сделать комментарии более информативными**: Объяснять, что делает код, а не просто повторять его. Избегать расплывчатых формулировок, таких как "получаем" или "делаем".
6.  **Избавиться от магических строк и чисел**: Использовать константы для хранения значений, которые используются в нескольких местах.
7.  **Добавить логирование ошибок**: Использовать `logger.error` для записи информации об ошибках, возникающих в процессе работы кода.
8.  **Использовать `j_loads` или `j_loads_ns`**:  Для чтения JSON или конфигурационных файлов заменить стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns`.
9.  **Использовать `|` вместо `Union[]`**:  Для аннотаций типов использовать `|` вместо `Union[]`.

**Оптимизированный код**:

```python
## \file /src/suppliers/hb/_experiments/ide_experiments_fields.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для экспериментов с полями товаров HB
=================================================

Модуль содержит функции для сбора и обработки данных о товарах с сайта HB.
Он включает функции для извлечения различных полей товара, таких как название,
описание, цена, характеристики и т.д.

Пример использования:
----------------------

>>> from src.suppliers import Supplier
>>> from src.product import Product, ProductFields
>>> s = Supplier(supplier_prefix='hb')
>>> p = Product(s)
>>> f = ProductFields(s)
>>> product_fields = grab_product_page(s)
"""

import os
import sys
from pathlib import Path
from typing import List, Union, Dict, Optional
from selenium.webdriver.remote.webelement import WebElement

# Добавление корневой директории позволяет мне плясать от печки
dir_root: Path = Path(os.getcwd()[: os.getcwd().rfind("hypotez") + 7])
sys.path.append(str(dir_root))  # Adding the root folder to sys.path
dir_src = Path(dir_root, 'src')
sys.path.append(str(dir_root))

from src.webdriver import executor

""" добавление корневой директории позволяет мне плясать от печки. """
####################################################################################################


from src import gs
from src.suppliers import Supplier
from src.product import Product, ProductFields

from src.logger.logger import logger
from src.webdriver.driver import Driver
from src.utils import StringFormatter, StringNormalizer

# Функция grabber() собирает поля товара. Для каждого товара есть своя функия - заполнитель поля
# В этом тесте Функция вызывается к конце файла

s: Supplier = Supplier(supplier_prefix='hb')
p: Product = Product(s)
l: Dict = s.locators["product"]
d: Driver = s.driver
f: ProductFields = ProductFields(s)

s.current_scenario: Dict = {
    "url": "https://hbdeadsea.co.il/product-category/bodyspa/feet-hand-treatment/",
    "name": "טיפוח כפות ידיים ורגליים",
    "condition": "new",
    "presta_categories": {
        "default_category": 11259,
        "additional_categories": [],
    },
}

d.get_url(s.current_scenario['url'])


def grab_product_page(supplier: Supplier, async_run: bool = True) -> ProductFields:
    """Собирает со страницы товара значения веб-элементов и приводит их к полям ProductFields.

    Args:
        supplier (Supplier): Класс поставщика. Веб-драйвер должен быть установлен на странице товара.
        async_run (bool): Флаг для асинхронного запуска. По умолчанию True.

    Returns:
        ProductFields: Объект с заполненными полями товара.
    """
    global s
    s = supplier

    global p
    p = Product(s)

    global f
    f = ProductFields(s)

    d = s.driver

    global l
    l = s.locators["product"]
    d.wait(5)
    d.execute_locator(l["close_banner"])
    """ закрываю баннер """

    d.scroll()
    """ прокручиваю страницу товара, чтобы захватить области, которые подгружаются через AJAX """

    ######################################################################################
    #
    #
    #\t\t\t""" Функции, специфичные для конкретного  поставщика """
    #
    #
    #
    #\t\t

    def product_reference_and_volume_and_price_for_100() -> None:
        """Извлекает объем, артикул поставщика и цену за единицу товара.
        Реализовать поле `цена за единицу товара`
        """
        global f, s
        webelements: List[WebElement] = d.execute_locator(
            l["product_reference_and_volume_and_price_for_100"]
        )

        for webelement in webelements:
            if ('Fl.oz' and 'מ"ל') in webelement.text:
                """ объем """
                f.volume = webelement.text
            elif str(r'מחיר ל100 מ"ל') in webelement.text:
                """ цена за единицу товара
                @todo придумать куда
                """
                print(f'цена за единицу товара:{webelement.text}')
            elif 'מקט' in webelement.text:
                f.supplier_reference = StringNormalizer.get_numbers_only(
                    webelement.text
                )
            ...
        ...
        #
        #
        #\t
        #######################################################################################

    def set_references(f: ProductFields, s: Supplier) -> None:
        """Устанавливает значения для идентификаторов товара."""
        # f.supplier_reference = field_supplier_reference()
        f.id_supplier = int(s.supplier_id)
        f.reference = f'{s.supplier_id}-{f.supplier_reference}'

    product_reference_and_volume_and_price_for_100()
    set_references(f, s)

    # f.active = field_active() # Совпадает с f.available_for_order
    # f.additional_delivery_times = field_additional_delivery_times()\t# [v]  Мое поле. Нахера - не знаю
    f.additional_shipping_cost = field_additional_shipping_cost()  # [v]
    # f.advanced_stock_management = field_advanced_stock_management()
    f.affiliate_short_link = field_affiliate_short_link()  # [v]
    # f.affiliate_summary = field_affiliate_summary()
    # f.affiliate_image_large = field_affiliate_image_large()
    # f.affiliate_image_medium = field_affiliate_image_medium()
    # f.affiliate_image_small = field_affiliate_image_small()
    # f.affiliate_summary_2 = field_affiliate_summary_2()
    # f.affiliate_text = field_affiliate_text()
    # f.affiliate_image_large = field_affiliate_image_large()
    # f.affiliate_image_medium = field_affiliate_image_medium()
    # f.affiliate_image_small = field_affiliate_image_small()
    # f.available_date = field_available_date()
    f.available_for_order = f.active = field_available_for_order()
    # f.available_later = field_available_later()
    # f.available_now = field_available_now()
    # f.cache_default_attribute = field_cache_default_attribute()
    # f.cache_has_attachments = field_cache_has_attachments()
    # f.cache_is_pack = field_cache_is_pack()
    # f.category_ids_append = field_category_ids_append() ##<- добавочные категории. Если надо дополнить уже внесенные
    f.condition = field_condition()
    # f.customizable = field_customizable()
    # f.date_add = field_date_add()
    # f.date_upd = field_date_upd()

    ################################################################################
    _images_urls: list = d.execute_locator(l["additional_images_urls"])
    if len(_images_urls) > 0:
        f.assist_fields_dict['default_image_url'] = _images_urls[0]
    if len(_images_urls) > 1:
        f.assist_fields_dict['images_urls'] = _images_urls[1::]
    ################################################################################

    # f.delivery_in_stock = field_delivery_in_stock()\t # [v]\t ##<- доставка
    # f.delivery_out_stock = field_delivery_out_stock()\t#   Заметка о доставке, когда товара нет в наличии

    # f.depth = field_depth()
    # f.description = field_description()
    f.description_short = f.description = field_description()
    # f.ean13 = field_ean13()
    # f.ecotax = field_ecotax()
    # f.height = field_height()
    f.how_to_use = field_how_to_use()
    f.id_category_default = field_id_category_default()
    # f.id_default_combination = field_id_default_combination()
    # f.id_default_image = field_id_default_image()
    # f.id_lang = s.locale
    f.id_manufacturer = field_id_manufacturer()
    # f.id_product = field_id_product()
    # f.id_shop_default = field_id_shop_default()   ## <- усранавливается в `product_fields_default_values.json`
    # f.id_supplier = s.supplier_id\t# [v] ## <- добывается функцией set_references()
    # f.id_tax = field_id_tax() # [v]
    # f.id_type_redirected = field_id_type_redirected()
    # f.images_urls = field_images_urls()\t# [v]
    # f.indexed = field_indexed()
    f.ingredients = field_ingredients()

    # f.is_virtual = field_is_virtual()
    # f.isbn = field_isbn()
    # f.link_rewrite = field_link_rewrite()
    # f.location = field_location()
    # f.low_stock_alert = field_low_stock_alert()
    # f.low_stock_threshold = field_low_stock_threshold()
    # f.meta_description = field_meta_description()
    # f.meta_keywords = field_meta_keywords()
    # f.meta_title = field_meta_title()
    # f.minimal_quantity = field_minimal_quantity()
    # f.mpn = field_mpn()

    ###########################################################################################################
    _name = d.execute_locator(l["name"])[0]  # чтоб два раза не бегать, Я получаю значение локатора в _name
    f.name = field_name(_name)  # а потом использую для f.name
    f.link_rewrite = field_link_rewrite(_name)  # и для f.link_rewrite
    ###########################################################################################################

    # f.online_only = field_online_only()
    f.on_sale = field_on_sale()
    # f.out_of_stock = field_out_of_stock()
    # f.pack_stock_type = field_pack_stock_type()
    # f.position_in_category = field_position_in_category()
    f.price = field_price()
    # f.product_type = field_product_type()
    # f.quantity = field_quantity()
    # f.quantity_discount = field_quantity_discount()
    # f.redirect_type = field_redirect_type()
    # f.reference = field_reference()\t# [v]  ## <- устанавливается в функции `set_references()`
    # f.show_condition = field_show_condition()
    # f.show_price = field_show_price()
    # f.state = field_state()
    # f.supplier_reference = field_supplier_reference()  # [v]  ## <- устанавливается в функции `set_references()`
    # f.text_fields = field_text_fields()
    # f.unit_price_ratio = field_unit_price_ratio()\t\t<- см описание поля в базе данных
    # f.unity = field_unity()
    # f.upc = field_upc()
    # f.uploadable_files = field_uploadable_files()
    # f.volume = field_volume()\t\t ## <- устанавливается в функции `product_reference_and_volume_and_price_for_100()`
    f.visibility = field_visibility()
    # f.weight = field_weight()
    # f.wholesale_price = field_wholesale_price()
    # f.width = field_width()
    ...
    return f


d.get_url(s.current_scenario["url"])
""" перехожу по URL сценария (обычно, категория)"""

list_products_in_category: list = s.related_modules.get_list_products_in_category(s)
""" собрал список товаров в категории """

if not list_products_in_category:
    ...

d.get_url(list_products_in_category[0])
""" перешел по первому url из списка """

d.wait(5)
d.execute_locator(s.locators["product"]["close_banner"])

...


# def set_references():
#     global f
#     f.supplier_reference = field_supplier_reference()
#     #f.id_supplier = s.supplier_id ## <- прописан в product.json
#     f.reference = f'{s.supplier_id}-{f.supplier_reference}'


def field_additional_shipping_cost() -> str:
    """Возвращает стоимость доставки.

    Returns:
        str: Стоимость доставки.
    """
    return d.execute_locator(l["additional_shipping_cost"])


# f.additional_shipping_cost  = field_additional_shipping_cost()


# f.affiliate_short_link = d.current_url

# f.affiliate_summary = f.affiliate_summary_2 = ''


def field_delivery_in_stock() -> str:
    """Возвращает информацию о доставке, когда товар в наличии.

    Returns:
        str: Информация о доставке.
    """
    return str(d.execute_locator(l["delivery_in_stock"]))
    ...


def field_active() -> int:
    """Определяет, активен ли товар.

    Returns:
        int: 1, если товар активен, 0 - если нет.
    """
    return f.active  # <-  поставить в зависимость от delivery_out_stock
    ...


def field_additional_delivery_times() -> str:
    """Возвращает дополнительное время доставки.

    Returns:
        str: Дополнительное время доставки.
    """
    return d.execute_locator(l["additional_delivery_times"])
    ...


def field_additional_shipping_cost() -> str:
    """Возвращает дополнительную стоимость доставки.

    Returns:
        str: Дополнительная стоимость доставки.
    """
    return d.execute_locator(l["additional_shipping_cost"])
    ...


def field_advanced_stock_management() -> str:
    """Возвращает информацию об управлении запасами.

    Returns:
        str: Информация об управлении запасами.
    """
    return f.advanced_stock_management
    ...


def field_affiliate_short_link() -> str:
    """Возвращает короткую ссылку для аффилиатов.

    Returns:
        str: Короткая ссылка.
    """
    return d.current_url
    ...


def field_affiliate_summary() -> str:
    """Возвращает краткое описание для аффилиатов.

    Returns:
        str: Краткое описание.
    """
    return f.affiliate_summary
    ...


def field_affiliate_summary_2() -> str:
    """Возвращает дополнительное краткое описание для аффилиатов.

    Returns:
        str: Дополнительное краткое описание.
    """
    return f.affiliate_summary_2
    ...


def field_affiliate_text() -> str:
    """Возвращает текст для аффилиатов.

    Returns:
        str: Текст для аффилиатов.
    """
    return f.affiliate_text
    ...


def field_affiliate_image_large() -> None:
    """Извлекает URL большого изображения для аффилиатов."""
    ...


def field_affiliate_image_medium() -> None:
    """Извлекает URL среднего изображения для аффилиатов."""
    ...


def field_affiliate_image_small() -> str:
    """Извлекает URL маленького изображения для аффилиатов.

    Returns:
        str: URL маленького изображения.
    """
    return d.execute_locator(l["affiliate_image_small"])


def field_available_date() -> str:
    """Возвращает дату доступности товара.

    Returns:
        str: Дата доступности.
    """
    return f.available_date
    ...


def field_available_for_order() -> int:
    """Определяет, доступен ли товар для заказа.

    Если вернулся веб-элемент, это флаг, что товара нет в наличии, а вернулся <p>המלאי אזל

    Returns:
        int: 1, если товар доступен для заказа, 0 - если нет.
    """
    available_for_order = d.execute_locator(l["available_for_order"])
    ...
    if available_for_order is None:
        f.available_for_order = 1
    else:
        f.available_for_order = 0
        f.active = 0
    ...


def field_available_later() -> str:
    """Возвращает текст о доступности товара позже.

    Returns:
        str: Текст о доступности позже.
    """
    return f.available_later
    ...


def field_available_now() -> str:
    """Возвращает текст о доступности товара сейчас.

    Returns:
        str: Текст о доступности сейчас.
    """
    return f.available_now
    ...


def field_category_ids() -> str:
    """Возвращает идентификаторы категорий товара.

    Returns:
        str: Идентификаторы категорий.
    """
    return f.category_ids
    ...


def field_category_ids_append() -> None:
    """Добавляет идентификаторы категорий товара."""
    # return f.category_ids_append
    ...


def field_cache_default_attribute() -> str:
    """Возвращает атрибут кэша по умолчанию.

    Returns:
        str: Атрибут кэша по умолчанию.
    """
    return f.cache_default_attribute
    ...


def field_cache_has_attachments() -> str:
    """Проверяет наличие вложений в кэше.

    Returns:
        str: Информация о наличии вложений.
    """
    return f.cache_has_attachments
    ...


def field_cache_is_pack() -> str:
    """Проверяет, является ли товар набором в кэше.

    Returns:
        str: Информация о том, является ли товар набором.
    """
    return f.cache_is_pack
    ...


def field_condition() -> str:
    """Возвращает условие товара.

    Returns:
        str: Условие товара.
    """
    return d.execute_locator(l.condition)


def field_customizable() -> str:
    """Определяет, настраиваемый ли товар.

    Returns:
        str: Информация о настраиваемости.
    """
    return f.customizable
    ...


def field_date_add() -> str:
    """Возвращает дату добавления товара.

    Returns:
        str: Дата добавления.
    """
    return f.date_add
    ...


def field_date_upd() -> str:
    """Возвращает дату обновления товара.

    Returns:
        str: Дата обновления.
    """
    return f.date_upd
    ...


def field_delivery_in_stock() -> str:
    """Возвращает информацию о доставке, когда товар в наличии.

    Returns:
        str: Информация о доставке.
    """
    return d.execute_locator(l["delivery_in_stock"])
    ...


def field_delivery_out_stock() -> str:
    """Возвращает заметку о доставке, когда товара нет в наличии.

    Returns:
        str: Заметка о доставке.
    """
    return f.delivery_out_stock
    ...


def field_depth() -> str:
    """Возвращает глубину товара.

    Returns:
        str: Глубина товара.
    """
    return d.execute_locator(l["depth"])
    ...


def field_description() -> str:
    """Возвращает полное описание товара.

    Returns:
        str: Полное описание товара.
    """
    return d.execute_locator(l["description"])[0].text
    ...


def field_id_category_default() -> int:
    """Возвращает главную категорию товара. Берется из сценария.

    Returns:
        int: ID главной категории.
    """
    return s.current_scenario["presta_categories"]["default_category"]
    ...


def field_ean13() -> str:
    """Возвращает EAN13 товара.

    Returns:
        str: EAN13.
    """
    return d.execute_locator(l["ean13"])
    ...


def field_ecotax() -> str:
    """Возвращает ecotax товара.

    Returns:
        str: Ecotax.
    """
    return f.ecotax
    ...


def field_height() -> str:
    """Возвращает высоту товара.

    Returns:
        str: Высота товара.
    """
    return d.execute_locator(l["height"])
    ...


def field_how_to_use() -> str:
    """Возвращает инструкцию по использованию товара.

    Returns:
        str: Инструкция по использованию.
    """
    return d.execute_locator(l["how_to_use"])[0].text
    ...


def field_id_category_default() -> int:
    """Возвращает главную категорию товара.

    Returns:
        int: ID главной категории.
    """
    return s.current_scenario["presta_categories"]["default_category"]
    ...


def field_id_default_combination() -> str:
    """Возвращает ID комбинации по умолчанию.

    Returns:
        str: ID комбинации.
    """
    return f.id_default_combination
    ...


def field_id_default_image() -> str:
    """Возвращает ID изображения по умолчанию.

    Returns:
        str: ID изображения.
    """
    return f.id_default_image
    ...


def field_id_lang() -> str:
    """Возвращает ID языка.

    Returns:
        str: ID языка.
    """
    return f.id_lang
    ...


def field_id_manufacturer() -> str:
    """Возвращает ID бренда. Может быть и названием бренда - престашоп сам разберется.

    Returns:
        str: ID бренда.
    """
    return d.execute_locator(l["id_manufacturer"])
    ...


def field_id_product() -> str:
    """Возвращает ID товара.

    Returns:
        str: ID товара.
    """
    return f.id_product
    ...


def field_id_shop_default() -> str:
    """Возвращает ID магазина по умолчанию.

    Returns:
        str: ID магазина.
    """
    return f.id_shop_default
    ...


def field_id_supplier() -> str:
    """Возвращает ID поставщика.

    Returns:
        str: ID поставщика.
    """
    return d.execute_locator(l["id_supplier"])
    ...


def field_id_tax() -> str:
    """Возвращает ID налога.

    Returns:
        str: ID налога.
    """
    return f.id_tax
    ...


def field_id_type_redirected() -> str:
    """Возвращает ID типа переадресации.

    Returns:
        str: ID типа переадресации.
    """
    return f.id_type_redirected
    ...


def field_images_urls() -> str:
    """Загружает дефолтную картинку.

    Returns:
        str: URL изображения.
    """
    return d.execute_locator(l["additional_images_urls"])
    ...


def field_indexed() -> str:
    """Определяет, индексирован ли товар.

    Returns:
        str: Информация об индексации.
    """
    return f.indexed
    ...


def field_ingredients() -> str:
    """Возвращает состав товара. Забираю с сайта HTML с картинками ингридиентов.

    Returns:
        str: Состав товара.
    """
    return d.execute_locator(l["ingredients"])[0].text
    ...


def field_meta_description() -> None:
    """Извлекает мета-описание товара."""
    d.execute_locator(l['meta_description'])
    ...


def field_meta_keywords() -> str:
    """Возвращает мета-ключевые слова товара.

    Returns:
        str: Мета-ключевые слова.
    """
    return d.execute_locator(l['meta_keywords'])
    ...


def field_meta_title() -> str:
    """Возвращает мета-заголовок товара.

    Returns:
        str: Мета-заголовок.
    """
    return d.execute_locator(l['meta_title'])
    ...


def field_is_virtual() -> str:
    """Определяет, является ли товар виртуальным.

    Returns:
        str: Информация о виртуальности.
    """
    return f.is_virtual
    ...


def field_isbn() -> str:
    """Возвращает ISBN товара.

    Returns:
        str: ISBN.
    """
    return f.isbn
    ...


def field_link_rewrite(product_name: str) -> str:
    """Создает link_rewrite из переменной `product_name`, которая содержит значение локатора l["name"].

    Args:
        product_name (str): Название товара.

    Returns:
        str: Link rewrite.
    """
    return StringNormalizer.normalize_link_rewrite(product_name)
    ...


def field_location() -> str:
    """Возвращает местоположение товара.

    Returns:
        str: Местоположение.
    """
    return f.location
    ...


def field_low_stock_alert() -> str:
    """Возвращает оповещение о низком запасе.

    Returns:
        str: Оповещение о низком запасе.
    """
    return f.low_stock_alert
    ...


def field_low_stock_threshold() -> str:
    """Возвращает порог низкого запаса.

    Returns:
        str: Порог низкого запаса.
    """
    return f.low_stock_threshold
    ...


def field_meta_description() -> None:
    """Извлекает мета-описание товара."""
    ...


def field_meta_keywords() -> str:
    """Возвращает мета-ключевые слова товара.

    Returns:
        str: Мета-ключевые слова.
    """
    return f.meta_keywords
    ...


def field_meta_title() -> str:
    """Возвращает мета-заголовок товара.

    Returns:
        str: Мета-заголовок.
    """
    return f.meta_title
    ...


def field_minimal_quantity() -> str:
    """Возвращает минимальное количество для заказа.

    Returns:
        str: Минимальное количество.
    """
    return f.minimal_quantity
    ...


def field_mpn() -> str:
    """Возвращает MPN товара.

    Returns:
        str: MPN.
    """
    return f.mpn
    ...


def field_name(name: str) -> str:
    """Возвращает название товара.

    Очищает поля от лишних параметров, которые не проходят в престашоп.

    Args:
        name (str): Название товара.

    Returns:
        str: Очищенное название товара.
    """
    return StringNormalizer.normalize_product_name(name)
    ...


def field_online_only() -> str:
    """Определяет, продается ли товар только в интернет-магазине.

    Returns:
        str: Информация о продаже только в интернет-магазине.
    """
    return d.execute_locator(l['online_only'])
    ...


def field_on_sale() -> str:
    """Определяет, находится ли товар на распродаже.

    Returns:
        str: Информация о распродаже.
    """
    return d.execute_locator(l['on_sale'])
    ...


def field_out_of_stock() -> str:
    """Определяет, есть ли товар в наличии.

    Returns:
        str: Информация о наличии.
    """
    return d.execute_locator(l["out_of_stock"])
    ...


def field_pack_stock_type() -> str:
    """Возвращает тип запаса для набора.

    Returns:
        str: Тип запаса.
    """
    return f.pack_stock_type
    ...


def field_position_in_category() -> str:
    """Возвращает позицию товара в категории.

    Returns:
        str: Позиция в категории.
    """
    return f.position_in_category
    ...


def field_price() -> str:
    """Возвращает цену товара.

    Returns:
        str: Цена товара.
    """
    return StringNormalizer.normalize_price(d.execute_locator(l["price"])[0])


def field_product_type() -> str:
    """Возвращает тип товара.

    Returns:
        str: Тип товара.
    """
    return f.product_type
    ...


#
# def field_quantity():
# \t"""
# \t
# \t@details
# \t"""
# \treturn f.quantity
# \t...


def field_quantity_discount() -> str:
    """Возвращает скидку за количество.

    Returns:
        str: Скидка за количество.
    """
    return f.quantity_discount
    ...


def field_redirect_type() -> str:
    """Возвращает тип переадресации.

    Returns:
        str: Тип переадресации.
    """
    return f.redirect_type
    ...


def field_reference() -> str:
    """Возвращает артикул поставщика.

    Returns:
        str: Артикул поставщика.
    """
    return f'{s.supplier_id}-{f.supplier_reference}'
    ...


def field_show_condition() -> str:
    """Определяет, отображается ли условие товара.

    Returns:
        str: Информация об отображении условия.
    """
    return f.show_condition


def field_show_price() -> str:
    """Определяет, отображается ли цена товара.