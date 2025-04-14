# Модуль для продвижения в Facebook

## Обзор

Модуль `promoter.py` предназначен для автоматизации процесса продвижения контента, такого как сообщения и события, в группах Facebook. Он обрабатывает кампании и события, публикуя их в группах Facebook, и предотвращает дублирование публикаций.

## Подробней

Этот модуль является частью системы автоматизации маркетинга `hypotez` и специализируется на взаимодействии с Facebook. Он использует WebDriver для автоматизации действий в браузере, таких как публикация сообщений и событий в группах. Модуль включает функциональность для настройки времени между публикациями, выбора целевых групп и категорий, а также для обработки мультиязычного контента.

## Классы

### `FacebookPromoter`

**Описание**: Класс для продвижения товаров и событий AliExpress в группах Facebook.

**Атрибуты**:
- `d` (Driver): Экземпляр WebDriver для автоматизации браузера.
- `group_file_paths` (str | Path): Список путей к файлам, содержащим данные о группах.
- `no_video` (bool): Флаг, указывающий, следует ли отключать видео в постах.
- `promoter` (str): Имя промоутера.

**Методы**:
- `__init__`: Инициализирует промоутер для групп Facebook.
- `promote`: Продвигает категорию или событие в группе Facebook.
- `log_promotion_error`: Регистрирует ошибку продвижения для категории или события.
- `update_group_promotion_data`: Обновляет данные о продвижении группы, добавляя информацию о новой публикации.
- `process_groups`: Обрабатывает все группы для текущей кампании или продвижения события.
- `get_category_item`: Получает элемент категории для продвижения на основе кампании и промоутера.
- `check_interval`: Проверяет, достаточно ли времени прошло для продвижения этой группы.
- `validate_group`: Проверяет, корректны ли данные группы.

### `__init__`

```python
def __init__(self, d: Driver, promoter: str, group_file_paths: Optional[list[str | Path] | str | Path] = None, no_video: bool = False):
    """Инициализирует промоутер для Facebook групп.

    Args:
        d (Driver): WebDriver instance for browser automation.
        promoter (str): Имя промоутера.
        group_file_paths (list[str | Path] | str | Path, optional): Список файловых путей, содержащих данные о группах. Defaults to None.
        no_video (bool, optional): Флаг для отключения видео в постах. Defaults to False.
    """
    ...
```

**Назначение**: Инициализирует экземпляр класса `FacebookPromoter`.

**Параметры**:
- `d` (Driver): Экземпляр WebDriver для управления браузером.
- `promoter` (str): Имя промоутера.
- `group_file_paths` (list[str | Path] | str | Path, optional): Список путей к файлам, содержащим информацию о группах Facebook. Если не указан, используется путь по умолчанию. По умолчанию `None`.
- `no_video` (bool, optional): Флаг, указывающий, нужно ли отключать использование видео в рекламных постах. По умолчанию `False`.

**Как работает функция**:
- Устанавливает значения атрибутов экземпляра класса: `promoter`, `d` (WebDriver instance), `group_file_paths` (пути к файлам с данными о группах) и `no_video` (флаг отключения видео).
- Если `group_file_paths` не указаны, использует функцию `get_filenames` для получения списка файлов из директории `gs.path.google_drive / 'facebook' / 'groups'`.
- Инициализирует `spinning_cursor` для отображения спиннера в консоли во время выполнения операций.

**Примеры**:

```python
from src.webdriver.driver import Driver
from src.webdriver import Firefox
driver = Driver(Firefox)
promoter = FacebookPromoter(d=driver, promoter='test_promoter', group_file_paths=['group1.json', 'group2.json'], no_video=True)
```

### `promote`

```python
def promote(self, group: SimpleNamespace, item: SimpleNamespace, is_event: bool = False, language: str = None, currency: str = None) -> bool:
    """Продвигает категорию или событие в Facebook группе.

    Args:
        group (SimpleNamespace): Данные о группе Facebook.
        item (SimpleNamespace): Данные о категории или события для продвижения.
        is_event (bool, optional): Флаг, указывающий, является ли продвигаемый объект событием. Defaults to False.
        language (str, optional): Язык продвижения. Defaults to None.
        currency (str, optional): Валюта продвижения. Defaults to None.

    Returns:
        bool: `True`, если продвижение прошло успешно, `False` в противном случае.
    """
    ...
```

**Назначение**: Продвигает категорию или событие в указанной группе Facebook.

**Параметры**:
- `group` (SimpleNamespace): Объект, содержащий данные о группе Facebook, включая URL, категории и другие параметры.
- `item` (SimpleNamespace): Объект, содержащий данные о продвигаемом элементе (категории или событии), включая название, описание и другие параметры.
- `is_event` (bool, optional): Флаг, указывающий, является ли продвигаемый элемент событием. По умолчанию `False`.
- `language` (str, optional): Язык, на котором должно быть выполнено продвижение. Если указан, сравнивается с языком группы. По умолчанию `None`.
- `currency` (str, optional): Валюта, используемая для продвижения. Если указана, сравнивается с валютой группы. По умолчанию `None`.

**Как работает функция**:
1. **Проверка языка и валюты**:
   - Если указаны `language` и `currency`, функция проверяет, соответствуют ли они языку и валюте, установленным для группы. Если не соответствуют, функция завершается.
2. **Выбор имени элемента**:
   - Определяет имя продвигаемого элемента в зависимости от того, является ли это событие или категория.
3. **Установка атрибутов для события**:
   - Если продвигается событие (`is_event` is `True`), устанавливает атрибуты события (начало, конец, рекламная ссылка).
4. **Публикация события или сообщения**:
   - Если продвигается событие, вызывается функция `post_event`.
   - Иначе, вызывается функция `post_message` для публикации сообщения.
5. **Обработка ошибок**:
   - Если публикация не удалась, вызывается функция `self.log_promotion_error` для регистрации ошибки.
6. **Обновление данных группы**:
   - Если публикация прошла успешно, вызывается функция `self.update_group_promotion_data` для обновления данных о продвижении группы.

**Примеры**:

```python
from types import SimpleNamespace
from src.webdriver.driver import Driver
from src.webdriver import Firefox
driver = Driver(Firefox)
promoter = FacebookPromoter(d=driver, promoter='test_promoter')

# Пример данных группы
group_data = {
    'group_url': 'https://www.facebook.com/groups/testgroup',
    'language': 'ru',
    'currency': 'USD',
    'promoted_categories': [],
    'promoted_events': []
}
group = SimpleNamespace(**group_data)

# Пример данных категории
category_data = {
    'category_name': 'Test Category',
    'language': SimpleNamespace(ru='Тестовая категория')
}
item = SimpleNamespace(**category_data)

# Продвижение категории
result = promoter.promote(group=group, item=item, is_event=False, language='ru', currency='USD')
print(f"Promotion result: {result}")  # Вывод: Promotion result: True или False
```

### `log_promotion_error`

```python
def log_promotion_error(self, is_event: bool, item_name: str):
    """Записывает в лог ошибку продвижения для категории или события.

    Args:
        is_event (bool): Флаг, указывающий, является ли продвигаемый объект событием.
        item_name (str): Название элемента (категории или события), для которого произошла ошибка.
    """
    ...
```

**Назначение**: Записывает в лог сообщение об ошибке, возникшей при попытке продвижения категории или события.

**Параметры**:
- `is_event` (bool): Флаг, указывающий, является ли продвигаемый элемент событием (`True`) или категорией (`False`).
- `item_name` (str): Название элемента (категории или события), для которого произошла ошибка.

**Как работает функция**:
- Использует модуль `logger` для записи сообщения об ошибке в лог. Сообщение содержит информацию о том, что произошла ошибка при публикации события или категории, а также название элемента, вызвавшего ошибку.

**Примеры**:

```python
from src.webdriver.driver import Driver
from src.webdriver import Firefox
driver = Driver(Firefox)
promoter = FacebookPromoter(d=driver, promoter='test_promoter')
promoter.log_promotion_error(is_event=True, item_name='Test Event')
```

### `update_group_promotion_data`

```python
def update_group_promotion_data(self, group: SimpleNamespace, item_name: str, is_event: bool = False):
    """Обновляет данные о продвижении группы, добавляя информацию о новой публикации.

    Args:
        group (SimpleNamespace): Объект, содержащий данные о группе Facebook.
        item_name (str): Название продвигаемого элемента (категории или события).
        is_event (bool, optional): Флаг, указывающий, является ли продвигаемый элемент событием. Defaults to False.
    """
    ...
```

**Назначение**: Обновляет данные о продвижении группы, добавляя информацию о новой публикации (категории или события).

**Параметры**:
- `group` (SimpleNamespace): Объект, содержащий данные о группе Facebook, включая информацию о последних отправленных промоакциях, категориях и событиях.
- `item_name` (str): Название продвигаемого элемента (категории или события).
- `is_event` (bool, optional): Флаг, указывающий, является ли продвигаемый элемент событием. По умолчанию `False`.

**Как работает функция**:
1. **Получение текущей временной метки**:
   - Получает текущую дату и время и форматирует их в строку.
2. **Обновление времени последней отправки промоакции**:
   - Обновляет атрибут `last_promo_sended` группы текущей временной меткой.
3. **Обновление списка продвигаемых событий или категорий**:
   - Если `is_event` равно `True`, добавляет название события в список `promoted_events`.
   - Если `is_event` равно `False`, добавляет название категории в список `promoted_categories`.
4. **Преобразование в список, если это необходимо**:
   - Преобразует `group.promoted_events` или `group.promoted_categories` в список, если они не являются списками.

**Примеры**:

```python
from types import SimpleNamespace
from src.webdriver.driver import Driver
from src.webdriver import Firefox
driver = Driver(Firefox)
promoter = FacebookPromoter(d=driver, promoter='test_promoter')

# Пример данных группы
group_data = {
    'group_url': 'https://www.facebook.com/groups/testgroup',
    'language': 'ru',
    'currency': 'USD',
    'promoted_categories': [],
    'promoted_events': []
}
group = SimpleNamespace(**group_data)

# Обновление данных группы после продвижения категории
promoter.update_group_promotion_data(group=group, item_name='Test Category', is_event=False)
print(f"Promoted categories: {group.promoted_categories}")  # Вывод: Promoted categories: ['Test Category']

# Обновление данных группы после продвижения события
promoter.update_group_promotion_data(group=group, item_name='Test Event', is_event=True)
print(f"Promoted events: {group.promoted_events}")  # Вывод: Promoted events: ['Test Event']
```

### `process_groups`

```python
def process_groups(self, campaign_name: str = None, events: list[SimpleNamespace] = None, is_event: bool = False, group_file_paths: list[str] = None, group_categories_to_adv: list[str] = ['sales'], language: str = None, currency: str = None):
    """Обрабатывает все группы для текущей кампании или продвижения события.

    Args:
        campaign_name (str, optional): Название кампании. Defaults to None.
        events (list[SimpleNamespace], optional): Список событий для продвижения. Defaults to None.
        is_event (bool, optional): Флаг, указывающий, является ли продвигаемый объект событием. Defaults to False.
        group_file_paths (list[str], optional): Список путей к файлам групп. Defaults to None.
        group_categories_to_adv (list[str], optional): Список категорий групп для продвижения. Defaults to ['sales'].
        language (str, optional): Язык продвижения. Defaults to None.
        currency (str, optional): Валюта продвижения. Defaults to None.
    """
    ...
```

**Назначение**: Обрабатывает все группы Facebook для продвижения текущей кампании или события.

**Параметры**:
- `campaign_name` (str, optional): Название кампании, которую нужно продвигать. Если указано, функция будет продвигать категории, связанные с этой кампанией. По умолчанию `None`.
- `events` (list[SimpleNamespace], optional): Список событий для продвижения. Используется, когда `is_event` равно `True`. По умолчанию `None`.
- `is_event` (bool, optional): Флаг, указывающий, нужно ли продвигать события (`True`) или категории (`False`). По умолчанию `False`.
- `group_file_paths` (list[str], optional): Список путей к файлам, содержащим информацию о группах Facebook. Если не указан, используются пути по умолчанию. По умолчанию `None`.
- `group_categories_to_adv` (list[str], optional): Список категорий групп, в которых нужно продвигать контент. По умолчанию `['sales']`.
- `language` (str, optional): Язык, на котором должно выполняться продвижение. Используется для фильтрации групп по языку. По умолчанию `None`.
- `currency` (str, optional): Валюта, в которой должно выполняться продвижение. Используется для фильтрации групп по валюте. По умолчанию `None`.

**Как работает функция**:
1. **Проверка наличия контента для продвижения**:
   - Проверяет, указаны ли `campaign_name` или `events`. Если оба параметра отсутствуют, функция завершает работу.
2. **Перебор файлов групп**:
   - Перебирает файлы, указанные в `group_file_paths`.
3. **Загрузка данных группы из файла**:
   - Загружает данные о группах из каждого файла, используя функцию `j_loads_ns`.
4. **Перебор групп в файле**:
   - Перебирает группы, информация о которых содержится в файле.
5. **Проверка интервала**:
   - Если продвигается категория (`is_event` is `False`), проверяет, прошло ли достаточно времени с момента последнего продвижения в этой группе, используя функцию `self.check_interval`. Если интервал не прошел, группа пропускается.
6. **Проверка категорий и статуса группы**:
   - Проверяет, пересекаются ли категории группы с категориями, указанными в `group_categories_to_adv`, и активен ли статус группы. Если нет, группа пропускается.
7. **Получение элемента для продвижения**:
   - Если продвигается категория, вызывается функция `self.get_category_item` для получения элемента категории.
   - Если продвигается событие, выбирается случайное событие из списка `events`.
8. **Проверка, было ли уже продвинуто**:
   - Проверяет, был ли уже продвинут выбранный элемент (категория или событие) в этой группе. Если да, группа пропускается.
9. **Фильтрация по языку и валюте**:
   - Если указаны `language` и `currency`, проверяет, соответствуют ли они языку и валюте группы. Если нет, группа пропускается.
10. **Получение URL группы или события**:
    - Получает URL для продвижения, используя либо URL группы, либо URL события, созданного на основе группы.
11. **Продвижение в группе**:
    - Вызывает функцию `self.promote` для продвижения элемента в группе.
12. **Сохранение данных группы**:
    - Сохраняет обновленные данные о группах в файл.
13. **Задержка**:
    - Делает случайную задержку перед переходом к следующей группе.

**Примеры**:

```python
from types import SimpleNamespace
from src.webdriver.driver import Driver
from src.webdriver import Firefox
driver = Driver(Firefox)
promoter = FacebookPromoter(d=driver, promoter='test_promoter')

# Пример данных события
event_data = {
    'event_name': 'Test Event',
    'language': SimpleNamespace(ru='Тестовое событие')
}
events = [SimpleNamespace(**event_data)]

# Пример списка файлов групп
group_file_paths = ['groups1.json', 'groups2.json']

# Продвижение событий
promoter.process_groups(events=events, is_event=True, group_file_paths=group_file_paths, language='ru', currency='USD')
```

### `get_category_item`

```python
def get_category_item(self, campaign_name: str, group: SimpleNamespace, language: str, currency: str) -> SimpleNamespace:
    """Получает элемент категории для продвижения на основе кампании и промоутера.

    Args:
        campaign_name (str): Название кампании.
        group (SimpleNamespace): Данные о группе Facebook.
        language (str): Язык продвижения.
        currency (str): Валюта продвижения.

    Returns:
        SimpleNamespace: Элемент категории для продвижения.
    """
    ...
```

**Назначение**: Получает элемент категории для продвижения на основе кампании и промоутера.

**Параметры**:
- `campaign_name` (str): Название кампании, из которой выбирается категория.
- `group` (SimpleNamespace): Объект, содержащий данные о группе Facebook, включая язык и валюту.
- `language` (str): Язык, на котором должно выполняться продвижение.
- `currency` (str): Валюта, в которой должно выполняться продвижение.

**Как работает функция**:
1. **Определение промоутера**:
   - Проверяет значение атрибута `self.promoter`, чтобы определить, от имени какого поставщика выполняется продвижение.
2. **Обработка AliExpress**:
   - Если `self.promoter` равно `'aliexpress'`:
     - Импортирует класс `AliCampaignEditor` из модуля `src.suppliers.suppliers_list.aliexpress.campaign`.
     - Создает экземпляр класса `AliCampaignEditor` с указанием названия кампании, языка и валюты группы.
     - Получает список категорий из кампании с помощью `ce.list_categories`.
     - Случайным образом перемешивает список категорий.
     - Выбирает первую категорию из перемешанного списка.
     - Получает информацию о выбранной категории с помощью `ce.get_category(category_name)`.
     - Получает список продуктов для выбранной категории с помощью `ce.get_category_products(item.category_name)`.
3. **Обработка других промоутеров**:
   - Если `self.promoter` не равно `'aliexpress'`:
     - Формирует путь к файлу с данными о категориях на основе имени промоутера, названия кампании, языка и валюты.
     - Загружает данные из JSON-файла с помощью `j_loads_ns`.
     - Преобразует категории из объекта в список пар "имя-значение".
     - Перемешивает список категорий случайным образом.
     - Для каждой категории считывает описание из файла `description.txt`.
     - Формирует путь к изображениям категории и получает список файлов изображений.
     - Если изображения найдены, выбирает первое изображение.
4. **Возврат элемента категории**:
   - Возвращает объект `item`, содержащий информацию о выбранной категории и ее продуктах (или описание и изображение для других промоутеров).

**Примеры**:

```python
from types import SimpleNamespace
from src.webdriver.driver import Driver
from src.webdriver import Firefox
driver = Driver(Firefox)
promoter = FacebookPromoter(d=driver, promoter='aliexpress')

# Пример данных группы
group_data = {
    'group_url': 'https://www.facebook.com/groups/testgroup',
    'language': 'ru',
    'currency': 'USD',
    'promoted_categories': [],
    'promoted_events': []
}
group = SimpleNamespace(**group_data)

# Получение элемента категории
category_item = promoter.get_category_item(campaign_name='test_campaign', group=group, language='ru', currency='USD')
print(f"Category item: {category_item}")
```

### `check_interval`

```python
def check_interval(self, group: SimpleNamespace) -> bool:
    """Проверяет, прошло ли достаточно времени для продвижения этой группы.

    Args:
        group (SimpleNamespace): Данные о группе Facebook.

    Returns:
        bool: True, если достаточно времени прошло, False в противном случае.
    """
    ...
```

**Назначение**: Проверяет, прошло ли достаточно времени с момента последней публикации в группе, чтобы выполнить новую публикацию.

**Параметры**:
- `group` (SimpleNamespace): Объект, содержащий данные о группе Facebook, включая информацию о времени последней публикации.

**Как работает функция**:
- Функция всегда возвращает `True`, подразумевая, что проверка интервала времени не реализована или всегда разрешена.

**Примеры**:

```python
from types import SimpleNamespace
from src.webdriver.driver import Driver
from src.webdriver import Firefox
driver = Driver(Firefox)
promoter = FacebookPromoter(d=driver, promoter='test_promoter')

# Пример данных группы
group_data = {
    'group_url': 'https://www.facebook.com/groups/testgroup',
    'language': 'ru',
    'currency': 'USD',
    'last_promo_sended': '20/07/2024 10:00'
}
group = SimpleNamespace(**group_data)

# Проверка интервала
is_allowed = promoter.check_interval(group=group)
print(f"Is promotion allowed: {is_allowed}")  # Вывод: Is promotion allowed: True
```

### `validate_group`

```python
def validate_group(self, group: SimpleNamespace) -> bool:
    """Проверяет, корректны ли данные группы.

    Args:
        group (SimpleNamespace): Данные о группе Facebook.

    Returns:
        bool: True, если данные корректны, False в противном случае.
    """
    ...
```

**Назначение**: Проверяет, содержит ли объект группы необходимые атрибуты `group_url` и `group_categories`.

**Параметры**:
- `group` (SimpleNamespace): Объект, содержащий данные о группе Facebook.

**Как работает функция**:
- Проверяет, что объект `group` не равен `None` и содержит атрибуты `group_url` и `group_categories`. Если все условия выполняются, возвращает `True`, иначе возвращает `False`.

**Примеры**:

```python
from types import SimpleNamespace
from src.webdriver.driver import Driver
from src.webdriver import Firefox
driver = Driver(Firefox)
promoter = FacebookPromoter(d=driver, promoter='test_promoter')

# Пример корректных данных группы
group_data = {
    'group_url': 'https://www.facebook.com/groups/testgroup',
    'group_categories': ['sales', 'marketing']
}
group = SimpleNamespace(**group_data)

# Проверка данных группы
is_valid = promoter.validate_group(group=group)
print(f"Is group data valid: {is_valid}")  # Вывод: Is group data valid: True

# Пример некорректных данных группы (отсутствует group_url)
group_data_invalid = {
    'group_categories': ['sales', 'marketing']
}
group_invalid = SimpleNamespace(**group_data_invalid)

# Проверка данных группы
is_valid = promoter.validate_group(group=group_invalid)
print(f"Is group data valid: {is_valid}")  # Вывод: Is group data valid: False
```

## Функции

### `get_event_url`

```python
def get_event_url(group_url: str) -> str:
    """Возвращает измененный URL для создания события в Facebook, заменяя `group_id` значением из входного URL.

    Args:
        group_url (str): URL группы Facebook, содержащий `group_id`.

    Returns:
        str: Измененный URL для создания события.
    """
    ...
```

**Назначение**: Формирует URL для создания события в группе Facebook на основе URL группы.

**Параметры**:
- `group_url` (str): URL группы Facebook, из которого извлекается идентификатор группы.

**Как работает функция**:
1. **Извлечение идентификатора группы**:
   - Извлекает идентификатор группы из URL группы, разделяя URL по символу `/` и беря последний элемент.
2. **Формирование базового URL**:
   - Определяет базовый URL для создания события в Facebook.
3. **Формирование параметров запроса**:
   - Создает словарь с параметрами запроса, включая идентификатор группы и контекст действия.
4. **Кодирование параметров в строку запроса**:
   - Кодирует параметры запроса в строку, используя функцию `urlencode`.
5. **Объединение базового URL и строки запроса**:
   - Объединяет базовый URL и строку запроса для получения полного URL для создания события.

**Примеры**:

```python
group_url = "https://www.facebook.com/groups/1234567890"
event_url = get_event_url(group_url)
print(event_url)
# Вывод: https://www.facebook.com/events/create/?acontext=%7B%22event_action_history%22%3A%5B%7B%22surface%22%3A%22group%22%7D%2C%7B%22mechanism%22%3A%22upcoming_events_for_group%22%2C%22surface%22%3A%22group%22%7D%5D%2C%22ref_notif_type%22%3Anull%7D&dialog_entry_point=group_events_tab&group_id=1234567890