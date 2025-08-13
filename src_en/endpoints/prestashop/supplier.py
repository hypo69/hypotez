# # \file /src/endpoints/prestashop/supplier.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

""".. module:: src.endpoints.prestashop.supplier 
	:platform: Windows, Unix
	:synopsis:"""


from types import SimpleNamespace
from typing import Optional
import header
from src import gs
from src.logger.logger import logger
from src.utils.jjson import j_loads_ns
from .api import PrestaShop


class PrestaSupplier(PrestaShop):
    """Class for working with Prestashop suppliers."""
    
    def __init__(self, 
                 credentials: Optional[dict | SimpleNamespace] = None, 
                 api_domain: Optional[str] = None, 
                 api_key: Optional[str] = None, 
                 *args, **kwargs):
        """Initialization of the Prestashop supplier.

        Args:
            Credentials (Optional [Dict | Simplenamespace], Optional): Dictionary or object Simplenamespace with `API_Domain` and` API_KEY` parameters. Defaults to None.
            API_DOMAIN (Optional [Str], Optional): API domain. Defaults to None.
            API_KEY (Optional [str], Optional): API key. Defaults to None."""
        super().__init__(
            api_key=api_key, 
            api_domain=api_domain,
            *args,
            **kwargs,
        )

    def get_suppliers_dict(self, id_supplier:Optional[int] = None) -> dict:
        """Get a dictionary of suppliers.
        Returns:
            Dict: Dictionary of suppliers."""
        kwargs = {'data_format': 'JSON'}
        return self.read(resource='suppliers', resource_id=id_supplier, **kwargs)
