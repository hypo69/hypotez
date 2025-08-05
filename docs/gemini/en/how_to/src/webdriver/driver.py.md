**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the `Driver` Class
=========================================================================================

Description
-------------------------
The `Driver` class provides a unified interface for interacting with Selenium web drivers. It supports various browsers like Chrome, Firefox, and Edge.

Execution Steps
-------------------------
1. **Initialization**:
    - Create a new `Driver` instance by passing the desired WebDriver class (e.g., `Chrome`, `Firefox`) as the first argument to the constructor. 
    - You can also provide additional arguments and keyword arguments specific to the chosen WebDriver.

2. **Methods**:
    - The `Driver` class provides various methods for interacting with the web browser, including:
        - `get_url(url: str) -> bool`: Navigates to the given URL.
        - `scroll(scrolls: int = 1, frame_size: int = 600, direction: str = 'both', delay: float = .3) -> bool`: Scrolls the page in a specified direction.
        - `locale() -> Optional[str]`: Detects the language of the page based on meta tags or JavaScript.
        - `wait(delay: float = .3) -> None`: Waits for a specified amount of time.
        - `_save_cookies_localy() -> None`: Saves the current cookies of the web driver to a local file.
        - `fetch_html(url: Optional[str] = '') -> bool`: Fetches HTML content from a local file or web URL and stores it.

3. **Usage Example**:

```python
from src.webdriver import Driver, Chrome  # Import Driver and Chrome classes

# Initialize a Chrome WebDriver
driver = Driver(Chrome, executable_path='/path/to/chromedriver')  

# Navigate to a URL
driver.get_url('https://www.example.com')

# Scroll the page down 
driver.scroll(scrolls=3, direction='down')

# Get the language of the page
lang = driver.locale()

# Print the detected language
print(lang)  # Output: 'en' (or None if not detected)

# Fetch HTML content from a local file
driver.fetch_html('file:///path/to/local/file.html')

# Access other WebDriver methods
# Example: Close the browser
driver.quit()
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".