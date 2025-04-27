# Модуль Firefox WebDriver

## Обзор

Этот модуль предоставляет класс `Firefox`, расширяющий стандартный `selenium.webdriver.Firefox`  дополнительными функциями, такими как управление пользовательскими профилями, режим киоска и настройки прокси.

## Детали

Модуль `Firefox` расширяет стандартный `selenium.webdriver.Firefox`  дополнительными функциями, необходимыми для работы с браузером Firefox. В нем реализованы настройки профиля, режим киоска, а также другие опции, которые могут быть использованы для работы с WebDriver в различных сценариях.

## Классы

### `class Config`

**Описание**: Класс конфигурации для Firefox WebDriver.

**Атрибуты**:

- `geckodriver_path` (str): Путь к исполняемому файлу GeckoDriver.
- `firefox_binary_path` (str): Путь к исполняемому файлу Firefox.
- `profile_directory_default` (str): Путь к директории профилей по умолчанию.
- `profile_directory_os` (str): Путь к директории профилей в операционной системе.
- `profile_directory_internal` (str): Путь к внутренней директории профилей.
- `options` (List[str]): Список опций Firefox.
- `headers` (Dict[str, Any]): Словарь заголовков для запросов.
- `proxy_enabled` (bool): Флаг, указывающий, включен ли прокси.

**Методы**:

- `__init__(self, config_path: Path)`: Инициализирует объект Config, загружая настройки из JSON-файла.

### `class Firefox`

**Описание**: Расширяет `webdriver.Firefox` с улучшенными возможностями.

**Особенности**:

- Поддержка пользовательских профилей Firefox.
- Режим киоска и другие режимы окон.
- Настройка user-agent.
- Настройки прокси.

**Атрибуты**:

- `driver_name` (str): Имя драйвера.

**Методы**:

- `__init__(self, profile_name: Optional[str] = None, geckodriver_version: Optional[str] = None, firefox_version: Optional[str] = None, user_agent: Optional[str] = None, proxy_file_path: Optional[str] = None, options: Optional[List[str]] = None, window_mode: Optional[str] = None, *args, **kwargs) -> None`: Инициализирует Firefox WebDriver с пользовательскими настройками.
- `set_proxy(self, options: Options) -> None`: Настраивает прокси-настройки из словаря.
- `_payload(self) -> None`: Загружает исполнители для локаторов и JavaScript-скриптов.

## Функции

### `set_proxy(self, options: Options) -> None`

**Цель**: Настраивает прокси-настройки из словаря.

**Параметры**:

- `options` (Options): Firefox options, к которым нужно добавить прокси-настройки.

**Возвращаемое значение**:
- `None`

**Пример**:

```python
# Creating a Firefox driver instance with proxy settings
driver = Firefox(proxy_file_path='path/to/proxy/file.json')
# Now the driver will use a proxy from the specified file
```

### `_payload(self) -> None`

**Цель**: Загружает исполнители для локаторов и JavaScript-скриптов.

**Параметры**:
- `None`

**Возвращаемое значение**:
- `None`

**Пример**:

```python
# After creating a Firefox driver instance, _payload will be called automatically
# and will load the executors for locators and JavaScript scripts
driver = Firefox()
# Now the driver has access to executors for locators and JavaScript scripts
```

## Примеры

```python
# Creating a Firefox driver instance
driver = Firefox()

# Opening a webpage
driver.get("https://google.com")

# Closing the browser
driver.quit()
```

## Дополнительная информация

- Для работы с веб-элементами, используйте `driver.execute_locator(l:dict)`, который возвращает значение веб-элемента по локатору.

- В коде могут использоваться выражения между `<` и `>`, например `<instruction for gemini model:Loading product descriptions into PrestaShop.>, <next, if available>`. 

- Всегда обращайтесь к системным инструкциям для обработки кода в проекте `hypotez`.

- Используйте `logger` из `src.logger` для логгирования.

-  Все комментарии и docstrings должны быть на русском языке в кодировке UTF-8.