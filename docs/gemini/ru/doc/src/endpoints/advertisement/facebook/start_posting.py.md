# Отправка рекламных объявлений в группы фейсбук

## Обзор

Модуль `src.endpoints.advertisement.facebook.start_posting.py`  предназначен для автоматической публикации рекламных объявлений в группы Facebook.  Он использует WebDriver для взаимодействия с интерфейсом Facebook и  класс `FacebookPromoter` для управления процессами публикации. 

## Подробнее

Этот файл содержит основную точку входа для запуска рекламной кампании.  В нем определен список файлов с описанием групп Facebook ( `filenames`),  которые будут использоваться для публикации,  а также список кампаний ( `campaigns`) с  указанием рекламных объявлений.

## Классы 

### `FacebookPromoter`

**Описание**:  Класс `FacebookPromoter`  отвечает за управление процессом публикации рекламных объявлений в группы Facebook.  

**Атрибуты**: 

-  `driver` (Driver):  Экземпляр WebDriver, который используется для взаимодействия с браузером.
-  `group_file_paths` (list[str]):  Список путей к файлам, содержащим описание групп Facebook.
-  `no_video` (bool): Флаг, который указывает,  необходимо ли использовать только изображения. 
    
**Методы**:

-  `run_campaigns(campaigns: list, group_file_paths: list)`:  Запускает публикацию рекламных объявлений для заданных кампаний в группы Facebook.

## Функции 

### `start_posting`

**Назначение**: Запускает рекламную кампанию с заданным списком групп, кампаний и опциями.

**Параметры**:

-  `filenames` (list[str]): Список файлов, содержащих описание групп Facebook.
-  `excluded_filenames` (list[str]): Список файлов, которые нужно исключить из списка `filenames`.
-  `campaigns` (list): Список кампаний,  для которых необходимо опубликовать объявления.

**Как работает функция**:

-  Создает экземпляр класса `FacebookPromoter` с переданными параметрами.
-  Запускает цикл, который бесконечно выполняет публикацию рекламных объявлений для заданных кампаний.
-  В цикле функция `run_campaigns`  вызывается с параметрами `campaigns` и `filenames`, чтобы опубликовать объявления в группах Facebook.
-  После каждой публикации функция ожидает заданное время (180 секунд) перед запуском следующей публикации.
-  При возникновении ошибки функция `logger.info` выводит сообщение о прерывании работы.

**Примеры**:

```python
from src.endpoints.advertisement.facebook import FacebookPromoter
from src.webdriver.driver import Driver, Chrome

# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Chrome)
driver.get_url(r"https://facebook.com")

# Определение списка файлов с описанием групп
filenames:list[str] = [
                        "usa.json",
                        "he_ils.json",
                        "ru_ils.json",
                        "katia_homepage.json",
                        "my_managed_groups.json",

                        ]

# Определение списка исключаемых файлов
excluded_filenames:list[str] = [
                        "my_managed_groups.json",                        
                        "ru_usd.json",
                        "ger_en_eur.json",  
                ]

# Определение списка кампаний
campaigns:list = [
                  'brands',
                  'mom_and_baby',
                  'pain',
                  'sport_and_activity',
                  'house',
                  'bags_backpacks_suitcases',
                  'man'
              ]

# Создание объекта `FacebookPromoter`
promoter:FacebookPromoter = FacebookPromoter(driver, group_file_paths=filenames, no_video = True)

# Запуск цикла публикации
try:
    while True:
        
        # Публикация рекламных объявлений
        promoter.run_campaigns(campaigns = copy.copy(campaigns), group_file_paths = filenames)
        print(f"Going sleep {time.localtime}")
        time.sleep(180)

except KeyboardInterrupt:
    logger.info("Campaign promotion interrupted.")

```
```markdown
## Параметры

- `filenames` (list[str]): Список файлов, содержащих описание групп Facebook. Файлы должны быть в формате JSON и содержать информацию о группе,  например, ID группы,  название группы и т.д.
-  `excluded_filenames` (list[str]): Список файлов, которые нужно исключить из списка `filenames`.
-  `campaigns` (list): Список кампаний,  для которых необходимо опубликовать объявления.  Каждая кампания должна быть представлена  именем,  которое соответствует названию папки с рекламными материалами (изображения, видео и т. д.).

## Примеры 

```python
# Пример использования  `start_posting`  с  заданными параметрами
start_posting(filenames=['usa.json', 'he_ils.json'], excluded_filenames=[], campaigns=['brands', 'mom_and_baby'])
```