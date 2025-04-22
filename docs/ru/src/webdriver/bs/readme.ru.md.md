# Документация модуля `src.webdriver.bs`

## Обзор

Модуль `src.webdriver.bs` предоставляет кастомную реализацию парсинга HTML-контента с использованием библиотек BeautifulSoup и XPath. Он позволяет загружать HTML-контент из файлов или URL-адресов, парсить его и извлекать элементы с помощью XPath-локаторов.

## Подробнее

Этот модуль предназначен для упрощения процесса парсинга HTML-страниц и извлечения данных с использованием гибких XPath-запросов. Он предоставляет удобный интерфейс для работы с BeautifulSoup и XPath, а также включает в себя механизмы логирования и обработки ошибок для обеспечения стабильности и надежности. Модуль использует файл конфигурации `bs.json` для централизованного управления настройками, такими как URL по умолчанию, пути к файлам, параметры прокси и параметры логирования.

## Конфигурация

### Файл `bs.json`

Конфигурация для парсера `BS` хранится в файле `bs.json`. Ниже приведён пример структуры конфигурационного файла и его описание:

```json
{
  "default_url": "https://example.com",
  "default_file_path": "file://path/to/your/file.html",
  "default_locator": {
    "by": "ID",
    "attribute": "element_id",
    "selector": "//*[@id=\'element_id\']"
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

#### `default_url`

URL по умолчанию для загрузки HTML-контента.

#### `default_file_path`

Путь к файлу по умолчанию для загрузки HTML-контента.

#### `default_locator`

Локатор по умолчанию для извлечения элементов:

- **by**: Тип локатора (например, `ID`, `CSS`, `TEXT`).
- **attribute**: Атрибут для поиска (например, `element_id`).
- **selector**: XPath-селектор для извлечения элементов.

#### `logging`

Настройки логирования:

- **level**: Уровень логирования (например, `INFO`, `DEBUG`, `ERROR`).
- **file**: Путь к файлу, куда будут записываться логи.

#### `proxy`

Настройки прокси-сервера:

- **enabled**: Булевое значение, указывающее, следует ли использовать прокси.
- **server**: Адрес прокси-сервера.
- **username**: Имя пользователя для аутентификации на прокси-сервере.
- **password**: Пароль для аутентификации на прокси-сервере.

#### `timeout`

Максимальное время ожидания для запросов (в секундах).

#### `encoding`

Кодировка, используемая при чтении файлов или запросах.

## Использование

Чтобы использовать парсер `BS` в своём проекте, просто импортируйте его и инициализируйте:

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

- **Ошибка при инициализации**: `Ошибка при инициализации парсера BS: <детали ошибки>`
- **Проблемы с конфигурацией**: `Ошибка в файле bs.json: <детали проблемы>`