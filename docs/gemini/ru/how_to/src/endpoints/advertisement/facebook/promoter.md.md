## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода представляет собой документацию для модуля **Facebook Promoter**, который автоматизирует продвижение товаров и мероприятий AliExpress в группах Facebook. Модуль управляет публикацией промоакций в Facebook, гарантируя, что категории и события рекламируются без дубликатов. Он использует WebDriver для автоматизации браузера, чтобы эффективно управлять промоакциями.

Шаги выполнения
-------------------------
1. **Инициализация WebDriver**: Создается экземпляр WebDriver для автоматизации браузера (например, Chrome или Firefox).
2. **Создание экземпляра FacebookPromoter**: Создается экземпляр класса `FacebookPromoter` с необходимыми конфигурациями:
    - `d`: Экземпляр WebDriver.
    - `promoter`: Название промоутера (например, "aliexpress").
    - `group_file_paths`: Пути к файлам с данными о группах.
    - `no_video`: Флаг для отключения видео в постах (по умолчанию `False`).
3. **Обработка групп для продвижения**: Метод `process_groups` запускает процесс продвижения товаров или событий в группах.
4. **Получение данных о группе**: Метод `get_group_data` извлекает данные о группе из файла.
5. **Проверка валидности данных о группе**: Проверяется, соответствуют ли данные группы необходимым требованиям.
6. **Получение товара категории для продвижения**: Метод `get_category_item` извлекает товар категории для продвижения.
7. **Проверка возможности продвижения в группе**: Проверяется, можно ли продвигать в этой группе.
8. **Продвижение категории или события**: Метод `promote` публикует промоакцию товара или события в группе.
9. **Обновление данных о группе**: После успешного продвижения метод `update_group_promotion_data` обновляет данные группы, добавив продвинутый товар в список уже продвинутых.
10. **Ожидание интервала между продвижениями**: Если группа не доступна для продвижения, метод `check_interval` проверяет, прошло ли достаточно времени для следующего продвижения.
11. **Завершение**: После обработки всех групп цикл завершается.

Пример использования
-------------------------

```python
from src.endpoints.advertisement.facebook.promoter import FacebookPromoter
from src.webdriver.driver import Driver
from src.utils.jjson import j_loads_ns

# Setup WebDriver instance (replace with actual WebDriver)
d = Driver()

# Create an instance of FacebookPromoter
promoter = FacebookPromoter(
    d=d, 
    promoter="aliexpress", 
    group_file_paths=["path/to/group/file1.json", "path/to/group/file2.json"]
)

# Start promoting products or events
promoter.process_groups(
    campaign_name="Campaign1",
    events=[], 
    group_categories_to_adv=["sales"],
    language="en",
    currency="USD"
)
```

## Класс `FacebookPromoter`

### Методы

#### `__init__(self, d: Driver, promoter: str, group_file_paths: Optional[list[str | Path] | str | Path] = None, no_video: bool = False)`

Инициализирует Facebook Promoter с необходимыми конфигурациями.

- **Аргументы:**
    - `d (Driver)`: Экземпляр WebDriver для автоматизации.
    - `promoter (str)`: Название промоутера (например, "aliexpress").
    - `group_file_paths (Optional[list[str | Path] | str | Path])`: Пути к файлам с данными о группах.
    - `no_video (bool)`: Флаг для отключения видео в постах. По умолчанию `False`.

#### `promote(self, group: SimpleNamespace, item: SimpleNamespace, is_event: bool = False, language: str = None, currency: str = None) -> bool`

Продвигает категорию или событие в указанной группе Facebook.

- **Аргументы:**
    - `group (SimpleNamespace)`: Данные о группе.
    - `item (SimpleNamespace)`: Товар категории или событие для продвижения.
    - `is_event (bool)`: Является ли товар событием.
    - `language (str)`: Язык продвижения.
    - `currency (str)`: Валюта для продвижения.

- **Возвращает:**
    - `bool`: Успешное ли было продвижение.

#### `log_promotion_error(self, is_event: bool, item_name: str)`

Регистрирует ошибку при неудачном продвижении.

- **Аргументы:**
    - `is_event (bool)`: Является ли товар событием.
    - `item_name (str)`: Название товара.

#### `update_group_promotion_data(self, group: SimpleNamespace, item_name: str, is_event: bool = False)`

Обновляет данные о группе после продвижения, добавив продвинутый товар в список уже продвинутых категорий или событий.

- **Аргументы:**
    - `group (SimpleNamespace)`: Данные о группе.
    - `item_name (str)`: Название товара, который был продвинут.
    - `is_event (bool)`: Является ли товар событием.

#### `process_groups(self, campaign_name: str = None, events: list[SimpleNamespace] = None, is_event: bool = False, group_file_paths: list[str] = None, group_categories_to_adv: list[str] = ['sales'], language: str = None, currency: str = None)`

Обрабатывает группы для текущей кампании или продвижения событий.

- **Аргументы:**
    - `campaign_name (str)`: Название кампании.
    - `events (list[SimpleNamespace])`: Список событий для продвижения.
    - `is_event (bool)`: Продвигать ли события или категории.
    - `group_file_paths (list[str])`: Пути к файлам с данными о группах.
    - `group_categories_to_adv (list[str])`: Категории для продвижения.
    - `language (str)`: Язык продвижения.
    - `currency (str)`: Валюта для продвижения.

#### `get_category_item(self, campaign_name: str, group: SimpleNamespace, language: str, currency: str) -> SimpleNamespace`

Извлекает товар категории для продвижения на основе кампании и промоутера.

- **Аргументы:**
    - `campaign_name (str)`: Название кампании.
    - `group (SimpleNamespace)`: Данные о группе.
    - `language (str)`: Язык для продвижения.
    - `currency (str)`: Валюта для продвижения.

- **Возвращает:**
    - `SimpleNamespace`: Товар категории для продвижения.

#### `check_interval(self, group: SimpleNamespace) -> bool`

Проверяет, прошло ли достаточно времени для продвижения в этой группе.

- **Аргументы:**
    - `group (SimpleNamespace)`: Данные о группе.

- **Возвращает:**
    - `bool`: Доступна ли группа для продвижения.

#### `validate_group(self, group: SimpleNamespace) -> bool`

Проверяет данные о группе на наличие необходимых атрибутов.

- **Аргументы:**
    - `group (SimpleNamespace)`: Данные о группе.

- **Возвращает:**
    - `bool`: Валидны ли данные о группе.

## Лицензия

Этот модуль является частью более крупного пакета **Facebook Promoter** и распространяется по лицензии MIT.