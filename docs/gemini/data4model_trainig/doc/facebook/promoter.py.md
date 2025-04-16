# Документация модуля Facebook Promoter

## Обзор

Модуль `src.endpoints.advertisement.facebook.promoter` предназначен для автоматизации процесса продвижения товаров и событий в группах Facebook.

## Подробней

Модуль предоставляет класс `FacebookPromoter` для управления продвижением, включая проверку интервалов, получение элементов для продвижения и отправку контента в группы Facebook.

## Классы

### `FacebookPromoter`

**Описание**: Класс для продвижения товаров и событий AliExpress в группах Facebook.

**Атрибуты**:

*   `d` (Driver): Экземпляр веб-драйвера.
*   `group_file_paths` (str | Path): Путь к файлу с данными о группах Facebook.
*   `no_video` (bool): Флаг, указывающий на необходимость отключения видео в рекламных публикациях.
*   `promoter` (str): Имя промоутера (например, 'aliexpress').
*   `spinner` (spinning_cursor): Объект для отображения спиннера в консоли.

**Методы**:

*   `__init__(self, d: Driver, promoter: str, group_file_paths: Optional[list[str | Path] | str | Path] = None, no_video: bool = False)`: Инициализирует промоутер для Facebook групп.
*   `promote(self, group: SimpleNamespace, item: SimpleNamespace, is_event: bool = False, language: str = None, currency: str = None) -> bool`: Продвигает категорию или событие в группе Facebook.
*   `log_promotion_error(self, is_event: bool, item_name: str)`: Логирует ошибку при неудачном продвижении категории или события.
*   `update_group_promotion_data(self, group: SimpleNamespace, item_name: str, is_event: bool = False)`: Обновляет данные группы после успешной публикации, добавляя информацию о продвигаемом элементе.
*   `process_groups(self, campaign_name: str = None, events: list[SimpleNamespace] = None, is_event: bool = False, group_file_paths: list[str] = None, group_categories_to_adv: list[str] = ['sales'], language: str = None, currency: str = None)`: Обрабатывает группы для текущей кампании или события.
*   `get_category_item(self, campaign_name: str, group: SimpleNamespace, language: str, currency: str) -> SimpleNamespace`: Извлекает элемент категории для продвижения на основе кампании и промоутера.
*   `check_interval(self, group: SimpleNamespace) -> bool`: Проверяет, достаточно ли времени прошло для повторного продвижения в этой группе.
*   `validate_group(self, group: SimpleNamespace) -> bool`: Проверяет, что данные группы корректны.
*   `get_event_url(group_url: str) -> str`: Возвращает URL для создания события в Facebook, заменяя `group_id` на значение из входного URL.

## Функции

### `get_event_url`

```python
def get_event_url(group_url: str) -> str:
```

**Назначение**: Возвращает URL для создания события в Facebook, заменяя `group_id` на значение из входного URL.

**Параметры**:

*   `group_url` (str): URL группы Facebook, содержащий `group_id`.

**Возвращает**:

*   `str`: URL для создания события.

**Как работает функция**:

1.  Извлекает `group_id` из URL группы.
2.  Формирует базовый URL для создания события.
3.  Добавляет параметры запроса, включая `group_id`.
4.  Возвращает URL с параметрами.

## Методы класса `FacebookPromoter`

### `__init__`

```python
def __init__(self, d: Driver, promoter: str, group_file_paths: Optional[list[str | Path] | str | Path] = None, no_video: bool = False):
```

**Назначение**: Инициализирует промоутер для Facebook групп.

**Параметры**:

*   `d` (Driver): Экземпляр веб-драйвера для автоматизации браузера.
*   `promoter` (str): Имя промоутера (например, "aliexpress").
*   `group_file_paths` (Optional[list[str | Path] | str | Path], optional): Список путей к файлам, содержащим данные о группах. По умолчанию `None`.
*   `no_video` (bool, optional): Флаг для отключения видео в постах. По умолчанию `False`.

**Как работает функция**:

1.  Инициализирует атрибуты `promoter`, `d`, `group_file_paths` и `no_video`.
2.  Получает список файлов групп, если `group_file_paths` не указан.

### `promote`

```python
def promote(self, group: SimpleNamespace, item: SimpleNamespace, is_event: bool = False, language: str = None, currency: str = None) -> bool:
```

**Назначение**: Продвигает категорию или событие в группе Facebook.

**Параметры**:

*   `group` (SimpleNamespace): Данные группы.
*   `item` (SimpleNamespace): Элемент категории или события для продвижения.
*   `is_event` (bool, optional): Указывает, является ли элемент событием. По умолчанию `False`.
*   `language` (str, optional): Язык продвижения. По умолчанию `None`.
*   `currency` (str, optional): Валюта для продвижения. По умолчанию `None`.

**Возвращает**:

*   `bool`: `True`, если продвижение выполнено успешно, `False` в противном случае.

**Как работает функция**:

1.  Проверяет соответствие языка и валюты группы заданным значениям `language` и `currency`.
2.  Вызывает функцию `post_event` или `post_message` в зависимости от типа продвигаемого элемента (событие или категория).
3.  Обновляет данные группы после успешной публикации.

### `log_promotion_error`

```python
def log_promotion_error(self, is_event: bool, item_name: str):
```

**Назначение**: Логирует ошибку при неудачном продвижении категории или события.

**Параметры**:

*   `is_event` (bool): Указывает, является ли элементом событие.
*   `item_name` (str): Название элемента.

**Как работает функция**:

1.  Логирует сообщение об ошибке с использованием `logger.debug`.

### `update_group_promotion_data`

```python
def update_group_promotion_data(self, group: SimpleNamespace, item_name: str, is_event: bool = False):
```

**Назначение**: Обновляет данные группы после успешной публикации, добавляя информацию о продвигаемом элементе.

**Параметры**:

*   `group` (SimpleNamespace): Данные группы.
*   `item_name` (str): Название элемента, который был продвинут.
*   `is_event` (bool, optional): Указывает, является ли элементом событие. По умолчанию `False`.

**Как работает функция**:

1.  Обновляет атрибуты `last_promo_sended`, `promoted_events` или `promoted_categories` в данных группы.

### `process_groups`

```python
def process_groups(self, campaign_name: str = None, events: list[SimpleNamespace] = None, is_event: bool = False, group_file_paths: list[str] = None, group_categories_to_adv: list[str] = ['sales'], language: str = None, currency: str = None):
```

**Назначение**: Обрабатывает группы для текущей рекламной кампании или продвижения события.

**Параметры**:

*   `campaign_name` (str, optional): Название кампании. По умолчанию `None`.
*   `events` (list[SimpleNamespace], optional): Список событий для продвижения. По умолчанию `None`.
*   `is_event` (bool, optional): Указывает, следует ли продвигать события или категории. По умолчанию `False`.
*   `group_file_paths` (list[str], optional): Список путей к файлам с данными о группах. По умолчанию `None`.
*   `group_categories_to_adv` (list[str], optional): Список категорий для продвижения. По умолчанию `['sales']`.
*   `language` (str, optional): Язык продвижения. По умолчанию `None`.
*   `currency` (str, optional): Валюта для продвижения. По умолчанию `None`.

**Как работает функция**:

1.  Итерируется по файлам групп.
2.  Загружает данные о группах из JSON-файла.
3.  Итерируется по группам.
4.  Проверяет условия для продвижения (интервал, категории, статус).
5.  Вызывает метод `promote` для продвижения элемента.
6.  Сохраняет обновленные данные о группах в JSON-файл.

### `get_category_item`

```python
def get_category_item(self, campaign_name: str, group: SimpleNamespace, language: str, currency: str) -> SimpleNamespace:
```

**Назначение**: Извлекает элемент категории для продвижения на основе кампании и промоутера.

**Параметры**:

*   `campaign_name` (str): Название кампании.
*   `group` (SimpleNamespace): Данные группы.
*   `language` (str): Язык для продвижения.
*   `currency` (str): Валюта для продвижения.

**Возвращает**:

*   `SimpleNamespace`: Элемент категории для продвижения.

**Как работает функция**:

1.  Извлекает элемент категории в зависимости от значения атрибута `promoter` ('aliexpress' или другой).
2.  Возвращает извлеченный элемент.

### `check_interval`

```python
def check_interval(self, group: SimpleNamespace) -> bool:
```

**Назначение**: Проверяет, достаточно ли времени прошло для повторного продвижения в этой группе.

**Параметры**:

*   `group` (SimpleNamespace): Данные группы.

**Возвращает**:

*   `bool`: `True`, если достаточно времени прошло, `False` в противном случае.

**Как работает функция**:

1.  В коде присутствует только заглушка `...`, а также безусловный возврат значения `True`. Реальная реализация должна проверять временной интервал с момента последней публикации.

### `validate_group`

```python
def validate_group(self, group: SimpleNamespace) -> bool:
```

**Назначение**: Проверяет, что данные группы корректны.

**Параметры**:

*   `group` (SimpleNamespace): Данные группы.

**Возвращает**:

*   `bool`: `True`, если данные группы корректны, `False` в противном случае.

**Как работает функция**:

1.  Проверяет, что `group` не `None` и содержит атрибуты `group_url` и `group_categories`.
2.  Возвращает `True`, если все условия выполнены, `False` в противном случае.