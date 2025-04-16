### Анализ кода модуля `hypotez/src/webdriver/firefox/firefox.py`

```rst
.. module:: src.webdriver.firefox
```

# Модуль Firefox WebDriver для Selenium

Этот модуль предоставляет кастомную реализацию Firefox WebDriver с использованием Selenium. Он интегрирует настройки конфигурации, определённые в файле `firefox.json`, такие как user-agent и настройки профиля браузера, чтобы обеспечить гибкие и автоматизированные взаимодействия с браузером.

## Описание

Модуль предназначен для упрощения и стандартизации работы с Firefox WebDriver в проекте `hypotez`.

## Ключевые особенности

*   **Централизованная конфигурация**: Все основные настройки драйвера хранятся в файле `firefox.json`.
*   **Поддержка профилей**: Возможность указать имя профиля Firefox для использования.
*   **Управление User-Agent**:  Поддержка установки пользовательского User-Agent, в том числе генерация случайного User-Agent.
*   **Управление опциями Firefox**:  Возможность передачи дополнительных опций командной строки в Firefox.
*   **Поддержка прокси**: Настройка прокси-сервера для обхода ограничений.
*   **Режимы окна**: Поддержка различных режимов окна браузера (например, `windowless`, `kiosk`, `full_window`).

## Классы

### `Config`

```python
class Config:
    """Configuration class for Firefox WebDriver."""

    def __init__(self, config_path: Path):
        """
        Initializes the Config object by loading settings from a JSON file.

        Args:
            config_path: Path to the JSON configuration file.
        """
        self._config = j_loads_ns(config_path)
        self.geckodriver_path = str(Path(gs.path.root, self._config.executable_path.geckodriver))
        self.firefox_binary_path = str(Path(gs.path.root, self._config.executable_path.firefox_binary))
        self.profile_directory_default = self._config.profile_directory.default
        self.profile_directory_os = self._config.profile_directory.os
        self.profile_directory_internal = self._config.profile_directory.internal
        self.options: List[str] = getattr(self._config, 'options', [])
        self.headers: Dict[str, Any] = vars(getattr(self._config, 'headers', {})) if hasattr(self._config, 'headers') else {}
        self.proxy_enabled: bool = getattr(self._config, 'proxy_enabled', False)
```

**Описание**:
Класс `Config` предназначен для загрузки и хранения конфигурационных параметров для Firefox WebDriver.

**Атрибуты**:
- `_config` (SimpleNamespace): Объект, содержащий загруженную конфигурацию из JSON-файла.
- `geckodriver_path` (str): Путь к исполняемому файлу GeckoDriver.
- `firefox_binary_path` (str): Путь к бинарному файлу Firefox.
- `profile_directory_default` (str): Значение по умолчанию для директории профиля.
- `profile_directory_os` (str): Путь к директории профиля для операционной системы.
- `profile_directory_internal` (str): Внутренний путь к директории профиля.
- `options` (List[str]): Список опций Firefox.
- `headers` (Dict[str, Any]): Словарь HTTP-заголовков.
- `proxy_enabled` (bool): Указывает, включен ли прокси-сервер.

**Методы**:
- `__init__(self, config_path: Path)`: Инициализирует объект `Config`, загружая настройки из JSON-файла.

### `Firefox`

```python
class Firefox(WebDriver):
    """
    Extends `webdriver.Firefox` with enhanced capabilities.

    Features:
        - Custom Firefox profile support.
        - Kiosk and other window modes.
        - User-agent customization.
        - Proxy settings.

    Args:
        profile_name: Name of the Firefox profile to use. Defaults to None.
        geckodriver_version: GeckoDriver version. Defaults to None.
        firefox_version: Firefox version. Defaults to None.
        user_agent: User agent string. If None, a random user agent is used. Defaults to None.
        proxy_file_path: Path to the proxy file. Defaults to None.
        options: List of Firefox options. Defaults to None.
        window_mode: Browser window mode (e.g., "windowless", "kiosk"). Defaults to None.

    Raises:
        WebDriverException: If the WebDriver fails to start.
        Exception: For other unexpected errors during initialization.
    """

    driver_name = "firefox"

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
        logger.info("Starting Firefox WebDriver")

        config = Config(Path(gs.path.src, "webdriver", "firefox", "firefox.json"))

        service = Service(executable_path=config.geckodriver_path)
        options_obj = Options()

        # Load options from config file
        if config.options:
            for option in config.options:
                options_obj.add_argument(option)

        # Set window mode
        if window_mode:
            options_obj.add_argument(f"--{window_mode}")

        # Add options from constructor
        if options:
            for option in options:
                options_obj.add_argument(option)

        # Add headers from config
        if config.headers:
            for key, value in config.headers.items():
                options_obj.add_argument(f"--{key}={value}")

        # Set user agent
        user_agent = user_agent or UserAgent().random
        options_obj.set_preference("general.useragent.override", user_agent)

        # Set proxy if enabled
        if config.proxy_enabled:
            self.set_proxy(options_obj)

        # Configure profile directory
        profile_directory = (
            config.profile_directory_os
            if config.profile_directory_default == "os"
            else str(Path(gs.path.src, config.profile_directory_internal))
        )

        if profile_name:
            profile_directory = str(Path(profile_directory).parent / profile_name)
        if "%LOCALAPPDATA%" in profile_directory:
            profile_directory = Path(
                profile_directory.replace("%LOCALAPPDATA%", os.environ.get("LOCALAPPDATA"))
            )

        # profile = FirefoxProfile(profile_directory=profile_directory) #  <- @debug не грузится профиль

        try:
            super().__init__(service=service, options=options_obj)
            self._payload()
            logger.success(f"Browser started successfully, {window_mode=}")
        except WebDriverException as ex:
            logger.critical(
                """
                ---------------------------------
                    Error starting WebDriver
                    Possible reasons:
                    - Firefox update
                    - Firefox not installed

                    Перезапусти код.
                ----------------------------------
                """,
                ex,
                False
            )
            sys.exit(1)
        except Exception as ex:
            logger.critical("Firefox WebDriver error:", ex, False)

            return
```

**Описание**:
Класс `Firefox` является расширением для `webdriver.Firefox` и предоставляет дополнительные возможности для управления браузером Firefox.

**Наследует**:
- `WebDriver` (из `selenium.webdriver`)

**Атрибуты**:
- `driver_name` (str): Имя драйвера (`'firefox'`).

**Параметры**:

*   `profile_name` (Optional[str], optional): Имя профиля Firefox.
*   `chromedriver_version` (Optional[str], optional): Версия GeckoDriver.
*   `firefox_version` (Optional[str], optional): Версия Firefox.
*   `user_agent` (Optional[str], optional): Пользовательский агент.
*   `proxy_file_path` (Optional[str], optional): Путь к файлу с прокси.
*   `options` (Optional[List[str]]): Дополнительные опции для Firefox.
*   `window_mode` (Optional[str]): Режим отображения окна (например, "windowless", "kiosk", "full_window").
*   `*args`: Дополнительные позиционные аргументы, передаваемые в конструктор базового класса.
*   `**kwargs`: Дополнительные именованные аргументы, передаваемые в конструктор базового класса.

**Методы**:

*   `__init__(self, profile_name: Optional[str] = None, chromedriver_version: Optional[str] = None, firefox_version: Optional[str] = None, user_agent: Optional[str] = None, proxy_file_path: Optional[str] = None, options: Optional[List[str]] = None, window_mode: Optional[str] = None, *args, **kwargs) -> None`: Инициализирует экземпляр класса `Firefox`.
*   `set_proxy(self, options: Options) -> None`: Настраивает прокси из словаря, возвращаемого `get_proxies_dict`.
*   `_payload(self) -> None`: Загружает исполнителей для локаторов и JavaScript сценариев.
*   `set_options(self, opts: Optional[List[str]] = None) -> Options`: Создает и настраивает параметры запуска для Firefox WebDriver.

## Методы класса

### `__init__`

```python
def __init__(self, profile_name: Optional[str] = None,
                 chromedriver_version: Optional[str] = None,
                 user_agent: Optional[str] = None,
                 proxy_file_path: Optional[str] = None,
                 options: Optional[List[str]] = None,
                 window_mode: Optional[str] = None,
                 *args, **kwargs) -> None:
    #  объявление переменных
    service = None
    options_obj = None
```

**Назначение**:
Инициализирует экземпляр класса Chrome.

**Параметры**:

*   `profile_name` (Optional[str]): Имя профиля.
*   `chromedriver_version` (Optional[str]): Версия GeckoDriver.
*   `firefox_version` (Optional[str]): Версия Firefox.
*   `user_agent` (Optional[str]): Строка User-Agent.
*   `proxy_file_path` (Optional[str]): Путь к файлу с прокси.
*   `options` (Optional[List[str]]): Дополнительные опции для Firefox.
*   `window_mode` (Optional[str]): Режим отображения окна (например, "kiosk", "windowless", "full_window").
*   `*args`: Дополнительные позиционные аргументы, передаваемые в конструктор базового класса.
*   `**kwargs`: Дополнительные именованные аргументы, передаваемые в конструктор базового класса.

**Как работает функция**:

1.  Загружает конфигурацию из файла `firefox.json`.
2.  Инициализирует объект `Options` для настройки Firefox.
3.  Добавляет пользовательский user-agent и другие параметры.
4.  Создает сервис Firefox с указанным путем к драйверу.
5.  Вызывает конструктор базового класса `WebDriver` с настроенными опциями и сервисом.

### `set_proxy`

```python
def set_proxy(self, options: Options) -> None:
    """Configures proxy settings from a dictionary.

    Args:
        options: Firefox options to add proxy settings to.
    """
    ...
```

**Назначение**:
Настраивает прокси из словаря, возвращаемого `get_proxies_dict`.

**Параметры**:
-   `options` (Options): Объект `Options`, к которому применяются настройки прокси.

**Как работает функция**:
1.  Получает словарь прокси-серверов, используя `get_proxies_dict()`.
2.  Проверяет, есть ли рабочие прокси и настраивает их, если они найдены.
3. Логирует параметры установленного прокси

### `_payload`

```python
def _payload(self) -> None:
    """
    Load executors for locators and JavaScript scenarios.
    """
    ...
```

**Назначение**:
Загружает исполнителей для локаторов и JavaScript сценариев.

**Как работает функция**:

1.  Создает экземпляр класса `JavaScript` и назначает его методы для управления веб-страницей.
2.  Создает экземпляр класса `ExecuteLocator` и назначает его методы для выполнения локаторов.

### `set_options`

```python
def set_options(self, opts: Optional[List[str]] = None) -> EdgeOptions:  
    """  
    Create and configure launch options for the Edge WebDriver.  

    :param opts: A list of options to add to the Edge WebDriver. Defaults to `None`.  
    :return: Configured `EdgeOptions` object.  
    """
    ...
```

**Назначение**:
Создает и настраивает параметры запуска для Firefox WebDriver.

**Параметры**:
-   `opts` (Optional[List[str]]): Список опций для добавления в Firefox WebDriver. По умолчанию None.

**Возвращает**:
-   `Options`: Настроенный объект `Options`.

**Как работает функция**:
1.  Создает объект `Options`.
2.  Если передан список опций, добавляет их к объекту `Options`.
3.  Возвращает настроенный объект `Options`.

## Переменные

-   `driver_name: str = 'firefox'` - имя драйвера

## Запуск

Для использования этого модуля необходимо установить библиотеку `selenium` и `fake_useragent`.
Также необходимо скачать и указать путь к GeckoDriver.

```bash
pip install selenium fake_useragent
```

Пример использования:

```python
from src.webdriver.firefox import Firefox

driver = Firefox(window_mode='full_window')
driver.get("https://google.com")