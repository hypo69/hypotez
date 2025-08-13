# # \file /src/endpoints/prestashop/customer.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

""".. module:: src.endpoints.prestashop 
	:platform: Windows, Unix
	:synopsis:"""



import sys
import os
from attr import attr, attrs
from pathlib import Path
from typing import Union
from types import SimpleNamespace

import header
from src import gs
from src.logger.logger import logger
from src.utils.jjson import j_loads as j_loads
from .api import PrestaShop
from src.logger.logger import logger
from src.logger.exceptions import PrestaShopException

from typing import Optional

class PrestaCustomer(PrestaShop):
    """Class for working with clients in Prestashop.

    Example of class use:

    .. Code-Block :: Python

        Prestacustomer = Prestacustomer (API_Domain = API_Domain, API_KEY = API_KEY)
        PRESTACustomer.Add_customer_Prestashop ('John Doe', 'Johndoe@example.com')
        Prestacustomer.delete_customer_prestashop (3)
        PRESTACER.UPDATE_CUSTOMER_PRESTASHOP (4, 'Updated Customer Name')
        Print (Prestacustomer.get_customer_details_prestashop (5))"""
    
    def __init__(self, 
                 credentials: Optional[dict | SimpleNamespace] = None, 
                 api_domain: Optional[str] = None, 
                 api_key: Optional[str] = None, 
                 *args, **kwargs):
        """Pristashop client initialization.

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
