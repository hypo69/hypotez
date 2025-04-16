### Анализ кода модуля `hypotez/src/webdriver/crawlee_python/crawlee_python.py`

## Обзор

Этот модуль предоставляет пользовательскую реализацию `PlaywrightCrawler` с использованием библиотеки Crawlee. Он позволяет настраивать параметры браузера, обрабатывать запросы и извлекать данные с веб-страниц.

## Подробнее

Модуль позволяет автоматизировать процесс сбора данных с веб-страниц с использованием Crawlee и Playwright. Он предоставляет удобный интерфейс для настройки параметров браузера, обработки запросов и извлечения данных.

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
```

**Описание**:
Класс `CrawleePython` представляет собой пользовательскую реализацию `PlaywrightCrawler` с использованием библиотеки Crawlee.

**Атрибуты**:
-   `max_requests` (int): Максимальное количество запросов для выполнения во время обхода.
-   `headless` (bool): Определяет, следует ли запускать браузер в безголовом режиме.
-   `browser_type` (str): Тип используемого браузера ('chromium', 'firefox', 'webkit').
-   `crawler` (PlaywrightCrawler): Экземпляр `PlaywrightCrawler`.

**Методы**:

*   `__init__(self, max_requests: int = 5, headless: bool = False, browser_type: str = 'firefox', options: Optional[List[str]] = None)`: Инициализирует объект класса `CrawleePython` с указанными параметрами.
*   `setup_crawler(self)`: Настраивает экземпляр `PlaywrightCrawler` с указанной конфигурацией.
*   `run_crawler(self, urls: List[str])`: Запускает обход с начальным списком URL.
*   `export_data(self, file_path: str)`: Экспортирует весь набор данных в JSON-файл.
*   `get_data(self) -> Dict[str, Any]`: Извлекает собранные данные.
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

**Назначение**: Инициализирует объект класса `CrawleePython` с указанными параметрами.

**Параметры**:
-   `max_requests` (int): Максимальное количество запросов для выполнения во время обхода.
-   `headless` (bool): Определяет, следует ли запускать браузер в безголовом режиме.
-   `browser_type` (str): Тип используемого браузера ('chromium', 'firefox', 'webkit').
-   `options` (Optional[List[str]]): Список дополнительных опций, передаваемых браузеру.

**Как работает функция**:
Сохраняет значения входных параметров в атрибуты экземпляра класса.

### `setup_crawler`

```python
async def setup_crawler(self):
    """
    Sets up the PlaywrightCrawler instance with the specified configuration.
    """
    ...
```

**Назначение**: Настраивает экземпляр `PlaywrightCrawler` с указанной конфигурацией.

**Как работает функция**:
1.  Создает экземпляр `PlaywrightCrawler` с указанными параметрами (максимальное количество запросов, безголовый режим, тип браузера и опции запуска).
2.  Определяет функцию `request_handler`, которая будет вызываться для каждой посещенной веб-страницы.
3.  Регистрирует `request_handler` в качестве обработчика по умолчанию для `crawler.router`.

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

**Назначение**: Запускает обход с начальным списком URL.

**Параметры**:
- `urls` (List[str]): Список URL для начала обхода.

**Как работает функция**:
Вызывает метод `run` экземпляра `PlaywrightCrawler`, передавая ему список URL-адресов.

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

**Назначение**: Экспортирует весь набор данных в JSON-файл.

**Параметры**:
- `file_path` (str): Путь для сохранения JSON-файла.

**Как работает функция**:
Вызывает метод `export_data` экземпляра `PlaywrightCrawler`, передавая ему путь к файлу.

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

**Назначение**: Извлекает собранные данные.

**Возвращает**:
- `Dict[str, Any]`: Извлеченные данные в виде словаря.

**Как работает функция**:
Вызывает метод `get_data` экземпляра `PlaywrightCrawler` и возвращает полученные данные.

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

**Назначение**: Основной метод для настройки, запуска обхода и экспорта данных.

**Параметры**:
- `urls` (List[str]): Список URL для начала обхода.

**Как работает функция**:

1. Вызывает метод `setup_crawler` для настройки обходчика.
2. Вызывает метод `run_crawler` для запуска обхода по указанным URL.
3. Вызывает метод `export_data` для экспорта собранных данных в JSON-файл.
4. Вызывает метод `get_data` для получения извлеченных данных.
5. Логирует информацию об извлеченных данных.

## Переменные

Отсутствуют

## Запуск

Для использования этого модуля необходимо установить библиотеки `crawlee`, `playwright`, `requests`, `fake-useragent` и `src.logger`.
Также необходимо установить браузер, который будет использоваться (chromium, firefox, webkit).
Например для chromium:

```bash
playwright install chromium
```

Пример использования:

```python
import asyncio
from src.webdriver.crawlee_python.crawlee_python import CrawleePython

async def main():
    crawler = CrawleePython(max_requests=5, headless=False, browser_type='firefox', options=["--headless"])
    await crawler.run(['https://www.example.com'])

asyncio.run(main())