# Модуль для продвижения в Facebook
## Обзор

Модуль `src.endpoints.advertisement.facebook.promoter` предназначен для автоматизации процесса продвижения сообщений и событий в группах Facebook. Он обрабатывает кампании и события, публикуя их в группах Facebook, избегая дублирования публикаций.

## Подробнее

Модуль содержит класс `FacebookPromoter`, который использует WebDriver для автоматизации действий в браузере и обеспечивает продвижение категорий и событий в группах Facebook. Класс проверяет интервалы между публикациями, чтобы избежать слишком частого размещения контента в одной и той же группе.

## Классы

### `FacebookPromoter`

**Описание**: Класс для продвижения товаров и событий AliExpress в группах Facebook.

**Принцип работы**:
Класс `FacebookPromoter` автоматизирует процесс публикации рекламных материалов в группах Facebook. Он использует WebDriver для управления браузером и выполняет следующие шаги:

1.  Инициализация: При создании экземпляра класса инициализируется WebDriver, определяются пути к файлам с данными о группах, устанавливается флаг для отключения видео (при необходимости).
2.  Обработка групп: Метод `process_groups` перебирает файлы с данными о группах, проверяет интервалы между публикациями и категории групп.
3.  Получение элементов для продвижения: В зависимости от типа промоутера (например, AliExpress) и типа контента (категория или событие) выбирается соответствующий элемент для публикации.
4.  Публикация: Метод `promote` публикует выбранный элемент в группе Facebook.
5.  Обновление данных группы: После успешной публикации обновляются данные о группе, чтобы избежать повторной публикации одного и того же контента.

**Атрибуты**:

*   `d` (Driver): Экземпляр WebDriver для автоматизации браузера.
*   `group_file_paths` (str | Path): Пути к файлам, содержащим данные о группах Facebook.
*   `no_video` (bool): Флаг, указывающий, следует ли отключать видео в публикациях.
*   `promoter` (str): Имя промоутера (например, "aliexpress").
*   `spinner`: Объект для отображения спиннера в консоли во время выполнения операций.

**Методы**:

*   `__init__(self, d: Driver, promoter: str, group_file_paths: Optional[list[str | Path] | str | Path] = None, no_video: bool = False)`: Инициализирует промоутер для групп Facebook.
*   `promote(self, group: SimpleNamespace, item: SimpleNamespace, is_event: bool = False, language: str = None, currency: str = None) -> bool`: Продвигает категорию или событие в группе Facebook.
*   `log_promotion_error(self, is_event: bool, item_name: str)`: Логирует ошибку продвижения для категории или события.
*   `update_group_promotion_data(self, group: SimpleNamespace, item_name: str, is_event: bool = False)`: Обновляет данные группы после успешной публикации.
*   `process_groups(self, campaign_name: str = None, events: list[SimpleNamespace] = None, is_event: bool = False, group_file_paths: list[str] = None, group_categories_to_adv: list[str] = ['sales'], language: str = None, currency: str = None)`: Обрабатывает все группы для текущей кампании или продвижения события.
*   `get_category_item(self, campaign_name: str, group: SimpleNamespace, language: str, currency: str) -> SimpleNamespace`: Получает элемент категории для продвижения на основе кампании и промоутера.
*   `check_interval(self, group: SimpleNamespace) -> bool`: Проверяет, достаточно ли времени прошло для продвижения этой группы.
*   `validate_group(self, group: SimpleNamespace) -> bool`: Проверяет, что данные группы корректны.

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

**Назначение**: Функция `get_event_url` создает URL-адрес для создания события в Facebook группе, заменяя `group_id` в базовом URL на значение, извлеченное из URL-адреса группы.

**Параметры**:

*   `group_url` (str): URL-адрес Facebook группы, содержащий `group_id`.

**Возвращает**:

*   `str`: Модифицированный URL-адрес для создания события.

**Как работает функция**:

1.  **Извлечение `group_id`**: Извлекает идентификатор группы из предоставленного URL-адреса группы Facebook.
2.  **Формирование базового URL**: Определяет базовый URL-адрес для создания события в Facebook.
3.  **Создание параметров запроса**: Создает параметры запроса, включая `acontext`, `dialog_entry_point` и `group_id`.
4.  **Кодирование параметров**: Кодирует параметры запроса в строку запроса.
5.  **Объединение URL и параметров**: Объединяет базовый URL-адрес и строку запроса для создания полного URL-адреса создания события.

```
   group_url
     ↓
   Извлечение group_id
     ↓
   Формирование базового URL
     ↓
   Создание параметров запроса
     ↓
   Кодирование параметров
     ↓
   Объединение URL и параметров → event_url
```

**Примеры**:

```python
group_url = "https://www.facebook.com/groups/1234567890/"
event_url = get_event_url(group_url)
print(event_url)  # Вывод: https://www.facebook.com/events/create/?acontext=%7B%22event_action_history%22%3A%5B%7B%22surface%22%3A%22group%22%7D%2C%7B%22mechanism%22%3A%22upcoming_events_for_group%22%2C%22surface%22%3A%22group%22%7D%5D%2C%22ref_notif_type%22%3Anull%7D&dialog_entry_point=group_events_tab&group_id=1234567890
```
```python
def __init__(self, d: Driver, promoter: str, group_file_paths: Optional[list[str | Path] | str | Path] = None, no_video: bool = False):
    """ Initializes the promoter for Facebook groups.

    Args:
        d (Driver): WebDriver instance for browser automation.
        group_file_paths (list[str | Path] | str | Path): List of file paths containing group data.
        no_video (bool, optional): Flag to disable videos in posts. Defaults to False.
    """
```

**Методы**:

*   `__init__`: Инициализирует промоутер для групп Facebook.

**Параметры**:

*   `d` (Driver): Экземпляр WebDriver для автоматизации браузера.
*   `promoter` (str): Имя промоутера (например, "aliexpress").
*   `group_file_paths` (list[str  |  Path] | str | Path, optional): Список путей к файлам, содержащим данные о группах. По умолчанию `None`. Если `None`, используется путь `gs.path.google_drive / 'facebook' / 'groups'`.
*   `no_video` (bool, optional): Флаг, указывающий, следует ли отключать видео в публикациях. По умолчанию `False`.

**Как работает функция**:

1.  **Инициализация атрибутов**: Присваивает переданные значения атрибутам экземпляра класса.
2.  **Определение путей к файлам групп**: Если `group_file_paths` не указан, использует функцию `get_filenames` для получения списка файлов из каталога `gs.path.google_drive / 'facebook' / 'groups'`.
3.  **Инициализация спиннера**: Создает экземпляр класса `spinning_cursor` для отображения спиннера в консоли во время выполнения операций.

```
       d, promoter, group_file_paths, no_video
         ↓
       Присвоение значений атрибутам экземпляра класса
         ↓
       Определение путей к файлам групп (если не указаны)
         ↓
       Инициализация спиннера
```
```python
def promote(self, group: SimpleNamespace, item: SimpleNamespace, is_event: bool = False, language: str = None, currency: str = None) -> bool:
    """Promotes a category or event in a Facebook group."""
    ...
```

**Методы**:

*   `promote`: Продвигает категорию или событие в группе Facebook.

**Параметры**:

*   `group` (SimpleNamespace): Объект, содержащий данные о группе Facebook.
*   `item` (SimpleNamespace): Объект, содержащий данные о категории или событии для продвижения.
*   `is_event` (bool, optional): Флаг, указывающий, является ли продвигаемый элемент событием. По умолчанию `False`.
*   `language` (str, optional): Язык продвигаемого элемента. По умолчанию `None`.
*   `currency` (str, optional): Валюта продвигаемого элемента. По умолчанию `None`.

**Возвращает**:

*   `bool`: `True`, если продвижение прошло успешно, `False` в противном случае.

**Как работает функция**:

1.  **Фильтрация по языку и валюте (если указаны)**: Если указаны язык и валюта, функция проверяет, соответствуют ли они языку и валюте группы. Если нет, функция завершается.
2.  **Определение имени элемента**: Определяет имя продвигаемого элемента (категории или события).
3.  **Установка атрибутов события или сообщения**: Если продвигается событие, устанавливает атрибуты `start`, `end` и `promotional_link`.
4.  **Публикация**: В зависимости от типа промоутера и типа элемента вызывается соответствующая функция для публикации. Для событий вызывается функция `post_event`, для категорий - `post_message` или `post_ad`.
5.  **Обработка ошибок**: Если публикация не удалась, функция логирует ошибку и завершается.
6.  **Обновление данных группы**: После успешной публикации функция обновляет данные о группе, чтобы избежать повторной публикации одного и того же контента.
7.  **Возврат значения**: Возвращает `True`, если продвижение прошло успешно, `False` в противном случае.

```
   group, item, is_event, language, currency
     ↓
   Фильтрация по языку и валюте (если указаны)
     ↓
   Определение имени элемента
     ↓
   Установка атрибутов события или сообщения
     ↓
   Публикация (post_event, post_message или post_ad)
     ↓
   Обработка ошибок
     ↓
   Обновление данных группы
     ↓
   Возврат значения
```
```python
def log_promotion_error(self, is_event: bool, item_name: str):
    """Logs promotion error for category or event."""
    logger.debug(f"Error while posting {\'event\' if is_event else \'category\'} {item_name}", None, False)
```

**Методы**:

*   `log_promotion_error`: Логирует ошибку продвижения для категории или события.

**Параметры**:

*   `is_event` (bool): Флаг, указывающий, является ли продвигаемый элемент событием.
*   `item_name` (str): Имя продвигаемого элемента.

**Как работает функция**:

1.  **Формирование сообщения об ошибке**: Формирует сообщение об ошибке, включающее тип элемента (событие или категория) и его имя.
2.  **Логирование ошибки**: Логирует сообщение об ошибке с использованием `logger.debug`.
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

**Методы**:

*   `update_group_promotion_data`: Обновляет данные группы после успешной публикации.

**Параметры**:

*   `group` (SimpleNamespace): Объект, содержащий данные о группе Facebook.
*   `item_name` (str): Имя продвигаемого элемента.
*   `is_event` (bool, optional): Флаг, указывающий, является ли продвигаемый элемент событием. По умолчанию `False`.

**Как работает функция**:

1.  **Получение текущей временной метки**: Получает текущую временную метку в формате "%d/%m/%y %H:%M".
2.  **Обновление времени последней отправки промо**: Обновляет атрибут `group.last_promo_sended` текущим временем.
3.  **Обновление списка продвинутых элементов**: В зависимости от того, является ли продвигаемый элемент событием или категорией, добавляет имя элемента в список `group.promoted_events` или `group.promoted_categories`.
4.  **Установка временной метки последней отправки промо**: Устанавливает атрибут `group.last_promo_sended` в текущую временную метку.
```python
def process_groups(self, campaign_name: str = None, events: list[SimpleNamespace] = None, is_event: bool = False, group_file_paths: list[str] = None, group_categories_to_adv: list[str] = ['sales'], language: str = None, currency: str = None):
    """Processes all groups for the current campaign or event promotion."""
    ...
```

**Методы**:

*   `process_groups`: Обрабатывает все группы для текущей кампании или продвижения события.

**Параметры**:

*   `campaign_name` (str, optional): Название кампании. По умолчанию `None`.
*   `events` (list[SimpleNamespace], optional): Список событий для продвижения. По умолчанию `None`.
*   `is_event` (bool, optional): Флаг, указывающий, является ли продвигаемый элемент событием. По умолчанию `False`.
*   `group_file_paths` (list[str], optional): Список путей к файлам, содержащим данные о группах. По умолчанию `None`.
*   `group_categories_to_adv` (list[str], optional): Список категорий групп для продвижения. По умолчанию `['sales']`.
*   `language` (str, optional): Язык продвигаемого элемента. По умолчанию `None`.
*   `currency` (str, optional): Валюта продвигаемого элемента. По умолчанию `None`.

**Как работает функция**:

1.  **Проверка наличия элементов для продвижения**: Если `campaign_name` и `events` не указаны, функция логирует сообщение и завершается.
2.  **Перебор файлов групп**: Перебирает файлы, указанные в `group_file_paths`.
3.  **Загрузка данных о группах**: Загружает данные о группах из каждого файла с использованием `j_loads_ns`.
4.  **Перебор групп**: Перебирает группы в каждом файле.
5.  **Проверка интервала**: Если продвигается категория, проверяет, прошло ли достаточно времени с момента последней публикации в группе.
6.  **Проверка категорий и статуса**: Проверяет, соответствуют ли категории группы категориям для продвижения и является ли группа активной.
7.  **Получение элемента для продвижения**: Если продвигается категория, вызывает функцию `get_category_item` для получения элемента. Если продвигается событие, выбирает случайное событие из списка `events`.
8.  **Проверка на дублирование**: Проверяет, был ли уже продвинут элемент в группе.
9.  **Получение URL**: Получает URL группы или события.
10. **Продвижение**: Вызывает функцию `promote` для продвижения элемента в группе.
11. **Сохранение данных о группах**: Сохраняет обновленные данные о группах в файл с использованием `j_dumps`.
12. **Задержка**: Приостанавливает выполнение на случайное время.
```python
def get_category_item(self, campaign_name: str, group: SimpleNamespace, language: str, currency: str) -> SimpleNamespace:
    """Fetches the category item for promotion based on the campaign and promoter."""
    ...
```

**Методы**:

*   `get_category_item`: Получает элемент категории для продвижения на основе кампании и промоутера.

**Параметры**:

*   `campaign_name` (str): Название кампании.
*   `group` (SimpleNamespace): Объект, содержащий данные о группе Facebook.
*   `language` (str): Язык продвигаемого элемента.
*   `currency` (str): Валюта продвигаемого элемента.

**Возвращает**:

*   `SimpleNamespace`: Объект, содержащий данные о категории для продвижения.

**Как работает функция**:

1.  **Определение промоутера**: Определяет, какой промоутер используется (например, "aliexpress").
2.  **Получение элемента для промоутера AliExpress**: Если промоутер "aliexpress", использует класс `AliCampaignEditor` для получения списка категорий и случайного выбора категории для продвижения.
3.  **Получение элемента для других промоутеров**: Если промоутер не "aliexpress", загружает данные о категориях из JSON-файла, выбирает случайную категорию и получает ее описание из текстового файла.
4.  **Возврат элемента**: Возвращает объект, содержащий данные о категории для продвижения.
```python
def check_interval(self, group: SimpleNamespace) -> bool:
    """Checks if enough time has passed for promoting this group."""
    ...
```

**Методы**:

*   `check_interval`: Проверяет, достаточно ли времени прошло для продвижения этой группы.

**Параметры**:

*   `group` (SimpleNamespace): Объект, содержащий данные о группе Facebook.

**Возвращает**:

*   `bool`: `True`, если достаточно времени прошло для продвижения группы, `False` в противном случае.

**Как работает функция**:

Функция всегда возвращает `True`. В предоставленном коде отсутствует реализация проверки интервала.
```python
def validate_group(self, group: SimpleNamespace) -> bool:
    """Validates that the group data is correct."""
    return group and hasattr(group, 'group_url') and hasattr(group, 'group_categories')
```

**Методы**:

*   `validate_group`: Проверяет, что данные группы корректны.

**Параметры**:

*   `group` (SimpleNamespace): Объект, содержащий данные о группе Facebook.

**Возвращает**:

*   `bool`: `True`, если данные группы корректны, `False` в противном случае.

**Как работает функция**:

1.  **Проверка наличия группы**: Проверяет, что объект `group` не является `None`.
2.  **Проверка наличия атрибутов**: Проверяет, что объект `group` имеет атрибуты `group_url` и `group_categories`.
3.  **Возврат значения**: Возвращает `True`, если все проверки пройдены, `False` в противном случае.