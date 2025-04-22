# Модуль `js`

## Обзор

Модуль `js` предоставляет набор JavaScript-утилит для взаимодействия с веб-страницами с использованием Selenium WebDriver. Он расширяет возможности Selenium WebDriver, добавляя общие функции на основе JavaScript для взаимодействия с веб-страницами, включая манипуляции с видимостью элементов, получение информации о странице и управление фокусом браузера.

## Подробней

Модуль предназначен для упрощения выполнения задач, требующих JavaScript, таких как изменение стилей элементов DOM, получение данных о состоянии страницы и управление фокусом окна браузера. Это может быть полезно в ситуациях, когда стандартных средств Selenium WebDriver недостаточно.

## Классы

### `JavaScript`

**Описание**: Предоставляет JavaScript-утилиты для взаимодействия с веб-страницей.

**Атрибуты**:
- `driver` (WebDriver): Экземпляр Selenium WebDriver для выполнения JavaScript.

**Методы**:
- `unhide_DOM_element(element: WebElement) -> bool`: Делает невидимый элемент DOM видимым, изменяя его свойства стиля.
- `ready_state() -> str`: Возвращает статус загрузки документа.
- `window_focus() -> None`: Устанавливает фокус на окно браузера.
- `get_referrer() -> str`: Возвращает URL-адрес referrer текущего документа.
- `get_page_lang() -> str`: Возвращает язык текущей страницы.

#### `__init__`
```python
def __init__(self, driver: WebDriver):
    """
    Инициализирует JavaScript helper с экземпляром Selenium WebDriver.

    Args:
        driver (WebDriver): Selenium WebDriver instance to execute JavaScript.
    """
```

**Параметры**:
- `driver` (WebDriver): Экземпляр Selenium WebDriver для выполнения JavaScript.

**Принцип работы**:
- Конструктор класса `JavaScript` принимает экземпляр `WebDriver` и сохраняет его в атрибуте `self.driver`. Этот драйвер используется для выполнения JavaScript-кода на веб-странице.

#### `unhide_DOM_element`
```python
def unhide_DOM_element(self, element: WebElement) -> bool:
    """
    Делает невидимый DOM элемент видимым, изменяя его свойства стиля.

    Args:
        element (WebElement): The WebElement object to make visible.

    Returns:
        bool: True если скрипт выполнился успешно, False в противном случае.
    """
```

**Параметры**:
- `element` (WebElement): Объект `WebElement`, который нужно сделать видимым.

**Возвращает**:
- `bool`: `True`, если скрипт выполнен успешно, `False` в противном случае.

**Как работает функция**:
- Функция `unhide_DOM_element` принимает `WebElement` в качестве аргумента. Она выполняет JavaScript-код, который изменяет свойства стиля элемента, делая его видимым.
- Свойства, которые изменяются: `opacity`, `transform`, `MozTransform`, `WebkitTransform`, `msTransform`, `OTransform`.
- Также вызывается метод `scrollIntoView(true)`, чтобы прокрутить элемент в видимую область.
- Если в процессе выполнения скрипта возникает исключение, оно логируется, и функция возвращает `False`.

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.js import JavaScript

# Инициализация WebDriver (пример для Chrome)
driver = webdriver.Chrome()
driver.get("https://example.com")

# Поиск элемента, который изначально невидим
hidden_element = driver.find_element("id", "hiddenElement")

# Создание экземпляра JavaScript helper
js_helper = JavaScript(driver)

# Попытка сделать элемент видимым
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
    Возвращает статус загрузки документа.

    Returns:
        str: 'loading' если документ все еще загружается, 'complete' если загрузка завершена.
    """
```

**Возвращает**:
- `str`: `'loading'`, если документ все еще загружается, `'complete'`, если загрузка завершена.

**Как работает функция**:
- Функция `ready_state` использует JavaScript для получения значения свойства `document.readyState`, которое указывает на статус загрузки документа.
- Если в процессе выполнения скрипта возникает исключение, оно логируется, и функция возвращает пустую строку.

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.js import JavaScript

# Инициализация WebDriver (пример для Chrome)
driver = webdriver.Chrome()
driver.get("https://example.com")

# Создание экземпляра JavaScript helper
js_helper = JavaScript(driver)

# Получение статуса загрузки документа
status = js_helper.ready_state

print(f"Статус загрузки документа: {status}")

driver.quit()
```

#### `window_focus`
```python
def window_focus(self) -> None:
    """
    Устанавливает фокус на окно браузера.

    Попытка вывода окна браузера на передний план.
    """
```

**Как работает функция**:
- Функция `window_focus` использует JavaScript для установки фокуса на окно браузера.
- Если в процессе выполнения скрипта возникает исключение, оно логируется.

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.js import JavaScript

# Инициализация WebDriver (пример для Chrome)
driver = webdriver.Chrome()
driver.get("https://example.com")

# Создание экземпляра JavaScript helper
js_helper = JavaScript(driver)

# Установка фокуса на окно браузера
js_helper.window_focus()

print("Фокус установлен на окно браузера")

driver.quit()
```

#### `get_referrer`
```python
def get_referrer(self) -> str:
    """
    Возвращает URL-адрес referrer текущего документа.

    Returns:
        str: URL-адрес referrer, или пустая строка, если он недоступен.
    """
```

**Возвращает**:
- `str`: URL-адрес referrer, или пустая строка, если он недоступен.

**Как работает функция**:
- Функция `get_referrer` использует JavaScript для получения значения свойства `document.referrer`, которое содержит URL-адрес страницы, с которой пользователь перешел на текущую страницу.
- Если в процессе выполнения скрипта возникает исключение, оно логируется, и функция возвращает пустую строку.

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.js import JavaScript

# Инициализация WebDriver (пример для Chrome)
driver = webdriver.Chrome()
driver.get("https://example.com")

# Создание экземпляра JavaScript helper
js_helper = JavaScript(driver)

# Получение URL-адреса referrer
referrer = js_helper.get_referrer()

print(f"URL-адрес referrer: {referrer}")

driver.quit()
```

#### `get_page_lang`
```python
def get_page_lang(self) -> str:
    """
    Возвращает язык текущей страницы.

    Returns:
        str: Код языка страницы, или пустая строка, если он недоступен.
    """
```

**Возвращает**:
- `str`: Код языка страницы, или пустая строка, если он недоступен.

**Как работает функция**:
- Функция `get_page_lang` использует JavaScript для получения значения свойства `document.documentElement.lang`, которое содержит код языка текущей страницы.
- Если в процессе выполнения скрипта возникает исключение, оно логируется, и функция возвращает пустую строку.

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.js import JavaScript

# Инициализация WebDriver (пример для Chrome)
driver = webdriver.Chrome()
driver.get("https://example.com")

# Создание экземпляра JavaScript helper
js_helper = JavaScript(driver)

# Получение языка страницы
lang = js_helper.get_page_lang()

print(f"Язык страницы: {lang}")

driver.quit()