## Анализ кода модуля `src/webdriver/chrome/chrome.py`

### Обзор

Этот модуль предоставляет пользовательскую реализацию Chrome WebDriver на основе Selenium. Он интегрирует настройки конфигурации, определённые в файле `chrome.json`, такие как user-agent и настройки профиля браузера, чтобы обеспечить гибкое и автоматизированное взаимодействие с браузером.

### Подробней

Модуль `src/webdriver/chrome/chrome.py` предоставляет класс `Chrome`, который наследует от `selenium.webdriver.Chrome` и позволяет настраивать различные параметры браузера, такие как пользовательский агент, профиль пользователя и другие опции, с использованием файла конфигурации `chrome.json`. Модуль также интегрирует функциональность для выполнения JavaScript-кода и взаимодействия с элементами на странице.

### Классы

#### `Chrome(WebDriver)`

**Описание**: Класс, расширяющий функциональность `webdriver.Chrome` для автоматизации управления браузером Chrome.

**Атрибуты:**

-   `driver_name` (str): Имя драйвера ("chrome").

**Методы:**

-   `__init__(self, profile_name: Optional[str] = None, chromedriver_version: Optional[str] = None, user_agent: Optional[str] = None, proxy_file_path: Optional[str] = None, options: Optional[List[str]] = None, window_mode: Optional[str] = None, *args, **kwargs) -> None`: Инициализирует экземпляр Chrome WebDriver с пользовательскими настройками.
-   `set_proxy(self, options: Options) -> None`: Настраивает прокси из словаря, полученного из `get_proxies_dict`.
-   `_payload(self) -> None`: Загружает исполнителей для локаторов и JavaScript сценариев.

#### Описание методов класса `Chrome`

##### `__init__`
```python
    def __init__(self, profile_name: Optional[str] = None,
                 chromedriver_version: Optional[str] = None,
                 user_agent: Optional[str] = None,
                 proxy_file_path: Optional[str] = None,
                 options: Optional[List[str]] = None,
                 window_mode: Optional[str] = None,
                 *args, **kwargs) -> None:
```

**Назначение**: Инициализирует класс `Chrome` с заданными параметрами.

**Параметры:**
- `profile_name` (Optional[str]): Имя пользовательского профиля Chrome.
- `chromedriver_version` (Optional[str]): Версия ChromeDriver (не используется в коде).
- `user_agent` (Optional[str]): Пользовательский агент для браузера. Если не указан, будет сгенерирован случайный.
- `proxy_file_path` (Optional[str]): Путь к файлу с прокси-серверами. (Не используется в текущей реализации)
- `options` (Optional[List[str]]): Список дополнительных опций командной строки для Chrome.
-  `window_mode` (Optional[str]): Режим окна браузера.

**Как работает функция**
1.  Загружает конфигурации Chrome из файла `chrome.json`.
2.  Инициализирует сервис Chrome, используя путь к ChromeDriver из конфигурации.
3.  Создает объект `Options` для настройки Chrome.
4.  Добавляет опции из файла конфигурации и переданных аргументов.
5. Устанавливает режим окна браузера (kiosk, windowless, full\_window).
6.  Устанавливает пользовательский агент, используя `fake_useragent` для генерации случайного агента, если не указан.
7. Настраивает прокси, если они включены в конфигурации, вызывая метод `set_proxy`.
8. Запускает Chrome WebDriver с заданными настройками и вызывает метод `_payload` для загрузки исполнителей локаторов и JavaScript.

##### `set_proxy`

```python
    def set_proxy(self, options: Options) -> None:
        """
        Настройка прокси из словаря, возвращаемого get_proxies_dict.

        :param options: Опции Chrome, в которые добавляются настройки прокси.
        :type options: Options
        """
        # Получение словаря прокси
        proxies_dict = get_proxies_dict()
        # Создание списка всех прокси
        all_proxies = proxies_dict.get('socks4', []) + proxies_dict.get('socks5', [])
        # Перебор прокси для поиска рабочего
        working_proxy = None
        for proxy in random.sample(all_proxies, len(all_proxies)):
            if check_proxy(proxy):\n
                working_proxy = proxy
                break
```

**Назначение**: Настраивает параметры прокси для Chrome, беря данные из словаря прокси.

**Параметры:**
- `options` (Options): Экземпляр класса `selenium.webdriver.chrome.options.Options`, в который добавляются настройки прокси.

**Как работает функция**
1. Получает словарь прокси, используя функцию `get_proxies_dict`.
2. Создаёт список всех прокси (SOCKS4 и SOCKS5) и пытается найти рабочий прокси, перебирая их в случайном порядке и проверяя их доступность функцией `check_proxy`.
3. Если рабочий прокси найден, устанавливает параметры прокси для Chrome, добавляя аргументы командной строки для HTTP, SOCKS4 или SOCKS5.

##### `_payload`

```python
 def _payload(self) -> None:
        """
        Load executors for locators and JavaScript scenarios.
        """
        j = JavaScript(self)
        self.get_page_lang = j.get_page_lang
        self.ready_state = j.ready_state
        self.get_referrer = j.ready_state
        self.unhide_DOM_element = j.unhide_DOM_element
        self.window_focus = j.window_focus

        execute_locator = ExecuteLocator(self)
        self.execute_locator = execute_locator.execute_locator
        self.get_webelement_as_screenshot = execute_locator.get_webelement_as_screenshot
        self.get_webelement_by_locator = execute_locator.get_webelement_by_locator
        self.get_attribute_by_locator = execute_locator.get_attribute_by_locator
        self.send_message = self.send_key_to_webelement = execute_locator.send_message
```

**Назначение**: Загружает и настраивает объекты, необходимые для выполнения JavaScript и локаторов элементов на веб-странице.

**Как работает функция**:

1. Создает экземпляр класса `JavaScript`, передавая ему экземпляр веб-драйвера.
2. Назначает методы из экземпляра `JavaScript` (например, `get_page_lang`, `ready_state`, `unhide_DOM_element`) атрибутам текущего объекта `Chrome`.
3. Создает экземпляр класса `ExecuteLocator`, передавая ему экземпляр веб-драйвера.
4.  Назначает методы из экземпляра `ExecuteLocator` (например, `execute_locator`, `get_webelement_as_screenshot`, `send_message`) атрибутам текущего объекта `Chrome`.

### Переменные модуля
 -   `driver_name` (str): Имя драйвера ("chrome").
-   `service` (Service): экземпляр класса `selenium.webdriver.chrome.service.Service`, который управляет процессом ChromeDriver.
-    `options_obj` (Options): экземпляр класса `selenium.webdriver.chrome.options.Options`, который используется для настройки параметров запуска браузера Chrome.
-   `chromedriver_path` (str): содержит путь к исполняемому файлу ChromeDriver.
-   `profile_directory` (str): содержит путь к профилю пользователя Chrome.

### Пример использования

**Создание экземпляра Chrome WebDriver с настройками по умолчанию:**

```python
from src.webdriver.chrome import Chrome

driver = Chrome()
driver.get("https://www.example.com")
driver.quit()
```

**Создание экземпляра Chrome WebDriver с пользовательским профилем и прокси:**

```python
from src.webdriver.chrome import Chrome

driver = Chrome(profile_name="my_profile", user_agent="My Custom Agent")
driver.get("https://www.example.com")
driver.quit()
```

### Взаимосвязь с другими частями проекта

Модуль `src/webdriver/chrome/chrome.py` взаимодействует со следующими модулями:

-   `selenium`: Для управления браузером Chrome.
-   `fake_useragent`: Для генерации случайных User-Agent.
-   `src`: Внутренние модули проекта `hypotez`:
    -   `src.webdriver.executor`: Для выполнения действий с веб-элементами.
    -   `src.webdriver.js`: Для выполнения JavaScript кода.
    -   `src.webdriver.proxy`: Для настройки прокси.
    -   `src.utils.jjson`: Для загрузки конфигурации из JSON файла.
    -   `src.logger.logger`: Для логирования событий.