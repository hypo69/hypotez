## \file /src/suppliers/get_graber_by_supplier.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для получения грабера на основе URL поставщика
=========================================================================================

Этот модуль предоставляет функциональность для получения соответствующего объекта грабера
для заданного URL поставщика. У каждого поставщика есть свой собственный грабер, который
извлекает значения полей с целевой HTML-страницы.

Пример использования
-------------------

```python
    from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_url
    from src.webdriver import Driver # Предполагается, что Driver импортируется так

    # Инициализация драйвера (пример)
    driver = Driver() 
    url = 'https://www.example.com'
    graber = get_graber_by_supplier_url(driver, url, 2) # Пример с lang_index = 2

    if graber:
        # Использование грабера для извлечения данных
        product_data = graber.get_product_data()
        print(f'Data extracted: {product_data}')
    else:
        # Обработка случая, когда грабер не найден
        print(f'No grabber found for URL: {url}')

```

.. module:: src.suppliers.get_graber_by_supplier
"""
from typing import Type # Используется для аннотации типа Driver без циклического импорта, если необходимо
from src.suppliers.graber import Graber
from src.suppliers.suppliers_list.aliexpress.graber import Graber as AliexpressGraber
from src.suppliers.suppliers_list.amazon.graber import Graber as AmazonGraber
from src.suppliers.suppliers_list.bangood.graber import Graber as BangoodGraber
from src.suppliers.suppliers_list.cdata.graber import Graber as CdataGraber
from src.suppliers.suppliers_list.ebay.graber import Graber as EbayGraber
from src.suppliers.suppliers_list.etzmaleh.graber import Graber as EtzmalehGraber
from src.suppliers.suppliers_list.gearbest.graber import Graber as GearbestGraber
from src.suppliers.suppliers_list.grandadvance.graber import Graber as GrandadvanceGraber
from src.suppliers.suppliers_list.hb.graber import Graber as HBGraber
from src.suppliers.suppliers_list.ivory.graber import Graber as IvoryGraber
from src.suppliers.suppliers_list.ksp.graber import Graber as KspGraber
from src.suppliers.suppliers_list.kualastyle.graber import Graber as KualaStyleGraber
from src.suppliers.suppliers_list.morlevi.graber import Graber as MorleviGraber
from src.suppliers.suppliers_list.visualdg.graber import Graber as VisualDGGraber
from src.suppliers.suppliers_list.wallashop.graber import Graber as WallaShopGraber
from src.suppliers.suppliers_list.wallmart.graber import Graber as WallmartGraber
from src.logger.logger import logger
# Предполагается, что класс Driver импортируется из модуля webdriver
# Если это вызывает циклический импорт, можно использовать Type['Driver']
from src.webdriver import Driver


def get_graber_by_supplier_url(driver: Driver, url: str, lang_index: int) -> Graber | None:
    """
    Функция возвращает соответствующий грабер для заданного URL поставщика.

    Для каждого поставщика существует свой грабер, который извлекает значения полей
    с целевой HTML-страницы. Функция сначала переходит по URL с помощью драйвера.

    Args:
        driver (Driver): Экземпляр веб-драйвера для взаимодействия со страницей.
        url (str): URL страницы поставщика.
        lang_index (int): Индекс языка в магазине Prestashop (например, для локализации).

    Returns:
        Graber | None: Экземпляр соответствующего класса Graber, если совпадение найдено, иначе None.

    Example:
        >>> from src.webdriver import Driver # Пример импорта
        >>> driver_instance = Driver() # Пример создания экземпляра
        >>> supplier_url = 'https://ksp.co.il/item/12345'
        >>> lang_id = 2
        >>> grabber_instance = get_graber_by_supplier_url(driver_instance, supplier_url, lang_id)
        >>> if grabber_instance:
        ...     print(f'Grabber found: {type(grabber_instance).__name__}')
        Grabber found: KspGraber # Пример вывода
    """
    # Переход по указанному URL
    driver.get_url(url)

    # Определение и возврат соответствующего грабера на основе URL
    if url.startswith(('https://aliexpress.com', 'https://wwww.aliexpress.com')):
        return AliexpressGraber(driver, lang_index)

    if url.startswith(('https://amazon.com', 'https://wwww.amazon.com')):
        return AmazonGraber(driver, lang_index)

    if url.startswith(('https://bangood.com', 'https://wwww.bangood.com')):
        return BangoodGraber(driver, lang_index)

    if url.startswith(('https://cdata.co.il', 'https://wwww.cdata.co.il')):
        return CdataGraber(driver, lang_index)

    if url.startswith(('https://ebay.', 'https://wwww.ebay.')): # Учитывает разные домены ebay (com, co.uk и т.д.)
        return EbayGraber(driver, lang_index)

    if url.startswith(('https://etzmaleh.co.il', 'https://www.etzmaleh.co.il')):
        return EtzmalehGraber(driver, lang_index)

    if url.startswith(('https://gearbest.com', 'https://wwww.gearbest.com')):
        return GearbestGraber(driver, lang_index)

    if url.startswith(('https://grandadvance.co.il', 'https://www.grandadvance.co.il')):
        return GrandadvanceGraber(driver, lang_index)

    if url.startswith(('https://hb-digital.co.il', 'https://www.hb-digital.co.il')):
        return HBGraber(driver, lang_index)

    if url.startswith(('https://ivory.co.il', 'https://www.ivory.co.il')):
        return IvoryGraber(driver, lang_index)

    if url.startswith(('https://ksp.co.il', 'https://www.ksp.co.il')):
        return KspGraber(driver, lang_index)

    if url.startswith(('https://kualastyle.com', 'https://www.kualastyle.com')):
        return KualaStyleGraber(driver, lang_index)

    if url.startswith(('https://morlevi.co.il', 'https://www.morlevi.co.il')):
        return MorleviGraber(driver, lang_index)

    if url.startswith(('https://www.visualdg.com', 'https://visualdg.com')):
        return VisualDGGraber(driver, lang_index)

    if url.startswith(('https://wallashop.co.il', 'https://www.wallashop.co.il')):
        return WallaShopGraber(driver, lang_index)

    if url.startswith(('https://www.wallmart.com', 'https://wallmart.com')):
        return WallmartGraber(driver, lang_index)

    # Логгирование, если грабер для URL не найден
    logger.debug(f'грабер для URL не найден: {url}')
    ... # Оставлено без изменений согласно требованиям
    return None # Явный возврат None, если ни одно условие не выполнено


def get_graber_by_supplier_prefix(driver: Driver, supplier_prefix: str, lang_index: int = 2) -> Graber | None:
    """
    Функция возвращает соответствующий грабер по префиксу имени поставщика.

    Args:
        driver (Driver): Экземпляр веб-драйвера.
        supplier_prefix (str): Строковый префикс или идентификатор поставщика (в нижнем регистре).
        lang_index (int, optional): Индекс языка. По умолчанию 2.

    Returns:
        Graber | None: Экземпляр соответствующего класса Graber, если префикс совпадает, иначе None.

    Example:
        >>> from src.webdriver import Driver # Пример импорта
        >>> driver_instance = Driver() # Пример создания экземпляра
        >>> prefix = 'ksp'
        >>> lang_id = 2
        >>> grabber_instance = get_graber_by_supplier_prefix(driver_instance, prefix, lang_id)
        >>> if grabber_instance:
        ...     print(f'Grabber found: {type(grabber_instance).__name__}')
        Grabber found: KspGraber # Пример вывода
    """
    # Объявление переменной в начале функции
    grabber: Graber | None = None
    ... # Оставлено без изменений согласно требованиям

    # Определение грабера на основе префикса
    # Приведение префикса к нижнему регистру для надежного сравнения
    prefix_lower: str = supplier_prefix.lower()

    if prefix_lower == 'aliexpress':
        grabber = AliexpressGraber(driver, lang_index)
    elif prefix_lower == 'amazon':
        grabber = AmazonGraber(driver, lang_index)
    elif prefix_lower == 'bangood': # Добавлен недостающий префикс
        grabber = BangoodGraber(driver, lang_index)
    elif prefix_lower == 'cdata': # Добавлен недостающий префикс
         grabber = CdataGraber(driver, lang_index)
    elif prefix_lower == 'ebay':
        grabber = EbayGraber(driver, lang_index)
    elif prefix_lower == 'etzmaleh': # Добавлен недостающий префикс
         grabber = EtzmalehGraber(driver, lang_index)
    elif prefix_lower == 'gearbest':
        grabber = GearbestGraber(driver, lang_index)
    elif prefix_lower == 'grandadvance':
        grabber = GrandadvanceGraber(driver, lang_index)
    elif prefix_lower == 'hb':
        grabber = HBGraber(driver, lang_index)
    elif prefix_lower == 'ivory':
        grabber = IvoryGraber(driver, lang_index)
    elif prefix_lower == 'ksp':
        grabber = KspGraber(driver, lang_index)
    elif prefix_lower == 'kualastyle':
        grabber = KualaStyleGraber(driver, lang_index)
    elif prefix_lower == 'morlevi':
        grabber = MorleviGraber(driver, lang_index)
    elif prefix_lower == 'visualdg':
        grabber = VisualDGGraber(driver, lang_index)
    elif prefix_lower == 'wallashop':
        grabber = WallaShopGraber(driver, lang_index)
    elif prefix_lower == 'wallmart':
        grabber = WallmartGraber(driver, lang_index)
    else:
         # Логгирование, если грабер для префикса не найден
         logger.debug(f'грабер для префикса поставщика не найден: {supplier_prefix}')


    # Возврат найденного грабера или None
    return grabber
