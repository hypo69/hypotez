# Модуль отправки рекламных объявлений в Facebook

## Обзор

Модуль `src.endpoints.advertisement.facebook.start_posting` предназначен для автоматической отправки рекламных объявлений в группы Facebook. Он использует веб-драйвер для взаимодействия с Facebook и выполняет итеративные рекламные кампании.

## Подробнее

Модуль предназначен для автоматизации процесса публикации рекламы в группах Facebook. Он использует класс `FacebookPromoter` для управления кампаниями и драйвер веб-браузера для взаимодействия с сайтом Facebook. Модуль настраивается через списки файлов групп, исключенные файлы и списки кампаний. Основная логика заключается в итеративном запуске кампаний и ожидании между запусками.

## Классы

### `FacebookPromoter`

**Описание**: Этот класс отвечает за управление рекламными кампаниями в Facebook.

**Принцип работы**:
Класс инициализируется драйвером веб-браузера и списками файлов групп, используемых для публикации рекламы. Он предоставляет методы для запуска кампаний и взаимодействия с Facebook через веб-драйвер.

## Переменные

- `filenames` (list[str]): Список файлов, содержащих информацию о группах для размещения рекламы.
- `excluded_filenames` (list[str]): Список файлов, исключенных из списка групп для размещения рекламы.
- `campaigns` (list): Список названий рекламных кампаний для запуска.
- `promoter` (FacebookPromoter): Экземпляр класса `FacebookPromoter`, используемый для управления рекламными кампаниями.

## Функции

### `run_campaigns`

```python
def run_campaigns(campaigns: list, group_file_paths: list) -> None:
    """
    Запускает заданные рекламные кампании для указанных групп Facebook.

    Args:
        campaigns (list): Список названий рекламных кампаний.
        group_file_paths (list): Список путей к файлам, содержащим информацию о группах Facebook.
    """
    ...
```
### `get_url`

```python
def get_url(url: str) -> None:
    """
    Открывает указанный URL в веб-браузере.

    Args:
        url (str): URL для открытия.
    """
    ...
```
### `sleep`

```python
def sleep(seconds: int) -> None:
    """
    Приостанавливает выполнение программы на заданное количество секунд.

    Args:
        seconds (int): Количество секунд для приостановки.
    """
    ...
```
###  Основной цикл `try`

```python
 try:
    while True:
        
        promoter.run_campaigns(campaigns = copy.copy(campaigns), group_file_paths = filenames)
        print(f"Going sleep {time.localtime}")
        time.sleep(180)
        ...

        
except KeyboardInterrupt:
    logger.info("Campaign promotion interrupted.")
```

**Описание**: Этот цикл запускает рекламные кампании в бесконечном режиме, пока не будет прерван пользователем.
Внутри цикла вызывается метод `run_campaigns` объекта `promoter` для запуска кампаний, после чего программа засыпает на 180 секунд.

**Как работает функция**:
1. Запускается бесконечный цикл `while True`.
2. Внутри цикла вызывается `promoter.run_campaigns` с копией списка кампаний и списком файлов групп.
3. Выводится сообщение в консоль о переходе в режим ожидания.
4. Программа приостанавливается на 180 секунд с помощью `time.sleep(180)`.
5. Если пользователь прерывает выполнение программы сочетанием клавиш (KeyboardInterrupt), происходит выход из цикла, и в лог записывается сообщение о прерывании.

**Примеры**:

```python
# Пример запуска цикла кампаний
try:
    while True:
        promoter.run_campaigns(campaigns=copy.copy(campaigns), group_file_paths=filenames)
        print(f"Going sleep {time.localtime()}")
        time.sleep(180)
except KeyboardInterrupt as ex:
    logger.info("Campaign promotion interrupted.", ex, exc_info=True)
```

## Параметры

- `filenames` (list[str]): Список файлов, содержащих пути к файлам с данными о группах Facebook.
- `excluded_filenames` (list[str]): Список файлов, которые следует исключить из обработки.
- `campaigns` (list): Список кампаний для запуска. Каждая кампания представляет собой набор настроек для публикации рекламы.

**Примеры**

- Создание экземпляра `FacebookPromoter` и запуск кампаний:

```python
from src.endpoints.advertisement.facebook import FacebookPromoter
from src.webdriver.driver import Driver, Chrome
import copy
import time

# Инициализация веб-драйвера
driver = Driver(Chrome)

# Список файлов с информацией о группах Facebook
filenames = ["usa.json", "he_ils.json", "ru_ils.json", "katia_homepage.json", "my_managed_groups.json"]

# Список кампаний для запуска
campaigns = ['brands', 'mom_and_baby', 'pain', 'sport_and_activity', 'house', 'bags_backpacks_suitcases', 'man']

# Создание экземпляра FacebookPromoter
promoter = FacebookPromoter(driver, group_file_paths=filenames, no_video=True)

# Запуск кампаний
try:
    while True:
        promoter.run_campaigns(campaigns=copy.copy(campaigns), group_file_paths=filenames)
        print(f"Going to sleep {time.localtime()}")
        time.sleep(180)
except KeyboardInterrupt:
    print("Campaign promotion interrupted.")