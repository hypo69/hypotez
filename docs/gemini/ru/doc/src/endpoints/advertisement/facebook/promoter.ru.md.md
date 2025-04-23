# Документация модуля Facebook Promoter

## Обзор

Модуль **Facebook Promoter** автоматизирует продвижение товаров и мероприятий AliExpress в группах Facebook. Модуль управляет публикациями рекламных материалов на Facebook, избегая дублирования. Для эффективного продвижения используется WebDriver для автоматизации браузера.

## Особенности модуля

- Продвижение категорий и мероприятий в группах Facebook.
- Избежание дублирования публикаций через отслеживание уже опубликованных элементов.
- Поддержка конфигурации данных групп через файлы.
- Возможность отключения загрузки видео в публикациях.

## Требования

- **Python** 3.x
- Необходимые библиотеки:
  - `random`
  - `datetime`
  - `pathlib`
  - `urllib.parse`
  - `types.SimpleNamespace`
  - `src` (пользовательский модуль)

## Использование

### Пример использования класса FacebookPromoter

```python
from src.endpoints.advertisement.facebook.promoter import FacebookPromoter
from src.webdriver.driver import Driver
from src.utils.jjson import j_loads_ns

# Настройка экземпляра WebDriver (замените на реальный WebDriver)
d = Driver()

# Создание экземпляра FacebookPromoter
promoter = FacebookPromoter(
    d=d, 
    promoter="aliexpress", 
    group_file_paths=["path/to/group/file1.json", "path/to/group/file2.json"]
)

# Начало продвижения товаров или мероприятий
promoter.process_groups(
    campaign_name="Campaign1",
    events=[], 
    group_categories_to_adv=["sales"],
    language="en",
    currency="USD"
)
```

## Классы

### Класс `FacebookPromoter`

**Описание**: Этот класс управляет процессом продвижения товаров и мероприятий AliExpress в группах Facebook.

**Принцип работы**:
1. Инициализируется WebDriver для управления браузером.
2. Получает данные о группах Facebook из указанных файлов.
3. Обрабатывает каждую группу для продвижения, проверяя валидность данных и интервалы между продвижениями.
4. Продвигает выбранные категории или мероприятия в группах.
5. Обновляет данные о продвижении для каждой группы.
6. Логирует ошибки при неудачном продвижении.

#### Методы

##### `__init__(self, d: Driver, promoter: str, group_file_paths: Optional[list[str | Path] | str | Path] = None, no_video: bool = False)`

**Назначение**: Инициализирует промоутер для Facebook с необходимыми конфигурациями.

**Параметры**:
- `d` (Driver): Экземпляр WebDriver для автоматизации.
- `promoter` (str): Имя промоутера (например, "aliexpress").
- `group_file_paths` (Optional[list[str | Path]  |  str | Path]): Пути к файлам с данными групп.
- `no_video` (bool): Флаг для отключения видео в публикациях. По умолчанию `False`.

**Как работает функция**:

Функция `__init__` инициализирует экземпляр класса `FacebookPromoter`. Она выполняет следующие действия:
1. Сохраняет переданные аргументы `d` (экземпляр WebDriver), `promoter` (имя промоутера) и `no_video` (флаг отключения видео) в атрибуты экземпляра класса.
2. Обрабатывает аргумент `group_file_paths`, который может быть списком путей, строкой пути или None. Приводит его к списку путей для дальнейшей обработки.
3. Сохраняет список путей к файлам групп в атрибут экземпляра класса.

**Примеры**:
```python
from src.webdriver.driver import Driver
from src.endpoints.advertisement.facebook.promoter import FacebookPromoter
from pathlib import Path

# Пример 1: Инициализация с указанием всех параметров
driver = Driver()
promoter = FacebookPromoter(d=driver, promoter="aliexpress", group_file_paths=["path/to/group1.json", "path/to/group2.json"], no_video=True)

# Пример 2: Инициализация с путем к одному файлу
driver = Driver()
promoter = FacebookPromoter(d=driver, promoter="aliexpress", group_file_paths="path/to/group.json")

# Пример 3: Инициализация без указания путей к файлам групп
driver = Driver()
promoter = FacebookPromoter(d=driver, promoter="aliexpress")
```

##### `promote(self, group: SimpleNamespace, item: SimpleNamespace, is_event: bool = False, language: str = None, currency: str = None) -> bool`

**Назначение**: Продвигает категорию или мероприятие в указанной группе Facebook.

**Параметры**:
- `group` (SimpleNamespace): Данные группы.
- `item` (SimpleNamespace): Категория или мероприятие для продвижения.
- `is_event` (bool): Является ли элемент мероприятием.
- `language` (str): Язык публикации.
- `currency` (str): Валюта для продвижения.

**Возвращает**:
- `bool`: Успешно ли прошло продвижение.

**Как работает функция**:

Функция `promote` выполняет продвижение товара или мероприятия в группе Facebook. Она выполняет следующие шаги:
1. Логирует начало процесса продвижения.
2. Подготавливает данные для публикации, включая URL, описание и цену.
3.  <инструкция для модели gemini:Авторизуется в Facebook, переходит в указанную группу, публикует рекламный пост и проверяет успешность публикации.>
4. Обрабатывает возможные исключения, логируя ошибки и возвращая `False` в случае неудачи.
5. Возвращает `True`, если продвижение прошло успешно, и `False` в противном случае.

**Примеры**:
```python
from types import SimpleNamespace
from src.webdriver.driver import Driver
from src.endpoints.advertisement.facebook.promoter import FacebookPromoter

# Пример создания экземпляра класса SimpleNamespace для имитации данных группы и товара
group_data = SimpleNamespace(id="1234567890", name="Test Group", url="https://www.facebook.com/groups/testgroup")
item_data = SimpleNamespace(name="Test Product", url="https://aliexpress.com/item/1234567890.html", price=10.00, image="https://ae01.alicdn.com/kf/test.jpg")

# Создание экземпляра класса FacebookPromoter (требуется предварительная настройка WebDriver)
driver = Driver() #  Замените на инициализацию вашего WebDriver
promoter = FacebookPromoter(d=driver, promoter="aliexpress")

# Вызов функции promote с данными группы и товара
success = promoter.promote(group=group_data, item=item_data, language="en", currency="USD")

if success:
    print("Продвижение успешно выполнено!")
else:
    print("Продвижение не удалось.")
```

##### `log_promotion_error(self, is_event: bool, item_name: str)`

**Назначение**: Записывает ошибку, если продвижение не удалось.

**Параметры**:
- `is_event` (bool): Является ли элемент мероприятием.
- `item_name` (str): Название элемента.

**Как работает функция**:

Функция `log_promotion_error` записывает сообщение об ошибке продвижения в лог. Она выполняет следующие действия:
1. Формирует сообщение об ошибке, указывая, является ли продвигаемый элемент мероприятием или категорией, и его название.
2. Использует модуль `logger` для записи сообщения об ошибке с уровнем `ERROR`.

**Примеры**:
```python
from src.webdriver.driver import Driver
from src.endpoints.advertisement.facebook.promoter import FacebookPromoter

# Создание экземпляра класса FacebookPromoter
driver = Driver() # Замените на инициализацию вашего WebDriver
promoter = FacebookPromoter(d=driver, promoter="aliexpress")

# Вызов функции log_promotion_error для логирования ошибки продвижения товара
promoter.log_promotion_error(is_event=False, item_name="Test Product")

# Вызов функции log_promotion_error для логирования ошибки продвижения мероприятия
promoter.log_promotion_error(is_event=True, item_name="Test Event")
```

##### `update_group_promotion_data(self, group: SimpleNamespace, item_name: str, is_event: bool = False)`

**Назначение**: Обновляет данные группы после продвижения, добавляя продвигаемый элемент в список продвигаемых категорий или мероприятий.

**Параметры**:
- `group` (SimpleNamespace): Данные группы.
- `item_name` (str): Название продвигаемого элемента.
- `is_event` (bool): Является ли элемент мероприятием.

**Как работает функция**:

Функция `update_group_promotion_data` обновляет информацию о продвижении в данных группы. Она выполняет следующие действия:
1. Определяет, является ли продвигаемый элемент мероприятием или категорией.
2. Добавляет имя продвигаемого элемента в соответствующий список (promoted_events или promoted_categories) в данных группы.
3. Обновляет время последнего продвижения группы.

**Примеры**:
```python
from types import SimpleNamespace
from src.webdriver.driver import Driver
from src.endpoints.advertisement.facebook.promoter import FacebookPromoter
import datetime

# Пример создания экземпляра класса SimpleNamespace для имитации данных группы
group_data = SimpleNamespace(
    id="1234567890", 
    name="Test Group", 
    url="https://www.facebook.com/groups/testgroup",
    promoted_categories=[],
    promoted_events=[],
    last_promotion_time=None
)

# Создание экземпляра класса FacebookPromoter (требуется предварительная настройка WebDriver)
driver = Driver() # Замените на инициализацию вашего WebDriver
promoter = FacebookPromoter(d=driver, promoter="aliexpress")

# Вызов функции update_group_promotion_data после продвижения товара
promoter.update_group_promotion_data(group=group_data, item_name="Test Product", is_event=False)

# Вызов функции update_group_promotion_data после продвижения мероприятия
promoter.update_group_promotion_data(group=group_data, item_name="Test Event", is_event=True)

# Вывод обновленных данных группы
print(group_data.promoted_categories)
print(group_data.promoted_events)
print(group_data.last_promotion_time)
```

##### `process_groups(self, campaign_name: str = None, events: list[SimpleNamespace] = None, is_event: bool = False, group_file_paths: list[str] = None, group_categories_to_adv: list[str] = ['sales'], language: str = None, currency: str = None)`

**Назначение**: Обрабатывает группы для текущей кампании или продвижения мероприятия.

**Параметры**:
- `campaign_name` (str): Название кампании.
- `events` (list[SimpleNamespace]): Список мероприятий для продвижения.
- `is_event` (bool): Является ли продвижение мероприятий или категорий.
- `group_file_paths` (list[str]): Пути к файлам с данными групп.
- `group_categories_to_adv` (list[str]): Категории для продвижения.
- `language` (str): Язык публикации.
- `currency` (str): Валюта для продвижения.

**Как работает функция**:

Функция `process_groups` выполняет обработку групп Facebook для продвижения товаров или мероприятий. Она выполняет следующие шаги:
1. Определяет, продвигаются ли мероприятия или категории.
2.  <инструкция для модели gemini:Загружает данные о группах из файлов, указанных в `group_file_paths` или из атрибута `group_file_paths` класса, если `group_file_paths` не указан.>
3. Итерируется по списку групп и выполняет следующие действия для каждой группы:
   - Проверяет, является ли группа валидной, вызывая метод `validate_group`. Если группа не валидна, записывает ошибку в лог.
   - Проверяет, можно ли продвигать группу в данный момент, вызывая метод `check_interval`. Если группа не может быть продвинута, переходит к следующей группе.
   - Получает элемент категории или мероприятие для продвижения, вызывая метод `get_category_item`.
   - Продвигает элемент в группе, вызывая метод `promote`.
   - Обновляет данные о продвижении группы, вызывая метод `update_group_promotion_data`.
4. Обрабатывает возможные исключения, логируя ошибки.

**Примеры**:
```python
from types import SimpleNamespace
from src.webdriver.driver import Driver
from src.endpoints.advertisement.facebook.promoter import FacebookPromoter

# Пример создания экземпляра класса FacebookPromoter (требуется предварительная настройка WebDriver и файлов групп)
driver = Driver() # Замените на инициализацию вашего WebDriver
promoter = FacebookPromoter(d=driver, promoter="aliexpress", group_file_paths=["path/to/group1.json", "path/to/group2.json"])

# Пример вызова функции process_groups для продвижения категорий
promoter.process_groups(campaign_name="SummerSales", group_categories_to_adv=["shoes", "bags"], language="en", currency="USD")

# Пример вызова функции process_groups для продвижения мероприятий
event1 = SimpleNamespace(name="Summer Sale", url="https://aliexpress.com/event/summersale.html")
event2 = SimpleNamespace(name="Black Friday", url="https://aliexpress.com/event/blackfriday.html")
promoter.process_groups(events=[event1, event2], is_event=True, language="en", currency="USD")
```

##### `get_category_item(self, campaign_name: str, group: SimpleNamespace, language: str, currency: str) -> SimpleNamespace`

**Назначение**: Получает элемент категории для продвижения в зависимости от кампании и промоутера.

**Параметры**:
- `campaign_name` (str): Название кампании.
- `group` (SimpleNamespace): Данные группы.
- `language` (str): Язык для публикации.
- `currency` (str): Валюта для публикации.

**Возвращает**:
- `SimpleNamespace`: Элемент категории для продвижения.

**Как работает функция**:

Функция `get_category_item` определяет, какой элемент категории продвигать в данной группе. Она выполняет следующие шаги:
1.  <инструкция для модели gemini:Формирует путь к файлу с данными о товарах для продвижения на основе имени кампании, имени промоутера и языка.>
2.  <инструкция для модели gemini:Загружает данные о товарах из файла, используя функцию `j_loads_ns`.>
3. Выбирает случайный элемент из списка товаров.
4.  <инструкция для модели gemini:Добавляет информацию о языке и валюте к выбранному элементу.>
5. Возвращает выбранный элемент.

**Примеры**:
```python
from types import SimpleNamespace
from src.webdriver.driver import Driver
from src.endpoints.advertisement.facebook.promoter import FacebookPromoter

# Пример создания экземпляра класса FacebookPromoter (требуется предварительная настройка WebDriver и файлов групп)
driver = Driver() # Замените на инициализацию вашего WebDriver
promoter = FacebookPromoter(d=driver, promoter="aliexpress")

# Пример создания экземпляра класса SimpleNamespace для имитации данных группы
group_data = SimpleNamespace(id="1234567890", name="Test Group", url="https://www.facebook.com/groups/testgroup")

# Вызов функции get_category_item для получения элемента категории для продвижения
category_item = promoter.get_category_item(campaign_name="SummerSales", group=group_data, language="en", currency="USD")

# Вывод полученных данных
print(category_item)
```

##### `check_interval(self, group: SimpleNamespace) -> bool`

**Назначение**: Проверяет, прошло ли достаточно времени, чтобы снова продвигать эту группу.

**Параметры**:
- `group` (SimpleNamespace): Данные группы.

**Возвращает**:
- `bool`: Можно ли снова продвигать группу.

**Как работает функция**:

Функция `check_interval` проверяет, прошло ли достаточно времени с момента последнего продвижения группы. Она выполняет следующие шаги:
1.  <инструкция для модели gemini:Получает время последнего продвижения группы из данных группы.>
2. Если время последнего продвижения не установлено, возвращает `True` (группу можно продвигать).
3.  <инструкция для модели gemini:Вычисляет разницу во времени между текущим временем и временем последнего продвижения.>
4.  <инструкция для модели gemini:Определяет интервал между продвижениями на основе имени промоутера (в данном случае "aliexpress").>
5.  <инструкция для модели gemini:Проверяет, прошло ли достаточно времени с момента последнего продвижения.>
6. Возвращает `True`, если прошло достаточно времени, и `False` в противном случае.

**Примеры**:
```python
from types import SimpleNamespace
from src.webdriver.driver import Driver
from src.endpoints.advertisement.facebook.promoter import FacebookPromoter
import datetime

# Пример создания экземпляра класса SimpleNamespace для имитации данных группы
group_data = SimpleNamespace(
    id="1234567890", 
    name="Test Group", 
    url="https://www.facebook.com/groups/testgroup",
    promoted_categories=[],
    promoted_events=[],
    last_promotion_time=None
)

# Создание экземпляра класса FacebookPromoter (требуется предварительная настройка WebDriver и файлов групп)
driver = Driver() # Замените на инициализацию вашего WebDriver
promoter = FacebookPromoter(d=driver, promoter="aliexpress")

# Пример проверки интервала для группы, которая еще не продвигалась
can_promote = promoter.check_interval(group=group_data)
print(f"Можно продвигать группу: {can_promote}")

# Пример установки времени последнего продвижения и повторной проверки интервала
group_data.last_promotion_time = datetime.datetime.now() - datetime.timedelta(hours=1)
can_promote = promoter.check_interval(group=group_data)
print(f"Можно продвигать группу: {can_promote}")
```

##### `validate_group(self, group: SimpleNamespace) -> bool`

**Назначение**: Проверяет данные группы, чтобы убедиться в их корректности.

**Параметры**:
- `group` (SimpleNamespace): Данные группы.

**Возвращает**:
- `bool`: Корректны ли данные группы.

**Как работает функция**:

Функция `validate_group` проверяет, являются ли данные группы Facebook корректными. Она выполняет следующие шаги:
1. Проверяет наличие обязательных атрибутов `id`, `name` и `url` в данных группы.
2. Проверяет, что `id` является числом, `name` и `url` являются строками.
3. Проверяет, что URL группы является валидным URL, используя `urllib.parse.urlparse`.
4. Логирует ошибки, если какие-либо из проверок не проходят.
5. Возвращает `True`, если все проверки пройдены успешно, и `False` в противном случае.

**Примеры**:
```python
from types import SimpleNamespace
from src.webdriver.driver import Driver
from src.endpoints.advertisement.facebook.promoter import FacebookPromoter

# Создание экземпляра класса FacebookPromoter (требуется предварительная настройка WebDriver и файлов групп)
driver = Driver() # Замените на инициализацию вашего WebDriver
promoter = FacebookPromoter(d=driver, promoter="aliexpress")

# Пример создания экземпляра класса SimpleNamespace с корректными данными группы
group_data_valid = SimpleNamespace(
    id="1234567890", 
    name="Test Group", 
    url="https://www.facebook.com/groups/testgroup"
)

# Пример создания экземпляра класса SimpleNamespace с некорректными данными группы (неверный URL)
group_data_invalid = SimpleNamespace(
    id="1234567890", 
    name="Test Group", 
    url="invalid_url"
)

# Проверка валидности данных группы
is_valid = promoter.validate_group(group=group_data_valid)
print(f"Данные группы валидны: {is_valid}")

is_valid = promoter.validate_group(group=group_data_invalid)
print(f"Данные группы валидны: {is_valid}")
```

## Лицензия

Модуль является частью пакета **Facebook Promoter** и лицензируется по лицензии MIT.