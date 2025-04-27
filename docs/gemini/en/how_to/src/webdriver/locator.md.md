**Locators for Web Elements**

========================================================================================

**Description**
-------------------------
Locators are structured descriptions (in JSON format in this case) that tell the web driver how to find a specific element (like a button, input field, image, or text block) on an HTML page. They contain information about the **search strategy** (e.g., XPath, CSS selector, ID) and the **selector value** (the specific XPath expression, CSS selector string, etc.). 

Additionally, a locator can include extra instructions:

* What **attribute** of the element to retrieve (e.g., `href`, `src`, `innerText`).
* What **action** (`event`) to perform on the element (e.g., `click()`, `screenshot()`).
* How to **handle** the situation if **multiple elements** are found (`if_list`).
* Whether to **wait** for the element to appear (`timeout`).
* Whether finding the element is **mandatory** (`mandatory`).

Each named JSON object in the `.json` files (located in the `locators/` directory of each supplier) represents one such locator, intended to find a specific field or perform an action on the page.

**Execution Steps**
-------------------------
1. The web driver uses the search strategy (`by`) and selector value (`selector`) to find the desired element on the HTML page. 
2. If the element is found, the web driver performs the specified actions (e.g., clicking, taking a screenshot, getting an attribute, or entering text).
3. The results of the action are returned based on the specified `attribute`, `if_list`, and `event`.

**Usage Example**
-------------------------

```python
# Inside the Graber class or its subclass
f = self.fields # An instance of ProductFields
# The name will be retrieved using the "name" locator from product.json
await self.name() # self.fields.name = await self.driver.execute_locator(self.product_locator.name)
# The price will be retrieved using the "price" locator
await self.price() # self.fields.price = await self.driver.execute_locator(self.product_locator.price)
...
```

**Example of a Locator**

```json
"close_banner": {
    "attribute": null, // Attribute not retrieved
    "by": "XPATH",     // Search strategy is XPath
    "selector": "//button[@id = 'closeXButton']", // Selector value (XPath expression)
    "if_list": "first", // If multiple found, take the first one
    "use_mouse": false, // Do not use mouse emulation
    "mandatory": false, // Locator is NOT mandatory (no error if not found)
    "timeout": 0,       // Element wait timeout (0 - do not wait)
    "timeout_for_event": "presence_of_element_located", // Wait condition before the event
    "event": "click()", // Action - click on the element
    "locator_description": "Close the pop-up window. If it doesn't appear, it's not a problem (`mandatory`: `false`). "
  },
```

**Details**

* The dictionary name (the top-level key in JSON, e.g., `"name"`, `"price"`, `"close_banner"`) usually corresponds to the field name of the `ProductFields` class ([more about `ProductFields`](../product/product_fields)) or describes the action being performed.

For example, the `name` locator will be used to get the product name, the `price` locator will be used to get the product price, and so on.

* You can also create your own locators to perform auxiliary actions on the page. For example, the `close_banner` locator is used to close the banner.

**Locator Keys**

* **`attribute`** (`string | null`): The attribute to get from the found web element (e.g.: `innerText`, `textContent`, `src`, `id`, `href`, `value`). If `null` or not specified *and* there is no `event`, WebDriver will return the web element itself (`WebElement`). If `event` is specified, `attribute` is often ignored (depends on `event`, e.g., `screenshot()` defines the return type itself).

* **`by`** (`string`): The strategy for finding the element. Corresponds to the constants in `selenium.webdriver.common.by.By`:
    *   `ID` -> `By.ID`
    *   `NAME` -> `By.NAME`
    *   `CLASS_NAME` -> `By.CLASS_NAME`
    *   `TAG_NAME` -> `By.TAG_NAME`
    *   `LINK_TEXT` -> `By.LINK_TEXT`
    *   `PARTIAL_LINK_TEXT` -> `By.PARTIAL_LINK_TEXT`
    *   `CSS_SELECTOR` -> `By.CSS_SELECTOR`
    *   `XPATH` -> `By.XPATH`
    *   `VALUE` (special value): Doesn't search for an element, but simply returns the value from the `attribute` field. Useful for setting static values (e.g., supplier ID).

* **`selector`** (`string`): The selector string that corresponds to the selected `by` strategy. Examples:
    *   For `XPATH`: `(//li[@class = 'slide selected previous'])[1]//img`, `//a[@id = 'mainpic']//img`, `//span[@class = 'ltr sku-copy']`
    *   For `CSS_SELECTOR`: `a#mainpic img`, `span.ltr.sku-copy`, `input[name='username']`
    *   For `ID`: `mainpic`
    *   For `VALUE`: Usually `"none"` or any other value, as the selector is not used.

* **`if_list`** (`string | list[int] | int`): Determines how to handle the list of found web elements (`web_elements`) if the search strategy returned more than one element:
    *   `first` (or `1`): select the first element (`web_elements[0]`).
    *   `last`: select the last element (`web_elements[-1]`).
    *   `all`: return the entire list of found elements (`web_elements`).
    *   `even`: select elements with even indices (`web_elements[0]`, `web_elements[2]`, ...).
    *   `odd`: select elements with odd indices (`web_elements[1]`, `web_elements[3]`, ...).
    *   `[1, 3, 5]` (list of ints): select elements with the specified indices (numbering from 1). Will return `[web_elements[0], web_elements[2], web_elements[4]]`.
    *   `3` (int): select the element with the specified number (numbering from 1). Will return `web_elements[2]`.
    *   *Alternative:* Often the desired element can be selected directly in the selector (especially in XPath), for example: `(//div[contains(@class, 'description')])[2]//p` will select `<p>` from the second `div`.

* **`use_mouse`** (`boolean`): `true` | `false`. Not currently used directly in `ExecuteLocator`, but may be reserved for future actions with `ActionChains` that require mouse emulation.

* **`event`** (`string | null`): The action that WebDriver should perform on the found web element(s).
    *   **Important❗**: If `event` is specified, it is usually performed **before** trying to get a value from `attribute` (if `attribute` is used at all).
    *   Examples:
        *   `click()`: Click on the element.
        *   `screenshot()`: Take a screenshot of the element. Returns `bytes`.
        *   `type(text)`: Enter the specified text into the element (e.g., an input field).
        *   `send_keys(KEYS_ENUM)`: Send special keys (e.g., `send_keys(ENTER)`). `KEYS_ENUM` should correspond to the attribute `selenium.webdriver.common.keys.Keys`.
        *   `clear()`: Clear the input field.
        *   `upload_media()`: Special event for uploading a file (expects the path to the file in `message` when calling `execute_locator`).
        *   `pause(seconds)`: Insert a pause (e.g., `pause(2)`).
        *   You can combine them using a semicolon: `clear();type(text);send_keys(ENTER)`
    *   If `event` is `null`, only the element search and/or attribute retrieval is performed.

* **`mandatory`** (`boolean`): Whether finding and successfully interacting with the element is mandatory.
    *   If `true`: In case of an error (element not found, not clickable, timeout, etc.), execution is interrupted (or raises an exception, depending on the handling).
    *   If `false`: In case of an error, the element is skipped, no error occurs, the method will return `None` or `False`.

* **`timeout`** (`float | int`): The wait time (in seconds) for the element to appear on the page before it is considered not found. If `0`, waiting is not used (`find_element(s)` is used instead of `WebDriverWait`).

* **`timeout_for_event`** (`string`): The `WebDriverWait` wait condition used if `timeout > 0`. Main values:
    *   `presence_of_element_located`: Wait until the element appears in the DOM (may be invisible).
    *   `visibility_of_element_located` / `visibility_of_all_elements_located`: Wait until the element(s) becomes visible.
    *   Other conditions from `selenium.webdriver.support.expected_conditions`.

* **`locator_description`** (`string`): An arbitrary text description of the locator for easy reading and debugging (printed in the logs).

---

**Complex Locators (Using Lists)**

* The keys `attribute`, `by`, `selector`, `event`, `use_mouse`, `mandatory`, `locator_description` can accept lists of the same length. This allows you to perform a sequence of actions.

**Example of a Locator with Lists**

```json
"description": {
    "attribute": [
      null,       // For the first step, the attribute is not needed
      "innerText" // For the second step - get the text
    ],
    "by": [
      "XPATH",    // Strategy for the first step
      "XPATH"     // Strategy for the second step
    ],
    "selector": [
      "//a[contains(@href, '#tab-description')]", // Selector for clicking on the tab
      "//div[@id = 'tab-description']//p"         // Selector for getting the description text
    ],
    "timeout": 0, // General timeout (can also be a list)
    "timeout_for_event": "presence_of_element_located", // General wait condition
    "event": [
      "click()",  // Click on the first step
      null        // No action on the second step
    ],
    "if_list": "first", // General rule for lists (can be a list)
    "use_mouse": false,  // General (can be a list)
    "mandatory": [
      true,       // The first step is mandatory
      true        // The second step is mandatory
    ],
    "locator_description": [
      "Clicking on the 'Description' tab.", // Description of the first step
      "Reading the text from the description block."  // Description of the second step
    ]
  }
```

In this example:

1. The element `//a[contains(@href, '#tab-description')]` (the "Description" tab) will be found.
2. `click()` will be performed on it.
3. Then the element `//div[@id = 'tab-description']//p` (paragraph inside the description block) will be found.
4. Its text content (`innerText`) will be retrieved.
This text will be the final result of executing this locator.

**Example of a Locator with a Dictionary in `attribute`**

```json
"specification_pairs": {
  "attribute": {"dt": "dd"}, // Key of the dictionary - selector for the key, Value - selector for the value
  "by": "XPATH",
  "selector": "//dl[@class='specifications-list']", // Parent element for pairs
  "if_list": "all", // Process all found pairs
  "mandatory": false,
  "timeout": 2,
  "timeout_for_event": "presence_of_element_located",
  "event": null,
  "locator_description": "Gets key-value pairs from the specifications list <dl>"
}
```

This format is used for extracting related data, such as "Characteristic: Value" pairs. The `get_attribute_by_locator` method in `ExecuteLocator` contains logic for handling such a dictionary: it finds the parent element (`//dl`), then within it searches for elements by the selectors from the key (`dt`) and value (`dd`) of the `attribute` dictionary and forms a Python dictionary `{key: value}`.

---

**Where Locators Are Located**

* Files with locators (`product.json`, `category.json`, etc.) are stored in the `locators` directory inside the folder of each specific supplier:

```text
src/
└── suppliers/
    ├── suppliers_list/
    │   ├── ksp/
    │   │   ├── __init__.py
    │   │   ├── graber.py  # <--- Graber class for ksp
    │   │   └── locators/  # <--- Folder with locators for ksp
    │   │       ├── product.json
    │   │       └── category.json
    │   ├── aliexpress/
    │   │   ├── __init__.py
    │   │   ├── graber.py
    │   │   └── locators/
    │   │       ├── product.json
    │   │       └── category.json
    │   └── ...
    ├── graber.py # Base Graber class
    └── get_graber_by_supplier.py # Graber factory
```

* Page layout can change (e.g., desktop/mobile versions). In such cases, it is recommended to create separate locator files for each version (e.g., `product_desktop.json`, `product_mobile.json`). You can implement the selection of the desired locator file in the `grab_page_async` method of the `Graber` subclass, checking, for example, the current URL:

```python
# Inside the Graber subclass (e.g., KspGraber)
class KspGraber(Graber):
    # ... __init__ ...

    async def grab_page_async(self, *args, **kwargs) -> ProductFields:
        # Check URL before loading default locators
        if 'ksp.co.il/mob' in self.driver.current_url:
            logger.info("Mobile version of the KSP website detected, loading mobile locators.")
            # Reload locators from the mobile file
            self.product_locator = j_loads_ns(__root__ / 'src' / 'suppliers' / 'suppliers_list' / self.supplier_prefix / 'locators' / 'product_mobile.json')
            self.category_locator = j_loads_ns(__root__ / 'src' / 'suppliers' / 'suppliers_list' / self.supplier_prefix / 'locators' / 'category_mobile.json')
        else:
            # Make sure desktop locators are used (if not loaded before or switched from mobile)
             self.product_locator = j_loads_ns(__root__ / 'src' / 'suppliers' / 'suppliers_list' / self.supplier_prefix / 'locators' / 'product.json')
             self.category_locator = j_loads_ns(__root__ / 'src' / 'suppliers' / 'suppliers_list' / self.supplier_prefix / 'locators' / 'category.json')


        # Further logic for collecting data...
        try:
            await super().grab_page_async(*args, **kwargs) # Call the base logic with the right locators
            return self.fields
        except Exception as ex:
            logger.error(f"Error in the `grab_page_async` function of KSP", ex)
            return None

```