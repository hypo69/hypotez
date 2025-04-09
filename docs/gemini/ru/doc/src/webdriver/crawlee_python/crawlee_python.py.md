# Модуль `crawlee_python`

## Обзор

Модуль предоставляет пользовательскую реализацию `PlaywrightCrawler` с использованием библиотеки Crawlee. Он позволяет настраивать параметры браузера, обрабатывать запросы и извлекать данные с веб-страниц.

## Подробней

Этот модуль предоставляет класс `CrawleePython`, который является оберткой для `PlaywrightCrawler` из библиотеки Crawlee. Он упрощает настройку и запуск краулера, позволяя указывать максимальное количество запросов, режим работы браузера (с графическим интерфейсом или без), тип браузера и другие опции.  Результаты работы краулера сохраняются в JSON-файл.

## Классы

### `CrawleePython`

**Описание**: Пользовательская реализация `PlaywrightCrawler` с использованием библиотеки Crawlee.

**Принцип работы**:
Класс инициализируется с параметрами, определяющими поведение краулера.  Метод `setup_crawler` создает экземпляр `PlaywrightCrawler` с заданной конфигурацией и регистрирует обработчик запросов по умолчанию. Этот обработчик извлекает данные со страницы (URL, заголовок, содержимое) и добавляет найденные ссылки в очередь на обработку.  Метод `run` запускает краулер с заданным списком URL-ов, экспортирует данные в JSON-файл и логирует извлеченные данные.

**Атрибуты**:

- `max_requests` (int): Максимальное количество запросов для выполнения во время обхода.
- `headless` (bool): Запускать ли браузер в режиме без графического интерфейса.
- `browser_type` (str): Тип используемого браузера ('chromium', 'firefox', 'webkit').
- `crawler` (PlaywrightCrawler): Экземпляр PlaywrightCrawler.
- `options` (Optional[List[str]]): Список дополнительных аргументов командной строки, передаваемых в браузер при запуске.

**Методы**:

- `__init__(self, max_requests: int = 5, headless: bool = False, browser_type: str = 'firefox', options: Optional[List[str]] = None)`: Инициализирует экземпляр класса `CrawleePython` с заданными параметрами.
- `setup_crawler(self)`: Настраивает экземпляр `PlaywrightCrawler` с заданной конфигурацией.
- `run_crawler(self, urls: List[str])`: Запускает краулер со списком начальных URL-ов.
- `export_data(self, file_path: str)`: Экспортирует все данные в JSON-файл.
- `get_data(self) -> Dict[str, Any]`: Получает извлеченные данные.
- `run(self, urls: List[str])`: Основной метод для настройки, запуска краулера и экспорта данных.

### `__init__(self, max_requests: int = 5, headless: bool = False, browser_type: str = 'firefox', options: Optional[List[str]] = None)`

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

**Назначение**: Инициализирует экземпляр класса `CrawleePython` с заданными параметрами.

**Параметры**:

- `max_requests` (int): Максимальное количество запросов для выполнения во время обхода. По умолчанию 5.
- `headless` (bool): Запускать ли браузер в режиме без графического интерфейса. По умолчанию `False`.
- `browser_type` (str): Тип используемого браузера ('chromium', 'firefox', 'webkit'). По умолчанию 'firefox'.
- `options` (Optional[List[str]]): Список дополнительных аргументов командной строки, передаваемых в браузер при запуске. По умолчанию `None`.

**Как работает**:

1.  Сохраняет значения переданных параметров в атрибуты экземпляра класса.
2.  Инициализирует атрибут `crawler` значением `None`.

### `setup_crawler(self)`

```python
async def setup_crawler(self):
    """
    Sets up the PlaywrightCrawler instance with the specified configuration.
    """
    ...
```

**Назначение**: Настраивает экземпляр `PlaywrightCrawler` с заданной конфигурацией.

**Как работает**:

1.  Создает экземпляр `PlaywrightCrawler` с использованием параметров `max_requests`, `headless` и `browser_type`, сохраненных в атрибутах экземпляра класса.  Дополнительно передает список опций `options` в браузер.
2.  Регистрирует обработчик запросов по умолчанию (`request_handler`) для всех URL-ов. Этот обработчик будет вызываться для каждой страницы, которую посетит краулер.

### `request_handler(context: PlaywrightCrawlingContext)`

```python
async def request_handler(context: PlaywrightCrawlingContext) -> None:
    """
    Default request handler for processing web pages.

    :param context: The crawling context.
    :type context: PlaywrightCrawlingContext
    """
    ...
```

**Назначение**: Обработчик запросов по умолчанию для обработки веб-страниц.

**Параметры**:

- `context` (PlaywrightCrawlingContext): Контекст обхода, содержащий информацию о текущем запросе и странице.

**Как работает**:

1.  Логирует информацию об обрабатываемом URL.
2.  Добавляет все найденные на странице ссылки в очередь на обработку с помощью `context.enqueue_links()`.
3.  Извлекает данные со страницы, используя API Playwright: URL, заголовок и первые 100 символов содержимого страницы.
4.  Сохраняет извлеченные данные в словарь.
5.  Отправляет извлеченные данные в набор данных по умолчанию с помощью `context.push_data(data)`.

### `run_crawler(self, urls: List[str])`

```python
async def run_crawler(self, urls: List[str]):
    """
    Runs the crawler with the initial list of URLs.

    :param urls: List of URLs to start the crawl.
    :type urls: List[str]
    """
    ...
```

**Назначение**: Запускает краулер со списком начальных URL-ов.

**Параметры**:

- `urls` (List[str]): Список URL-ов для начала обхода.

**Как работает**:

1.  Запускает краулер с переданным списком URL-ов, используя метод `self.crawler.run(urls)`.

### `export_data(self, file_path: str)`

```python
async def export_data(self, file_path: str):
    """
    Exports the entire dataset to a JSON file.

    :param file_path: Path to save the exported JSON file.
    :type file_path: str
    """
    ...
```

**Назначение**: Экспортирует все данные в JSON-файл.

**Параметры**:

- `file_path` (str): Путь для сохранения экспортированного JSON-файла.

**Как работает**:

1.  Экспортирует все данные, собранные краулером, в JSON-файл по указанному пути, используя метод `self.crawler.export_data(file_path)`.

### `get_data(self) -> Dict[str, Any]`

```python
async def get_data(self) -> Dict[str, Any]:
    """
    Retrieves the extracted data.

    :return: Extracted data as a dictionary.
    :rtype: Dict[str, Any]
    """
    ...
```

**Назначение**: Получает извлеченные данные.

**Возвращает**:

- `Dict[str, Any]`: Извлеченные данные в виде словаря.

**Как работает**:

1.  Получает извлеченные данные из краулера с помощью метода `self.crawler.get_data()`.
2.  Возвращает полученные данные.

### `run(self, urls: List[str])`

```python
async def run(self, urls: List[str]):
    """
    Main method to set up, run the crawler, and export data.

    :param urls: List of URLs to start the crawl.
    :type urls: List[str]
    """
    ...
```

**Назначение**: Основной метод для настройки, запуска краулера и экспорта данных.

**Параметры**:

- `urls` (List[str]): Список URL-ов для начала обхода.

**Как работает**:

1.  Вызывает `self.setup_crawler()` для настройки краулера.
2.  Вызывает `self.run_crawler(urls)` для запуска краулера с заданным списком URL-ов.
3.  Вызывает `self.export_data()` для экспорта данных в JSON-файл. Путь к файлу берется из настроек `gs.path.tmp / 'results.json'`.
4.  Вызывает `self.get_data()` для получения извлеченных данных.
5.  Логирует извлеченные данные с помощью `logger.info()`.
6.  Обрабатывает возможные исключения, возникающие в процессе работы краулера, и логирует критическую ошибку с помощью `logger.critical()`.

## Функции

В модуле нет отдельных функций, все основные действия выполняются методами класса `CrawleePython`.

## Примеры

```python
if __name__ == '__main__':
    async def main():
        crawler = CrawleePython(max_requests=5, headless=False, browser_type='firefox', options=["--headless"])
        await crawler.run(['https://www.example.com'])

    asyncio.run(main())
```
```