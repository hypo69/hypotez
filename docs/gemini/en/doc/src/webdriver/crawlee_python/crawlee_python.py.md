# Crawlee Python Crawler

## Overview

The module provides a custom implementation of `PlaywrightCrawler` using the Crawlee library. It allows you to configure browser settings, handle requests, and extract data from web pages.

## Details

This module is designed to streamline web crawling tasks using Playwright, a powerful browser automation library. It extends the functionality of Crawlee's `PlaywrightCrawler` by providing a more user-friendly interface and simplifying the process of extracting and exporting data from web pages.

## Classes

### `CrawleePython`

**Description**: This class represents a custom implementation of `PlaywrightCrawler` for web scraping. It allows you to configure browser settings, handle requests, and extract data from web pages.

**Inherits**: N/A

**Attributes**:

- `max_requests` (int): Maximum number of requests to perform during the crawl.
- `headless` (bool): Whether to run the browser in headless mode.
- `browser_type` (str): The type of browser to use ('chromium', 'firefox', 'webkit').
- `crawler` (PlaywrightCrawler): The PlaywrightCrawler instance.

**Methods**:

- `__init__(self, max_requests: int = 5, headless: bool = False, browser_type: str = 'firefox', options: Optional[List[str]] = None)`: Initializes the `CrawleePython` crawler with the specified parameters.
- `setup_crawler(self)`: Sets up the `PlaywrightCrawler` instance with the specified configuration.
- `request_handler(context: PlaywrightCrawlingContext) -> None`: Default request handler for processing web pages.
- `run_crawler(self, urls: List[str])`: Runs the crawler with the initial list of URLs.
- `export_data(self, file_path: str)`: Exports the entire dataset to a JSON file.
- `get_data(self) -> Dict[str, Any]`: Retrieves the extracted data.
- `run(self, urls: List[str])`: Main method to set up, run the crawler, and export data.

## Class Methods

### `__init__`

```python
    def __init__(self, max_requests: int = 5, headless: bool = False, browser_type: str = 'firefox', options: Optional[List[str]] = None):
        """
        Инициализирует объект CrawleePython с заданными параметрами.

        :param max_requests: Максимальное количество запросов, которые будут выполнены во время сканирования.
        :type max_requests: int
        :param headless: Запускать ли браузер в headless-режиме.
        :type headless: bool
        :param browser_type: Тип браузера, который будет использоваться ('chromium', 'firefox', 'webkit').
        :type browser_type: str
        :param options: Список дополнительных параметров, которые будут переданы браузеру.
        :type options: Optional[List[str]]
        """
        self.max_requests = max_requests
        self.headless = headless
        self.browser_type = browser_type
        self.options = options or []
        self.crawler = None
```

**Purpose**: Initializes the `CrawleePython` object with the specified parameters.

**Parameters**:

- `max_requests` (int): Maximum number of requests to perform during the crawl.
- `headless` (bool): Whether to run the browser in headless mode.
- `browser_type` (str): The type of browser to use ('chromium', 'firefox', 'webkit').
- `options` (Optional[List[str]]): A list of custom options to pass to the browser.

**Returns**: None

**Raises Exceptions**: None

**How the Method Works**:

- The method sets the `max_requests`, `headless`, and `browser_type` attributes to the values provided as arguments.
- It initializes an empty `options` list if no custom options are provided.
- It sets the `crawler` attribute to `None`, as the crawler will be initialized later using the `setup_crawler` method.

**Examples**:

```python
>>> crawler = CrawleePython(max_requests=10, headless=True, browser_type='chromium')
>>> crawler.max_requests
10
>>> crawler.headless
True
>>> crawler.browser_type
'chromium'

>>> crawler = CrawleePython(options=['--no-sandbox'])
>>> crawler.options
['--no-sandbox']
```

### `setup_crawler`

```python
    async def setup_crawler(self):
        """
        Инициализирует объект PlaywrightCrawler с заданной конфигурацией.
        """
        self.crawler = PlaywrightCrawler(
            max_requests_per_crawl=self.max_requests,
            headless=self.headless,
            browser_type=self.browser_type,
            launch_options={"args": self.options}
        )

        @self.crawler.router.default_handler
        async def request_handler(context: PlaywrightCrawlingContext) -> None:
            """
            Обработчик запросов по умолчанию для обработки веб-страниц.

            :param context: Контекст сканирования.
            :type context: PlaywrightCrawlingContext
            """
            context.log.info(f'Processing {context.request.url} ...')

            # Enqueue all links found on the page.
            await context.enqueue_links()

            # Extract data from the page using Playwright API.
            data = {
                'url': context.request.url,
                'title': await context.page.title(),
                'content': (await context.page.content())[:100],
            }

            # Push the extracted data to the default dataset.
            await context.push_data(data)
```

**Purpose**: Initializes the `PlaywrightCrawler` object with the configured settings.

**Parameters**: None

**Returns**: None

**Raises Exceptions**: None

**How the Method Works**:

- The method creates a `PlaywrightCrawler` instance using the `max_requests_per_crawl`, `headless`, and `browser_type` attributes set during initialization.
- It configures the crawler to use the specified `options` for the browser.
- It defines a default request handler (`request_handler`) that will be executed for each page visited during the crawl.
- The `request_handler` logs information about the processed URL, enqueues all links found on the page, extracts data using the Playwright API, and pushes the extracted data to the default dataset.

**Examples**:

```python
>>> crawler = CrawleePython(max_requests=5, headless=False, browser_type='firefox')
>>> crawler.setup_crawler()
>>> crawler.crawler  # Accessing the initialized PlaywrightCrawler instance
<crawlee.playwright_crawler.PlaywrightCrawler object at 0x...>
```

### `request_handler`

```python
        @self.crawler.router.default_handler
        async def request_handler(context: PlaywrightCrawlingContext) -> None:
            """
            Обработчик запросов по умолчанию для обработки веб-страниц.

            :param context: Контекст сканирования.
            :type context: PlaywrightCrawlingContext
            """
            context.log.info(f'Processing {context.request.url} ...')

            # Enqueue all links found on the page.
            await context.enqueue_links()

            # Extract data from the page using Playwright API.
            data = {
                'url': context.request.url,
                'title': await context.page.title(),
                'content': (await context.page.content())[:100],
            }

            # Push the extracted data to the default dataset.
            await context.push_data(data)
```

**Purpose**: This function serves as the default request handler for processing web pages during the crawl.

**Parameters**:

- `context` (PlaywrightCrawlingContext): The crawling context, providing access to information about the current request and the browser page.

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

- The function logs information about the processed URL.
- It enqueues all links found on the page for further processing.
- It extracts data from the page using the Playwright API, including the URL, title, and a snippet of the page's content.
- It pushes the extracted data to the default dataset for storage and later analysis.

**Examples**:

```python
>>> # This function is automatically executed for each page visited during the crawl,
>>> # so no direct examples are needed.
```

### `run_crawler`

```python
    async def run_crawler(self, urls: List[str]):
        """
        Запускает сканирование с начальным списком URL.

        :param urls: Список URL, с которых нужно начать сканирование.
        :type urls: List[str]
        """
        await self.crawler.run(urls)
```

**Purpose**: Runs the crawler with the provided initial list of URLs.

**Parameters**:

- `urls` (List[str]): List of URLs to start the crawl.

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

- The method calls the `run` method of the `PlaywrightCrawler` instance to initiate the crawl.
- The crawler starts processing the provided URLs and follows links found on the pages to explore the website.

**Examples**:

```python
>>> crawler = CrawleePython()
>>> crawler.setup_crawler()
>>> crawler.run_crawler(['https://www.example.com'])
```

### `export_data`

```python
    async def export_data(self, file_path: str):
        """
        Экспортирует весь набор данных в файл JSON.

        :param file_path: Путь для сохранения экспортированного файла JSON.
        :type file_path: str
        """
        await self.crawler.export_data(file_path)
```

**Purpose**: Exports the entire dataset collected during the crawl to a JSON file.

**Parameters**:

- `file_path` (str): Path to save the exported JSON file.

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

- The method calls the `export_data` method of the `PlaywrightCrawler` instance, which saves the extracted data to the specified JSON file.

**Examples**:

```python
>>> crawler = CrawleePython()
>>> crawler.setup_crawler()
>>> crawler.run_crawler(['https://www.example.com'])
>>> crawler.export_data('results.json')
```

### `get_data`

```python
    async def get_data(self) -> Dict[str, Any]:
        """
        Получает извлеченные данные.

        :return: Извлеченные данные в виде словаря.
        :rtype: Dict[str, Any]
        """
        data = await self.crawler.get_data()
        return data
```

**Purpose**: Retrieves the extracted data from the crawler's dataset.

**Parameters**: None

**Returns**:

- `Dict[str, Any]`: Extracted data as a dictionary.

**Raises Exceptions**: None

**How the Function Works**:

- The method calls the `get_data` method of the `PlaywrightCrawler` instance to retrieve the collected data.
- It returns the data as a dictionary, which can then be used for further processing or analysis.

**Examples**:

```python
>>> crawler = CrawleePython()
>>> crawler.setup_crawler()
>>> crawler.run_crawler(['https://www.example.com'])
>>> data = crawler.get_data()
>>> data  # Accessing the extracted data as a dictionary
{'url': 'https://www.example.com', 'title': 'Example Domain', 'content': 'Example Domain\nThis domain is for use in illustrative examples in documents. You may use this\ndomain in literature without prior coordination or asking for permission...'}
```

### `run`

```python
    async def run(self, urls: List[str]):
        """
        Основной метод для настройки, запуска сканирования и экспорта данных.

        :param urls: Список URL, с которых нужно начать сканирование.
        :type urls: List[str]
        """
        try:
            await self.setup_crawler()
            await self.run_crawler(urls)
            await self.export_data(str(Path(gs.path.tmp / 'results.json')))
            data = await self.get_data()
            logger.info(f'Extracted data: {data.items()}')
        except Exception as ex:
            logger.critical('Crawler failed with an error:', ex)
```

**Purpose**: This method serves as the main entry point for setting up, running the crawler, and exporting data.

**Parameters**:

- `urls` (List[str]): List of URLs to start the crawl.

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:

- The method sets up the crawler using the `setup_crawler` method.
- It runs the crawler with the provided URLs using the `run_crawler` method.
- It exports the collected data to a JSON file using the `export_data` method.
- It retrieves the extracted data using the `get_data` method and logs the results.
- The method includes error handling to log any exceptions that occur during the crawl process.

**Examples**:

```python
>>> crawler = CrawleePython(max_requests=5, headless=False, browser_type='firefox')
>>> crawler.run(['https://www.example.com'])
```

## Parameter Details

- `max_requests` (int): Specifies the maximum number of requests that the crawler will make during the crawl. This helps control the amount of data collected and the load on the target website.
- `headless` (bool): Determines whether the browser will run in headless mode. If `True`, the browser will run without a visible window, which is useful for automated tasks that don't require user interaction.
- `browser_type` (str): Specifies the type of browser to use for the crawl. The available options are 'chromium' (Chrome), 'firefox', and 'webkit' (Safari).
- `options` (Optional[List[str]]): Allows you to pass custom options to the browser, such as command-line arguments or configuration settings. This can be used to customize the browser's behavior or enable specific features.
- `urls` (List[str]):  Defines the list of starting URLs for the crawl. The crawler will begin processing these URLs and follow links found on the pages to explore the website.
- `file_path` (str):  Specifies the path to the file where the extracted data will be saved in JSON format. This allows you to store the collected information for further analysis or processing.

## Examples

```python
# Example 1: Simple crawl with default settings
from src.webdriver.crawlee_python.crawlee_python import CrawleePython

async def main():
    crawler = CrawleePython()
    await crawler.run(['https://www.example.com'])

asyncio.run(main())

# Example 2: Crawl with custom settings and headless mode
from src.webdriver.crawlee_python.crawlee_python import CrawleePython

async def main():
    crawler = CrawleePython(max_requests=10, headless=True, browser_type='chromium', options=['--no-sandbox'])
    await crawler.run(['https://www.example.com', 'https://www.google.com'])

asyncio.run(main())
```

## Conclusion

This module provides a comprehensive solution for web crawling using the Crawlee library and Playwright. It simplifies the process of configuring browser settings, handling requests, extracting data, and exporting results to a JSON file. The well-documented code and the examples provided make it easy to implement and customize for various web scraping tasks.