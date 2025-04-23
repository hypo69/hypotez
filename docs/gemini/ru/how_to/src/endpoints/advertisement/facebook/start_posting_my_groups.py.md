### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода отвечает за запуск рекламных кампаний в Facebook, используя предоставленные группы и рекламные материалы. Он инициализирует веб-драйвер, настраивает промоутер Facebook и запускает рекламные кампании до прерывания пользователем.

Шаги выполнения
-------------------------
1. **Инициализация веб-драйвера**:
   - Импортируются необходимые модули, включая `Driver` и `Chrome` из `src.webdriver.driver`.
   - Создается экземпляр веб-драйвера Chrome: `d = Driver(Chrome)`.
   - Выполняется переход по ссылке: `d.get_url(r"https://facebook.com")`.

2. **Настройка файлов и кампаний**:
   - Определяется список файлов, содержащих информацию о группах Facebook: `filenames:list = ['my_managed_groups.json',]`.
   - Определяется список кампаний, которые будут запущены: `campaigns:list = ['brands', 'mom_and_baby', 'pain', 'sport_and_activity', 'house', 'bags_backpacks_suitcases', 'man']`.

3. **Инициализация промоутера Facebook**:
   - Создается экземпляр класса `FacebookPromoter` с передачей веб-драйвера, списка файлов групп и указанием, что видео не используются: `promoter = FacebookPromoter(d, group_file_paths = filenames, no_video = True)`.

4. **Запуск рекламных кампаний**:
   - Внутри бесконечного цикла `while True:` запускаются рекламные кампании.
   - Вызывается метод `run_campaigns` промоутера с передачей списка кампаний и файлов групп: `promoter.run_campaigns(campaigns = copy.copy(campaigns), group_file_paths = filenames)`.
   - Внутри `run_campaigns` происходит итерация по группам и кампаниям, и для каждой комбинации выполняется постинг рекламного объявления.

5. **Обработка прерывания**:
   - Если пользователь прерывает выполнение программы (например, нажатием Ctrl+C), перехватывается исключение `KeyboardInterrupt`.
   - В лог записывается сообщение о прерывании продвижения кампании: `logger.info("Campaign promotion interrupted.")`.

Пример использования
-------------------------

```python
## \file /src/endpoints/advertisement/facebook/start_posting_my_groups.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
.. module:: src.endpoints.advertisement.facebook 
	:platform: Windows, Unix
	:synopsis: Отправка рекламных объявлений в группы фейсбук (my groups?)

"""



import header 
import copy
from src.webdriver.driver import Driver, Chrome
from src.endpoints.advertisement.facebook.promoter import FacebookPromoter
from src.logger.logger import logger

d = Driver(Chrome)
d.get_url(r"https://facebook.com")

filenames:list = ['my_managed_groups.json',]  

campaigns:list = ['brands',
                  'mom_and_baby',
                  'pain',
                  'sport_and_activity',
                  'house',
                  'bags_backpacks_suitcases',
                  'man']

promoter = FacebookPromoter(d, group_file_paths = filenames, no_video = True)

try:
    while True:
        
        promoter.run_campaigns(campaigns = copy.copy(campaigns), group_file_paths = filenames)
        ...

        
except KeyboardInterrupt:
    logger.info("Campaign promotion interrupted.")