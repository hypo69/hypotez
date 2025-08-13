import asyncio
from header import __root__
from src.webdriver.pydoll.tab import Tab
from src.webdriver.pydoll.options import Options
from src.webdriver.pydoll.browser import Browser

from src.logger import logger

if __name__ == "__main__":
    import asyncio

    async def main():
        """Example of launching the Browser and using it with a locator."""
        # Create a browser instance (default: headless mode from Options config)

        # Use it as an async context manager
        async with Browser() as br:
            tab = await br.start()
            if not tab:
                logger.error("Failed to start the browser")
                return

            # Open a page
            await tab.goto("https://quotes.toscrape.com")

            # Execute a locator (example: take page title text)
            title_locator = {
                "attribute": "innerText",
                "by": "XPATH",
                "selector": "//h1"
            }
            try:
                result = await tab.execute_locator(title_locator)
                print("Page title:", result)
            except Exception as ex:
                logger.error("Error executing locator", ex, exc_info=True)

    asyncio.run(main())

