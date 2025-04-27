## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код импортирует модуль `header` и создает экземпляр объекта `Driver` из `src.webdriver.driver` с использованием браузера Firefox. Затем с помощью `driver.get_url()` открывает URL-адрес "https://www.aliexpress.com".

Шаги выполнения
-------------------------
1. Импортирует модуль `header`, который предоставляет необходимую функциональность для работы с AliExpress.
2. Создает объект `Driver` с использованием браузера Firefox.
3. Использует метод `get_url()` объекта `Driver` для открытия URL-адреса "https://www.aliexpress.com".

Пример использования
-------------------------

```python
## \file /src/suppliers/aliexpress/_experiments/alirequests.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.suppliers.suppliers_list.aliexpress._experiments 
	:platform: Windows, Unix
	:synopsis:

"""



"""
	:platform: Windows, Unix
	:synopsis:

"""



"""
	:platform: Windows, Unix
	:synopsis:

"""



"""
	:platform: Windows, Unix
	:synopsis:

"""



"""
  :platform: Windows, Unix

"""
"""
  :platform: Windows, Unix
  :platform: Windows, Unix
  :synopsis:
"""
  

""" module: src.suppliers.suppliers_list.aliexpress._experiments """


""" HERE SHOULD BE A DESCRIPTION OF THE MODULE OPERATION ! """

import header   

from src.webdriver.driver import Driver, Chrome, Firefox

d = Driver(Firefox)
d.get_url(r"https://www.aliexpress.com")
...
```