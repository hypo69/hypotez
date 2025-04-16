### Анализ кода модуля `src/webdriver/crawlee_python/crawlee_python.py`

## Обзор

Этот модуль предоставляет пользовательскую реализацию `PlaywrightCrawler` с использованием библиотеки Crawlee. Он позволяет настраивать параметры браузера, обрабатывать запросы и извлекать данные с веб-страниц.

## Подробней

Модуль `src/webdriver/crawlee_python/crawlee_python.py` предоставляет класс `CrawleePython`, который является оберткой вокруг `PlaywrightCrawler` из библиотеки Crawlee. Этот класс упрощает настройку и запуск веб-скрейперов, позволяя указывать максимальное количество запросов, режим работы браузера (с графическим интерфейсом или без), тип браузера и другие параметры. Он предназначен для автоматизации сбора данных с веб-страниц с использованием библиотеки Crawlee.

## Классы

### `CrawleePython`

**Описание**: Пользовательская реализация `PlaywrightCrawler` с использованием библиотеки Crawlee.

**Атрибуты**:

-   `max_requests` (int): Максимальное количество запросов для выполнения во время обхода.
-   `headless` (bool): Указывает, следует ли запускать браузер в безголовом режиме.
-   `browser_type` (str): Тип используемого браузера ('chromium', 'firefox', 'webkit').
-   `crawler` (PlaywrightCrawler): Экземпляр PlaywrightCrawler.

**Методы**:

-   `__init__(self, max_requests: int = 5, headless: bool = False, browser_type: str = 'firefox', options: Optional[List[str]] = None)`: Инициализирует объект `CrawleePython` с указанными параметрами.
-   `setup_crawler(self)`: Настраивает экземпляр `PlaywrightCrawler` с указанной конфигурацией.
-   `run_crawler(self, urls: List[str])`: Запускает обход страниц с начальным списком URL.
-   `export_data(self, file_path: str)`: Экспортирует весь набор данных в JSON файл.
-   `get_data(self) -> Dict[str, Any]`: Извлекает собранные данные.
-   `run(self, urls: List[str])`: Основной метод для настройки, запуска обхода и экспорта данных.

#### `__init__`

**Назначение**: Инициализирует объект `CrawleePython` с указанными параметрами.

```python
def __init__(self, max_requests: int = 5, headless: bool = False, browser_type: str = 'firefox', options: Optional[List[str]] = None):
    """
    Initializes the CrawleePython crawler with the specified parameters.

    :param max_requests: Maximum number of requests to perform during the crawl.
    :type max_requests: int
    :param headless: Whether to run the browser in headless mode.
    :type headless: bool
    :param browser_type: The type of browser to use ('chromium', 'firefox', 'webkit').
    :type browser_type: str
    :param options: A list of custom options to pass to the browser.
    :type options: Optional[List[str]]
    """
    ...
```

**Параметры**:

-   `max_requests` (int): Максимальное количество запросов для выполнения во время обхода. По умолчанию 5.
-   `headless` (bool): Указывает, следует ли запускать браузер в безголовом режиме. По умолчанию `False`.
-   `browser_type` (str): Тип используемого браузера ('chromium', 'firefox', 'webkit'). По умолчанию `'firefox'`.
-   `options` (Optional[List[str]]): Список пользовательских опций для передачи в браузер. По умолчанию `None`.

**Как работает функция**:

1.  Сохраняет переданные параметры в атрибутах объекта.
2.  Инициализирует атрибут `crawler` значением `None`.

#### `setup_crawler`

**Назначение**: Настраивает экземпляр `PlaywrightCrawler` с указанной конфигурацией.

```python
async def setup_crawler(self):
    """
    Sets up the PlaywrightCrawler instance with the specified configuration.
    """
    ...
```

**Как работает функция**:

1.  Создает экземпляр `PlaywrightCrawler` с использованием переданных параметров (`max_requests`, `headless`, `browser_type`, `options`).
2.  Определяет функцию `request_handler` для обработки веб-страниц. Эта функция выполняет следующие действия:
    -   Логирует информацию об обрабатываемом URL.
    -   Добавляет в очередь все ссылки, найденные на странице.
    -   Извлекает данные со страницы (URL, заголовок, содержимое).
    -   Сохраняет извлеченные данные в набор данных (dataset).
3.  Регистрирует функцию `request_handler` как обработчик по умолчанию для `PlaywrightCrawler`.

#### `run_crawler`

**Назначение**: Запускает обход страниц с начальным списком URL.

```python
async def run_crawler(self, urls: List[str]):
    """
    Runs the crawler with the initial list of URLs.

    :param urls: List of URLs to start the crawl.
    :type urls: List[str]
    """
    ...
```

**Параметры**:

-   `urls` (List[str]): Список URL для начала обхода.

**Как работает функция**:

1.  Запускает обход страниц, используя метод `run` объекта `PlaywrightCrawler`.

#### `export_data`

**Назначение**: Экспортирует весь набор данных в JSON файл.

```python
async def export_data(self, file_path: str):
    """
    Exports the entire dataset to a JSON file.

    :param file_path: Path to save the exported JSON file.
    :type file_path: str
    """
    ...
```

**Параметры**:

-   `file_path` (str): Путь для сохранения экспортированного JSON файла.

**Как работает функция**:

1.  Экспортирует данные в JSON файл, используя метод `export_data` объекта `PlaywrightCrawler`.

#### `get_data`

**Назначение**: Извлекает собранные данные.

```python
async def get_data(self) -> Dict[str, Any]:
    """
    Retrieves the extracted data.

    :return: Extracted data as a dictionary.
    :rtype: Dict[str, Any]
    """
    ...
```

**Возвращает**:

-   `Dict[str, Any]`: Извлеченные данные в виде словаря.

**Как работает функция**:

1.  Получает данные из объекта `PlaywrightCrawler`, используя метод `get_data`.
2.  Возвращает полученные данные.

#### `run`

**Назначение**: Основной метод для настройки, запуска обхода и экспорта данных.

```python
async def run(self, urls: List[str]):
    """
    Main method to set up, run the crawler, and export data.

    :param urls: List of URLs to start the crawl.
    :type urls: List[str]
    """
    ...
```

**Параметры**:

-   `urls` (List[str]): Список URL для начала обхода.

**Как работает функция**:

1.  Вызывает метод `setup_crawler` для настройки обходчика.
2.  Вызывает метод `run_crawler` для запуска обхода страниц.
3.  Экспортирует данные в JSON файл, используя метод `export_data`. Путь к файлу определяется с использованием `gs.path.tmp`.
4.  Получает данные, используя метод `get_data`.
5.  Логирует информацию об извлеченных данных, используя `logger.info`.
6.  Обрабатывает возможные исключения, логируя критические ошибки с использованием `logger.critical`.

## Переменные модуля

-   В данном модуле отсутствуют глобальные переменные, за исключением импортированных модулей.

## Пример использования

```python
import asyncio
from src.webdriver.crawlee_python import CrawleePython

async def main():
    crawler = CrawleePython(max_requests=5, headless=False, browser_type='firefox')
    await crawler.run(['https://www.example.com'])

asyncio.run(main())
```

## Взаимосвязь с другими частями проекта

-   Модуль `src/webdriver/crawlee_python/crawlee_python.py` зависит от библиотеки `crawlee` для реализации веб-скрейпинга, от модуля `src.logger.logger` для логирования и от модуля `src.utils.jjson` для работы с JSON.
-   Он также использует модуль `header` для получения корневого пути проекта (хотя header не используется напрямую).
-   Этот модуль может использоваться другими частями проекта `hypotez` для автоматизированного сбора данных с веб-страниц.