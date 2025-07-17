# ## \file /src/suppliers/get_pydoll_graber_by_supplier.py
# # -*- coding: utf-8 -*-
# #! .pyenv/bin/python3

# """
# Модуль возвращает экземпляр pydoll грабера (Graber) для каждого конкретного поставщика.
# """

# import importlib
# from urllib.parse import urlparse

# from typing import TYPE_CHECKING, Optional
# if TYPE_CHECKING:
#     from src.suppliers.graber import GraberBase
#     from src.webdriver.driverless.use_pydoll import Driver

# from src.logger import logger


# def dynamic_import_graber(supplier_alias: str)  -> Optional['GraberBase']:
#     """Динамически импортирует Graber класс по supplier_alias.

#     Args:
#         supplier_alias (str): Алиас поставщика, например "morlevi_co_il".

#     Returns:
#         Optional[type[Graber]]: Класс Graber, если найден, иначе None.
#     """
#     module_path = f"src.suppliers.suppliers_list.{supplier_alias}.graber_via_pydoll"
#     try:
#         module = importlib.import_module(module_path)
#         return getattr(module, "Graber")
#     except ModuleNotFoundError:
#         logger.error(f"Модуль {module_path} не найден")
#     except AttributeError:
#         logger.error(f"Класс Graber не найден в модуле {module_path}")
#     except Exception as ex:
#         logger.critical(f"Ошибка при импорте Graber из {module_path}", ex, True)
#     return None


# def get_graber_by_supplier_prefix(supplier_prefix: str,  driver:'Driver') -> Optional['GraberBase']:
#     """Возвращает экземпляр `Graber` для данного префикса поставщика.

#     Args:
#         supplier_prefix (str): Префикс поставщика, например "morlevi" или "morlevi.co.il".

#     Returns:
#         Graber: Экземпляр подходящего Graber или базовый Graber в случае ошибки.
#     """
#     supplier_alias = supplier_prefix.replace('.', '_').replace('-', '_')
#     GraberClass = dynamic_import_graber(supplier_alias)
#     if GraberClass:
#         try:
#             return GraberClass(supplier_prefix = supplier_prefix, driver = driver)
#         except Exception as ex:
#             logger.critical(f"Не удалось создать экземпляр Graber для {supplier_alias}", ex)
#             return None
#     logger.critical(f"Не удалось создать экземпляр Graber для {supplier_alias}", ex)
#     return None


# def get_graber_by_supplier_url(url: str, driver:'Driver') -> Optional['GraberBase']:
#     """
#     Извлекает домен из URL и возвращает экземпляр соответствующего класса Graber.

#     Args:
#         url (str): Входной URL.

#     Returns:
#         Optional[Graber]: Экземпляр подходящего Graber или None при ошибке.
#     """
#     if not url.startswith(('http://', 'https://')):
#         url = 'http://' + url

#     parsed_url = urlparse(url)
#     domain = parsed_url.netloc or parsed_url.path
#     domain = domain.split(':')[0].replace('www.', '')
#     supplier_alias = domain.replace('.', '_').replace('-', '_')

#     GraberClass = dynamic_import_graber(supplier_alias)
#     if GraberClass:
#         try:
#             return GraberClass(supplier_prefix = domain, driver = driver)
#         except Exception as ex:
#             logger.critical(f"Не удалось создать экземпляр Graber для домена {domain}", ex, True)
#             return None

#     logger.critical(f"Graber класс не найден для домена: {domain}")
#     return None
