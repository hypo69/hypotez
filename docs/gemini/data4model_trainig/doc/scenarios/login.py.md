# Модуль для выполнения сценария входа в Facebook

## Обзор

Модуль `src.endpoints.advertisement.facebook.scenarios.login` предназначен для выполнения сценария входа в Facebook.

## Подробней

Модуль содержит функцию `login`, которая использует веб-драйвер для автоматизации процесса входа в Facebook.

## Функции

### `login`

```python
def login(d: Driver) -> bool:
```

**Назначение**: Выполняет вход на Facebook.

**Параметры**:

*   `d` (Driver): Экземпляр драйвера для взаимодействия с веб-элементами.

**Возвращает**:

*   `bool`: `True`, если авторизация прошла успешно, иначе `False`.

**Вызывает исключения**:

*   `Exception`: Если возникает ошибка при вводе логина, пароля или нажатии кнопки.

**Как работает функция**:

1.  Загружает учетные данные Facebook из `gs.facebook_credentials[0]`.
2.  Вводит логин и пароль в соответствующие поля, используя методы веб-драйвера.
3.  Нажимает кнопку входа.
4.  Возвращает `True`, если все шаги выполнены успешно, иначе `False`.

**Примеры**:

```python
from src.webdriver.driver import Driver, Chrome
from src.endpoints.advertisement.facebook.scenarios.login import login

# Создание экземпляра драйвера
d = Driver(Chrome)
d.get_url("https://facebook.com")

# Выполнение сценария входа
if login(d):
    print("Вход выполнен успешно")
else:
    print("Ошибка при входе")