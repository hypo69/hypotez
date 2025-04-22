### **Анализ кода модуля `get_graber_by_supplier`**

## \file /src/suppliers/get_graber_by_supplier.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для получения граббера на основе URL поставщика
=========================================================================================

Этот модуль предоставляет функциональность для получения соответствующего объекта граббера
для заданного URL поставщика. У каждого поставщика есть свой собственный граббер, который
извлекает значения полей из целевой HTML-страницы.

Пример использования
---------------------

.. code-block:: python

    from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_url
    from src.webdriver import WebDriver

    driver = WebDriver()
    url = 'https://www.example.com'
    graber = get_graber_by_supplier_url(driver, url)

    if graber:
        # Использовать граббер для извлечения данных
        pass
    else:
        # Обработать случай, когда граббер не найден
        pass
"""
from typing import Optional
import header
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


def get_graber_by_supplier_url(driver: 'Driver', url: str, lang_index:int ) -> Graber | None:
    """
    Функция возвращает соответствующий граббер для заданного URL поставщика.

    У каждого поставщика есть свой граббер, который извлекает значения полей из целевой HTML-страницы.

    Args:
        driver: Инстанс драйвера, используемый для граббинга.
        url (str): URL страницы поставщика.
        lang_index (int): Индекс языка для магазина Prestashop.
    Returns:
        Graber | None: Объект граббера, если соответствие найдено, иначе None.
    """
    driver.get_url(url)
    # Проверка, начинается ли URL с одного из указанных префиксов для каждого поставщика.
    if url.startswith(('https://aliexpress.com', 'https://wwww.aliexpress.com')):# aliexpress
        return AliexpressGraber(driver,lang_index)

    if url.startswith(('https://amazon.com', 'https://wwww.amazon.com')):# amazon
        return AmazonGraber(driver,lang_index)

    if url.startswith(('https://bangood.com', 'https://wwww.bangood.com')):# bangood
        return BangoodGraber(driver,lang_index)

    if url.startswith(('https://cdata.co.il', 'https://wwww.cdata.co.il')):# cdata
        return CdataGraber(driver,lang_index)

    if url.startswith(('https://ebay.', 'https://wwww.ebay.')):# ebay
        return EbayGraber(driver,lang_index)

    if url.startswith(('https://etzmaleh.co.il','https://www.etzmaleh.co.il')):# etzmaleh
        return EtzmalehGraber(driver,lang_index)

    if url.startswith(('https://gearbest.com', 'https://wwww.gearbest.com')):# gearbest
        return GearbestGraber(driver,lang_index)

    if url.startswith(('https://grandadvance.co.il', 'https://www.grandadvance.co.il')):# grandadvance
        return GrandadvanceGraber(driver,lang_index)

    if url.startswith(('https://hb-digital.co.il', 'https://www.hb-digital.co.il')):# hb
        return HBGraber(driver,lang_index)

    if url.startswith(('https://ivory.co.il', 'https://www.ivory.co.il')):# ivory
        return IvoryGraber(driver,lang_index)

    if url.startswith(('https://ksp.co.il', 'https://www.ksp.co.il')):# ksp
        return KspGraber(driver,lang_index)

    if url.startswith(('https://kualastyle.com', 'https://www.kualastyle.com')):# kualastyle
        return KualaStyleGraber(driver,lang_index)

    if url.startswith(('https://morlevi.co.il', 'https://www.morlevi.co.il')):# morlevi
        return MorleviGraber(driver,lang_index)

    if url.startswith(('https://www.visualdg.com', 'https://visualdg.com')):# visualdg
        return VisualDGGraber(driver,lang_index)

    if url.startswith(('https://wallashop.co.il', 'https://www.wallashop.co.il')):# wallashop
        return WallaShopGraber(driver,lang_index)

    if url.startswith(('https://www.wallmart.com', 'https://wallmart.com')):# wallmart
        return WallmartGraber(driver,lang_index)
    # Логирование, если граббер не найден для данного URL.
    logger.debug(f'No graber found for URL: {url}')
    ...
    return

def get_graber_by_supplier_prefix(driver: 'Driver', supplier_prefix: str, lang_index:str = '2' ) -> Optional[Graber] | bool:
    """Функция возвращает граббер по префиксу поставщика"""
    ...
    # Проверка соответствия префикса и создание соответствующего граббера.
    if supplier_prefix == 'aliexpress':# aliexpress
        grabber = AliexpressGraber(driver,lang_index)
    if supplier_prefix == 'amazon':# amazon
        grabber = AmazonGraber(driver,lang_index)
    if supplier_prefix == 'ebay':# ebay
        grabber = EbayGraber(driver,lang_index)
    if supplier_prefix == 'gearbest':# gearbest
        grabber = GearbestGraber(driver,lang_index)
    if supplier_prefix == 'grandadvance':# grandadvance
        grabber = GrandadvanceGraber(driver,lang_index)
    if supplier_prefix == 'hb':# hb
        grabber = HBGraber(driver,lang_index)
    if supplier_prefix == 'ivory':# ivory
        grabber = IvoryGraber(driver,lang_index)
    if supplier_prefix == 'ksp':# ksp
        grabber = KspGraber(driver,lang_index)
    if supplier_prefix == 'kualastyle':# kualastyle
        grabber = KualaStyleGraber(driver,lang_index)
    if supplier_prefix == 'morlevi':# morlevi
        grabber = MorleviGraber(driver,lang_index)
    if supplier_prefix == 'visualdg':# visualdg
        grabber = VisualDGGraber(driver,lang_index)
    if supplier_prefix == 'wallashop':# wallashop
        grabber = WallaShopGraber(driver,lang_index)
    if supplier_prefix == 'wallmart':# wallmart
        grabber = WallmartGraber(driver,lang_index)
    # Возвращает объект граббера или False, если соответствие не найдено.
    return grabber or False
```

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код хорошо структурирован и легко читается.
    - Присутствуют docstring для функций, что облегчает понимание их назначения.
    - Используется модуль `logger` для логирования.
- **Минусы**:
    - docstring для функции `get_graber_by_supplier_url` на английском языке.
    - Функция `get_graber_by_supplier_prefix` имеет пустой docstring.
    - В функции `get_graber_by_supplier_prefix` не указан тип для `lang_index:str = '2'`.
    - Есть дублирование проверок URL в `get_graber_by_supplier_url`.
    - Не все переменные аннотированы типами.

**Рекомендации по улучшению:**

- Перевести docstring для `get_graber_by_supplier_url` на русский язык.
- Добавить подробный docstring для функции `get_graber_by_supplier_prefix` на русском языке.
- Указать тип `lang_index` в функции `get_graber_by_supplier_prefix` как `int`.
- Избавиться от дублирования проверок URL, используя, например, словарь соответствий URL и грабберов.
- Аннотировать все переменные типами.

**Оптимизированный код:**

```python
## \file /src/suppliers/get_graber_by_supplier.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для получения граббера на основе URL поставщика
=========================================================================================

Этот модуль предоставляет функциональность для получения соответствующего объекта граббера
для заданного URL поставщика. У каждого поставщика есть свой собственный граббер, который
извлекает значения полей из целевой HTML-страницы.

Пример использования
---------------------

.. code-block:: python

    from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_url
    from src.webdriver import WebDriver

    driver = WebDriver()
    url = 'https://www.example.com'
    graber = get_graber_by_supplier_url(driver, url)

    if graber:
        # Использовать граббер для извлечения данных
        pass
    else:
        # Обработать случай, когда граббер не найден
        pass
"""
from typing import Optional, Type
import header
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


def get_graber_by_supplier_url(driver: 'Driver', url: str, lang_index: int) -> Graber | None:
    """
    Функция возвращает соответствующий граббер для заданного URL поставщика.

    У каждого поставщика есть свой граббер, который извлекает значения полей из целевой HTML-страницы.

    Args:
        driver: Инстанс драйвера, используемый для граббинга.
        url (str): URL страницы поставщика.
        lang_index (int): Индекс языка для магазина Prestashop.

    Returns:
        Graber | None: Объект граббера, если соответствие найдено, иначе None.
    """
    # Словарь соответствий префиксов URL и классов грабберов
    grabbers: dict[tuple[str, ...], Type[Graber]] = {
        ('https://aliexpress.com', 'https://wwww.aliexpress.com'): AliexpressGraber,
        ('https://amazon.com', 'https://wwww.amazon.com'): AmazonGraber,
        ('https://bangood.com', 'https://wwww.bangood.com'): BangoodGraber,
        ('https://cdata.co.il', 'https://wwww.cdata.co.il'): CdataGraber,
        ('https://ebay.', 'https://wwww.ebay.'): EbayGraber,
        ('https://etzmaleh.co.il', 'https://www.etzmaleh.co.il'): EtzmalehGraber,
        ('https://gearbest.com', 'https://wwww.gearbest.com'): GearbestGraber,
        ('https://grandadvance.co.il', 'https://www.grandadvance.co.il'): GrandadvanceGraber,
        ('https://hb-digital.co.il', 'https://www.hb-digital.co.il'): HBGraber,
        ('https://ivory.co.il', 'https://www.ivory.co.il'): IvoryGraber,
        ('https://ksp.co.il', 'https://www.ksp.co.il'): KspGraber,
        ('https://kualastyle.com', 'https://www.kualastyle.com'): KualaStyleGraber,
        ('https://morlevi.co.il', 'https://www.morlevi.co.il'): MorleviGraber,
        ('https://www.visualdg.com', 'https://visualdg.com'): VisualDGGraber,
        ('https://wallashop.co.il', 'https://www.wallashop.co.il'): WallaShopGraber,
        ('https://www.wallmart.com', 'https://wallmart.com'): WallmartGraber,
    }
    driver.get_url(url)
    # Функция извлекает граббер на основе URL поставщика
    for prefixes, grabber_class in grabbers.items():# итерация по словарю grabbers
        if url.startswith(prefixes):# Если URL начинается с одного из префиксов
            return grabber_class(driver, lang_index)  # Функция возвращает инстанс граббера для соответствующего URL

    # Логирование, если граббер не найден для данного URL.
    logger.debug(f'No graber found for URL: {url}')
    ...
    return


def get_graber_by_supplier_prefix(driver: 'Driver', supplier_prefix: str, lang_index: int = 2) -> Optional[Graber] | bool:
    """
    Функция возвращает соответствующий граббер для заданного префикса поставщика.

    Args:
        driver: Инстанс драйвера, используемый для граббинга.
        supplier_prefix (str): Префикс поставщика.
        lang_index (int): Индекс языка для магазина Prestashop.

    Returns:
        Graber | bool: Объект граббера, если соответствие найдено, иначе False.
    """

    # Словарь соответствий префиксов поставщиков и классов грабберов
    grabbers: dict[str, Type[Graber]] = {
        'aliexpress': AliexpressGraber,
        'amazon': AmazonGraber,
        'ebay': EbayGraber,
        'gearbest': GearbestGraber,
        'grandadvance': GrandadvanceGraber,
        'hb': HBGraber,
        'ivory': IvoryGraber,
        'ksp': KspGraber,
        'kualastyle': KualaStyleGraber,
        'morlevi': MorleviGraber,
        'visualdg': VisualDGGraber,
        'wallashop': WallaShopGraber,
        'wallmart': WallmartGraber,
    }
    # Функция проверяет соответствие префикса и создание соответствующего граббера.
    grabber: Optional[Graber] = grabbers.get(supplier_prefix)(driver, lang_index) if supplier_prefix in grabbers else None # Функция извлекает граббер на основе префикса поставщика
    # Возвращает объект граббера или False, если соответствие не найдено.
    return grabber or False