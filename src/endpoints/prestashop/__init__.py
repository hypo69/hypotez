## \file /src/endpoints/prestashop/__init__.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.endpoints.prestashop 
	:platform: Windows, Unix
	:synopsis:

"""


# from .supplier import PrestaSupplier
# from .category import PrestaCategory, PrestaCategoryAsync
# from .warehouse import PrestaWarehouse
# from .language_async import PrestaLanguageAync
# from .shop import PrestaShopShop
# from .pricelist import PriceListRequester
# from .customer import PrestaCustomer

from .product_fields import ProductFields

from .api.api import PrestaShop
from .api.api_async import PrestaShopAsync
from .product import PrestaProduct
from .product_async import PrestaProductAsync
