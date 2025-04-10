### **Анализ кода модуля `__morlevi__.py`**

**Качество кода:**

- **Соответствие стандартам**: 4/10
- **Плюсы**:
    - Код выполняет основные функции: логин, сбор данных о товаре и получение списка товаров в категории.
    - Используется модуль `logger` для логирования.
- **Минусы**:
    - Отсутствует подробная документация и docstring для большинства функций.
    - Многочисленные проблемы с форматированием, включая отсутствие пробелов вокруг операторов присваивания, использование старого стиля форматирования строк и неконсистентность в использовании кавычек.
    - Не везде используются аннотации типов.
    - Неправильное использование `json_loads`.
    - Некорректная обработка исключений.
    - Использование `eval` для вычисления цены.

**Рекомендации по улучшению:**

1.  **Добавить docstring ко всем функциям и классам**:

    -   Описать назначение каждой функции, параметры, возвращаемые значения и возможные исключения.
    -   Для внутренних функций также добавить docstring.
2.  **Исправить форматирование кода**:

    -   Использовать пробелы вокруг операторов присваивания: `x = 5` вместо `x=5`.
    -   Перейти на f-strings или `.format()` для форматирования строк, избегая конкатенации строк через `+`.
    -   Использовать одинарные кавычки для строк.
3.  **Добавить аннотации типов**:

    -   Для всех переменных и параметров функций указать типы данных.
4.  **Улучшить обработку исключений**:

    -   Использовать `ex` вместо `e` в блоках `except`.
    -   Логировать ошибки с использованием `logger.error(f'Error message', ex, exc_info=True)`.
5.  **Заменить `json_loads`**:

    -   Использовать `j_loads` из модуля `src.settings`.
6.  **Избегать использования `eval`**:

    -   Найти более безопасный способ для вычисления цены.
7.  **Удалить лишние комментарии и дублирующуюся документацию**:

    -   Удалить старые и неинформативные комментарии.
8.  **Привести код в соответствие со стандартами PEP8**.
9.  **Добавить обработку исключений для всех методов webdriver.**

**Оптимизированный код:**

```python
"""
Модуль для работы с поставщиком morlevi
======================================

Модуль содержит функции для логина на сайт поставщика,
сбора информации о товарах и получения списка товаров в категории.

Пример использования:
----------------------

>>> from src.suppliers.ivory import __morlevi__
>>> # Пример вызова функций модуля
"""

from pathlib import Path
import requests
import pandas as pd
from typing import List, Optional

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys

import settings
from src.settings import j_loads, logger, StringFormatter
from src.suppliers.Product import Product
from src.webdirver import Driver


def login(supplier) -> bool | None:
    """
    Выполняет вход на сайт поставщика.

    Args:
        supplier: Объект поставщика с настроенными параметрами.

    Returns:
        bool | None: True в случае успешного входа, None в случае ошибки.
    """
    _s = supplier
    _d: Driver = _s.driver
    _d.get_url('https://www.morlevi.co.il')
    if _login(_s):
        return True
    else:
        try:
            """
            закрываю модальные окна сайта
            выпадающие до входа
            """
            logger.error('Ошибка, пытаюсь закрыть popup')
            _d.page_refresh()
            if _login(_s):
                return True

            close_pop_up_locator = _s.locators['login']['close_pop_up_locator']
            close_pop_up_btn = _d.execute_locator(close_pop_up_locator)
            _d.wait(5)

            if isinstance(close_pop_up_btn, list):  # Если появилось несколько
                for b in close_pop_up_btn:
                    try:
                        b.click()
                        if _login(_s):
                            return True
                            break
                    except Exception as ex:
                        logger.error('Ошибка при закрытии модального окна', ex, exc_info=True)
                        ...
            if isinstance(close_pop_up_btn, WebElement):  # нашелся только один элемент
                close_pop_up_btn.click()
                return _login(_s)
        except Exception as ex:
            logger.error('Не удалось залогиниться', ex, exc_info=True)
            return


def _login(_s) -> bool | None:
    """
    Внутренняя функция для выполнения логина.

    Args:
        _s: Объект поставщика.

    Returns:
        bool | None: True в случае успешного входа, None в случае ошибки.
    """
    logger.debug('Собссно, логин Морлеви')
    _s.driver.refresh()
    # self.driver.switch_to_active_element()
    _d: Driver = _s.driver
    _l: dict = _s.locators['login']

    try:
        _d.execute_locator(_l['open_login_dialog_locator'])
        _d.wait(1.3)
        _d.execute_locator(_l['email_locator'])
        _d.wait(0.7)
        _d.execute_locator(_l['password_locator'])
        _d.wait(0.7)
        _d.execute_locator(_l['loginbutton_locator'])
        logger.debug('Mor logged in')
        return True
    except Exception as ex:
        logger.error(f'LOGIN ERROR', ex, exc_info=True)
        return


def grab_product_page(s) -> Product | None:
    """
    Собирает информацию о товаре со страницы.

    Args:
        s: Объект поставщика.

    Returns:
        Product | None: Объект товара с заполненными данными, None в случае ошибки.
    """
    p = Product(supplier=s)
    _: dict = s.locators['product']
    _d: Driver = s.driver
    _field = p.fields
    _s = s

    """ морлеви может выкинуть модальное окно """
    #_d.click(s.locators['close_pop_up_locator'])

    def set_id():
        """Устанавливает ID товара."""
        _id = _d.execute_locator(_['sku_locator'])
        if isinstance(_id, list):
            _field['id'] = _id[0]
            _field['Rewritten URL'] = str(_id[1]).replace(' ', '-')

    def set_sku_suppl():
        """Устанавливает артикул поставщика."""
        _field['sku suppl'] = _field['id']

    def set_sku_prod():
        """Устанавливает артикул товара."""
        _field['sku'] = str('mlv-') + _field['id']

    def set_title():
        """Устанавливает заголовок товара."""
        _field['title'] = _d.title

    def set_summary():
        """Устанавливает краткое описание товара."""
        _field['summary'] = _d.execute_locator(_['summary_locator'])
        _field['meta description'] = _field['summary']

    def set_description():
        """Устанавливает описание товара."""
        _field['description'] = _d.execute_locator(_['description_locator'])

    def set_cost_price():
        """Устанавливает цену товара."""
        _price = _d.execute_locator(_['price_locator'])
        if _price:
            _price = _price.replace(',', '')
            """  Может прийти все, что угодно  """
            _price = StringFormatter.clear_price(_price)
            try:
                price = float(_price)  # Преобразуем цену в число
                _field['cost price'] = round(price * float(s.settings['price_rule']))  # Используем float для вычислений
            except ValueError as ex:
                logger.error(f'Не удалось преобразовать цену: {_price}', ex, exc_info=True)
                return False
        else:
            logger.error('Not found price for ... ')
            return False
        return True

    def set_before_tax_price():
        """Устанавливает цену без налога."""
        _field['price tax excluded'] = _field['cost price']
        return True

    def set_delivery():
        """TODO перенести в комбинации"""
        # product_delivery_list = _d.execute_locator(_['product_delivery_locator'])
        # for i in product_delivery_list:
        #    ...
        ...

    def set_images(via_ftp=False):
        """Устанавливает изображения товара."""
        # _http_server = f'''http://davidka.esy.es/supplier_imgs/{_s.supplier_prefix}'''
        # _img_name = f'''{_field['sku']}.png'''
        # _field['img url'] =f'''{_http_server}/{_img_name}'''
        # screenshot = _d.execute_locator(_['main_image_locator'])
        # _s.save_and_send_via_ftp({_img_name:screenshot})

        _images = _d.execute_locator(_['main_image_locator'])
        if not _images:
            return
        _field['img url'] = _images

    def set_combinations():
        """Устанавливает комбинации товара."""
        ...

    def set_qty():
        """Устанавливает количество товара."""
        ...

    def set_specification():
        """Устанавливает спецификацию товара."""
        _field['specification'] = _d.execute_locator(_['product_name_locator'])

    def set_customer_reviews():
        """Устанавливает отзывы клиентов."""
        ...

    def set_supplier():
        """Устанавливает поставщика."""
        _field['supplier'] = '2784'
        ...

    def set_rewritted_URL():
        """Устанавливает переписанный URL."""
        # _field['Rewritten URL'] = StringFormatter.set_rewritted_URL(_field['title'])
        ...

    set_id()
    set_sku_suppl()
    set_sku_prod()
    set_title()
    set_cost_price()
    set_before_tax_price()
    set_delivery()
    set_images()
    set_combinations()
    # set_qty()
    # set_byer_protection()
    set_description()
    set_summary()
    # set_specification()
    # set_customer_reviews()
    set_supplier()
    set_rewritted_URL()

    return p
    ...


def list_products_in_category_from_pagination(supplier) -> list[str]:
    """
    Получает список товаров в категории, переходя по страницам пагинации.

    Args:
        supplier: Объект поставщика.

    Returns:
        list[str]: Список URL товаров в категории.
    """
    _s = supplier
    _d: Driver = _s.driver
    _l = _s.locators['product']['link_to_product_locator']

    list_products_in_category: list[str] = []
    _product_list_from_page = _d.execute_locator(_l)
    """ может вернуться или список адресов или строка или None
    если нет товаров на странице на  данный момент"""
    if _product_list_from_page is None or not _product_list_from_page:
        """ нет смысла продожать. Нет товаров в категории
        Возвращаю пустой список"""
        # logger.debug(f''' Нет товаров в категории по адресу {_d.current_url}''')
        return list_products_in_category

    if isinstance(_product_list_from_page, list):
        list_products_in_category.extend(_product_list_from_page)
    else:
        list_products_in_category.append(_product_list_from_page)

    pages = _d.execute_locator(_s.locators['pagination']['a'])
    if isinstance(pages, list):
        for page in pages:
            _product_list_from_page = _d.execute_locator(_l)
            """ может вернуться или список адресов или строка. """
            if isinstance(_product_list_from_page, list):
                list_products_in_category.extend(_product_list_from_page)
            else:
                list_products_in_category.append(_product_list_from_page)

            _perv_url = _d.current_url
            page.click()

            """ дошел до конца листалки """
            if _perv_url == _d.current_url:
                break

    if isinstance(list_products_in_category, list):
        list_products_in_category = list(set(list_products_in_category))
    return list_products_in_category


def get_list_products_in_category(s, scenario, presath):
    """
    s:Supplier
    scenario:JSON
    presath:PrestaShopWebServiceDict
    """
    l = list_products_in_category_from_pagination(s, scenario)
    ...


def get_list_categories_from_site(s, scenario_file, brand=''):
    ...