# Module for loading locales data from JSON file
===============================================================

The module contains functions for loading and processing locales data from a JSON file.

## Table of Contents

- [Functions](#functions)
    - [get_locales](#get_locales)

## Functions

### get_locales

```python
def get_locales(locales_path: Path | str) -> list[dict[str, str]] | None:
    """Загружает данные о языках из JSON-файла.

    Args:
        locales_path (Path): Путь к JSON-файлу, содержащему данные о языках.

    Returns:
        list[dict[str, str]]: Список словарей с парами "язык-валюта".

    Examples:
        >>> from src.suppliers.suppliers_list.aliexpress.utils.locales import load_locales_data
        >>> locales = load_locales_data(Path('/path/to/locales.json'))
        >>> print(locales)
        [{'EN': 'USD'}, {'HE': 'ILS'}, {'RU': 'ILS'}, {'EN': 'EUR'}, {'EN': 'GBR'}, {'RU': 'EUR'}]
    """
    locales = j_loads_ns(locales_path)
    return locales.locales or None
```

**Purpose**: This function loads locales data from a JSON file.

**Parameters**:

- `locales_path` (Path): Path to the JSON file containing locales data.

**Returns**:

- `list[dict[str, str]] | None`: A list of dictionaries with locale and currency pairs, or `None` if the file does not exist or the data is invalid.

**Raises Exceptions**:

- `FileNotFoundError`: If the specified file does not exist.
- `json.JSONDecodeError`: If the file contains invalid JSON data.

**How the Function Works**:

1. The function uses the `j_loads_ns` function from `src.utils.jjson` to load the JSON data from the specified file.
2. The function checks if the loaded data has a "locales" key and returns the value associated with that key. If the key is not found or the value is not a list, the function returns `None`.

**Examples**:

```python
from src.suppliers.suppliers_list.aliexpress.utils.locales import get_locales

# Load locales data from a JSON file
locales = get_locales(Path('/path/to/locales.json'))

# Print the locales data
if locales:
    print(locales)
else:
    print('Locales data not found.')
```