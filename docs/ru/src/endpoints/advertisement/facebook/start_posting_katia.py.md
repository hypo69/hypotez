# Модуль для отправки рекламных объявлений в группы Facebook

## Обзор

Модуль `start_posting_katia.py` предназначен для автоматической публикации рекламных объявлений в различные группы Facebook. Он использует веб-драйвер для взаимодействия с Facebook и класс `FacebookPromoter` для управления рекламными кампаниями.

## Подробней

Этот скрипт автоматизирует процесс размещения рекламы в группах Facebook, используя веб-драйвер для навигации и взаимодействия с сайтом. Он загружает конфигурации групп из файлов JSON и выполняет рекламные кампании, определенные в списке. Скрипт предназначен для упрощения и ускорения процесса продвижения товаров и услуг через социальную сеть Facebook.

## Классы

В данном модуле напрямую классы не определены, но используется класс `FacebookPromoter` из модуля `src.endpoints.advertisement.facebook.promoter`.

## Функции

В данном модуле функции отсутствуют.

## Методы класса

### `FacebookPromoter`

Класс `FacebookPromoter` используется для управления рекламными кампаниями в Facebook.

**Принцип работы**:
- Инициализируется веб-драйвером, списком файлов с информацией о группах и флагом, указывающим на необходимость публикации видео.
- Предоставляет метод `run_campaigns` для запуска рекламных кампаний.

```python
class FacebookPromoter:
    """
    Класс для управления рекламными кампаниями в Facebook.

    Args:
        driver (Driver): Инстанс веб-драйвера.
        group_file_paths (list): Список путей к файлам с информацией о группах.
        no_video (bool): Флаг, указывающий на необходимость публикации видео.

    Methods:
        run_campaigns(campaigns: list): Запускает рекламные кампании.
    """

    def __init__(self, driver: Driver, group_file_paths: list, no_video: bool):
        """
        Инициализирует класс FacebookPromoter.

        Args:
            driver (Driver): Инстанс веб-драйвера.
            group_file_paths (list): Список путей к файлам с информацией о группах.
            no_video (bool): Флаг, указывающий на необходимость публикации видео.
        """
        ...

    def run_campaigns(self, campaigns: list):
        """
        Запускает рекламные кампании.

        Args:
            campaigns (list): Список названий кампаний для запуска.
        """
        ...
```

## Параметры модуля

- `filenames` (list): Список имен файлов, содержащих информацию о группах Facebook. Пример: `['katia_homepage.json']`.
- `campaigns` (list): Список названий рекламных кампаний. Пример: `['sport_and_activity', 'bags_backpacks_suitcases', 'pain', 'brands', 'mom_and_baby', 'house']`.
- `promoter` (FacebookPromoter): Экземпляр класса `FacebookPromoter`, используемый для запуска рекламных кампаний.
- `d` (Driver): Экземпляр класса `Driver`, используемый для управления веб-драйвером.

## Примеры

Пример использования модуля:

```python
import header
from src.webdriver.driver import Driver, Chrome
from src.endpoints.advertisement.facebook.promoter import FacebookPromoter
from src.logger.logger import logger

d = Driver(Chrome)
d.get_url(r"https://facebook.com")

filenames: list = ['katia_homepage.json', ]
campaigns: list = ['sport_and_activity',
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
```
В данном примере создается экземпляр веб-драйвера Chrome, переходим на сайт Facebook, задаются имена файлов с информацией о группах и список рекламных кампаний. Затем создается экземпляр класса `FacebookPromoter` и запускаются рекламные кампании. В случае прерывания процесса с клавиатуры, в лог записывается соответствующее сообщение.