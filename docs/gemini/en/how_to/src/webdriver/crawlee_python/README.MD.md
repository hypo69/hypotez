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
This code block defines a Python module named `src.webdriver.crawlee_python`, which provides a custom implementation of `PlaywrightCrawler` using the Crawlee library. It allows you to configure browser launch parameters, process web pages, and extract data from them. The configuration is managed via the `crawlee_python.json` file.

Execution Steps
-------------------------
1. **Import Necessary Modules**: Import the required modules, including `CrawleePython` from the `src.webdriver.crawlee_python` module.
2. **Initialize CrawleePython**: Create an instance of the `CrawleePython` class, passing in optional configuration parameters like `max_requests`, `headless`, `browser_type`, and `options`.
3. **Run the Crawler**: Use the `crawler.run()` method to start the crawling process. You can specify the target URLs as an argument to this method.
4. **Process and Extract Data**: Within the `CrawleePython` instance, the code will use the Crawlee library to process web pages, extract data, and handle browser interactions based on the provided configuration.

Usage Example
-------------------------

```python
from src.webdriver.crawlee_python import CrawleePython
import asyncio

# Initialize CrawleePython with custom options
async def main():
    crawler = CrawleePython(max_requests=10, headless=True, browser_type='chromium', options=["--headless"])
    await crawler.run(['https://www.example.com'])

asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".