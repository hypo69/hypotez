## \file /src/suppliers/suppliers_list/aliexpress_com/utils/locales.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
.. module:: src.suppliers.suppliers_list.aliexpress_com.utils.locales
    :platform: Windows, Unix
    :synopsis: Module for loading locale data from a JSON file for AliExpress operations.

AliExpress Locales Management
=========================================================================================

This module handles the loading and processing of locale data (language and currency pairs)
from a JSON configuration file, specifically for AliExpress-related functionalities.

Example usage
-------------

```python
    from pathlib import Path
    from src.suppliers.suppliers_list.aliexpress_com.utils.locales import get_locales

    # Assuming 'locales.json' is in the same directory or a known path
    locales_file_path = Path(__file__).parent / 'locales.json'
    loaded_locales = get_locales(locales_file_path)

    if loaded_locales:
        print(f"Loaded Locales: {loaded_locales}")
        # Example output: [{'EN': 'USD'}, {'HE': 'ILS'}]
    else:
        print("Failed to load locales or no locales found.")
```

:author: hypo69
:license: Proprietary. All rights reserved.
:version: 1.0.0
:location: suppliers/suppliers_list/aliexpress_com/utils/locales.py
"""


from pathlib import Path

from src import gs
from src.utils.jjson import j_loads, j_loads_ns

def get_locales(locales_path: Path | str) -> list[dict[str, str]] | None:
    """Load locales data from a JSON file.

    Args:
        path (Path): Path to the JSON file containing locales data.

    Returns:
        list[dict[str, str]]: List of dictionaries with locale and currency pairs.

    Examples:
        >>> from src.suppliers.suppliers_list.aliexpress_com.utils.locales import load_locales_data
        >>> locales = load_locales_data(Path('/path/to/locales.json'))
        >>> print(locales)
        [{'EN': 'USD'}, {'HE': 'ILS'}, {'RU': 'ILS'}, {'EN': 'EUR'}, {'EN': 'GBR'}, {'RU': 'EUR'}]
    """
    locales = j_loads_ns(locales_path)
    return locales.locales or None

locales: list[dict[str, str]] | None = get_locales (gs.path.src / 'suppliers' / 'suppliers_list' / 'aliexpress_com' / 'utils' / 'locales.json') # defined locales for campaigns
