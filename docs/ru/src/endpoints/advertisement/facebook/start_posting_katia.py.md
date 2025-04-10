# Модуль для отправки рекламных объявлений в Facebook

## Обзор

Этот модуль предназначен для автоматической публикации рекламных объявлений в группах Facebook. Он использует веб-драйвер для управления браузером и взаимодействует с платформой Facebook через класс `FacebookPromoter`.

## Подробнее

Модуль `start_posting_katia.py` автоматизирует процесс публикации рекламных объявлений в группах Facebook. Он использует веб-драйвер (`Driver` и `Chrome` из `src.webdriver.driver`) для управления браузером и навигации по сайту Facebook. Класс `FacebookPromoter` (из `src.endpoints.advertisement.facebook.promoter`) отвечает за выполнение кампаний, определенных в файлах конфигурации (`.json`). Модуль предназначен для облегчения и ускорения процесса размещения рекламы в Facebook, позволяя запускать несколько рекламных кампаний одновременно.

## Классы

### `FacebookPromoter`

**Описание**: Класс для продвижения рекламных кампаний в Facebook.

**Методы**:

-   `run_campaigns(campaigns: list)`: Запускает рекламные кампании на основе переданного списка кампаний.

## Функции

### `__main__`

**Описание**: Основная часть скрипта, которая выполняет следующие действия:

1.  Инициализирует веб-драйвер.
2.  Открывает сайт Facebook.
3.  Определяет список файлов конфигурации и кампаний.
4.  Создает экземпляр класса `FacebookPromoter`.
5.  Запускает рекламные кампании.
6.  Обрабатывает прерывание с клавиатуры.

**Как работает функция**:

```
A [Инициализация драйвера и открытие Facebook]
│
B [Определение файлов конфигурации и списка кампаний]
│
C [Создание экземпляра FacebookPromoter]
│
D [Запуск рекламных кампаний]
│
E [Обработка прерывания с клавиатуры]
```

A: Инициализация веб-драйвера `Driver` с использованием браузера Chrome и открытие страницы Facebook.
B: Определение списка файлов конфигурации (`filenames`) и списка кампаний (`campaigns`), которые будут запущены.
C: Создание экземпляра класса `FacebookPromoter`, который отвечает за выполнение рекламных кампаний.
D: Запуск рекламных кампаний с использованием метода `run_campaigns` класса `FacebookPromoter`.
E: Обработка прерывания с клавиатуры (KeyboardInterrupt), которое позволяет остановить выполнение скрипта в любой момент.

**Примеры**:

```python
# Пример запуска скрипта с предопределенными параметрами
import header
from src.webdriver.driver import Driver, Chrome
from src.endpoints.advertisement.facebook.promoter import FacebookPromoter
from src.logger.logger import logger

d = Driver(Chrome)
d.get_url(r"https://facebook.com")

filenames: list = ['katia_homepage.json']
campaigns: list = [
    'sport_and_activity',
    'bags_backpacks_suitcases',
    'pain',
    'brands',
    'mom_and_baby',
    'house',
]
promoter = FacebookPromoter(d, group_file_paths=filenames, no_video=False)

try:
    promoter.run_campaigns(campaigns)
except KeyboardInterrupt as ex:
    logger.info("Campaign promotion interrupted.", ex, exc_info=True)