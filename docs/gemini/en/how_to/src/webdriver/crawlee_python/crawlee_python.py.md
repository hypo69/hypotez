**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the CrawleePython Class
=========================================================================================

Description
-------------------------
The `CrawleePython` class is a custom implementation of the `PlaywrightCrawler` class from the Crawlee library. It allows you to easily crawl web pages and extract data using a browser (Chrome, Firefox, or Webkit) and the Playwright library.

Execution Steps
-------------------------
1. **Initialize CrawleePython**:
   - Create an instance of `CrawleePython` with options like `max_requests`, `headless`, and `browser_type`. 
   - The `options` argument allows you to pass custom browser arguments for the selected browser.
2. **Set up the Crawler**:
   - Call the `setup_crawler` method to initialize the `PlaywrightCrawler` instance with the configured settings.
   - This method also sets up the `request_handler` which defines actions to be taken for each web page visited during the crawl.
3. **Run the Crawler**:
   - Call the `run_crawler` method with a list of initial URLs to start the crawling process.
   - The `request_handler` will handle each URL, extract data, and enqueue any additional links found on the page.
4. **Export Data**:
   - After crawling, call the `export_data` method to save the extracted data to a JSON file.
   - The default location for the exported file is `gs.path.tmp / 'results.json'`.
5. **Get Data**:
   - Optionally, you can call the `get_data` method to retrieve the extracted data as a dictionary.
6. **Main Method**:
   - The `run` method combines all the steps above: setup, run, export data, and retrieve data. 

Usage Example
-------------------------

```python
    async def main():
        crawler = CrawleePython(max_requests=5, headless=False, browser_type='firefox', options=["--headless"])
        await crawler.run(['https://www.example.com'])

    asyncio.run(main())
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".