# # \file src/webdriver/llm_driver/controllers.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""Module of controllers for managing a web browser and processing content.
=====================================================================================================
Provides classes for low -level control browser (BrowserController),
DECTIONS OF BETTRACED Data (DataextRactionController), work with forms (FormController),
download controls (downloadController), creation of screenshots (ScreenshotController),
Fulfillment JavaScript (JavaScriptexecheationController) and Statemanager.
These controllers use ** asynchronous ** API PlayWright and are designed for
Creating tools in Langchain asynchronous agents.

`` `RST
.. Module :: SRC.webdriver.llm_driver.controllers
`` `"""

# Standard libraries
import json
import re # To extract contacts
import asyncio # For Async Sleep and Cycle Management
import time # Can be removed or used for rare synchronous pauses
from pathlib import Path
from types import SimpleNamespace # May not be used here
from typing import (Any, AsyncIterator, Callable, Dict, List, Optional, Tuple, # pylint: disable=unused-import
                    Type, Union, TypeAlias, Coroutine) # Added Coroutine
from urllib.parse import urljoin # For processing relative links

# === Playwright Async Imports ===
# Imports of asynchronous components Playwright
from playwright.async_api import (async_playwright, Page, Browser, Playwright, # ASYNC API is used
                                  BrowserContext, Error as PlaywrightError, Download) # Added download, BrowserContext
# None

# === Data Extraction Imports ===
# Beautifulsoup import attempt to extract data
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE: bool = True # Flag Availability Beautifulsoup
except ImportError:
    BS4_AVAILABLE = False # Flag unavailability Beautifulsoup
# None

# === Internal/Project Imports ===
import header # Pylint: Disable = Unused-IMPORT # is imported for sid effects (sys.path)
# Import __root__ for correct relative project pathways
from header import __root__
# From SRC Import GS # GS may not be needed in this particular file
from src.logger import logger # I import the configured project logger
# None

# Determining pseudonyms for ASYNC API PlayWright to improve readability
ContextPage: TypeAlias = Optional[Page]
ContextBrowser: TypeAlias = Optional[Browser]
ContextPlaywright: TypeAlias = Optional[Playwright]
ContextBrowserContext: TypeAlias = Optional[BrowserContext]


# === BrowserController Class Definition (Async Version) ===
class BrowserController:
    """Controls a copy of the browser using ** asynchronous ** API PlayWright
    For navigation, data extraction and clicks by elements."""
    # Class attributes with type annotations
    playwright: ContextPlaywright = None # Playwright copy
    browser: ContextBrowser = None       # A copy of the browser
    page: ContextPage = None             # Current active page
    context: ContextBrowserContext = None # Browser context (for insulation of sessions)
    headless: bool                       # Browser launching flag in the headless mode
    default_timeout: int                 # Default timeout for operations
    _is_started: bool = False            # Flag for tracking asynchronous initialization

    def __init__(self, headless: bool = True, timeout: int = 30000) -> None:
        """Synchronously initializes the controller, preserving the parameters.
        Playwright asynchronous launch and browser are performed by `Start ()`.

        Args:
            Headless (Bool): Run the browser in Headless mode (without UI). By default True.
            Timeout (int): The default timing for navigation/actions in milliseconds. By default 30,000 (30C)."""
        # Initialization of instance attributes
        self.playwright = None
        self.browser = None
        self.page = None
        self.context = None
        self.headless = headless
        self.default_timeout = timeout
        self._is_started = False # Installation of the initial state is "not launched"
        logger.info(f'BrowserController создан (Headless={self.headless}, Timeout={self.default_timeout}ms). Вызовите start() для инициализации.')

    async def start(self) -> bool:
        """Asynchronically initializes Playwright, launches a browser and creates a page.
        Must be called from `AWAIT` before using other methods.

        Returns:
            Bool: True, if the initialization was successful, otherwise FALSE.

        RAISES:
            Runtimeerror: if you can’t initialize PlayWright or browser (it returns FALSE in the current implementation).

        Example:
            >>> Controller = BrowserController ()
            >>> if AWAIT CONTROLLER.START ():
            ... # Work with the controller
            ... aWAIT CONTROLLER.CLOSE ()"""
        # Check if the controller has already been launched
        if self._is_started:
            logger.warning('BrowserController уже инициализирован.')
            return True # If already launched, return is true

        logger.info('Асинхронная инициализация BrowserController...')
        try:
            # Playwright asynchronous launch
            self.playwright = await async_playwright().start()
            # Assinchronous launch of the browser (Chromium by default)
            self.browser = await self.playwright.chromium.launch(headless=self.headless)
            # Asynchronous creation of a new browser context
            self.context = await self.browser.new_context()
            # Asynchronous creation of a new page in context
            self.page = await self.context.new_page()
            # Setting the default time for the page
            if self.page: # Added check that Page is not none
                self.page.set_default_timeout(self.default_timeout)
            # Installation of the flag of successful launch
            self._is_started = True
            logger.info('Playwright запущен, браузер открыт, контекст и страница созданы (Async).')
            return True
        except Exception as ex:
            # Logging a critical error in initialization
            logger.error('КРИТИЧЕСКАЯ ОШИБКА Async: Не удалось инициализировать Playwright/Браузер.', ex, exc_info=True)
            # Attempts of asynchronous closure of resources when error
            await self.close()
            # FALSE return instead of exception so that the main code can process it
            return False

    async def navigate(self, url: str) -> str:
        """Asynkhronno translates the browser page to the specified URL.

        Args:
            URL (str): URL for navigation.

        Returns:
            STR: Status message about the success or navigation error.

        Example:
            >>> Status = AWAIT CONTROLLER.NAVIGATE ('https://toscrape.com/')
            >>> Print (status)
            A successful transition to https://toscraft.com/. Title: Example Domain. Start of the text: this domain is for uce in Illustrative Examps in Documents ..."""
        # Checking the initialization of the controller and the state of the page
        if not self._is_started or not self.page or self.page.is_closed():
             logger.error('Ошибка навигации: Контроллер не инициализирован или страница закрыта.')
             return 'Ошибка: Контроллер/страница не инициализированы или закрыты.'

        logger.info(f'Переход на: {url}')
        try:
            # Asynchronous transition to the URL, waiting for loading Dom
            response = await self.page.goto(url, wait_until='domcontentloaded')
            # Checking the success of the server response
            if response and response.ok:
                title: str = await self.page.title() # Asynchronous receipt of the page title
                logger.info(f"Успешный переход на {url}. Статус: {response.status}. Заголовок: '{title[:100]}'")
                try:
                    # Asynchronous receipt of Body's text content for a preamination
                    body_text: str = await self.page.locator('body').inner_text(timeout=5000) # TIMUout to extract text
                    return f'Успешный переход на {url}. Заголовок: {title}. Начало текста: {body_text[:200]}...'
                except Exception as text_ex:
                    # Warning logistics if it was not possible to quickly get the text
                    logger.warning(f'Не удалось быстро получить текст после навигации на {url}.', text_ex, exc_info=False)
                    return f'Успешный переход на {url}. Заголовок: {title}. (Текст не получен)'
            else:
                # Processing an unsuccessful answer
                status_code: Union[int, str] = response.status if response else 'N/A'
                logger.warning(f'Ошибка навигации для {url}. Статус: {status_code}')
                return f'Не удалось перейти на {url}. Статус: {status_code}'
        except PlaywrightError as ex:
            # Playwright error processing
            error_msg: str = ex.message.splitlines()[0] # Elimination of the first line of error messages
            logger.error(f'Ошибка Playwright при переходе на {url}: {error_msg}', None, exc_info=False)
            return f'Ошибка навигации на {url}: {error_msg}'
        except Exception as ex:
            # Processing other unexpected errors
            logger.error(f'Неожиданная ошибка при переходе на {url}.', ex, exc_info=True)
            return f'Неожиданная ошибка навигации на {url}: {str(ex)}'

    async def scrape_text(self, selector: Optional[str] = None) -> str:
        """Asynchronously extracts text content from the current page.
        If the selector is indicated, it extracts the text from the elements corresponding to the selector.
        Otherwise, it extracts the text of the entire tag `<body>`.

        Args:
            Selector (Optional [Str]): CSS selector. If None, it extracts the text of everything Body. By default None.

        Returns:
            STR: extracted and cleaned text or error message.

        Example:
            >>> Text_all = AWAIT CONTROLER.SCRAPE_TEXT ()
            >>> Heading_text = AWAIT CONTROLER.SCRAPE_TEXT ('h1.main-Title')"""
        # Verification of the initialization and state of the page
        if not self._is_started or not self.page or self.page.is_closed():
             logger.error('Ошибка извлечения текста: Контроллер не инициализирован или страница закрыта.')
             return 'Ошибка: Контроллер/страница не инициализированы или закрыты.'

        action_description: str = f'Извлечение текста (Селектор: {selector})' if selector else 'Извлечение текста (Body)'
        logger.info(action_description)
        content_raw: str = '' # Raw extracted contents
        cleaned_content: str = '' # Cleaned contents
        try:
            if selector:
                # Working with the specified selector
                elements = self.page.locator(selector)
                count: int = await elements.count() # Asynchronous receipt of the number of elements found
                if count == 0:
                    logger.warning(f"Элементы не найдены для селектора: '{selector}'")
                    return f"Элементы не найдены для селектора: {selector}"
                # Asynchronous receipt of the texts of all found elements
                all_texts: List[str] = await elements.all_inner_texts()
                # Combining texts, removing extra gaps
                content_raw = '\n\n'.join(t.strip() for t in all_texts if t.strip())
                logger.info(f'Извлечен текст из {count} элемент(ов) по селектору "{selector}". Длина: {len(content_raw)}')
            else:
                # Extracting the text of all Body
                content_raw = await self.page.locator('body').inner_text()
                logger.info(f'Извлечен текст из body. Длина: {len(content_raw)}')

            # Cleaning the extracted text: removal of empty lines and extra gaps in each line
            cleaned_content = '\n'.join([line.strip() for line in content_raw.splitlines() if line.strip()])
            return cleaned_content
        except PlaywrightError as ex:
            error_msg: str = ex.message.splitlines()[0]
            logger.error(f'Ошибка Playwright при извлечении текста (Селектор: {selector}): {error_msg}', None, exc_info=False)
            return f'Ошибка извлечения текста: {error_msg}'
        except Exception as ex:
            logger.error(f'Неожиданная ошибка при извлечении текста (Селектор: {selector}).', ex, exc_info=True)
            return f'Неожиданная ошибка извлечения текста: {str(ex)}'

    async def scrape_html(self, selector: Optional[str] = None) -> str:
        """Asynchronously extracts HTML contents from the current page or the specified element.

        Args:
            Selector (Optional [Str]): CSS element selector. If None, extracts HTML the entire page. By default None.

        Returns:
            STR: a line with HTML Content or an error message.

        Example:
            >>> Page_html = AWAIT CONTROLER.SCRAPE_HTML ()
            >>> Element_html = AWAIT CONTROLLER.SCRAPE_HTML ('# Unique-Element')"""
        # Verification of the initialization and state of the page
        if not self._is_started or not self.page or self.page.is_closed():
             logger.error('Ошибка извлечения HTML: Контроллер не инициализирован или страница закрыта.')
             return 'Ошибка: Контроллер/страница не инициализированы или закрыты.'

        action_description: str = f'Извлечение HTML (Селектор: {selector})' if selector else 'Извлечение HTML (Body)'
        logger.info(action_description)
        html_content: str = ''
        try:
            if selector:
                 # JavaScript asynchronous execution for obtaining Outerhtml of the first element by selector
                 html_content = await self.page.locator(selector).first.evaluate('element => element.outerHTML', timeout=10000)
            else:
                 # Asynchronous receipt of the HTML content of the entire page
                 html_content = await self.page.content()
            logger.info(f'Извлечен HTML. Длина: {len(html_content)}')
            return html_content
        except PlaywrightError as ex:
            error_msg: str = ex.message.splitlines()[0]
            logger.error(f'Ошибка Playwright при извлечении HTML (Селектор: {selector}): {error_msg}', None, exc_info=False)
            return f'Ошибка извлечения HTML: {error_msg}'
        except Exception as ex:
            logger.error(f'Неожиданная ошибка при извлечении HTML (Селектор: {selector}).', ex, exc_info=True)
            return f'Неожиданная ошибка извлечения HTML: {str(ex)}'

    async def click_element(self, selector: str) -> str:
        """Asynchronously clicks on the first visible element corresponding to the CSS selector.

        Args:
            Selector (str): CSS element selector for click.

        Returns:
            STR: Status message about success or click error.

        Example:
            >>> Status = AWAIT CONTROLLER.Click_ELEMENT ('Button# Submit-OrM"""
        # Verification of the initialization and state of the page
        if not self._is_started or not self.page or self.page.is_closed():
             logger.error('Ошибка клика: Контроллер не инициализирован или страница закрыта.')
             return 'Ошибка: Контроллер/страница не инициализированы или закрыты.'
        # Checking the presence of a selector
        if not selector:
            logger.warning('Ошибка клика: Не предоставлен селектор.')
            return 'Ошибка: Не указан селектор для клика.'

        logger.info(f"Попытка клика по элементу с селектором: '{selector}'")
        try:
            element_locator = self.page.locator(selector)
            count: int = await element_locator.count() # Asynchronous receipt of the number of elements
            if count == 0:
                logger.warning(f"Не удалось кликнуть: Элемент не найден по селектору '{selector}'")
                return f"Ошибка: Элемент не найден по селектору '{selector}'"
            if count > 1:
                # Warning if several elements are found (the first will be selected)
                logger.warning(f"Найдено несколько элементов ({count}) по селектору '{selector}'. Клик по первому видимому.")

            # Asynchronous expectation of visibility of the first element
            await element_locator.first.wait_for(state='visible', timeout=self.default_timeout // 3) # Timesout to wait
            # Asynchronous click on the first element
            await element_locator.first.click(timeout=self.default_timeout // 3) # Timesout for click
            logger.info(f"Успешный клик по первому элементу с селектором: '{selector}'")
            return f"Успешный клик по элементу: {selector}"
        except PlaywrightError as ex:
            error_msg: str = ex.message.splitlines()[0]
            logger.error(f"Ошибка Playwright при клике по '{selector}': {error_msg}", None, exc_info=False)
            # Special processing of the Timesout error
            if 'Timeout' in error_msg:
                 return f"Ошибка (таймаут) при клике/ожидании элемента '{selector}'. Возможно, он не появился или не кликабелен."
            return f"Ошибка клика по '{selector}': {error_msg}"
        except Exception as ex:
            logger.error(f"Неожиданная ошибка при клике по '{selector}'.", ex, exc_info=True)
            return f"Неожиданная ошибка клика по '{selector}': {str(ex)}"

    def get_current_url(self) -> str:
        """Synchronously returns the current URL page.
        Getting URL is the property of an object `page` and does not require asynchronism.

        Returns:
            STR: a line with the current URL or an error message if the page/controller is not ready."""
        if not self._is_started or not self.page or self.page.is_closed():
            logger.error('Ошибка получения URL: Контроллер не инициализирован или страница закрыта.')
            return 'Ошибка: Контроллер/страница не инициализированы или закрыты.'
        return self.page.url # Access to the property Page.url

    async def close(self) -> None:
        """Asynchronously closes the page, context, browser and stops Playwright.
        Liberates all related resources in the correct order.

        Example:
            >>> AWAIT CONTROLLER.CLOSE ()"""
        logger.info('Асинхронное закрытие BrowserController...')
        # Closing resources in the reverse order of their creation to prevent errors
        if self.page and not self.page.is_closed():
            try: await self.page.close(); logger.debug('Страница закрыта (Async).')
            except Exception as ex: logger.warning('Ошибка при закрытии страницы (Async).', ex, exc_info=False)
        self.page = None # Knocking the link

        if self.context: # PlayWright Context does not have an is_closed () as such, checking just the presence
             try: await self.context.close(); logger.debug('Контекст закрыт (Async).')
             except Exception as ex: logger.warning('Ошибка при закрытии контекста (Async).', ex, exc_info=False)
        self.context = None # Knocking the link

        if self.browser and self.browser.is_connected():
            try: await self.browser.close(); logger.debug('Браузер закрыт (Async).')
            except Exception as ex: logger.warning('Ошибка при закрытии браузера (Async).', ex, exc_info=False)
        self.browser = None # Knocking the link
        
        # PlayWright.Stop () is synchronous and designed to stop the PlayWright process,
        # Usually it is not necessary to call it clearly at each browser closing, if the application continues to work.
        # Playwright itself controls its life cycle.
        # if self.playwright:
        # Logger.debug ('PlayWright Object exists, Stop () is not called in Async Close.')
        self.playwright = None # Knocking the link

        self._is_started = False # Reset of the flag of initialization
        logger.info('Ресурсы BrowserController освобождены (Async).')

# None

# === DataExtractionController Class Definition ===
class DataExtractionController:
    """It extracts structured information from HTML or text (synchronously).
    Methods of this class do not require `AWAIT`, as they work with already obtained data (lines)."""
    def __init__(self) -> None:
        """Initiates the controller and checks the availability of the Beautifulsoup library."""
        if not BS4_AVAILABLE:
            # Warning if Beautifulsoup is not available
            logger.warning('Библиотека BeautifulSoup4 не найдена. Функции DataExtractionController будут ограничены.')
        logger.debug('DataExtractionController инициализирован.')

    # Методы extract_product_details, extract_contact_info, find_links
    # They remain synchronous, as they process the lines of HTML/text in memory.
    def extract_product_details(self, html_content: str) -> Dict[str, Any]:
        """It extracts goods about the product from the provided HTML content (implementation-playerlder). 
        For full work, it requires the availability of Beautifulsoup."""
        # Variables for storing data and facilities of parsing
        extracted_data: Dict[str, Any]
        soup: BeautifulSoup
        title_tag: Optional[Any] # Type depends on Beautifulsoup

        logger.info(f'Попытка извлечения данных о товаре (Длина HTML: {len(html_content)})...')
        # BeautifulSoup availability check
        if not BS4_AVAILABLE: return {'error': 'BeautifulSoup4 not available'}
        # Valinity check of input html
        if not html_content or not isinstance(html_content, str): return {'error': 'Invalid HTML content provided'}
        
        # Initialization of the dictionary for the extracted data with default values
        extracted_data = {
            'product_name': 'not found', 'url': 'not found', 'product_sku': 'not found', 
            'category_name': 'not found', 'parent_category': 'not found', 
            'brand_name': 'not found', 'brand_url': 'not found', 'product_image': 'not found', 
            'product_price': 'not found', 'product_description': 'not found', 
            'specifications': 'not found', 'product_params': {}, 
            'available_for_order': 'unknown', 'condition': 'not found'
        }
        try:
            # HTML Parsing using LXML (Fast Parser)
            soup = BeautifulSoup(html_content, 'lxml')
            # Example: extracting the name of goods from tag <h1>
            title_tag = soup.find('h1')
            if title_tag: extracted_data['product_name'] = title_tag.get_text(strip=True)
            # --- Other extract rules can be added here ---
            # For example, the search for prices, descriptions, SKU, etc. According to specific selectors.
            logger.warning('Извлечение данных о товаре ЗАВЕРШЕНО (базовая логика). Для реальных данных нужны специфичные парсеры.')
            return extracted_data
        except Exception as ex: 
            # Error logging when extracting
            logger.error('Ошибка при извлечении данных о товаре.', ex, exc_info=True)
            return {'error': f'Extraction failed: {str(ex)}'}

    def extract_contact_info(self, text_content: str) -> Dict[str, List[str]]:
        """Removes email addresses and telephone numbers from the provided text content.
        Uses regular expressions to search."""
        # Initialization of the dictionary for storage of contacts
        contacts: Dict[str, List[str]] = {'emails': [], 'phones': []}
        # Patterns of regular expressions for email and phones
        email_pattern: str
        phone_pattern: str
        logger.info(f'Попытка извлечения контактов (Длина текста: {len(text_content)})...')
        # Validity of the input text
        if not text_content or not isinstance(text_content, str): return {'error': 'Invalid text content provided'}
        
        # Pattern for email addresses
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        # Pattern for telephone numbers (simplified, may require finalization for different formats)
        phone_pattern = r'\(?\+?\d{1,4}?\)?[-\s\.]?\(?\d{1,4}?\)?[\d\s\.-]{7,}'
        try:
            # Search for all emails and phones, duplicate removal and sorting
            contacts['emails'] = sorted(list(set(re.findall(email_pattern, text_content))))
            contacts['phones'] = sorted(list(set(re.findall(phone_pattern, text_content))))
            logger.info(f"Найдено контактов: Emails={len(contacts['emails'])}, Phones={len(contacts['phones'])}")
            return contacts
        except Exception as ex: 
            # Error logging when extracting
            logger.error('Ошибка при извлечении контактов.', ex, exc_info=True)
            return {'error': f'Contact extraction failed: {str(ex)}'}

    def find_links(self, html_content: str, base_url: Optional[str] = None) -> Union[List[str], Dict[str, str]]:
        """Finds all unique links (tags `<a>` with the attribute `href`) in HTML content.
        Relative links are transformed into absolute if provided by `Base_url`."""
        # Initialization of the list of references
        links: List[str] = []
        soup: BeautifulSoup
        a_tag: Any # Type depends on Beautifulsoup
        href: str
        absolute_url: str
        unique_links: List[str]
        logger.info(f'Поиск ссылок (Длина HTML: {len(html_content)})...')
        # BeautifulSoup availability check
        if not BS4_AVAILABLE: return {'error': 'BeautifulSoup4 not available'}
        # Valinity check of input html
        if not html_content or not isinstance(html_content, str): return {'error': 'Invalid HTML content provided'}
        try:
            # Parsing html
            soup = BeautifulSoup(html_content, 'lxml')
            # Search for all tags <a> with an attribute href
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href'].strip() # Obtaining HREF value and gap removal
                # Filtration of empty references, anchor links and javascript link
                if href and not href.startswith('# ') and not href.startswith('javascript:'):
                     # Converting relative URLs into absolute, if there is a base_url
                     if base_url and not href.startswith(('http://', 'https://', '//')):
                         try: 
                             absolute_url = urljoin(base_url, href)
                             links.append(absolute_url)
                         except Exception as url_ex: 
                             # Logging URL transformation error
                             logger.warning(f'Не удалось сделать URL абсолютным: {href} (base: {base_url}).', url_ex, exc_info=False)
                             links.append(href) # Adding as it is with an error
                     else:
                         links.append(href) # Adding absolute or protocol-references
            # Duplicate removal and sorting
            unique_links = sorted(list(set(links)))
            logger.info(f'Найдено {len(unique_links)} уникальных ссылок.')
            return unique_links
        except Exception as ex: 
            # Logging error when searching for links
            logger.error('Ошибка при поиске ссылок.', ex, exc_info=True)
            return {'error': f'Link extraction failed: {str(ex)}'}

# None

# === FormController Class Definition (Async Version) ===
class FormController:
    """Controls the filling and sending HTML form on the page using
    Asynchronous API Playwright."""
    page: Page # Active Playwright page
    def __init__(self, page: Page) -> None:
        """Initializes FormController.

        Args:
            Page (Page): Active object of the PlayWright page.

        RAISES:
            Valuerror: if `page` is not provided or closed."""
        if not page or page.is_closed(): 
            raise ValueError('FormController требует активный объект страницы Playwright.')
        self.page = page
        logger.debug('FormController инициализирован.')

    async def fill_input_field(self, selector: str, value: str) -> str:
        """Asynchronously finds the entry field along the selector and introduces the indicated value into it.

        Args:
            Selector (StR): CSS input field selector.
            Value (str): meaning for entering into the field.

        Returns:
            STR: Status message about success or error."""
        field: Any # Playwright Locator
        logger.info(f"Заполнение поля '{selector}' значением '{value[:20]}...'")
        # Checking the state of the page
        if not self.page or self.page.is_closed(): return 'Ошибка: Страница закрыта.'
        try:
            # Obtaining the first element by the selector
            field = self.page.locator(selector).first
            # Waiting for the visibility of the element
            await field.wait_for(state='visible', timeout=10000)
            # Filling the field
            await field.fill(value)
            logger.info(f"Поле '{selector}' успешно заполнено.")
            return f"Поле '{selector}' заполнено."
        except PlaywrightError as ex: 
            error_msg=ex.message.splitlines()[0]
            logger.error(f"Ошибка Playwright при заполнении '{selector}': {error_msg}", None, exc_info=False)
            return f"Ошибка заполнения '{selector}': {error_msg}"
        except Exception as ex: 
            logger.error(f"Ошибка при заполнении '{selector}'.", ex, exc_info=True)
            return f"Ошибка заполнения '{selector}': {str(ex)}"

    async def select_dropdown_option(self, selector: str, value: Optional[str] = None, label: Optional[str] = None) -> str:
        """Asynchronously chooses the option in the drop -down list of value (`value`) or the text (` label`).

        Args:
            Selector (StR): CSS sealing list.
            Value (Optional [Str]): Value of the option for choosing.
            Label (Optional [str]): Text (label) options for selection.

        Returns:
            STR: Status message about success or error."""
        # Check that at least one selection criterion (Value or Label) is indicated
        if not value and not label: return 'Ошибка: Нужно указать value или label.'
        target_selection: str = f"value='{value}'" if value else f"label='{label}'"
        logger.info(f"Выбор опции {target_selection} в списке '{selector}'")
        # Checking the state of the page
        if not self.page or self.page.is_closed(): return 'Ошибка: Страница закрыта.'
        try:
            # Obtaining the first element (drop -down list) by the selector
            dropdown = self.page.locator(selector).first
            # Waiting for the visibility of the list
            await dropdown.wait_for(state='visible', timeout=10000)
            # Selecting the option by value or mark
            if value: await dropdown.select_option(value=value)
            elif label: await dropdown.select_option(label=label)
            logger.info(f"Опция {target_selection} успешно выбрана в '{selector}'.")
            return f"Опция {target_selection} выбрана в '{selector}'."
        except PlaywrightError as ex: 
            error_msg=ex.message.splitlines()[0]
            logger.error(f"Ошибка Playwright при выборе в '{selector}': {error_msg}", None, exc_info=False)
            return f"Ошибка выбора в '{selector}': {error_msg}"
        except Exception as ex: 
            logger.error(f"Ошибка при выборе в '{selector}'.", ex, exc_info=True)
            return f"Ошибка выбора в '{selector}': {str(ex)}"

    async def submit_form(self, form_selector: Optional[str] = None, submit_button_selector: Optional[str] = None) -> str:
        """Asynchronously sends a form. Can either click on the specified sending button,
        Or try to find and click on the standard sending button inside the specified form.
        This method by default does not expect the completion of navigation after sending.

        Args:
            Form_selector (Optional [Str]): CSS HTML form selector.
            Submit_button_selector (Optional [Str]): CSS selector of the Sending buttons.

        Returns:
            STR: Status message about success or error."""
        # Check that at least one selector is indicated (form or buttons)
        if not form_selector and not submit_button_selector: return 'Ошибка: Укажите селектор формы или кнопки.'
        target_action: str = f"кнопку '{submit_button_selector}'" if submit_button_selector else f"форму '{form_selector}'"
        logger.info(f"Отправка {target_action}")
        # Checking the state of the page
        if not self.page or self.page.is_closed(): return 'Ошибка: Страница закрыта.'
        try:
            if submit_button_selector:
                # If the button selector is indicated, click on it
                button = self.page.locator(submit_button_selector).first
                await button.wait_for(state='visible', timeout=10000)
                await button.click() # Simple click that does not expect navigation
            elif form_selector:
                 # If the form selector is indicated, we are looking for a standard sending button inside it
                 form_element = self.page.locator(form_selector).first
                 # Search for the Submit or Input Type Submit button
                 submit_btn_locator = form_element.locator('button[type="submit"], input[type="submit"]').first
                 is_btn_visible: bool = await submit_btn_locator.is_visible(timeout=5000)
                 if not is_btn_visible: 
                     return f"Ошибка: Не найдена видимая кнопка отправки в форме '{form_selector}'"
                 await submit_btn_locator.click() # Simple click
            logger.info(f"Форма/кнопка {target_action} успешно отправлена (клик выполнен).")
            return f"Форма/кнопка {target_action} отправлена."
        except PlaywrightError as ex: 
            error_msg=ex.message.splitlines()[0]
            logger.error(f"Ошибка Playwright при отправке {target_action}: {error_msg}", None, exc_info=False)
            return f"Ошибка отправки {target_action}: {error_msg}"
        except Exception as ex: 
            logger.error(f"Ошибка при отправке {target_action}.", ex, exc_info=True)
            return f"Ошибка отправки {target_action}: {str(ex)}"

# None

# === ScreenshotController Class Definition (Async Version) ===
class ScreenshotController:
    """Creates screenshots of the current page or its individual elements
    Using asynchronous API Playwright."""
    page: Page # Active Playwright page
    def __init__(self, page: Page) -> None:
        """Initializes ScreenshotController.

        Args:
            Page (Page): Active object of the PlayWright page.

        RAISES:
            Valuerror: if `page` is not provided or closed."""
        if not page or page.is_closed(): 
            raise ValueError('ScreenshotController требует активный объект страницы Playwright.')
        self.page = page
        logger.debug('ScreenshotController инициализирован.')

    async def take_screenshot(self, save_path: str, full_page: bool = True, selector: Optional[str] = None) -> str:
        """Asynchronously takes a screenshot. Can take a screenshot of the entire page visible part
        or the indicated element.

        Args:
            Save_path (str): the path to save the screenshot file.
            Full_Page (Bool): Do you take the screenshot of the entire page (if `Selector` is not indicated). By default True.
            Selector (Optional [Str]): CSS element selector for a screenshot. If specified, `Full_Page` is ignored.

        Returns:
            STR: Status message about success or error."""
        path_obj: Path = Path(save_path) # Transformation of the line line into an object PATH
        try:
            # Creating a parent directory if it does not exist
            path_obj.parent.mkdir(parents=True, exist_ok=True)
        except Exception as ex: 
            logger.error(f'Не удалось создать директорию: {path_obj.parent}', ex, exc_info=True)
            return f'Ошибка создания директории {path_obj.parent}'
        
        # Determination of the screenshot object for logging
        target_description: str = f"элемента '{selector}'" if selector else ("всей страницы" if full_page else "видимой части")
        logger.info(f'Создание скриншота {target_description} в файл: {path_obj}')
        # Checking the state of the page
        if not self.page or self.page.is_closed(): return 'Ошибка: Страница закрыта.'
        try:
             if selector:
                 # Screenshot of a particular element
                 element_locator = self.page.locator(selector).first
                 await element_locator.wait_for(state='visible', timeout=10000) # Waiting for the visibility of the element
                 await element_locator.screenshot(path=path_obj) # Creating a screenshot of the element
             else:
                 # Ground screenshot (all or visible part)
                 await self.page.screenshot(path=path_obj, full_page=full_page)
             logger.info(f'Скриншот {target_description} успешно сохранен в {path_obj}')
             return f'Скриншот сохранен: {path_obj}'
        except PlaywrightError as ex: 
            error_msg=ex.message.splitlines()[0]
            logger.error(f'Ошибка Playwright при создании скриншота {target_description}: {error_msg}', None, exc_info=False)
            return f'Ошибка скриншота {target_description}: {error_msg}'
        except Exception as ex: 
            logger.error(f'Ошибка при создании скриншота {target_description}.', ex, exc_info=True)
            return f'Ошибка скриншота {target_description}: {str(ex)}'

# None

# === DownloadController Class Definition (Async Version) ===
class DownloadController:
    """Controls the download of files initiated by actions on the page,
    Using asynchronous API Playwright."""
    page: Page # Active Playwright page
    def __init__(self, page: Page) -> None:
        """Initializes downloadController.

        Args:
            Page (Page): Active object of the PlayWright page.

        RAISES:
            Valuerror: if `page` is not provided or closed."""
        if not page or page.is_closed(): 
            raise ValueError('DownloadController требует активный объект страницы Playwright.')
        self.page = page
        logger.debug('DownloadController инициализирован.')

    async def click_and_download(self, click_selector: str, save_directory: str, timeout: int = 60000) -> str:
        """Asynchronously clicks on the element (for example, link or button) and expects the beginning
        File download. The downloaded file is stored in the specified directory.

        Args:
            Click_selector (str): CSS element selector, click on which the download initiates.
            Save_Directory (str): Directory for saving a downloaded file.
            Timeout (int): Timesout of waiting for the beginning of download in milliseconds. By default 60,000 (60C).

        Returns:
            STR: Status message about success or download error."""
        save_dir_path: Path = Path(save_directory) # Transformation of the line line into an object PATH
        try:
            # Creation of a directory for conservation if it does not exist
            save_dir_path.mkdir(parents=True, exist_ok=True)
        except Exception as ex: 
            logger.error(f'Не удалось создать директорию: {save_dir_path}', ex, exc_info=True)
            return f'Ошибка создания директории {save_dir_path}'
        
        logger.info(f"Попытка скачивания после клика на '{click_selector}' в {save_dir_path} (Таймаут: {timeout}ms)")
        # Checking the state of the page
        if not self.page or self.page.is_closed(): return 'Ошибка: Страница закрыта.'
        try:
            # Using a context manager `Expect_Download` to wait for the download event
            # Simultaneously with the performance of the action (click)
            async with self.page.expect_download(timeout=timeout) as download_info:
                # Find the element and click on it
                button_or_link = self.page.locator(click_selector).first
                await button_or_link.wait_for(state='visible', timeout=10000) # Waiting for the visibility of the element
                await button_or_link.click() # Click for downloading

            # Obtaining an object download after waiting for waiting
            download: Download = await download_info.value
            suggested_filename: str = download.suggested_filename # Obtaining the proposed file name
            save_path: Path = save_dir_path / suggested_filename # Full way to save a file
            # Preservation of the downloaded file
            await download.save_as(save_path)
            logger.info(f"Файл '{suggested_filename}' успешно скачан в {save_path}")
            return f'Файл скачан: {save_path}'
        except PlaywrightError as ex: 
            error_msg=ex.message.splitlines()[0]
            logger.error(f"Ошибка Playwright при скачивании '{click_selector}': {error_msg}", None, exc_info=False)
            return f"Ошибка скачивания '{click_selector}': {error_msg}"
        except Exception as ex: 
            logger.error(f"Ошибка при скачивании '{click_selector}'.", ex, exc_info=True)
            return f"Ошибка скачивания '{click_selector}': {str(ex)}"

# None

# === JavaScriptExecutionController Class Definition (Async Version) ===
class JavaScriptExecutionController:
    """Performs an arbitrary JavaScript code on the current page
    Using asynchronous API Playwright."""
    page: Page # Active Playwright page
    def __init__(self, page: Page) -> None:
        """Initializes JavaScriptexecitationController.

        Args:
            Page (Page): Active object of the PlayWright page.

        RAISES:
            Valuerror: if `page` is not provided or closed."""
        if not page or page.is_closed(): 
            raise ValueError('JavaScriptExecutionController требует активный объект страницы Playwright.')
        self.page = page
        logger.debug('JavaScriptExecutionController инициализирован.')

    async def execute_script(self, script: str) -> Union[str, Any]:
        """Asynchronously performs the JavaScript code on the page and returns the result.
        The result of the script is serialized in JSON, if possible.

        Args:
            Script (str): a string with a JavaScript code for execution.

        Returns:
            Union [str, ain]: the result of the script (serialized in json or as a line) 
                             Or an error message."""
        logger.warning(f'Выполнение JavaScript (ОСТОРОЖНО!): {script[:100]}...') # Potential danger warning
        # Checking the state of the page
        if not self.page or self.page.is_closed(): return 'Ошибка: Страница закрыта.'
        try:
            # Asynchronous performance of the script
            result: Any = await self.page.evaluate(script)
            logger.info(f'JavaScript выполнен успешно. Результат: {str(result)[:100]}...')
            try: 
                # Trying to serialize the result in json
                return json.dumps(result) 
            except TypeError: 
                # If serialization in JSON failed, return as a line
                return str(result) 
        except PlaywrightError as ex: 
            error_msg=ex.message.splitlines()[0]
            logger.error(f'Ошибка Playwright при выполнении JS: {error_msg}', None, exc_info=False)
            return f'Ошибка выполнения JS: {error_msg}'
        except Exception as ex: 
            logger.error('Ошибка при выполнении JS.', ex, exc_info=True)
            return f'Ошибка выполнения JS: {str(ex)}'

# None

# === StateManager Class Definition (Async Version) ===
class StateManager:
    """Managing the state of the browser session (cookies, localstorage, SessionStorage)
    Using asynchronous API Playwright."""
    context: BrowserContext # Playwright browser context
    page: ContextPage       # Optional active page (for operations with Localstorage/SessionStorage)
    def __init__(self, context: BrowserContext, page: ContextPage = None) -> None:
        """Initializes Statemanager.

        Args:
            CONTEXT (BROWSERCONTEXT): Active context of the PlayWright browser.
            PAGE (CONTEXTPAGE, OPTIONAL): Active Playwright page (necessary for `Clear_Storage`).
                                           By default None.

        RAISES:
            Valuerror: if `CONTEXT` is not provided or closed."""
        # PlayWright BrowserContext does not have IS_CLOSED (), verification only on NONE
        if not context: 
            raise ValueError('StateManager требует активный контекст браузера Playwright.')
        self.context = context
        self.page = page
        logger.debug('StateManager инициализирован.')

    async def get_cookies(self, url: Optional[str] = None) -> Union[List[Dict[str, Any]], str]:
        """Asynchronously returns the Cookies list for the current context of the browser.
        You can specify the URL for filtering cookies.

        Args:
            URL (Optional [str]): URL for filtering cookies. If None, returns all cookies.

        Returns:
            Union [list [dict [str, a ain], str]: a list of dictionaries with cookies or error message."""
        logger.info(f"Получение cookies (URL: {url or 'Все'})")
        # Checking the condition of the context (no IS_CLOSED (), check for NONE)
        if not self.context: return 'Ошибка: Контекст браузера закрыт или не инициализирован.'
        try: 
            # Asynchronous receipt of cookies
            cookies_list: List[Dict[str, Any]] = await self.context.cookies(urls=[url] if url else None)
            logger.info(f'Получено {len(cookies_list)} cookies.'); return cookies_list
        except Exception as ex: 
            logger.error('Ошибка при получении cookies.', ex, exc_info=True)
            return f'Ошибка получения cookies: {str(ex)}'

    async def add_cookies(self, cookies: List[Dict[str, Any]]) -> str:
        """Asynchronously adds a cooking list to the current context of the browser.

        Args:
            cookies (list [dict [str, any]): a list of dictionaries, each of which is represented by cookie.

        Returns:
            STR: Status message about success or error."""
        cookies_count: int = len(cookies)
        logger.info(f'Добавление {cookies_count} cookies...')
        # Checking the condition of the context
        if not self.context: return 'Ошибка: Контекст браузера закрыт или не инициализирован.'
        try: 
            # Asynchronous adding cookies
            await self.context.add_cookies(cookies)
            logger.info(f'{cookies_count} cookies успешно добавлены.'); return f'{cookies_count} cookies добавлены.'
        except Exception as ex: 
            logger.error('Ошибка при добавлении cookies.', ex, exc_info=True)
            return f'Ошибка добавления cookies: {str(ex)}'

    async def clear_cookies(self) -> str:
        """Asynchronically cleans all cookies in the current context of the browser.

        Returns:
            STR: Status message about success or error."""
        logger.info('Очистка cookies...')
        # Checking the condition of the context
        if not self.context: return 'Ошибка: Контекст браузера закрыт или не инициализирован.'
        try: 
            # Asynchronous cleaning cookies
            await self.context.clear_cookies()
            logger.info('Cookies очищены.'); return 'Cookies очищены.'
        except Exception as ex: 
            logger.error('Ошибка при очистке cookies.', ex, exc_info=True)
            return f'Ошибка очистки cookies: {str(ex)}'

    async def clear_storage(self) -> str:
        """Asynchronically cleans Localstorage and SessionStorage for the current active page.
        It requires that the attribute `page` be installed and the page be active.

        Returns:
            STR: Status message about success or error."""
        logger.info('Очистка localStorage и sessionStorage...')
        # Checking the availability and condition of the page
        if not self.page or self.page.is_closed(): return 'Ошибка: Страница закрыта или не доступна для очистки storage.'
        try: 
            # Performing JavaScript to clean Localstorage and SessionStorage
            await self.page.evaluate('() => { localStorage.clear(); sessionStorage.clear(); }')
            logger.info('localStorage и sessionStorage очищены.'); return 'localStorage и sessionStorage очищены.'
        except Exception as ex: 
            logger.error('Ошибка при очистке storage.', ex, exc_info=True)
            return f'Ошибка очистки storage: {str(ex)}'

    # Login remains a synchronous plug, since the logic of the entrance is highly dependent on a specific site
    # And usually requires the sequence of asynchronous actions that are best implemented in the agent.
    def login(self, *args: Any, **kwargs: Any) -> str:
         """Grandmother method for entering the site.
         The real logic of the entrance should be implemented using other controller methods
         (for example, navigation, filling fields, click) as part of an agent."""
         logger.warning('Метод login в StateManager является заглушкой и не выполняет реальных действий.'); return 'Заглушка: Вход не реализован.'

# None
