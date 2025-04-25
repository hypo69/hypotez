# BeautifulSoup и XPath парсер

## Обзор

Этот модуль предоставляет собственную реализацию для разбора HTML-контента с использованием BeautifulSoup и XPath. Он позволяет вам получать HTML-контент из файлов или URL, анализировать его и извлекать элементы с использованием XPath-локаторов.

## Ключевые особенности

- **Разбор HTML**: Использует BeautifulSoup и XPath для эффективного разбора HTML.
- **Поддержка файлов и URL**: Получает HTML-контент из локальных файлов или веб-URL.
- **Пользовательские локаторы**: Позволяет вам определять пользовательские XPath-локаторы для извлечения элементов.
- **Журналирование и обработка ошибок**: Обеспечивает подробные журналы для отладки и отслеживания ошибок.
- **Поддержка конфигурации**: Централизованная конфигурация через файл `bs.json`.

## Требования

Перед использованием этого модуля убедитесь, что установлены следующие зависимости:

- Python 3.x
- BeautifulSoup
- lxml
- requests

Установите необходимые зависимости Python:

```bash
pip install beautifulsoup4 lxml requests
```

## Конфигурация

Конфигурация для парсера `BS` хранится в файле `bs.json`. Ниже приведена примерная структура конфигурационного файла и его описание:

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

URL по умолчанию для получения HTML-контента.

#### 2. `default_file_path`

Путь к файлу по умолчанию для получения HTML-контента.

#### 3. `default_locator`

Локатор по умолчанию для извлечения элементов:

- **by**: Тип локатора (например, `ID`, `CSS`, `TEXT`).
- **attribute**: Атрибут для поиска (например, `element_id`).
- **selector**: XPath-селектор для извлечения элементов.

#### 4. `logging`

Настройки журналирования:

- **level**: Уровень журналирования (например, `INFO`, `DEBUG`, `ERROR`).
- **file**: Путь к файлу журнала.

#### 5. `proxy`

Настройки прокси-сервера:

- **enabled**: Логическое значение, указывающее, следует ли использовать прокси.
- **server**: Адрес прокси-сервера.
- **username**: Имя пользователя для аутентификации прокси.
- **password**: Пароль для аутентификации прокси.

#### 6. `timeout`

Максимальное время ожидания запросов (в секундах).

#### 7. `encoding`

Кодировка, используемая при чтении файлов или выполнении запросов.

## Использование

Чтобы использовать парсер `BS` в вашем проекте, просто импортируйте и инициализируйте его:

```python
from src.webdriver.bs import BS
from types import SimpleNamespace
from src.utils.jjson import j_loads_ns
from pathlib import Path

# Загрузка настроек из конфигурационного файла
settings_path = Path('path/to/bs.json')
settings = j_loads_ns(settings_path)

# Инициализация парсера BS с использованием URL по умолчанию
parser = BS(url=settings.default_url)

# Использование локатора по умолчанию из конфигурации
locator = SimpleNamespace(**settings.default_locator)
elements = parser.execute_locator(locator)
print(elements)
```

### Пример: Получение HTML из файла

```python
parser = BS()
parser.get_url('file://path/to/your/file.html')
locator = SimpleNamespace(by='ID', attribute='element_id', selector='//*[@id="element_id"]')
elements = parser.execute_locator(locator)
print(elements)
```

### Пример: Получение HTML из URL

```python
parser = BS()
parser.get_url('https://example.com')
locator = SimpleNamespace(by='CSS', attribute='class_name', selector='//*[contains(@class, "class_name")]')
elements = parser.execute_locator(locator)
print(elements)
```

## Журналирование и отладка

Парсер `BS` использует `logger` из `src.logger` для регистрации ошибок, предупреждений и общей информации. Все проблемы, возникшие при инициализации, конфигурации или выполнении, будут зарегистрированы для удобства отладки.

### Пример журналов

- **Ошибка при инициализации**: `Error initializing BS parser: <error details>`
- **Проблемы с конфигурацией**: `Error in bs.json file: <issue details>`

## Лицензия

Этот проект лицензирован по лицензии MIT. См. файл [LICENSE](../../LICENSE) для получения подробной информации.