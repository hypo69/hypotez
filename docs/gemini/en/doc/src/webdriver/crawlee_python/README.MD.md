# Crawlee Python Module for Automation and Data Scraping

## Overview

This module provides a custom implementation of `PlaywrightCrawler` using the Crawlee library. It allows you to configure browser launch parameters, process web pages, and extract data from them. Configuration is managed via the `crawlee_python.json` file.

## Details

This module offers a flexible and robust solution for web scraping and automation tasks. It provides a centralized configuration system for easily managing browser settings, proxy servers, and other essential parameters. This module leverages the powerful capabilities of Playwright and Crawlee libraries to ensure efficient and reliable web interactions.

## Classes

### `CrawleePython`

**Description**: This class represents the Crawlee Python module, responsible for managing browser configurations and launching a crawler to perform scraping and automation tasks.

**Inherits**: 
- `PlaywrightCrawler` from the `crawlee` library

**Attributes**:
- `max_requests` (int): The maximum number of requests to perform during the crawl. Defaults to `10`.
- `headless` (bool): A boolean value indicating whether the browser should run in headless mode. Defaults to `True`.
- `browser_type` (str): The type of browser to be used. Possible values:
    - `chromium` (default)
    - `firefox`
    - `webkit`
- `options` (List[str]): A list of command-line arguments passed to the browser. Examples:
    - `--disable-dev-shm-usage`: Disables the use of `/dev/shm` in Docker containers.
    - `--no-sandbox`: Disables the sandbox mode.
    - `--disable-gpu`: Disables GPU hardware acceleration.
- `user_agent` (str): The user-agent string to be used for browser requests.
- `proxy` (dict): Proxy server settings:
    - **enabled**: A boolean value indicating whether to use a proxy.
    - **server**: The address of the proxy server.
    - **username**: The username for proxy authentication.
    - **password**: The password for proxy authentication.
- `viewport` (dict): The dimensions of the browser window:
    - **width**: The width of the window.
    - **height**: The height of the window.
- `timeout` (int): The maximum waiting time for operations (in milliseconds). Defaults to `30000` (30 seconds).
- `ignore_https_errors` (bool): A boolean value indicating whether to ignore HTTPS errors. Defaults to `False`.

**Methods**:
- `run(urls: List[str])`: This method initializes and runs the Crawlee Python crawler for the specified list of URLs. 

**Principle of Operation**:
- This class reads the configuration from the `crawlee_python.json` file.
- It utilizes the settings to launch a Playwright browser instance with the specified configurations.
- The crawler uses the browser to access the provided URLs, process the web pages, and extract the desired data.

**Example**:

```python
from src.webdriver.crawlee_python import CrawleePython
import asyncio

# Initialize CrawleePython with custom options
async def main():
    crawler = CrawleePython(max_requests=10, headless=True, browser_type='chromium', options=["--headless"])
    await crawler.run(['https://www.example.com'])

asyncio.run(main())
```


## Functions

### `load_config(path: str | Path = 'crawlee_python.json')`:

**Purpose**: This function loads the configuration from the specified JSON file, defaulting to `crawlee_python.json`.

**Parameters**:
- `path` (str | Path): Path to the configuration file. Defaults to `crawlee_python.json`.

**Returns**:
- `dict | None`: A dictionary containing the configuration data or `None` if an error occurs during loading.

**Raises Exceptions**:
- `FileNotFoundError`: If the specified configuration file does not exist.
- `json.JSONDecodeError`: If the file content is not valid JSON.

**How the Function Works**:
- The function attempts to read the specified configuration file using the `Path` object.
- If the file exists, it attempts to load the content as JSON using the `json.load()` method.
- The loaded JSON data is then returned as a dictionary.

**Examples**:
- `config = load_config('custom_config.json')`: Loads the configuration from `custom_config.json`.
- `config = load_config()`: Loads the configuration from the default `crawlee_python.json` file.


## Parameter Details

- `max_requests` (int): This parameter specifies the maximum number of requests the crawler will perform during its execution.
- `headless` (bool): This parameter controls whether the browser will be launched in headless mode (without a visible window).
- `browser_type` (str): This parameter sets the type of browser to be used. It accepts three possible values: `chromium`, `firefox`, or `webkit`.
- `options` (List[str]): This parameter is used to pass custom command-line arguments to the browser.
- `user_agent` (str): This parameter defines the user-agent string that will be sent with each browser request. This can be useful for mimicking different browsers or platforms.
- `proxy` (dict): This parameter contains settings for using a proxy server. It includes flags to enable/disable the proxy, the proxy server address, and credentials for authentication if required.
- `viewport` (dict): This parameter sets the dimensions of the browser window, specifying the width and height in pixels.
- `timeout` (int): This parameter defines the maximum waiting time for operations in milliseconds.
- `ignore_https_errors` (bool): This parameter determines whether the crawler should ignore HTTPS errors that might occur during the process.


## Examples

**Example 1: Basic CrawleePython usage**

```python
from src.webdriver.crawlee_python import CrawleePython
import asyncio

async def main():
    crawler = CrawleePython(max_requests=5, headless=True)
    await crawler.run(['https://www.example.com', 'https://www.google.com'])

asyncio.run(main())
```

This example demonstrates the basic usage of the `CrawleePython` class. It sets a maximum of 5 requests and runs in headless mode, visiting two websites.

**Example 2: Crawling with custom browser options**

```python
from src.webdriver.crawlee_python import CrawleePython
import asyncio

async def main():
    crawler = CrawleePython(
        max_requests=5,
        headless=False,
        browser_type='chromium',
        options=['--disable-dev-shm-usage', '--no-sandbox', '--disable-gpu']
    )
    await crawler.run(['https://www.example.com'])

asyncio.run(main())
```

This example demonstrates how to use the `options` parameter to customize the browser configuration by disabling the use of `/dev/shm`, sandbox mode, and GPU acceleration. 

**Example 3: Using a proxy server**

```python
from src.webdriver.crawlee_python import CrawleePython
import asyncio

async def main():
    crawler = CrawleePython(
        max_requests=5,
        headless=True,
        proxy={'enabled': True, 'server': 'http://proxy.example.com:8080', 'username': 'user', 'password': 'password'}
    )
    await crawler.run(['https://www.example.com'])

asyncio.run(main())
```

This example shows how to enable and configure a proxy server for the browser using the `proxy` parameter. 

**Example 4: Setting a custom user-agent**

```python
from src.webdriver.crawlee_python import CrawleePython
import asyncio

async def main():
    crawler = CrawleePython(
        max_requests=5,
        headless=True,
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    )
    await crawler.run(['https://www.example.com'])

asyncio.run(main())
```

This example sets a specific user-agent string for the browser, allowing you to mimic a particular browser or device.

**Example 5: Configuring viewport size**

```python
from src.webdriver.crawlee_python import CrawleePython
import asyncio

async def main():
    crawler = CrawleePython(
        max_requests=5,
        headless=True,
        viewport={'width': 1280, 'height': 720}
    )
    await crawler.run(['https://www.example.com'])

asyncio.run(main())
```

This example sets the browser window size to 1280x720 pixels using the `viewport` parameter.