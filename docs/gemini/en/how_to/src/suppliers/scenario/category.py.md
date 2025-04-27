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
The `Category` class provides methods for crawling and processing product categories, particularly relevant for PrestaShop. It inherits from `PrestaCategoryAsync`, leveraging asynchronous programming for efficient data retrieval.

Execution Steps
-------------------------
1. **Initialization**: The `__init__` method initializes a `Category` object, accepting API credentials for accessing category data.
2. **Asynchronous Category Crawling**: The `crawl_categories_async` method asynchronously crawls categories from a given URL, recursively exploring child categories up to a specified depth. It uses a Selenium WebDriver to navigate web pages and extracts category links based on a provided XPath locator. The method checks for duplicate URLs to avoid redundant crawling.
3. **Synchronous Category Crawling**: The `crawl_categories` method implements the same crawling logic as `crawl_categories_async` but synchronously. It iterates through category links, checks for duplicates, and recursively calls itself for each child category. 
4. **Duplicate URL Check**: The `_is_duplicate_url` method checks if a URL already exists in the category dictionary.
5. **Missing Key Comparison**: The `compare_and_print_missing_keys` function compares a current dictionary with data from a JSON file and prints missing keys.

Usage Example
-------------------------

```python
from src.suppliers.scenario.category import Category
from src.webdirver import Driver, Chrome

# Initialize a Category object with API credentials
api_credentials = {'username': 'your_username', 'password': 'your_password'}
category = Category(api_credentials)

# Set up the WebDriver
driver = Driver(Chrome)
driver.set_default_timeout(5)

# Crawl categories from the specified URL
category_data = category.crawl_categories_async('https://www.example.com/categories', depth=2, driver=driver, locator={'by': 'XPATH', 'selector': '//a[@class="category-link"]'}, dump_file='category_data.json', default_category_id=1)
print(category_data)

# Compare the crawled data with data from a file
compare_and_print_missing_keys(category_data, 'category_data.json')
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".