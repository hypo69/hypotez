# Модуль `login`

## Обзор

Модуль `login` предназначен для автоматизации процесса авторизации на сайте Amazon с использованием веб-драйвера. Он предоставляет функцию `login`, которая принимает объект поставщика (`Supplier`) в качестве аргумента и выполняет шаги, необходимые для входа в систему. Модуль использует локаторы, хранящиеся в объекте поставщика, для взаимодействия с элементами веб-страницы.

## Подробнее

Модуль `login` является частью системы для работы с поставщиками и автоматизации задач, связанных с их веб-сайтами. Он использует веб-драйвер для эмуляции действий пользователя, таких как ввод адреса электронной почты и пароля, нажатие кнопок и т. д.

## Функции

### `login(s)`

**Назначение**: Выполняет процесс авторизации на сайте Amazon.

**Параметры**:

-   `s` (Supplier): Объект поставщика, содержащий информацию о локаторах элементов страницы и инстанс веб-драйвера.

**Возвращает**:

-   `bool`: `True`, если авторизация прошла успешно, `False` в противном случае.

**Как работает функция**:

1.  **Извлекает локаторы**: Извлекает локаторы для элементов страницы из `s.locators_store['login']`.
2.  **Получает инстанс драйвера**: Получает инстанс веб-драйвера из `s.driver`.
3.  **Переходит на страницу Amazon**: Открывает главную страницу Amazon (`https://amazon.com/`) в браузере.
4.  **Нажимает кнопку входа**: Нажимает кнопку, открывающую форму входа, используя локатор `_l['open_login_inputs']`. Если первая попытка не удалась, обновляет страницу и повторяет попытку.
5.  **Вводит адрес электронной почты**: Вводит адрес электронной почты в поле ввода, используя локатор `_l['email_input']`.
6.  **Нажимает кнопку "Продолжить"**: Нажимает кнопку "Продолжить", используя локатор `_l['continue_button']`.
7.  **Вводит пароль**: Вводит пароль в поле ввода, используя локатор `_l['password_input']`.
8.  **Отмечает чекбокс "Оставаться в системе"**: Отмечает чекбокс "Оставаться в системе", используя локатор `_l['keep_signed_in_checkbox']`.
9.  **Нажимает кнопку "Войти"**: Нажимает кнопку для завершения процесса входа, используя локатор `_l['success_login_button']`.
10. **Проверяет URL**: Проверяет текущий URL, чтобы убедиться, что авторизация прошла успешно. Если URL указывает на страницу входа, значит, авторизация не удалась, и функция возвращает `False`.
11. **Разворачивает окно браузера**: Разворачивает окно браузера на весь экран.
12. **Логирует информацию об успехе**: Записывает сообщение об успешной авторизации в лог.

**Внутренние функции**:

В данной функции нет внутренних функций.

**Примеры**:

```python
from src.suppliers.supplier import Supplier
from src.webdriver import Driver, Firefox

# Создание экземпляра поставщика и настройка драйвера (пример с Firefox)
driver = Driver(Firefox)
supplier = Supplier(driver)
supplier.locators_store = {
    'login': {
        'open_login_inputs': {'by': 'XPATH', 'selector': '//a[@id="nav-link-accountList"]', 'timeout': 10},
        'email_input': {'by': 'ID', 'selector': 'ap_email', 'timeout': 10},
        'continue_button': {'by': 'ID', 'selector': 'continue', 'timeout': 10},
        'password_input': {'by': 'ID', 'selector': 'ap_password', 'timeout': 10},
        'keep_signed_in_checkbox': {'by': 'ID', 'selector': 'auth-remember-me', 'timeout': 10},
        'success_login_button': {'by': 'ID', 'selector': 'signInSubmit', 'timeout': 10}
    }
}

# Вызов функции login
success = login(supplier)
if success:
    print("Авторизация прошла успешно")
else:
    print("Авторизация не удалась")
```

```python
from src.suppliers.supplier import Supplier
from src.webdriver import Driver, Chrome

# Создание экземпляра поставщика и настройка драйвера (пример с Chrome)
driver = Driver(Chrome)
supplier = Supplier(driver)
supplier.locators_store = {
    'login': {
        'open_login_inputs': {'by': 'XPATH', 'selector': '//a[@id="nav-link-accountList"]', 'timeout': 10},
        'email_input': {'by': 'ID', 'selector': 'ap_email', 'timeout': 10},
        'continue_button': {'by': 'ID', 'selector': 'continue', 'timeout': 10},
        'password_input': {'by': 'ID', 'selector': 'ap_password', 'timeout': 10},
        'keep_signed_in_checkbox': {'by': 'ID', 'selector': 'auth-remember-me', 'timeout': 10},
        'success_login_button': {'by': 'ID', 'selector': 'signInSubmit', 'timeout': 10}
    }
}

# Вызов функции login
success = login(supplier)
if success:
    print("Авторизация прошла успешно")
else:
    print("Авторизация не удалась")