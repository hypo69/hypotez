# Модуль для продвижения в Facebook группах
## Обзор

Модуль `promoter.py` предназначен для автоматизации продвижения сообщений и событий в группах Facebook. Он обрабатывает кампании и события, публикуя их в группах Facebook, избегая повторных публикаций.

## Подробнее

Этот модуль предоставляет класс `FacebookPromoter`, который позволяет продвигать товары и события AliExpress в группах Facebook. Класс использует WebDriver для автоматизации публикаций в Facebook, обеспечивая продвижение категорий и событий, избегая дублирования.

## Классы

### `FacebookPromoter`

**Описание**: Класс для продвижения товаров AliExpress и событий в группах Facebook.

**Принцип работы**:
Класс `FacebookPromoter` автоматизирует процесс публикации рекламных материалов в группах Facebook. Он использует WebDriver для управления браузером и выполнения действий, таких как вход в Facebook, навигация по группам и публикация сообщений. Класс также включает логику для предотвращения повторных публикаций и управления интервалами между публикациями.

**Аттрибуты**:

- `d` (Driver): Инстанс WebDriver для автоматизации браузера.
- `group_file_paths` (str | Path): Список путей к файлам, содержащим данные групп Facebook.
- `no_video` (bool): Флаг, указывающий на необходимость отключения видео в постах.
- `promoter` (str): Имя промоутера.

**Методы**:

- `__init__`: Инициализирует экземпляр класса `FacebookPromoter`.
- `promote`: Продвигает категорию или событие в группе Facebook.
- `log_promotion_error`: Логирует ошибку продвижения для категории или события.
- `update_group_promotion_data`: Обновляет данные о продвижении группы с новой информацией о продвижении.
- `process_groups`: Обрабатывает все группы для текущей кампании или продвижения событий.
- `get_category_item`: Получает элемент категории для продвижения на основе кампании и промоутера.
- `check_interval`: Проверяет, достаточно ли времени прошло для продвижения этой группы.
- `validate_group`: Проверяет, что данные группы корректны.

### `__init__`

```python
def __init__(self, d: Driver, promoter: str, group_file_paths: Optional[list[str | Path] | str | Path] = None, no_video: bool = False):
    """ Инициализирует промоутера для Facebook групп.

    Args:
        d (Driver): WebDriver instance для автоматизации браузера.
        promoter (str): Имя промоутера.
        group_file_paths (list[str | Path] | str | Path, optional): Список путей к файлам, содержащим данные групп. По умолчанию `None`.
        no_video (bool, optional): Флаг для отключения видео в постах. По умолчанию `False`.
    """
```

**Назначение**: Инициализирует экземпляр класса `FacebookPromoter` с заданными параметрами.

**Параметры**:

- `d` (Driver): Инстанс WebDriver для управления браузером.
- `promoter` (str): Имя промоутера.
- `group_file_paths` (list[str | Path] | str | Path, optional): Список путей к файлам, содержащим данные групп Facebook. По умолчанию `None`. Если не указан, используется путь по умолчанию из `gs.path.google_drive / 'facebook' / 'groups'`.
- `no_video` (bool, optional): Флаг, указывающий, следует ли отключать видео в постах. По умолчанию `False`.

**Как работает функция**:

1. **Инициализация атрибутов**: Функция инициализирует атрибуты экземпляра класса `FacebookPromoter` переданными значениями: `promoter`, `d` (WebDriver instance), `group_file_paths` и `no_video`.
2. **Обработка `group_file_paths`**: Если `group_file_paths` не указан, он получает список файлов из директории `gs.path.google_drive / 'facebook' / 'groups'` с помощью функции `get_filenames`.
3. **Инициализация спиннера**: Создает экземпляр класса `spinning_cursor` для отображения спиннера в консоли во время выполнения операций.

```
Инициализация атрибутов --> Проверка и установка путей к файлам групп --> Инициализация спиннера
```

**Примеры**:

```python
from src.webdriver.driver import Driver
from src.webdriver import Firefox

# Создание инстанса драйвера
driver = Driver(Firefox)

# Пример инициализации FacebookPromoter с указанием путей к файлам групп
promoter = FacebookPromoter(d=driver, promoter='aliexpress', group_file_paths=['path/to/group1.json', 'path/to/group2.json'])

# Пример инициализации FacebookPromoter без указания путей к файлам групп (будет использован путь по умолчанию)
promoter = FacebookPromoter(d=driver, promoter='aliexpress')
```

### `promote`

```python
def promote(self, group: SimpleNamespace, item: SimpleNamespace, is_event: bool = False, language: str = None, currency: str = None) -> bool:
    """Продвигает категорию или событие в группе Facebook."""
    ...
```

**Назначение**: Продвигает категорию или событие в указанной группе Facebook.

**Параметры**:

- `group` (SimpleNamespace): Объект, содержащий данные о группе Facebook.
- `item` (SimpleNamespace): Объект, содержащий данные о категории или событии для продвижения.
- `is_event` (bool, optional): Флаг, указывающий, является ли продвигаемый элемент событием. По умолчанию `False`.
- `language` (str, optional): Язык, на котором нужно продвигать. По умолчанию `None`.
- `currency` (str, optional): Валюта, в которой нужно продвигать. По умолчанию `None`.

**Возвращает**:

- `bool`: `True`, если продвижение прошло успешно, иначе `False`.

**Как работает функция**:

1. **Проверка соответствия языка и валюты**: Если указаны язык и валюта, функция проверяет, соответствуют ли они языку и валюте группы. Если нет, функция завершается.
2. **Выбор объекта для продвижения**: В зависимости от того, является ли продвигаемый элемент событием или категорией, функция выбирает соответствующий объект для продвижения.
3. **Продвижение события**: Если продвигается событие, функция вызывает функцию `post_event` для публикации события в группе Facebook.
4. **Продвижение категории**: Если продвигается категория, функция вызывает функцию `post_message` для публикации сообщения о категории в группе Facebook. Если промоутер - kazarinov или emil, то вызывается `post_ad`
5. **Обновление данных группы**: После успешной публикации функция вызывает функцию `update_group_promotion_data` для обновления данных о продвижении группы.
6. **Возврат результата**: Функция возвращает `True`, если продвижение прошло успешно, и `False` в противном случае.

```
Проверка соответствия языка и валюты --> Выбор объекта для продвижения --> Продвижение события или категории --> Обновление данных группы --> Возврат результата
```

**Примеры**:

```python
from src.webdriver.driver import Driver
from src.webdriver import Firefox
from types import SimpleNamespace

# Создание инстанса драйвера
driver = Driver(Firefox)

# Создание инстанса промоутера
promoter = FacebookPromoter(d=driver, promoter='aliexpress')

# Создание тестовых данных для группы и элемента
group = SimpleNamespace(
    group_url='https://www.facebook.com/groups/testgroup',
    language='ru',
    currency='USD'
)
item = SimpleNamespace(
    category_name='test_category',
    language=SimpleNamespace(ru='Тестовая категория')
)

# Пример продвижения категории
result = promoter.promote(group=group, item=item)
print(f"Результат продвижения категории: {result}")

# Создание тестовых данных для события
event = SimpleNamespace(
    event_name='test_event',
    language=SimpleNamespace(ru='Тестовое событие'),
    start='2024-01-01',
    end='2024-01-02',
    promotional_link='https://example.com'
)

# Пример продвижения события
result = promoter.promote(group=group, item=event, is_event=True)
print(f"Результат продвижения события: {result}")
```

### `log_promotion_error`

```python
def log_promotion_error(self, is_event: bool, item_name: str):
    """Logs promotion error for category or event."""
    logger.debug(f"Error while posting {\'event\' if is_event else \'category\'} {item_name}", None, False)
```

**Назначение**: Логирует ошибку продвижения для категории или события.

**Параметры**:

- `is_event` (bool): Флаг, указывающий, является ли продвигаемый элемент событием.
- `item_name` (str): Название категории или события, для которого произошла ошибка.

**Как работает функция**:

1. **Формирование сообщения об ошибке**: Функция формирует сообщение об ошибке, которое включает тип продвигаемого элемента (событие или категория) и его название.
2. **Логирование ошибки**: Функция использует модуль `logger` для записи сообщения об ошибке в лог.

**Примеры**:

```python
from src.webdriver.driver import Driver
from src.webdriver import Firefox
from src.logger.logger import logger

# Создание инстанса драйвера
driver = Driver(Firefox)

# Создание инстанса промоутера
promoter = FacebookPromoter(d=driver, promoter='aliexpress')

# Пример логирования ошибки продвижения категории
promoter.log_promotion_error(is_event=False, item_name='test_category')
# Вывод в лог: "Error while posting category test_category"

# Пример логирования ошибки продвижения события
promoter.log_promotion_error(is_event=True, item_name='test_event')
# Вывод в лог: "Error while posting event test_event"
```

### `update_group_promotion_data`

```python
def update_group_promotion_data(self, group: SimpleNamespace, item_name: str, is_event: bool = False):
    """Updates group promotion data with the new promotion."""
    timestamp = datetime.now().strftime("%d/%m/%y %H:%M")
    group.last_promo_sended = gs.now
    if is_event:
        group.promoted_events = group.promoted_events if isinstance(group.promoted_events, list) else [group.promoted_events]
        group.promoted_events.append(item_name)
    else:
        group.promoted_categories = group.promoted_categories if isinstance(group.promoted_categories, list) else [group.promoted_categories]
        group.promoted_categories.append(item_name)
    group.last_promo_sended = timestamp
```

**Назначение**: Обновляет данные о продвижении группы информацией о новой публикации.

**Параметры**:

- `group` (SimpleNamespace): Объект, представляющий группу Facebook, данные которой нужно обновить.
- `item_name` (str): Название продвигаемого элемента (категории или события).
- `is_event` (bool, optional): Флаг, указывающий, является ли продвигаемый элемент событием. По умолчанию `False`.

**Как работает функция**:

1. **Получение текущей временной метки**: Функция получает текущую дату и время и форматирует их в строку.
2. **Обновление времени последней отправки**: Функция обновляет атрибут `last_promo_sended` объекта `group` текущей временной меткой.
3. **Обновление списка продвигаемых событий или категорий**: В зависимости от того, является ли продвигаемый элемент событием или категорией, функция добавляет название элемента в список `promoted_events` или `promoted_categories` объекта `group`. Если список не существует, он создается.

```
Получение текущей временной метки --> Обновление времени последней отправки --> Обновление списка продвигаемых событий или категорий
```

**Примеры**:

```python
from types import SimpleNamespace
from src.webdriver.driver import Driver
from src.webdriver import Firefox

# Создание инстанса драйвера
driver = Driver(Firefox)
# Создание инстанса промоутера
promoter = FacebookPromoter(d=driver, promoter='aliexpress')

# Создание тестовых данных для группы
group = SimpleNamespace(
    group_url='https://www.facebook.com/groups/testgroup',
    language='ru',
    currency='USD',
    promoted_categories=['old_category'],
    promoted_events=['old_event']
)

# Пример обновления данных группы после продвижения категории
promoter.update_group_promotion_data(group=group, item_name='new_category', is_event=False)
print(f"Список продвигаемых категорий: {group.promoted_categories}")
print(f"Время последней отправки: {group.last_promo_sended}")

# Пример обновления данных группы после продвижения события
promoter.update_group_promotion_data(group=group, item_name='new_event', is_event=True)
print(f"Список продвигаемых событий: {group.promoted_events}")
print(f"Время последней отправки: {group.last_promo_sended}")
```

### `process_groups`

```python
def process_groups(self, campaign_name: str = None, events: list[SimpleNamespace] = None, is_event: bool = False, group_file_paths: list[str] = None, group_categories_to_adv: list[str] = ['sales'], language: str = None, currency: str = None):
    """Processes all groups for the current campaign or event promotion."""
    ...
```

**Назначение**: Обрабатывает все группы для продвижения текущей кампании или события.

**Параметры**:

- `campaign_name` (str, optional): Название кампании. По умолчанию `None`.
- `events` (list[SimpleNamespace], optional): Список событий для продвижения. По умолчанию `None`.
- `is_event` (bool, optional): Флаг, указывающий, является ли продвижение событием. По умолчанию `False`.
- `group_file_paths` (list[str], optional): Список путей к файлам с данными о группах. По умолчанию `None`.
- `group_categories_to_adv` (list[str], optional): Список категорий групп для продвижения. По умолчанию `['sales']`.
- `language` (str, optional): Язык, на котором нужно продвигать. По умолчанию `None`.
- `currency` (str, optional): Валюта, в которой нужно продвигать. По умолчанию `None`.

**Как работает функция**:

1. **Проверка наличия кампании или событий**: Функция проверяет, указаны ли имя кампании или список событий для продвижения. Если ни то, ни другое не указано, функция завершается.
2. **Перебор файлов с данными о группах**: Функция перебирает файлы, указанные в параметре `group_file_paths`.
3. **Загрузка данных о группах**: Для каждого файла функция загружает данные о группах с помощью функции `j_loads_ns`.
4. **Перебор групп**: Функция перебирает группы, указанные в файле.
5. **Проверка интервала**: Если продвигается не событие, функция проверяет, прошло ли достаточно времени с момента последней публикации в группе.
6. **Проверка категорий и статуса**: Функция проверяет, соответствует ли категория группы категориям, указанным в параметре `group_categories_to_adv`, и активен ли статус группы.
7. **Получение элемента для продвижения**: Функция получает элемент (категорию или событие) для продвижения с помощью функции `get_category_item`.
8. **Проверка на повторную публикацию**: Функция проверяет, был ли уже опубликован данный элемент в группе.
9. **Получение URL группы** Если продвигается событие, то берется event_url, иначе group_url.
10. **Продвижение элемента**: Функция вызывает функцию `promote` для публикации элемента в группе.
11. **Сохранение данных о группах**: Функция сохраняет обновленные данные о группах в файл с помощью функции `j_dumps`.
12. **Ожидание**: Функция ожидает случайное количество времени перед переходом к следующей группе.

```
Проверка наличия кампании или событий --> Перебор файлов с данными о группах --> Загрузка данных о группах --> Перебор групп --> Проверка интервала --> Проверка категорий и статуса --> Получение элемента для продвижения --> Проверка на повторную публикацию --> Продвижение элемента --> Сохранение данных о группах --> Ожидание
```

**Примеры**:

```python
from src.webdriver.driver import Driver
from src.webdriver import Firefox
from types import SimpleNamespace

# Создание инстанса драйвера
driver = Driver(Firefox)

# Создание инстанса промоутера
promoter = FacebookPromoter(d=driver, promoter='aliexpress')

# Пример вызова process_groups для продвижения кампании
promoter.process_groups(campaign_name='test_campaign', group_file_paths=['path/to/group1.json', 'path/to/group2.json'])

# Пример вызова process_groups для продвижения событий
events = [
    SimpleNamespace(
        event_name='test_event1',
        language=SimpleNamespace(ru='Тестовое событие 1'),
        start='2024-01-01',
        end='2024-01-02',
        promotional_link='https://example.com/event1'
    ),
    SimpleNamespace(
        event_name='test_event2',
        language=SimpleNamespace(ru='Тестовое событие 2'),
        start='2024-01-03',
        end='2024-01-04',
        promotional_link='https://example.com/event2'
    )
]
promoter.process_groups(events=events, is_event=True, group_file_paths=['path/to/group1.json', 'path/to/group2.json'])
```

### `get_category_item`

```python
def get_category_item(self, campaign_name: str, group: SimpleNamespace, language: str, currency: str) -> SimpleNamespace:
    """Fetches the category item for promotion based on the campaign and promoter."""
    ...
```

**Назначение**: Получает элемент категории для продвижения на основе кампании и промоутера.

**Параметры**:

- `campaign_name` (str): Название кампании.
- `group` (SimpleNamespace): Объект, содержащий данные о группе Facebook.
- `language` (str): Язык, на котором нужно продвигать.
- `currency` (str): Валюта, в которой нужно продвигать.

**Возвращает**:

- `SimpleNamespace`: Объект, содержащий данные о категории для продвижения.

**Как работает функция**:

1. **Проверка промоутера**: Функция проверяет, является ли промоутер 'aliexpress'.
2. **Получение элемента для aliexpress**: Если промоутер 'aliexpress', функция использует класс `AliCampaignEditor` для получения категории и ее продуктов.
3. **Получение элемента для других промоутеров**: Если промоутер не 'aliexpress', функция загружает данные о категориях из JSON-файла, выбирает случайную категорию и получает ее описание и изображение.

```
Проверка промоутера --> Получение элемента для aliexpress или других промоутеров
```

**Примеры**:

```python
from src.webdriver.driver import Driver
from src.webdriver import Firefox
from types import SimpleNamespace

# Создание инстанса драйвера
driver = Driver(Firefox)

# Создание инстанса промоутера
promoter = FacebookPromoter(d=driver, promoter='aliexpress')

# Создание тестовых данных для группы
group = SimpleNamespace(
    group_url='https://www.facebook.com/groups/testgroup',
    language='ru',
    currency='USD'
)

# Пример получения элемента категории для aliexpress
item = promoter.get_category_item(campaign_name='test_campaign', group=group, language='ru', currency='USD')
print(f"Элемент категории: {item}")

# Пример получения элемента категории для другого промоутера (предполагается, что файлы кампании существуют)
promoter.promoter = 'other_promoter'
item = promoter.get_category_item(campaign_name='test_campaign', group=group, language='ru', currency='USD')
print(f"Элемент категории: {item}")
```

### `check_interval`

```python
def check_interval(self, group: SimpleNamespace) -> bool:
    """Checks if enough time has passed for promoting this group."""
    ...
```

**Назначение**: Проверяет, прошло ли достаточно времени для продвижения этой группы.

**Параметры**:

- `group` (SimpleNamespace): Объект, содержащий данные о группе Facebook, включая время последней отправки.

**Возвращает**:

- `bool`: `True`, если достаточно времени прошло для продвижения группы, `False` в противном случае.

**Как работает функция**:

Функция в текущей реализации всегда возвращает `True`, то есть предполагает, что достаточно времени прошло для продвижения группы. В реальной реализации здесь должна быть логика проверки времени, прошедшего с момента последней публикации, и сравнения его с заданным интервалом.

**Примеры**:

```python
from types import SimpleNamespace
from src.webdriver.driver import Driver
from src.webdriver import Firefox

# Создание инстанса драйвера
driver = Driver(Firefox)
# Создание инстанса промоутера
promoter = FacebookPromoter(d=driver, promoter='aliexpress')

# Создание тестовых данных для группы
group = SimpleNamespace(
    group_url='https://www.facebook.com/groups/testgroup',
    language='ru',
    currency='USD',
    last_promo_sended='01/01/24 10:00'
)

# Пример проверки интервала
result = promoter.check_interval(group=group)
print(f"Прошло достаточно времени для продвижения: {result}")
```

### `validate_group`

```python
def validate_group(self, group: SimpleNamespace) -> bool:
    """Validates that the group data is correct."""
    return group and hasattr(group, 'group_url') and hasattr(group, 'group_categories')
```

**Назначение**: Проверяет, что данные группы корректны.

**Параметры**:

- `group` (SimpleNamespace): Объект, представляющий группу Facebook, данные которой нужно проверить.

**Возвращает**:

- `bool`: `True`, если данные группы корректны, `False` в противном случае.

**Как работает функция**:

Функция проверяет, что объект `group` не является `None` и содержит атрибуты `group_url` и `group_categories`. Если все условия выполняются, функция возвращает `True`, иначе `False`.

**Примеры**:

```python
from types import SimpleNamespace
from src.webdriver.driver import Driver
from src.webdriver import Firefox

# Создание инстанса драйвера
driver = Driver(Firefox)
# Создание инстанса промоутера
promoter = FacebookPromoter(d=driver, promoter='aliexpress')

# Создание тестовых данных для группы
group = SimpleNamespace(
    group_url='https://www.facebook.com/groups/testgroup',
    group_categories=['sales', 'marketing']
)

# Пример проверки данных группы
result = promoter.validate_group(group=group)
print(f"Данные группы корректны: {result}")

# Пример проверки данных группы с отсутствующим атрибутом
group = SimpleNamespace(
    group_url='https://www.facebook.com/groups/testgroup'
)
result = promoter.validate_group(group=group)
print(f"Данные группы корректны: {result}")
```

## Функции

### `get_event_url`

```python
def get_event_url(group_url: str) -> str:
    """
    Returns the modified URL for creating an event on Facebook, replacing `group_id` with the value from the input URL.

    Args:
        group_url (str): Facebook group URL containing `group_id`.

    Returns:
        str: Modified URL for creating the event.
    """
    ...
```

**Назначение**: Возвращает измененный URL для создания события в Facebook, заменяя `group_id` значением из входного URL.

**Параметры**:

- `group_url` (str): URL группы Facebook, содержащий `group_id`.

**Возвращает**:

- `str`: Измененный URL для создания события.

**Как работает функция**:

1. **Извлечение `group_id`**: Извлекает `group_id` из URL группы Facebook.
2. **Формирование базового URL**: Определяет базовый URL для создания события в Facebook.
3. **Формирование параметров запроса**: Создает словарь с параметрами запроса, включая `acontext`, `dialog_entry_point` и `group_id`.
4. **Кодирование параметров запроса**: Кодирует параметры запроса в строку запроса.
5. **Формирование полного URL**: Объединяет базовый URL и строку запроса для создания полного URL для создания события.

```
Извлечение group_id --> Формирование базового URL --> Формирование параметров запроса --> Кодирование параметров запроса --> Формирование полного URL
```

**Примеры**:

```python
# Пример использования функции
group_url = "https://www.facebook.com/groups/1234567890"
event_url = get_event_url(group_url)
print(f"URL для создания события: {event_url}")