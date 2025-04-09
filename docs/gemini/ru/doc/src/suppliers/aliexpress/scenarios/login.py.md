# Модуль `login`

## Обзор

Модуль `login` предназначен для автоматизации процесса входа в учетную запись на сайте AliExpress с использованием веб-драйвера.

## Подробней

Этот модуль предоставляет функцию `login`, которая принимает объект поставщика (`Supplier`) в качестве аргумента и использует веб-драйвер для выполнения шагов входа на сайт AliExpress. Он включает в себя открытие страницы входа, ввод учетных данных и подтверждение входа. Также в модуле используется модуль `logger` для логирования действий и ошибок.

## Функции

### `login`

```python
def login(s)->bool:
    """ login to aliexpress via webdriver
    @param s `Supplier` - класс поставщика с запущенным 
    """
```

**Назначение**: Осуществляет вход в учетную запись AliExpress с использованием веб-драйвера.

**Параметры**:
- `s` (Supplier): Объект поставщика с запущенным веб-драйвером и настроенными локаторами.

**Возвращает**:
- `bool`: `True` в случае успешного входа, `False` в случае неудачи.

**Как работает функция**:

1.  Принимает объект поставщика `s`, который содержит экземпляр веб-драйвера и локаторы элементов для страницы входа.
2.  Получает доступ к веб-драйверу и локаторам из объекта поставщика.
3.  Переходит на страницу AliExpress.
4.  Принимает куки.
5.  Нажимает на кнопку открытия формы входа.
6.  Заполняет поля электронной почты и пароля, используя локаторы.
7.  Нажимает кнопку входа.
8.  Возвращает `True` в случае успешного входа, `False` в противном случае.

**Примеры**:

Предположим, у нас есть объект поставщика `supplier` с настроенным веб-драйвером и локаторами.

```python
from src.suppliers.aliexpress.scenarios.login import login
from src.suppliers.aliexpress.aliexpress import AliexpressSupplier
from src.webdriver import Driver, Firefox

# Создание инстанса драйвера (пример с Firefox)
driver = Driver(Firefox)
# Создаем экземпляр класса AliexpressSupplier
supplier = AliexpressSupplier(driver)

# Настройка локаторов (пример)
supplier.locators = {
    'login': {
        'cookies_accept': {'by': 'XPATH', 'selector': '//button[text()="Accept All"]'},
        'open_login': {'by': 'XPATH', 'selector': '//a[@id="open-login-form"]'},
        'email_locator': {'by': 'ID', 'selector': 'fm-login-id'},
        'password_locator': {'by': 'ID', 'selector': 'fm-login-password'},
        'loginbutton_locator': {'by': 'XPATH', 'selector': '//button[contains(@class, "fm-submit")]'}
    }
}
supplier.driver.get_url("https://aliexpress.com") # Открываем aliexpress

success = login(supplier)
if success:
    print("Login successful!")
else:
    print("Login failed.")