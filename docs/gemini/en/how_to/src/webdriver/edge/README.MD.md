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
This code block defines a `Edge` class that represents the Edge WebDriver, handling its configuration, initialization, and interaction with the browser. It integrates with the `edge.json` configuration file to specify settings such as user agent, browser profiles, and executable path.

Execution Steps
-------------------------
1. **Import and Initialize:**
   - Import the `Edge` class from the `src.webdriver.edge` module.
   - Instantiate the `Edge` object, providing optional arguments for user agent and custom options.

2. **Configure WebDriver:**
   - The `Edge` class loads configuration settings from the `edge.json` file.
   - These settings define browser options, profiles, executable path, and HTTP headers.
   - Settings are applied to the WebDriver instance during initialization.

3. **Browser Interaction:**
   - Use the `get` method to navigate to a website.
   - Use the `quit` method to close the browser.

4. **Singleton Pattern:**
   - The `Edge` WebDriver uses the Singleton pattern, ensuring only one instance is created.
   - If an instance already exists, the same instance is reused, and a new window is opened.

5. **Logging and Debugging:**
   - The WebDriver utilizes the `logger` module from `src.logger` for logging errors, warnings, and informational messages.
   -  This provides a detailed log of initialization, configuration issues, and WebDriver errors, aiding in debugging.

Usage Example
-------------------------

```python
from src.webdriver.edge import Edge

# Initialize Edge WebDriver with a custom user agent and additional options
browser = Edge(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)", options=["--headless", "--disable-gpu"])

# Navigate to a website
browser.get("https://www.example.com")

# Close the browser
browser.quit()
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".