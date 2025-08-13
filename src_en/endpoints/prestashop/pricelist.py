# # \file /src/endpoints/prestashop/pricelist.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

""".. Module :: src.endpoints.prestashop
    : Platform: Windows, Unix
    : synopsis: module for working with requests from the Prestashop price list."""


import sys
import os
from attr import attr, attrs
from pathlib import Path
from typing import Union, Dict, Any, List

import header
from src import gs
from src.logger.logger import logger
from src.utils.jjson import j_loads, j_loads_ns
from .api import PrestaShop
from types import SimpleNamespace


class PriceListRequester(PrestaShop):
    """Class for requesting a price list.

    Args:
        Prestashop: Basic class for working with API Prestashop."""

    def __init__(self, api_credentials: Dict[str, str]) -> None:
        """Initializes the object of the Pricelistrequester class.

        Args:
            API_Credentials (DICT [STR, StR]): Dictionary with accounting data for API,
                Including 'API_Domain' and 'API_KEY'.

        Returns:
            None"""
        super().__init__(api_credentials['api_domain'], api_credentials['api_key'])

    def request_prices(self, products: List[str]) -> Dict[str, float]:
        """Requests a list of prices for these goods.

        Args:
            Products (List [str]): a list of goods for which you need to get prices.

        Returns:
            DICT [str, float]: a dictionary where the goods are with the keys, and the values are their prices.
                For example: {'Product1': 10.99, 'Product2': 5.99}"""
        # Here is a code to send a request for prices from a data source
        ...
        return {}

    def update_source(self, new_source: str) -> None:
        """Updates the data source for price request.

        Args:
            New_Source (str): a new data source.

        Returns:
            None"""
        self.source = new_source

    def modify_product_price(self, product: str, new_price: float) -> None:
        """Modifies the price of the specified product.

        Args:
            Product (StR): Product name.
            New_Price (Float): New Product price.

        Returns:
            None"""
        # Here the code to change the price of the goods in the data source
        ...