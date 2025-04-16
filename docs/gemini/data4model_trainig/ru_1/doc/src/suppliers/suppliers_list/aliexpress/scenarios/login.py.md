# Модуль для логина на Aliexpress

## Обзор

Модуль `login.py` предназначен для автоматического входа в систему Aliexpress с использованием веб-драйвера. Он содержит функцию `login`, которая принимает объект класса `Supplier` в качестве параметра и использует его для взаимодействия с веб-сайтом Aliexpress через Selenium WebDriver. Модуль также включает обработку файлов cookie и ввод учетных данных для входа в систему.

## Подробней

Этот модуль является частью системы для автоматизации работы с поставщиками на платформе Aliexpress. Он использует драйвер веб-браузера для навигации по сайту, принятия файлов cookie и ввода учетных данных пользователя для входа в систему. После успешного входа в систему могут быть выполнены другие действия, такие как настройка языка, валюты и страны доставки.

## Функции

### `login`

```python
def login(s) -> bool:
    """Выполняет вход на Aliexpress через веб-драйвер.

    Args:
        s (Supplier): Класс поставщика с запущенным драйвером.

    Returns:
        bool: Возвращает `True` в случае успешного входа.

    Raises:
        Exception: Если во время входа возникают какие-либо ошибки.

    Example:
        >>> from src.suppliers.suppliers_list.aliexpress.scenarios.login import login
        >>> from src.suppliers.supplier import Supplier  # Предполагается, что Supplier определён в supplier.py
        >>> # Создание экземпляра Supplier и настройка драйвера
        >>> s = Supplier()
        >>> s.driver = ... # Инициализация веб-драйвера
        >>> s.locators = {'login': {'cookies_accept': ..., 'open_login': ..., 'email_locator': ..., 'password_locator': ..., 'loginbutton_locator': ...}}  # Заполнение локаторов
        >>> result = login(s)
        >>> print(result)
        True
    """
```

**Назначение**: Функция выполняет вход на сайт Aliexpress с использованием предоставленного веб-драйвера и локаторов элементов страницы.

**Параметры**:
- `s` (Supplier): Объект класса `Supplier`, содержащий настроенный веб-драйвер и локаторы элементов для входа.

**Возвращает**:
- `bool`: Возвращает `True` в случае успешного входа. На текущий момент всегда возвращает `True` (debug).

**Как работает функция**:
1. Функция принимает объект `Supplier` в качестве аргумента, который содержит веб-драйвер и локаторы элементов для входа.
2.  Получает ссылку на  `WebDriver` из объекта поставщика `s` в переменную `_d` и локаторы из `s.locators['login']` в переменную `_l`.
3.  Переходит на страницу Aliexpress.
4.  Выполняет клик на элементе для принятия файлов cookie, используя локатор `_l['cookies_accept']`.
5.  Кликает на элементе для открытия формы входа, используя локатор `_l['open_login']`.
6.  Заполняет поля электронной почты и пароля, используя локаторы `_l['email_locator']` и `_l['password_locator']` соответственно.
7.  Нажимает кнопку входа, используя локатор `_l['loginbutton_locator']`.
8.  Временно закомментированы строки, отвечающие за полноэкранный режим и настройку языка/валюты/страны доставки.
9.  В коде присутствуют заготовки для обработки ситуаций, когда не удается получить доступ к элементам страницы (TODO).
10. В текущей версии функция всегда возвращает `True`.

**Примеры**:

```python
from src.suppliers.suppliers_list.aliexpress.scenarios.login import login
from src.suppliers.supplier import Supplier  # Предполагается, что Supplier определён в supplier.py

# Создание экземпляра Supplier и настройка драйвера
s = Supplier()
s.driver = ...  # Инициализация веб-драйвера (например, Chrome)
s.locators = {
    'login': {
        'cookies_accept': {'by': 'XPATH', 'selector': '//button[@id="accept-cookies"]'},
        'open_login': {'by': 'XPATH', 'selector': '//a[@id="open-login-form"]'},
        'email_locator': {'by': 'XPATH', 'selector': '//input[@id="email"]'},
        'password_locator': {'by': 'XPATH', 'selector': '//input[@id="password"]'},
        'loginbutton_locator': {'by': 'XPATH', 'selector': '//button[@id="login-button"]'}
    }
}
result = login(s)
print(result)