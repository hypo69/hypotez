**How to Use the `src.logger` Module**

=========================================================================================

**Description**
-------------------------

The `src.logger` module provides a flexible logging system for Python applications. It supports logging to the console, files, and JSON format. It uses the Singleton design pattern to ensure a single logger instance is used throughout the application. The logger supports various logging levels (e.g., `INFO`, `ERROR`, `DEBUG`) and includes colorized output for console logging. You can also customize output formats and manage logging to different files.

**Execution Steps**
-------------------------

1. **Import the `Logger` Class:**
   ```python
   from src.logger import Logger
   ```

2. **Initialize the Logger:**
   - Create an instance of the `Logger` class:
     ```python
     logger: Logger = Logger()
     ```
   - Configure the logger with desired settings:
     ```python
     config = {
         'info_log_path': 'logs/info.log',
         'debug_log_path': 'logs/debug.log',
         'errors_log_path': 'logs/errors.log',
         'json_log_path': 'logs/log.json'
     }
     logger.initialize_loggers(**config)
     ```
   - This initializes loggers for console and file logging (information, debugging, errors, and JSON).

3. **Log Messages:**
   - Use methods like `info`, `success`, `warning`, `debug`, `error`, and `critical` to log messages at different levels:
     ```python
     logger.info('This is an informational message')
     logger.success('This message indicates a successful operation')
     logger.warning('This is a warning message')
     logger.debug('This is a debug message')
     logger.error('This is an error message')
     logger.critical('This is a critical message')
     ```

4. **Customize Output:**
   - Set colors for console output:
     ```python
     logger.info('This message will be green', colors=(colorama.Fore.GREEN, colorama.Back.BLACK))
     logger.error('This message has a red background', colors=(colorama.Fore.WHITE, colorama.Back.RED))
     ```

**Usage Example**
-------------------------

```python
from src.logger import Logger
import colorama

# Initialize the logger
logger: Logger = Logger()
config = {
    'info_log_path': 'logs/info.log',
    'debug_log_path': 'logs/debug.log',
    'errors_log_path': 'logs/errors.log',
    'json_log_path': 'logs/log.json'
}
logger.initialize_loggers(**config)

# Log messages at different levels
logger.info('This is an informational message')
logger.success('This message indicates a successful operation')
logger.warning('This is a warning message')
logger.debug('This is a debug message')
logger.error('This is an error message')
logger.critical('This is a critical message')

# Customize console output colors
logger.info('This message will be green', colors=(colorama.Fore.GREEN, colorama.Back.BLACK))
logger.error('This message has a red background', colors=(colorama.Fore.WHITE, colorama.Back.RED))
```

**Key Points**

- The `src.logger` module provides a robust and configurable logging system.
- You can easily log messages to the console, files, and in JSON format.
- The module supports different logging levels and allows for customization of output formats and colors.
- The Singleton design pattern ensures a single logger instance is used throughout your application.
- The module makes it easy to manage and debug your Python applications effectively.