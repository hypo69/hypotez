# Модуль Facebook Promoter

## Обзор

Модуль **Facebook Promoter** автоматизирует продвижение товаров и событий AliExpress в группах Facebook. Модуль управляет публикацией рекламных акций в Facebook, обеспечивая продвижение категорий и событий без дубликатов. Он использует WebDriver для автоматизации работы браузера, чтобы эффективно управлять рекламными акциями.

## Функциональность модуля

- Продвижение категорий и событий в группах Facebook.
- Избежание дублирования рекламных акций путем отслеживания ранее продвигаемых элементов.
- Поддержка конфигурации данных группы через файлы.
- Возможность отключения загрузки видео в рекламных акциях.

## Требования

- **Python** 3.x
- Необходимые библиотеки:
  - `random`
  - `datetime`
  - `pathlib`
  - `urllib.parse`
  - `types.SimpleNamespace`
  - `src` (пользовательский модуль)

## Блок-схема

```mermaid
flowchart TD
    A[Start] --> B[Инициализация WebDriver];
    B --> C[Создание экземпляра FacebookPromoter];
    C --> D[Обработка групп для продвижения];
    D --> E[Получение данных группы];
    E --> F{Данные группы действительны?};
    F -- Да --> G[Получение элемента категории для продвижения];
    F -- Нет --> H[Логирование ошибки и выход];
    G --> I{Можно ли продвигать группу?};
    I -- Да --> J[Продвижение категории или события];
    I -- Нет --> K[Ожидание интервала между продвижениями];
    J --> L[Обновление данных группы];
    K --> L;
    L --> M[Конец];
    H --> M;
```

## Использование

### Пример использования класса FacebookPromoter

```python
from src.endpoints.advertisement.facebook.promoter import FacebookPromoter
from src.webdriver.driver import Driver
from src.utils.jjson import j_loads_ns

# Настройка экземпляра WebDriver (замените фактическим WebDriver)
d = Driver()

# Создание экземпляра FacebookPromoter
promoter = FacebookPromoter(
    d=d,
    promoter="aliexpress",
    group_file_paths=["path/to/group/file1.json", "path/to/group/file2.json"]
)

# Начать продвижение товаров или событий
promoter.process_groups(
    campaign_name="Campaign1",
    events=[],
    group_categories_to_adv=["sales"],
    language="en",
    currency="USD"
)
```

## Документация по классам

### Класс `FacebookPromoter`

Этот класс управляет процессом продвижения товаров и событий AliExpress в группах Facebook.

#### Методы

##### `__init__(self, d: Driver, promoter: str, group_file_paths: Optional[list[str | Path] | str | Path] = None, no_video: bool = False)`

Инициализирует промоутер Facebook с необходимыми конфигурациями.

- **Args:**
    - `d (Driver)`: Экземпляр WebDriver для автоматизации.
    - `promoter (str)`: Название промоутера (например, "aliexpress").
    - `group_file_paths (Optional[list[str | Path] | str | Path])`: Пути к файлам данных группы.
    - `no_video (bool)`: Флаг для отключения видео в постах. По умолчанию `False`.

##### `promote(self, group: SimpleNamespace, item: SimpleNamespace, is_event: bool = False, language: str = None, currency: str = None) -> bool`

Продвигает категорию или событие в указанной группе Facebook.

- **Args:**
    - `group (SimpleNamespace)`: Данные группы.
    - `item (SimpleNamespace)`: Элемент категории или события для продвижения.
    - `is_event (bool)`: Указывает, является ли элемент событием.
    - `language (str)`: Язык рекламной акции.
    - `currency (str)`: Валюта для рекламной акции.

- **Returns:**
    - `bool`: Успешно ли прошло продвижение.

##### `log_promotion_error(self, is_event: bool, item_name: str)`

Логирует ошибку при сбое продвижения.

- **Args:**
    - `is_event (bool)`: Указывает, является ли элемент событием.
    - `item_name (str)`: Название элемента.

##### `update_group_promotion_data(self, group: SimpleNamespace, item_name: str, is_event: bool = False)`

Обновляет данные группы после продвижения, добавляя продвигаемый элемент в список продвинутых категорий или событий.

- **Args:**
    - `group (SimpleNamespace)`: Данные группы.
    - `item_name (str)`: Название продвинутого элемента.
    - `is_event (bool)`: Указывает, является ли элемент событием.

##### `process_groups(self, campaign_name: str = None, events: list[SimpleNamespace] = None, is_event: bool = False, group_file_paths: list[str] = None, group_categories_to_adv: list[str] = ['sales'], language: str = None, currency: str = None)`

Обрабатывает группы для текущей рекламной кампании или продвижения события.

- **Args:**
    - `campaign_name (str)`: Название кампании.
    - `events (list[SimpleNamespace])`: Список событий для продвижения.
    - `is_event (bool)`: Указывает, продвигать события или категории.
    - `group_file_paths (list[str])`: Пути к файлам данных группы.
    - `group_categories_to_adv (list[str])`: Категории для продвижения.
    - `language (str)`: Язык рекламной акции.
    - `currency (str)`: Валюта для рекламной акции.

##### `get_category_item(self, campaign_name: str, group: SimpleNamespace, language: str, currency: str) -> SimpleNamespace`

Получает элемент категории для продвижения на основе кампании и промоутера.

- **Args:**
    - `campaign_name (str)`: Название кампании.
    - `group (SimpleNamespace)`: Данные группы.
    - `language (str)`: Язык рекламной акции.
    - `currency (str)`: Валюта для рекламной акции.

- **Returns:**
    - `SimpleNamespace`: Элемент категории для продвижения.

##### `check_interval(self, group: SimpleNamespace) -> bool`

Проверяет, достаточно ли времени прошло для повторного продвижения этой группы.

- **Args:**
    - `group (SimpleNamespace)`: Данные группы.

- **Returns:**
    - `bool`: Может ли группа быть продвинута.

##### `validate_group(self, group: SimpleNamespace) -> bool`

Проверяет данные группы, чтобы убедиться, что у нее есть необходимые атрибуты.

- **Args:**
    - `group (SimpleNamespace)`: Данные группы.

- **Returns:**
    - `bool`: Действительны ли данные группы.

## Лицензия

Этот модуль является частью более крупного пакета **Facebook Promoter** и лицензируется в соответствии с лицензией MIT.