# Модуль `via_webdriver`

## Обзор

Модуль предназначен для парсинга данных с сайта поставщика Kualastyle с использованием веб-драйвера. Он извлекает список URL товаров из заданной категории.

## Подробней

Этот модуль является частью пакета `src.suppliers.kualastyle` и отвечает за получение списка товаров с использованием Selenium WebDriver. Он использует локаторы, определенные для категории товаров, для извлечения ссылок на товары.

## Функции

### `get_list_products_in_category(s)`

Функция возвращает список URL товаров со страницы категории.

**Параметры:**

- `s` (объект поставщика): Объект поставщика, содержащий информацию о драйвере и локаторах.

**Возвращает:**

- `list[str, str, None]`: Список URL товаров или `None` в случае ошибки.

**Как работает функция:**

1.  Извлекает инстанс драйвера из объекта поставщика `s`.
2.  Получает локаторы для категории из объекта поставщика `s`.
3.  Прокручивает страницу вниз 10 раз для загрузки всех товаров.
4.  Извлекает список URL товаров, используя локатор `product_links`.
5.  Возвращает список URL товаров.

**Примеры:**

```python
# Пример вызова функции
# from src.suppliers.kualastyle.kualastyle import Kualastyle
# from src.webdriver import Driver, Chrome

# driver = Driver(Chrome)
# supplier = Kualastyle(driver)
# urls = get_list_products_in_category(supplier)
# if urls:
#     print(urls)
# else:
#     print("Не удалось получить список URL товаров.")
```
```python
def get_list_products_in_category(s) -> list[str,str,None]:    
    """ Returns list of products urls from category page
    Attrs:\
        s - Suplier
    @returns
        list of products urls or None
    """
    d = s.driver
    l: dict = s.locators.get(\'category\')
    d.scroll(scroll_count = 10, direction = "forward")

    _ = d.execute_locator
    list_products_in_category = _(l[\'product_links\'])\
    #pprint(list_products_in_category)
    return list_products_in_categoryy
```
```
```
```python
def get_list_products_in_category(s) -> list[str,str,None]:    
    """
    Функция возвращает список URL товаров со страницы категории.
    
    Args:
        s: Объект поставщика, содержащий информацию о драйвере и локаторах.
        
    Returns:
        list[str, str, None]: Список URL товаров или None в случае ошибки.
    """
    d = s.driver
    l: dict = s.locators.get('category')
    d.scroll(scroll_count = 10, direction = "forward")

    _ = d.execute_locator
    list_products_in_category = _(l['product_links'])
    #pprint(list_products_in_category)
    return list_products_in_categoryy
```
```

```
```python
def get_list_products_in_category(s) -> list[str,str,None]:    
    """
    Функция возвращает список URL товаров со страницы категории.

    Args:
        s: Объект поставщика, содержащий информацию о драйвере и локаторах.

    Returns:
        list[str, str, None]: Список URL товаров или None в случае ошибки.
    """
    d = s.driver
    l: dict = s.locators.get('category')
    d.scroll(scroll_count = 10, direction = "forward")

    _ = d.execute_locator
    list_products_in_category = _(l['product_links'])
    #pprint(list_products_in_category)
    return list_products_in_categoryy
```
```
```python
from src.logger.logger import logger
from typing import Union

from src import gs
from src.logger.logger import logger

def get_list_products_in_category(s) -> list[str,str,None]:    
    """
    Функция возвращает список URL товаров со страницы категории.

    Args:
        s: Объект поставщика, содержащий информацию о драйвере и локаторах.

    Returns:
        list[str, str, None]: Список URL товаров или None в случае ошибки.
    """
    d = s.driver
    l: dict = s.locators.get('category')
    d.scroll(scroll_count = 10, direction = "forward")

    _ = d.execute_locator
    list_products_in_category = _(l['product_links'])
    #pprint(list_products_in_category)
    return list_products_in_categoryy
```
```python
from src.logger.logger import logger
from typing import Union

from src import gs


def get_list_products_in_category(s) -> list[str | str | None]:
    """
    Возвращает список URL товаров со страницы категории.

    Args:
        s: Объект поставщика, содержащий информацию о драйвере и локаторах.

    Returns:
        list[str | str | None]: Список URL товаров или None в случае ошибки.
    """
    d = s.driver  # Извлечение драйвера из объекта поставщика
    l: dict = s.locators.get('category')  # Функция извлекает локаторы для категории из объекта поставщика
    d.scroll(scroll_count=10, direction="forward")  # Функция выполняет прокрутку страницы вниз 10 раз

    _ = d.execute_locator  # Функция присваивает метод execute_locator драйвера локальной переменной _
    list_products_in_category = _(l['product_links'])  # Функция вызывает execute_locator для получения списка элементов, соответствующих локатору ссылок на товары
    # pprint(list_products_in_category)
    return list_products_in_category


```
```
```python
from src.logger.logger import logger
from typing import Union

from src import gs


def get_list_products_in_category(s) -> list[str | str | None]:
    """
    Возвращает список URL товаров со страницы категории.

    Args:
        s: Объект поставщика, содержащий информацию о драйвере и локаторах.

    Returns:
        list[str | str | None]: Список URL товаров или None в случае ошибки.
    """
    d = s.driver  # Функция извлекает драйвер из объекта поставщика
    l: dict = s.locators.get('category')  # Функция извлекает локаторы для категории из объекта поставщика
    d.scroll(scroll_count=10, direction="forward")  # Функция выполняет прокрутку страницы вниз 10 раз

    _ = d.execute_locator  # Функция присваивает метод execute_locator драйвера локальной переменной _
    list_products_in_category = _(l['product_links'])  # Функция вызывает execute_locator для получения списка элементов, соответствующих локатору ссылок на товары
    # pprint(list_products_in_category)
    return list_products_in_category


```
```
## \file /src/suppliers/suppliers_list/kualastyle/via_webdriver.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для получения списка товаров с Kualastyle с использованием webdriver.
===========================================================================

Модуль содержит функции для извлечения списка URL товаров из категории на сайте Kualastyle с использованием Selenium WebDriver.
Он использует локаторы, определенные для категории товаров, для извлечения ссылок на товары.

Зависимости:
    - src.logger.logger
    - typing
    - src.gs

 .. module:: src.suppliers.kualastyle.via_webdriver
"""

from src.logger.logger import logger
from typing import Union

from src import gs


def get_list_products_in_category(s) -> list[str | str | None]:
    """
    Возвращает список URL товаров со страницы категории.

    Args:
        s: Объект поставщика, содержащий информацию о драйвере и локаторах.

    Returns:
        list[str | str | None]: Список URL товаров или None в случае ошибки.
    """
    d = s.driver  # Функция извлекает драйвер из объекта поставщика
    l: dict = s.locators.get('category')  # Функция извлекает локаторы для категории из объекта поставщика
    d.scroll(scroll_count=10, direction="forward")  # Функция выполняет прокрутку страницы вниз 10 раз

    _ = d.execute_locator  # Функция присваивает метод execute_locator драйвера локальной переменной _
    list_products_in_category = _(l['product_links'])  # Функция вызывает execute_locator для получения списка элементов, соответствующих локатору ссылок на товары
    # pprint(list_products_in_category)
    return list_products_in_category