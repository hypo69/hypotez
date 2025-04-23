### **Как использовать этот блок кода**

=========================================================================================

Описание
-------------------------
Этот код предназначен для автоматической публикации мероприятий в группы Facebook с использованием веб-драйвера Chrome. Он циклически выполняет публикацию мероприятий, определенных в файлах конфигурации, в различные группы Facebook, списки которых также загружаются из файлов конфигурации.

Шаги выполнения
-------------------------
1. **Инициализация драйвера**:
   - Создается экземпляр драйвера Chrome для управления браузером.
   - Выполняется переход на главную страницу Facebook.

2. **Определение файлов конфигурации**:
   - Определяются списки имен файлов, содержащих информацию о группах Facebook и исключенных файлах.
   - Определяется список имен мероприятий для публикации.

3. **Инициализация промоутера Facebook**:
   - Создается экземпляр класса `FacebookPromoter`, который отвечает за публикацию мероприятий в группах Facebook.
   - Ему передаются драйвер Chrome, пути к файлам с информацией о группах и флаг, указывающий на отсутствие видео.

4. **Запуск цикла публикации мероприятий**:
   - Запускается бесконечный цикл, который выполняет следующие действия:
     - Логирует время начала работы.
     - Вызывает метод `run_events` объекта `FacebookPromoter` для публикации мероприятий, определенных в файлах конфигурации, в группы Facebook.
     - Логирует время ухода в сон.
     - Приостанавливает выполнение на 7200 секунд (2 часа).

5. **Обработка прерывания с клавиатуры**:
   - Если пользователь прерывает выполнение программы с помощью комбинации клавиш, например Ctrl+C, то выводится информационное сообщение о прерывании продвижения кампании.

Пример использования
-------------------------

```python
## \file /src/endpoints/advertisement/facebook/start_event.py
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