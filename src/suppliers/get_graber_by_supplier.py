## \file /src/suppliers/get_graber_by_supplier.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль вохвращает экземпляр грабера (Graber) для каждого конкретного поставщика.

```rst
.. :module:: src.suppliers.get_graber_by_supplier 
```

"""


import importlib
from urllib.parse import urlparse
from src.logger import logger


def get_graber_by_supplier_prefix(supplier_prefix: str):
    """! Возвращает класс Graber для данного ключа поставщика.

    Args:
        supplier_prefix (str): Ключ поставщика, например 'aliexpress'

    Returns:
        Type[Graber]: Класс Graber

    Raises:
        ValueError: Если класс для поставщика не найден
    """
    supplier_alias: str = supplier_prefix.replace('.', '_').replace('-', '_')
    module_path = f"src.suppliers.suppliers_list.{supplier_alias}.graber"

    try:
        graber_module = importlib.import_module(module_path)
        return getattr(graber_module, "Graber")
    except Exception as ex:
        raise ValueError(f"Graber class not found for supplier: {supplier_alias}") from ex


def get_graber_by_supplier_url(url: str):
    """! Возвращает класс Graber по входному URL, соответствующий известному поставщику.

    Args:
        url (str): Исходный URL (например, 'https://aliexpress.com/item/abc123')

    Returns:
        Type[Graber]: Класс Graber

    Raises:
        ValueError: Если URL не соответствует ни одному из известных поставщиков
    """
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path
    domain = domain.split(':')[0].replace('www.', '')
    supplier_key = domain.replace('.', '_').replace('-', '_')

    try:
        return get_graber_by_supplier_prefix(supplier_key)
    except Exception as ex:
        logger.critical(f"Graber not found for domain: {domain}", ex, exc_info=True)
        raise ValueError(f"Graber not found for domain: {domain}") from ex
