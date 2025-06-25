## \file /src/suppliers/suppliers_list/aliexpress/graber_via_pydoll.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для сбора данных о товарах с Aliexpress с изпользованием библиотеки `pydoll`.
=========================================================================================

rst```
.. module:: src.suppliers.suppliers_list.aliexpress.graber_via_pydoll 
```

"""
from pathlib import Path
from types import SimpleNamespace
from typing import Optional, List

from pydoll.browser.chrome import Chrome
from pydoll.constants import By
from pydoll.browser.page import Page

from header import __root__
from src import gs
from src.endpoints.prestashop.product_fields import ProductFields
from src.webdriver.executor_pydoll import execute_locator
from src.utils.file import get_filenames_from_directory
from src.utils.jjson import j_loads_ns
from src.utils.image import save_image_async, save_image_from_url_async

from src.logger.logger import logger


class Config:
    ENDPOINT: Path = __root__ / 'src' / 'suppliers' / 'suppliers_list' / 'aliexpress' 

    actual_fields:list = ['id_supplier',                                                              
                         'name',
                         'price',
                         'reference',
                         'description',
                         'description_short',
                         'default_image_url',
                         'local_image_path',]

    product_locators:SimpleNamespace = j_loads_ns(ENDPOINT / 'locators' / 'product.json')
    category_locators:SimpleNamespace = j_loads_ns(ENDPOINT / 'locators' / 'category.json')


async def fetch_product_fields(page: Page, actual_fields:Optional[list] = None) -> ProductFields:
    """Grab product fields."""
    
    actual_fields = actual_fields or Config.actual_fields
    locator:SimpleNamespace = Config.product_locators
    current_url = await page.current_url

    async def save_local_image(f) -> bool:
        """Fetch and save an image locally.

        Функция получает `URL` картинки или байты изображения, сохраняет изображение в формате `PNG` в директории `tmp` 
        и устанавливает путь к сохранённой картинке в поле `local_image_path`.
        """
        try:
            # Получаем результат из локатора как `bytes` или `str`(url)
            image_url:str = f.default_image_url
            img_path:Path = Path(gs.path.tmp / f'{f.id_supplier}_{f.reference}.png')
            await save_image_from_url_async(image_url, img_path)
            return img_path
        except Exception as ex:
            logger.error(f'Ошибка сохранения изображения в поле `local_image_path`', ex)
            ...
            return None


    f:ProductFields = ProductFields()

    f.id_supplier = locator.id_supplier.attribute
    f.name = await execute_locator(page, locator.name)
    f.reference = current_url.split("/item/")[1].split(".html")[0]
    f.price = await execute_locator(page, locator.price)

    if 'description' in actual_fields:
        f.description = await execute_locator(page, locator.description)
    if 'description_short' in actual_fields:
        f.description_short = await execute_locator(page, locator.description_short)
    if 'default_image_url' in actual_fields:
        f.default_image_url = await execute_locator(page, locator.default_image_url)
    if 'local_image_path' in actual_fields:
        f.local_image_path = await save_local_image(f)

    return f

async def grab_product_page( page: Page, product_url: str, actual_fields:Optional[list] = None) -> ProductFields:
    """
    Загружает страницу товара по URL и возвращает структуру данных ProductFields.
    Поддерживаются входные URL формата:
        //he.aliexpress.com/item/
        https://he.aliexpress.com/item/
        he.aliexpress.com/item/
    """

    if product_url.startswith('//'):
        url = f'https:{product_url}'
    elif product_url.startswith('http://') or product_url.startswith('https://'):
        url = product_url
    else:
        url = f'https://{product_url.lstrip("/")}'

    await page.go_to(url)
    return await fetch_product_fields(product_url, page, actual_fields or Config.actual_fields)

async def get_product_urls_from_category_page(category_url:str, locator:SimpleNamespace, page: Page) -> List[str]:
    """Get product URLs from the current page.
   Отдельная функция для каждого поставщика, так как локаторы могут отличаться.
    """
    await page.go_to(category_url)
    product_urls = await execute_locator(page, locator)
    return product_urls
