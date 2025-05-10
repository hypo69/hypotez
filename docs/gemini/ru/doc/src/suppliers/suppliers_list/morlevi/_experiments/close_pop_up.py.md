# Модуль `src.suppliers.morlevi._experiments.close_pop_up`

## Обзор

Этот модуль содержит код для проверки локатора закрытия поп-ап окна на сайте Morlevi. Он импортирует необходимые модули для работы с веб-драйвером, анализа данных и логгирования. 

## Подробнее

Модуль `src.suppliers.morlevi._experiments.close_pop_up`  - это экспериментальный код, который проверяет эффективность локатора для закрытия поп-ап окна на сайте Morlevi.  В модуле используется веб-драйвер `Firefox` для открытия страницы товара на Morlevi, а также класс `Graber` для извлечения информации о товаре, включая его `id`. 

## Классы

### `Driver`
**Описание**: Класс, который управляет веб-драйвером. 
**Наследует**: `Driver` - базовый класс для работы с веб-драйвером. 
**Атрибуты**: 
   - `Firefox`:  Указывает на использование веб-драйвера `Firefox`.
**Методы**:
   - `execute_locator(l: dict)`: Метод для выполнения действия над веб-элементом по заданному локатору. 

### `Graber` 
**Описание**: Класс для извлечения информации о товаре с сайта Morlevi. 
**Наследует**: `MorleviGraber` -  класс, который наследует функциональность для работы с сайтом Morlevi.
**Атрибуты**:
   - `driver`: Веб-драйвер, используемый для взаимодействия с сайтом.
**Методы**:
   - `id_product`:  Метод для получения `id` товара.

## Функции

### `j_loads_ns`

**Назначение**: Функция для загрузки данных из JSON-файла.
**Параметры**: 
    - `file_path (str | Path)`: Путь к JSON-файлу.
**Возвращает**:
    - `dict`: Словарь с данными из JSON-файла.

## Примеры 

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