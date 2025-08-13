# # \file /src/endpoints/prestashop/category.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""`` `RST
  .. Module :: src.endpoints.prestashop.category
`` `
Category management module in Prestashop.
=====================================================
Contains the PrestaCategory class, which allows
Get information about parental categories.

Module classes:
-------------
- Prestacategory - class for managing categories in Prestashop."""

from typing import List, Dict, Optional
from types import SimpleNamespace
import asyncio
from src.logger.logger import logger
from src.utils.jjson import j_loads, j_dumps
from src.endpoints.prestashop.api import PrestaShop, PrestaShopAsync


class PrestaCategory(PrestaShop):
    """Class for managing categories in PrestaShop."""

    def __init__(self, api_key: str, api_domain: str, *args, **kwargs) -> None:
        """Initializes a Product Object.

        Args:
            API_KEY (str): API key for access to Prestashop.
            API_Domain (str): domain name Prestashop.

        Returns:
            None

        Example:
            >>> CATEGORY = PRESTACATEGORY (API_KEY = 'YOUR_API_KEY', API_Domain = 'Your_Domain')"""
        super().__init__(api_key=api_key, api_domain=api_domain, *args, **kwargs)

    def get_parent_categories_list(
        self, id_category: str | int, parent_categories_list: Optional[List[int | str]] = None
    ) -> List[int | str]:
        """Retrieve Parent Categories from Prestashop for a Given Category.

        Args:
            ID_Category (str | int): Categories ID for which you need to get parental categories.
            Parent_categories_List (Optional [List [int | str]], Optional): List of parental categories. Defaults to None.

        Returns:
            List [int | Str]: list of ID of parental categories.

        RAISES:
            Valuerror: if there is no ID category.
            Exception: If an error occurs when receiving data on the category.

        Example:
            >>> CATEGORY = PRESTACATEGORY (API_KEY = 'YOUR_API_KEY', API_Domain = 'Your_Domain')
            >>> Parent_categories = Category.get_part_categories_list (id_category = '10 ')
            >>> Print (Parent_categories)
            [2, 10]"""
        if not id_category:
            logger.error('Missing category ID.')
            return parent_categories_list or []

        category: Optional[Dict] = super().get(
            'categories', resource_id=id_category, display='full', io_format='JSON'
        )
        if not category:
            logger.error('Issue with retrieving categories.')
            return parent_categories_list or []

        _parent_category: int = int(category['id_parent'])
        parent_categories_list = parent_categories_list or []
        parent_categories_list.append(_parent_category)

        if _parent_category <= 2:
            return parent_categories_list
        else:
            return self.get_parent_categories_list(_parent_category, parent_categories_list)
