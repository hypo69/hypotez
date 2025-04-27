# Модуль для отправки рекламных объявлений в Facebook

## Обзор

Этот модуль отвечает за отправку рекламных объявлений в группы Facebook. Он реализует логику работы с Facebook API и использует WebDriver для взаимодействия с веб-сайтом Facebook.

## Детали

Модуль использует `FacebookPromoter` класс для управления процессом отправки объявлений. `FacebookPromoter` класс инициализируется с помощью `Driver` объекта (который представляет собой экземпляр WebDriver) и списком путей к файлам, содержащим информацию о группах Facebook, в которые нужно отправлять объявления. Класс также принимает опциональный параметр `no_video`, который определяет, нужно ли отправлять видео объявления.

`FacebookPromoter` класс предоставляет метод `run_campaigns`, который принимает список кампаний и запускает процесс отправки объявлений в группы Facebook.

## Классы

### `FacebookPromoter`

**Описание**: Класс для управления процессом отправки рекламных объявлений в Facebook.

**Атрибуты**:

- `driver` (Driver): Экземпляр WebDriver, используемый для взаимодействия с Facebook.
- `group_file_paths` (list): Список путей к файлам, содержащим информацию о группах Facebook.
- `no_video` (bool): Флаг, определяющий, нужно ли отправлять видео объявления.

**Методы**:

- `run_campaigns(campaigns: list)`: Запускает процесс отправки рекламных объявлений в группы Facebook.

## Функции

### `start_posting_katia`

**Цель**:  Основная функция для запуска процесса отправки рекламных объявлений.

**Параметры**:  -  (не используются)

**Возвращает**:  -  (не возвращает значение)

**Описание**:  -  Создает экземпляр `Driver` объекта для работы с Chrome, а затем инициализирует `FacebookPromoter` класс.
-  Запускает процесс отправки рекламных объявлений в группы Facebook, используя метод `run_campaigns` класса `FacebookPromoter`.
-  Обрабатывает исключения `KeyboardInterrupt` для прерывания процесса.

**Примеры**:

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
```

## Параметры

- `filenames` (list): Список имен файлов, содержащих информацию о группах Facebook.
- `campaigns` (list): Список кампаний, которые нужно запустить.

## Примеры

```python
# Пример использования
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