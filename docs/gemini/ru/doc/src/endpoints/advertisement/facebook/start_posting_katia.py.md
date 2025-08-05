# Модуль `start_posting_katia.py`

## Обзор

Этот модуль реализует отправку рекламных объявлений в группы Facebook. Он использует веб-драйвер для взаимодействия с Facebook и работает с JSON-файлами, которые содержат информацию о группах Facebook, в которые необходимо размещать рекламу. 

## Подробнее

Модуль `start_posting_katia.py` предназначен для автоматической публикации рекламных объявлений в группы Facebook.  Он использует класс `FacebookPromoter` для обработки процесса публикации, который включает в себя:

- Загрузку JSON-файлов, содержащих информацию о группах.
- Инициализацию веб-драйвера (Chrome) для взаимодействия с Facebook.
- Выполнение процесса публикации объявлений.
- Логирование действий и ошибок с помощью `logger` из модуля `src.logger.logger`.

##  Функции

### `run_campaigns`

```python
def run_campaigns(campaigns: list) -> None:
    """
    Запускает кампании по публикации объявлений в группы Facebook.

    Args:
        campaigns (list): Список кампаний для запуска (имена групп).

    Returns:
        None
    """
```

##  Классы

### `FacebookPromoter`

```python
class FacebookPromoter:
    """
    Класс для управления процессом публикации рекламных объявлений в группы Facebook.

    Attributes:
        d (Driver): Экземпляр драйвера для работы с Facebook.
        group_file_paths (list): Список путей к JSON-файлам с информацией о группах.
        no_video (bool): Флаг, указывающий на необходимость отключения видео в рекламных объявлениях.

    Methods:
        run_campaigns(campaigns: list): Запускает кампании по публикации объявлений в группы Facebook.
    """
```

## Примеры

```python
# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Chrome)

# Загрузка JSON-файлов с информацией о группах
filenames = ['katia_homepage.json']

# Список кампаний (имена групп)
campaigns = [
    'sport_and_activity',
    'bags_backpacks_suitcases',
    'pain',
    'brands',
    'mom_and_baby',
    'house',
]

# Создание экземпляра класса FacebookPromoter
promoter = FacebookPromoter(driver, group_file_paths=filenames, no_video=False)

# Запуск кампаний
promoter.run_campaigns(campaigns)
```

##  Параметры

### `campaigns`

- **Тип**: `list`
- **Описание**: Список кампаний для запуска (имена групп).

### `group_file_paths`

- **Тип**: `list`
- **Описание**: Список путей к JSON-файлам с информацией о группах. 

### `no_video`

- **Тип**: `bool`
- **Описание**: Флаг, указывающий на необходимость отключения видео в рекламных объявлениях.