**Instructions for Using the Playwright Crawler Module**

=========================================================================================

## Description

This module provides a custom implementation of the `PlaywrightCrawler` using the Playwright library. It allows you to configure browser launch parameters, such as user-agent, proxy, window size, and other settings defined in the `playwrid.json` file. 

## Key Features

- **Centralized Configuration**: Configuration is managed through the `playwrid.json` file.
- **User Option Support**: Ability to pass custom options during initialization.
- **Improved Logging and Error Handling**: Provides detailed logs for initialization, configuration issues, and WebDriver errors.
- **Proxy Support**: Setting up a proxy server to bypass restrictions.
- **Flexible Browser Settings**: Ability to customize window size, user-agent, and other parameters.

## Requirements

Before using this module, make sure you have the following dependencies installed:

- Python 3.x
- Playwright
- Crawlee

Install the necessary Python dependencies:

```bash
pip install playwright crawlee
```

Additionally, ensure Playwright is installed and configured to work with the browser. Install browsers using the command:

```bash
playwright install
```

## Configuration

Configuration for the Playwright Crawler is stored in the `playwrid.json` file. Below is an example of the configuration file structure and its description:

### Example Configuration (`playwrid.json`)

```json
{
  "browser_type": "chromium",
  "headless": true,
  "options": [
    "--disable-dev-shm-usage",
    "--no-sandbox",
    "--disable-gpu"
  ],
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

### Configuration Field Descriptions

#### 1. `browser_type`

The type of browser to use. Possible values:

- `chromium` (default)
- `firefox`
- `webkit`

#### 2. `headless`

A boolean value indicating whether the browser should be launched in headless mode. Default is `true`.

#### 3. `options`

A list of command-line arguments passed to the browser. Examples:

- `--disable-dev-shm-usage`: Disables the use of `/dev/shm` in Docker containers.
- `--no-sandbox`: Disables sandbox mode.
- `--disable-gpu`: Disables GPU hardware acceleration.

#### 4. `user_agent`

The user-agent string to be used for browser requests.

#### 5. `proxy`

Proxy server settings:

- **enabled**: A boolean value indicating whether to use a proxy.
- **server**: The address of the proxy server.
- **username**: The username for authentication on the proxy server.
- **password**: The password for authentication on the proxy server.

#### 6. `viewport`

The dimensions of the browser window:

- **width**: The width of the window.
- **height**: The height of the window.

#### 7. `timeout`

The maximum waiting time for operations (in milliseconds). Default is `30000` (30 seconds).

#### 8. `ignore_https_errors`

A boolean value indicating whether to ignore HTTPS errors. Default is `false`.

## Usage

To use `Playwrid` in your project, simply import it and initialize it:

```python
from src.webdriver.playwright import Playwrid

# Initialize the Playwright Crawler with custom options
browser = Playwrid(options=["--headless"])

# Launch the browser and navigate to the website
browser.start("https://www.example.com")
```

The `Playwrid` class automatically loads settings from the `playwrid.json` file and uses them to configure the WebDriver. You can also specify a custom user-agent and pass additional options when initializing the WebDriver.

## Logging and Debugging

The WebDriver class uses `logger` from `src.logger` to log errors, warnings, and general information. Any problems encountered during initialization, configuration, or execution will be written to the logs for easy debugging.

### Example Logs

- **Error during WebDriver initialization**: `Error initializing Playwright Crawler: <error details>`
- **Configuration issues**: `Error in playwrid.json file: <problem details>`

## License

This project is licensed under the MIT License. For details, see the [LICENSE](../../LICENSE) file.