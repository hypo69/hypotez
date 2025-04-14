# Модуль WebDriver Firefox

## Обзор

Модуль предоставляет класс `Firefox`, расширяющий стандартный `selenium.webdriver.Firefox` дополнительными функциями, такими как управление пользовательским профилем, режим киоска и настройки прокси.

## Подробнее

Этот модуль предназначен для управления экземплярами браузера Firefox с использованием Selenium WebDriver. Он включает в себя функциональность для настройки профиля Firefox, установки параметров прокси и управления режимом отображения окна браузера.

## Классы

### `Config`

**Описание**: Класс конфигурации для WebDriver Firefox.

**Атрибуты**:
- `geckodriver_path` (str): Путь к исполняемому файлу GeckoDriver.
- `firefox_binary_path` (str): Путь к бинарному файлу Firefox.
- `profile_directory_default` (str): Значение по умолчанию для директории профиля.
- `profile_directory_os` (str): Путь к директории профиля, специфичной для операционной системы.
- `profile_directory_internal` (str): Внутренний путь к директории профиля.
- `options` (List[str]): Список опций Firefox.
- `headers` (Dict[str, Any]): Словарь заголовков для Firefox.
- `proxy_enabled` (bool): Флаг, указывающий, включен ли прокси.

#### `__init__`
```python
def __init__(self, config_path: Path):
    """
    Инициализирует объект Config, загружая настройки из JSON-файла.

    Args:
        config_path: Путь к JSON-файлу конфигурации.
    """
```

**Как работает функция**:

- Функция `__init__` инициализирует объект `Config`, загружая параметры конфигурации из указанного JSON-файла.
- Она извлекает пути к исполняемым файлам `geckodriver` и `firefox_binary`, а также настройки директорий профиля и другие параметры, такие как опции, заголовки и статус прокси.
- Пути к исполняемым файлам и директориям профиля формируются на основе базового пути проекта `gs.path.root` и значений, определенных в файле конфигурации.
- Полученные параметры сохраняются в соответствующих атрибутах объекта `Config` для дальнейшего использования при настройке WebDriver Firefox.

**Примеры**:

```python
from pathlib import Path
from src import gs

# Допустим, что gs.path.root указывает на корень проекта, а файл конфигурации находится по пути "path/to/firefox.json"
config_path = Path(gs.path.root, "path", "to", "firefox.json")
config = Config(config_path)

# Теперь можно получить доступ к параметрам конфигурации через атрибуты объекта config
print(config.geckodriver_path)
print(config.firefox_binary_path)
```

### `Firefox`

**Описание**: Расширяет `webdriver.Firefox` для обеспечения расширенных возможностей.

**Наследует**:
- `webdriver.Firefox`

**Атрибуты**:
- `driver_name` (str): Имя драйвера ("firefox").

#### `__init__`
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
    """Инициализирует Firefox WebDriver с пользовательскими настройками."""
```

**Параметры**:
- `profile_name` (Optional[str]): Имя профиля Firefox для использования. По умолчанию `None`.
- `geckodriver_version` (Optional[str]): Версия GeckoDriver. По умолчанию `None`.
- `firefox_version` (Optional[str]): Версия Firefox. По умолчанию `None`.
- `user_agent` (Optional[str]): Строка user agent. Если `None`, используется случайный user agent. По умолчанию `None`.
- `proxy_file_path` (Optional[str]): Путь к файлу прокси. По умолчанию `None`.
- `options` (Optional[List[str]]): Список опций Firefox. По умолчанию `None`.
- `window_mode` (Optional[str]): Режим окна браузера (например, "windowless", "kiosk"). По умолчанию `None`.

**Как работает класс**:

- Класс `Firefox` инициализирует WebDriver Firefox с настраиваемыми параметрами, такими как профиль, версия, user-agent, прокси и режим окна.
- При инициализации загружается конфигурация из файла `firefox.json`, устанавливаются параметры сервиса и опции Firefox.
- User-agent может быть указан явно или сгенерирован случайным образом.
- Если включен прокси, вызывается метод `set_proxy` для настройки параметров прокси.
- Профиль Firefox настраивается на основе указанного имени профиля и пути к директории профиля.
- В случае возникновения исключений при запуске WebDriver, они логируются, и программа завершается.

**Примеры**:

```python
from src.webdriver.firefox.firefox import Firefox

# Инициализация Firefox с профилем "custom_profile" и режимом киоска
driver = Firefox(profile_name="custom_profile", window_mode="kiosk")
driver.get("https://www.example.com")
driver.quit()

# Инициализация Firefox со случайным user-agent и списком опций
options = ["--disable-gpu", "--disable-extensions"]
driver = Firefox(user_agent=None, options=options)
driver.get("https://www.example.com")
driver.quit()
```

#### `set_proxy`
```python
def set_proxy(self, options: Options) -> None:
    """Настраивает параметры прокси из словаря.

    Args:
        options: Опции Firefox для добавления настроек прокси.
    """
```

**Как работает функция**:

- Метод `set_proxy` настраивает параметры прокси для Firefox на основе данных из словаря прокси.
- Он получает список прокси из файла, выбирает случайный рабочий прокси и устанавливает соответствующие параметры в опциях Firefox.
- Поддерживаются протоколы HTTP, SOCKS4 и SOCKS5.
- Если рабочий прокси не найден, выводится предупреждение в лог.

**Примеры**:

```python
from selenium.webdriver.firefox.options import Options
from src.webdriver.firefox.firefox import Firefox

# Создание инстанса Firefox
driver = Firefox()
options = Options()
driver.set_proxy(options)  # Настройка прокси
driver.get("https://www.example.com")
driver.quit()
```

#### `_payload`
```python
def _payload(self) -> None:
    """Загружает исполнителей для локаторов и JavaScript-скриптов."""
```

**Как работает функция**:

- Метод `_payload` загружает исполнителей для локаторов и JavaScript-скриптов, чтобы расширить возможности WebDriver.
- Он инициализирует класс `JavaScript` и присваивает его методы текущему экземпляру класса `Firefox`.
- Затем он инициализирует класс `ExecuteLocator` и присваивает его методы, связанные с выполнением локаторов и получением информации об элементах веб-страницы, текущему экземпляру класса `Firefox`.
- Это позволяет использовать методы `JavaScript` и `ExecuteLocator` непосредственно через экземпляр `Firefox`.

**Примеры**:

```python
from src.webdriver.firefox.firefox import Firefox

# Создание инстанса Firefox
driver = Firefox()
driver._payload()  # Загрузка исполнителей

# Теперь можно использовать методы JavaScript и ExecuteLocator
page_lang = driver.get_page_lang()
element = driver.execute_locator({"by": "id", "selector": "some_id"})
```

## Примеры

```python
if __name__ == "__main__":
    driver = Firefox()
    driver.get("https://google.com")