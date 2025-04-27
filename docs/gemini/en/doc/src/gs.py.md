# Module Name: `gs`

## Overview

This module provides a simple mechanism for loading program parameters without using the KeePass password manager. It's highly discouraged to use this method for storing sensitive information as it lacks security and convenience compared to KeePass.

## Details

The module defines a global variable `gs` which is populated with data from the `config.json` file located within the project. This file contains key configurations, API keys, passwords, and other program-specific settings. 

**Important Considerations:**

- **Security:** Storing credentials in plain text files (.env) is highly insecure. Sensitive information should always be encrypted and stored securely, ideally in a dedicated password manager like KeePass.
- **Maintainability:** This approach can lead to difficulties in managing and updating configurations as the application grows.  KeePass provides a more structured and organized way to store and manage sensitive data.


## Classes

This module does not define any classes.

## Functions

This module does not define any functions.

## Parameter Details

- **`gs`:** This global variable stores the contents of the `config.json` file as a dictionary. It is intended to hold key program parameters and configurations.

## Examples

```python
import header
from header import __root__
from src.utils.jjson import j_loads_ns
from pathlib import Path

gs = j_loads_ns(__root__ / 'src' / 'config.json')
```

In this example, the module loads the configuration data from the `config.json` file and stores it in the `gs` dictionary. This allows the application to access the configuration parameters throughout its execution. 

**For example, to access the API key:**

```python
api_key = gs['api_key']
```

**Note:** This approach is strongly discouraged for storing sensitive information like API keys or passwords. You should use KeePass for this purpose.