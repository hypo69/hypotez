# Модуль для разбора ссылок из OneTab

## Обзор

Этот модуль содержит функцию `fetch_target_urls_onetab`, которая парсит целевые URL-адреса из OneTab. 
Функция извлекает ссылки из OneTab, а также цену и описание (если доступны) и возвращает их.

## Подробней

Функция `fetch_target_urls_onetab` принимает URL OneTab в качестве аргумента. Она выполняет запрос к этому URL, 
парсит HTML-контент с помощью `BeautifulSoup` и извлекает целевые URL-адреса из HTML-структуры. 
Функция также извлекает цену и описание товара из элемента с классом `tabGroupLabel`. 

## Функции

### `fetch_target_urls_onetab`

**Назначение**: Парсит целевые URL-адреса, цену и описание товара из OneTab.

**Параметры**:

- `one_tab_url` (str): URL OneTab.

**Возвращает**:

- `tuple[str, str, list[str]] | bool`: Кортеж из трех элементов:
    - `price` (str): Цена товара (извлекается из `tabGroupLabel`, если доступна).
    - `description` (str): Описание товара (извлекается из `tabGroupLabel`, если доступно).
    - `urls` (list[str]): Список целевых URL-адресов.
- `False` в случае ошибки.

**Вызывает исключения**:

- `requests.exceptions.RequestException`: В случае возникновения ошибки при выполнении запроса к OneTab.

**Как работает функция**:

1. Выполняет HTTP-запрос к URL OneTab.
2. Парсит HTML-контент с помощью `BeautifulSoup`.
3. Извлекает целевые URL-адреса из элементов `a` с классом `tabLink`.
4. Извлекает текст из элемента `div` с классом `tabGroupLabel`.
5. Если текст доступен, разделяет его на цену и описание.
6. Возвращает `tuple` из трех элементов: цену, описание и список URL-адресов.

**Примеры**:

```python
>>> from src.endpoints.fetch_one_tab import fetch_target_urls_onetab
>>> one_tab_url = 'https://www.onetab.com/page/1234567890'
>>> price, description, urls = fetch_target_urls_onetab(one_tab_url)
>>> print(f'Price: {price}, Description: {description}, URLs: {urls}')
Price: 100, Description: Example product, URLs: ['https://www.example.com/', 'https://www.example2.com/']

>>> one_tab_url = 'https://www.onetab.com/page/invalid_url'
>>> result = fetch_target_urls_onetab(one_tab_url)
>>> print(result)
False
```