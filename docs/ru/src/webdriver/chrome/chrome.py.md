# Модуль для работы с WebDriver Chrome

## Обзор

Модуль `chrome.py` предоставляет класс `Chrome`, расширяющий стандартный `webdriver.Chrome` из библиотеки Selenium. Он предназначен для упрощения и расширения функциональности управления браузером Chrome, добавляя возможности управления профилем, прокси, пользовательским агентом и другими параметрами.

## Подробней

Этот модуль предназначен для работы с браузером Chrome через WebDriver. Он включает в себя настройку опций Chrome, управление профилем пользователя, установку прокси и пользовательского агента. Класс `Chrome` наследуется от `selenium.webdriver.Chrome` и предоставляет дополнительные методы и атрибуты для более удобного взаимодействия с браузером.

## Классы

### `Chrome`

**Описание**: Класс `Chrome` расширяет `webdriver.Chrome` и предоставляет дополнительные возможности для управления браузером Chrome.

**Наследует**:
- `selenium.webdriver.Chrome`

**Атрибуты**:
- `driver_name` (str): Имя драйвера (в данном случае 'chrome').

**Параметры**:
- `profile_name` (Optional[str]): Имя пользовательского профиля Chrome.
- `chromedriver_version` (Optional[str]): Версия ChromeDriver.
- `user_agent` (Optional[str]): Пользовательский агент в формате строки.
- `proxy_file_path` (Optional[str]): Путь к файлу с прокси.
- `options` (Optional[List[str]]): Список опций для Chrome.
- `window_mode` (Optional[str]): Режим окна браузера (`windowless`, `kiosk`, `full_window` и т.д.).

**Принцип работы**:

Класс `Chrome` инициализирует драйвер Chrome с заданными параметрами, такими как профиль пользователя, версия ChromeDriver, пользовательский агент, прокси и режим окна. Он также загружает настройки Chrome из файла конфигурации `chrome.json`.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `Chrome`, настраивает параметры Chrome и запускает WebDriver.
- `set_proxy`: Настраивает прокси из словаря, полученного из `get_proxies_dict`.
- `_payload`: Загружает исполнителей для локаторов и JavaScript сценариев.

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
    """
    Инициализирует экземпляр класса `Chrome`, настраивает параметры Chrome и запускает WebDriver.

    Args:
        profile_name (Optional[str], optional): Имя пользовательского профиля Chrome. По умолчанию `None`.
        chromedriver_version (Optional[str], optional): Версия ChromeDriver. По умолчанию `None`.
        user_agent (Optional[str], optional): Пользовательский агент в формате строки. По умолчанию `None`.
        proxy_file_path (Optional[str], optional): Путь к файлу с прокси. По умолчанию `None`.
        options (Optional[List[str]], optional): Список опций для Chrome. По умолчанию `None`.
        window_mode (Optional[str], optional): Режим окна браузера (`windowless`, `kiosk`, `full_window` и т.д.). По умолчанию `None`.

    Raises:
        WebDriverException: Если возникает ошибка при запуске WebDriver (например, из-за несовместимой версии Chrome или ChromeDriver).
        Exception: Если возникает любая другая ошибка при работе Chrome WebDriver.
    """
```

**Как работает функция**:

1. **Объявление переменных**: В начале функции объявляются переменные `service` и `options_obj`, которые будут использоваться для настройки и запуска Chrome WebDriver.
2. **Загрузка настроек Chrome**: Загружаются настройки Chrome из файла `chrome.json` с использованием функции `j_loads_ns`.
3. **Путь к ChromeDriver**: Определяется путь к исполняемому файлу ChromeDriver на основе конфигурации.
4. **Инициализация сервиса**: Создается экземпляр сервиса ChromeDriver с указанным путем к исполняемому файлу.
5. **Настройка опций Chrome**: Создается объект `Options` для настройки опций Chrome.
6. **Добавление опций из файла настроек**: Если в файле конфигурации указаны опции, они добавляются к объекту `options_obj`.
7. **Установка режима окна**: Устанавливается режим окна браузера на основе конфигурации или переданных параметров (kiosk, windowless, full_window).
8. **Добавление опций, переданных при инициализации**: Если при инициализации класса были переданы дополнительные опции, они добавляются к объекту `options_obj`.
9. **Установка пользовательского агента**: Устанавливается пользовательский агент, либо случайный, либо указанный при инициализации.
10. **Установка прокси**: Если в конфигурации включена поддержка прокси, вызывается метод `set_proxy` для настройки прокси.
11. **Настройка директории профиля**: Настраивается директория профиля пользователя Chrome на основе конфигурации и переданных параметров.
12. **Запуск Chrome WebDriver**: Запускается Chrome WebDriver с настроенными опциями и сервисом. Если возникают исключения, они логируются, и функция возвращает управление.
13. **Загрузка payload**: После успешного запуска драйвера вызывается метод `_payload` для загрузки дополнительных функций и исполнителей.

**Примеры**:

```python
# Пример 1: Запуск Chrome с профилем пользователя и в полноэкранном режиме
driver = Chrome(profile_name='my_profile', window_mode='full_window')

# Пример 2: Запуск Chrome с пользовательским агентом и дополнительными опциями
driver = Chrome(user_agent='CustomUserAgent', options=['--disable-extensions'])

# Пример 3: Запуск Chrome с прокси и указанием версии ChromeDriver
driver = Chrome(proxy_file_path='path/to/proxy.txt', chromedriver_version='87.0.4280.88')
```

### `set_proxy`

```python
def set_proxy(self, options: Options) -> None:
    """
    Настраивает прокси из словаря, возвращаемого get_proxies_dict.

    Args:
        options (Options): Опции Chrome, в которые добавляются настройки прокси.
    """
```

**Как работает функция**:

1. **Получение словаря прокси**: Функция вызывает `get_proxies_dict()` для получения словаря с настройками прокси.
2. **Создание списка всех прокси**: Из словаря извлекаются списки прокси для протоколов socks4 и socks5, и они объединяются в один список `all_proxies`.
3. **Перебор прокси для поиска рабочего**: Функция перебирает прокси из списка `all_proxies` в случайном порядке, чтобы найти рабочий прокси. Для проверки используется функция `check_proxy()`.
4. **Настройка прокси, если он найден**: Если рабочий прокси найден, функция настраивает опции Chrome для использования этого прокси. В зависимости от протокола (http, socks4, socks5) добавляются соответствующие аргументы командной строки для Chrome.
5. **Логирование**: Функция логирует информацию о настройке прокси или предупреждения, если прокси не найдены или тип прокси неизвестен.

**Примеры**:

```python
# Пример настройки прокси для Chrome
options = Options()
chrome_instance = Chrome()
chrome_instance.set_proxy(options)
```

### `_payload`

```python
def _payload(self) -> None:
    """
    Загружает исполнителей для локаторов и JavaScript сценариев.
    """
```

**Как работает функция**:

1. **Создание экземпляра `JavaScript`**: Создается экземпляр класса `JavaScript`, который используется для выполнения JavaScript-кода в браузере.
2. **Назначение методов `JavaScript`**: Методы из экземпляра `JavaScript` (например, `get_page_lang`, `ready_state`, `get_referrer`, `unhide_DOM_element`, `window_focus`) присваиваются текущему экземпляру класса `Chrome`, чтобы их можно было вызывать напрямую через экземпляр драйвера Chrome.
3. **Создание экземпляра `ExecuteLocator`**: Создается экземпляр класса `ExecuteLocator`, который используется для выполнения локаторов элементов на веб-странице.
4. **Назначение методов `ExecuteLocator`**: Методы из экземпляра `ExecuteLocator` (например, `execute_locator`, `get_webelement_as_screenshot`, `get_webelement_by_locator`, `get_attribute_by_locator`, `send_message`, `send_key_to_webelement`) присваиваются текущему экземпляру класса `Chrome`, чтобы их можно было вызывать напрямую через экземпляр драйвера Chrome.

**Примеры**:

```python
# Пример вызова _payload после инициализации Chrome
driver = Chrome()
driver._payload()
```

## Параметры класса

- `profile_name` (Optional[str]): Имя пользовательского профиля Chrome.
- `chromedriver_version` (Optional[str]): Версия chromedriver.
- `user_agent` (Optional[str]): Пользовательский агент в формате строки.
- `proxy_file_path` (Optional[str]): Путь к файлу с прокси.
- `options` (Optional[List[str]]): Список опций для Chrome.
- `window_mode` (Optional[str]): Режим окна браузера (`windowless`, `kiosk`, `full_window` и т.д.).

**Примеры**:

```python
# Пример использования различных параметров при создании экземпляра класса Chrome
driver1 = Chrome(profile_name='test_profile', window_mode='kiosk')
driver2 = Chrome(user_agent='Mozilla/5.0', options=['--disable-gpu'])
driver3 = Chrome(proxy_file_path='/path/to/proxy.txt')
```