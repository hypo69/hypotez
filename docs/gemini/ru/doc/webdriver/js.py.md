# Модуль для работы с JavaScript в Selenium (js.py)

## Обзор

Этот модуль предоставляет JavaScript утилиты для взаимодействия с веб-страницей, расширяя возможности Selenium WebDriver.

## Подробней

Модуль `src/webdriver/js.py` предназначен для расширения возможностей Selenium WebDriver путем добавления общих JavaScript-функций для взаимодействия с веб-страницами. Он включает функции для управления видимостью DOM-элементов, получения информации о странице (например, статуса загрузки, referrer, языка) и управления фокусом окна браузера.

## Классы

### `JavaScript`

**Описание**: Предоставляет JavaScript утилиты для взаимодействия с веб-страницей.

**Атрибуты**:

-   `driver` (WebDriver): Экземпляр Selenium WebDriver, используемый для выполнения JavaScript-кода.

**Методы**:

-   `__init__(self, driver: WebDriver)`: Инициализирует объект `JavaScript` с экземпляром Selenium WebDriver.
-   `unhide_DOM_element(self, element: WebElement) -> bool`: Делает невидимый DOM-элемент видимым, изменяя его свойства стиля.
-   `ready_state(self) -> str`: Возвращает статус загрузки документа.
-   `window_focus(self) -> None`: Устанавливает фокус на окно браузера, используя JavaScript.
-   `get_referrer(self) -> str`: Возвращает URL-адрес страницы, с которой перешли на текущую.
-   `get_page_lang(self) -> str`: Возвращает язык текущей страницы.

#### `__init__`

**Назначение**: Инициализирует объект `JavaScript` с экземпляром Selenium WebDriver.

```python
def __init__(self, driver: WebDriver):
    """Initializes the JavaScript helper with a Selenium WebDriver instance.

    Args:
        driver (WebDriver): Selenium WebDriver instance to execute JavaScript.
    """
    ...
```

**Параметры**:

-   `driver` (WebDriver): Экземпляр Selenium WebDriver, используемый для выполнения JavaScript-кода.

**Как работает функция**:

1.  Принимает экземпляр `WebDriver` в качестве аргумента.
2.  Сохраняет экземпляр `WebDriver` в атрибуте `self.driver`.

#### `unhide_DOM_element`

**Назначение**: Делает невидимый DOM-элемент видимым, изменяя его свойства стиля.

```python
def unhide_DOM_element(self, element: WebElement) -> bool:
    """Makes an invisible DOM element visible by modifying its style properties.

    Args:
        element (WebElement): The WebElement object to make visible.

    Returns:
        bool: True if the script executes successfully, False otherwise.
    """
    ...
```

**Параметры**:

-   `element` (WebElement): Объект `WebElement`, который нужно сделать видимым.

**Возвращает**:

-   `bool`: `True`, если скрипт выполнен успешно, `False` - в противном случае.

**Как работает функция**:

1.  Определяет JavaScript-код, который изменяет свойства стиля элемента, чтобы сделать его видимым (устанавливает `opacity = 1`, `transform = 'translate(0px, 0px) scale(1)'` и прокручивает элемент в поле зрения).
2.  Выполняет JavaScript-код, используя `self.driver.execute_script(script, element)`.
3.  Логирует информацию об ошибках, используя `logger.error`.

#### `ready_state`

**Назначение**: Возвращает статус загрузки документа.

```python
@property
def ready_state(self) -> str:
    """Retrieves the document loading status.

    Returns:
        str: 'loading' if the document is still loading, 'complete' if loading is finished.
    """
    ...
```

**Возвращает**:

-   `str`: `'loading'`, если документ еще загружается, `'complete'`, если загрузка завершена.

**Как работает функция**:

1.  Выполняет JavaScript-код `return document.readyState;`, чтобы получить статус загрузки документа.
2.  Логирует информацию об ошибках, используя `logger.error`.

#### `window_focus`

**Назначение**: Устанавливает фокус на окно браузера, используя JavaScript.

```python
def window_focus(self) -> None:
    """Sets focus to the browser window using JavaScript.

    Attempts to bring the browser window to the foreground.
    """
    ...
```

**Как работает функция**:

1.  Выполняет JavaScript-код `window.focus();`, чтобы установить фокус на окно браузера.
2.  Логирует информацию об ошибках, используя `logger.error`.

#### `get_referrer`

**Назначение**: Возвращает URL-адрес страницы, с которой перешли на текущую.

```python
def get_referrer(self) -> str:
    """Retrieves the referrer URL of the current document.

    Returns:
        str: The referrer URL, or an empty string if unavailable.
    """
    ...
```

**Возвращает**:

-   `str`: URL-адрес страницы, с которой перешли на текущую, или пустая строка, если referrer недоступен.

**Как работает функция**:

1.  Выполняет JavaScript-код `return document.referrer;`, чтобы получить URL-адрес referrer.
2.  Логирует информацию об ошибках, используя `logger.error`.

#### `get_page_lang`

**Назначение**: Возвращает язык текущей страницы.

```python
def get_page_lang(self) -> str:
    """Retrieves the language of the current page.

    Returns:
        str: The language code of the page, or an empty string if unavailable.
    """
    ...
```

**Возвращает**:

-   `str`: Код языка страницы или пустая строка, если язык не определен.

**Как работает функция**:

1.  Выполняет JavaScript-код `return document.documentElement.lang;`, чтобы получить код языка страницы.
2.  Логирует информацию об ошибках, используя `logger.error`.

## Переменные модуля

-   В данном модуле отсутствуют переменные, за исключением импортированных модулей.

## Пример использования

```python
from src.webdriver.driver import Driver
from src.webdriver.js import JavaScript
from selenium.webdriver import Firefox

# Инициализация драйвера
driver = Driver(Firefox)
js = JavaScript(driver.driver)

# Пример использования функции unhide_DOM_element
element = driver.find_element("id", "myElement")
js.unhide_DOM_element(element)

# Пример получения статуса загрузки страницы
ready_state = js.ready_state
print(f"Ready state: {ready_state}")

driver.quit()
```

## Взаимосвязь с другими частями проекта

-   Модуль `src/webdriver/js.py` зависит от библиотеки `selenium` для взаимодействия с веб-браузерами и выполнения JavaScript-кода, от модуля `header` для определения путей (хотя он не используется явно) и от модуля `src.logger.logger` для логирования.
-   Он предназначен для использования в других модулях, работающих с веб-драйверами, для выполнения более сложных операций на веб-страницах.