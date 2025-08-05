# Модуль парсера BeautifulSoup и XPath

## Обзор

Модуль `src.webdriver.bs` предоставляет кастомную реализацию для парсинга HTML-контента с использованием BeautifulSoup и XPath. Он позволяет загружать HTML-контент из файлов или URL-адресов, парсить его и извлекать элементы с помощью XPath-локаторов.

## Подробней

Этот модуль является частью проекта `hypotez` и используется для извлечения данных из HTML-страниц с помощью BeautifulSoup и XPath. 

- Модуль импортируется как `BS`.
- Для загрузки конфигурации используйте `j_loads_ns` из модуля `src.utils.jjson`.
- Для определения локатора используйте `SimpleNamespace` из `types`.

## Классы

### `BS`

**Описание**: Класс `BS` реализует парсер BeautifulSoup и XPath для HTML-контента. Он предоставляет методы для загрузки HTML-контента из файлов или URL-адресов, парсинга его и извлечения элементов с помощью XPath-локаторов.

**Атрибуты**:

- `_url` (str): URL или путь к файлу, из которого был загружен HTML-контент.
- `_soup` (BeautifulSoup): Объект BeautifulSoup, представляющий HTML-контент.
- `_default_locator` (dict): Локатор по умолчанию для извлечения элементов.

**Методы**:

#### `get_url(url: str)`

**Назначение**: Загружает HTML-контент из указанного URL-адреса.

**Параметры**:

- `url` (str): URL-адрес HTML-страницы.

#### `get_file(file_path: str)`

**Назначение**: Загружает HTML-контент из указанного файла.

**Параметры**:

- `file_path` (str): Путь к файлу, содержащему HTML-контент.

#### `execute_locator(locator: dict) -> list`

**Назначение**: Извлекает элементы из HTML-контента с помощью XPath-локатора.

**Параметры**:

- `locator` (dict): Словарь, содержащий описание локатора:
    - `by` (str): Тип локатора (например, `ID`, `CSS`, `TEXT`).
    - `attribute` (str): Атрибут для поиска (например, `element_id`).
    - `selector` (str): XPath-селектор для извлечения элементов.

**Возвращает**:

- `list`: Список элементов, найденных с помощью указанного локатора.

#### `get_soup() -> BeautifulSoup`

**Назначение**: Возвращает объект BeautifulSoup, представляющий HTML-контент.

**Возвращает**:

- `BeautifulSoup`: Объект BeautifulSoup.


## Примеры

### Пример 1: Загрузка HTML из файла

```python
from src.webdriver.bs import BS
from types import SimpleNamespace
from src.utils.jjson import j_loads_ns
from pathlib import Path

# Загрузка настроек из конфигурационного файла
settings_path = Path('path/to/bs.json')
settings = j_loads_ns(settings_path)

# Инициализация парсера BS с URL по умолчанию
parser = BS(url=settings.default_url)

# Использование локатора по умолчанию из конфигурации
locator = SimpleNamespace(**settings.default_locator)
elements = parser.execute_locator(locator)
print(elements)
```

### Пример 2: Загрузка HTML из URL

```python
from src.webdriver.bs import BS
from types import SimpleNamespace

parser = BS()
parser.get_url('https://example.com')
locator = SimpleNamespace(by='CSS', attribute='class_name', selector='//*[contains(@class, "class_name")]')
elements = parser.execute_locator(locator)
print(elements)
```

## Логирование и отладка

Парсер `BS` использует `logger` из `src.logger` для логирования ошибок, предупреждений и общей информации. Все проблемы, возникающие при инициализации, конфигурации или выполнении, будут записываться в логи для удобства отладки.

### Примеры логов

- **Ошибка при инициализации**: `Ошибка при инициализации парсера BS: <детали ошибки>`
- **Проблемы с конфигурацией**: `Ошибка в файле bs.json: <детали проблемы>`
- **Ошибка при обработке**: `Ошибка при выполнении XPath-локатора: <детали ошибки>`
- **Ошибка при получении HTML**: `Ошибка при загрузке HTML-контента: <детали ошибки>`

## Лицензия

Этот проект лицензирован на условиях MIT License. Подробности см. в файле [LICENSE](../../LICENSE).