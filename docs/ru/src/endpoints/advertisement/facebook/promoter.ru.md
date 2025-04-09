# Модуль Facebook Promoter

## Обзор

Модуль **Facebook Promoter** предназначен для автоматизации процесса продвижения товаров и мероприятий AliExpress в группах Facebook. Он управляет публикацией рекламных материалов, избегая дублирования контента, и использует WebDriver для автоматизации действий в браузере.

## Подробнее

Этот модуль автоматизирует продвижение категорий товаров и мероприятий в группах Facebook. Он отслеживает уже опубликованные элементы, чтобы избежать дублирования публикаций, и поддерживает конфигурацию данных групп через файлы. Также предусмотрена возможность отключения загрузки видео в публикациях.

## Классы

### `FacebookPromoter`

**Описание**: Класс `FacebookPromoter` управляет процессом продвижения товаров и мероприятий AliExpress в группах Facebook.

**Принцип работы**: Класс инициализируется с WebDriver, именем промоутера и путями к файлам с данными групп. Он предоставляет методы для продвижения элементов в группах, обновления данных о группах после продвижения, проверки интервалов между продвижениями и проверки корректности данных группы. Класс использует WebDriver для автоматизации действий в браузере и управляет процессом публикации рекламных материалов в группах Facebook.

#### Методы

- `__init__(self, d: Driver, promoter: str, group_file_paths: Optional[list[str | Path] | str | Path] = None, no_video: bool = False)`: Инициализирует промоутер для Facebook с необходимыми конфигурациями.
- `promote(self, group: SimpleNamespace, item: SimpleNamespace, is_event: bool = False, language: str = None, currency: str = None) -> bool`: Продвигает категорию или мероприятие в указанной группе Facebook.
- `log_promotion_error(self, is_event: bool, item_name: str)`: Записывает ошибку, если продвижение не удалось.
- `update_group_promotion_data(self, group: SimpleNamespace, item_name: str, is_event: bool = False)`: Обновляет данные группы после продвижения, добавляя продвигаемый элемент в список продвигаемых категорий или мероприятий.
- `process_groups(self, campaign_name: str = None, events: list[SimpleNamespace] = None, is_event: bool = False, group_file_paths: list[str] = None, group_categories_to_adv: list[str] = ['sales'], language: str = None, currency: str = None)`: Обрабатывает группы для текущей кампании или продвижения мероприятия.
- `get_category_item(self, campaign_name: str, group: SimpleNamespace, language: str, currency: str) -> SimpleNamespace`: Получает элемент категории для продвижения в зависимости от кампании и промоутера.
- `check_interval(self, group: SimpleNamespace) -> bool`: Проверяет, прошло ли достаточно времени, чтобы снова продвигать эту группу.
- `validate_group(self, group: SimpleNamespace) -> bool`: Проверяет данные группы, чтобы убедиться в их корректности.

## Функции

### `__init__`

```python
def __init__(self, d: Driver, promoter: str, group_file_paths: Optional[list[str | Path] | str | Path] = None, no_video: bool = False):
    """
    Инициализирует промоутер для Facebook с необходимыми конфигурациями.

    Args:
        d (Driver): Экземпляр WebDriver для автоматизации.
        promoter (str): Имя промоутера (например, "aliexpress").
        group_file_paths (Optional[list[str  |  Path] | str | Path], optional): Пути к файлам с данными групп. По умолчанию `None`.
        no_video (bool): Флаг для отключения видео в публикациях. По умолчанию `False`.
    """
```

**Назначение**: Инициализация экземпляра класса `FacebookPromoter`.

**Параметры**:
- `d` (Driver): Экземпляр WebDriver для управления браузером.
- `promoter` (str): Имя промоутера, например, "aliexpress".
- `group_file_paths` (Optional[list[str | Path] | str | Path], optional): Путь к файлу или список путей к файлам, содержащим данные о группах Facebook. По умолчанию `None`.
- `no_video` (bool): Флаг, указывающий, нужно ли отключать загрузку видео в публикациях. По умолчанию `False`.

**Как работает функция**:

1. Инициализирует экземпляр класса `FacebookPromoter` с переданными параметрами.
2. Сохраняет переданные параметры в атрибуты экземпляра класса.
3. Если `group_file_paths` не указан, он остается `None`.

**Примеры**:

```python
from src.webdriver.driver import Driver
from pathlib import Path

# Пример с указанием одного пути к файлу
d = Driver()
promoter = FacebookPromoter(d=d, promoter="aliexpress", group_file_paths="path/to/group.json")

# Пример с указанием списка путей к файлам
d = Driver()
promoter = FacebookPromoter(d=d, promoter="aliexpress", group_file_paths=["path/to/group1.json", "path/to/group2.json"])

# Пример с отключением загрузки видео
d = Driver()
promoter = FacebookPromoter(d=d, promoter="aliexpress", group_file_paths="path/to/group.json", no_video=True)

# Пример с использованием pathlib.Path
d = Driver()
group_path = Path("path/to/group.json")
promoter = FacebookPromoter(d=d, promoter="aliexpress", group_file_paths=group_path)
```

### `promote`

```python
def promote(self, group: SimpleNamespace, item: SimpleNamespace, is_event: bool = False, language: str = None, currency: str = None) -> bool:
    """
    Продвигает категорию или мероприятие в указанной группе Facebook.

    Args:
        group (SimpleNamespace): Данные группы.
        item (SimpleNamespace): Категория или мероприятие для продвижения.
        is_event (bool): Является ли элемент мероприятием.
        language (str): Язык публикации.
        currency (str): Валюта для продвижения.

    Returns:
        bool: Успешно ли прошло продвижение.
    """
```

**Назначение**: Осуществляет продвижение категории или мероприятия в указанной группе Facebook.

**Параметры**:
- `group` (SimpleNamespace): Данные группы Facebook, в которой будет осуществляться продвижение.
- `item` (SimpleNamespace): Информация о категории или мероприятии, которое нужно продвигать.
- `is_event` (bool, optional): Флаг, указывающий, является ли продвигаемый элемент мероприятием. По умолчанию `False`.
- `language` (str, optional): Язык публикации. По умолчанию `None`.
- `currency` (str, optional): Валюта для продвижения. По умолчанию `None`.

**Возвращает**:
- `bool`: Возвращает `True`, если продвижение прошло успешно, и `False` в противном случае.

**Как работает функция**:

1. Принимает данные группы, информацию о продвигаемом элементе (категории или мероприятии) и флаг, указывающий, является ли элемент мероприятием.
2. Выполняет необходимые действия для продвижения элемента в группе Facebook с использованием предоставленных данных и WebDriver.
3. Возвращает `True`, если продвижение прошло успешно, и `False`, если произошла ошибка.

**Примеры**:

```python
from types import SimpleNamespace
from src.webdriver.driver import Driver

# Предположим, что у вас уже есть экземпляр класса FacebookPromoter и WebDriver
d = Driver()
promoter = FacebookPromoter(d=d, promoter="aliexpress")

# Создаем фиктивные данные группы и элемента для примера
group_data = SimpleNamespace(id="123456789", name="Test Group", last_promotion_time=None, promoted_categories=[])
item_data = SimpleNamespace(name="Test Item", url="https://example.com")

# Пример продвижения категории
success = promoter.promote(group=group_data, item=item_data, is_event=False, language="en", currency="USD")
print(f"Promotion successful: {success}")

# Пример продвижения мероприятия
event_data = SimpleNamespace(name="Test Event", url="https://example.com/event")
success = promoter.promote(group=group_data, item=event_data, is_event=True, language="en", currency="USD")
print(f"Event promotion successful: {success}")
```

### `log_promotion_error`

```python
def log_promotion_error(self, is_event: bool, item_name: str):
    """
    Записывает ошибку, если продвижение не удалось.

    Args:
        is_event (bool): Является ли элемент мероприятием.
        item_name (str): Название элемента.
    """
```

**Назначение**: Записывает информацию об ошибке продвижения в журнал.

**Параметры**:
- `is_event` (bool): Указывает, был ли продвигаемый элемент мероприятием (`True`) или категорией (`False`).
- `item_name` (str): Название элемента, который не удалось продвинуть.

**Как работает функция**:

1.  Определяет тип продвигаемого элемента (мероприятие или категория) на основе значения параметра `is_event`.
2.  Формирует сообщение об ошибке, включающее название элемента и его тип.
3.  Записывает сформированное сообщение об ошибке в журнал с использованием модуля `logger`.

**Примеры**:

```python
from src.webdriver.driver import Driver

# Пример использования класса FacebookPromoter
d = Driver()

# Создание экземпляра FacebookPromoter
promoter = FacebookPromoter(d=d, promoter="aliexpress")

# Логирование ошибки продвижения категории
promoter.log_promotion_error(is_event=False, item_name="Category1")

# Логирование ошибки продвижения мероприятия
promoter.log_promotion_error(is_event=True, item_name="Event1")
```

### `update_group_promotion_data`

```python
def update_group_promotion_data(self, group: SimpleNamespace, item_name: str, is_event: bool = False):
    """
    Обновляет данные группы после продвижения, добавляя продвигаемый элемент в список продвигаемых категорий или мероприятий.

    Args:
        group (SimpleNamespace): Данные группы.
        item_name (str): Название продвигаемого элемента.
        is_event (bool): Является ли элемент мероприятием.
    """
```

**Назначение**: Обновляет информацию о группе после успешного продвижения элемента (категории или мероприятия).

**Параметры**:
- `group` (SimpleNamespace): Объект, содержащий данные группы Facebook.
- `item_name` (str): Название продвигаемого элемента (категории или мероприятия).
- `is_event` (bool, optional): Флаг, указывающий, является ли продвигаемый элемент мероприятием. По умолчанию `False`.

**Как работает функция**:

1.  Определяет, является ли продвигаемый элемент мероприятием или категорией, на основе значения параметра `is_event`.
2.  Добавляет название продвигаемого элемента в соответствующий список (`promoted_events` или `promoted_categories`) в данных группы.
3.  Обновляет время последнего продвижения группы.

**Примеры**:

```python
from types import SimpleNamespace
from src.webdriver.driver import Driver

# Создаем экземпляр класса FacebookPromoter и WebDriver
d = Driver()
promoter = FacebookPromoter(d=d, promoter="aliexpress")

# Создаем фиктивные данные группы
group_data = SimpleNamespace(id="123456789", name="Test Group", last_promotion_time=None, promoted_categories=[], promoted_events=[])

# Пример обновления данных группы после продвижения категории
promoter.update_group_promotion_data(group=group_data, item_name="Category1", is_event=False)
print(f"Promoted categories: {group_data.promoted_categories}")

# Пример обновления данных группы после продвижения мероприятия
promoter.update_group_promotion_data(group=group_data, item_name="Event1", is_event=True)
print(f"Promoted events: {group_data.promoted_events}")
```

### `process_groups`

```python
def process_groups(self, campaign_name: str = None, events: list[SimpleNamespace] = None, is_event: bool = False, group_file_paths: list[str] = None, group_categories_to_adv: list[str] = ['sales'], language: str = None, currency: str = None):
    """
    Обрабатывает группы для текущей кампании или продвижения мероприятия.

    Args:
        campaign_name (str): Название кампании.
        events (list[SimpleNamespace]): Список мероприятий для продвижения.
        is_event (bool): Является ли продвижение мероприятий или категорий.
        group_file_paths (list[str]): Пути к файлам с данными групп.
        group_categories_to_adv (list[str]): Категории для продвижения.
        language (str): Язык публикации.
        currency (str): Валюта для продвижения.
    """
```

**Назначение**: Метод `process_groups` предназначен для обработки списка групп и продвижения товаров или мероприятий в этих группах. Он выполняет итерацию по группам, проверяет, можно ли продвигать группу, и, если возможно, продвигает товары или мероприятия в этой группе.

**Параметры**:

- `campaign_name` (str, optional): Название рекламной кампании. По умолчанию `None`.
- `events` (list[SimpleNamespace], optional): Список объектов `SimpleNamespace`, представляющих мероприятия для продвижения. По умолчанию `None`.
- `is_event` (bool, optional): Флаг, указывающий, нужно ли продвигать мероприятия (если `True`) или категории товаров (если `False`). По умолчанию `False`.
- `group_file_paths` (list[str], optional): Список путей к файлам, содержащим данные о группах Facebook. По умолчанию `None`.
- `group_categories_to_adv` (list[str], optional): Список категорий товаров, которые нужно продвигать. По умолчанию `['sales']`.
- `language` (str, optional): Язык, на котором будет публиковаться рекламный контент. По умолчанию `None`.
- `currency` (str, optional): Валюта, в которой будут отображаться цены товаров. По умолчанию `None`.

**Как работает функция**:

1.  Загружает данные о группах из файлов, указанных в `group_file_paths`.
2.  Итерируется по списку групп.
3.  Для каждой группы проверяет, можно ли ее продвигать, используя метод `validate_group`.
4.  Если группа валидна, получает элемент категории для продвижения, используя метод `get_category_item`.
5.  Продвигает категорию или мероприятие в группе, используя метод `promote`.
6.  Обновляет данные о продвижении группы, используя метод `update_group_promotion_data`.
7.  В случае возникновения ошибки логирует ее, используя метод `log_promotion_error`.

**Примеры**:

```python
from types import SimpleNamespace
from src.webdriver.driver import Driver

# Пример использования класса FacebookPromoter
d = Driver()

# Создание экземпляра FacebookPromoter
promoter = FacebookPromoter(d=d, promoter="aliexpress")

# Пример вызова process_groups с минимальными параметрами
promoter.process_groups()

# Пример вызова process_groups с указанием кампании и категорий для продвижения
promoter.process_groups(campaign_name="SummerSale", group_categories_to_adv=["electronics", "clothing"])

# Пример вызова process_groups с указанием списка мероприятий для продвижения
event1 = SimpleNamespace(name="Event1", url="https://example.com/event1")
event2 = SimpleNamespace(name="Event2", url="https://example.com/event2")
promoter.process_groups(events=[event1, event2], is_event=True)

# Пример вызова process_groups с указанием языка и валюты
promoter.process_groups(language="es", currency="EUR")
```

### `get_category_item`

```python
def get_category_item(self, campaign_name: str, group: SimpleNamespace, language: str, currency: str) -> SimpleNamespace:
    """
    Получает элемент категории для продвижения в зависимости от кампании и промоутера.

    Args:
        campaign_name (str): Название кампании.
        group (SimpleNamespace): Данные группы.
        language (str): Язык для публикации.
        currency (str): Валюта для публикации.

    Returns:
        SimpleNamespace: Элемент категории для продвижения.
    """
```

**Назначение**: Получает элемент категории для продвижения в зависимости от кампании, данных группы, языка и валюты.

**Параметры**:
- `campaign_name` (str): Название кампании.
- `group` (SimpleNamespace): Данные группы.
- `language` (str): Язык для публикации.
- `currency` (str): Валюта для публикации.

**Возвращает**:
- `SimpleNamespace`: Элемент категории для продвижения.

**Как работает функция**:

1.  Формирует URL для получения элемента категории, используя название кампании, данные группы, язык и валюту.
2.  Выполняет HTTP-запрос для получения данных элемента категории.
3.  Преобразует полученные данные в объект `SimpleNamespace`.
4.  Возвращает полученный элемент категории.

**Примеры**:

```python
from types import SimpleNamespace
from src.webdriver.driver import Driver

# Создаем экземпляр класса FacebookPromoter
d = Driver()
promoter = FacebookPromoter(d=d, promoter="aliexpress")

# Создаем фиктивные данные группы
group_data = SimpleNamespace(id="123456789", name="Test Group")

# Получаем элемент категории для продвижения
category_item = promoter.get_category_item(campaign_name="SummerSale", group=group_data, language="en", currency="USD")

# Выводим информацию об элементе категории
print(f"Category item name: {category_item.name}")
print(f"Category item URL: {category_item.url}")
```

### `check_interval`

```python
def check_interval(self, group: SimpleNamespace) -> bool:
    """
    Проверяет, прошло ли достаточно времени, чтобы снова продвигать эту группу.

    Args:
        group (SimpleNamespace): Данные группы.

    Returns:
        bool: Можно ли снова продвигать группу.
    """
```

**Назначение**: Проверяет, прошло ли достаточно времени с момента последнего продвижения группы, чтобы можно было снова продвигать ее.

**Параметры**:
- `group` (SimpleNamespace): Объект, содержащий данные о группе, включая время последнего продвижения.

**Возвращает**:
- `bool`: `True`, если прошло достаточно времени с момента последнего продвижения, и `False` в противном случае.

**Как работает функция**:

1.  Получает время последнего продвижения группы из объекта `group`.
2.  Вычисляет разницу между текущим временем и временем последнего продвижения.
3.  Сравнивает вычисленную разницу с заданным интервалом между продвижениями.
4.  Возвращает `True`, если разница больше или равна интервалу, и `False` в противном случае.

**Примеры**:

```python
from types import SimpleNamespace
from datetime import datetime, timedelta
from src.webdriver.driver import Driver

# Создаем экземпляр класса FacebookPromoter
d = Driver()
promoter = FacebookPromoter(d=d, promoter="aliexpress")

# Создаем фиктивные данные группы
group_data = SimpleNamespace(id="123456789", name="Test Group", last_promotion_time=datetime.now() - timedelta(hours=2))

# Проверяем, можно ли снова продвигать группу
can_promote = promoter.check_interval(group=group_data)
print(f"Can promote group: {can_promote}")

# Обновляем время последнего продвижения и снова проверяем
group_data.last_promotion_time = datetime.now() - timedelta(hours=1)
can_promote = promoter.check_interval(group=group_data)
print(f"Can promote group: {can_promote}")
```

### `validate_group`

```python
def validate_group(self, group: SimpleNamespace) -> bool:
    """
    Проверяет данные группы, чтобы убедиться в их корректности.

    Args:
        group (SimpleNamespace): Данные группы.

    Returns:
        bool: Корректны ли данные группы.
    """
```

**Назначение**: Проверяет, являются ли данные группы корректными и пригодными для использования в процессе продвижения.

**Параметры**:
- `group` (SimpleNamespace): Объект, содержащий данные о группе, которые необходимо проверить.

**Возвращает**:
- `bool`: `True`, если данные группы корректны и прошли все проверки, и `False` в противном случае.

**Как работает функция**:

1.  Проверяет наличие необходимых атрибутов в данных группы, таких как `id` и `name`.
2.  Проверяет, что `id` группы является допустимым значением (например, не является пустым).
3.  Выполняет другие проверки, специфичные для данных группы.
4.  Возвращает `True`, если все проверки пройдены успешно, и `False`, если хотя бы одна проверка не пройдена.

**Примеры**:

```python
from types import SimpleNamespace
from src.webdriver.driver import Driver

# Создаем экземпляр класса FacebookPromoter
d = Driver()
promoter = FacebookPromoter(d=d, promoter="aliexpress")

# Создаем фиктивные данные группы
group_data = SimpleNamespace(id="123456789", name="Test Group")

# Проверяем, являются ли данные группы корректными
is_valid = promoter.validate_group(group=group_data)
print(f"Is group data valid: {is_valid}")

# Изменяем данные группы, чтобы они стали некорректными
group_data.id = ""
is_valid = promoter.validate_group(group=group_data)
print(f"Is group data valid: {is_valid}")
```