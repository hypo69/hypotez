### Анализ кода `hypotez/src/webdriver/crawlee_python/crawlee_python.py.md`

## Обзор

Модуль предоставляет пользовательскую реализацию `PlaywrightCrawler` с использованием библиотеки Crawlee для автоматизации сбора данных из веб-страниц.

## Подробнее

Этот модуль содержит класс `CrawleePython`, который является расширением `PlaywrightCrawler` из библиотеки Crawlee. Он позволяет настраивать параметры браузера, обрабатывать запросы и извлекать данные из веб-страниц. Модуль предоставляет удобный интерфейс для настройки и запуска веб-пауков (web crawlers) с использованием библиотеки Crawlee и асинхронного веб-драйвера Playwright.

## Классы

### `CrawleePython`

```python
class CrawleePython:
    """
    Custom implementation of `PlaywrightCrawler` using the Crawlee library.

    Attributes:
        max_requests (int): Maximum number of requests to perform during the crawl.
        headless (bool): Whether to run the browser in headless mode.
        browser_type (str): The type of browser to use ('chromium', 'firefox', 'webkit').
        crawler (PlaywrightCrawler): The PlaywrightCrawler instance.
    """
    ...
```

**Описание**:
Пользовательская реализация `PlaywrightCrawler` с использованием библиотеки Crawlee.

**Атрибуты**:

*   `max_requests` (int): Максимальное количество запросов для выполнения во время обхода.
*   `headless` (bool): Указывает, следует ли запускать браузер в безголовом режиме.
*   `browser_type` (str): Тип используемого браузера ('chromium', 'firefox', 'webkit').
*   `crawler` (PlaywrightCrawler): Экземпляр `PlaywrightCrawler`.

**Методы**:

*   `__init__(self, max_requests: int = 5, headless: bool = False, browser_type: str = 'firefox', options: Optional[List[str]] = None)`: Инициализирует экземпляр класса `CrawleePython` с указанными параметрами.
*   `setup_crawler(self)`: Настраивает экземпляр `PlaywrightCrawler` с указанной конфигурацией.
*   `run_crawler(self, urls: List[str])`: Запускает обход с начальным списком URL-адресов.
*   `export_data(self, file_path: str)`: Экспортирует весь набор данных в JSON-файл.
*   `get_data(self) -> Dict[str, Any]`: Получает извлеченные данные.
*   `run(self, urls: List[str])`: Основной метод для настройки, запуска обхода и экспорта данных.

## Методы класса

### `__init__`

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

**Назначение**:
Инициализирует класс `CrawleePython` с заданными параметрами.

**Параметры**:

*   `max_requests` (int): Максимальное количество запросов для выполнения во время обхода. По умолчанию 5.
*   `headless` (bool): Указывает, следует ли запускать браузер в безголовом режиме. По умолчанию `False`.
*   `browser_type` (str): Тип используемого браузера ('chromium', 'firefox', 'webkit'). По умолчанию `'firefox'`.
*   `options` (Optional[List[str]]): Список пользовательских опций для передачи в браузер. По умолчанию `None`.

**Как работает функция**:
1.Сохраняет переданные параметры в атрибуты экземпляра класса.
2.Инициализирует атрибут `crawler` значением `None`.

### `setup_crawler`

```python
async def setup_crawler(self):
    """
    Sets up the PlaywrightCrawler instance with the specified configuration.
    """
    ...
```

**Назначение**:
Настраивает экземпляр `PlaywrightCrawler` с указанной конфигурацией.

**Как работает функция**:

1.  Создает экземпляр `PlaywrightCrawler` с использованием значений атрибутов `max_requests`, `headless` и `browser_type`.
2.  Определяет функцию `request_handler`, которая будет вызываться для каждой страницы, которую посетит обходчик.
3.  Внутри `request_handler`:

    *   Логирует информацию об обрабатываемом URL.
    *   Добавляет все ссылки, найденные на странице, в очередь для дальнейшей обработки.
    *   Извлекает данные (URL, заголовок, первые 100 символов содержимого) из страницы.
    *   Отправляет извлеченные данные в набор данных по умолчанию.
4.Регистрирует функцию `request_handler` в качестве обработчика по умолчанию для `PlaywrightCrawler`.

### `run_crawler`

```python
async def run_crawler(self, urls: List[str]):
    """
    Runs the crawler with the initial list of URLs.

    :param urls: List of URLs to start the crawl.
    :type urls: List[str]
    """
    ...
```

**Назначение**:
Запускает обход с начальным списком URL-адресов.

**Параметры**:

*   `urls` (List[str]): Список URL-адресов для начала обхода.

**Как работает функция**:

1.  Запускает обход, используя метод `run` объекта `PlaywrightCrawler`.

### `export_data`

```python
async def export_data(self, file_path: str):
    """
    Exports the entire dataset to a JSON file.

    :param file_path: Path to save the exported JSON file.
    :type file_path: str
    """
    ...
```

**Назначение**:
Экспортирует весь набор данных в JSON-файл.

**Параметры**:

*   `file_path` (str): Путь для сохранения экспортированного JSON-файла.

**Как работает функция**:

1.  Экспортирует данные, используя метод `export_data` объекта `PlaywrightCrawler`.

### `get_data`

```python
async def get_data(self) -> Dict[str, Any]:
    """
    Retrieves the extracted data.

    :return: Extracted data as a dictionary.
    :rtype: Dict[str, Any]
    """
    ...
```

**Назначение**:
Получает извлеченные данные.

**Возвращает**:

*   `Dict[str, Any]`: Извлеченные данные в виде словаря.

**Как работает функция**:

1.  Получает данные, используя метод `get_data` объекта `PlaywrightCrawler`.

### `run`

```python
async def run(self, urls: List[str]):
    """
    Main method to set up, run the crawler, and export data.

    :param urls: List of URLs to start the crawl.
    :type urls: List[str]
    """
    ...
```

**Назначение**:
Основной метод для настройки, запуска обходчика и экспорта данных.

**Параметры**:

*   `urls` (List[str]): Список URL-адресов для начала обхода.

**Как работает функция**:

1.  Вызывает `setup_crawler` для настройки обходчика.
2.  Вызывает `run_crawler` для запуска обхода.
3.  Вызывает `export_data` для экспорта данных в JSON-файл.
4.  Вызывает `get_data` для получения извлеченных данных.
5.  Логирует извлеченные данные.
6.  Обрабатывает возможные исключения.

## Переменные

*   `max_requests` (int): Максимальное количество запросов для выполнения во время обхода.
*   `headless` (bool): Указывает, следует ли запускать браузер в безголовом режиме.
*   `browser_type` (str): Тип используемого браузера ('chromium', 'firefox', 'webkit').
*   `crawler` (PlaywrightCrawler): Экземпляр `PlaywrightCrawler`.
*    `options`:  Список опций, переданных  в browser_type

## Примеры использования

```python
import asyncio
from src.webdriver.crawlee_python import CrawleePython

async def main():
    crawler = CrawleePython(max_requests=5, headless=False, browser_type='firefox')
    await crawler.run(['https://www.example.com'])

asyncio.run(main())
```

## Зависимости

*   `pathlib.Path`: Для работы с путями к файлам.
*   `typing.Optional, typing.List, typing.Dict, typing.Any`: Для аннотаций типов.
*   `crawlee.playwright_crawler.PlaywrightCrawler, crawlee.playwright_crawler.PlaywrightCrawlingContext`: Для реализации веб-паука.
*   `src.logger.logger`: Для логирования.
*   `src.utils.jjson.j_loads_ns`: Для загрузки настроек из JSON.

## Взаимосвязи с другими частями проекта

*   Модуль использует `src.logger.logger` для логирования информации об обходе и ошибках.
*   Он зависит от библиотеки `crawlee` для реализации основных функций веб-паука.
*   Использует  `j_loads_ns`  для загрузки настроек.