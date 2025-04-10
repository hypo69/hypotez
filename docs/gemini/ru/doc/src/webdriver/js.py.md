# Модуль `src.webdriver.js`

## Обзор

Модуль предоставляет набор JavaScript-утилит для взаимодействия с веб-страницей. Он расширяет возможности Selenium WebDriver, добавляя функции для манипуляции видимостью элементов DOM, получения информации о странице и управления фокусом браузера.

## Подробнее

Модуль предназначен для облегчения автоматизированного взаимодействия с веб-страницами посредством выполнения JavaScript-кода через Selenium WebDriver. Это позволяет решать задачи, которые сложно или невозможно выполнить стандартными средствами Selenium, например, принудительное отображение скрытых элементов или получение специфичной информации о странице.

## Классы

### `JavaScript`

**Описание**: Предоставляет JavaScript-утилиты для взаимодействия с веб-страницей.

**Атрибуты**:

- `driver` (WebDriver): Экземпляр Selenium WebDriver для выполнения JavaScript.

**Методы**:

- `unhide_DOM_element(element: WebElement) -> bool`: Делает невидимый элемент DOM видимым.
- `ready_state() -> str`: Возвращает статус загрузки документа.
- `window_focus() -> None`: Устанавливает фокус на окно браузера.
- `get_referrer() -> str`: Возвращает URL-адрес реферера текущего документа.
- `get_page_lang() -> str`: Возвращает язык текущей страницы.

#### `__init__`

```python
def __init__(self, driver: WebDriver):
    """
    Инициализирует экземпляр класса JavaScript с заданным драйвером WebDriver.

    Args:
        driver (WebDriver): Экземпляр Selenium WebDriver для выполнения JavaScript.
    """
    self.driver = driver
```

**Назначение**: Инициализирует класс `JavaScript`, принимая в качестве аргумента экземпляр WebDriver.

**Параметры**:

- `driver` (WebDriver): Экземпляр Selenium WebDriver, который будет использоваться для выполнения JavaScript-кода.

**Как работает функция**:
Функция сохраняет переданный экземпляр WebDriver в атрибуте `self.driver`, чтобы его можно было использовать для выполнения JavaScript-кода в других методах класса.

#### `unhide_DOM_element`

```python
def unhide_DOM_element(self, element: WebElement) -> bool:
    """
    Делает невидимый DOM элемент видимым, изменяя его свойства стиля.

    Args:
        element (WebElement): Объект WebElement, который нужно сделать видимым.

    Returns:
        bool: True, если скрипт выполнен успешно, False в противном случае.
    """
    script = """
    arguments[0].style.opacity = 1;
    arguments[0].style.transform = 'translate(0px, 0px) scale(1)';
    arguments[0].style.MozTransform = 'translate(0px, 0px) scale(1)';
    arguments[0].style.WebkitTransform = 'translate(0px, 0px) scale(1)';
    arguments[0].style.msTransform = 'translate(0px, 0px) scale(1)';
    arguments[0].style.OTransform = 'translate(0px, 0px) scale(1)';
    arguments[0].scrollIntoView(true);
    return true;
    """
    try:
        self.driver.execute_script(script, element)
        return True
    except Exception as ex:
        logger.error('Error in unhide_DOM_element: %s', ex)
        return False
```

**Назначение**: Изменяет стили DOM-элемента, чтобы сделать его видимым.

**Параметры**:

- `element` (WebElement): DOM-элемент, который нужно сделать видимым.

**Возвращает**:

- `bool`: `True`, если выполнение скрипта прошло успешно, `False` в случае ошибки.

**Вызывает исключения**:

- `Exception`: Логирует ошибку, если не удается выполнить JavaScript.

**Как работает функция**:

1. Определяет JavaScript-код, который устанавливает свойства `opacity`, `transform`, `MozTransform`, `WebkitTransform`, `msTransform`, `OTransform` элемента в значения, делающие его видимым. Также прокручивает элемент в область видимости.
2. Пытается выполнить этот JavaScript-код с помощью `driver.execute_script`, передавая `element` в качестве аргумента.
3. В случае успеха возвращает `True`.
4. Если во время выполнения скрипта возникает исключение, логирует ошибку с помощью `logger.error` и возвращает `False`.

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.js import JavaScript

# Создание экземпляра драйвера (пример с Chrome)
driver = webdriver.Chrome()
driver.get("https://example.com")

# Находим элемент, который изначально скрыт
hidden_element = driver.find_element("id", "hiddenElement")

# Создаем экземпляр JavaScript хелпера
js_helper = JavaScript(driver)

# Пытаемся сделать элемент видимым
result = js_helper.unhide_DOM_element(hidden_element)

if result:
    print("Элемент успешно отображен")
else:
    print("Не удалось отобразить элемент")

driver.quit()
```

#### `ready_state`

```python
@property
def ready_state(self) -> str:
    """
    Получает статус загрузки документа.

    Returns:
        str: 'loading', если документ еще загружается, 'complete', если загрузка завершена.
    """
    try:
        return self.driver.execute_script('return document.readyState;')
    except Exception as ex:
        logger.error('Error retrieving document.readyState: %s', ex)
        return ''
```

**Назначение**: Возвращает текущее состояние готовности документа (readyState).

**Возвращает**:

- `str`: Статус готовности документа: `"loading"`, если документ ещё загружается, `"complete"`, если загрузка завершена, или `""`, если произошла ошибка.

**Вызывает исключения**:

- `Exception`: Логирует ошибку, если не удается получить значение `document.readyState`.

**Как работает функция**:

1. Пытается выполнить JavaScript-код `return document.readyState;` с помощью `driver.execute_script`.
2. Возвращает полученное значение.
3. Если во время выполнения скрипта возникает исключение, логирует ошибку с помощью `logger.error` и возвращает пустую строку `""`.

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.js import JavaScript

# Создание экземпляра драйвера (пример с Chrome)
driver = webdriver.Chrome()
driver.get("https://example.com")

# Создаем экземпляр JavaScript хелпера
js_helper = JavaScript(driver)

# Получаем состояние готовности документа
ready_state = js_helper.ready_state

print(f"Состояние готовности документа: {ready_state}")

driver.quit()
```

#### `window_focus`

```python
def window_focus(self) -> None:
    """
    Устанавливает фокус на окно браузера, используя JavaScript.

    Попытки вывести окно браузера на передний план.
    """
    try:
        self.driver.execute_script('window.focus();')
    except Exception as ex:
        logger.error('Error executing window.focus(): %s', ex)
```

**Назначение**: Переводит фокус на текущее окно браузера.

**Как работает функция**:

1. Пытается выполнить JavaScript-код `window.focus();` с помощью `driver.execute_script`.
2. Если во время выполнения скрипта возникает исключение, логирует ошибку с помощью `logger.error`.

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.js import JavaScript

# Создание экземпляра драйвера (пример с Chrome)
driver = webdriver.Chrome()
driver.get("https://example.com")

# Создаем экземпляр JavaScript хелпера
js_helper = JavaScript(driver)

# Устанавливаем фокус на окно
js_helper.window_focus()

print("Фокус установлен на окно браузера")

driver.quit()
```

#### `get_referrer`

```python
def get_referrer(self) -> str:
    """
    Получает URL-адрес реферера текущего документа.

    Returns:
        str: URL-адрес реферера или пустая строка, если он недоступен.
    """
    try:
        return self.driver.execute_script('return document.referrer;') or ''
    except Exception as ex:
        logger.error('Error retrieving document.referrer: %s', ex)
        return ''
```

**Назначение**: Возвращает URL-адрес страницы, с которой пользователь перешел на текущую страницу.

**Возвращает**:

- `str`: URL-адрес реферера. Если реферер отсутствует или произошла ошибка, возвращается пустая строка.

**Вызывает исключения**:

- `Exception`: Логирует ошибку, если не удается получить значение `document.referrer`.

**Как работает функция**:

1. Пытается выполнить JavaScript-код `return document.referrer;` с помощью `driver.execute_script`.
2. Если значение `document.referrer` не определено (равно `null`), возвращает пустую строку.
3. Если во время выполнения скрипта возникает исключение, логирует ошибку с помощью `logger.error` и возвращает пустую строку.

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.js import JavaScript

# Создание экземпляра драйвера (пример с Chrome)
driver = webdriver.Chrome()
driver.get("https://example.com")

# Создаем экземпляр JavaScript хелпера
js_helper = JavaScript(driver)

# Получаем реферер
referrer = js_helper.get_referrer()

print(f"Реферер: {referrer}")

driver.quit()
```

#### `get_page_lang`

```python
def get_page_lang(self) -> str:
    """
    Получает язык текущей страницы.

    Returns:
        str: Код языка страницы или пустая строка, если он недоступен.
    """
    try:
        return self.driver.execute_script('return document.documentElement.lang;') or ''
    except Exception as ex:
        logger.error('Error retrieving document.documentElement.lang: %s', ex)
        return ''
```

**Назначение**: Возвращает язык, установленный для текущей страницы.

**Возвращает**:

- `str`: Код языка страницы (например, "en" или "ru"). Если язык не определен или произошла ошибка, возвращается пустая строка.

**Вызывает исключения**:

- `Exception`: Логирует ошибку, если не удается получить значение `document.documentElement.lang`.

**Как работает функция**:

1. Пытается выполнить JavaScript-код `return document.documentElement.lang;` с помощью `driver.execute_script`.
2. Если значение `document.documentElement.lang` не определено (равно `null`), возвращает пустую строку.
3. Если во время выполнения скрипта возникает исключение, логирует ошибку с помощью `logger.error` и возвращает пустую строку.

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.js import JavaScript

# Создание экземпляра драйвера (пример с Chrome)
driver = webdriver.Chrome()
driver.get("https://example.com")

# Создаем экземпляр JavaScript хелпера
js_helper = JavaScript(driver)

# Получаем язык страницы
page_lang = js_helper.get_page_lang()

print(f"Язык страницы: {page_lang}")

driver.quit()