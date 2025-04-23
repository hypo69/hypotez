### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предназначен для автоматической публикации рекламных объявлений в группах Facebook с использованием класса `FacebookPromoter`. Он инициализирует веб-драйвер, загружает конфигурации кампаний и запускает процесс публикации объявлений.

Шаги выполнения
-------------------------
1. **Инициализация веб-драйвера**:
   - Импортируются необходимые модули, включая `Driver` и `Chrome` из `src.webdriver.driver`.
   - Создается экземпляр веб-драйвера `Driver` с использованием браузера Chrome.
   - Выполняется переход на главную страницу Facebook.

2. **Настройка параметров кампании**:
   - Определяется список файлов конфигурации (`filenames`), содержащих параметры для групп Facebook.
   - Определяется список кампаний (`campaigns`), которые будут запущены. Каждая кампания соответствует определенной тематике.
   - Создается экземпляр класса `FacebookPromoter` с передачей веб-драйвера, списка файлов конфигурации и указанием на необходимость использования видео (в данном случае `no_video = False`).

3. **Запуск кампаний**:
   - Вызывается метод `run_campaigns` у экземпляра `promoter` с передачей списка кампаний для запуска.
   - Обрабатывается исключение `KeyboardInterrupt`, которое позволяет остановить процесс публикации объявлений принудительно.

Пример использования
-------------------------

```python
## \file /src/endpoints/advertisement/facebook/start_posting_katia.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.endpoints.advertisement.facebook 
	:platform: Windows, Unix
	:synopsis: Отправка рекламных объявлений в группы фейсбук (Katia?)

"""

import header 
from src.webdriver.driver import Driver, Chrome
from src.endpoints.advertisement.facebook.promoter import FacebookPromoter
from src.logger.logger import logger

d = Driver(Chrome)
d.get_url(r"https://facebook.com")

filenames:list = ['katia_homepage.json',]
campaigns:list = [ 'sport_and_activity',
                  'bags_backpacks_suitcases',
                    'pain',
                    'brands',
                    'mom_and_baby',
                    'house',
                ]
promoter = FacebookPromoter(d, group_file_paths = filenames, no_video = False)

try:
    promoter.run_campaigns(campaigns)
except KeyboardInterrupt:
    logger.info("Campaign promotion interrupted.")