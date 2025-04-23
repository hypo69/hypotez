# Module src.endpoints.advertisement.facebook.start_posting

## Overview

Модуль предназначен для автоматической отправки рекламных объявлений в группы Facebook. Он использует веб-драйвер для взаимодействия с Facebook и модуль `FacebookPromoter` для управления рекламными кампаниями.

## More details

Модуль циклически запускает рекламные кампании, используя список групп Facebook из файлов конфигурации. Он также включает обработку прерываний с клавиатуры для завершения работы.

## Classes

### `FacebookPromoter`

**Описание**: Класс для управления рекламными кампаниями в Facebook.

**Attributes**:

-   `driver`: Экземпляр веб-драйвера для взаимодействия с Facebook.
-   `group_file_paths`: Список путей к файлам, содержащим информацию о группах Facebook.
-   `no_video`: Флаг, указывающий, следует ли исключать видео из рекламных объявлений.

**Methods**:

-   `run_campaigns()`: Запускает рекламные кампании.

## Variables

-   `d`: Экземпляр веб-драйвера (Chrome) для взаимодействия с Facebook.
-   `filenames`: Список имен файлов, содержащих информацию о группах Facebook.
-   `excluded_filenames`: Список имен файлов, которые следует исключить из обработки.
-   `campaigns`: Список названий рекламных кампаний.
-   `promoter`: Экземпляр класса `FacebookPromoter` для управления рекламными кампаниями.

## Code Description

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

filenames: list[str] = [
    "usa.json",
    "he_ils.json",
    "ru_ils.json",
    "katia_homepage.json",
    "my_managed_groups.json",
]
excluded_filenames: list[str] = [
    "my_managed_groups.json",
    "ru_usd.json",
    "ger_en_eur.json",
]
campaigns: list = [
    "brands",
    "mom_and_baby",
    "pain",
    "sport_and_activity",
    "house",
    "bags_backpacks_suitcases",
    "man",
]

promoter: FacebookPromoter = FacebookPromoter(d, group_file_paths=filenames, no_video=True)

try:
    while True:
        promoter.run_campaigns(campaigns=copy.copy(campaigns), group_file_paths=filenames)
        print(f"Going sleep {time.localtime}")
        time.sleep(180)
        ...

except KeyboardInterrupt:
    logger.info("Campaign promotion interrupted.")
```

## Variables

-   `d (Driver)`: Экземпляр класса `Driver` для управления браузером Chrome. Используется для навигации по Facebook.
-   `filenames (list[str])`: Список имен файлов, содержащих данные о группах Facebook, в которых будут размещаться объявления.
-   `excluded_filenames (list[str])`: Список имен файлов, которые исключаются из списка файлов для обработки.
-   `campaigns (list)`: Список рекламных кампаний, которые будут запущены.
-   `promoter (FacebookPromoter)`: Экземпляр класса `FacebookPromoter`, который управляет процессом публикации объявлений.

## Functions

### `FacebookPromoter.run_campaigns`

```python
FacebookPromoter.run_campaigns(campaigns: list, group_file_paths: list[str])
```

**Описание**: Запускает рекламные кампании в группах Facebook.

**Параметры**:

-   `campaigns (list)`: Список названий кампаний для запуска.
-   `group_file_paths (list[str])`: Список путей к файлам, содержащим информацию о группах Facebook.

**Возвращает**:

-   `None`

**Как работает функция**:

-   Функция вызывает метод `run_campaigns` объекта `promoter`, передавая ему список кампаний и список путей к файлам групп.
-   Функция организует процесс выполнения рекламных кампаний, распределяя задачи и обеспечивая последовательность действий.
-   Обеспечивает итеративный запуск кампаний с использованием данных о группах Facebook, содержащихся в указанных файлах.

**Примеры**:

```python
promoter.run_campaigns(campaigns=['brands', 'mom_and_baby'], group_file_paths=['usa.json', 'he_ils.json'])
```

### `time.sleep`

```python
time.sleep(seconds: int)
```

**Описание**: Приостанавливает выполнение текущего потока на заданное количество секунд.

**Параметры**:

-   `seconds (int)`: Количество секунд, на которое нужно приостановить выполнение.

**Возвращает**:

-   `None`

**Как работает функция**:

-   Функция приостанавливает выполнение текущего потока на 180 секунд.
-   Это необходимо для избежания перегрузки системы запросами к Facebook и для имитации поведения пользователя.

**Примеры**:

```python
time.sleep(180)
```

### `logger.info`

```python
logger.info(message: str)
```

**Описание**: Записывает информационное сообщение в журнал.

**Параметры**:

-   `message (str)`: Сообщение, которое нужно записать в журнал.

**Возвращает**:

-   `None`

**Как работает функция**:

-   Функция записывает сообщение о прерывании кампании в журнал.
-   Это необходимо для отслеживания событий в процессе выполнения программы.

**Примеры**:

```python
logger.info("Campaign promotion interrupted.")
```

### Main Loop

Основной цикл программы выполняется до тех пор, пока не будет прерван пользователем с помощью `KeyboardInterrupt`. Внутри цикла выполняются следующие действия:

1.  Запуск рекламных кампаний с помощью `promoter.run_campaigns`.
2.  Ожидание в течение 180 секунд с помощью `time.sleep`.

### Обработка исключений

```python
try:
    while True:
        promoter.run_campaigns(campaigns=copy.copy(campaigns), group_file_paths=filenames)
        print(f"Going sleep {time.localtime()}")
        time.sleep(180)
        ...

except KeyboardInterrupt:
    logger.info("Campaign promotion interrupted.")
```

**Описание**: Обрабатывает прерывание с клавиатуры (`KeyboardInterrupt`).

**Параметры**:

-   `KeyboardInterrupt`: Исключение, которое возникает при нажатии комбинации клавиш, прерывающей выполнение программы (обычно Ctrl+C).

**Возвращает**:

-   `None`

**Как работает функция**:

-   При возникновении исключения `KeyboardInterrupt` программа переходит в блок `except`.
-   В блоке `except` вызывается функция `logger.info` для записи сообщения о прерывании кампании в журнал.
-   Это позволяет корректно завершить работу программы при прерывании пользователем.