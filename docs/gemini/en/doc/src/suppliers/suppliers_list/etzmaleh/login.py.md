# Module: src.suppliers.etzmaleh.login

## Overview

This module provides the login functionality for the EtzMaleh supplier, implementing login using a web driver.

## Details

This module is responsible for handling the login process for EtzMaleh. It utilizes a web driver to interact with the supplier's website and authenticate user credentials. 

## Functions

### `login`

**Purpose:** This function implements the login process for the EtzMaleh supplier.

**Parameters:**

- `s` (`Supplier`): The `Supplier` object representing the supplier instance.

**Returns:**

- `bool`: Returns `True` if the login was successful, otherwise `False`.

**Raises Exceptions:**

- `None`

**How the Function Works:**

The `login` function logs the user into the EtzMaleh platform using the provided `Supplier` object. It interacts with the website through a web driver to enter credentials and submit the login form. The function then verifies the login status and returns `True` if the login is successful, `False` otherwise.

**Examples:**

```python
from src.suppliers.etzmaleh.login import login
from src.suppliers.supplier import Supplier

supplier = Supplier(
    supplier_id='etzmaleh',
    login='username',
    password='password',
    ...
)

login_success = login(supplier)
print(f'Login status: {login_success}')
```

**Inner Functions:**

None.