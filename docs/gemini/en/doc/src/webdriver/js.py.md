# Модуль `js`

## Обзор

Модуль `js` предоставляет утилиты на JavaScript для взаимодействия с веб-страницей. Он предназначен для расширения возможностей Selenium WebDriver путем добавления общих функций на основе JavaScript для взаимодействия с веб-страницами, включая манипуляции с видимостью, получение информации о странице и управление фокусом браузера.

## Подробнее

Этот модуль предназначен для расширения возможностей Selenium WebDriver путем добавления общих функций на основе JavaScript для взаимодействия с веб-страницами, включая манипуляции с видимостью, получение информации о странице и управление фокусом браузера.

## Классы

### `JavaScript`

**Описание**: Предоставляет утилиты JavaScript для взаимодействия с веб-страницей.

**Атрибуты**:
- `driver` (WebDriver): Экземпляр Selenium WebDriver для выполнения JavaScript.

**Методы**:
- `unhide_DOM_element(element: WebElement) -> bool`: Делает невидимый DOM-элемент видимым, изменяя его свойства стиля.
- `ready_state() -> str`: Возвращает статус загрузки документа.
- `window_focus() -> None`: Устанавливает фокус на окно браузера, используя JavaScript.
- `get_referrer() -> str`: Возвращает URL-адрес реферера текущего документа.
- `get_page_lang() -> str`: Возвращает язык текущей страницы.

## Методы класса

### `__init__`

```python
def __init__(self, driver: WebDriver):
    """
    Инициализирует помощника JavaScript с экземпляром Selenium WebDriver.

    Args:
        driver (WebDriver): Экземпляр Selenium WebDriver для выполнения JavaScript.
    """
```

### `unhide_DOM_element`

```python
def unhide_DOM_element(self, element: WebElement) -> bool:
    """
    Делает невидимый DOM-элемент видимым, изменяя его свойства стиля.

    Args:
        element (WebElement): Объект WebElement, который нужно сделать видимым.

    Returns:
        bool: True, если скрипт выполнен успешно, False в противном случае.
    """
```

### `ready_state`

```python
@property
def ready_state(self) -> str:
    """
    Возвращает статус загрузки документа.

    Returns:
        str: 'loading', если документ все еще загружается, 'complete', если загрузка завершена.
    """
```

### `window_focus`

```python
def window_focus(self) -> None:
    """
    Устанавливает фокус на окно браузера, используя JavaScript.

    Попытки вывода окна браузера на передний план.
    """
```

### `get_referrer`

```python
def get_referrer(self) -> str:
    """
    Возвращает URL-адрес реферера текущего документа.

    Returns:
        str: URL-адрес реферера или пустая строка, если он недоступен.
    """
```

### `get_page_lang`

```python
def get_page_lang(self) -> str:
    """
    Возвращает язык текущей страницы.

    Returns:
        str: Код языка страницы или пустая строка, если он недоступен.
    """
```

## Примеры

```python
from selenium import webdriver
from src.webdriver.js import JavaScript

# Создание экземпляра драйвера (пример с Chrome)
driver = webdriver.Chrome()
driver.get("https://example.com")

# Создание экземпляра JavaScript
js_utils = JavaScript(driver)

# Пример использования unhide_DOM_element
element = driver.find_element_by_id("hidden_element")
if js_utils.unhide_DOM_element(element):
    print("Элемент успешно отображен")
else:
    print("Не удалось отобразить элемент")

# Пример использования ready_state
ready_state = js_utils.ready_state
print(f"Статус загрузки документа: {ready_state}")

# Пример использования window_focus
js_utils.window_focus()
print("Фокус установлен на окно браузера")

# Пример использования get_referrer
referrer = js_utils.get_referrer()
print(f"URL-адрес реферера: {referrer}")

# Пример использования get_page_lang
page_lang = js_utils.get_page_lang()
print(f"Язык страницы: {page_lang}")

driver.quit()