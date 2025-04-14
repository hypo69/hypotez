# Модуль для работы с WebDriver Chrome

## Обзор

Модуль `chrome.py` предназначен для управления браузером Google Chrome с использованием Selenium WebDriver. Он предоставляет класс `Chrome`, который расширяет функциональность стандартного `webdriver.Chrome`, добавляя возможности управления профилем, пользовательским агентом, прокси и другими параметрами запуска браузера.

## Подробнее

Модуль содержит класс `Chrome`, который наследуется от `selenium.webdriver.Chrome` и предоставляет дополнительные методы для настройки и управления Chrome WebDriver. Он позволяет задавать пользовательский профиль, версию chromedriver, user-agent, прокси, опции запуска и режим окна браузера. Класс также включает методы для установки прокси и загрузки исполнителей для локаторов и JavaScript-сценариев.

## Классы

### `Chrome`

**Описание**: Класс `Chrome` расширяет функциональность `webdriver.Chrome` для упрощения настройки и управления браузером Chrome.

**Наследует**: `selenium.webdriver.Chrome`

**Атрибуты**:
- `driver_name` (str): Имя драйвера (`'chrome'`).

**Методы**:
- `__init__`: Инициализирует экземпляр класса `Chrome`, настраивает параметры запуска браузера.
- `set_proxy`: Настраивает прокси для Chrome на основе предоставленных данных.
- `_payload`: Загружает исполнителей для локаторов и JavaScript-сценариев.

#### `__init__`

```python
def __init__(self, profile_name: Optional[str] = None,
             chromedriver_version: Optional[str] = None,
             user_agent: Optional[str] = None,
             proxy_file_path: Optional[str] = None,
             options: Optional[List[str]] = None,
             window_mode: Optional[str] = None,
             *args, **kwargs) -> None:
    """
    Инициализирует экземпляр класса `Chrome`, настраивая параметры запуска браузера.

    Args:
        profile_name (Optional[str], optional): Имя пользовательского профиля Chrome. По умолчанию `None`.
        chromedriver_version (Optional[str], optional): Версия ChromeDriver. По умолчанию `None`.
        user_agent (Optional[str], optional): Пользовательский агент. По умолчанию `None`.
        proxy_file_path (Optional[str], optional): Путь к файлу с прокси. По умолчанию `None`.
        options (Optional[List[str]], optional): Список опций для Chrome. По умолчанию `None`.
        window_mode (Optional[str], optional): Режим окна браузера. По умолчанию `None`.

    Raises:
        WebDriverException: Если не удается запустить WebDriver.
        Exception: При возникновении других ошибок во время работы Chrome WebDriver.
    """
```

**Как работает функция**:
- Функция инициализирует класс `Chrome`, загружает конфигурацию из файла `chrome.json`, устанавливает путь к `chromedriver`, настраивает опции Chrome, устанавливает пользовательский профиль, `user-agent` и прокси, а затем запускает Chrome WebDriver.
- В случае возникновения исключений, таких как `WebDriverException` или `Exception`, функция логирует соответствующие ошибки и возвращает управление.

**Примеры**:

```python
driver = Chrome(window_mode='full_window')
driver = Chrome(profile_name='my_profile', user_agent='Mozilla/5.0')
```

#### `set_proxy`

```python
def set_proxy(self, options: Options) -> None:
    """
    Настраивает прокси для Chrome на основе предоставленных данных.

    Args:
        options (Options): Опции Chrome, в которые добавляются настройки прокси.
    """
```

**Как работает функция**:
- Функция `set_proxy` настраивает прокси для Chrome, получая данные из словаря прокси, созданного функцией `get_proxies_dict`. Она перебирает доступные прокси, проверяет их работоспособность и, если находит рабочий прокси, устанавливает его в опции Chrome в зависимости от протокола (`http`, `socks4`, `socks5`).
- Если рабочий прокси не найден, функция регистрирует предупреждение в лог.

**Примеры**:

```python
options = Options()
chrome_instance = Chrome()
chrome_instance.set_proxy(options)
```

#### `_payload`

```python
def _payload(self) -> None:
    """
    Загружает исполнителей для локаторов и JavaScript-сценариев.
    """
```

**Как работает функция**:
- Функция `_payload` загружает исполнителей для локаторов и JavaScript-сценариев.
- Она инициализирует класс `JavaScript` и присваивает его методы текущему экземпляру класса.
- Также создает экземпляр класса `ExecuteLocator` и присваивает его методы текущему экземпляру класса.

**Примеры**:

```python
chrome_instance = Chrome()
chrome_instance._payload()
```

## Параметры класса

- `profile_name` (Optional[str]): Имя пользовательского профиля Chrome.
- `chromedriver_version` (Optional[str]): Версия ChromeDriver.
- `user_agent` (Optional[str]): Пользовательский агент.
- `proxy_file_path` (Optional[str]): Путь к файлу с прокси.
- `options` (Optional[List[str]]): Список опций для Chrome.
- `window_mode` (Optional[str]): Режим окна браузера (`windowless`, `kiosk`, `full_window` и т.д.).

## Методы класса

### `set_proxy`

```python
def set_proxy(self, options: Options) -> None:
    """
    Настройка прокси из словаря, возвращаемого get_proxies_dict.

    Args:
        options (Options): Опции Chrome, в которые добавляются настройки прокси.
    """
```

**Параметры**:
- `options` (Options): Опции Chrome, в которые добавляются настройки прокси.

### `_payload`

```python
def _payload(self) -> None:
    """
    Загружает исполнителей для локаторов и JavaScript сценариев.
    """
```

## Примеры

Примеры создания и использования экземпляра класса `Chrome`:

```python
from src.webdriver.chrome.chrome import Chrome

# Создание экземпляра Chrome с настройками по умолчанию
driver = Chrome()

# Создание экземпляра Chrome с указанием режима окна
driver = Chrome(window_mode='full_window')

# Создание экземпляра Chrome с указанием пользовательского профиля и user-agent
driver = Chrome(profile_name='my_profile', user_agent='Mozilla/5.0')
```