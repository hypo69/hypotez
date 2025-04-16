### Анализ кода модуля `src/webdriver/firefox/firefox.py`

## Обзор

Этот модуль предоставляет пользовательскую реализацию Firefox WebDriver на основе Selenium, упрощая его настройку и использование.

## Подробней

Модуль `src/webdriver/firefox/firefox.py` определяет класс `Firefox`, который является расширением стандартного `selenium.webdriver.Firefox` и предназначен для упрощения настройки и управления Firefox WebDriver. Он интегрирует конфигурацию из файла `firefox.json`, предоставляет возможность установки пользовательского профиля, управления режимом окна и настройки прокси. Модуль также использует другие модули проекта `hypotez` для выполнения JavaScript-кода и взаимодействия с элементами на странице.

## Классы

### `Config`

**Описание**: Внутренний класс для загрузки и хранения конфигурации Firefox WebDriver из JSON-файла.

**Атрибуты**:

-   `geckodriver_path` (str): Путь к исполняемому файлу GeckoDriver.
-   `firefox_binary_path` (str): Путь к бинарному файлу Firefox.
-   `profile_directory_default` (str): Значение по умолчанию для директории профиля.
-   `profile_directory_os` (str): Путь к директории профиля в операционной системе.
-   `profile_directory_internal` (str): Внутренний путь к директории профиля.
-   `options` (List[str]): Список опций для запуска Firefox.
-   `headers` (Dict[str, Any]): HTTP-заголовки, используемые в запросах браузера.
-   `proxy_enabled` (bool): Указывает, включен ли прокси.

**Методы**:

-   `__init__(self, config_path: Path)`: Инициализирует объект `Config`, загружая настройки из JSON-файла.

#### `__init__`

**Назначение**: Инициализирует объект `Config`, загружая настройки из JSON-файла.

```python
def __init__(self, config_path: Path):
    """
    Initializes the Config object by loading settings from a JSON file.

    Args:
        config_path: Path to the JSON configuration file.
    """
    ...
```

**Параметры**:

-   `config_path` (Path): Путь к JSON-файлу конфигурации.

**Как работает функция**:

1.  Загружает JSON-файл конфигурации, используя функцию `j_loads_ns`.
2.  Извлекает значения различных параметров конфигурации и сохраняет их в атрибутах объекта `Config`.

### `Firefox`

**Описание**: Пользовательская реализация Firefox WebDriver, расширяющая возможности стандартного `selenium.webdriver.Firefox`.

**Наследует**:

-   `selenium.webdriver.Firefox`

**Атрибуты**:

-   `driver_name` (str): Имя драйвера ("firefox").

**Методы**:

-   `__init__(self, profile_name: Optional[str] = None, chromedriver_version: Optional[str] = None, firefox_version: Optional[str] = None, user_agent: Optional[str] = None, proxy_file_path: Optional[str] = None, options: Optional[List[str]] = None, window_mode: Optional[str] = None, *args, **kwargs) -> None`: Инициализирует экземпляр класса `Firefox` с указанными параметрами.
-   `set_proxy(self, options: Options) -> None`: Настраивает прокси из словаря, возвращаемого `get_proxies_dict`.
-   `_payload(self) -> None`: Загружает исполнителей для локаторов и JavaScript сценариев.

#### `__init__`

**Назначение**: Инициализирует экземпляр класса `Firefox`.

```python
def __init__(
        self,
        profile_name: Optional[str] = None,
        geckodriver_version: Optional[str] = None,
        firefox_version: Optional[str] = None,
        user_agent: Optional[str] = None,
        proxy_file_path: Optional[str] = None,
        options: Optional[List[str]] = None,
        window_mode: Optional[str] = None,
        *args,
        **kwargs,
    ) -> None:
    """Initializes the Firefox WebDriver with custom settings."""
    ...
```

**Параметры**:

-   `profile_name` (Optional[str]): Имя пользовательского профиля Firefox.
-   `geckodriver_version` (Optional[str]): Версия GeckoDriver (не используется в коде).
-   `firefox_version` (Optional[str]): Версия Firefox (не используется в коде).
-   `user_agent` (Optional[str]): Пользовательский агент в формате строки. Если `None`, будет сгенерирован случайный User-Agent.
-   `proxy_file_path` (Optional[str]): Путь к файлу с прокси (не используется в коде).
-   `options` (Optional[List[str]]): Список опций для Firefox.
-   `window_mode` (Optional[str]): Режим окна браузера (`windowless`, `kiosk`, `full_window` и т.д.).
-   `*args`: Произвольные позиционные аргументы, передаваемые в конструктор базового класса.
-   `**kwargs`: Произвольные именованные аргументы, передаваемые в конструктор базового класса.

**Как работает функция**:

1.  Загружает конфигурацию Firefox из файла `firefox.json`, используя внутренний класс `Config`.
2.  Инициализирует объект `Service` для управления процессом GeckoDriver.
3.  Создает объект `Options` для настройки Firefox.
4.  Добавляет опции из файла конфигурации и переданных аргументов.
5.  Устанавливает режим окна браузера (kiosk, windowless, full\_window).
6.  Устанавливает пользовательский агент, используя `fake_useragent` для генерации случайного агента, если не указан.
7.  Настраивает прокси, если они включены в конфигурации, вызывая метод `set_proxy`.
8.  Настраивает директорию профиля пользователя.
9.  Создает экземпляр `Firefox WebDriver` с указанными настройками.
10. Вызывает функцию `_payload` для загрузки исполнителей для локаторов и JavaScript сценариев.
11. Логирует информацию о процессе запуска и обрабатывает возможные исключения.

#### `set_proxy`

**Назначение**: Настраивает прокси из словаря, возвращаемого `get_proxies_dict`.

```python
def set_proxy(self, options: Options) -> None:
    """
    Настройка прокси из словаря, возвращаемого get_proxies_dict.

    :param options: Опции Chrome, в которые добавляются настройки прокси.
    :type options: Options
    """
    ...
```

**Параметры**:

-   `options` (Options): Опции Firefox, в которые добавляются настройки прокси.

**Как работает функция**:

1.  Получает словарь прокси-серверов, используя функцию `get_proxies_dict`.
2.  Создает список всех прокси-серверов (SOCKS4 и SOCKS5).
3.  Перебирает прокси-серверы в случайном порядке, чтобы найти рабочий прокси.
4.  Если рабочий прокси найден, устанавливает параметры прокси для Firefox, добавляя соответствующие настройки в объект `options`.
5.  Логирует информацию о настройке прокси или отсутствии доступных прокси-серверов.

#### `_payload`

**Назначение**: Загружает исполнителей для локаторов и JavaScript сценариев.

```python
def _payload(self) -> None:
    """
    Load executors for locators and JavaScript scenarios.
    """
    ...
```

**Как работает функция**:

1.  Создает экземпляр класса `JavaScript`, передавая ему экземпляр веб-драйвера.
2.  Назначает методы из экземпляра `JavaScript` (например, `get_page_lang`, `ready_state`, `unhide_DOM_element`) атрибутам текущего объекта `Firefox`.
3.  Создает экземпляр класса `ExecuteLocator`, передавая ему экземпляр веб-драйвера.
4.  Назначает методы из экземпляра `ExecuteLocator` (например, `execute_locator`, `get_webelement_as_screenshot`, `send_message`) атрибутам текущего объекта `Firefox`.

## Переменные модуля

-   `driver_name` (str): Имя драйвера ("firefox").

## Пример использования

**Создание экземпляра Firefox WebDriver с настройками по умолчанию:**

```python
from src.webdriver.firefox import Firefox

driver = Firefox()
driver.get("https://www.example.com")
driver.quit()
```

**Создание экземпляра Firefox WebDriver с пользовательским профилем и User-Agent:**

```python
from src.webdriver.firefox import Firefox

driver = Firefox(profile_name="my_profile", user_agent="My Custom Agent")
driver.get("https://www.example.com")
driver.quit()
```

## Взаимосвязь с другими частями проекта

-   Модуль `src/webdriver/firefox/firefox.py` зависит от библиотеки `selenium` для управления браузером Firefox, от модуля `src.webdriver.executor` для выполнения действий с веб-элементами, от модуля `src.webdriver.js` для выполнения JavaScript-кода, от модуля `fake_useragent` для генерации случайных User-Agent, от модуля `src.logger.logger` для логирования и от модуля `src.utils.jjson` для загрузки конфигурации.
-    Он также зависит от `src.webdriver.proxy` для настройки прокси.
-   Он предоставляет класс `Firefox`, который используется в других модулях для создания и управления веб-драйвером Firefox.