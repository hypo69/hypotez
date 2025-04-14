# Модуль `src.webdriver.js`

## Обзор

Модуль `src.webdriver.js` предоставляет набор JavaScript-утилит для взаимодействия с веб-страницей. Он расширяет возможности Selenium WebDriver, добавляя функции, основанные на JavaScript, для манипулирования видимостью элементов, получения информации о странице и управления фокусом браузера.

## Подробнее

Этот модуль предназначен для расширения возможностей Selenium WebDriver путем добавления общих JavaScript-функций для взаимодействия с веб-страницами, включая манипуляции с видимостью, получение информации о странице и управление фокусом браузера.

Основные возможности:

1.  Делает невидимые DOM-элементы видимыми для взаимодействия.
2.  Извлекает метаданные, такие как состояние готовности документа, referrer или язык страницы.
3.  Программно управляет фокусом окна браузера.

## Классы

### `JavaScript`

**Описание**: Предоставляет JavaScript-утилиты для взаимодействия с веб-страницей.

**Принцип работы**: Класс `JavaScript` инициализируется экземпляром Selenium WebDriver и предоставляет методы для выполнения JavaScript-кода в контексте текущей веб-страницы. Это позволяет выполнять действия, которые сложно или невозможно выполнить с помощью стандартных средств Selenium WebDriver.

**Методы**:

*   `__init__`: Инициализирует экземпляр класса `JavaScript`.
*   `unhide_DOM_element`: Делает невидимый DOM-элемент видимым.
*   `ready_state`: Получает статус загрузки документа.
*   `window_focus`: Устанавливает фокус на окно браузера.
*   `get_referrer`: Получает URL-адрес referrer текущего документа.
*   `get_page_lang`: Получает язык текущей страницы.

### `JavaScript.__init__(self, driver: WebDriver)`

```python
    def __init__(self, driver: WebDriver):
        """Initializes the JavaScript helper with a Selenium WebDriver instance.

        Args:
            driver (WebDriver): Selenium WebDriver instance to execute JavaScript.
        """
        self.driver = driver
```

**Назначение**: Инициализирует класс `JavaScript` с экземпляром `WebDriver`.

**Параметры**:

*   `driver` (`WebDriver`): Экземпляр `WebDriver`, используемый для выполнения JavaScript.

**Как работает функция**:

1.  Функция `__init__` является конструктором класса `JavaScript`.
2.  Она принимает экземпляр `WebDriver` в качестве аргумента.
3.  Сохраняет предоставленный экземпляр `WebDriver` в атрибуте `self.driver` для дальнейшего использования.

```
A[Инициализация класса JavaScript]
|
B[Сохранение экземпляра WebDriver в self.driver]
```

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.js import JavaScript

# Инициализация WebDriver (пример с Chrome)
driver = webdriver.Chrome()

# Создание экземпляра JavaScript с использованием WebDriver
js_executor = JavaScript(driver)
```

### `JavaScript.unhide_DOM_element(self, element: WebElement) -> bool`

```python
    def unhide_DOM_element(self, element: WebElement) -> bool:
        """Makes an invisible DOM element visible by modifying its style properties.

        Args:
            element (WebElement): The WebElement object to make visible.

        Returns:
            bool: True if the script executes successfully, False otherwise.
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

*   `element` (`WebElement`): Объект `WebElement`, который нужно сделать видимым.

**Возвращает**:

*   `bool`: `True`, если скрипт выполнен успешно, `False` в противном случае.

**Вызывает исключения**:

*   `Exception`: Если возникает ошибка при выполнении JavaScript-скрипта.

**Как работает функция**:

1.  Функция `unhide_DOM_element` принимает объект `WebElement` в качестве аргумента.
2.  Определяет JavaScript-скрипт, который изменяет свойства стиля элемента, чтобы сделать его видимым. Скрипт устанавливает `opacity` в 1, `transform` в `translate(0px, 0px) scale(1)` и вызывает `scrollIntoView(true)` для прокрутки элемента в видимую область.
3.  Пытается выполнить JavaScript-скрипт с использованием `self.driver.execute_script`.
4.  Если скрипт выполняется успешно, возвращает `True`.
5.  Если возникает исключение, логирует ошибку с использованием `logger.error` и возвращает `False`.

```
A[Принимает WebElement]
|
B[Определяет JavaScript-скрипт для изменения свойств стиля элемента]
|
C[Пытается выполнить JavaScript-скрипт]
|
D[Скрипт выполнен успешно?]
|
E[Возвращает True]                                       F[Логирует ошибку и возвращает False]
```

**Примеры**:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from src.webdriver.js import JavaScript

# Инициализация WebDriver (пример с Chrome)
driver = webdriver.Chrome()
driver.get("https://example.com")  # Откройте нужную страницу

# Создание экземпляра JavaScript с использованием WebDriver
js_executor = JavaScript(driver)

# Найти элемент, который изначально невидимый
element = driver.find_element(By.ID, "hiddenElement")

# Сделать элемент видимым
result = js_executor.unhide_DOM_element(element)

if result:
    print("Элемент успешно сделан видимым.")
else:
    print("Не удалось сделать элемент видимым.")
```

### `JavaScript.ready_state(self) -> str`

```python
    @property
    def ready_state(self) -> str:
        """Retrieves the document loading status.

        Returns:
            str: 'loading' if the document is still loading, 'complete' if loading is finished.
        """
        try:
            return self.driver.execute_script('return document.readyState;')
        except Exception as ex:
            logger.error('Error retrieving document.readyState: %s', ex)
            return ''
```

**Назначение**: Получает статус загрузки документа.

**Возвращает**:

*   `str`: `'loading'`, если документ еще загружается, `'complete'`, если загрузка завершена, или пустую строку в случае ошибки.

**Вызывает исключения**:

*   `Exception`: Если возникает ошибка при выполнении JavaScript-скрипта.

**Как работает функция**:

1.  Функция `ready_state` пытается выполнить JavaScript-скрипт `return document.readyState;`, который возвращает текущий статус загрузки документа.
2.  Если скрипт выполняется успешно, возвращает полученный статус.
3.  Если возникает исключение, логирует ошибку с использованием `logger.error` и возвращает пустую строку.

```
A[Пытается выполнить JavaScript-скрипт для получения document.readyState]
|
B[Скрипт выполнен успешно?]
|
C[Возвращает статус загрузки]                                       D[Логирует ошибку и возвращает пустую строку]
```

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.js import JavaScript

# Инициализация WebDriver (пример с Chrome)
driver = webdriver.Chrome()
driver.get("https://example.com")

# Создание экземпляра JavaScript с использованием WebDriver
js_executor = JavaScript(driver)

# Получение статуса загрузки документа
ready_state = js_executor.ready_state

print(f"Статус загрузки документа: {ready_state}")
```

### `JavaScript.window_focus(self) -> None`

```python
    def window_focus(self) -> None:
        """Sets focus to the browser window using JavaScript.

        Attempts to bring the browser window to the foreground.
        """
        try:
            self.driver.execute_script('window.focus();')
        except Exception as ex:
            logger.error('Error executing window.focus(): %s', ex)
```

**Назначение**: Устанавливает фокус на окно браузера с помощью JavaScript.

**Как работает функция**:

1.  Функция `window_focus` пытается выполнить JavaScript-скрипт `window.focus();`, который устанавливает фокус на текущее окно браузера.
2.  Если возникает исключение, логирует ошибку с использованием `logger.error`.

```
A[Пытается выполнить JavaScript-скрипт для установки фокуса на окно браузера]
|
B[Возникла ошибка?]
|
C[Логирует ошибку]
```

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.js import JavaScript

# Инициализация WebDriver (пример с Chrome)
driver = webdriver.Chrome()
driver.get("https://example.com")

# Создание экземпляра JavaScript с использованием WebDriver
js_executor = JavaScript(driver)

# Установка фокуса на окно браузера
js_executor.window_focus()
```

### `JavaScript.get_referrer(self) -> str`

```python
    def get_referrer(self) -> str:
        """Retrieves the referrer URL of the current document.

        Returns:
            str: The referrer URL, or an empty string if unavailable.
        """
        try:
            return self.driver.execute_script('return document.referrer;') or ''
        except Exception as ex:
            logger.error('Error retrieving document.referrer: %s', ex)
            return ''
```

**Назначение**: Получает URL-адрес referrer текущего документа.

**Возвращает**:

*   `str`: URL-адрес referrer или пустую строку, если он недоступен.

**Вызывает исключения**:

*   `Exception`: Если возникает ошибка при выполнении JavaScript-скрипта.

**Как работает функция**:

1.  Функция `get_referrer` пытается выполнить JavaScript-скрипт `return document.referrer;`, который возвращает URL-адрес referrer текущего документа.
2.  Если скрипт выполняется успешно, возвращает полученный URL-адрес. Если URL-адрес отсутствует, возвращает пустую строку.
3.  Если возникает исключение, логирует ошибку с использованием `logger.error` и возвращает пустую строку.

```
A[Пытается выполнить JavaScript-скрипт для получения document.referrer]
|
B[Скрипт выполнен успешно?]
|
C[Возвращает URL-адрес referrer]                                       D[Логирует ошибку и возвращает пустую строку]
```

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.js import JavaScript

# Инициализация WebDriver (пример с Chrome)
driver = webdriver.Chrome()
driver.get("https://example.com")

# Создание экземпляра JavaScript с использованием WebDriver
js_executor = JavaScript(driver)

# Получение URL-адреса referrer
referrer = js_executor.get_referrer()

print(f"URL-адрес referrer: {referrer}")
```

### `JavaScript.get_page_lang(self) -> str`

```python
    def get_page_lang(self) -> str:
        """Retrieves the language of the current page.

        Returns:
            str: The language code of the page, or an empty string if unavailable.
        """
        try:
            return self.driver.execute_script('return document.documentElement.lang;') or ''
        except Exception as ex:
            logger.error('Error retrieving document.documentElement.lang: %s', ex)
            return ''
```

**Назначение**: Получает язык текущей страницы.

**Возвращает**:

*   `str`: Код языка страницы или пустую строку, если он недоступен.

**Вызывает исключения**:

*   `Exception`: Если возникает ошибка при выполнении JavaScript-скрипта.

**Как работает функция**:

1.  Функция `get_page_lang` пытается выполнить JavaScript-скрипт `return document.documentElement.lang;`, который возвращает код языка текущей страницы.
2.  Если скрипт выполняется успешно, возвращает полученный код языка. Если код языка отсутствует, возвращает пустую строку.
3.  Если возникает исключение, логирует ошибку с использованием `logger.error` и возвращает пустую строку.

```
A[Пытается выполнить JavaScript-скрипт для получения document.documentElement.lang]
|
B[Скрипт выполнен успешно?]
|
C[Возвращает код языка страницы]                                       D[Логирует ошибку и возвращает пустую строку]
```

**Примеры**:

```python
from selenium import webdriver
from src.webdriver.js import JavaScript

# Инициализация WebDriver (пример с Chrome)
driver = webdriver.Chrome()
driver.get("https://example.com")

# Создание экземпляра JavaScript с использованием WebDriver
js_executor = JavaScript(driver)

# Получение языка страницы
page_lang = js_executor.get_page_lang()

print(f"Язык страницы: {page_lang}")