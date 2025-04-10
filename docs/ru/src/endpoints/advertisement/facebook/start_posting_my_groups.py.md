# Модуль для отправки рекламных объявлений в группы Facebook

## Обзор

Модуль `start_posting_my_groups.py` предназначен для автоматической отправки рекламных объявлений в группы Facebook. Он использует веб-драйвер для взаимодействия с Facebook и модуль `FacebookPromoter` для управления кампаниями и группами.

## Подробней

Модуль предназначен для автоматизации процесса публикации рекламных объявлений в Facebook группах. Он инициализирует веб-драйвер, настраивает параметры кампаний и групп, а затем запускает процесс продвижения.  В текущей версии используется Chrome в качестве веб-драйвера.

## Классы

В данном модуле классы не определены.  В модуле используются экземпляры классов `Driver` и `FacebookPromoter`.

## Функции

В данном модуле функции не определены.

## Обзор кода

### Инициализация веб-драйвера

```python
from src.webdriver.driver import Driver, Chrome
d = Driver(Chrome)
d.get_url(r"https://facebook.com")
```

Создается экземпляр веб-драйвера Chrome и выполняется переход на сайт Facebook.

### Определение списков файлов и кампаний

```python
filenames:list = ['my_managed_groups.json',]  

campaigns:list = ['brands',
                  'mom_and_baby',
                  'pain',
                  'sport_and_activity',
                  'house',
                  'bags_backpacks_suitcases',
                  'man']
```

Определяются списки файлов с информацией о группах и списки рекламных кампаний.

### Создание экземпляра класса `FacebookPromoter`

```python
from src.endpoints.advertisement.facebook.promoter import FacebookPromoter
promoter = FacebookPromoter(d, group_file_paths = filenames, no_video = True)
```

Создается экземпляр класса `FacebookPromoter`, который отвечает за управление процессом продвижения.

### Запуск цикла продвижения кампаний

```python
try:
    while True:
        
        promoter.run_campaigns(campaigns = copy.copy(campaigns), group_file_paths = filenames)
        ...

        
except KeyboardInterrupt:
    logger.info("Campaign promotion interrupted.")
```

Запускается бесконечный цикл, в котором выполняются рекламные кампании. Цикл прерывается при получении сигнала `KeyboardInterrupt`.

#### Обработка прерывания

```python
except KeyboardInterrupt:
    logger.info("Campaign promotion interrupted.")
```

При получении сигнала `KeyboardInterrupt` в лог записывается сообщение о прерывании кампании.