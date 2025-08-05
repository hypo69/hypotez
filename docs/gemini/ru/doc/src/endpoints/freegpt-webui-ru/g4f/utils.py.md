# Модуль `utils`

## Обзор

Модуль `utils` предоставляет набор утилитных функций для работы с cookies. 

## Подробнее

Модуль `utils` используется для работы с cookies пользователей из различных браузеров. 
Он реализует функции для получения cookies из браузеров и извлечения 
конкретных cookies по имени. 

## Классы

### `class Utils`

**Описание**: Класс `Utils` предоставляет методы для работы с cookies.

**Атрибуты**:

- `browsers` (list): Список функций для получения cookies из разных браузеров, 
                      предоставленных модулем `browser_cookie3`.

**Методы**:

- `get_cookies(domain: str, setName: str = None, setBrowser: str = False) -> dict`: 
    Функция для получения cookies с определенного домена. 

## Функции

### `get_cookies(domain: str, setName: str = None, setBrowser: str = False) -> dict`

**Назначение**: Функция извлекает cookies с указанного домена из всех доступных браузеров.

**Параметры**:

- `domain` (str): Домен, с которого необходимо получить cookies.
- `setName` (str, optional): Имя конкретного cookie, которое нужно извлечь. По умолчанию `None`.
- `setBrowser` (str, optional): Имя браузера, из которого нужно получить cookies. 
                               По умолчанию `False`.

**Возвращает**:

- `dict`: Словарь с cookies, полученных с указанного домена. Если `setName` задано, возвращает 
        словарь с одним элементом, ключом которого является `setName`, а значением - 
        значение cookie. 

**Вызывает исключения**:

- `ValueError`: Если `setName` задано, но соответствующее cookie не найдено в браузере.

**Как работает функция**:

- Функция перебирает список браузеров `Utils.browsers` и пытается извлечь cookies 
  с указанного домена.
- Если `setBrowser` не задан, функция пытается извлечь cookies из всех браузеров.
- Если `setBrowser` задан, функция извлекает cookies только из указанного браузера.
- Если `setName` не задан, функция возвращает словарь всех cookies.
- Если `setName` задан, функция возвращает словарь с одним элементом, ключом которого 
  является `setName`, а значением - значение cookie.

**Примеры**:

```python
# Получение всех cookies с домена example.com
cookies = Utils.get_cookies(domain='example.com')
print(cookies)

# Получение cookie с именем 'session_id' с домена example.com
session_id = Utils.get_cookies(domain='example.com', setName='session_id')
print(session_id)

# Получение cookies с домена example.com из браузера Chrome
chrome_cookies = Utils.get_cookies(domain='example.com', setBrowser='chrome')
print(chrome_cookies)
```

## Примеры

```python
from src.endpoints.freegpt-webui-ru.g4f.utils import Utils

# Получение cookies с домена example.com
cookies = Utils.get_cookies(domain='example.com')
print(cookies)

# Получение cookie с именем 'session_id' с домена example.com
session_id = Utils.get_cookies(domain='example.com', setName='session_id')
print(session_id)

# Получение cookies с домена example.com из браузера Chrome
chrome_cookies = Utils.get_cookies(domain='example.com', setBrowser='chrome')
print(chrome_cookies)
```