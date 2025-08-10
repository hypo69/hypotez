## \file /src/suppliers/scenario/_experiments/amazon_murano_glass.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.scenario._experiments
    :platform: Windows, Unix
    :synopsis: Example for Amazon Murano Glass scenario.

This module contains an example of running a scenario for Amazon Murano Glass.

Example usage
-------------

```python
    import asyncio
    from src.suppliers.scenario._experiments.amazon_murano_glass import s

    async def main():
        # Assuming 'scenario' and 's' are defined elsewhere and properly initialized
        # s.run_scenario(scenario['Murano Glass'])
        pass

    if __name__ == "__main__":
        asyncio.run(main())
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: src/suppliers/scenario/_experiments/amazon_murano_glass.py
"""

import header
#from header import j_dumps, j_loads,  logger, Category, Product, Supplier, gs, start_supplier
from header import start_supplier
s = start_supplier('amazon')
""" s - throughout the code means the `Supplier` class """

from dict_scenarios import scenario
s.run_scenario(scenario['Murano Glass'])

k = list(s.current_scenario['presta_categories']['default_category'].keys())[0]
