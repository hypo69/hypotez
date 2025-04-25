# Модуль WebDriver для Firefox

## Обзор

Этот модуль предоставляет класс `Firefox`, расширяющий стандартный `selenium.webdriver.Firefox` дополнительными функциями, такими как управление профилем, киоск-режим и прокси-настройки.

## Подробнее

Этот модуль используется для запуска браузера Firefox с помощью Selenium WebDriver. Он предоставляет различные возможности для настройки и управления браузером, такие как:

- **Управление профилем**: Модуль позволяет использовать пользовательские профили Firefox для запуска WebDriver.
- **Киоск-режим**: Модуль позволяет запускать Firefox в киоск-режиме, скрывая меню и панели инструментов.
- **Настройка User-Agent**:  Модуль позволяет задавать пользовательский User-Agent для Firefox.
- **Настройки прокси**: Модуль позволяет настроить прокси-сервер для Firefox.

## Классы

### `class Firefox`

**Описание**: Класс `Firefox` расширяет стандартный `selenium.webdriver.Firefox` с дополнительными функциями, включая управление профилем, киоск-режим и прокси-настройки.

**Наследует**: `selenium.webdriver.Firefox`

**Атрибуты**:

- `driver_name` (str): Имя WebDriver (``"firefox"``).

**Параметры**:

- `profile_name` (Optional[str]): Имя профиля Firefox, который будет использоваться. По умолчанию: ``None``.
- `geckodriver_version` (Optional[str]): Версия GeckoDriver. По умолчанию: ``None``.
- `firefox_version` (Optional[str]): Версия Firefox. По умолчанию: ``None``.
- `user_agent` (Optional[str]): Строка User-Agent. Если ``None``, используется случайный User-Agent. По умолчанию: ``None``.
- `proxy_file_path` (Optional[str]): Путь к файлу прокси. По умолчанию: ``None``.
- `options` (Optional[List[str]]): Список опций Firefox. По умолчанию: ``None``.
- `window_mode` (Optional[str]): Режим окна браузера (например, "windowless", "kiosk"). По умолчанию: ``None``.

**Пример**:

```python
from src.webdriver import Firefox
from src.logger import logger

logger.info('Запускаю WebDriver')
browser = Firefox(
    profile_name="custom_profile",  # Имя профиля
    window_mode="kiosk"  # Режим киоска
)
browser.get("https://www.example.com")
logger.success('Браузер запущен')
browser.quit()
```

**Методы**:

- `__init__(self, profile_name: Optional[str] = None, geckodriver_version: Optional[str] = None, firefox_version: Optional[str] = None, user_agent: Optional[str] = None, proxy_file_path: Optional[str] = None, options: Optional[List[str]] = None, window_mode: Optional[str] = None, *args, **kwargs) -> None`: Инициализирует Firefox WebDriver с пользовательскими настройками.
- `set_proxy(self, options: Options) -> None`: Настраивает параметры прокси из словаря.
- `_payload(self) -> None`: Загружает исполнители для локаторов и JavaScript-скриптов.

**Как работает класс:**

- Инициализирует WebDriver с заданными настройками.
- Загружает настройки из файла конфигурации ``firefox.json``.
- Настраивает параметры WebDriver, такие как опции, User-Agent, прокси, и профиль.
- Запускает WebDriver.
- Загружает исполнители для локаторов и JavaScript-скриптов.

**Внутренние функции:**

- `_payload(self) -> None`: Загружает исполнители для локаторов и JavaScript-скриптов. Эта функция определяет объекты `JavaScript` и `ExecuteLocator` для использования в WebDriver.


### `class Config`

**Описание**: Класс `Config` содержит настройки для Firefox WebDriver, которые загружаются из файла конфигурации ``firefox.json``.

**Атрибуты**:

- `geckodriver_path` (str): Путь к исполняемому файлу GeckoDriver.
- `firefox_binary_path` (str): Путь к исполняемому файлу Firefox.
- `profile_directory_default` (str): Имя каталога профиля Firefox.
- `profile_directory_os` (str): Путь к каталогу профиля Firefox в операционной системе.
- `profile_directory_internal` (str): Путь к каталогу профиля Firefox внутри проекта.
- `options` (List[str]): Список опций Firefox.
- `headers` (Dict[str, Any]): Словарь с заголовками для Firefox.
- `proxy_enabled` (bool): Флаг, указывающий, включена ли прокси-настройка.


## Функции


## Параметры


**Примеры**:

```python
from src.webdriver.firefox import Firefox

# Создание инстанса драйвера
driver = Firefox(
    profile_name="custom_profile",
    window_mode="kiosk",
)
driver.get("https://google.com")
# Дальнейшее использование WebDriver...
```

```python
from src.webdriver.firefox import Firefox

# Запуск Firefox в киоск-режиме
driver = Firefox(window_mode="kiosk")
driver.get("https://www.example.com")
# Дальнейшее использование WebDriver...
```

## Твое поведение при анализе кода:

- Внутри кода ты можешь встретить выражение между `<` `>`. Например: <инструкция для модели gemini:Загрузка описаний продуктов в PrestaShop.>, <далее, если есть>. Это заготовки, куда ты вставляешь релевантное значение
- Всегда смотри системную инструкцию для обработки кода проекта `hypotez`;
- Анализируй расположение файла в проекте. Это поможет понять его назначение и взаимосвязь с другими файлами. Расположение файла ты найдешь в самой превой строке кода, начинающейся с `## \\file /...`;
- Запоминай предоставленный код и анализируй его связь с другими частями проекта;
- В этой инструкции не надо предлагать улучшение кода. Четко следуй пункту 5. **Пример файла** при составлении ответа