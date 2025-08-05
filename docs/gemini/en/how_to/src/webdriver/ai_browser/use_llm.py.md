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
[Explanation of what the code does.]

Execution Steps
-------------------------
1. [Description of the first step.]
2. [Description of the second step.]
3. [Continue as needed...]

Usage Example
-------------------------

```python
    [Code usage example]
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".
```

## \file src/webdriver/ai_browser/use_ai.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Module for running tasks using LLM through LangChain and standard agents.
==================================================================================
(Uses tools that interact with BrowserController and/or search API)

Provides functionality for:
- Configuring models (Gemini, OpenAI).
- Setting API keys.
- Running a task using LLM and available tools (web search, browser).
- Executing a task to completion (`run_task`).
- Streaming task execution (`stream_task`).

Dependencies:
    - langchain-openai, langchain-google-genai, langchain-core, langchainhub, langchain
    - langchain-community (for SerpAPIWrapper)
    - google-search-results (for SerpAPIWrapper)
    - python-dotenv
    - browser_use (or your module with BrowserController)
    - src.gs, src.logger, src.utils, header

.. module:: src.webdriver.ai_browser.use_ai
"""

import os
import asyncio
from types import SimpleNamespace
from typing import List, Dict, Any, Optional, Callable, Type, Tuple, AsyncIterator
from pathlib import Path
import logging # Стандартный logging

# LangChain components
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.exceptions import LangChainException
from langchain import hub
# --- Tool for searching via API ---
# Make sure it's installed: pip install google-search-results
from langchain_community.utilities import SerpAPIWrapper
from browser_use import Agent

# --- Internal modules ---
import header
from header import __root__
from src import gs
from src.logger import logger
from src.utils.jjson import j_loads, j_loads_ns
from src.utils.printer import pprint as print

try:
    from .controlers import BrowserController # Example
    BROWSER_CONTROLLER_AVAILABLE = True
except ImportError as ex:
    logger.warning("Failed to import BrowserController. Browser tools will be unavailable.", ex, exc_info=False)
    class BrowserController: # Stub
        def __init__(self,*args,**kwargs): pass
        def search(self,q): return "Error: Browser controller is unavailable."
        def navigate(self,u): return "Error: Browser controller is unavailable."
        def scrape_text(self,s=None): return "Error: Browser controller is unavailable."
        def click_element(self,s): return "Error: Browser controller is unavailable."
        def close(self): pass
    BROWSER_CONTROLLER_AVAILABLE = False


from dotenv import load_dotenv
load_dotenv()

class Config:
    """ Class for storing static application configuration. """
    ENDPOINT: Path = __root__ / 'src' / 'webdriver' / 'ai_browser'
    # Config loading when the class is defined
    config: SimpleNamespace = j_loads_ns(ENDPOINT/ 'use_llm.json') # May raise an error if the file is not found/incorrect
    # Class attributes with default values
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_STATUS: str = 'inactive'
    GEMINI_MODEL_NAME: str = ''
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_API_STATUS: str = 'inactive'
    OPENAI_MODEL_NAME: str = ''

    if config: 
        try:

            os.environ['GEMINI_API_KEY']  = GEMINI_API_KEY = gs.credentials.gemini.kazarinov.api_key
            os.environ['OPENAI_API_KEY']  = OPENAI_API_KEY = gs.credentials.openai.hypotez.api_key
            os.environ['SERPAPI_API_KEY'] =  gs.credentials.serpapi.onela.api_key 

            GEMINI_STATUS = config.models.gemini.status
            GEMINI_MODEL_NAME = config.models.gemini.model_name

            OPENAI_API_STATUS = config.models.openai.status
            OPENAI_MODEL_NAME = config.models.openai.model_name

            logger.info(f"Config Gemini: Status={GEMINI_STATUS}, Model={GEMINI_MODEL_NAME}, Key Present={bool(GEMINI_API_KEY)}")
            logger.info(f"Config OpenAI: Status={OPENAI_API_STATUS}, Model={OPENAI_MODEL_NAME}, Key Present={bool(OPENAI_API_KEY)}")

        except Exception as ex:
            logger.error("Unexpected error initializing Config.", ex, exc_info=True)
            ...
            # Class attributes will remain with default values
    else:
        # This branch will execute if j_loads_ns returned a Falsy value
        logger.error("Configuration loading error: j_loads_ns returned an incorrect value.", None, exc_info=False)
        ...
        raise ValueError("Failed to load configuration from use_ai.json")

# ===============================================================
# Streaming function 
# ===============================================================
async def stream_agent_execution(executor: AgentExecutor, task_input: Dict[str, Any], logger_instance) -> Tuple[Optional[str], List[Dict[str, Any]]]:
    """ Asynchronously executes the agent through AgentExecutor and streams steps. """
    final_answer: Optional[str] = None; all_chunks: List[Dict[str, Any]] = []; run_id: Optional[str] = None
    logger_instance.info(f"--- Starting streaming for input: {task_input} ---")
    try:
        async for chunk in executor.astream(task_input):
            all_chunks.append(chunk)
            current_run_info = chunk.get("__run", {}); current_run_id = getattr(current_run_info, 'id', None)
            if current_run_id and current_run_id != run_id: run_id = current_run_id; logger_instance.debug(f"Agent Run ID: {run_id}", exc_info=False)
            if actions := chunk.get("actions"):
                for action in actions:
                    tool=getattr(action, 'tool', 'N/A'); tool_input=getattr(action, 'tool_input', 'N/A'); log_msg=getattr(action, 'log', '').strip()
                    logger_instance.info(f"Planned action: Tool={tool}, Input={tool_input}")
                    if log_msg: logger_instance.debug(f"  Log (Thoughts): {log_msg}", exc_info=False)
            elif steps := chunk.get("steps"):
                for step in steps:
                    observation = getattr(step, 'observation', None)
                    if observation is not None: logger_instance.info(f"Action result (Observation): {str(observation)[:500]}...")
                    else: logger_instance.debug(f"Step received without observation: {step}", exc_info=False)
            elif output := chunk.get("output"): logger_instance.info(f"Final answer: {output}"); final_answer = output
            elif messages := chunk.get("messages"):
                for msg in messages:
                    if content := getattr(msg, 'content', None): logger_instance.debug(f"Message Chunk: {content}", exc_info=False)
    except LangChainException as e: logger_instance.error("LangChain error during streaming.", e, exc_info=True)
    except Exception as e: logger_instance.error("Unexpected error during streaming.", e, exc_info=True)
    logger_instance.info(f"--- Streaming completed ---"); return final_answer, all_chunks
# ===============================================================


class Driver:
    """
    Class for managing LLM and running LangChain agents with web tools.
    """
    config: Config = Config
    gemini: Optional[ChatGoogleGenerativeAI] = None
    openai: Optional[ChatOpenAI] = None
    tools: List[Tool] = [] # Initialize with an empty list
    browser: Optional[BrowserController] = None
    search_api: SerpAPIWrapper

    def __init__(self,
                 GEMINI_API_KEY: Optional[str] = None,
                 OPENAI_API_KEY: Optional[str] = None,
                 openai_model_name: Optional[str] = None,
                 gemini_model_name: Optional[str] = None,
                 start_browser: bool = True,
                 **kwargs):
        """
        Initializes LLM, browser controller and tools.
        """
        # Getting keys and models
        openai_api_key = OPENAI_API_KEY or Config.OPENAI_API_KEY
        gemini_api_key = GEMINI_API_KEY or Config.GEMINI_API_KEY
        openai_model_to_use = openai_model_name or Config.OPENAI_MODEL_NAME
        gemini_model_to_use = gemini_model_name or Config.GEMINI_MODEL_NAME

        # --- LLM Initialization ---
        if openai_api_key and Config.OPENAI_API_STATUS.lower() == 'active':
            logger.info(f"Initializing OpenAI: Model={openai_model_to_use}")
            os.environ['OPENAI_API_KEY'] = openai_api_key
            try: self.openai = ChatOpenAI(model_name=openai_model_to_use, openai_api_key=openai_api_key)
            except Exception as ex: logger.error("OpenAI initialization error.", ex, exc_info=True); self.openai = None
            if self.openai: logger.info("OpenAI LLM initialized.")
        else: logger.warning(f"OpenAI LLM not initialized (Key={bool(openai_api_key)}, Status={Config.OPENAI_API_STATUS})", exc_info=False); self.openai = None

        if gemini_api_key and Config.GEMINI_STATUS.lower() == 'active':
            logger.info(f"Initializing Gemini: Model={gemini_model_to_use}")
            os.environ['GOOGLE_API_KEY'] = gemini_api_key
            logger.debug("Environment variable GOOGLE_API_KEY set.", exc_info=False)
            try: self.gemini = ChatGoogleGenerativeAI(model=gemini_model_to_use, google_api_key=gemini_api_key)
            except Exception as ex: logger.error("Gemini initialization error.", ex, exc_info=True); self.gemini = None
            if self.gemini: logger.info("Gemini LLM initialized.")
        else: logger.warning(f"Gemini LLM not initialized (Key={bool(gemini_api_key)}, Status={Config.GEMINI_STATUS})", exc_info=False); self.gemini = None

        # --- Tool initialization ---
        self.tools = [] # Start with an empty list
        self.browser = None

        # 1. Attempt to add a search tool via API (SerpApi)
        #    Requires the SERPAPI_API_KEY environment variable to be set
        try:
            self.search_api = SerpAPIWrapper() # Will try to find the key in os.environ
            # Check if it was successfully initialized (may fail if the key is not found or is invalid)
            # Make a test request to ensure key functionality
            self.search_api.run("test") # Uncomment to check the key during initialization (may slow down)

            self.tools.append(Tool(
                name="WebSearchAPI",
                func=self.search_api.run,
                description="Reliable tool for finding up-to-date information on the internet (news, facts, weather, etc.) through API. Input - search query. Returns a brief summary of the results."
            ))
            logger.info("WebSearchAPI (SerpApi) tool added.")
        except Exception as ex:
             # Failed to initialize SerpApi (key not found, invalid, or other error)
             logger.warning(f"Failed to initialize WebSearchAPI (SerpApi) tool. API search is unavailable. Error: ",ex, exc_info=False)
             ...
            

        # 2. Attempt to initialize BrowserController and add browser tools
        if start_browser and BROWSER_CONTROLLER_AVAILABLE:
            try:
                logger.info("Attempting to initialize BrowserController...")
                self.browser = BrowserController() # YOUR INITIALIZATION
                logger.info("BrowserController successfully initialized.")

                # --- Add browser tools only if BrowserController is created ---
                self.tools.extend([ # Use extend to add multiple tools
                    Tool(
                        name="BrowserNavigate",
                        func=lambda url: self.browser.navigate(url),
                        description="Navigates the browser to the specified URL. Input - full URL."
                    ),
                    Tool(
                        name="BrowserScrapeText",
                        func=lambda selector=None: self.browser.scrape_text(selector),
                        description="Extracts text from the CURRENT browser page (optionally by CSS selector)."
                    ),
                    Tool(
                        name="BrowserClickElement",
                        func=lambda selector: self.browser.click_element(selector),
                        description="Clicks on an element on the CURRENT browser page (input - CSS selector)."
                    ),
                    # --- You can add browser search as an ALTERNATIVE to API ---
                    # Tool(
                    #     name="BrowserSearch",
                    #     func=lambda query: self.browser.search(query),
                    #     description="Performs a search on the internet through the browser window. Less reliable than WebSearchAPI. Input - search query."
                    # ),
                ])
                logger.info(f"Added {len(self.tools) - (1 if any(t.name == 'WebSearchAPI' for t in self.tools) else 0)} browser tools.") # Log the number of browser tools added
            except Exception as ex:
                logger.error("Error initializing BrowserController or adding browser tools.", ex, exc_info=True)
                self.browser = None # Reset the browser
                # Don't clear self.tools, as it may contain WebSearchAPI
        elif not BROWSER_CONTROLLER_AVAILABLE:
            logger.warning("BrowserController is unavailable, browser tools are not added.", exc_info=False)
        else: # start_browser is False
            logger.info("Browser initialization skipped. Browser tools are not added.")

        logger.info(f"Final tool list: {[tool.name for tool in self.tools]}") # Log the final list
        # Check for unused arguments
        if kwargs: logger.warning(f"Unused arguments when initializing Driver: {kwargs}", exc_info=False)

    def __del__(self):
        if self.browser:
            logger.info("Closing the browser when deleting the Driver object...")
            try: self.browser.close()
            except Exception as ex: logger.error("Error calling browser.close() in __del__.", ex, exc_info=True)


    # --- _get_agent_executor, run_task, stream_task methods (no changes) ---
    async def _get_agent_executor(self, llm: BaseChatModel) -> Optional[AgentExecutor]:
        if not llm: logger.error("LLM is not initialized.", None, exc_info=False); return None
        # Check for an empty list of tools is now more relevant
        if not self.tools:
             logger.error("The list of tools is empty! The agent will not be able to interact with the outside world.", None, exc_info=False)
             # Perhaps return None if tools are mandatory
             # return None
             logger.warning("Continuing to work without tools.", exc_info=False) # Or just warn

        try:
            prompt = hub.pull("hwchase17/react") # Standard ReAct prompt
            agent_runnable = create_react_agent(llm=llm, tools=self.tools, prompt=prompt)
            agent_executor = AgentExecutor(
                agent=agent_runnable,
                tools=self.tools, # Pass the current list of tools
                verbose=True,
                handle_parsing_errors=True
            )
            logger.info("AgentExecutor successfully created.")
            return agent_executor
        except Exception as ex:
            logger.error("Error creating AgentExecutor.", ex, exc_info=True)
            return None

    async def run_task(self, task: str, use_gemini: bool = True) -> Optional[str]:
        model_name = 'Gemini' if use_gemini else 'OpenAI'; logger.info(f"Running run_task ({model_name}): '{task[:100]}...'")
        selected_llm = self.gemini if use_gemini else self.openai
        if not selected_llm: logger.error(f"LLM ({model_name}) is not initialized.", None, exc_info=False); return None

        # Simple warning if there are no tools at all
        if not self.tools:
             logger.warning(f"Attempting to execute task '{task[:50]}...' WITHOUT ANY tools!", exc_info=False)

        agent_executor = await self._get_agent_executor(selected_llm)
        if not agent_executor: logger.error(f"Failed to create AgentExecutor for {model_name}.", None, exc_info=False); return None
        try:
            result_data = await agent_executor.ainvoke({"input": task})
            final_answer = result_data.get('output')
            logger.info(f"Agent ({model_name}) completed run_task.");
            if final_answer is not None: logger.info(f"Result: {final_answer}")
            else: logger.warning(f"Final answer is missing ({model_name}).", exc_info=False)
            return final_answer
        except LangChainException as e: logger.error(f"LangChain error ({model_name}).", e, exc_info=True); return None
        except Exception as ex: logger.error(f"Unexpected error ({model_name}).", ex, exc_info=True); return None

    async def stream_task(self, task: str, use_gemini: bool = True) -> Tuple[Optional[str], List[Dict[str, Any]]]:
        model_name = 'Gemini' if use_gemini else 'OpenAI'; logger.info(f"Running stream_task ({model_name}): '{task[:100]}...'")
        selected_llm = self.gemini if use_gemini else self.openai
        if not selected_llm: logger.error(f"LLM ({model_name}) is not initialized.", None, exc_info=False); return None, []
        if not self.tools: logger.warning(f"Attempting to stream task '{task[:50]}...' WITHOUT ANY tools!", exc_info=False)
        agent_executor = await self._get_agent_executor(selected_llm)
        if not agent_executor: logger.error(f"Failed to create AgentExecutor for {model_name}.", None, exc_info=False); return None, []
        final_answer, all_chunks = await stream_agent_execution(executor=agent_executor, task_input={"input": task}, logger_instance=logger)
        return final_answer, all_chunks

# --- main function for demonstration ---
async def main():

    driver:Driver = None
    try:
        # Initialize Driver, which will try to create tools
        driver = Driver(start_browser=True) # Set to False if the browser is not needed
    except Exception as ex:
        logger.error("Critical error initializing Driver.", ex, exc_info=True); return
    if not driver: logger.error("Driver object was not created.", None, exc_info=False); return
    logger.info("Driver initialized.")

    # Check which tools are actually available
    if not driver.tools:
        logger.warning("Tools are NOT available. Testing is limited to tasks without external access.", exc_info=False)
        task_to_run = "Write a short poem about programming." # Task without tools
    else:
        logger.info(f"Available tools: {[tool.name for tool in driver.tools]}")
        # Task that most likely requires search (WebSearchAPI or BrowserSearch)
        task_to_run = "What is the capital of Australia and what is the weather there now?"
        # Or a task for the browser, if it is available
        # task_to_run = "Find 'LangChain python quickstart', go to the page and extract the first code example."

    print(f"\nTest task: {task_to_run}")

    # --- Test run_task ---
    print("\n" + "="*10 + " Test run_task " + "="*10)
    llm_to_test_run = []
    if driver.gemini: llm_to_test_run.append(("Gemini", True))
    if driver.openai: llm_to_test_run.append(("OpenAI", False)) # You can add OpenAI if it's configured
    if not llm_to_test_run: print("No active LLMs to run run_task.")
    else:
        for name, flag in llm_to_test_run:
            print(f"\n--- Running run_task ({name}) ---")
            result = await driver.run_task(task_to_run, use_gemini=flag)
            print(f"[Result run_task ({name})]: {result if result is not None else 'Error or no response'}")

    # --- Test stream_task ---
    print("\n" + "="*10 + " Test stream_task " + "="*10)
    # Let's run streaming only for Gemini for brevity of the example
    llm_to_test_stream = [("Gemini", True)] if driver.gemini else []
    if not llm_to_test_stream: print("No active LLMs to run stream_task.")
    else:
        for name, flag in llm_to_test_stream:
            print(f"\n--- Running stream_task ({name}) ---")
            final_answer, chunks = await driver.stream_task(task_to_run, use_gemini=flag)
            print(f"\nStreaming ({name}) completed. Chunks: {len(chunks)}")
            print(f"[Final answer ({name})]: {final_answer if final_answer is not None else 'No response or error'}")

    logger.info("="*20 + " Completing main " + "="*20)


if __name__ == "__main__":
    # Make sure the SERPAPI_API_KEY is set in .env or environment variables,
    # if you want to use WebSearchAPI.
    asyncio.run(main())
```

**How to Use the Driver Class**
=========================================================================================

**Description**
The `Driver` class serves as a central point for managing and interacting with LangChain agents equipped with web tools.  

**Steps**

1. **Initialization**:
    - Create an instance of the `Driver` class.
    - Pass API keys for OpenAI and Gemini if you want to use them.
    - Optionally, pass the desired model names.
    - Specify `start_browser=True` if you want to enable browser tools.
2. **Using Web Tools**:
    - The `Driver` automatically sets up tools based on your configuration:
        - **`WebSearchAPI`**: Uses the `SerpAPIWrapper` for web search if a `SERPAPI_API_KEY` is available.
        - **Browser Tools**: Provides tools for navigating, scraping text, and clicking elements within a browser, using the `BrowserController` if it's available.
3. **Running Tasks**:
    - Use the `run_task` method to execute a task with the chosen LLM (Gemini or OpenAI).
    - Pass the task as a string to `run_task` and specify `use_gemini=True` for Gemini or `use_gemini=False` for OpenAI.
    - The agent will use the available tools to complete the task.
4. **Streaming Tasks**:
    - Utilize the `stream_task` method for streaming the execution steps of a task.
    - This method provides real-time updates as the agent interacts with tools.
    - Pass the task as a string to `stream_task` and specify `use_gemini=True` or `use_gemini=False` as needed.
5. **Cleanup**:
    - The `Driver` class handles closing the browser automatically when the object is deleted (`__del__` method).

**Usage Example**

```python
async def main():
    driver = Driver(start_browser=True)

    if not driver.tools:
        print("Tools are not available, so we'll run a simple task.")
        task_to_run = "Write a short poem about programming."
    else:
        print(f"Available tools: {[tool.name for tool in driver.tools]}")
        task_to_run = "What is the capital of Australia and what is the weather there now?"

    # Run a task using Gemini
    print("\nRunning run_task (Gemini):")
    if driver.gemini:
        result = await driver.run_task(task_to_run, use_gemini=True)
        print(f"Result: {result}")
    else:
        print("Gemini is not available.")

    # Stream a task using Gemini
    print("\nStreaming stream_task (Gemini):")
    if driver.gemini:
        final_answer, chunks = await driver.stream_task(task_to_run, use_gemini=True)
        print(f"Final answer: {final_answer}")
        print(f"Chunks: {len(chunks)}")
    else:
        print("Gemini is not available.")

asyncio.run(main())
```

**Additional Information**

- Ensure that the necessary API keys are set in environment variables (e.g., `SERPAPI_API_KEY`) if you want to use the corresponding tools.
- The `BrowserController` is an example; you'll likely need to replace it with your own browser control implementation or a library that provides browser automation functionality.
- This code utilizes standard Python logging.
- The provided `Config` class defines the API key and model settings, which you may need to customize to match your specific configuration.
- The `stream_agent_execution` function handles the asynchronous streaming of agent execution.

This documentation provides a thorough guide on how to use the `Driver` class for managing LLM agents and their web tools.