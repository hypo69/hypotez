**Webdriver Documentation**

=========================================================================================

This document provides an overview of all webdrivers available in the project, their configurations, and options. Each webdriver has its own set of parameters that can be customized in their respective JSON files.

# Webdrivers and Their Configurations

This document provides descriptions of all webdrivers available in the project, their configurations, and options. Each webdriver provides capabilities for automating browsers and collecting data.

---

## Table of Contents

1. [Firefox WebDriver](#1-firefox-webdriver)
2. [Chrome WebDriver](#2-chrome-webdriver)
3. [Edge WebDriver](#3-edge-webdriver)
4. [Playwright Crawler](#4-playwright-crawler)
5. [BeautifulSoup and XPath Parser](#5-beautifulsoup-и-xpath-parser)
6. [Conclusion](#заключение)

---

## 1. Firefox WebDriver

### Description

The Firefox WebDriver provides functionality for interacting with the Firefox browser. It supports customizing user profiles, proxies, user agents, and other parameters.

### Settings

- **profile_name**: Name of the Firefox user profile.
- **geckodriver_version**: Version of geckodriver.
- **firefox_version**: Version of Firefox.
- **user_agent**: User agent string.
- **proxy_file_path**: Path to the proxy file.
- **options**: List of options for Firefox (e.g., `["--kiosk", "--headless"]`).

### Example Configuration (`firefox.json`)

```json
{
  "options": ["--kiosk", "--headless"],
  "profile_directory": {
    "os": "%LOCALAPPDATA%\\\\Mozilla\\\\Firefox\\\\Profiles\\\\default",
    "internal": "webdriver\\\\firefox\\\\profiles\\\\default"
  },
  "executable_path": {
    "firefox_binary": "bin\\\\webdrivers\\\\firefox\\\\ff\\\\core-127.0.2\\\\firefox.exe",
    "geckodriver": "bin\\\\webdrivers\\\\firefox\\\\gecko\\\\33\\\\geckodriver.exe"
  },
  "headers": {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
  },
  "proxy_enabled": false
}
```

---

## 2. Chrome WebDriver

### Description

The Chrome WebDriver provides functionality for interacting with the Google Chrome browser. It supports customizing profiles, user agents, proxies, and other parameters.

### Settings

- **profile_name**: Name of the Chrome user profile.
- **chromedriver_version**: Version of chromedriver.
- **chrome_version**: Version of Chrome.
- **user_agent**: User agent string.
- **proxy_file_path**: Path to the proxy file.
- **options**: List of options for Chrome (e.g., `["--headless", "--disable-gpu"]`).

### Example Configuration (`chrome.json`)

```json
{
  "options": ["--headless", "--disable-gpu"],
  "profile_directory": {
    "os": "%LOCALAPPDATA%\\\\Google\\\\Chrome\\\\User Data\\\\Default",
    "internal": "webdriver\\\\chrome\\\\profiles\\\\default"
  },
  "executable_path": {
    "chrome_binary": "bin\\\\webdrivers\\\\chrome\\\\125.0.6422.14\\\\chrome.exe",
    "chromedriver": "bin\\\\webdrivers\\\\chrome\\\\125.0.6422.14\\\\chromedriver.exe"
  },
  "headers": {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
  },
  "proxy_enabled": false
}
```

---

## 3. Edge WebDriver

### Description

The Edge WebDriver provides functionality for interacting with the Microsoft Edge browser. It supports customizing profiles, user agents, proxies, and other parameters.

### Settings

- **profile_name**: Name of the Edge user profile.
- **edgedriver_version**: Version of edgedriver.
- **edge_version**: Version of Edge.
- **user_agent**: User agent string.
- **proxy_file_path**: Path to the proxy file.
- **options**: List of options for Edge (e.g., `["--headless", "--disable-gpu"]`).

### Example Configuration (`edge.json`)

```json
{
  "options": ["--headless", "--disable-gpu"],
  "profiles": {
    "os": "%LOCALAPPDATA%\\\\Microsoft\\\\Edge\\\\User Data\\\\Default",
    "internal": "webdriver\\\\edge\\\\profiles\\\\default"
  },
  "executable_path": {
    "edge_binary": "bin\\\\webdrivers\\\\edge\\\\123.0.2420.97\\\\edge.exe",
    "edgedriver": "bin\\\\webdrivers\\\\edge\\\\123.0.2420.97\\\\msedgedriver.exe"
  },
  "headers": {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
  },
  "proxy_enabled": false
}
```

---

## 4. Playwright Crawler

### Description

The Playwright Crawler provides functionality for browser automation using the Playwright library. It supports customizing proxies, user agents, window sizes, and other parameters.

### Settings

- **max_requests**: Maximum number of requests.
- **headless**: Headless browser mode.
- **browser_type**: Type of browser (`chromium`, `firefox`, `webkit`).
- **user_agent**: User agent string.
- **proxy**: Proxy server settings.
- **viewport**: Size of the browser window.
- **timeout**: Timeout for requests.
- **ignore_https_errors**: Ignore HTTPS errors.

### Example Configuration (`playwrid.json`)

```json
{
  "max_requests": 10,
  "headless": true,
  "browser_type": "chromium",
  "options": ["--disable-dev-shm-usage", "--no-sandbox"],
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
  "proxy": {
    "enabled": false,
    "server": "http://proxy.example.com:8080",
    "username": "user",
    "password": "password"
  },
  "viewport": {
    "width": 1280,
    "height": 720
  },
  "timeout": 30000,
  "ignore_https_errors": false
}
```

---

## 5. BeautifulSoup and XPath Parser

### Description

This module is for parsing HTML content using BeautifulSoup and XPath. It allows you to extract data from local files or web pages.

### Settings

- **default_url**: Default URL for loading HTML.
- **default_file_path**: Default file path.
- **default_locator**: Default locator for extracting elements.
- **logging**: Logging settings.
- **proxy**: Proxy server settings.
- **timeout**: Timeout for requests.
- **encoding**: Encoding for reading files or requests.

### Example Configuration (`bs.json`)

```json
{
  "default_url": "https://example.com",
  "default_file_path": "file://path/to/your/file.html",
  "default_locator": {
    "by": "ID",
    "attribute": "element_id",
    "selector": "//*[@id=\'element_id\']"
  },
  "logging": {
    "level": "INFO",
    "file": "logs/bs.log"
  },
  "proxy": {
    "enabled": false,
    "server": "http://proxy.example.com:8080",
    "username": "user",
    "password": "password"
  },
  "timeout": 10,
  "encoding": "utf-8"
}
```

---

## Conclusion

This document provides an overview of the webdrivers available in the project, including their configuration and options. Each webdriver is designed to handle different browser interactions and data scraping needs. Refer to the specific JSON configuration files for detailed customization and usage instructions.