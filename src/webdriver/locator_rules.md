# Guide to Locators: Logic and Strategy

## Introduction

In web automation and scraping, a **locator** is a command that tells a script how to find a specific element on a web page. The `executor.py` module relies heavily on well-defined locators to interact with web pages. This guide explains what locators are, how to construct them, and the strategies for making them effective and resilient to changes in the web page structure.

## What is a WebElement?

A web page is structured as a tree of objects called the Document Object Model (DOM). Every item on the page—a button, a text field, an image, a paragraph—is represented as a node in this tree. A **WebElement** is the programming object that represents one of these nodes. To interact with a part of a web page (like clicking a button or typing in a search box), you first need to find its corresponding WebElement.

## What is a Locator?

A locator is essentially an address for a WebElement. It provides the necessary information to uniquely identify one or more elements on a page. In our framework, a locator is a structured object (a dictionary or `SimpleNamespace`) that contains all the instructions for finding and interacting with an element.

## Building a Locator: The Core Components

A locator has two fundamental components:

1.  **`by`**: This specifies the *strategy* to use for finding the element.
2.  **`selector`**: This is the *value* to use with the chosen strategy.

### Common Locator Strategies (`by`)

Here are the most common strategies supported by Selenium and our executor:

*   **`ID`**: Finds an element by its unique `id` attribute. This is usually the fastest and most reliable strategy.
    *   *Example Selector*: `"main-login-button"`
*   **`NAME`**: Finds an element by its `name` attribute, often used for form fields.
    *   *Example Selector*: `"username"`
*   **`CLASS_NAME`**: Finds elements that have a specific CSS class.
    *   *Example Selector*: `"product-title"`
*   **`TAG_NAME`**: Finds elements by their HTML tag name.
    *   *Example Selector*: `"h1"` (finds all top-level headings)
*   **`LINK_TEXT`**: Finds a link (`<a>` tag) by the exact text it displays.
    *   *Example Selector*: `"Sign In"`
*   **`PARTIAL_LINK_TEXT`**: Finds a link by a partial match of its visible text.
    *   *Example Selector*: `"Sign"`
*   **`CSS_SELECTOR`**: Finds elements using a CSS selector. This is very powerful and flexible.
    *   *Example Selector*: `"div#user-profile > span.username"`
*   **`XPATH`**: Finds elements using an XPath expression. This is the most powerful strategy, allowing you to navigate the entire DOM tree.
    *   *Example Selector*: `"//div[@id='user-profile']/span[@class='username']"`

## The `executor.py` Locator Structure

Our framework uses a detailed locator object that goes beyond just `by` and `selector`. This allows for complex interactions to be defined in a single, reusable object.

Here are the key fields:

*   `by` (str): The locator strategy (e.g., `"XPATH"`, `"ID"`).
*   `selector` (str): The selector value.
*   `attribute` (str, optional): The attribute to retrieve from the element (e.g., `"innerText"`, `"href"`). If this is omitted, the executor will return the WebElement object itself.
*   `event` (str, optional): An action to perform on the element (e.g., `"click()"`, `"clear()"`, `"type(Hello)"`). Multiple events can be chained with a semicolon: `"clear();type(Hello)"`.
*   `if_list` (str/int/list, optional): A filter to apply if the locator finds multiple elements.
    *   `"first"`: Return only the first element.
    *   `"last"`: Return only the last element.
    *   `"all"`: Return all elements in a list.
    *   `int`: Return the element at a specific index (e.g., `2` for the third element).
    *   `list`: Return elements at the specified indices (e.g., `[0, 2, 4]`).
*   `mandatory` (bool): If `True`, the script will log an error if the element cannot be found. If `False`, it will fail silently.
*   `timeout` (int): The number of seconds to wait for the element to appear on the page before giving up.
*   `timeout_for_event` (str): The specific condition to wait for (e.g., `"presence_of_element_located"`, `"element_to_be_clickable"`).
*   `locator_description` (str): A human-readable name for the locator, used in logging to make debugging easier.

## Strategies for Creating Robust Locators

1.  **Prefer Unique and Static IDs**: Always use the `id` attribute when it is available and unique. It's the most resilient to page structure changes.

2.  **Use Data Attributes**: Look for custom data attributes like `data-testid` or `data-cy`. Developers often add these for testing, and they are more stable than CSS classes or structure.
    *   *Example (XPath)*: `"//button[@data-testid='submit-form']"`

3.  **Be Specific, But Not *Too* Specific**: A very long and detailed XPath, like `//div/div[2]/div/div[1]/div/div/div/div[2]/div/a`, is extremely brittle. A small change to the page layout will break it. Instead, try to find a closer, more stable parent element and locate the target relative to it.
    *   *Brittle*: `//div/div[2]/div/div[1]/div/div/div/div[2]/div/a`
    *   *Better*: `//div[@id='product-details']//a[@class='add-to-cart-button']`

4.  **Use Text Content**: You can find elements based on the text they contain. This is useful for buttons and links.
    *   *Example (XPath)*: `//button[contains(text(), 'Add to Cart')]`

5.  **Combine Strategies with XPath**: XPath allows for complex logic.
    *   Find an input field that is either a text or password field: `//input[@type='text' or @type='password']`
    *   Find a label and then get the input field associated with it: `//label[text()='Username']/following-sibling::input`

## Complete Locator Examples

**1. Clicking a Login Button**

```python
login_button_locator = {
    "by": "ID",
    "selector": "login-submit-button",
    "event": "click()",
    "mandatory": True,
    "timeout": 10,
    "timeout_for_event": "element_to_be_clickable",
    "locator_description": "Login Submit Button"
}
```

**2. Typing into a Search Bar**

```python
search_bar_locator = {
    "by": "XPATH",
    "selector": "//input[@aria-label='Search']",
    "event": "type(Automated Web Scraping)",
    "mandatory": True,
    "locator_description": "Main Search Input"
}
```

**3. Extracting All Product Titles from a Page**

```python
product_titles_locator = {
    "by": "CSS_SELECTOR",
    "selector": ".product-list .product-title",
    "attribute": "innerText",
    "if_list": "all",
    "mandatory": False,
    "locator_description": "List of Product Titles"
}
```
