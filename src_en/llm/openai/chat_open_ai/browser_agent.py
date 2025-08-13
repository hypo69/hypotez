# # \file /src/ai/openai/chat_openai/browser_agent.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""Module: src.ai.openai.chat_openai.browser_agent 
	: Platform: Windows, Unix
	: synopsis: quickly configure and launch the AI-agent that can look for information on Google and analyze web pages.

    Article: https://github.com/hypo69/1001-pethon-ru/tree/master/articles/lang_chain_and_browser_use"""

from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
from typing import Optional, List, Union
import urllib.parse

import header
from src import gs
from src.logger import logger


# None

ENDPOINT = 'openai.browser_agent'
from src import USE_ENV
MODE: str = 'PRODUCTION'  # <- defines the developer regime. If Mode == 'Production' will be launched by Kazarionaov Bot, otherwise a testboat
MODE: str = 'DEV'
# None

if USE_ENV:
    load_dotenv()


class AIBrowserAgent:
    """A class for creating an agent using a browser to complete tasks."""

    def __init__(self,
                 api_key: str,
                 model_name: str = "gpt-4o-mini",
                 search_engine: str = "google",
                 custom_driver: Optional[object] = None):  # Type hint: object
        """Initializes the class Browsraagent.

        Args:
            API_KEY: Key API Openai (optional). If not specified, the key from the environment variables will be used.
            Model_name: the name of the Openai language model for use (by default "GPT-4O-Mini").
            Search_engine: search engine for use (by default "Google").
            Custom_DRIVER: Optionally Injected WebDriver Instance, Defaults to None (Browser_use Default)."""
        self.api_key = api_key
        self.model_name = model_name
        self.search_engine = search_engine
        self.llm = ChatOpenAI(model=self.model_name, api_key=self.api_key)  # Initialize LLM here
        self.custom_driver = custom_driver  # Save injected driver to local variable

    async def run_task(self, task_prompt: str) -> Optional[str]:
        """It launches an agent to complete a given task.

        Args:
            TASK_PROMPT: The text of the task for the agent.

        Returns:
            The result of the task in the form of a line, or None in case of an error."""
        try:
            logger.info(f"Агент начал выполнение задачи: {task_prompt}")

            # 1. Default:  browser_use managed Playwright driver (no driver needed)
            driver = None  # By default let browser_use create its own driver.

            # 2. CUSTOM:  Adapt Selenium-based driver
            # if self.custom_driver:  # if injected instance of webdriver.FireFox
            # playwright_driver = PlaywrightFirefoxAdapter(self.custom_driver)  # Adapt.
            # driver = playwright_driver

            # 3. Playwright driver already adapted (or pure Playwright)
            if self.custom_driver:
                driver = self.custom_driver

            agent = Agent(task=task_prompt, llm=self.llm, driver=driver)  # Pass to agent
            result = await agent.run()
            logger.info("Агент завершил выполнение задачи.")

            if hasattr(driver, 'close') and callable(getattr(driver, 'close')):
                driver.close()  # Try closing driver, if implemented

            return result

        except Exception as ex:
            logger.error(f"Произошла ошибка во время выполнения задачи: ", ex, exc_info=True)
            return None

    async def find_product_alternatives(self, product_url: Optional[str] = None,
                                        sku: Optional[str] = None) -> Optional[str]:
        """Looking for analogues for goods on a given URL or SKU on the network.

        Args:
            Product_URL: URL of the product for which analogues need to be found (optionally).
            SKU: SKU of goods for which analogues need to be found (optionally).

        Returns:
            A line with a description of the found analogues, or None in case of an error."""

        if product_url:
            search_query = f"аналоги {product_url}"
        elif sku:
            search_query = f"аналоги товара с артикулом {sku}"
        else:
            logger.warning("Не указан ни product_url, ни sku.  Невозможно выполнить поиск аналогов.")
            return None

        encoded_search_query = urllib.parse.quote_plus(search_query)  # URL encode search query

        if self.search_engine == "google":
            search_url = f"https://www.google.com/search?q={encoded_search_query}"
        else:  # DuckDuckGo
            search_url = f"https://duckduckgo.com/?q={encoded_search_query}"

        task_prompt = f"""Using the search system {self.search_engine}, go to the address {search_url}.  
        Find and provide a list of 3-5 goods analogues.  
        For each analogue, indicate the name and brief description."""

        return await self.run_task(task_prompt)

    def ask(self, q: str) -> Optional[str]:
        """Synchronous wrapper for the asynchronous method ask_async.  Not recommended for use."""
        task_prompt = f"""Answer the next question using a search on the Internet, if necessary: {q}"""
        return self.run_task(task_prompt)

    async def ask_async(self, q: str) -> Optional[str]:
        """He answers the question asked using a search on the Internet, if necessary.

        Args:
            Question: The question that needs to be answered.

        Returns:
            The answer to the question in the form of a line, or None in case of an error."""
        task_prompt = f"""Answer the next question using a search on the Internet, if necessary: {q}"""
        return await self.run_task(task_prompt)


async def main():
    """An example of using the BROWSERAGENT class."""
    # api_key: str = gs.credentials.openai.hypotez.api_key  # Replace with your actual method of obtaining the API key
    api_key: str = None  # Replace with your actual method of obtaining the API key
    model_name: str = 'gpt-4o-mini'  # GPT-4O-Mini exists if the API_KEY is specified

    # None
    # OPTIONAL:  Inject custom Chrome, Firefox, Edge driver
    # selenium_driver = Firefox()  # (Or with args you use in Firefox class)
    # playwright_driver = PlaywrightFirefoxAdapter(selenium_driver)
    # agent = BrowserAgent(api_key=api_key, model_name=model_name, custom_driver = playwright_driver)
    # None
    agent = AIBrowserAgent(api_key=api_key, model_name=model_name) # Default browser_use driver

    # An example of finding analogues of goods
    sku: str = '1493001'
    product_url: str = None  # "https://www.apple.com/iphone-14/" # Replace with the URL of the goods you are interested in
    alternatives = await agent.find_product_alternatives(product_url=product_url, sku=sku)
    if alternatives:
        print("Найденные аналоги:")
        print(alternatives)
    else:
        print("Не удалось найти аналоги.")

    # An example of an answer to a question
    question = "Какая сейчас погода в Москве?"
    answer = await agent.ask_async(question)  # The asynchronous method is used directly
    if answer:
        print("Ответ на вопрос:")
        print(answer)
    else:
        print("Не удалось получить ответ на вопрос.")


if __name__ == "__main__":
    asyncio.run(main())