# Модуль Chrome WebDriver

## Обзор

Модуль предоставляет класс `Chrome`, который расширяет базовый `webdriver.Chrome` для работы с браузером Chrome, 
обеспечивая дополнительные возможности и настройки.

## Детали

`Chrome` использует настройки из `chrome.json`, хранящегося в папке `src/webdriver/chrome`, для конфигурации драйвера, 
включая путь к chromedriver, настройки прокси, режим окна и другие опции. 

Модуль также предоставляет методы для работы с локаторами, JavaScript-скриптами и загрузкой страниц. 

## Классы

### `class Chrome`

**Описание**: Класс `Chrome` представляет собой расширение для `webdriver.Chrome` с дополнительной функциональностью. 
Он предоставляет возможность настройки драйвера, установки прокси, изменения режима окна и загрузки локаторов и JavaScript. 

**Наследование**:  `webdriver.Chrome`

**Атрибуты**:

- `driver_name: str = 'chrome'`: Имя драйвера (chrome).

**Параметры**:

- `profile_name: Optional[str] = None`: Имя пользовательского профиля Chrome.
- `chromedriver_version: Optional[str] = None`: Версия chromedriver.
- `user_agent: Optional[str] = None`: Пользовательский агент в формате строки.
- `proxy_file_path: Optional[str] = None`: Путь к файлу с прокси.
- `options: Optional[List[str]] = None`: Список опций для Chrome.
- `window_mode: Optional[str] = None`: Режим окна браузера (`windowless`, `kiosk`, `full_window` и т.д.).

**Методы**:

- `__init__(self, profile_name: Optional[str] = None, chromedriver_version: Optional[str] = None, user_agent: Optional[str] = None, proxy_file_path: Optional[str] = None, options: Optional[List[str]] = None, window_mode: Optional[str] = None, *args, **kwargs) -> None`: Конструктор класса `Chrome`. 
   - Загружает конфигурацию из `chrome.json`. 
   - Устанавливает путь к chromedriver.
   - Настраивает опции браузера, включая режим окна, прокси и пользовательский агент.
   - Инициализирует драйвер Chrome.
   - Загружает исполнители для локаторов и JavaScript-сценариев. 
- `set_proxy(self, options: Options) -> None`: Настраивает прокси из словаря, возвращаемого `get_proxies_dict`.
   - Получает список прокси из файла.
   - Проверяет прокси на работоспособность.
   - Добавляет настройки прокси к опциям Chrome.
- `_payload(self) -> None`: Загружает исполнители для локаторов и JavaScript-скриптов.
   - Инициализирует объекты `JavaScript` и `ExecuteLocator`.
   - Загружает методы для работы с локаторами, JavaScript-скриптами и загрузкой страниц.

## Примеры

```python
driver = Chrome(window_mode='full_window')
driver.get(r"https://google.com")
```

## Parameter Details

- `profile_name: Optional[str] = None`: Имя пользовательского профиля Chrome. Используется для загрузки настроек 
  из конкретного профиля.
- `chromedriver_version: Optional[str] = None`: Версия chromedriver. Используется для загрузки конкретной версии 
  chromedriver.
- `user_agent: Optional[str] = None`: Пользовательский агент в формате строки. Используется для подмены 
  пользовательского агента для имитации определенного браузера.
- `proxy_file_path: Optional[str] = None`: Путь к файлу с прокси. Используется для настройки прокси-сервера.
- `options: Optional[List[str]] = None`: Список дополнительных опций для Chrome. Используется для настройки 
  поведения браузера.
- `window_mode: Optional[str] = None`: Режим окна браузера. Возможные варианты: 
  - `windowless`: Безоконный режим.
  - `kiosk`: Режим киоска (полноэкранный режим).
  - `full_window`:  Режим полного окна.

## Как работает класс `Chrome`

Класс `Chrome` работает следующим образом:

1. При инициализации, он загружает конфигурацию из `chrome.json`, которая содержит настройки, такие как путь к 
   chromedriver, настройки прокси, режим окна и другие опции. 
2. Затем класс устанавливает путь к chromedriver, настраивает опции браузера, включая режим окна, прокси и 
   пользовательский агент, и инициализирует драйвер Chrome.
3. После инициализации драйвера, класс загружает исполнители для локаторов и JavaScript-сценариев, что 
   позволяет выполнять команды для взаимодействия с веб-страницей.
4. Класс предоставляет методы для настройки прокси, которые позволяют выбрать подходящий прокси из 
   предоставленного файла, а также методы для взаимодействия с веб-страницей через JavaScript-скрипты и 
   локаторы.

## Функции

### `set_proxy(self, options: Options) -> None`

**Назначение**: Настройка прокси из словаря, возвращаемого `get_proxies_dict`.

**Параметры**:

- `options`: Опции Chrome, в которые добавляются настройки прокси.

**Возвращаемое значение**: 
- `None`.

**Как работает функция**: 

- Функция получает список прокси из файла.
- Проверяет каждый прокси на работоспособность.
- Если найден рабочий прокси, он добавляется к опциям Chrome.

## Inner Functions

### `_payload(self) -> None`

**Назначение**: Загружает исполнители для локаторов и JavaScript-скриптов.

**Параметры**:
- `self`: Объект класса `Chrome`.

**Возвращаемое значение**:
- `None`.

**Как работает функция**:

- Функция инициализирует объекты `JavaScript` и `ExecuteLocator`.
- Затем она загружает методы для работы с локаторами, JavaScript-скриптами и загрузкой страниц.
  - `get_page_lang`: Извлекает язык страницы.
  - `ready_state`: Проверяет состояние готовности DOM.
  - `get_referrer`: Возвращает ссылку на предыдущую страницу.
  - `unhide_DOM_element`: Делает скрытый элемент DOM видимым.
  - `window_focus`: Перемещает фокус на окно.
  - `execute_locator`: Выполняет действия по локатору (например, клик, получение атрибута).
  - `get_webelement_as_screenshot`: Получает скриншот веб-элемента.
  - `get_webelement_by_locator`: Находит веб-элемент по локатору.
  - `get_attribute_by_locator`: Получает атрибут веб-элемента.
  - `send_message`: Отправляет текст в веб-элемент.

## Examples

```python
# Создание экземпляра Chrome WebDriver
driver = Chrome(window_mode='full_window')

# Открытие страницы
driver.get(r"https://google.com")

# Выполнение действия по локатору
result = driver.execute_locator({
  "attribute": null,
  "by": "XPATH",
  "selector": "//button[@id = 'closeXButton']",
  "if_list": "first",
  "use_mouse": false,
  "mandatory": false,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": "click()",
  "locator_description": "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
})

# Ожидание готовности DOM
driver.ready_state()

# Получение языка страницы
page_lang = driver.get_page_lang()

# Получение ссылки на предыдущую страницу
referrer = driver.get_referrer()

# Делаем скрытый элемент видимым
driver.unhide_DOM_element({
    "attribute": null,
    "by": "XPATH",
    "selector": "//div[@class='hidden-element']",
    "if_list": "first",
    "use_mouse": false,
    "mandatory": false,
    "timeout": 0,
    "timeout_for_event": "presence_of_element_located",
    "event": null,
    "locator_description": "Делаем элемент с классом `hidden-element` видимым."
})

# Перемещение фокуса на окно
driver.window_focus()

# Закрытие драйвера
driver.quit()
```