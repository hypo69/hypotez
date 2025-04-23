# Модуль: src.endpoints.advertisement.facebook.promoter

## Обзор

Модуль `promoter.py` предназначен для управления продвижением сообщений и событий в группах Facebook. Он обрабатывает кампании и события, публикуя их в группах Facebook и избегая дублирования публикаций.

## Более подробно

Модуль автоматизирует размещение рекламных материалов в группах Facebook с использованием экземпляра WebDriver, обеспечивая продвижение категорий и событий с учетом избежания дубликатов. В модуле используются различные сценарии для публикации сообщений, событий, загрузки медиа и т.д.

## Классы

### `FacebookPromoter`

**Описание**: Класс для продвижения товаров и событий AliExpress в группах Facebook.

**Описание наследования**:
- Класс не наследуется от других классов.

**Атрибуты**:
- `d` (Driver): Экземпляр WebDriver для автоматизации браузера.
- `group_file_paths` (str | Path): Пути к файлам, содержащим данные о группах.
- `no_video` (bool): Флаг для отключения видео в публикациях.
- `promoter` (str): Имя промоутера.

**Принцип работы**:

Класс `FacebookPromoter` предназначен для автоматизации процесса продвижения товаров и событий в группах Facebook. Он инициализируется с использованием драйвера WebDriver, путей к файлам с данными о группах и флага, указывающего на необходимость отключения видео в публикациях. Основной метод `promote` отвечает за фактическую публикацию контента в группах, а вспомогательные методы используются для логирования ошибок, обновления данных о продвижении и проверки интервалов между публикациями. Класс также содержит методы для получения элементов категорий и проверки данных о группах.

**Методы**:
- `__init__`: Инициализирует промоутер для групп Facebook.
- `promote`: Продвигает категорию или событие в группе Facebook.
- `log_promotion_error`: Логирует ошибки продвижения для категории или события.
- `update_group_promotion_data`: Обновляет данные о продвижении группы с учетом новой публикации.
- `process_groups`: Обрабатывает все группы для текущей кампании или продвижения события.
- `get_category_item`: Получает элемент категории для продвижения на основе кампании и промоутера.
- `check_interval`: Проверяет, достаточно ли времени прошло для продвижения этой группы.
- `validate_group`: Проверяет корректность данных группы.

## Методы класса

### `__init__`

```python
def __init__(self, d: Driver, promoter: str, group_file_paths: Optional[list[str | Path] | str | Path] = None, no_video: bool = False):
    """
    Инициализирует промоутер для Facebook групп.

    Args:
        d (Driver): Экземпляр WebDriver для автоматизации браузера.
        promoter (str): Имя промоутера.
        group_file_paths (list[str | Path] | str | Path, optional): Список путей к файлам, содержащим данные о группах. Defaults to None.
        no_video (bool, optional): Флаг для отключения видео в постах. Defaults to False.
    """
```

### `promote`

```python
def promote(self, group: SimpleNamespace, item: SimpleNamespace, is_event: bool = False, language: str = None, currency: str = None) -> bool:
    """
    Продвигает категорию или событие в группе Facebook.

    Args:
        group (SimpleNamespace): Объект, содержащий данные о группе Facebook.
        item (SimpleNamespace): Объект, содержащий данные о категории или событии для продвижения.
        is_event (bool, optional): Флаг, указывающий, является ли продвигаемый элемент событием. Defaults to False.
        language (str, optional): Язык, на котором нужно продвигать. Defaults to None.
        currency (str, optional): Валюта, в которой нужно продвигать. Defaults to None.

    Returns:
        bool: True, если продвижение прошло успешно, иначе False.
    """
```

### `log_promotion_error`

```python
def log_promotion_error(self, is_event: bool, item_name: str):
    """
    Логирует ошибку продвижения для категории или события.

    Args:
        is_event (bool): Флаг, указывающий, является ли продвигаемый элемент событием.
        item_name (str): Название категории или события.
    """
```

### `update_group_promotion_data`

```python
def update_group_promotion_data(self, group: SimpleNamespace, item_name: str, is_event: bool = False):
    """
    Обновляет данные о продвижении группы с учетом новой публикации.

    Args:
        group (SimpleNamespace): Объект, содержащий данные о группе Facebook.
        item_name (str): Название категории или события.
        is_event (bool, optional): Флаг, указывающий, является ли продвигаемый элемент событием. Defaults to False.
    """
```

### `process_groups`

```python
def process_groups(self, campaign_name: str = None, events: list[SimpleNamespace] = None, is_event: bool = False, group_file_paths: list[str] = None, group_categories_to_adv: list[str] = ['sales'], language: str = None, currency: str = None):
    """
    Обрабатывает все группы для текущей кампании или продвижения события.

    Args:
        campaign_name (str, optional): Название кампании. Defaults to None.
        events (list[SimpleNamespace], optional): Список объектов, содержащих данные о событиях. Defaults to None.
        is_event (bool, optional): Флаг, указывающий, является ли продвигаемый элемент событием. Defaults to False.
        group_file_paths (list[str], optional): Список путей к файлам с данными о группах. Defaults to None.
        group_categories_to_adv (list[str], optional): Список категорий групп для продвижения. Defaults to ['sales'].
        language (str, optional): Язык, на котором нужно продвигать. Defaults to None.
        currency (str, optional): Валюта, в которой нужно продвигать. Defaults to None.
    """
```

### `get_category_item`

```python
def get_category_item(self, campaign_name: str, group: SimpleNamespace, language: str, currency: str) -> SimpleNamespace:
    """
    Получает элемент категории для продвижения на основе кампании и промоутера.

    Args:
        campaign_name (str): Название кампании.
        group (SimpleNamespace): Объект, содержащий данные о группе Facebook.
        language (str): Язык, на котором нужно продвигать.
        currency (str): Валюта, в которой нужно продвигать.

    Returns:
        SimpleNamespace: Объект, содержащий данные о категории для продвижения.
    """
```

### `check_interval`

```python
def check_interval(self, group: SimpleNamespace) -> bool:
    """
    Проверяет, достаточно ли времени прошло для продвижения этой группы.

    Args:
        group (SimpleNamespace): Объект, содержащий данные о группе Facebook.

    Returns:
        bool: True, если достаточно времени прошло, иначе False.
    """
```

### `validate_group`

```python
def validate_group(self, group: SimpleNamespace) -> bool:
    """
    Проверяет корректность данных группы.

    Args:
        group (SimpleNamespace): Объект, содержащий данные о группе Facebook.

    Returns:
        bool: True, если данные группы корректны, иначе False.
    """
```

## Функции

### `get_event_url`

```python
def get_event_url(group_url: str) -> str:
    """
    Возвращает измененный URL для создания события на Facebook, заменяя `group_id` значением из входного URL.

    Args:
        group_url (str): URL группы Facebook, содержащий `group_id`.

    Returns:
        str: Измененный URL для создания события.
    """
```
```
## Class Parameters
- `param` (str): More detailed Description of the `param` parameter.
- `param1` (Optional[str | dict | str], optional): More detailed Description of the `param1` parameter. Defaults to `None`.
```
```python

## Class Parameters
- `param` (str): More detailed Description of the `param` parameter.
- `param1` (Optional[str | dict | str], optional): More detailed Description of the `param1` parameter. Defaults to `None`.