## \file /src/suppliers/suppliers_list/aliexpress_com/campaign/_experiments/deals_from_xls.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.campaign._experiments
    :platform: Windows, Unix
    :synopsis: Module for parsing deals from XLS files.

This module provides functionality to parse deal information from XLS files generated
from the AliExpress partner portal (portals.aliexpress_com.com).

Example usage
-------------

```python
    from src.suppliers.suppliers_list.aliexpress_com.campaign._experiments.deals_from_xls import DealsFromXLS

    # Example of parsing deals from an XLS file
    # deals_parser = DealsFromXLS(language='EN', currency= 'USD')
    # for deal in deals_parser.get_next_deal():
    #     print(deal)
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/suppliers_list/aliexpress_com/campaign/_experiments/deals_from_xls.py
"""



""" XLS table parser, generated in the personal account of portals.aliexpress_com.com"""
...
import header
from src.suppliers.suppliers_list.aliexpress.deals_from_xls import DealsFromXLS
from src.utils.printer import pprint

deals_parser = DealsFromXLS(language='EN', currency= 'USD')

for deal in deals_parser.get_next_deal():
    pprint(deal)
    ...
...
