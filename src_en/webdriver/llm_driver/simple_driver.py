# # \file src/webdriver/llm_driver/simple_browser.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""Module for launching tasks using LLM through Langchain and standard agents.
==================================================================================================
(Uses tools interacting with BrowserController and/or search API)

Provides functionality for:
- Configuration of models (Gemini, Openai).
- Installations of the API keys.
- starting the task using LLM and available tools (web-road, browser).
- completing the task to the final result (`run_task`).
- Streaming of the task (`stream_task`).

Dependencies:
    -Langchain-Openai, Langchain-Google-Genai, Langchain-Core, Langchainhub, Langchain
    - Langchain-comunity (for serpapiwrapper)
    -Google-Search-Results (for Serpapiwrapper)
    - Python-Dotenv
    - Browser_use (or your module with BrowserController)
    - SRC.GS, SRC.Logger, SRC.utils, Header

`` `RST
.. Module :: SRC.webdriver.llm_driver.simple_browser
`` `"""

# Standard libraries
import os
import sys
import io
import asyncio
import time
from types import SimpleNamespace
from typing import List, Dict, Any, Optional, Callable, Type, Tuple, AsyncIterator
from pathlib import Path

# Langchain components
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.exceptions import LangChainException
from langchain import hub
# --- a tool for searching through API ---
# Make sure that installed: PIP Install Google-Earch-RESULTS
from langchain_community.utilities import SerpAPIWrapper
# Import of an agent from the local module Browser_use
from browser_use import Agent # type: ignore # assumed that Agent has a specific interface

# --- internal modules ---
import header
from header import __root__
from src import gs
# from src.webdriver.ai_browser import tools
# from src.webdriver.ai_browser.tools import get_tools, get_tools_by_type, get_tools_by_name
# Import Config, Driver and Stream_agent_EXECUTION from a higher module
from src.webdriver.llm_driver.use_llm import Config as BaseDriverConfig, Driver, stream_agent_execution

from src.logger import logger
from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.printer import pprint as print

# Downloading variables of the environment from .env file
from dotenv import load_dotenv
load_dotenv()

class Config:
    """Configuration class for Simpledriver.
    Determines the base point for related files."""
    # Determining the path to the directory for files associated with this module (Sandbox/Davidka)
    ENDPOINT:Path = Path(__root__/'SANDBOX'/'davidka')
    GEMINI_API_KEY:str = None, 
    OPENAI_API_KEY:str = None, 
    OPENAI_MODEL_NAME:str = None, 
    GEMINI_MODEL_NAME:str = None, 

class SimpleDriver(Driver):
    """Simplified driver in order from the main class of Driver.
    Designed to perform specific tasks using LLM and agent `Browser_use.agent`."""
    def __init__(self,
                 openai_api_key:str = None,
                 gemini_api_key:str = None, 
                 openai_model_name:str = None, 
                 gemini_model_name:str = None, 
                 start_browser:bool = True, # The type of bool is changed to comply with the parental class
                **kwargs: Any) -> None:
        """The Simpledriver copy initializes.

        Args:
            Gemini_api_key (Optional [str]): API key for gemini. By default `none`.
            Openai_api_key (Optional [str]): API key for Openai. By default `none`.
            Opena_Model_name (Optional [Str]): name of the Openai model. By default `none`.
            gemini_model_name (Optional [str]): name of the model Gemini. By default `none`.
            Start_browser (Bool): A flag indicating whether the browser needs to be launched. By default `true`.
            ** KWARGS (ANY): additional named arguments transmitted to the parent designer."""
        # Calling the DRIVER parent -class designer
        super().__init__(
            
            openai_api_key=openai_api_key,
            gemini_api_key=gemini_api_key,
            openai_model_name=openai_model_name,
            gemini_model_name=gemini_model_name,
            start_browser=start_browser,
            **kwargs
        ) 

    async def simple_process_task_async(self, task:str = 'Hello, world!') -> Any:
        """Asynchronically processes the task using the `Browser_use.agent` agent.
        The function extracts and cleanses JSON-like data from the results of the agent.

        Args:
            TASK (STR): The text of the task for the agent. By default 'HELLO, World!'

        Returns:
            ANY: a dictionary with aggregated data extraction results or an empty line in the case of a critical error.
                 The type of return of the value depends on the contents of `result_dict`.
        
        Example:
            >>> Driver = simpledriver ()
            >>> # asyncio.ru (driver.async_init ()) # # is necessary to initial LLM in Driver if not done earlier
            >>> # Result = asyncio.ru (driver.simple_process_task_async ("Find information about Python"))
            >>> # Print (Result)
            # The expected result depends on the implementation of browser_use.agent and tasks"""
        # Initialization of the dictionary for storing results
        result_dict:dict = {}

        def clean_json(raw_text: str) -> str:
            """The function cleans the line, trying to extract a valid JSON-fragment from it.
            1. Removes everything to the first opening figure bracket `{`.
            2. Removes the framing symbols of `` `, transfers of lines and spaces.

            Args:
                RAW_TEXT (STR): The initial line with a potential JSON.

            Returns:
                STR: A cleaned line ready for parsing as a JSON, or the original line, if the cleaning has failed."""
            json_start_index: int = -1 # Initialization of the JSON index
            # 1. Trying to find the first opening figure bracket
            try:
                json_start_index = raw_text.index('{')
            except ValueError: # Valuerror occurs if the symbol is not found
                logger.warning(f"Первая фигурная скобка '{{' не найдена в тексте: '{raw_text[:100]}...'")
                return raw_text # If the bracket is not found, the source text is returned
            
            # Extracting the text starting with the first curly bracket
            json_cleaned: str = raw_text[json_start_index:]
    
            # 2. Removing the framing triple quotes (Markdown Code Block) and excessive test characters
            json_cleaned = json_cleaned.strip('`\n ')
            
            return json_cleaned

        try:
            # Initialization Agent `browser_use.agent`
            # The transfer of the problem and the initialized LLM model (preferably Gemini)
            agent = Agent(
                task=task,
                llm=self.gemini, # Self.Gemini is used, which should be initialized in Driver
            )
            logger.info(f"Агент начинает выполнение задачи: \"{task}\"")
            # Asynchronous launch of the task by agent
            answer: Any = await agent.run() # The type `ANSWER` depends on the implementation` agent.ru () `

            # Check if the result is returned from the agent
            if not answer:
                logger.error('Не вернулся результат действий агента. Попытка перезапуска задачи через 5 минут.')
                # Waiting for a second attempt
                await asyncio.sleep(300) # Asyncio.sleep is used for asynchronous delay
                # Recursive call for re -processing the problem
                return await self.simple_process_task_async(task)

            # Obtaining a current temporary mark (used for logging or naming files, if necessary)
            # TimeStamp: str = GS.now # is made, since it is not used later

            # Processing the history of agent actions to extract results
            if hasattr(answer, 'history') and isinstance(answer.history, list):
                for action_result_item in answer.history:
                    # It is assumed that `Action_Result` contains an attribute` result` (list)
                    result_list: Optional[list] = getattr(action_result_item, 'result', None)
                    if not result_list or not isinstance(result_list, list) or not result_list:
                        continue # Pass, if there is no result, not a list or empty

                    # It is assumed that the first element of the `Result` list is the object` ActionResult`
                    # and contains the attribute `extexted_content`
                    result_obj: Any = result_list[0] # Type `ActionResult` is not defined, ANY is used
                    extracted_content: Optional[str] =	getattr(result_obj, 'extracted_content', None)

                    if not extracted_content or not isinstance(extracted_content, str):
                        continue # Pass if the extracted content is absent or not a string

                    # Cleaning extracted content to obtain a JSON-like line
                    cleaned_json_text: str = clean_json(extracted_content)
                    try:
                        # Parsing attempt to purified line like json
                        data: Optional[Dict[str, Any]] = j_loads(cleaned_json_text)
                        # If Parsing failed or returned an empty result, but the line is not empty,
                        # then the initial peeled string is stored in the key 'Data'
                        if not data and cleaned_json_text: 
                            data = {'data': cleaned_json_text}
                        
                        if not data: 
                            continue # Pass if there is no data
                    except Exception as ex_json: # A more general exception for J_loads
                        logger.error(f"Ошибка разбора JSON из текста: '{cleaned_json_text[:100]}...'", ex_json, exc_info=True)
                        # If Json is not steamed, you can save the purified text
                        data = {'raw_cleaned_text': cleaned_json_text}
                        # Continue # Continuing solution depends on the requirements

                    # Updating the general dictionary of results from the current step
                    if isinstance(data, dict): # Check that Data is a dictionary
                        result_dict.update(data)
            else:
                logger.warning("Атрибут 'history' отсутствует или не является списком в ответе агента.")

            logger.info("Агент завершил выполнение задачи.")
            ...
            return result_dict # Return of aggregated results
        except Exception as agent_err:
            # Logging a critical error during the agent's work
            logger.error(f"\n\n !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\nПроизошла ошибка во время инициализации или выполнения задачи агентом.\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n", agent_err, exc_info=True)
            ...
            return '' # Return of an empty line in the event of an agent’s critical error


def main() -> None:
    """The main function for demonstrating the launch of the `simpledriver 'agent and the task.
    The function initializes `simpledriver`, determines the task and triggers its asynchronous processing."""
    # An example of using Simpledriver
    # Initialization of the driver indicating the Gemini model
    # It is assumed that the API Gemini key will be picked up from config or environment variables
    driver = SimpleDriver(gemini_model_name='gemini-2.5-flash') # Updated the name of the model
                                                        # Determining the problem from the instructions file
    # Formation of the path to the file with instructions
    instruction_file_path: Path = __root__ / 'src' / 'webdriver' / 'ai_browser' / 'instructions' / 'get_supplier_categories.md'
    task_text: str
    # Reading the text of the file from the file
    if instruction_file_path.exists():
        task_text = instruction_file_path.read_text(encoding='utf-8')
    else:
        logger.error(f"Файл с инструкциями не найден: {instruction_file_path}")
        task_text = "Найди основные категории товаров на сайте example.com" # Default task

    # Launch of asynchronous processing of the problem
    # Asyncio.ru is used to perform asynchronous function from synchronous context
    # First, it is necessary to initialize the parental Driver if he uses async_init
    async def run_driver_task():
        # Asynchronous initialization of the parent driver (LLM, tools, etc.)
        # This is important since Simpledriver is inherited from Driver, which can demand async_init
        if not driver._initialized: # Checking the flag of initialization
             await driver.async_init()
        # Fulfillment of the main task
        return await driver.simple_process_task_async(task_text)

    result: Any = asyncio.run(run_driver_task())
    
    # Output of the result of the task
    print(f"Результат выполнения задачи: {result}")

if __name__ == "__main__":
    # Calling the main function when starting the script
    main()
