# Документация для модуля `close_pop_up`

## Обзор

Модуль `close_pop_up` предназначен для проверки локатора закрытия всплывающего окна на веб-сайте поставщика Morlevi. Он использует веб-драйвер для автоматизации взаимодействия с веб-страницей и проверки функциональности закрытия всплывающего окна.

## Подробнее

Модуль выполняет следующие действия:

1.  Инициализирует веб-драйвер (в данном случае, Firefox).
2.  Создает экземпляр класса `MorleviGraber`, который, вероятно, содержит методы для извлечения данных с сайта Morlevi.
3.  Открывает URL-адрес товара на сайте Morlevi.
4.  Извлекает `product_id` с использованием `MorleviGraber`.

## Импортированные модули

*   `header`: Предположительно, содержит общие определения или конфигурации.
*   `src.gs`:  Неизвестный модуль, возможно, глобальные настройки или утилиты.
*   `src.webdriver.driver.Driver`: Класс для управления веб-драйвером.
*   `src.webdriver.firefox.Firefox`: Класс для настройки и запуска Firefox в качестве веб-драйвера.
*   `src.suppliers.morlevi.graber.Graber`: Класс для извлечения информации с сайта Morlevi.
*   `src.utils.jjson.j_loads_ns`: Функция для загрузки JSON-данных из файла, возможно, с использованием пространств имен.

## Переменные

*   `driver`: Экземпляр класса `Driver`, используемый для управления веб-браузером Firefox.
*   `graber`: Экземпляр класса `Graber`, используемый для извлечения данных с сайта Morlevi.
*   `product_id`: Идентификатор товара, полученный с использованием `MorleviGraber`.

## Код

```python
## \file /src/suppliers/morlevi/_experiments/close_pop_up.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
module: src.suppliers.morlevi._experiments.close_pop_up
\t:platform: Windows, Unix
\t:synopsis: Проверка локатора закрытия поп-ап окна
   """

import header
from src import gs
from src.webdriver.driver import Driver
#from src.webdriver.chrome import Chrome
from src.webdriver.firefox import Firefox
from src.suppliers.morlevi.graber import Graber as MorleviGraber
from src.utils.jjson import j_loads_ns

driver = Driver(Firefox)
graber = MorleviGraber(driver)
driver.get_url('https://www.morlevi.co.il/product/19041')
product_id = graber.id_product
...
```

```python
driver = Driver(Firefox)
```

**Назначение**:
Создание экземпляра веб-драйвера Firefox для управления браузером.

**Как работает**:
Инициализирует объект `Driver` с использованием класса `Firefox`, что позволяет автоматизировать взаимодействие с браузером Firefox.

**Примеры**:

```python
driver = Driver(Firefox)
```

```python
graber = MorleviGraber(driver)
```

**Назначение**:
Создание экземпляра класса `MorleviGraber` для извлечения данных с сайта Morlevi.

**Как работает**:
Создает объект `Graber`, передавая ему экземпляр веб-драйвера (`driver`), чтобы `Graber` мог использовать веб-драйвер для взаимодействия с сайтом.

**Примеры**:

```python
graber = MorleviGraber(driver)
```

```python
driver.get_url('https://www.morlevi.co.il/product/19041')
```

**Назначение**:
Открытие страницы товара на сайте Morlevi с использованием веб-драйвера.

**Как работает**:
Использует метод `get_url` объекта `driver` для перехода по указанному URL-адресу.

**Примеры**:

```python
driver.get_url('https://www.morlevi.co.il/product/19041')
```

```python
product_id = graber.id_product
```

**Назначение**:
Извлечение идентификатора товара с использованием объекта `MorleviGraber`.

**Как работает**:
Получает значение атрибута `id_product` объекта `graber`, который, предположительно, содержит идентификатор товара, извлеченный с веб-страницы.

**Примеры**:

```python
product_id = graber.id_product