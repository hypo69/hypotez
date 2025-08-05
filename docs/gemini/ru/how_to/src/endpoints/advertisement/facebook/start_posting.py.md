## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Блок кода реализует цикл для запуска рекламных кампаний в Facebook. Он использует объект `FacebookPromoter` для управления рекламными кампаниями и запускает их в группах Facebook, указанных в списке `filenames`. 

Шаги выполнения
-------------------------
1. **Инициализация**:
    - Создается объект `Driver` с браузером Chrome.
    - Открывается страница Facebook.
    - Определяется список файлов `filenames` с информацией о группах Facebook.
    - Определяется список `campaigns` с названиями рекламных кампаний.
    - Создается объект `FacebookPromoter` с использованием драйвера и списка файлов.
2. **Запуск цикла**:
    - Начинается бесконечный цикл `while True`.
    - **Вызов функции `run_campaigns`**: Вызывается метод `run_campaigns` объекта `FacebookPromoter` для запуска рекламных кампаний.
    - **Ожидание**: Выполняется ожидание 180 секунд (3 минуты).
    - **Повторение**: Цикл повторяется с шага 2.
3. **Обработка прерывания**:
    - При нажатии комбинации клавиш Ctrl+C выполняется прерывание программы (KeyboardInterrupt).
    - Логируется сообщение о прерывании.

Пример использования
-------------------------

```python
                ## \\file /src/endpoints/advertisement/facebook/start_posting.py
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
```

**Этот блок кода запускает непрерывную отправку рекламных объявлений в Facebook.**  Он будет работать до тех пор, пока пользователь не прервет его.