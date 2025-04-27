# Модуль: src.endpoints.advertisement.facebook.start_event.py

## Обзор

Модуль `src.endpoints.advertisement.facebook.start_event.py` отвечает за отправку рекламных событий в группы Facebook. 

## Подробности

Модуль использует Selenium WebDriver для взаимодействия с Facebook. Он обрабатывает отправку различных типов рекламных событий, таких как выбор дня, выбор варианта и т.д.

## Классы 

### `Driver`

**Описание:**
- Класс `Driver` предоставляет базовый API для управления Selenium WebDriver.
- Он предоставляет методы для взаимодействия с браузером, такие как открытие URL, получение элементов, обработка событий, ожидание элементов и т.д.
- Класс `Driver` обеспечивает абстракцию над конкретными веб-драйверами, такими как Chrome, Firefox, Playwright, позволяя выбирать браузер, который вам подходит.
- Используйте его для создания экземпляра драйвера, а затем используйте `driver.execute_locator(l:dict)` для выполнения действий над веб-элементами.

**Наследование:** 
-  `Driver` наследует базовый класс `webdriver.Driver`.

**Атрибуты:** 
-  `web_driver` (webdriver.Driver): Экземпляр конкретного веб-драйвера (Chrome, Firefox, Playwright).

**Методы:** 
- `get_url(url: str) -> None`: Открывает URL в браузере.
- `execute_locator(l:dict) -> None`: Выполняет действие над веб-элементом по локатору.

**Как работает класс:**
- Класс `Driver` инкапсулирует основные действия Selenium WebDriver для упрощения работы с браузером.
- Используя методы `get_url` и `execute_locator`, можно легко автоматизировать взаимодействие с сайтами.

**Примеры:**
```python
# Creating a driver instance (example with Chrome)
driver = Driver(Chrome)

close_banner = {
  "attribute": null,
  "by": "XPATH",
  "selector": "//button[@id = 'closeXButton']",
  "if_list": "first",
  "use_mouse": false,
  "mandatory": false,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": "click()",
  "locator_description": "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
}

result = driver.execute_locator(close_banner)
```


### `FacebookPromoter`

**Описание:**
- Класс `FacebookPromoter`  отвечает за отправку рекламных событий в группы Facebook.

**Наследование:**
-  `FacebookPromoter` не наследует никаких классов.

**Атрибуты:**
- `driver` (Driver): Экземпляр класса `Driver`.
- `group_file_paths` (list[str]): Список путей к файлам, содержащим данные о группах Facebook.
- `no_video` (bool): Флаг, определяющий, требуется ли видео в рекламном событии.

**Методы:**
- `run_events(events_names: list, group_file_paths: list) -> None`: Отправляет рекламные события в группы Facebook.

**Как работает класс:**
- Класс `FacebookPromoter` использует `Driver` для взаимодействия с Facebook.
- Он обрабатывает отправку различных типов рекламных событий, таких как выбор дня, выбор варианта и т.д.

**Примеры:**
```python
promoter:FacebookPromoter = FacebookPromoter(d, group_file_paths=filenames, no_video = True)
promoter.run_events(events_names = events_names, group_file_paths = filenames)
```


## Функции

### `run_events`

**Цель:**
-  Отправляет рекламные события в группы Facebook.

**Параметры:**
- `events_names` (list): Список имен событий, которые необходимо отправить.
- `group_file_paths` (list): Список путей к файлам, содержащим данные о группах Facebook.

**Возвращаемое значение:**
-  `None`.

**Возможные исключения:**
- `Exception`: Если возникает ошибка при отправке событий.

**Как работает функция:**
-  Функция получает список имен событий и список путей к файлам с данными о группах Facebook.
-  Она использует `Driver` для взаимодействия с Facebook, обрабатывает отправку событий и логгирует результаты.

**Примеры:**
```python
promoter.run_events(events_names = events_names, group_file_paths = filenames)
```


## Пример кода

```python
                ## \\file /src/endpoints/advertisement/facebook/start_event.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.endpoints.advertisement.facebook 
	:platform: Windows, Unix
	:synopsis: Отправка мероприятий в группы фейсбук

"""


from math import log
import header
import time
from src.utils.jjson import j_loads
from src.webdriver.driver import Driver, Chrome
from src.endpoints.advertisement.facebook import FacebookPromoter
from src.logger.logger import logger

d = Driver(Chrome)
d.get_url(r"https://facebook.com")

filenames:list[str] = [ "my_managed_groups.json",
                        "usa.json",
                        "he_il.json",
                        "ru_il.json",
                        "katia_homepage.json",
                        
                        "ru_usd.json",
                        "ger_en_eur.json",            
                        ]
excluded_filenames:list[str] = ["my_managed_groups.json",]

events_names:list = ["choice_day_01_10"]


promoter:FacebookPromoter = FacebookPromoter(d, group_file_paths=filenames, no_video = True)

try:
    while True:
        logger.debug(f"waikig up {time.strftime('%H:%M:%S')}",None,False)
        promoter.run_events(events_names = events_names, group_file_paths = filenames)
        logger.debug(f"going to sleep at {time.strftime('%H:%M:%S')}",None,False)
        time.sleep(7200)
        

except KeyboardInterrupt:
    logger.info("Campaign promotion interrupted.")
```

## Сводка

Этот модуль является ключевой частью системы автоматизации рекламных кампаний в Facebook. Он обеспечивает надежное и простое взаимодействие с платформой Facebook, позволяя выполнять повторяющиеся операции по отправке рекламных событий в группы.