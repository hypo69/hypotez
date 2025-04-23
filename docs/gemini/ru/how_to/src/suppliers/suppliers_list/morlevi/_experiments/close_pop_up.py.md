### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода предназначен для инициализации веб-драйвера Firefox, создания экземпляра класса `MorleviGraber` и открытия страницы товара на сайте morlevi.co.il с целью извлечения идентификатора товара.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей и классов**: Импортируются модули `header`, `gs`, `Driver` (из `src.webdriver.driver`), `Firefox` (из `src.webdriver.firefox`), `MorleviGraber` (из `src.suppliers.morlevi.graber`) и `j_loads_ns` (из `src.utils.jjson`).
2. **Инициализация веб-драйвера**: Создается экземпляр веб-драйвера `Firefox` с помощью `driver = Driver(Firefox)`.
3. **Создание экземпляра класса `MorleviGraber`**: Создается объект `graber` класса `MorleviGraber` с передачей экземпляра драйвера в качестве аргумента: `graber = MorleviGraber(driver)`.
4. **Открытие URL**: Выполняется открытие страницы товара на сайте morlevi.co.il с использованием метода `driver.get_url('https://www.morlevi.co.il/product/19041')`.
5. **Извлечение идентификатора товара**: Идентификатор товара извлекается с использованием атрибута `id_product` объекта `graber` и сохраняется в переменной `product_id`: `product_id = graber.id_product`.

Пример использования
-------------------------

```python
                ## \file /src/suppliers/morlevi/_experiments/close_pop_up.py
# -*- coding: utf-8 -*-.

#! .pyenv/bin/python3

"""
module: src.suppliers.morlevi._experiments.close_pop_up
	:platform: Windows, Unix
	:synopsis: Проверка локатора закрытия поп-ап окна
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

# Функция извлекает идентификатор товара
product_id = graber.id_product
print(f"ID товара: {product_id}") # Вывод идентификатора товара в консоль
...