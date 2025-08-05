**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the `Logger` Class
=========================================================================================

Description
-------------------------
The `Logger` class provides a centralized logging mechanism for the project. It supports console, file, and JSON logging with configurable levels and colors. It implements the Singleton pattern to ensure that only one instance of the logger exists.

Execution Steps
-------------------------
1. **Initialize the Logger**:  The `Logger` class is initialized with optional file paths for info, debug, errors, and JSON logs. If no file paths are provided, default paths are used. 
2. **Set Up Loggers**: The `__init__` method creates separate loggers for console, info file, debug file, errors file, and JSON file. Each logger is configured with its corresponding level and formatter.
3. **Log Messages**: The `Logger` class provides methods for logging messages at different levels: `info`, `warning`, `debug`, `error`, and `critical`. Each method accepts a message, optional exception information, and optional text and background colors. 
4. **Format and Output Messages**: The `_format_message` method formats the message with a log symbol, color, and exception information. It outputs the formatted message to the specified logger(s). 

Usage Example
-------------------------

```python
from src.logger.logger import logger

# Log an info message with a custom color
logger.info("Starting the application", text_color="green")

# Log a warning message
logger.warning("File not found: 'data.csv'")

# Log an error message with exception details
try:
    # ... some code that might raise an exception
except Exception as ex:
    logger.error("Error occurred during data processing", ex, exc_info=True)

# Log a debug message
logger.debug("Current value of 'x' is: {}".format(x))

# Log a success message
logger.success("Data processed successfully", text_color="yellow")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".