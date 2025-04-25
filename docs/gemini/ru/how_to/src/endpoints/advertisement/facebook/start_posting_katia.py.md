## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода запускает рекламную кампанию в Facebook для группы "Katia" (предположительно, по именам файлов).

Шаги выполнения
-------------------------
1. **Инициализация WebDriver:** Создается экземпляр WebDriver с использованием браузера Chrome.
2. **Открытие Facebook:** WebDriver открывает веб-страницу Facebook по адресу `https://facebook.com`.
3. **Загрузка конфигурации:** Загружаются имена файлов с данными для рекламной кампании.
4. **Создание промоутера:** Создается экземпляр класса `FacebookPromoter`, который будет управлять кампанией. 
   - В качестве аргументов передаются WebDriver, список имен файлов с данными для групп и флаг `no_video` (указывающий на отсутствие видео в кампании).
5. **Запуск кампании:** Метод `run_campaigns` промоутера запускает рекламную кампанию с заданными кампаниями.
6. **Обработка прерывания:**  Добавлен обработчик прерывания (`KeyboardInterrupt`), который позволяет завершить кампанию вручную.

Пример использования
-------------------------

```python
                ## \\file /src/endpoints/advertisement/facebook/start_posting_katia.py
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
                ```