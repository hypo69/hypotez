## \file /src/endpoints/prestashop/supplier.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.endpoints.prestashop.supplier 
	:platform: Windows, Unix
	:synopsis:

"""


from types import SimpleNamespace
from typing import Optional
import header
from src import gs
from src.logger.logger import logger
from src.utils.jjson import j_loads_ns
from .api import PrestaShop


class PrestaSupplier(PrestaShop):
    """Класс для работы с поставщиками PrestaShop."""
    
    def __init__(self, 
                 credentials: Optional[dict | SimpleNamespace] = None, 
                 api_domain: Optional[str] = None, 
                 api_key: Optional[str] = None, 
                 *args, **kwargs):
        """Инициализация поставщика PrestaShop.

        Args:
            credentials (Optional[dict | SimpleNamespace], optional): Словарь или объект SimpleNamespace с параметрами `api_domain` и `api_key`. Defaults to None.
            api_domain (Optional[str], optional): Домен API. Defaults to None.
            api_key (Optional[str], optional): Ключ API. Defaults to None.
        """
        super().__init__(
            api_key=api_key, 
            api_domain=api_domain,
            *args,
            **kwargs,
        )

    def get_suppliers_dict(self, id_supplier:Optional[int] = None) -> dict:
        """Получить словарь поставщиков.
        Returns:
            dict: Словарь поставщиков.
        """
        kwargs = {'data_format': 'JSON'}
        return self.read(resource='suppliers', resource_id=id_supplier, **kwargs)
