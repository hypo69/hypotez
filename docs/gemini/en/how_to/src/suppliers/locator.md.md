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
This code defines a set of locators for web elements on a product page. Each locator is a dictionary containing information about how to find the element on the page and what actions to perform with it.

Execution Steps
-------------------------
1. Define a dictionary of locators, where the key is the name of the field in the `ProductFields` class and the value is a locator dictionary.
2. Each locator dictionary contains the following keys:
    - `attribute`: The attribute to get from the web element. 
    - `by`: The strategy to use to find the element.
    - `selector`: The selector that defines how to find the web element.
    - `if_list`:  Determines how to handle a list of found web elements.
    - `use_mouse`:  Indicates whether to use the mouse for interaction with the element.
    - `event`:  Specifies an action to perform on the found element.
    - `mandatory`:  Indicates whether the locator is mandatory.
    - `locator_description`:  A description of what the locator does.

Usage Example
-------------------------

```python
# This example assumes that the 'd' variable is a WebDriver object
# and 'ProductFields' is a class defined in the project

from src.webdirver import Driver, Chrome, Firefox, Playwright
d = Driver(Chrome)

product_data = {
    'name': d.execute_locator('name'),
    'price': d.execute_locator('price'),
    # ... more fields
}

f = ProductFields(**product_data)
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".

```markdown
### Example of a Locator:

```json
"close_banner": {
    "attribute": null, 
    "by": "XPATH",
    "selector": "//button[@id = \'closeXButton\']",
    "if_list": "first",
    "use_mouse": false,
    "mandatory": false,
    "timeout": 0,
    "timeout_for_event": "presence_of_element_located",
    "event": "click()",
    "locator_description": "Closes the pop-up window. If the window is not present, it's not a problem (`mandatory`: `false`)."
  },
  "additional_images_urls": {
    "attribute": "src",
    "by": "XPATH",
    "selector": "//ol[contains(@class, \'flex-control-thumbs\')]//img",
    "if_list": "all",
    "use_mouse": false,
    "mandatory": false,
    "timeout": 0,
    "timeout_for_event": "presence_of_element_located",
    "event": null,
    "locator_description": "Retrieves a list of URLs for additional images."
  },
  "id_supplier": {
    "attribute": "innerText",
    "by": "XPATH",
    "selector": "//span[@class = \'ltr sku-copy\']",
    "if_list": "first",
    "use_mouse": false,
    "mandatory": true,
    "timeout": 0,
    "timeout_for_event": "presence_of_element_located",
    "event": null,
    "locator_description": "SKU Morlevi."
  },
  "default_image_url": {
    "attribute": null,
    "by": "XPATH",
    "selector": "//a[@id = \'mainpic\']//img",
    "if_list": "first",
    "use_mouse": false,
    "timeout": 0,
    "timeout_for_event": "presence_of_element_located",
    "event": "screenshot()",
    "mandatory": true,
    "locator_description": "Note! In Morlevi, the image is obtained using `screenshot` and returned as PNG (`bytes`)."
  }
```

### Details:

The dictionary name corresponds to the field name in the `ProductFields` class ([learn more about `ProductFields`](../product/product_fields)).

For example, the locator `name {}` will be used to get the product name, the locator `price {}` will be used to get the product price, etc.

```python
f = ProductFields(
    name = d.execute_locator('name'),
    price = d.execute_locator('price'),
    ...
)
```

In addition, you can create your own locators for additional actions on the page.
For example, `close_banner {}` will be used to close the banner on the page.

The locator dictionary contains the following keys:

- **`attribute`**: The attribute that needs to be obtained from the web element. For example: `innerText`, `src`, `id`, `href`, etc.
    If you set the value of `attribute` to `none/false`, then WebDriver will return the entire web element (`WebElement`).

- **`by`**: The strategy for finding the element:
    - `ID` corresponds to `By.ID`
    - `NAME` corresponds to `By.NAME`
    - `CLASS_NAME` corresponds to `By.CLASS_NAME`
    - `TAG_NAME` corresponds to `By.TAG_NAME`
    - `LINK_TEXT` corresponds to `By.LINK_TEXT`
    - `PARTIAL_LINK_TEXT` corresponds to `By.PARTIAL_LINK_TEXT`
    - `CSS_SELECTOR` corresponds to `By.CSS_SELECTOR`
    - `XPATH` corresponds to `By.XPATH`

- **`selector`**: The selector that defines how to find the web element. Examples:
    `(//li[@class = 'slide selected previous'])[1]//img`,
    `//a[@id = 'mainpic']//img`,
    `//span[@class = 'ltr sku-copy']`.

- **`if_list`**: Determines what to do with the list of found web elements (`web_element`). Possible values:
    - `first`: select the first element from the list.
    - `all`: select all elements.
    - `last`: select the last element.
    - `even`, `odd`: select even/odd elements.
    - Specifying specific numbers, for example, `1,2,...` or `[1,3,5]`: select elements with the specified numbers.

    An alternative way is to specify the element number directly in the selector, for example:
    `(//div[contains(@class, 'description')])[2]//p`

- **`use_mouse`**: `true` | `false`
    Used to perform actions with the mouse.

- **`event`**: WebDriver can perform an action on a web element, for example, `click()`, `screenshot()`, `scroll()`, etc.
    **Important❗**: If `event` is specified, it will be executed **before** getting the value from `attribute`.
    For example:
    ```json
    {
        ...
        "attribute": "href",
        ...
        "timeout": 0,
        "timeout_for_event": "presence_of_element_located",
        "event": "click()",
        ...
    }
    ```
    In this case, the driver will first perform `click()` on the web element, and then get its `href` attribute.
    The principle of operation: **action -> attribute**.
    More event examples:
    - `screenshot()` returns the web element as a screenshot. Useful when the `CDN` server does not return the image through `URL`.
    - `send_message()` - sends a message to the web element.
        I recommend sending a message through the `%EXTERNAL_MESSAGE%` variable, as shown below:
        ```json
        {"timeout": 0,
         "timeout_for_event": "presence_of_element_located",
         "event": "click();backspace(10);%EXTERNAL_MESSAGE%"
        }
        ```

        ```
        executes the sequence:
        <ol type="1">
          <li><code>click()</code> - clicks on the web element (sets the focus to the input field) <code>&lt;textbox&gt;</code>.</li>
          <li><code>backspace(10)</code> - moves the cursor 10 characters to the left (clears the text in the input field).</li>
          <li><code>%EXTERNAL_MESSAGE%</code> - sends a message to the input field.</li>
        </ol>

        ```

- **`mandatory`**: Whether the locator is mandatory.
    If `{mandatory: true}` and interaction with the web element is not possible, the code will throw an error. If `mandatory: false`, the element will be skipped.

- **`locator_description`**: A description of the locator.

---

### Complex Locators:

Lists, tuples, or dictionaries can be passed into the locator keys.

#### Example of a Locator with Lists:

```json
"sample_locator": {
    "attribute": [
      null,
      "href"
    ],
    "by": [
      "XPATH",
      "XPATH"
    ],
    "selector": [
      "//a[contains(@href, '#tab-description')]",
      "//div[@id = 'tab-description']//p"
    ],
    "timeout": 0,
    "timeout_for_event": "presence_of_element_located",
    "event": [
      "click()",
      null
    ],
    "if_list": "first",
    "use_mouse": [
      false,
      false
    ],
    "mandatory": [
      true,
      true
    ],
    "locator_description": [
      "Click on the tab to open the description field.",
      "Read data from the div."
    ]
  }
```
In this example, the element `//a[contains(@href, '#tab-description')]` will be found first.
The driver will execute the `click()` command, then get the value of the `href` attribute of the element `//a[contains(@href, '#tab-description')]`.

#### Example of a Locator with a Dictionary:

```json
"sample_locator": {
  "attribute": {"href": "name"},
  ...
}
```

---

### Description of Locator Keys:

1. **`attribute`**:
    This key indicates the attribute that will be used to find the element. In this case, the value is `null`, which means that the attribute is not used for searching.

2. **`by`**:
    Indicates the method for finding the element on the page. In this case, it is `'XPATH'`, which means using XPath to find the element.

3. **`selector`**:
    This is a string representing the locator that will be used to find the element. In this case, it is the XPath expression `"//a[@id = 'mainpic']//img"`, which means finding the image inside the `a` tag with `id='mainpic'`.

4. **`if_list`**:
    Indicates the rule for handling the list of elements. In this case, `'first'` is specified, which means that if there are multiple elements, the first element from the found list will be returned.

5. **`use_mouse`**:
    A boolean value that indicates whether to use the mouse to interact with the element. In this case, `false` is set, which means the mouse is not used.

6. **`timeout`**:
    The wait time (in seconds) to find the element. In this case, the value `0` is set, which means that the element search will be performed immediately without waiting.

7. **`timeout_for_event`**:
    The wait time (in seconds) for the event. In this case, `"presence_of_element_located"` is specified, which means that WebDriver will wait for the element to appear before executing the event.

8. **`event`**:
    Indicates what event should be performed on the found element. For example, it can be `click()`, to click on the element, or `screenshot()`, to take a screenshot of the element.

9. **`mandatory`**:
    Indicates whether the locator is mandatory. If the value is set to `true`, then if the element is not found or it is not possible to interact with it, an error will be thrown.

10. **`locator_description`**:
    A description of what the locator does to help understand its purpose.

-----------------
- The page layout can change. For example, desktop/mobile versions. In this case, I recommend keeping multiple locator files for each of the versions.
For example: `product.json`, `product_mobile_site.json`

By default, locators are read from the `product.json` file. Here's how you can change this:
In the supplier's page graber file, check for the `url`
```python
    async def grab_page(self) -> ProductFields:
        ...
         = driver
        if 'ksp.co.il/mob' in d.current_url: # <- sometimes connects to the mobile version of the site
            self.locator = j_loads_ns(gs.path.src / 'suppliers' / 'ksp' / 'locators' / 'product_mobile_site.json')
        ...
```
### Where locators are located:
```text
src/
├── suppliers/
│   ├── suppliers_list/
│   │   ├── supplier_a/
│   │   │   ├── __init__.py
│   │   │   ├── graber.py  # <--- Module for supplier_a
│   │   │   └── locators/
│   │   │       └── category.json # <--- Locators for supplier_a
│   │   ├── supplier_b/
│   │   │   ├── __init__.py
│   │   │   ├── graber.py  # <--- Module for supplier_b
│   │   │   └── locators/
│   │   │       └── category.json
│   │   └── ...
│   └── ...
└── ...
```

Learn more about locators in `locator.ru.md` in the `webdrivaer` module
                ```