### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предназначен для автоматической публикации рекламных объявлений в группах Facebook. Он использует веб-драйвер для взаимодействия с Facebook и выполняет цикл публикаций, пока не будет прерван вручную.

Шаги выполнения
-------------------------
1. **Инициализация веб-драйвера**:
   - Создается экземпляр класса `Driver` с использованием браузера Chrome.
   - Функция `get_url` открывает главную страницу Facebook в браузере.

2. **Определение списка файлов и кампаний**:
   - `filenames`: Список JSON файлов, содержащих информацию о группах, в которых будет размещаться реклама.
   - `excluded_filenames`: Список файлов, которые следует исключить из процесса публикации.
   - `campaigns`: Список названий рекламных кампаний.

3. **Инициализация промоутера Facebook**:
   - Создается экземпляр класса `FacebookPromoter`, который отвечает за публикацию объявлений.
   - В конструктор передаются драйвер, список файлов с группами и флаг `no_video`, указывающий на отсутствие видео в объявлениях.

4. **Запуск цикла продвижения**:
   - В бесконечном цикле вызывается метод `run_campaigns` для выполнения публикации объявлений.
   - После каждой итерации цикл засыпает на 180 секунд.
   - В случае прерывания с клавиатуры (KeyboardInterrupt), программа завершает работу, логируя сообщение об остановке продвижения.

Пример использования
-------------------------

```python
## \file /src/endpoints/advertisement/facebook/start_posting.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.endpoints.advertisement.facebook 
	:platform: Windows, Unix
	:synopsis: Отправка рекламных объявлений в группы фейсбук

"""


from math import log
import header
import time
import copy
from src.webdriver.driver import Driver, Chrome
from src.endpoints.advertisement.facebook import FacebookPromoter
from src.logger.logger import logger

d = Driver(Chrome)
d.get_url(r"https://facebook.com")

filenames:list[str] = [
                        "usa.json",
                        "he_ils.json",
                        "ru_ils.json",
                        "katia_homepage.json",
                        "my_managed_groups.json",
          
                        ]
excluded_filenames:list[str] = ["my_managed_groups.json",                        
                                "ru_usd.json",
                            "ger_en_eur.json",  ]
campaigns:list = ['brands',
                  'mom_and_baby',
                  'pain',
                  'sport_and_activity',
                  'house',
                  'bags_backpacks_suitcases',
                  'man']

promoter:FacebookPromoter = FacebookPromoter(d, group_file_paths=filenames, no_video = True)

try:
    while True:
        
        promoter.run_campaigns(campaigns = copy.copy(campaigns), group_file_paths = filenames)
        print(f"Going sleep {time.localtime}")
        time.sleep(180)
        ...

        
except KeyboardInterrupt:
    logger.info("Campaign promotion interrupted.")