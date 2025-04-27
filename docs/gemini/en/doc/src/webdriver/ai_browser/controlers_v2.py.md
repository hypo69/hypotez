# Модуль управления веб-браузером

## Обзор

Этот модуль предоставляет класс `BrowserController` для управления веб-браузером с использованием Selenium. Он включает в себя методы для навигации, поиска, скрапинга и взаимодействия с веб-страницами.

## Детали

`BrowserController` использует Selenium для управления веб-браузером Chrome. Он предоставляет удобный интерфейс для выполнения различных задач, таких как:

- Запуск браузера в headless режиме
- Поиск в Google
- Скрапинг текста с веб-страниц

## Классы

### `BrowserController`

**Описание**: Класс для управления веб-браузером (Chrome) с использованием Selenium. Предоставляет методы для навигации, поиска, скрапинга и взаимодействия.

**Атрибуты**:

- `driver` (Optional[webdriver.Chrome]): Экземпляр WebDriver для Chrome, который используется для взаимодействия с веб-браузером.

**Методы**:

#### `__init__`

**Описание**: Инициализирует WebDriver для Chrome.

**Параметры**:

- `headless` (bool): Запускать ли браузер в "безголовом" режиме (без GUI). True по умолчанию для автоматизации.

**Возвращает**: None

**Пример**:

```python
browser = BrowserController(headless=True)
```

#### `_check_driver`

**Описание**: Проверяет, был ли драйвер успешно инициализирован.

**Параметры**: None

**Возвращает**: bool - True, если драйвер инициализирован, False в противном случае.

**Пример**:

```python
if browser._check_driver():
    # ...
```

#### `search`

**Описание**: Выполняет поиск в указанной поисковой системе.

**Параметры**:

- `query` (str): Текст запроса для поиска.
- `search_engine_url` (str): URL поисковой системы, по умолчанию Google.

**Возвращает**: str - Текст с результатами поиска, если поиск был успешным, или сообщение об ошибке в противном случае.

**Пример**:

```python
results = browser.search("python programming")
print(results)
```

## Функции

## Параметры

## Примеры

### Создание экземпляра BrowserController

```python
from hypotez.src.webdriver.ai_browser.controlers_v2 import BrowserController

browser = BrowserController(headless=True)
```

### Выполнение поиска в Google

```python
results = browser.search("python programming")
print(results)
```

### Закрытие браузера

```python
browser.driver.quit()
```