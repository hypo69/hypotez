# `ChromiumOptions` and `Options` Class Reference

Модуль предоставляет классы `ChromiumOptions` и `Options` для гибкой конфигурации параметров запуска браузера Chrome в библиотеке Pydoll. Он позволяет управлять аргументами командной строки, путями к исполняемому файлу, расширениями, экспериментальными возможностями и пользовательскими настройками.

Класс `Options` является псевдонимом для `ChromiumOptions` и служит для обратной совместимости.

## Использование

Основной способ использования — создать экземпляр `ChromiumOptions`, настроить его с помощью предоставляемых методов, а затем передать его при запуске браузера.

```python
from src.webdriver.pydoll.options import ChromiumOptions
from pydoll import Browser

# 1. Создание экземпляра опций
options = ChromiumOptions()

# 2. Настройка опций
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
options.set_preference('profile.managed_default_content_settings.images', 2) # Блокировка изображений

# 3. Запуск браузера с опциями
# (Предполагается, что в Pydoll есть способ передать опции)
# browser = await Browser.launch(options=options.to_capabilities())
```

## Класс `ChromiumOptions`

### Инициализация

#### `__init__(self)`

Создает пустой объект `ChromiumOptions` со значениями по умолчанию.

### Свойства

#### `binary_location`
-   **Тип:** `Optional[str]`
-   **Описание:** Позволяет получить или установить путь к исполняемому файлу браузера Chrome.
-   **Пример:**
    ```python
    options.binary_location = '/usr/bin/google-chrome-stable'
    print(options.binary_location)
    ```

#### `arguments`
-   **Тип:** `List[str]` (только для чтения)
-   **Описание:** Возвращает копию списка всех добавленных аргументов командной строки.

#### `extensions`
-   **Тип:** `List[str]` (только для чтения)
-   **Описание:** Возвращает копию списка путей к расширениям.

#### `experimental_options`
-   **Тип:** `Dict[str, Any]` (только для чтения)
-   **Описание:** Возвращает копию словаря с экспериментальными опциями.

#### `preferences`
-   **Тип:** `Dict[str, Any]` (только для чтения)
-   **Описание:** Возвращает копию словаря пользовательских настроек (prefs).

#### `debugger_address`
-   **Тип:** `Optional[str]`
-   **Описание:** Позволяет получить или установить адрес для подключения к уже запущенному экземпляру Chrome (например, `'127.0.0.1:9222'`).

#### `page_load_strategy`
-   **Тип:** `str`
-   **Описание:** Позволяет получить или установить стратегию загрузки страницы.
    -   `normal` (по умолчанию): ожидает полной загрузки документа.
    -   `eager`: ожидает загрузки DOM, но не ждет стили, изображения.
    -   `none`: не ожидает ничего.
-   **Пример:**
    ```python
    options.page_load_strategy = 'eager'
    ```

#### `timeouts`
-   **Тип:** `Dict[str, int]` (только для чтения)
-   **Описание:** Возвращает копию словаря с таймаутами.

### Методы

#### `add_argument(self, argument: str)`
Добавляет аргумент командной строки для запуска браузера.
-   **Пример:**
    ```python
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    ```

#### `remove_argument(self, argument: str)`
Удаляет ранее добавленный аргумент командной строки. Возвращает `True`, если удаление прошло успешно.

#### `add_extension(self, extension_path: str)`
Добавляет расширение, которое будет загружено при старте браузера.
-   **Параметры:**
    -   `extension_path` (`str`): Путь к файлу `.crx` или к распакованной папке с расширением.

#### `add_experimental_option(self, name: str, value: Any)`
Устанавливает экспериментальную опцию. Это мощный механизм для управления поведением браузера.
-   **Пример:**
    ```python
    # Отключить панель "Chrome is being controlled by automated test software"
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    ```

#### `set_preference(self, name: str, value: Any)`
Устанавливает пользовательскую настройку (pref) в профиле браузера.
-   **Пример:**
    ```python
    # Отключить всплывающие окна с уведомлениями
    options.set_preference('profile.default_content_setting_values.notifications', 2)
    ```

#### `set_timeout(self, timeout_type: str, seconds: int)`
Устанавливает таймауты для различных операций.
-   **Параметры:**
    -   `timeout_type` (`str`): Тип таймаута (`'implicit'`, `'page_load'`, `'script'`).
    -   `seconds` (`int`): Время в секундах.

#### `add_mobile_emulation(self, device_metrics: Dict[str, Any])`
Включает режим эмуляции мобильного устройства.
-   **Пример:**
    ```python
    mobile_emulation = {
        'deviceMetrics': {'width': 375, 'height': 812, 'pixelRatio': 3.0},
        'userAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) ...'
    }
    options.add_mobile_emulation(mobile_emulation)
    ```

#### `add_encoded_extension(self, extension: str)`
Добавляет расширение, закодированное в формате Base64.

#### `to_capabilities(self) -> Dict[str, Any]`
Преобразует все настроенные опции в словарь `capabilities`, совместимый с протоколом WebDriver. Этот метод используется для передачи опций драйверу при запуске.

#### `from_config(cls, config_data: Union[Dict, Path, str])`
Классовый метод для создания и настройки экземпляра `ChromiumOptions` из словаря, JSON-файла или JSON-строки.
-   **Пример:**
    ```python
    config = {
        "arguments": ["--headless"],
        "preferences": {"intl.accept_languages": "en,en_US"}
    }
    options = ChromiumOptions.from_config(config)
    ```

---

## Класс `Options`

Является дочерним классом `ChromiumOptions` и не добавляет новой функциональности. Он существует для обеспечения обратной совместимости и может использоваться как полная замена `ChromiumOptions`.

```python
from src.webdriver.pydoll.options import Options

# Использование идентично ChromiumOptions
options = Options()
options.add_argument('--headless')
```