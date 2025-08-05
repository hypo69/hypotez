# Модуль `js`

## Обзор

Модуль `js` предоставляет JavaScript-утилиты для взаимодействия с веб-страницей. Он предназначен для расширения возможностей Selenium WebDriver, добавляя общие функции на основе JavaScript для взаимодействия с веб-страницами, включая манипуляции с видимостью, получение информации о странице и управление фокусом браузера.

## Подробней

Этот модуль расширяет возможности Selenium WebDriver, предоставляя JavaScript-функции для управления видимостью элементов DOM, получения метаданных страницы и управления фокусом браузера. Он упрощает выполнение JavaScript-кода в контексте веб-страницы через WebDriver.

## Классы

### `JavaScript`

**Описание**: Предоставляет JavaScript-утилиты для взаимодействия с веб-страницей.

**Атрибуты**:
- `driver` (WebDriver): Экземпляр Selenium WebDriver для выполнения JavaScript.

**Методы**:
- `unhide_DOM_element(element: WebElement) -> bool`: Делает невидимый DOM-элемент видимым, изменяя его свойства стиля.
- `ready_state -> str`: Возвращает статус загрузки документа.
- `window_focus() -> None`: Устанавливает фокус на окно браузера.
- `get_referrer() -> str`: Возвращает URL-адрес реферера текущего документа.
- `get_page_lang() -> str`: Возвращает язык текущей страницы.

### `__init__`

```python
def __init__(self, driver: WebDriver):
    """Инициализирует JavaScript helper с экземпляром Selenium WebDriver.

    Args:
        driver (WebDriver): Экземпляр Selenium WebDriver для выполнения JavaScript.
    """
    self.driver = driver
```

**Назначение**: Инициализирует экземпляр класса `JavaScript`.

**Параметры**:
- `driver` (WebDriver): Экземпляр Selenium WebDriver для выполнения JavaScript.

**Как работает функция**:
Функция инициализирует класс `JavaScript`, сохраняя переданный экземпляр `WebDriver` в атрибуте `self.driver`. Это позволяет использовать `driver` для выполнения JavaScript-кода на веб-странице.

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.js import JavaScript

# Создание экземпляра WebDriver (пример с Chrome)
driver = webdriver.Chrome()
driver.get("https://example.com")

# Создание экземпляра JavaScript helper
js_helper = JavaScript(driver)
```

### `unhide_DOM_element`

```python
def unhide_DOM_element(self, element: WebElement) -> bool:
    """Делает невидимый DOM-элемент видимым, изменяя его свойства стиля.

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

**Назначение**: Делает невидимый DOM-элемент видимым, изменяя его свойства стиля.

**Параметры**:
- `element` (WebElement): Объект WebElement, который нужно сделать видимым.

**Возвращает**:
- `bool`: `True`, если скрипт выполнен успешно, `False` в противном случае.

**Вызывает исключения**:
- `Exception`: Логируется в случае ошибки выполнения JavaScript.

**Как работает функция**:
Функция выполняет JavaScript-код, который изменяет стили элемента DOM, делая его видимым. Она устанавливает свойства `opacity`, `transform`, `MozTransform`, `WebkitTransform`, `msTransform` и `OTransform` элемента, а также прокручивает элемент в поле зрения. В случае ошибки выполнения JavaScript, функция логирует ошибку и возвращает `False`.

**Примеры**:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from src.webdriver.js import JavaScript

# Создание экземпляра WebDriver (пример с Chrome)
driver = webdriver.Chrome()
driver.get("https://example.com")

# Создание экземпляра JavaScript helper
js_helper = JavaScript(driver)

# Поиск элемента, который нужно сделать видимым
element = driver.find_element(By.ID, "hiddenElement")

# Сделать элемент видимым
js_helper.unhide_DOM_element(element)
```

### `ready_state`

```python
@property
def ready_state(self) -> str:
    """Получает статус загрузки документа.

    Returns:
        str: 'loading', если документ все еще загружается, 'complete', если загрузка завершена.
    """
    try:
        return self.driver.execute_script('return document.readyState;')
    except Exception as ex:
        logger.error('Error retrieving document.readyState: %s', ex)
        return ''
```

**Назначение**: Получает статус загрузки документа.

**Возвращает**:
- `str`: `'loading'`, если документ все еще загружается, `'complete'`, если загрузка завершена, или пустая строка в случае ошибки.

**Вызывает исключения**:
- `Exception`: Логируется в случае ошибки выполнения JavaScript.

**Как работает функция**:
Функция выполняет JavaScript-код, который возвращает значение свойства `document.readyState`. Это свойство указывает на статус загрузки документа. Если возникает ошибка при выполнении JavaScript, функция логирует ошибку и возвращает пустую строку.

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.js import JavaScript

# Создание экземпляра WebDriver (пример с Chrome)
driver = webdriver.Chrome()
driver.get("https://example.com")

# Создание экземпляра JavaScript helper
js_helper = JavaScript(driver)

# Получение статуса загрузки документа
ready_state = js_helper.ready_state
print(f"Ready state: {ready_state}")
```

### `window_focus`

```python
def window_focus(self) -> None:
    """Устанавливает фокус на окно браузера с использованием JavaScript.

    Попытки вывода окна браузера на передний план.
    """
    try:
        self.driver.execute_script('window.focus();')
    except Exception as ex:
        logger.error('Error executing window.focus(): %s', ex)
```

**Назначение**: Устанавливает фокус на окно браузера.

**Вызывает исключения**:
- `Exception`: Логируется в случае ошибки выполнения JavaScript.

**Как работает функция**:
Функция выполняет JavaScript-код, который устанавливает фокус на окно браузера, вызывая метод `window.focus()`. Если возникает ошибка при выполнении JavaScript, функция логирует ошибку.

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.js import JavaScript

# Создание экземпляра WebDriver (пример с Chrome)
driver = webdriver.Chrome()
driver.get("https://example.com")

# Создание экземпляра JavaScript helper
js_helper = JavaScript(driver)

# Установка фокуса на окно браузера
js_helper.window_focus()
```

### `get_referrer`

```python
def get_referrer(self) -> str:
    """Получает URL-адрес реферера текущего документа.

    Returns:
        str: URL-адрес реферера или пустая строка, если он недоступен.
    """
    try:
        return self.driver.execute_script('return document.referrer;') or ''
    except Exception as ex:
        logger.error('Error retrieving document.referrer: %s', ex)
        return ''
```

**Назначение**: Получает URL-адрес реферера текущего документа.

**Возвращает**:
- `str`: URL-адрес реферера или пустая строка, если он недоступен.

**Вызывает исключения**:
- `Exception`: Логируется в случае ошибки выполнения JavaScript.

**Как работает функция**:
Функция выполняет JavaScript-код, который возвращает значение свойства `document.referrer`. Это свойство содержит URL-адрес страницы, с которой пользователь перешел на текущую страницу. Если возникает ошибка при выполнении JavaScript, функция логирует ошибку и возвращает пустую строку.

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.js import JavaScript

# Создание экземпляра WebDriver (пример с Chrome)
driver = webdriver.Chrome()
driver.get("https://example.com")

# Создание экземпляра JavaScript helper
js_helper = JavaScript(driver)

# Получение URL-адреса реферера
referrer = js_helper.get_referrer()
print(f"Referrer: {referrer}")
```

### `get_page_lang`

```python
def get_page_lang(self) -> str:
    """Получает язык текущей страницы.

    Returns:
        str: Код языка страницы или пустая строка, если он недоступен.
    """
    try:
        return self.driver.execute_script('return document.documentElement.lang;') or ''
    except Exception as ex:
        logger.error('Error retrieving document.documentElement.lang: %s', ex)
        return ''
```

**Назначение**: Получает язык текущей страницы.

**Возвращает**:
- `str`: Код языка страницы или пустая строка, если он недоступен.

**Вызывает исключения**:
- `Exception`: Логируется в случае ошибки выполнения JavaScript.

**Как работает функция**:
Функция выполняет JavaScript-код, который возвращает значение свойства `document.documentElement.lang`. Это свойство содержит код языка, установленный для текущей страницы. Если возникает ошибка при выполнении JavaScript, функция логирует ошибку и возвращает пустую строку.

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.js import JavaScript

# Создание экземпляра WebDriver (пример с Chrome)
driver = webdriver.Chrome()
driver.get("https://example.com")

# Создание экземпляра JavaScript helper
js_helper = JavaScript(driver)

# Получение языка страницы
page_lang = js_helper.get_page_lang()
print(f"Page language: {page_lang}")