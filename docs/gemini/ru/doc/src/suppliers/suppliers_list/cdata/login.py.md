# Модуль `login.py`

## Обзор

Модуль `login.py` предназначен для реализации интерфейса авторизации с использованием веб-драйвера. Он предоставляет функцию `login`, которая выполняет вход на сайт C-data Reseller.

## Подробней

Этот модуль содержит функцию `login`, которая автоматизирует процесс входа пользователя на сайт C-data Reseller. Он использует `selenium` для поиска элементов на странице и заполнения полей логина и пароля.

## Функции

### `login`

```python
def login(self) -> bool:
    """
    Выполняет авторизацию на сайте C-data Reseller.

    Args:
        self: Экземпляр класса, содержащего информацию о локаторах и методах для взаимодействия с веб-драйвером.

    Returns:
        bool: Возвращает `True` в случае успешной авторизации.

    Raises:
        Exception: В случае возникновения каких-либо проблем при авторизации.
        <Дополнить описание возможных исключений>

    Примеры:
        >>> login_successful = login(driver_instance)
        >>> if login_successful:
        ...     print("Login successful!")
        ... else:
        ...     print("Login failed.")
    """
```

**Назначение**:
Функция `login` автоматизирует процесс авторизации на сайте C-data Reseller. Она получает URL, находит элементы ввода email и пароля, заполняет их, находит кнопку логина и нажимает на неё.

**Как работает функция**:

1.  Получает URL страницы логина `https://reseller.c-data.co.il/Login` с использованием `self.get_url()`.
2.  Извлекает данные для email и пароля из `self.locators['login']['email']` и `self.locators['login']['password']`.
3.  Определяет локаторы для полей email, пароля и кнопки логина, используя значения из `self.locators['login']`.
4.  Выводит отладочную информацию о локаторах в консоль.
5.  Находит поле email с использованием локатора `email_locator` и вводит email.
6.  Находит поле пароля с использованием локатора `password_locator` и вводит пароль.
7.  Находит кнопку логина с использованием локатора `loginbutton_locator` и нажимает на неё.
8.  Логирует сообщение об успешной авторизации.
9.  Возвращает `True` в случае успешной авторизации.

**Внутренние переменные**:

*   `email`: email для авторизации. Извлекается из `self.locators['login']['email']`
*   `password`: пароль для авторизации. Извлекается из `self.locators['login']['password']`
*   `email_locator`:  Локатор поля email, представляет собой кортеж, содержащий тип локатора (`by`) и его значение (`selector`).
*   `password_locator`: Локатор поля пароля, представляет собой кортеж, содержащий тип локатора (`by`) и его значение (`selector`).
*   `loginbutton_locator`: Локатор кнопки логина, представляет собой кортеж, содержащий тип локатора (`by`) и его значение (`selector`).

**Примеры**:

В этом примере предполагается, что у вас есть экземпляр класса, содержащий необходимые методы (`get_url`, `find`, `send_keys`, `click`, `log`, `print`) и атрибут `locators` с данными для входа.

```python
# Пример использования функции login
class CDataAuthenticator:
    def __init__(self, driver, locators, email, password):
        self.driver = driver
        self.locators = locators
        self.email = email
        self.password = password

    def get_url(self, url: str):
        """
        Переходит по указанному URL.
        """
        self.driver.get(url)

    def find(self, locator: tuple):
        """
        Находит элемент на странице по указанному локатору.
        """
        from selenium.webdriver.common.by import By
        by, selector = locator
        if by.upper() == "XPATH":
             return self.driver.find_element(By.XPATH, selector)

    def send_keys(self, keys: str):
        """
        Вводит текст в найденный элемент.
        """
        self.find().send_keys(keys)

    def click(self):
        """
        Кликает на найденный элемент.
        """
        self.find().click()

    def log(self, message: str):
        """
        Логирует сообщение.
        """
        print(message)

    def print(self, message: str):
        """
        Выводит сообщение в консоль.
        """
        print(message)

locators = {
    'login': {
        'email': 'test@example.com',
        'password': 'password123',
        'email_locator': {'by': 'XPATH', 'selector': '//input[@id="email"]'},
        'password_locator': {'by': 'XPATH', 'selector': '//input[@id="password"]'},
        'loginbutton_locator': {'by': 'XPATH', 'selector': '//button[@id="login-button"]'}
    }
}

# Создание экземпляра драйвера (пример с Chrome)
from selenium import webdriver
driver = webdriver.Chrome()

# Создание экземпляра аутентификатора с настроенным драйвером и данными
authenticator = CDataAuthenticator(driver, locators, locators['login']['email'], locators['login']['password'])

# Вызов функции login
success = authenticator.login()

if success:
    print("Login successful")
else:
    print("Login failed")

driver.quit()