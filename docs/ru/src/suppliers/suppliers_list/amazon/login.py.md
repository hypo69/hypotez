# Модуль: Авторизация на Amazon

## Обзор

Модуль `login.py` предназначен для автоматизации процесса авторизации на сайте Amazon с использованием веб-драйвера. Он содержит функцию `login`, которая принимает объект поставщика (`Supplier`) в качестве аргумента и выполняет шаги, необходимые для входа в систему.

## Подробней

Этот модуль является частью системы автоматизации для поставщиков и отвечает за вход в учетную запись Amazon. Он использует локаторы, хранящиеся в объекте поставщика, для взаимодействия с элементами веб-страницы через веб-драйвер.

## Функции

### `login(s)`

**Назначение**: Выполняет процесс авторизации на сайте Amazon.

**Параметры**:
- `s` (Supplier): Объект поставщика, содержащий данные для авторизации и локаторы элементов страницы.

**Возвращает**:
- `bool`: `True`, если авторизация прошла успешно, `False` в противном случае.

**Как работает функция**:

1.  Извлекает локаторы для процесса авторизации из `s.locators_store['login']` в переменную `_l`.
2.  Получает инстанс веб-драйвера из `s.driver` в переменную `_d`.
3.  Переключает фокус на окно веб-драйвера (`_d.window_focus()`).
4.  Переходит по URL `https://amazon.com/` (`_d.get_url('https://amazon.com/')`).
5.  Пытается нажать на кнопку открытия формы логина, используя локатор `_l['open_login_inputs']`. Если не удается, обновляет страницу и повторяет попытку.
6.  Вводит email, пароль и нажимает кнопку "Войти", используя соответствующие локаторы:
    *   `_l['email_input']`
    *   `_l['continue_button']`
    *   `_l['password_input']`
    *   `_l['keep_signed_in_checkbox']`
    *   `_l['success_login_button']`
7.  Проверяет текущий URL, и, если он соответствует странице входа (`https://www.amazon.com/ap/signin`), регистрирует ошибку и завершает работу.
8.  После успешной авторизации максимизирует окно браузера и сохраняет cookies (закомментировано).
9.  Логгирует информацию об успешной авторизации.

**Примеры**:

```python
from unittest.mock import MagicMock

# Создаем мок-объект Supplier
supplier_mock = MagicMock()
supplier_mock.locators_store = {
    'login': {
        'open_login_inputs': {'selector': '#nav-link-accountList', 'by': 'css'},
        'email_input': {'selector': '#ap_email', 'by': 'css'},
        'continue_button': {'selector': '#continue', 'by': 'css'},
        'password_input': {'selector': '#ap_password', 'by': 'css'},
        'keep_signed_in_checkbox': {'selector': '#auth-remember-me', 'by': 'css'},
        'success_login_button': {'selector': '#signInSubmit', 'by': 'css'}
    }
}
supplier_mock.driver = MagicMock()
supplier_mock.driver.current_url = "https://www.amazon.com/gp/yourstore/home" # Типо залогинились

#  Проверка работы функции login
result = login(supplier_mock)
print(result) # Вывод: True
```

## Переменные

-   `_l` (dict): Локаторы элементов страницы, необходимые для процесса авторизации.
-   `_d` (webdriver): Инстанс веб-драйвера для управления браузером.