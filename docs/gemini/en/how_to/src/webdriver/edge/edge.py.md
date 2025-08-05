**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use This Code Block
=========================================================================================

Description
-------------------------
The `Edge` class provides a customized WebDriver for interacting with the Microsoft Edge browser. It simplifies configuration by using the `fake_useragent` library for random user-agent generation and a JSON configuration file to define WebDriver options, executable paths, and profile settings.

Execution Steps
-------------------------
1. **Initialization:**
   - The `__init__` method initializes the WebDriver instance. It takes optional arguments like the user agent string, a list of Edge options, and window mode settings.
   - It loads configuration data from the `edge.json` file located within the project's `webdriver/edge` directory.
   - It sets the user agent string and configures options based on the provided arguments and the configuration file.
   - It initializes a `EdgeService` object with the executable path and initializes the `WebDriver` instance.
2. **Custom Payload:**
   - The `_payload` method adds custom executors for locators and JavaScript scenarios.
   - It creates instances of the `ExecuteLocator` and `JavaScript` classes, which provide methods for interacting with web elements and executing JavaScript.
3. **Setting Options:**
   - The `set_options` method creates and configures launch options for the Edge WebDriver. It takes an optional list of options and adds them to an `EdgeOptions` object.

Usage Example
-------------------------

```python
from hypotez.src.webdriver.edge import Edge

# Initialize Edge WebDriver with full window mode
driver = Edge(window_mode='full_window')

# Navigate to a website
driver.get("https://www.example.com")
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".