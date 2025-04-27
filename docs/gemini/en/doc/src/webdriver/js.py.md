# Модуль `src.webdriver.js`

## Обзор

Этот модуль разработан для расширения функциональных возможностей Selenium WebDriver, добавляя общие JavaScript-функции для взаимодействия с веб-страницами, такие как управление видимостью элементов, получение информации о странице и управление фокусом браузера.

## Детали

Модуль `src.webdriver.js` предоставляет набор полезных JavaScript-функций, которые могут быть использованы для взаимодействия с веб-страницами в Selenium WebDriver. 

Этот модуль используется для:

- **Управление видимостью элементов:** Функция `unhide_DOM_element` делает невидимые элементы DOM видимыми, изменяя их стили, что позволяет взаимодействовать с ними.
- **Получение информации о странице:** Функции `ready_state`, `get_referrer` и `get_page_lang` используются для извлечения информации о состоянии загрузки документа, ссылочном URL и языке страницы соответственно.
- **Управление фокусом браузера:** Функция `window_focus` переносит фокус на окно браузера, чтобы переместить внимание пользователя на активное окно.

## Классы

### `JavaScript`

**Описание**: Класс, предоставляющий набор JavaScript-функций для взаимодействия с веб-страницами.

**Inherits**: 

**Attributes**:
- `driver` (WebDriver): Экземпляр WebDriver для выполнения JavaScript-кода.

**Methods**:

#### `__init__(self, driver: WebDriver)`

**Purpose**: Инициализирует объект `JavaScript` с экземпляром Selenium WebDriver.

**Parameters**:
- `driver` (WebDriver): Экземпляр WebDriver, который будет использоваться для выполнения JavaScript-кода.

#### `unhide_DOM_element(self, element: WebElement) -> bool`

**Purpose**: Делает невидимый элемент DOM видимым, изменяя его стили.

**Parameters**:
- `element` (WebElement): Элемент WebElement, который нужно сделать видимым.

**Returns**:
- `bool`: `True` если скрипт успешно выполнился, `False` в противном случае.

**How the Function Works**:

1. Функция определяет JavaScript-код, который изменяет стили элемента (opacity, transform, scale) и скроллит его в видимую область. 
2. Затем код выполняется с помощью метода `driver.execute_script`.
3. Если скрипт выполнился успешно, функция возвращает `True`, в противном случае - `False`.

**Examples**:

```python
from src.webdriver.js import JavaScript
from selenium import webdriver

driver = webdriver.Chrome()  # или другой браузер
js = JavaScript(driver)

# Найдем скрытый элемент на странице
element = driver.find_element_by_xpath("//div[@class='hidden-element']")

# Сделаем элемент видимым
success = js.unhide_DOM_element(element)
```

#### `ready_state(self) -> str`

**Purpose**: Возвращает статус загрузки документа.

**Returns**:
- `str`: 'loading' если документ все еще загружается, 'complete' если загрузка завершена.

**How the Function Works**:

1. Функция выполняет JavaScript-код, который возвращает значение свойства `document.readyState`.
2. Возвращает строку 'loading', если документ все еще загружается, или 'complete' если загрузка завершена.

**Examples**:

```python
from src.webdriver.js import JavaScript
from selenium import webdriver

driver = webdriver.Chrome()  # или другой браузер
js = JavaScript(driver)

# Получим статус загрузки документа
ready_state = js.ready_state
```

#### `window_focus(self) -> None`

**Purpose**: Переносит фокус на окно браузера.

**Parameters**: 
- Нет

**Returns**: 
- Нет

**How the Function Works**:

1. Функция выполняет JavaScript-код `window.focus()`, который переводит фокус на текущее окно браузера.

**Examples**:

```python
from src.webdriver.js import JavaScript
from selenium import webdriver

driver = webdriver.Chrome()  # или другой браузер
js = JavaScript(driver)

# Переведем фокус на окно браузера
js.window_focus()
```

#### `get_referrer(self) -> str`

**Purpose**: Возвращает URL-адрес ссылки на текущий документ.

**Returns**:
- `str`: URL-адрес ссылки, или пустая строка, если он недоступен.

**How the Function Works**:

1. Функция выполняет JavaScript-код, который возвращает значение свойства `document.referrer`.
2. Возвращает URL-адрес ссылки, или пустую строку, если он недоступен.

**Examples**:

```python
from src.webdriver.js import JavaScript
from selenium import webdriver

driver = webdriver.Chrome()  # или другой браузер
js = JavaScript(driver)

# Получим URL-адрес ссылки
referrer_url = js.get_referrer()
```

#### `get_page_lang(self) -> str`

**Purpose**: Возвращает язык текущей страницы.

**Returns**:
- `str`: Код языка страницы, или пустая строка, если он недоступен.

**How the Function Works**:

1. Функция выполняет JavaScript-код, который возвращает значение свойства `document.documentElement.lang`.
2. Возвращает код языка страницы, или пустую строку, если он недоступен.

**Examples**:

```python
from src.webdriver.js import JavaScript
from selenium import webdriver

driver = webdriver.Chrome()  # или другой браузер
js = JavaScript(driver)

# Получим код языка страницы
page_lang = js.get_page_lang()
```

## Inner Functions:

- Нет внутренних функций.

## Parameter Details:

- `driver` (WebDriver): Экземпляр Selenium WebDriver, используемый для выполнения JavaScript-кода.
- `element` (WebElement): Элемент WebElement, который нужно сделать видимым.

## Examples:

- См. примеры в описании каждой функции.