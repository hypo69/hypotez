# Module: `src.suppliers.cdata.login`

## Overview

This module provides a function for handling authorization within the C-data supplier platform using a web driver. 

## Details

The `login` function is used to authenticate a user on the C-data reseller website. It utilizes web driver interactions to locate and interact with specific web elements (like input fields for email and password, and login buttons) for the authorization process. The `login` function also logs success or failure events for the authorization process. 

## Functions

### `login`

```python
def login(self):
    """ Функция выполняет авторизацию на сайте C-Data.

    Args:
        self: Объект, к которому привязан метод.
    
    Returns:
        bool: Возвращает `True`, если авторизация прошла успешно, иначе `False`.

    Raises:
        Exception: Если возникает ошибка во время авторизации.
    """
    self.get_url('https://reseller.c-data.co.il/Login')

    emaiocators['login']['email']
    password = self.locators['login']['password']

    email_locator = (self.locators['login']['email_locator']['by'],
                        self.locators['login']['email_locator']['selector'])

    password_locator = (self.locators['login']['password_locator']['by'],
                            self.locators['login']['password_locator']['selector'])

    loginbutton_locator =  (self.locators['login']['loginbutton_locator']['by'],
                                self.locators['login']['loginbutton_locator']['selector'])

    self.print(f''' email_locator {email_locator}
            password_locator {password_locator}
            loginbutton_locator {loginbutton_locator}''')

    self.find(email_locator).send_keys(email)
    self.find(password_locator).send_keys(password)
    self.find(loginbutton_locator).click()
    self.log('C-data logged in')
    return Truee
```

**Purpose**: The function performs user authorization on the C-data reseller website using web driver interactions.

**Parameters**:

- `self`: The object to which the method is attached.

**Returns**:

- `bool`: Returns `True` if authorization is successful, otherwise `False`.

**Raises Exceptions**:

- `Exception`: If an error occurs during the authorization process.

**How the Function Works**:

1. The function first navigates to the login page of the C-data reseller website.
2. It retrieves email and password values from the `self.locators` object.
3. It extracts locators for the email field, password field, and login button from the `self.locators` object.
4. It locates the email field, password field, and login button using the retrieved locators.
5. It enters the email and password values into the corresponding fields.
6. It clicks the login button.
7. It logs the successful authorization event.
8. It returns `True` if the login is successful.

**Examples**:

```python
# Assuming an instance of the class containing the login function is called 'supplier'
supplier.login()
```

**Note**:

The `login` function relies on a `self.locators` object, which is assumed to contain a mapping of locators for different web elements on the C-data login page. This object would need to be defined or populated elsewhere in the project for this function to work properly.