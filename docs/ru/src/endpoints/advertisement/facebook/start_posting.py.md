# Модуль для отправки рекламных объявлений в Facebook

## Обзор

Модуль `src.endpoints.advertisement.facebook.start_posting` предназначен для автоматической отправки рекламных объявлений в группы Facebook. Он использует веб-драйвер для взаимодействия с сайтом Facebook и выполняет продвижение рекламных кампаний на основе заданных параметров и файлов с группами.

## Подробней

Этот модуль является частью системы для автоматизации рекламных кампаний в Facebook. Он использует драйвер веб-браузера для доступа к Facebook и публикации объявлений в различных группах. Основная цель модуля - автоматизировать процесс продвижения, уменьшить ручную работу и обеспечить постоянную публикацию контента в целевых группах.

## Функции

### `main`

```python
# -*- coding: utf-8 -*-
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
```

**Назначение**: Главная функция модуля, которая запускает процесс продвижения рекламных кампаний в Facebook.

**Как работает функция**:

1.  **Инициализация**:

    *   Создается экземпляр веб-драйвера `Driver` для браузера Chrome.

    *   Выполняется переход по URL `https://facebook.com` с помощью драйвера.

    *   Определяются списки файлов с группами (`filenames`) и исключенными файлами (`excluded_filenames`).

    *   Определяется список рекламных кампаний (`campaigns`).

    *   Создается экземпляр класса `FacebookPromoter`, который отвечает за продвижение в Facebook.
2.  **Цикл продвижения**:

    *   Запускается бесконечный цикл `while True:`, в котором происходит продвижение кампаний.

    *   Внутри цикла вызывается метод `run_campaigns` объекта `promoter` для выполнения продвижения.

    *   Выводится сообщение о переходе в состояние сна с указанием текущего времени.

    *   Программа переходит в состояние сна на 180 секунд.
3.  **Обработка прерывания**:

    *   Если происходит прерывание с клавиатуры (`KeyboardInterrupt`), выводится информационное сообщение о прерывании продвижения кампании.

**Примеры**:

```python
# Пример запуска процесса продвижения
# (Предполагается, что все необходимые файлы и настройки уже определены)

# Запуск бесконечного цикла продвижения
# python src/endpoints/advertisement/facebook/start_posting.py
```

## Переменные

-   `d`: Экземпляр класса `Driver`, используемый для управления браузером Chrome.
-   `filenames`: Список путей к файлам, содержащим информацию о группах для размещения рекламы.
-   `excluded_filenames`: Список файлов, которые исключаются из процесса размещения рекламы.
-   `campaigns`: Список названий рекламных кампаний, которые будут запущены.
-   `promoter`: Экземпляр класса `FacebookPromoter`, используемый для продвижения рекламных кампаний в Facebook.