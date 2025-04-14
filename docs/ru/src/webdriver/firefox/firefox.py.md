# Модуль webdriver для Firefox

## Обзор

Модуль `firefox.py` предоставляет класс `Firefox`, расширяющий стандартный `selenium.webdriver.Firefox`.
Он добавляет такие функции, как управление пользовательским профилем, режим киоска и настройки прокси.

## Подробней

Этот модуль позволяет запускать браузер Firefox с различными настройками, такими как пользовательский профиль, режим киоска, пользовательский агент и прокси. Он использует библиотеку `selenium` для управления браузером и `fake_useragent` для генерации случайных пользовательских агентов. Модуль также содержит класс `Config`, который загружает настройки из JSON-файла.

## Классы

### `Config`

**Описание**: Класс конфигурации для Firefox WebDriver.

**Принцип работы**:
Класс `Config` предназначен для загрузки и хранения конфигурационных параметров, необходимых для инициализации и настройки Firefox WebDriver. Он читает данные из JSON-файла, указанного в `config_path`, и предоставляет атрибуты для доступа к различным параметрам, таким как пути к исполняемым файлам (geckodriver и firefox), настройки профиля, опции командной строки, заголовки и настройки прокси.

**Аттрибуты**:

- `config_path` (Path): Путь к JSON-файлу конфигурации.
- `_config` (dict): Словарь, содержащий загруженные конфигурационные данные.
- `geckodriver_path` (str): Путь к исполняемому файлу geckodriver.
- `firefox_binary_path` (str): Путь к исполняемому файлу Firefox.
- `profile_directory_default` (str): Значение по умолчанию для директории профиля.
- `profile_directory_os` (str): Путь к директории профиля, специфичной для операционной системы.
- `profile_directory_internal` (str): Внутренний путь к директории профиля.
- `options` (List[str]): Список опций командной строки для Firefox.
- `headers` (Dict[str, Any]): Словарь HTTP-заголовков, которые будут добавлены в запросы.
- `proxy_enabled` (bool): Флаг, указывающий, включено ли использование прокси.

**Методы**:

- `__init__(self, config_path: Path)`: Инициализирует объект `Config`, загружая настройки из JSON-файла.

### `Firefox`

**Описание**: Расширяет `webdriver.Firefox` с расширенными возможностями.

**Принцип работы**:
Класс `Firefox` наследуется от `selenium.webdriver.Firefox` и предоставляет расширенные возможности для управления браузером Firefox. Он позволяет настраивать профиль Firefox, устанавливать режим окна (например, "kiosk" или "windowless"), изменять User-Agent, использовать прокси и выполнять JavaScript-скрипты. При инициализации класса загружаются настройки из файла `firefox.json`, создается объект `Service` для управления geckodriver, настраиваются опции Firefox и устанавливается прокси, если это необходимо.

**Аттрибуты**:
- `driver_name` (str): Имя драйвера ("firefox").

**Методы**:
- `__init__(self, profile_name: Optional[str] = None, geckodriver_version: Optional[str] = None, firefox_version: Optional[str] = None, user_agent: Optional[str] = None, proxy_file_path: Optional[str] = None, options: Optional[List[str]] = None, window_mode: Optional[str] = None, *args, **kwargs) -> None`: Инициализирует драйвер Firefox с заданными настройками.
- `set_proxy(self, options: Options) -> None`: Настраивает параметры прокси из словаря.
- `_payload(self) -> None`: Загружает исполнителей для локаторов и скриптов JavaScript.

## Функции

### `Config.__init__`

```python
def __init__(self, config_path: Path):
    """
    Initializes the Config object by loading settings from a JSON file.

    Args:
        config_path: Path to the JSON configuration file.
    """
```

**Назначение**:
Инициализирует объект `Config`, загружая настройки из указанного JSON-файла.

**Параметры**:
- `config_path` (Path): Путь к JSON-файлу конфигурации.

**Возвращает**:
- `None`

**Вызывает исключения**:
- Отсутствуют явные указания на исключения.

**Как работает функция**:

1.  **Загрузка конфигурации**: Функция загружает конфигурацию из JSON-файла, используя `j_loads_ns(config_path)`. Этот метод предполагает чтение и парсинг JSON-файла.
2.  **Извлечение путей к исполняемым файлам**: Извлекаются пути к исполняемым файлам `geckodriver` и `firefox` из загруженной конфигурации. Пути формируются на основе базового пути проекта (`gs.path.root`) и соответствующих настроек в конфигурации.
3.  **Извлечение настроек директории профиля**: Извлекаются настройки, связанные с директориями профилей, включая директорию по умолчанию, специфичную для ОС и внутреннюю директорию.
4.  **Извлечение опций и заголовков**: Опции командной строки и HTTP-заголовки извлекаются из конфигурации. Если заголовки существуют, они преобразуются в словарь.
5.  **Извлечение флага прокси**: Извлекается флаг, указывающий, включено ли использование прокси.

**ASCII Flowchart**:

```
     A Загрузка конфигурации из JSON
     |
     B Извлечение путей к исполняемым файлам (geckodriver, firefox)
     |
     C Извлечение настроек директории профиля
     |
     D Извлечение опций и заголовков
     |
     E Извлечение флага прокси
```

**Примеры**:

```python
from pathlib import Path
from src import gs
config_path = Path(gs.path.src, "webdriver", "firefox", "firefox.json")
config = Config(config_path)
print(config.geckodriver_path)
```

### `Firefox.__init__`

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
```

**Назначение**:
Инициализирует драйвер Firefox с пользовательскими настройками, такими как профиль, User-Agent, прокси и другие опции.

**Параметры**:
- `profile_name` (Optional[str]): Имя профиля Firefox для использования. По умолчанию `None`.
- `geckodriver_version` (Optional[str]): Версия GeckoDriver. По умолчанию `None`.
- `firefox_version` (Optional[str]): Версия Firefox. По умолчанию `None`.
- `user_agent` (Optional[str]): Строка User-Agent. Если `None`, используется случайный User-Agent. По умолчанию `None`.
- `proxy_file_path` (Optional[str]): Путь к файлу прокси. По умолчанию `None`.
- `options` (Optional[List[str]]): Список опций Firefox. По умолчанию `None`.
- `window_mode` (Optional[str]): Режим окна браузера (например, "windowless", "kiosk"). По умолчанию `None`.
- `*args`: Произвольные позиционные аргументы.
- `**kwargs`: Произвольные именованные аргументы.

**Возвращает**:
- `None`

**Вызывает исключения**:
- `WebDriverException`: Если не удается запустить WebDriver.
- `Exception`: Для других неожиданных ошибок во время инициализации.

**Как работает функция**:

1.  **Инициализация конфигурации**: Создается экземпляр класса `Config` для загрузки настроек из файла `firefox.json`.
2.  **Создание сервиса GeckoDriver**: Создается объект `Service` для управления процессом GeckoDriver, используя путь к исполняемому файлу, полученный из конфигурации.
3.  **Создание объекта Options**: Создается объект `Options` для настройки параметров Firefox.
4.  **Загрузка опций из конфигурационного файла**: Опции, указанные в конфигурационном файле, добавляются в объект `Options`.
5.  **Установка режима окна**: Если указан режим окна (`window_mode`), он добавляется в опции Firefox.
6.  **Добавление опций из конструктора**: Опции, переданные в конструктор, добавляются в объект `Options`.
7.  **Добавление заголовков из конфигурации**: Заголовки, указанные в конфигурационном файле, добавляются в опции Firefox.
8.  **Установка User-Agent**: Если User-Agent не указан, генерируется случайный User-Agent с использованием библиотеки `fake_useragent`.
9.  **Установка прокси**: Если включена опция `proxy_enabled` в конфигурации, вызывается метод `set_proxy` для настройки прокси.
10. **Конфигурация директории профиля**: Определяется директория профиля Firefox на основе настроек в конфигурации и имени профиля, переданного в конструктор.
11. **Инициализация WebDriver**: Вызывается конструктор базового класса `WebDriver` с настроенными опциями и сервисом.
12. **Загрузка исполнителей**: Вызывается метод `_payload` для загрузки исполнителей локаторов и JavaScript-скриптов.
13. **Обработка исключений**:
    *   Если возникает исключение `WebDriverException` (например, если не удается запустить GeckoDriver), регистрируется критическая ошибка и программа завершается.
    *   Если возникает другое исключение, регистрируется критическая ошибка.

**ASCII Flowchart**:

```
     A Инициализация конфигурации
     |
     B Создание сервиса GeckoDriver
     |
     C Создание объекта Options
     |
     D Загрузка опций из конфигурационного файла
     |
     E Установка режима окна
     |
     F Добавление опций из конструктора
     |
     G Добавление заголовков из конфигурации
     |
     H Установка User-Agent
     |
     I Установка прокси
     |
     J Конфигурация директории профиля
     |
     K Инициализация WebDriver
     |
     L Загрузка исполнителей
     |
     M Обработка исключений
```

**Примеры**:

```python
from src.webdriver.firefox.firefox import Firefox

# Запуск Firefox с профилем "my_profile" в режиме киоска
driver = Firefox(profile_name="my_profile", window_mode="kiosk")
driver.get("https://www.example.com")
driver.quit()

# Запуск Firefox с пользовательским User-Agent
driver = Firefox(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver.get("https://www.example.com")
driver.quit()
```

### `Firefox.set_proxy`

```python
def set_proxy(self, options: Options) -> None:
    """Configures proxy settings from a dictionary.

    Args:
        options: Firefox options to add proxy settings to.
    """
```

**Назначение**:
Настраивает параметры прокси на основе словаря прокси.

**Параметры**:
- `options` (Options): Объект опций Firefox, к которому будут добавлены настройки прокси.

**Возвращает**:
- `None`

**Вызывает исключения**:
- Отсутствуют явные указания на исключения.

**Как работает функция**:

1.  **Получение списка прокси**: Функция получает словарь прокси, вызывая `get_proxies_dict()`.
2.  **Объединение прокси**: Функция объединяет списки прокси SOCKS4 и SOCKS5 из полученного словаря.
3.  **Выбор рабочего прокси**: Функция случайным образом выбирает прокси из объединенного списка и проверяет его работоспособность с помощью `check_proxy(proxy)`. Если рабочий прокси найден, он используется; в противном случае, функция продолжает итерации, пока не переберет все прокси.
4.  **Установка параметров прокси**: Если рабочий прокси найден, функция устанавливает параметры прокси в объект `options` в зависимости от протокола прокси (HTTP, SOCKS4 или SOCKS5). Используются методы `options.set_preference` для установки соответствующих настроек прокси.
5.  **Логирование**: Функция логирует информацию об установленном прокси, включая протокол, хост и порт.

**ASCII Flowchart**:

```
     A Получение списка прокси
     |
     B Объединение прокси SOCKS4 и SOCKS5
     |
     C Выбор рабочего прокси
     |
     D Установка параметров прокси в options
     |
     E Логирование информации об установленном прокси
```

**Примеры**:

```python
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from src.webdriver.firefox.firefox import Firefox
from src.webdriver.proxy import get_proxies_dict, check_proxy # чтобы пример работал - надо импортировать у себя эти методы

#  Предположим, что Firefox уже инициирован

#  Получение инстанса класса Options
options = Options()

#  Вызов метода set_proxy для установки прокси
driver = Firefox()
driver.set_proxy(options)
```

### `Firefox._payload`

```python
def _payload(self) -> None:
    """Loads executors for locators and JavaScript scripts."""
```

**Назначение**:
Загружает исполнителей для локаторов и скриптов JavaScript.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- `None`

**Вызывает исключения**:
- Отсутствуют явные указания на исключения.

**Как работает функция**:

1.  **Инициализация JavaScript**: Создается экземпляр класса `JavaScript`, который предоставляет методы для выполнения JavaScript-скриптов в браузере.
2.  **Присвоение методов JavaScript**: Методы из объекта `JavaScript` присваиваются текущему объекту `Firefox`, чтобы их можно было вызывать непосредственно через экземпляр `Firefox`.
    - `get_page_lang`: Получает язык страницы.
    - `ready_state`: Получает состояние готовности страницы.
    - `get_referrer`: Получает referrer страницы.
    - `unhide_DOM_element`: Делает DOM-элемент видимым.
    - `window_focus`: Передает фокус окну браузера.
3.  **Инициализация ExecuteLocator**: Создается экземпляр класса `ExecuteLocator`, который предоставляет методы для выполнения локаторов элементов на странице.
4.  **Присвоение методов ExecuteLocator**: Методы из объекта `ExecuteLocator` присваиваются текущему объекту `Firefox`, чтобы их можно было вызывать непосредственно через экземпляр `Firefox`.
    - `execute_locator`: Выполняет поиск элемента по локатору.
    - `get_webelement_as_screenshot`: Получает скриншот веб-элемента.
    - `get_webelement_by_locator`: Получает веб-элемент по локатору.
    - `get_attribute_by_locator`: Получает атрибут веб-элемента по локатору.
    - `send_message`: Отправляет сообщение веб-элементу.
    - `send_key_to_webelement`: Отправляет клавишу веб-элементу.

**ASCII Flowchart**:

```
     A Инициализация JavaScript
     |
     B Присвоение методов JavaScript
     |
     C Инициализация ExecuteLocator
     |
     D Присвоение методов ExecuteLocator
```

**Примеры**:

```python
from src.webdriver.firefox.firefox import Firefox

# Инициализация Firefox
driver = Firefox()

# Теперь можно использовать методы JavaScript и ExecuteLocator через экземпляр Firefox
driver.get("https://www.example.com")
page_language = driver.get_page_lang()
print(f"Page Language: {page_language}")
driver.quit()
```

## Примеры

```python
if __name__ == "__main__":
    driver = Firefox()
    driver.get("https://google.com")