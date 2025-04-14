Okay, here is the comprehensive guide translated into English, followed by a set of *new and different* examples for each method to illustrate diverse use cases.

---

## Complete Guide: Effective Interaction with Web Elements using `ExecuteLocator`

The `ExecuteLocator` class is a powerful tool within your automation framework, designed to simplify and standardize the process of finding web elements and performing actions on them using Selenium WebDriver. Its primary goal is to provide a unified, asynchronous interface that abstracts the complexities of waiting for elements, handling various Selenium exceptions, and executing standard interactions like clicks, text input, attribute retrieval, and much more.

**Key Advantages:**

*   **Asynchronicity:** All I/O-bound operations (waiting for elements, interacting with the driver) are performed asynchronously (`async`/`await`), allowing your application to remain responsive while waiting for page loads or element appearances.
*   **Abstraction:** Hides Selenium implementation details (like `WebDriverWait`, `expected_conditions`), offering higher-level methods.
*   **Unification:** Works with locators defined in a standardized format (Python dictionaries or `SimpleNamespace` objects), making them easier to manage.
*   **Error Handling:** Includes basic handling for timeouts and other common exceptions, with options for logging and controlling element necessity (`mandatory`).
*   **Flexibility:** Supports various location strategies (ID, XPath, CSS, Class Name, etc.) and diverse actions on elements.

### 1. Getting Started

Before using `ExecuteLocator`, ensure the following prerequisites are met:

1.  **Initialized WebDriver:** You must have an active instance of your custom `Driver` (e.g., `Firefox` from `src/webdriver/firefox/firefox.py`), which, in turn, manages a Selenium WebDriver instance.
2.  **`ExecuteLocator` Instance:** Create an object of `ExecuteLocator`, passing your active `driver` to it.
3.  **Asynchronous Environment:** Since all `ExecuteLocator` methods are coroutines (`async def`), they must be called using the `await` keyword inside another asynchronous function.
4.  **Locator Format:** You need to define locators for the elements you want to interact with. A locator is a Python dictionary or a `types.SimpleNamespace` object describing how to find an element and what to do with it.

```python
import asyncio
from types import SimpleNamespace
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys # For send_keys

# --- Mock Objects for Demonstration ---
class MockWebElement:
    def get_attribute(self, attr): print(f"  [Mock] Getting attribute: {attr}"); return f"value_of_{attr}" if attr != 'textContent' else "Mock Text Content"
    def click(self): print("  [Mock] Clicked element")
    def send_keys(self, keys): print(f"  [Mock] Sent keys: {keys}")
    def clear(self): print("  [Mock] Cleared element")
    @property
    def screenshot_as_png(self): print("  [Mock] Took screenshot"); return b"PNG_MOCK_DATA"
    def __repr__(self): return "<MockWebElement>"

class MockDriver:
    _elements_found = [MockWebElement(), MockWebElement(), MockWebElement()] # Simulate finding multiple elements
    def find_elements(self, by, selector): print(f"  [Mock] Searching MULTIPLE by {by} for '{selector}'"); return self._elements_found
    def find_element(self, by, selector): print(f"  [Mock] Searching SINGLE by {by} for '{selector}'"); return self._elements_found[0]
    def execute_script(self, script, *args): print(f"  [Mock] Executing script: {script[:50]}..."); return True
    def current_url(self): return "https://example.com/products?category=electronics&sort=price_desc&page=2"
    # Add other Selenium methods as needed for tests
    class MockActionChains:
        def move_to_element(self, el): print(f"  [Mock] Moved to {el}"); return self
        def send_keys(self, keys): print(f"  [Mock AC] Sent keys: {keys}"); return self
        def pause(self, duration): print(f"  [Mock AC] Paused for {duration}s"); return self
        def key_down(self, key): print(f"  [Mock AC] Key down: {key}"); return self
        def key_up(self, key): print(f"  [Mock AC] Key up: {key}"); return self
        def perform(self): print("  [Mock AC] Performed actions")
    def ActionChains(self, driver_instance): return self.MockActionChains()

# --- Initialization ---
driver = MockDriver() # Using a mock for example purposes
# executor = ExecuteLocator(driver) # In real code, use your actual driver

# --- Locator Structure (Detailed) ---
# locator_example = {
#     "locator_description": "Login button on the main page", # Optional description for logging
#     "by": By.XPATH,                  # Required: Search method (from selenium.webdriver.common.by.By) or string "url", "value"
#     "selector": "//button[@id='login']", # Required (except for by='value'/'url'): Selector for searching
#     "attribute": None,               # Optional: Name of the attribute to extract ('href', 'value', 'src', 'textContent', 'data-id', "{'key_attr':'value_attr'}")
#     "event": None,                   # Optional: Action to perform ('click()', 'clear();type(text)', 'send_keys(ENTER)', 'screenshot()', 'pause(2)', 'upload_media()')
#     "if_list": "first",              # Optional ('all'|'first'|'last'|'even'|'odd'|int|list[int]): How to handle if multiple elements are found. Default 'all'.
#     "mandatory": True,               # Optional (True|False): Should it be an error if the element is not found within the timeout? Default None (depends on context).
#     "timeout": 10,                   # Optional (float): Maximum waiting time for the element (in seconds). 0 - no wait.
#     "timeout_for_event": "presence_of_element_located", # Optional: Selenium wait condition ('presence...', 'visibility...')
# }
# Can use SimpleNamespace for convenient dot access:
# locator_ns = SimpleNamespace(**locator_example)
```

### 2. Getting a Web Element (`get_webelement_by_locator`)

**Purpose:** This method is used when you need the actual `WebElement` object (or a list of objects) returned by Selenium. This is useful if you need to perform custom actions on the element not covered by standard `execute_event` actions, or if you need to pass the element to another function/method.

**How it works:**
1.  Accepts a locator (dict or SimpleNamespace).
2.  Uses `by` and `selector` to find the element(s).
3.  Considers `timeout` and `timeout_for_event` for waiting.
4.  Applies the `if_list` rule to filter the list of found elements if multiple are returned.
5.  Returns a `WebElement`, a list `[WebElement]`, or `None` if the element is not found (and `mandatory=False` or not explicitly set to `True` in a critical context).

**(New) Example 1: Get all list items within a specific menu**

```python
async def example_get_all_list_items():
    print("\n--- Example: get_webelement_by_locator (all elements) ---")
    locator = SimpleNamespace(
        locator_description="All items in the side menu",
        by=By.CSS_SELECTOR,
        selector="ul#side-menu > li", # Selects all direct li children of ul with id side-menu
        if_list="all", # Explicitly get all matches
        timeout=5
    )
    try:
        menu_items = await executor.get_webelement_by_locator(locator)
        if menu_items:
            # menu_items will be a list of MockWebElement objects
            print(f"Found {len(menu_items)} menu items: {menu_items}")
        else:
            print(f"No menu items found for selector '{locator.selector}'.")
    except Exception as e:
        print(f"Error finding menu items: {e}")

# asyncio.run(example_get_all_list_items())
```

**(New) Example 2: Get the third product image on the page**

```python
async def example_get_nth_element():
    print("\n--- Example: get_webelement_by_locator (nth element) ---")
    locator = SimpleNamespace(
        locator_description="Third product image",
        by=By.CSS_SELECTOR,
        selector="div.product-gallery img.product-thumbnail",
        if_list=3, # Get the 3rd element (index 2)
        timeout=10,
        mandatory=False
    )
    try:
        third_image = await executor.get_webelement_by_locator(locator)
        if third_image:
             # third_image will be a single MockWebElement
            print(f"Found the third product image: {third_image}")
        else:
            print("Less than three product images found or selector invalid.")
    except Exception as e:
        print(f"Error finding the third image: {e}")

# asyncio.run(example_get_nth_element())
```

### 3. Getting an Element's Attribute (`get_attribute_by_locator`)

**Purpose:** Used to extract the value of a specific HTML attribute (e.g., `href`, `src`, `value`, `class`, `id`, `style`, `data-*`) or the text content of an element.

**How it works:**
1.  Finds the element(s) using `get_webelement_by_locator` with `by`, `selector`, `timeout`, `if_list`.
2.  If the element(s) are found, extracts the value of the attribute specified in the `attribute` field.
3.  Supports getting text content via `attribute="textContent"` or `attribute="innerText"`.
4.  Supports the special format `attribute="{key_attr:value_attr}"` to extract key-value pairs where keys and values are themselves attributes of the element (useful for tables or `data-*` lists).
5.  Returns a string with the attribute value, a list of strings (if multiple elements found and `if_list='all'` or similar), a dictionary (for `{key:value}` format), a list of dictionaries, or `None` if the element/attribute is not found.

**(New) Example 1: Get the CSS classes of an active tab**

```python
async def example_get_class_attribute():
    print("\n--- Example: get_attribute_by_locator (attribute 'class') ---")
    locator = SimpleNamespace(
        locator_description="CSS Classes of the active navigation tab",
        by=By.CSS_SELECTOR,
        selector="nav .tab.active", # Find the element with both 'tab' and 'active' classes
        attribute="class", # Get the full class string
        timeout=5
    )
    try:
        active_tab_classes = await executor.get_attribute_by_locator(locator)
        if active_tab_classes is not None:
            print(f"Classes of the active tab: '{active_tab_classes}'") # Expect "value_of_class"
        else:
            print("Active tab or its class attribute not found.")
    except Exception as e:
        print(f"Error getting 'class' attribute: {e}")

# asyncio.run(example_get_class_attribute())
```

**(New) Example 2: Get the inline style of a specific container**

```python
async def example_get_style_attribute():
    print("\n--- Example: get_attribute_by_locator (attribute 'style') ---")
    locator = SimpleNamespace(
        locator_description="Inline style of the header container",
        by=By.ID,
        selector="header-container",
        attribute="style", # Get the inline style string
        timeout=3
    )
    try:
        header_style = await executor.get_attribute_by_locator(locator)
        if header_style is not None and header_style != "value_of_style": # Check if style is actually set
             print(f"Header inline style: '{header_style}'")
        elif header_style == "value_of_style": # Mock returns this
             print(f"Header inline style (mock): '{header_style}'")
        else:
            print("Header container or its style attribute not found/empty.")
    except Exception as e:
        print(f"Error getting 'style' attribute: {e}")

# asyncio.run(example_get_style_attribute())
```

### 4. Executing an Event (`execute_event`)

**Purpose:** This method performs predefined actions (events) on the located web element. It's the primary way to interact with the page.

**How it works:**
1.  Finds the element(s) using `get_webelement_by_locator`.
2.  Parses the `event` string. Events are separated by semicolons (`;`), allowing for chained actions.
3.  Executes each event sequentially:
    *   `click()`: Performs a click on the element. Handles `ElementClickInterceptedException`.
    *   `clear()`: Clears an input field (`<input>`, `<textarea>`).
    *   `type(text)`: Enters the specified `text` into an input field. Uses Selenium's `send_keys`. Can be used with `typing_speed`.
    *   `send_keys(KEY)`: Sends special keys (e.g., `ENTER`, `TAB`, `CONTROL+A`). Key names are taken from `selenium.webdriver.common.keys.Keys`. Combinations are specified with `+`, e.g., `send_keys(CONTROL+A)`.
    *   `screenshot()`: Takes a screenshot of *only this element* and returns binary PNG data.
    *   `pause(seconds)`: Pauses execution for the specified number of seconds (`asyncio.sleep`).
    *   `upload_media()`: Designed for `<input type="file">` fields. Uses `send_keys` to provide the file path, which is passed via the `message` parameter of the `execute_locator` or `execute_event` method call.
4.  Returns `True` if all events in the chain executed successfully, `False` in case of an error (e.g., element not found and `mandatory=True`, click intercepted, JS click error). If the event is `screenshot()`, it returns the binary screenshot data (or a list of data if multiple elements/screenshots).

**(New) Example 1: Upload a profile picture**

```python
async def example_event_upload_file():
    print("\n--- Example: execute_event (upload_media) ---")
    locator = SimpleNamespace(
        locator_description="File input for profile picture",
        by=By.CSS_SELECTOR,
        selector="input[type='file'][name='profile_pic']",
        event="upload_media()",
        timeout=5,
        mandatory=True
    )
    file_path = "C:\\path\\to\\your\\image.jpg" # IMPORTANT: Use the actual path to a file
    try:
        # The file path is passed as the 'message' argument
        success = await executor.execute_event(locator, message=file_path)
        print(f"Result of file upload attempt: {success}") # Expect True if element found
        # Mock will print: [Mock] Sent keys: C:\path\to\your\image.jpg
    except Exception as e:
        print(f"Error uploading file: {e}")

# asyncio.run(example_event_upload_file())
```

**(New) Example 2: Navigate through a form using TAB**

```python
async def example_event_send_tab_key():
    print("\n--- Example: execute_event (send_keys TAB) ---")
    locator = SimpleNamespace(
        locator_description="First name input field",
        by=By.ID,
        selector="firstName",
        event="send_keys(TAB)", # Send the TAB key to move to the next field
        timeout=5,
        mandatory=True
    )
    try:
        success = await executor.execute_event(locator)
        print(f"Result of sending TAB key: {success}") # Expect True
        # Mock will print: [Mock AC] Sent keys: Keys.TAB
    except Exception as e:
        print(f"Error sending TAB key: {e}")

# asyncio.run(example_event_send_tab_key())
```

**(New) Example 3: Click a button and wait for an animation/effect**

```python
async def example_event_click_and_pause():
    print("\n--- Example: execute_event (click and pause) ---")
    locator = SimpleNamespace(
        locator_description="Expand details button",
        by=By.XPATH,
        selector="//button[contains(@class, 'expand-details')]",
        event="click();pause(2)", # Click and then wait 2 seconds
        timeout=10
    )
    try:
        success = await executor.execute_event(locator)
        print(f"Result of click and pause: {success}") # Expect True
        # Mock will print: [Mock] Clicked element -> [Mock AC] Paused for 2s
    except Exception as e:
        print(f"Error during click and pause: {e}")

# asyncio.run(example_event_click_and_pause())
```

### 5. Getting an Element's Screenshot (`get_webelement_as_screenshot`)

**Purpose:** This is a specialized method, equivalent to calling `execute_event` with `event="screenshot()"`. It is solely intended for retrieving the binary PNG data of a specific element's screenshot.

**How it works:**
1.  Finds the element using `get_webelement_by_locator`.
2.  Calls the `.screenshot_as_png` method on the found `WebElement`.
3.  Returns the binary data (`bytes`) or `None` if the element is not found or an error occurs during screenshotting.

**(New) Example: Screenshot a field validation error message**

```python
async def example_direct_error_screenshot():
    print("\n--- Example: get_webelement_as_screenshot (error message) ---")
    locator = SimpleNamespace(
        locator_description="Email validation error message",
        by=By.CSS_SELECTOR,
        selector="div.error-message[data-field='email']",
        timeout=5,
        mandatory=False # Error might not be present
    )
    try:
        error_png = await executor.get_webelement_as_screenshot(locator)
        if error_png:
            print(f"Obtained screenshot data for error message: {len(error_png)} bytes")
        else:
            print("Could not take screenshot (error message element not found?).")
    except Exception as e:
        print(f"Error getting error message screenshot: {e}")

# asyncio.run(example_direct_error_screenshot())
```

### 6. Sending a Message (Simulated Typing) (`send_message`)

**Purpose:** This method is specifically designed to simulate *user typing* into input fields (`<input>`, `<textarea>`). It allows control over typing speed and handles special characters (like line breaks).

**How it works:**
1.  Finds the target element using `get_webelement_by_locator`.
2.  Moves the cursor to the element using `ActionChains`.
3.  Iterates through words and characters in the provided `message` string.
4.  For each character, uses `ActionChains.send_keys(character)`.
5.  If `typing_speed` (delay in seconds) is set, adds a pause (`ActionChains.pause`) after each character.
6.  Handles the `;` character as a command to press `Shift+Enter` (line break without submitting).
7.  Executes the accumulated actions using `ActionChains.perform()`.
8.  Returns `True` on success, `False` if the element is not found.

**(New) Example: Typing a multi-line address into a textarea**

```python
async def example_typing_address():
    print("\n--- Example: send_message (simulated typing - address) ---")
    locator = SimpleNamespace(
        locator_description="Address input textarea",
        by=By.ID,
        selector="address-field",
        timeout=5,
        mandatory=True
    )
    # Use ';' for Shift+Enter (new line in textarea)
    address = "123 Automation Lane;Suite 500;Testville, CA 90210"
    try:
        # Simulate typing at approx 10 chars/sec
        success = await executor.send_message(
            locator,
            message=address,
            typing_speed=0.1
        )
        if success:
            # Mock ActionChains will show the simulated key presses including Shift+Enter
            print("Address typed successfully.")
        else:
            print("Failed to type address.")
    except Exception as e:
        print(f"Error typing address: {e}")

# asyncio.run(example_typing_address())
```

### 7. The Universal Method (`execute_locator`)

**Purpose:** This is the main, versatile method of the class. It analyzes the provided locator and decides internally which action to perform: get an element, extract an attribute, or execute an event. Use it when you don't need to explicitly specify the type of operation.

**How it works:**
1.  Accepts a locator (dict or SimpleNamespace), `timeout`, `timeout_for_event`, `message`, `typing_speed`.
2.  **Checks `by`:**
    *   If `by == 'value'`, it simply returns the value from the locator's `attribute` field (interpreted as a constant).
    *   If `by == 'url'`, it extracts the parameter value from `driver.current_url`, with the parameter name taken from `attribute`.
3.  **Checks `event`:** If the `event` field is populated, it calls `execute_event` to perform the specified event(s).
4.  **Checks `attribute`:** If `event` is empty but `attribute` is populated, it calls `get_attribute_by_locator` to extract the attribute.
5.  **Default:** If `event` and `attribute` are empty (and `by` is not 'value'/'url'), it calls `get_webelement_by_locator` to get the web element itself.
6.  Returns the result from the corresponding called method (`WebElement`, `list[WebElement]`, `str`, `list[str]`, `dict`, `list[dict]`, `bool`, `bytes`, `list[bytes]`, or `None`).

**(New) Examples using `execute_locator`:**

```python
async def example_universal_executor_new():
    print("\n--- Example: execute_locator (universal) - New Cases ---")

    # Case 1: Get element (different selector)
    locator_element = SimpleNamespace(by=By.PARTIAL_LINK_TEXT, selector="Terms of", timeout=3)
    result1 = await executor.execute_locator(locator_element)
    print(f"Result 1 (Expect WebElement for 'Terms of...'): {result1}")

    # Case 2: Get text content (attribute='textContent')
    locator_attr = SimpleNamespace(by=By.CSS_SELECTOR, selector="h1", attribute="textContent", timeout=2)
    result2 = await executor.execute_locator(locator_attr)
    print(f"Result 2 (Expect H1 text): '{result2}'") # Mock Text Content

    # Case 3: Execute 'clear' event
    locator_event = SimpleNamespace(by=By.ID, selector="search-input", event="clear()", timeout=5)
    result3 = await executor.execute_locator(locator_event)
    print(f"Result 3 (Expect True/False from clear): {result3}") # True

    # Case 4: Get different URL parameter (by='url')
    locator_url = SimpleNamespace(by="url", attribute="sort") # Get 'sort' param
    result4 = await executor.execute_locator(locator_url)
    print(f"Result 4 (Expect value of 'sort' URL param): '{result4}'") # price_desc

# asyncio.run(example_universal_executor_new())
```

### 8. Best Practices and Tips

*   **Choose Reliable Selectors:** Prefer IDs (if unique and static), then CSS selectors, and use XPath sparingly (especially avoid absolute XPath). Utilize `data-*` attributes if available.
*   **Use `locator_description`:** Add descriptions to your locators to improve log readability and ease debugging.
*   **Configure Timeouts:** Select appropriate `timeout` values based on the expected element load time. Avoid excessively long timeouts unless necessary.
*   **Manage `mandatory`:** Set `mandatory=True` only for elements whose absence constitutes a critical failure for your script. For optional elements, leave it as `False` or `None`.
*   **Understand `if_list`:** Use `if_list` to precisely specify which element you need if your selector might return multiple matches.
*   **Asynchronicity:** Remember all calls must use `await`. Use `asyncio.gather` to run independent locator operations in parallel if needed.
*   **Logging:** Study the logs generated by your `logger` to diagnose issues with element location or event execution.

---

This guide provides a comprehensive overview of the `ExecuteLocator` class's capabilities. By using its methods correctly, you can significantly enhance the reliability, readability, and efficiency of your web automation code.