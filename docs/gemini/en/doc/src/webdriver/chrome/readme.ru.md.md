# Модуль кастомной реализации Chrome WebDriver для Selenium

## Обзор

Модуль `src.webdriver.chrome` предоставляет кастомную реализацию Chrome WebDriver с использованием Selenium. Он интегрирует настройки конфигурации, определённые в файле `chrome.json`, такие как user-agent и настройки профиля браузера, чтобы обеспечить гибкие и автоматизированные взаимодействия с браузером.

## Детали

Этот модуль создан для управления веб-драйвером Chrome. Он предоставляет возможность настройки различных параметров Chrome, таких как user-agent, опции, профили, пути к бинарникам, заголовки и использование прокси-сервера. 

## Классы

### `Chrome`

**Описание**: Класс `Chrome` представляет собой кастомную реализацию Chrome WebDriver. Он наследует от класса `Driver` и предоставляет возможность инициализировать WebDriver с различными настройками.

**Наследует**: Класс `Driver`

**Атрибуты**:

- `driver` (`webdriver.Chrome`): Экземпляр `webdriver.Chrome` (Selenium).

**Методы**:

- `__init__(self, user_agent: str = None, options: list = None, headless: bool = False, proxy_enabled: bool = False)`: Инициализирует объект `Chrome` с заданными настройками.

    **Параметры**:
    - `user_agent` (`str`, optional): Строка user-agent для Chrome. По умолчанию используется значение из `chrome.json`.
    - `options` (`list`, optional): Список дополнительных опций командной строки для Chrome. По умолчанию используется значение из `chrome.json`.
    - `headless` (`bool`, optional): Флаг, указывающий, должен ли WebDriver работать в безголовом режиме. По умолчанию значение из `chrome.json`.
    - `proxy_enabled` (`bool`, optional): Флаг, указывающий, следует ли использовать прокси-сервер. По умолчанию значение из `chrome.json`.

- `get(self, url: str) -> None`: Открывает веб-страницу по заданному URL.

    **Параметры**:
    - `url` (`str`): URL-адрес веб-страницы.

- `quit(self) -> None`: Закрывает браузер.


## Функции

### `j_loads(path: str | Path, encoding: str = 'utf-8', default: Any = None) -> Any`:

**Цель**: Читает содержимое файла JSON, десериализует его в Python-объект и возвращает результат.

**Параметры**:

- `path` (`str | Path`): Путь к файлу JSON.
- `encoding` (`str`, optional): Кодировка файла. По умолчанию `utf-8`.
- `default` (`Any`, optional): Значение по умолчанию, которое возвращается, если файл не существует или не может быть прочитан. По умолчанию `None`.

**Возвращает**:
- `Any`: Десериализованный Python-объект или значение по умолчанию.

**Пример**:

```python
from pathlib import Path

config_file = Path('config.json')
config = j_loads(config_file)
```

### `j_loads_ns(path: str | Path, namespace: str = '', encoding: str = 'utf-8', default: Any = None) -> Any`:

**Цель**: Читает содержимое файла JSON, десериализует его в Python-объект,  используя заданное пространство имен, и возвращает результат.

**Параметры**:

- `path` (`str | Path`): Путь к файлу JSON.
- `namespace` (`str`, optional): Пространство имен для доступа к данным в файле JSON. По умолчанию `''`.
- `encoding` (`str`, optional): Кодировка файла. По умолчанию `utf-8`.
- `default` (`Any`, optional): Значение по умолчанию, которое возвращается, если файл не существует или не может быть прочитан. По умолчанию `None`.

**Возвращает**:
- `Any`: Десериализованный Python-объект или значение по умолчанию.

**Пример**:

```python
from pathlib import Path

config_file = Path('config.json')
config = j_loads_ns(config_file, namespace='chrome')
```

## Принцип работы

Класс `Chrome` инициализируется с помощью конфигурации из файла `chrome.json`. Он использует `logger` для записи информации о процессе инициализации, конфигурации и работе WebDriver. В случае ошибки инициализации WebDriver, `Chrome` записывает сообщение об ошибке в лог.

## Примеры

```python
from src.webdriver.chrome import Chrome

# Инициализация Chrome WebDriver
browser = Chrome(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)", options=["--headless", "--disable-gpu"])

# Открытие веб-сайта
browser.get("https://www.example.com")

# Закрытие браузера
browser.quit()
```

## Дополнительные сведения

- **Инициализация WebDriver**: При инициализации WebDriver, `Chrome` использует `user_agent` и `options` для настройки поведения браузера.
- **Логирование**: `Chrome` использует `logger` для записи информации о процессе инициализации, конфигурации и работе WebDriver.
- **Паттерн Singleton**: `Chrome` реализует паттерн Singleton, чтобы обеспечить создание только одного экземпляра WebDriver.

## License

Этот проект лицензирован на условиях MIT License — см. файл [LICENSE](../../LICENSE) для подробностей.