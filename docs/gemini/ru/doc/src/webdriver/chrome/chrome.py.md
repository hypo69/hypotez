# Модуль `src.webdriver.chrome.chrome`

## Обзор

Модуль `src.webdriver.chrome.chrome` предоставляет расширение для `webdriver.Chrome` с дополнительной функциональностью, необходимой для работы с веб-драйвером Chrome. 

## Подробнее

Этот модуль расширяет стандартный `webdriver.Chrome` с помощью следующих функций:

- **Настройка пользовательского профиля:** Возможность указать имя профиля Chrome, который будет использоваться.
- **Управление прокси:** Поддержка использования прокси-серверов.
- **Настройка пользовательского агента:**  Возможность задать пользовательский агент для Chrome.
- **Настройка режима окна:**  Возможность выбрать режим окна браузера (`windowless`, `kiosk`, `full_window` и т.д.).

## Классы

### `Chrome`

**Описание**: Расширение для `webdriver.Chrome` с дополнительной функциональностью.

**Наследует**: `selenium.webdriver.chrome.webdriver.WebDriver`

**Атрибуты**:

- `driver_name: str = 'chrome'`: Имя драйвера (используется для идентификации драйвера).

**Параметры**:

- `profile_name: Optional[str] = None`: Имя пользовательского профиля Chrome.
- `chromedriver_version: Optional[str] = None`: Версия chromedriver.
- `user_agent: Optional[str] = None`: Пользовательский агент в формате строки.
- `proxy_file_path: Optional[str] = None`: Путь к файлу с прокси.
- `options: Optional[List[str]] = None`: Список опций для Chrome.
- `window_mode: Optional[str] = None`: Режим окна браузера (`windowless`, `kiosk`, `full_window` и т.д.).

**Принцип работы**:

- Конструктор класса `Chrome` инициализирует объект Chrome с необходимыми параметрами.
- Сначала загружаются настройки Chrome из файла `chrome.json`, расположенного в `src/webdriver/chrome`.
- Затем устанавливается путь к chromedriver, считываемый из конфигурационного файла.
- После этого создается объект `Options` для Chrome и в него добавляются настройки:
    - Опции из файла настроек.
    - Режим окна (если указан).
    - Опции, переданные при инициализации класса.
    - Пользовательский агент.
    - Прокси-сервер (если включены).
- Настраивается директория профиля Chrome.
- В конце происходит запуск драйвера и инициализация дополнительной функциональности, необходимой для работы с локаторами и JavaScript.

**Методы**:

- `__init__(self, profile_name: Optional[str] = None, chromedriver_version: Optional[str] = None, user_agent: Optional[str] = None, proxy_file_path: Optional[str] = None, options: Optional[List[str]] = None, window_mode: Optional[str] = None, *args, **kwargs) -> None`: Конструктор класса `Chrome`.
- `set_proxy(self, options: Options) -> None`: Настройка прокси из словаря, возвращаемого `get_proxies_dict`.
- `_payload(self) -> None`: Загрузка исполнителей для локаторов и JavaScript сценариев.

**Примеры**:

```python
from src.webdriver import Chrome

# Создание инстанса драйвера Chrome с полным окном
driver = Chrome(window_mode='full_window')

# Открытие Google
driver.get('https://google.com')

# Закрытие браузера
driver.quit()
```

## Методы класса

### `set_proxy(self, options: Options) -> None`

**Описание**: Настройка прокси из словаря, возвращаемого `get_proxies_dict`.

**Параметры**:

- `options: Options`: Опции Chrome, в которые добавляются настройки прокси.

**Принцип работы**:

- Получение словаря прокси из функции `get_proxies_dict`.
- Создание списка всех прокси из словаря.
- Перебор прокси из списка для поиска рабочего.
- Если рабочий прокси найден, то он устанавливается в опции Chrome в зависимости от типа протокола.
- Если рабочий прокси не найден, то выводится предупреждающее сообщение.

**Примеры**:

```python
from src.webdriver import Chrome

# Создание инстанса драйвера Chrome
driver = Chrome()

# Настройка прокси для драйвера
driver.set_proxy(driver.options)

# Открытие веб-сайта
driver.get('https://www.example.com')
```

### `_payload(self) -> None`

**Описание**: Загрузка исполнителей для локаторов и JavaScript сценариев.

**Принцип работы**:

- Создание объекта `JavaScript` для выполнения JavaScript-кода.
- Инициализация атрибутов класса `Chrome` с помощью методов из `JavaScript`:
    - `get_page_lang`: Получение языка страницы.
    - `ready_state`: Проверка готовности документа.
    - `get_referrer`: Получение реферера.
    - `unhide_DOM_element`: Показ скрытых элементов DOM.
    - `window_focus`: Переключение фокуса на окно.
- Создание объекта `ExecuteLocator` для выполнения действий с локаторами.
- Инициализация атрибутов класса `Chrome` с помощью методов из `ExecuteLocator`:
    - `execute_locator`: Выполнение действий с локатором.
    - `get_webelement_as_screenshot`: Получение скриншота элемента по локатору.
    - `get_webelement_by_locator`: Получение элемента по локатору.
    - `get_attribute_by_locator`: Получение атрибута элемента по локатору.
    - `send_message`: Отправка сообщения элементу по локатору.

**Примеры**:

```python
from src.webdriver import Chrome

# Создание инстанса драйвера Chrome
driver = Chrome()

# Получение языка страницы
page_lang = driver.get_page_lang()

# Проверка готовности документа
ready_state = driver.ready_state()

# Выполнение действий с локатором
result = driver.execute_locator({'selector': '#my-element', 'event': 'click()'})
```

## Параметры класса

- `profile_name: Optional[str] = None`: Имя пользовательского профиля Chrome. Если не указано, используется стандартный профиль.
- `chromedriver_version: Optional[str] = None`: Версия chromedriver. Если не указано, используется последняя версия.
- `user_agent: Optional[str] = None`: Пользовательский агент. Если не указано, генерируется случайный пользовательский агент.
- `proxy_file_path: Optional[str] = None`: Путь к файлу с прокси. Если не указано, прокси не используются.
- `options: Optional[List[str]] = None`: Список дополнительных опций для Chrome. 
- `window_mode: Optional[str] = None`: Режим окна браузера (`windowless`, `kiosk`, `full_window` и т.д.). Если не указано, используется значение из файла конфигурации.

## Примеры

### Создание инстанса драйвера Chrome с полным окном:

```python
from src.webdriver import Chrome

# Создание инстанса драйвера Chrome с полным окном
driver = Chrome(window_mode='full_window')

# Открытие Google
driver.get('https://google.com')

# Закрытие браузера
driver.quit()
```

### Настройка прокси для драйвера:

```python
from src.webdriver import Chrome

# Создание инстанса драйвера Chrome
driver = Chrome()

# Настройка прокси для драйвера
driver.set_proxy(driver.options)

# Открытие веб-сайта
driver.get('https://www.example.com')
```

### Выполнение действий с локатором:

```python
from src.webdriver import Chrome

# Создание инстанса драйвера Chrome
driver = Chrome()

# Выполнение действий с локатором
result = driver.execute_locator({'selector': '#my-element', 'event': 'click()'})