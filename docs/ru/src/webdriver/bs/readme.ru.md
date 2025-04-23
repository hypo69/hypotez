# Документация модуля `src.webdriver.bs`

## Обзор

Модуль `src.webdriver.bs` предоставляет функциональность для парсинга HTML-контента с использованием библиотек BeautifulSoup и XPath. Он позволяет загружать HTML из файлов или URL-адресов, анализировать его и извлекать необходимые элементы, используя XPath-локаторы.

## Подробней

Этот модуль предназначен для упрощения процесса парсинга HTML-страниц в проекте `hypotez`. Он предоставляет удобный интерфейс для загрузки и анализа HTML-контента, а также гибкие возможности для извлечения данных с использованием XPath-локаторов. Модуль включает поддержку конфигурации через файл `bs.json`, что позволяет настраивать параметры парсинга, такие как URL по умолчанию, пути к файлам, настройки прокси и параметры логирования.

## Содержание

1.  [Классы](#классы)
    *   [BS](#bs)
2.  [Конфигурация](#конфигурация)
    *   [Пример конфигурации (bs.json)](#пример-конфигурации-bsjson)
    *   [Описание полей конфигурации](#описание-полей-конфигурации)
3.  [Использование](#использование)
    *   [Пример: Загрузка HTML из файла](#пример-загрузка-html-из-файла)
    *   [Пример: Загрузка HTML из URL](#пример-загрузка-html-из-url)
4.  [Логирование и отладка](#логирование-и-отладка)
5.  [Лицензия](#лицензия)

## Классы

### `BS`

**Описание**: Класс `BS` предоставляет методы для загрузки, парсинга и извлечения элементов из HTML-контента с использованием BeautifulSoup и XPath.

**Атрибуты**:
*   `default_url` (str): URL по умолчанию для загрузки HTML-контента.
*   `default_file_path` (str): Путь к файлу по умолчанию для загрузки HTML-контента.
*   `default_locator` (dict): Локатор по умолчанию для извлечения элементов.
*   `logging` (dict): Настройки логирования.
*   `proxy` (dict): Настройки прокси-сервера.
*   `timeout` (int): Максимальное время ожидания для запросов (в секундах).
*   `encoding` (str): Кодировка, используемая при чтении файлов или запросах.

**Методы**:
*   `__init__(self, url: Optional[str] = None, file_path: Optional[str] = None, config_path: Optional[str | Path] = None)`: Инициализирует экземпляр класса `BS`.
*   `get_url(self, url: str, method: str = 'get', data: Optional[dict] = None, headers: Optional[dict] = None) -> str`: Загружает HTML-контент из указанного URL.
*   `get_file(self, file_path: str, encoding: str = 'utf-8') -> str`: Загружает HTML-контент из указанного файла.
*   `get_html(self, html: str) -> str`: Устанавливает HTML-контент для парсинга.
*   `execute_locator(self, locator: dict) -> list`: Извлекает элементы из HTML-контента, используя указанный локатор.

## Конфигурация

Конфигурация для парсера `BS` хранится в файле `bs.json`.

### Пример конфигурации (`bs.json`)

```json
{
  "default_url": "https://example.com",
  "default_file_path": "file://path/to/your/file.html",
  "default_locator": {
    "by": "ID",
    "attribute": "element_id",
    "selector": "//*[@id='element_id']"
  },
  "logging": {
    "level": "INFO",
    "file": "logs/bs.log"
  },
  "proxy": {
    "enabled": false,
    "server": "http://proxy.example.com:8080",
    "username": "user",
    "password": "password"
  },
  "timeout": 10,
  "encoding": "utf-8"
}
```

### Описание полей конфигурации

#### 1. `default_url`

URL по умолчанию для загрузки HTML-контента.

#### 2. `default_file_path`

Путь к файлу по умолчанию для загрузки HTML-контента.

#### 3. `default_locator`

Локатор по умолчанию для извлечения элементов:

*   **by**: Тип локатора (например, `ID`, `CSS`, `TEXT`).
*   **attribute**: Атрибут для поиска (например, `element_id`).
*   **selector**: XPath-селектор для извлечения элементов.

#### 4. `logging`

Настройки логирования:

*   **level**: Уровень логирования (например, `INFO`, `DEBUG`, `ERROR`).
*   **file**: Путь к файлу, куда будут записываться логи.

#### 5. `proxy`

Настройки прокси-сервера:

*   **enabled**: Булевое значение, указывающее, следует ли использовать прокси.
*   **server**: Адрес прокси-сервера.
*   **username**: Имя пользователя для аутентификации на прокси-сервере.
*   **password**: Пароль для аутентификации на прокси-сервере.

#### 6. `timeout`

Максимальное время ожидания для запросов (в секундах).

#### 7. `encoding`

Кодировка, используемая при чтении файлов или запросах.

## Использование

Для использования парсера `BS` в своём проекте, импортируйте его и инициализируйте:

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

### Пример: Загрузка HTML из файла

```python
parser = BS()
parser.get_url('file://path/to/your/file.html')
locator = SimpleNamespace(by='ID', attribute='element_id', selector='//*[@id="element_id"]')
elements = parser.execute_locator(locator)
print(elements)
```

### Пример: Загрузка HTML из URL

```python
parser = BS()
parser.get_url('https://example.com')
locator = SimpleNamespace(by='CSS', attribute='class_name', selector='//*[contains(@class, "class_name")]')
elements = parser.execute_locator(locator)
print(elements)
```

## Логирование и отладка

Парсер `BS` использует `logger` из `src.logger` для логирования ошибок, предупреждений и общей информации. Все проблемы, возникающие при инициализации, конфигурации или выполнении, будут записываться в логи для удобства отладки.

### Примеры логов

*   **Ошибка при инициализации**: `Ошибка при инициализации парсера BS: <детали ошибки>`
*   **Проблемы с конфигурацией**: `Ошибка в файле bs.json: <детали проблемы>`

## Лицензия

Этот проект лицензирован на условиях MIT License. Подробности см. в файле [LICENSE](../../LICENSE).