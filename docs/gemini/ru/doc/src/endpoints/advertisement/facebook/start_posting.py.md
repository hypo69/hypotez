# Модуль для отправки рекламных объявлений в группы Facebook

## Обзор

Модуль предназначен для автоматической публикации рекламных объявлений в различные группы Facebook. Он использует веб-драйвер для взаимодействия с сайтом Facebook и модуль `FacebookPromoter` для управления рекламными кампаниями.

## Подробнее

Этот модуль является частью системы автоматизации маркетинга `hypotez`. Он предназначен для автоматизации процесса публикации рекламных объявлений в группах Facebook. Модуль использует веб-драйвер для эмуляции действий пользователя в браузере, таких как вход в систему, навигация по сайту и публикация сообщений. Он также использует модуль `FacebookPromoter` для управления рекламными кампаниями, включая выбор групп для публикации, составление рекламных текстов и изображений, а также отслеживание результатов кампании.

## Классы

### `FacebookPromoter`

**Описание**: Класс для управления рекламными кампаниями в Facebook.

**Атрибуты**:

-   `d` (Driver): Инстанс веб-драйвера для взаимодействия с Facebook.
-   `group_file_paths` (list[str]): Список путей к файлам, содержащим информацию о группах Facebook.
-   `no_video` (bool): Флаг, указывающий, следует ли исключать видео из рекламных объявлений.

**Методы**:

-   `run_campaigns(campaigns: list, group_file_paths: list)`: Запускает рекламные кампании.

## Функции

### `run_campaigns(campaigns: list, group_file_paths: list)`

**Назначение**: Запускает рекламные кампании в Facebook.

**Параметры**:

-   `campaigns` (list): Список названий рекламных кампаний.
-   `group_file_paths` (list): Список путей к файлам, содержащим информацию о группах Facebook.

**Возвращает**:

-   `None`: Функция ничего не возвращает.

**Вызывает исключения**:

-   `KeyboardInterrupt`: Возникает при прерывании выполнения программы пользователем (например, нажатием Ctrl+C).

**Как работает функция**:

1.  Функция `run_campaigns` принимает список названий рекламных кампаний и список путей к файлам, содержащим информацию о группах Facebook.
2.  Внутри функции происходит вызов метода `promoter.run_campaigns` с переданными параметрами. Этот метод, вероятно, отвечает за выполнение основных действий по публикации рекламных объявлений в Facebook.
3.  После завершения кампаний, программа переходит в режим ожидания на 180 секунд, используя функцию `time.sleep(180)`. Это позволяет снизить нагрузку на систему и избежать блокировки со стороны Facebook.
4.  Процесс повторяется до тех пор, пока не будет прерван пользователем.

**Примеры**:

```python
promoter.run_campaigns(campaigns=['brands', 'mom_and_baby'], group_file_paths=['usa.json', 'he_ils.json'])
```

В этом примере функция `run_campaigns` запускает рекламные кампании `brands` и `mom_and_baby` с использованием информации о группах Facebook, содержащейся в файлах `usa.json` и `he_ils.json`.

## Переменные

-   `filenames` (list[str]): Список имен файлов, содержащих информацию о группах Facebook.
-   `excluded_filenames` (list[str]): Список имен файлов, которые следует исключить из обработки.
-   `campaigns` (list): Список названий рекламных кампаний.
-   `promoter` (FacebookPromoter): Инстанс класса `FacebookPromoter` для управления рекламными кампаниями.

## Код
```python
            
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
        
except KeyboardInterrupt as ex:
    logger.info("Campaign promotion interrupted.")
```
## Пошаговый разбор кода

1.  **Импорт необходимых модулей**:
    *   `math.log`: Используется для математических операций (в данном коде не используется).
    *   `header`: Предположительно, модуль для работы с заголовками (содержимое не предоставлено).
    *   `time`: Модуль для работы со временем (используется для задержки выполнения программы).
    *   `copy`: Модуль для создания копий объектов (используется для копирования списка кампаний).
    *   `src.webdriver.driver.Driver`, `src.webdriver.driver.Chrome`: Классы для управления веб-драйвером Chrome.
    *   `src.endpoints.advertisement.facebook.FacebookPromoter`: Класс для управления рекламными кампаниями в Facebook.
    *   `src.logger.logger.logger`: Объект для логирования событий.
2.  **Инициализация веб-драйвера**:
    *   `d = Driver(Chrome)`: Создается инстанс веб-драйвера Chrome.
    *   `d.get_url(r"https://facebook.com")`: Открывается сайт Facebook в браузере, управляемом веб-драйвером.
3.  **Определение списков файлов и кампаний**:
    *   `filenames:list[str]`: Список имен файлов, содержащих информацию о группах Facebook.
    *   `excluded_filenames:list[str]`: Список имен файлов, которые следует исключить из обработки.
    *   `campaigns:list`: Список названий рекламных кампаний.
4.  **Инициализация промоутера**:
    *   `promoter:FacebookPromoter = FacebookPromoter(d, group_file_paths=filenames, no_video = True)`: Создается инстанс класса `FacebookPromoter`, который будет управлять рекламными кампаниями. Ему передается инстанс веб-драйвера, список файлов с информацией о группах и флаг, указывающий, что видео не следует использовать в объявлениях.
5.  **Запуск рекламных кампаний в цикле**:
    *   `try:`: Блок `try` используется для обработки исключения `KeyboardInterrupt`, которое возникает при прерывании выполнения программы пользователем.
    *   `while True:`: Бесконечный цикл, который запускает рекламные кампании.
    *   `promoter.run_campaigns(campaigns = copy.copy(campaigns), group_file_paths = filenames)`: Запускается выполнение рекламных кампаний с использованием списка кампаний и списка файлов с информацией о группах.
    *   `print(f"Going sleep {time.localtime}")`: Выводится сообщение о том, что программа переходит в режим ожидания.
    *   `time.sleep(180)`: Программа приостанавливает выполнение на 180 секунд.
    *   `...`: Многоточие указывает на пропущенный код (в данном случае, код, который должен выполняться после завершения кампаний, но перед повторным запуском цикла).
    *   `except KeyboardInterrupt as ex:`: Блок `except` обрабатывает исключение `KeyboardInterrupt`.
    *   `logger.info("Campaign promotion interrupted.")`: В лог записывается сообщение о том, что выполнение рекламных кампаний было прервано.