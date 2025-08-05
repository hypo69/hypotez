## Как использовать блок кода для закрытия всплывающего окна
=========================================================================================

Описание
-------------------------
Этот блок кода проверяет локатор для закрытия всплывающего окна на сайте MorLevi. Он  использует `webdriver` для управления браузером,  `Graber` для получения информации о товаре, а также `j_loads_ns` для загрузки конфигурации. 

Шаги выполнения
-------------------------
1. **Инициализация драйвера:** Создается экземпляр `Driver` с браузером Firefox.
2. **Инициализация Graber:** Создается экземпляр `MorleviGraber`, передавая ему драйвер браузера.
3. **Открытие страницы товара:**  Функция `get_url` открывает страницу товара с заданным `product_id`.
4. **Получение ID товара:**  `Graber` получает ID товара с помощью  `id_product`.
5. **Проверка локатора:**  (Проверка локатора происходит дальше в коде, не показанном в примере). 
6. **Закрытие всплывающего окна:** ( Закрытие окна происходит после проверки локатора, также не показано в примере).

Пример использования
-------------------------

```python
## \file /src/suppliers/morlevi/_experiments/close_pop_up.py
# -*- coding: utf-8 -*-

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
product_id = graber.id_product
# ...  # Здесь должен быть код проверки локатора и закрытия окна
```

**Важно:**  В данном примере показаны только базовые настройки для работы с `webdriver` и  `MorleviGraber`.  В  `...`  должен быть код, который проверяет локатор  и закрывает всплывающее окно.