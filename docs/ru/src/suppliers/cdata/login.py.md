# Модуль авторизации `login.py` для CData

## Обзор

Модуль `login.py` предназначен для автоматизации процесса авторизации на сайте CData с использованием веб-драйвера. Он содержит функцию `login`, которая выполняет вход в систему, используя предоставленные учетные данные.

## Подробней

Этот модуль автоматизирует процесс входа на сайт CData, что может быть полезно для автоматического сбора данных или выполнения других задач, требующих авторизованного доступа. Он использует веб-драйвер для взаимодействия с элементами на странице входа, такими как поля ввода электронной почты, пароля и кнопка входа.

## Функции

### `login`

```python
def login(self) -> bool:
    """
    Выполняет авторизацию на сайте CData.

    Args:
        self: Ссылка на экземпляр класса, в котором определен метод.

    Returns:
        bool: Возвращает `True` в случае успешной авторизации.

    Raises:
        Exception: В случае возникновения каких-либо проблем во время авторизации.
        Например, если не удалось найти элементы, или элементы не кликабельны

    Example:
        >>> login_result = login(self)
        >>> print(login_result)
        True
    """
```

**Назначение**: Функция `login` выполняет процесс авторизации на сайте CData.

**Параметры**:
- `self`: Ссылка на экземпляр класса, в котором определен метод.

**Возвращает**:
- `bool`: Возвращает `True` в случае успешной авторизации.

**Как работает функция**:

1.  Функция получает URL страницы авторизации с помощью `self.get_url('https://reseller.c-data.co.il/Login')`.
2.  Извлекает данные для входа (email и пароль) из атрибута `self.locators`.
3.  Определяет локаторы для полей ввода email, пароля и кнопки входа, также используя `self.locators`.
4.  Выводит в консоль значения локаторов для отладки.
5.  Заполняет поля email и пароля, используя методы `self.find(email_locator).send_keys(email)` и `self.find(password_locator).send_keys(password)`.
6.  Кликает на кнопку входа с помощью `self.find(loginbutton_locator).click()`.
7.  Записывает сообщение об успешной авторизации в лог с помощью `self.log('C-data logged in')`.
8.  Возвращает `True`, если все шаги выполнены успешно.

**Примеры**:

```python
# Пример вызова функции login
login_result = login(self)
print(login_result)
```