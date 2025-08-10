## \file /src/suppliers/get_graber_by_supplier.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
This module returns a Graber instance for each specific supplier.

```rst
.. :module:: src.suppliers.get_graber_by_supplier
```

"""


import importlib
from token import OP
from urllib.parse import urlparse
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.suppliers.graber import GraberBase
    from src.webdriver.pydoll import Driver
from src.logger import logger

def dynamic_import_graber(supplier_alias: str) -> Optional['GraberBase']:
    """Dynamically imports the Graber class by supplier_alias.

    Args:
        supplier_alias (str): Supplier alias, e.g., "morlevi_co_il".

    Returns:
        Optional[type[Graber]]: The Graber class, if found, otherwise None.
    """
    module_path = f"src.suppliers.suppliers_list.{supplier_alias}.graber"
    try:
        module = importlib.import_module(module_path)
        return getattr(module, "Graber")
    except ModuleNotFoundError:
        logger.error(f"Module {module_path} not found")
    except AttributeError:
        logger.error(f"Graber class not found in module {module_path}")
    except Exception as ex:
        logger.critical(f"Error importing Graber from {module_path}", ex, True)
    return None

def get_graber_by_supplier_prefix(supplier_prefix: str, driver:'Driver') -> Optional['GraberBase']:
    """Returns a Graber instance for the given supplier key.

    Args:
        supplier_prefix (str): Supplier key, e.g., 'aliexpress'
        driver (Driver): Web content driver. Can be one of the types: `selenium`, `pydoll`, `llm_driver`, `playwright`, ...

    Returns:
        Graber: Graber instance

    Raises:
        ValueError: If no instance is found for the supplier
    """
    supplier_alias: str = supplier_prefix.replace('.', '_').replace('-', '_')
    GraberClass = dynamic_import_graber(supplier_alias)
    if GraberClass:
        try:
            return GraberClass(supplier_prefix = supplier_prefix, driver = driver)
        except Exception as ex:
            logger.critical(f"Failed to create Graber instance for {supplier_alias}", ex, True)
            ...
    return None


def get_graber_by_supplier_url(url: str, driver:'Driver') -> Optional['GraberBase']:
    """Returns a Graber instance by input URL, corresponding to a known supplier.

    Args:
        url (str): Source URL (e.g., 'https://aliexpress.com/item/abc123')
        driver (Driver): Web content driver. Can be one of the types: `selenium`, `pydoll`, `llm_driver`, `playwright`, ...

    Returns:
        Graber: Graber instance

    Raises:
        ValueError: If the URL does not match any known suppliers
    """
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path
    domain = domain.split(':')[0].replace('www.', '')

    try:
        return get_graber_by_supplier_prefix(domain, driver)
    except Exception as ex:
        logger.critical(f"Graber not found for domain: {domain}", ex, exc_info=True)
        #raise ValueError(f"Graber not found for domain: {domain}") from ex
        return
