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
from token import OP
from urllib.parse import urlparse
from typing import List, Optional
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.suppliers.graber import GraberBase
    from src.webdriver.driverless.use_pydoll import Driver

from src.logger import logger
from src.suppliers.graber import GraberBase

def dynamic_import_graber(supplier_alias: str) -> Optional['GraberBase']:
    """Динамически импортирует Graber класс по supplier_alias.

    Args:
        supplier_alias (str): Алиас поставщика, например "morlevi_co_il".

    Returns:
        Optional[type[Graber]]: Класс Graber, если найден, иначе None.
    """
    module_path = f"src.suppliers.suppliers_list.{supplier_alias}.graber"
    try:
        module = importlib.import_module(module_path)
        return getattr(module, "Graber")
    except ModuleNotFoundError:
        logger.error(f"Модуль {module_path} не найден")
    except AttributeError:
        logger.error(f"Класс Graber не найден в модуле {module_path}")
    except Exception as ex:
        logger.critical(f"Ошибка при импорте Graber из {module_path}", ex, True)
    return None

def get_graber_by_supplier_prefix(supplier_prefix: str, driver:'Driver') -> Optional['GraberBase']:
    """ Возвращает экземпляр Graber для данного ключа поставщика.

    Args:
        supplier_prefix (str): Ключ поставщика, например 'aliexpress'
        driver (Driver): Драйвер для вебконтанта. Может быть одним из типов: `selenium`, `pydoll`, `llm_driver`, `playwright` , ...

    Returns:
        Graber: Экземпляр Graber

    Raises:
        ValueError: Если экземпляр для поставщика не найден
    """
    supplier_alias: str = supplier_prefix.replace('.', '_').replace('-', '_')
    GraberClass = dynamic_import_graber(supplier_alias)
    if GraberClass:
        try:
            return GraberClass(driver = driver)
        except Exception as ex:
            logger.critical(f"Не удалось создать экземпляр Graber для {supplier_alias}", ex, True)
    return None


def get_graber_by_supplier_url(url: str, driver:'Driver') -> Optional['GraberBase']:
    """ Возвращает экземпляр Graber по входному URL, соответствующий известному поставщику.

    Args:
        url (str): Исходный URL (например, 'https://aliexpress.com/item/abc123')
        driver (Driver): Драйвер для вебконтанта. Может быть одним из типов: `selenium`, `pydoll`, `llm_driver`, `playwright` , ...

    Returns:
        Graber: Экземпляр Graber

    Raises:
        ValueError: Если URL не соответствует ни одному из известных поставщиков
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
