import asyncio
from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import Optional

from pydoll.browser.chrome import Chrome
from pydoll.constants import By


@dataclass
class Pydoll:
    """
    A dataclass wrapper for automating browser interaction using Pydoll.
    """
    url: str
    browser: Optional[Chrome] = field(default=None, init=False)
    page: Optional[object] = field(default=None, init=False)

    async def __aenter__(self):
        """Enter async context: start browser and open page."""
        self.browser = Chrome()
        await self.browser.__aenter__()
        await self.browser.start()
        self.page = await self.browser.get_page()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context: close browser."""
        if self.browser:
            await self.browser.__aexit__(exc_type, exc_val, exc_tb)

    async def get_url(self, url: str) -> None:
        """Navigate to the provided URL."""
        await self.page.go_to(url)

    async def click_star_button(self) -> None:
        """Click the GitHub 'Star' button if it exists."""
        star_button = await self.page.wait_element(
            By.XPATH,
            '//form[@action="/autoscrape-labs/pydoll/star"]//button',
            timeout=5,
            raise_exc=False
        )
        if not star_button:
            print("Ops! The button was not found.")
            return
        await star_button.click()
        await asyncio.sleep(3)

    async def execute_locator(self, locator: SimpleNamespace):
        """Locate and return content from the element based on locator info."""
        _webelement = await self.page.find_element(By[locator.by.upper()], locator.selector)

        if locator.attribute.lower() == 'innertext':
            return await _webelement.get_element_text()
        elif locator.attribute.lower() == 'innerhtml':
            return await _webelement.inner_html
        # Можно добавить return None или raise, если атрибут неизвестен

    async def run(self) -> None:
        """Main runner that executes all browser automation steps."""
        await self.get_url(self.url)
        await self.click_star_button()


async def run_pydoll(url: str) -> None:
    """
    Run the Pydoll automation for the given URL.
    :param url: The URL to navigate to.
    """
    async with Pydoll(url) as pydoll:
        await pydoll.run()


if __name__ == '__main__':
    asyncio.run(run_pydoll("https://github.com/autoscrape-labs/pydoll"))
