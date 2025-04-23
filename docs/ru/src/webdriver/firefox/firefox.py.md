# Модуль WebDriver Firefox

## Обзор

Модуль предоставляет класс `Firefox`, расширяющий стандартный `selenium.webdriver.Firefox` с дополнительными функциями, такими как управление пользовательским профилем, режим киоска и настройки прокси.

## Подробнее

Этот модуль расширяет возможности веб-драйвера Firefox, предоставляя дополнительные функции для настройки и управления экземпляром Firefox. Он позволяет использовать пользовательские профили, устанавливать режим киоска, настраивать user-agent и прокси-серверы.

## Классы

### `Config`

**Описание**: Класс конфигурации для WebDriver Firefox.

**Атрибуты**:

- `geckodriver_path` (str): Путь к исполняемому файлу GeckoDriver.
- `firefox_binary_path` (str): Путь к исполняемому файлу Firefox.
- `profile_directory_default` (str): Значение по умолчанию для каталога профиля.
- `profile_directory_os` (str): Каталог профиля, специфичный для операционной системы.
- `profile_directory_internal` (str): Внутренний каталог профиля.
- `options` (List[str]): Список опций Firefox.
- `headers` (Dict[str, Any]): Словарь заголовков.
- `proxy_enabled` (bool): Флаг, указывающий, включен ли прокси.

**Методы**:

- `__init__(config_path: Path)`: Инициализирует объект `Config`, загружая настройки из JSON-файла.

   **Параметры**:
   - `config_path` (Path): Путь к JSON-файлу конфигурации.

   **Как работает функция**:
    - Функция загружает конфигурацию из JSON-файла, используя `j_loads_ns`.
    - Извлекает пути к исполняемым файлам `geckodriver` и `firefox_binary` из конфигурации и преобразует их в строки.
    - Загружает параметры каталога профиля, опции командной строки и заголовки из файла конфигурации.
    - Определяет, включен ли прокси-сервер на основе файла конфигурации.
    - Все пути формируются относительно корня проекта, используя `gs.path.root`.

   **Примеры**:
    ```python
    from pathlib import Path
    config_path = Path("path/to/firefox.json")  # Замените на актуальный путь к файлу конфигурации
    config = Config(config_path)
    print(f"Путь к geckodriver: {config.geckodriver_path}")
    print(f"Включен ли прокси: {config.proxy_enabled}")
    ```

### `Firefox`

**Описание**: Расширяет `webdriver.Firefox` с расширенными возможностями.

**Наследует**:
- `selenium.webdriver.Firefox`

**Атрибуты**:
- `driver_name` (str): Имя драйвера (`"firefox"`).

**Параметры**:

- `profile_name` (Optional[str], optional): Имя профиля Firefox для использования. По умолчанию `None`.
- `geckodriver_version` (Optional[str], optional): Версия GeckoDriver. По умолчанию `None`.
- `firefox_version` (Optional[str], optional): Версия Firefox. По умолчанию `None`.
- `user_agent` (Optional[str], optional): Строка user agent. Если `None`, используется случайный user agent. По умолчанию `None`.
- `proxy_file_path` (Optional[str], optional): Путь к файлу прокси. По умолчанию `None`.
- `options` (Optional[List[str]], optional): Список опций Firefox. По умолчанию `None`.
- `window_mode` (Optional[str], optional): Режим окна браузера (например, `"windowless"`, `"kiosk"`). По умолчанию `None`.

**Принцип работы**:

1. **Инициализация**:
   - Инициализирует WebDriver Firefox с пользовательскими настройками, такими как профиль, user-agent, прокси и режим окна.
   - Загружает конфигурацию из JSON-файла `firefox.json`.
   - Настраивает параметры службы GeckoDriver и параметры Firefox.
   - Устанавливает user-agent, прокси (если включен) и каталог профиля.
2. **Настройка параметров**:
   - Загружает параметры из файла конфигурации, параметры командной строки и устанавливает user-agent.
   - Настраивает прокси, если он включен в конфигурации.
3. **Профиль Firefox**:
   - Настраивает каталог профиля Firefox, используя либо профиль по умолчанию, либо указанный профиль.
4. **Запуск WebDriver**:
   - Инициализирует WebDriver Firefox с заданными параметрами и обрабатывает любые исключения, которые могут возникнуть во время запуска.
   - Вызывает метод `_payload` для загрузки исполнителей для локаторов и скриптов JavaScript.

**Методы**:

- `__init__(profile_name: Optional[str] = None, geckodriver_version: Optional[str] = None, firefox_version: Optional[str] = None, user_agent: Optional[str] = None, proxy_file_path: Optional[str] = None, options: Optional[List[str]] = None, window_mode: Optional[str] = None, *args, **kwargs)`: Инициализирует WebDriver Firefox с пользовательскими настройками.

   **Параметры**:
   - `profile_name` (Optional[str], optional): Имя профиля Firefox для использования. По умолчанию `None`.
   - `geckodriver_version` (Optional[str], optional): Версия GeckoDriver. По умолчанию `None`.
   - `firefox_version` (Optional[str], optional): Версия Firefox. По умолчанию `None`.
   - `user_agent` (Optional[str], optional): Строка user agent. Если `None`, используется случайный user agent. По умолчанию `None`.
   - `proxy_file_path` (Optional[str], optional): Путь к файлу прокси. По умолчанию `None`.
   - `options` (Optional[List[str]], optional): Список опций Firefox. По умолчанию `None`.
   - `window_mode` (Optional[str], optional): Режим окна браузера (например, `"windowless"`, `"kiosk"`). По умолчанию `None`.
   - `*args`: Произвольные позиционные аргументы.
   - `**kwargs`: Произвольные аргументы ключевого слова.

   **Как работает функция**:
    - Функция инициализирует WebDriver Firefox с пользовательскими настройками, такими как профиль, user-agent, прокси и режим окна.
    - Сначала она загружает конфигурацию из JSON-файла `firefox.json`, используя класс `Config`.
    - Затем она настраивает параметры службы GeckoDriver и параметры Firefox, включая режим окна и любые дополнительные опции, переданные в конструктор.
    - Если `user_agent` не указан, функция генерирует случайный user-agent с использованием библиотеки `fake_useragent`.
    - Если включен прокси-сервер, функция вызывает метод `set_proxy` для настройки параметров прокси.
    - Наконец, она инициализирует WebDriver Firefox с заданными параметрами и обрабатывает любые исключения, которые могут возникнуть во время запуска.

   **Вызывает исключения**:
   - `WebDriverException`: Если WebDriver не запускается.
   - `Exception`: Для других непредвиденных ошибок во время инициализации.

   **Примеры**:
    ```python
    from src.webdriver.firefox.firefox import Firefox
    from pathlib import Path

    # Пример 1: Запуск Firefox с профилем по умолчанию и режимом киоска
    driver1 = Firefox(window_mode="kiosk")
    driver1.get("https://www.example.com")
    driver1.quit()

    # Пример 2: Запуск Firefox с пользовательским профилем и user-agent
    profile_name = "custom_profile"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    driver2 = Firefox(profile_name=profile_name, user_agent=user_agent)
    driver2.get("https://www.example.com")
    driver2.quit()

    # Пример 3: Запуск Firefox с пользовательскими опциями
    options = ["--disable-extensions", "--mute-audio"]
    driver3 = Firefox(options=options)
    driver3.get("https://www.example.com")
    driver3.quit()
    ```

- `set_proxy(options: Options) -> None`: Настраивает параметры прокси из словаря.

   **Параметры**:
   - `options` (Options): Параметры Firefox для добавления настроек прокси.

   **Как работает функция**:
    - Функция настраивает параметры прокси в Firefox, выбирая случайный рабочий прокси из списка, полученного с помощью `get_proxies_dict`.
    - Она пробует случайным образом прокси из списка, пока не найдет рабочий, используя `check_proxy`.
    - Если рабочий прокси найден, он устанавливает параметры прокси в Firefox, используя `options.set_preference`.
    - Поддерживаются протоколы HTTP, SOCKS4 и SOCKS5.

   **Примеры**:
    ```python
    from selenium.webdriver.firefox.options import Options
    from src.webdriver.firefox.firefox import Firefox

    # Создаем объект Firefox
    driver = Firefox()
    options = Options()
    # Пример вызова функции set_proxy
    driver.set_proxy(options)
    ```

- `_payload(self) -> None`: Загружает исполнителей для локаторов и скриптов JavaScript.

   **Как работает функция**:
    - Функция загружает и присваивает методы JavaScript и ExecuteLocator экземпляру WebDriver Firefox.
    - Она инициализирует класс `JavaScript` с экземпляром драйвера и присваивает различные методы JavaScript экземпляру драйвера для использования.
    - Кроме того, она инициализирует класс `ExecuteLocator` с экземпляром драйвера и присваивает его методы экземпляру драйвера для выполнения поиска элементов и других действий.

   **Примеры**:
    ```python
    from src.webdriver.firefox.firefox import Firefox

    # Создаем объект Firefox
    driver = Firefox()

    # Пример вызова функции _payload
    driver._payload()
    ```

## Примеры

```python
if __name__ == "__main__":
    driver = Firefox()
    driver.get("https://google.com")