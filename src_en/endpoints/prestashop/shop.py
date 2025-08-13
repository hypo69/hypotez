# # \file /src/endpoints/prestashop/shop.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

""".. module:: src.endpoints.prestashop 
	:platform: Windows, Unix
	:synopsis:"""


from types import SimpleNamespace
from typing import Optional
import header
from src import gs
from src.logger.logger import logger
from src.utils.jjson import j_loads
from .api import PrestaShop
from src.logger.exceptions import PrestaShopException
from pathlib import Path
from attr import attr, attrs
import sys
import os

class PrestaShopShop(PrestaShop):
    """Class for working with Prestashop stores."""
    
    def __init__(self, 
                 credentials: Optional[dict | SimpleNamespace] = None, 
                 api_domain: Optional[str] = None, 
                 api_key: Optional[str] = None, 
                 *args, **kwargs):
        """Initialization of the Prestashop store.

        Args:
            Credentials (Optional [Dict | Simplenamespace], Optional): Dictionary or object Simplenamespace with `API_Domain` and` API_KEY` parameters. Defaults to None.
            API_DOMAIN (Optional [Str], Optional): API domain. Defaults to None.
            API_KEY (Optional [str], Optional): API key. Defaults to None."""
        
        if credentials is not None:
            api_domain = credentials.get('api_domain', api_domain)
            api_key = credentials.get('api_key', api_key)
        
        if not api_domain or not api_key:
            raise ValueError('Необходимы оба параметра: api_domain и api_key.')
        
        super().__init__(api_domain, api_key, *args, **kwargs)
