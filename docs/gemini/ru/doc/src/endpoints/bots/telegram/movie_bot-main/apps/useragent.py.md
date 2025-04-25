# Модуль useragent

## Обзор

Модуль `useragent.py` предоставляет функцию `get_useragent()`, которая возвращает случайный User-Agent из списка. User-Agent - это строка, которая идентифицирует браузер пользователя, операционную систему и другие характеристики устройства.

## Подробней

Данный модуль используется в проекте `hypotez` для имитации поведения реальных пользователей при взаимодействии с веб-сайтами. 

**Пример использования:**

```python
from hypotez.src.endpoints.bots.telegram.movie_bot-main.apps.useragent import get_useragent

user_agent = get_useragent()
print(user_agent)  # Выводит случайный User-Agent из списка
```

## Функции

### `get_useragent()`

**Назначение**: Возвращает случайный User-Agent из списка.

**Параметры**:

-  None

**Возвращает**:

- `str`: Случайный User-Agent из списка.

**Как работает функция**:

- Функция `get_useragent()` выбирает случайный элемент из списка `_useragent_list` и возвращает его.

**Примеры**:

```python
>>> from hypotez.src.endpoints.bots.telegram.movie_bot-main.apps.useragent import get_useragent
>>> get_useragent()
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'
>>> get_useragent()
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
```

**Внутренние функции**:

- None

## Параметры модуля

- `_useragent_list`: Список строк, содержащих User-Agents различных браузеров.

## Примеры

```python
# Пример 1: Получение User-Agent и вывода его в консоль
from hypotez.src.endpoints.bots.telegram.movie_bot-main.apps.useragent import get_useragent

user_agent = get_useragent()
print(user_agent)  # Выводит случайный User-Agent из списка

# Пример 2: Использование User-Agent при отправке запроса к веб-сайту
import requests

user_agent = get_useragent()
headers = {'User-Agent': user_agent}
response = requests.get('https://www.google.com', headers=headers)
print(response.status_code)
```