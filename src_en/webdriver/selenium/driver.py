# # \file /src/webdriver/driver.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3
"""Module for working with web-drivers Selenium.
===================================================
The main purpose of the `Driver` class is to provide a unified interface for working with Selenium web-drivers.

It provides an interface for interacting with web browsers,
Such as Chrome, Firefox and Edge. The webravel code is located in the dummies of `chrome`,` firefox`, `edge`,` Playwright`.
Cettleing files for web browsers are in: `chrome \ chrome.json`,` firefox \ firefox.json`, `edge \ edge.json`,` PlayWright \ Playwright.json`.
The Driver class simplifies the tasks of initializing the driver, navigation on the URL, Couring and Exception Processing.

`` `RST
.. Module :: SRC.WebDriver.Driver
`` `"""
import copy
import pickle
import time
import re
from pathlib import Path
from typing import Optional, Union, Any
import urllib.parse # Added for better processing File: // uri
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    InvalidArgumentException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
    ElementNotVisibleException,
    WebDriverException as SeleniumWebDriverException # Rename for clarity
)

import header # If you need to report
from src import gs # If you need to report

from src.logger.logger import logger
# Exceptions of Executelocatorexception, WebDriverexception are not used in this file directly
# Left if they are used in other parts of the project importing this module
from src.logger.exceptions import ExecuteLocatorException, WebDriverException 



class Driver:
    """The class provides a convenient interface for working with various drivers, such as Chrome, Firefox and Edge.
    The copy of Selenium Webdriver is wrapping, providing additional methods and state management.

    Attributes:
        Driver (Selenium.webdriver.remote.webdriver.webdriver): copy of Selenium Webdriver (or compatible).
        Current_Url (str): current URL open in a browser. Initialized by an empty line.
        html_content (Optional [str]): Full HTML The contents of the last successfully loaded page.
                                      It is installed by `Fetch_html`.
        Previous_Url (Optional [str]): URL, which was opened to the last successful transition.
                                      It is initialized as NONE."""
    # Current URL open in a browser
    current_url: str = ''
    # Full HTML The contents of the last successfully loaded page
    html_content: Optional[str] = None 
    # Previous URL
    previous_url: Optional[str] = None 
    # Instance webdriver (type of type for clarity)
    driver: SeleniumWebDriverException # The overall exclusion of Selenium is used, but a specific type of driver is better if known

    def __init__(self, webdriver_cls: type, *args: Any, **kwargs: Any) -> None: # Webdriver_cls should be a type
        """The Driver copy initializes, creating a specimen provided by WebDriver.

        Args:
            Webdriver_cls (Type): WebDriver class for instance (for example, `selenium.webdriver.chrome`).
            *Args: Positional arguments transmitted to the designer `Webdriver_cls`.
            ** kwargs: named arguments transmitted to the constructor `Webdriver_cls`.

        RAISES:
            Typeerror: if `Webdriver_Cls` is not a class or does not have the necessary WebDriver attributes.

        Example:
            >>> # Mock Webdriver Class for Example
            >>> Class mockwebdriver:
            ... Def __init __ (self, *arg, ** kwargs): Self.page_Source = ""
            ... Def Get (Self, URL): Self._current_url_prop = url; self.page_source = f "<html> <body> control for {url} </body> </ html>"
            ... Def Execute_Script (Self, Script): Return 'Complete' # Mock Ready State
            ... @property
            ... Def Current_url (Self): Return Getattr (Self, '_current_URL_PROP', '') # changed to _current_URL_PROP
            ... Def get_cookies (Self): Return [{'Name': 'Session', 'Value': '123'}]
            ... Def Find_element (Self, By, Value): Raise Exception ("Not Found")
            ... Def Switch_to (SELF): Return Self 
            ... Def Window (Self, Handle): Pass 
            ... @property
            ... Def Window_handles (Self): Return ['Handle1'] 
            >>> Driver_instance = Driver (Mockwebdriver) 
            >>> Print (ISINSTANCE (Driver_instance.driver, MorkWebDriver))
            True"""
        # Check that Webdriver_cls is a class and has a 'get' method
        if not isinstance(webdriver_cls, type) or not hasattr(webdriver_cls, 'get'): 
            raise TypeError('`webdriver_cls` должен быть допустимым классом WebDriver (например, selenium.webdriver.Chrome).')
        # Creating a webdriver instance
        self.driver = webdriver_cls(*args, **kwargs)
        # Initialization of previous_url by None value
        self.previous_url: Optional[str] = None 

    def __init_subclass__(cls, *, browser_name: Optional[str] = None, **kwargs: Any) -> None:
        """Python life cycle method automatically caused by creating a subclass `driver`.
        Used to install the attribute `Browser_name` at the level of the subclass class.

        Args:
            Browser_name (Optional [str]): the name of the browser, which must indicate the subclass.
            ** KWARGS (ANY): additional named arguments transmitted in `super () .__ Init_subclass__`.

        RAISES:
            Valuerror: if `browser_name` is not indicated when determining the subclass."""
        super().__init_subclass__(**kwargs)
        if browser_name is None:
            raise ValueError(f'Класс {cls.__name__} должен указать аргумент `browser_name` при наследовании от Driver.')
        # Installation of a browser name as an attribute of class
        cls.browser_name = browser_name

    def __getattr__(self, item: str) -> Any:
        """The magical method for delegating access to attributes.
        If the attribute `item` is not found in the specimen` driver`, the search is transmitted
        Inbound object `self.driver` (copy of Selenium Webdriver).

        Args:
            item (str): the name of the attribute for access.

        Returns:
            ANY: The value of the requested attribute.

        RAISES:
            Attributeerror: if the attribute is not found in `driver`, nor in the attached` self.driver`.

        Example:
            >>> Class mockwebdriverattr:
            ... Def __init __ (self): self._url_prop = "http://example.com" # changed to _url_prop
            ... @property
            ... Def Current_Url (Self): Return Self._url_prop # Used _url_prop
            ... Def Get (Self, URL): Pass 
            >>> Driver_instance = Driver
            >>> Print (driver_instance.current_url) # access to driver.current_url through __getttr__
            http://example.com"""
        # First check if there is an attribute at the very copy of Driver
        if item in self.__dict__:
            return self.__dict__[item]
        # If not, we are trying to get it from the invested self.driver
        try:
            return getattr(self.driver, item)
        except AttributeError:
            # If the attribute is not found there, we generate the standard exclusion of Attributeerror
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}' and its 'driver' object ({type(self.driver).__name__}) also has no attribute '{item}'")


    def scroll(self, scrolls: int = 1, frame_size: int = 600, direction: str = 'both', delay: float = .3) -> bool:
        """Scrolls the current web page in the indicated direction.

        Args:
            Scrolls (Int): The number of separate scrolls for execution. By default 1.
            Frame_size (int): the size of each scroll in pixels. By default 600.
            Direction (str): direction of scrolling. Permissible values:
                             'Down' or 'Forward' (down),
                             'up' or 'backward' (up),
                             'Both' (first down, then up). By default 'Both'.
            Delay (Float): Delay in seconds between consistent scrolls. By default 0.3.

        Returns:
            Bool: `true`, if all scrolls in the indicated direction (yach) are successfully performed, otherwise` false`.

        Example:
            >>> Class mockwebdriverscroll:
            ... Def Get (Self, URL): Pass
            ... Def Execute_Script (Self, Script): Print (F "Executed: {Script}"); Return None
            >>> Driver_instance = Driver (Mockwebdriverscroll)
            >>> Driver_instance.scroll (Scrolls = 1, Direction = 'Down') # doctest: + ellipse
            Executed: Window.Scrollby (0.600)
            True"""
        # Internal auxiliary function for scrolling
        def carousel(dir_sign: str = '', num_scrolls: int = 1, size: int = 600, scroll_delay: float = .3) -> bool:
            """The local method for performing a series of scrolls in one direction."""
            try:
                for _ in range(num_scrolls):
                    # JavaScript execution to scroll the window
                    self.driver.execute_script(f'window.scrollBy(0,{dir_sign}{size})')
                    # Using the self.wait method to delay
                    self.wait(scroll_delay)
                return True # Successful implementation
            except Exception as ex:
                # Logging error during scrolling
                logger.error(f'Ошибка при прокрутке ({dir_sign or "down"}):', None, exc_info=ex)
                return False # Unsuccessful execution

        try:
            # Processing of various areas of scrolling
            if direction in ('forward', 'down'):
                return carousel('', scrolls, frame_size, delay)
            elif direction in ('backward', 'up'):
                return carousel('-', scrolls, frame_size, delay)
            elif direction == 'both':
                # Scroll down, then up
                down_success: bool = carousel('', scrolls, frame_size, delay)
                # Self.Wait (Delay) # Additional delay between "down" and "Up" (optionally)
                up_success: bool = carousel('-', scrolls, frame_size, delay)
                return down_success and up_success # Success if both areas are successful
            else:
                # Error 500 (Server Error)!!1500.That’s an error.There was an error. Please try again later.That’s all we know.
                logger.warning(f"Неизвестное направление прокрутки: {direction}")
                return False
        except Exception as ex:
            # Logging an unexpected error in the main function of Scroll
            logger.error('Неожиданная ошибка в функции scroll:', None, exc_info=ex)
            return False


    @property
    def locale(self) -> Optional[str]:
        """Determines the language (local) of the current web page.
        Trying to extract the tongue first from the meta-tag 'Content-Language',
        Then from the attributes of `Lang` tags` <html> `or` <body> `,
        And finally, from the properties of JavaScript `navigator.language` or` navigator.userlanguage`.

        Returns:
            Optional [str]: a line with a language code (for example, 'en -us', 'fr'), if found, otherwise `none`.

        Example:
            >>> Class mockwebdriverlocalemeta:
            ... Def Get (Self, URL): Pass
            ... Def found_element (Self, By, Value):
            ... if value == "Meta [http-equiv = 'content-language']":
            ... Class mockelement:
            ... Def get_attribute (Self, NAME): Return 'EN-GB' if Name == 'Content' Else None
            ... Return Mockelement ()
            ... Else: Raise Seleniumwebdriverexception ("Meta Not Found") # Used SeleniumWebDriverexception
            ... Def Execute_Script (Self, Script): Return 'Fr-Ca' 
            >>> Driver_instance_meta = Driver (MOCKWEBDRIVERLOCalemeta)
            >>> Print (driver_instance_meta.locale)
            EN-GB
            >>> Class mockwebdriverlocalejs:
            ... Def Get (Self, URL): Pass
            ... Def Find_element (Self, By, Value): Raise SeleniumWebDriverexception ("Meta Not Found")
            ... Def Execute_Script (Self, Script):
            ... if 'doocument.documentElement.lang' in script: return 'de-de'
            ... Return None 
            >>> Driver_instance_js = Driver (Mockwebdriverlocalejs)
            >>> Print (driver_instance_js.locale)
            De-de"""
        try:
             # Trying to find meta-language meta-tag
            meta_language_element = self.driver.find_element(By.CSS_SELECTOR, "meta[http-equiv='Content-Language']")
            lang_code: Optional[str] = meta_language_element.get_attribute('content')
            if lang_code: return lang_code
        except Exception: # If the meta-tag is not found or another error has occurred
            logger.debug('Не удалось определить язык из META "Content-Language", попытка через JS.')
            pass # We continue attempts in other ways

        try:
            # An attempt to get a language through JavaScript (attributes of HTML, Body, Navigator)
            # The script returns the first non -empty value of the listed properties
            lang_code_js: Optional[str] = self.driver.execute_script(
                "return document.documentElement.lang || document.body.lang || navigator.language || navigator.userLanguage;"
            )
            if lang_code_js:
                return str(lang_code_js) # Return language if it is found through js
            else:
                logger.debug('JavaScript не вернул информацию о языке.')
                return None # If js has not returned the tongue
        except Exception as ex_js:
            # Warning logistics, if through JS it was not possible to determine the language
            logger.warning('Не удалось определить язык сайта из JavaScript.', None, exc_info=ex_js)
            return None # None return if all attempts are unsuccessful

    @property
    def ready_state(self) -> Optional[str]:
         """Returns the state of downloading the document (`doCumb.Readystate`).
         Possible values: 'Loading', 'Interactive', 'Complete'.

         Returns:
            Optional [str]: a string with a state `doCument.readystate` or` none` in case of an error."""
         try:
             # Performing JavaScript to obtain doocument.readstaystate
             return self.driver.execute_script('return document.readyState;')
         except Exception as ex:
              # Error logging if it was not possible to get ReadyState
              logger.error("Не удалось получить document.readyState:", None, exc_info=ex)
              return None

    def get_url(self, url: str) -> bool:
        """It crosses the specified URL.
        Updates `self.current_url` and` self.previous_url`.
        It expects that `doCumb.Readystate` is not 'Complete' or 'Interactive'.
        Saves cookies after a successful transition (if the logic is _save_cook_Localy` active).

        Args:
            URL (str): URL for navigation.

        Returns:
            Bool: `true`, if the transition is successful and the page is loaded (ReadyState 'Complete' or 'Interactive'), 
                  `False` Otherwise (for example, incorrect URL, WebDriver error, loading Timout)."""
        # Preservation of the current URL as the previous one before the transition
        _previous_url_local: str = copy.copy(self.current_url)

        try:
            logger.info(f"Переход на URL: {url}")
            # Execution of the transition using the Get driver method
            self.driver.get(url)

            # Waiting for page loading (ReadyState check)
            attempts: int = 10 # The number of attempts to verify ReadyState
            loaded: bool = False # Successful loading flag
            while attempts > 0:
                state: Optional[str] = self.ready_state # Obtaining the current ReadyState
                logger.debug(f"Попытка {11-attempts}/10: readyState={state} для {url}")
                # Check whether the state of the COMPLETE or 'Interactive'
                if state in ('complete', 'interactive'):
                    loaded = True
                    logger.info(f"Страница загружена (readyState={state}): {url}")
                    break # Exit from the cycle if the page is loaded
                attempts -= 1
                if attempts == 0:
                    # Error logging if the page has not loaded for all attempts
                    logger.error(f'Страница не достигла состояния "complete" или "interactive" за 10 попыток: {url}')
                    return False # Explicit return FALSE
                self.wait(0.5) # Short delay between checks

            # URL update and conservation of cookies only if the load was successful
            if loaded:
                # Obtaining actual URL after a possible redirect
                actual_url_after_get: str = self.driver.current_url
                logger.info(f"Фактический URL после перехода: {actual_url_after_get}")
                self.current_url = actual_url_after_get # Current_url update

                # Previous_url update if the URL has changed
                if self.current_url != _previous_url_local:
                    self.previous_url = _previous_url_local
                    logger.debug(f"Предыдущий URL сохранен: {_previous_url_local}")

                # SELF._SAVE_COOKIES_LOCALY () # uncomfort
                return True # Successful transition and loading

        except InvalidArgumentException as ex_invalid_arg:
            # Incorrect URL error processing
            logger.error(f"Некорректный URL '{url}': {ex_invalid_arg}")
            return False
        except SeleniumWebDriverException as ex_webdriver: 
            # Processing General Errors WebDriver
            logger.error(f'Ошибка WebDriver при переходе на {url}: {ex_webdriver}')
            return False
        except Exception as ex_other: 
            # Processing of any other unexpected mistakes
            logger.error(f'Неожиданная ошибка при переходе по URL: {url}', None, exc_info=ex_other)
            return False
        return False # Added for cases when Loaded remains FALSE, but there were no exceptions

    def window_open(self, url: Optional[str] = None) -> None:
        """Opens a new tab in the current browser window and switches to it.
        If `url` is indicated, it goes on this URL in a new tab.

        Args:
            URL (Optional [str]): URL for opening in a new tab. If `none` opens an empty tab.
                                By default `none`."""
        logger.debug("Открытие новой вкладки.")
        # Performing JavaScript to open a new empty tab
        self.driver.execute_script('window.open("");') 
        # Obtaining a descriptor of the last open tab
        new_window_handle: str = self.driver.window_handles[-1]
        # Switching to a new tab
        self.driver.switch_to.window(new_window_handle)
        logger.debug(f"Переключено на новую вкладку: {new_window_handle}")
        # If the URL is provided, the transition on it using self.get_url
        if url:
            self.get_url(url) 

    def wait(self, delay: float = .3) -> None:
        """Suspenses execution for the indicated amount of time.

        Args:
            Dlavy (Float): Delay time in seconds. By default 0.3."""
        if delay > 0:
            # logger.debug (f "Waiting {delay} sec.") # can be divorced for debugging
            time.sleep(delay) # Using the standard Time.Sleep function

    def _save_cookies_localy(self) -> None:
        """Saves current web drive cakes to a local file using `pickle`.
        The path to the Cooks file is taken from `gs.cookies_filepath`.
        If the path is not installed or errors occur, the cookies are not preserved and the corresponding message is logged in."""
        # Check, whether the Way to the Cook file is set
        if not hasattr(gs, 'cookies_filepath') or not gs.cookies_filepath: # Added Hasattr check
             logger.warning("Путь к файлу куки (gs.cookies_filepath) не установлен. Куки не сохранены.")
             return
        try:
            # Getting cookies from the driver
            cookies: list = self.driver.get_cookies()
            if cookies: # Preservation only if there are cookies
                # We guarantee that the parent directory for the Cook file exists
                Path(gs.cookies_filepath).parent.mkdir(parents=True, exist_ok=True)
                # Opening the file in binary mode for recording (WB) and saving cookies
                with open(gs.cookies_filepath, 'wb') as cookiesfile:
                    pickle.dump(cookies, cookiesfile)
                logger.info(f"Куки успешно сохранены в файл: {gs.cookies_filepath}")
            else:
                logger.info("Нет куки для сохранения.")
        except AttributeError:
             # Case processing if the driver does not support Get_Cookies ()
             logger.error("Текущий драйвер не поддерживает get_cookies().")
        except pickle.PicklingError as ex_pickle:
            # Pickle serialization errors processing
            logger.error(f"Ошибка сериализации (pickle) при сохранении куки в {gs.cookies_filepath}:", None, exc_info=ex_pickle)
        except IOError as ex_io:
            # Input and output errors
            logger.error(f"Ошибка ввода/вывода при сохранении куки в {gs.cookies_filepath}:", None, exc_info=ex_io)
        except Exception as ex_other: 
            # Processing other unexpected errors
            logger.error(f"Неожиданная ошибка при сохранении куки в {gs.cookies_filepath}:", None, exc_info=ex_other)


    def fetch_html(self, url: Optional[str] = '') -> Union[str, bool]:
        """Loads HTML content from a local file (diagram 'File: //') or from web-URL (schemes 'http: //', 'https: //').
        If `url` is not provided,` self.current_url` is used.
        With successful loading of HTML content, it remains in `self.html_content` and returns.

        Args:
            URL (Optional [str]): url (web or file: //) for loading. If an empty line or `none`,
                                 Used `self.current_url`. By default, an empty line.

        Returns:
            Union [str, bool]:
                - STR: Full HTML content of the page, if the load was successful.
                - FALSE: If an error has occurred (incorrect URL/path, the file was not found, the reading error,
                         Network error, unsupported protocol).

        Side Effects:
            - sets `Self.html_content` in the full line of HTML with success.
            - can change `self.current_url` and` self.previous_url` through a call `self.get_url`
              When processing web-URL.
            - Loggs information and errors using `logger`."""
        # Determining the effective URL for loading
        effective_url: str = url if isinstance(url, str) and url else self.current_url
        # Reset html_content before a new attempt
        self.html_content = None 

        # Check that the URL is defined for loading
        if not effective_url:
            logger.error("Ошибка fetch_html: URL не указан и self.current_url не установлен.")
            return False

        full_html_content: Optional[str] = '' # Store for the loaded html

        try:
            # Processing of local files (diagram 'File: //')
            if effective_url.startswith('file://'):
                try:
                    # Parsing URI file
                    parsed_uri: urllib.parse.ParseResult = urllib.parse.urlparse(effective_url)
                    if parsed_uri.scheme != 'file':
                         # This check is here for completeness, although Startswith has already checked
                         raise ValueError("Внутренняя ошибка: URI не является file:// в блоке обработки файлов.")

                    # Converting URI to the Way to the file, taking into account the features of platforms and coding
                    file_path_str_decoded: str = urllib.parse.unquote(parsed_uri.path)
                    
                    # Removing the leading slash for Windows routes (for example,/c:/... -> c:/...)
                    if re.match(r"\/[a-zA-Z]:", file_path_str_decoded): # Pattern for Windows Paths
                         file_path_str_decoded = file_path_str_decoded[1:] 

                    file_path_obj: Path = Path(file_path_str_decoded) # Creating an object PATH

                    # Checking the existence and type of file
                    if file_path_obj.exists() and file_path_obj.is_file():
                        # Reading the contents of the file
                        with file_path_obj.open('r', encoding='utf-8', errors='ignore') as file_handle:
                            full_html_content = file_handle.read()
                        logger.info(f"Успешно прочитан файл: {file_path_obj}")
                    elif not file_path_obj.exists():
                        logger.error(f'Локальный файл не найден: {file_path_obj}')
                        return '&nbsp;'
                    else: # If the path exists, but this is not a file (for example, a directory)
                        logger.error(f'Указанный путь не является файлом: {file_path_obj}')
                        return '&nbsp;'
                except ValueError as ve_uri: 
                    # Parsing error processing URI or creating a path
                    logger.error(f"Ошибка обработки URI/пути файла '{effective_url}': {ve_uri}")
                    return '&nbsp;'
                except IOError as e_io_file: 
                    # File reading errors
                    logger.error(f'Ошибка чтения файла {file_path_obj}: {e_io_file}') # file_path_obj may not be defined here
                    return '&nbsp;'
                except Exception as e_file_other: 
                     # Processing other unexpected errors when working with a file
                     logger.error(f'Неожиданная ошибка обработки пути файла {effective_url}:', None, exc_info=e_file_other)
                     return '&nbsp;'

            # Web-URL processing (schemes 'http: //', 'https: //')
            elif effective_url.startswith(('http://', 'https://')):
                try:
                    # If the requested URL differs from the current, we perform the transition
                    # This prevents unnecessary rebooting if the URL is already open.
                    if effective_url != self.current_url: 
                        if not self.get_url(effective_url):
                            # If Get_url returned false, then there is a loading error
                            logger.error(f'Ошибка при вызове get_url для {effective_url} внутри fetch_html.')
                            return False 
                    
                    # After a successful (or missed) get_url, we get the original page code
                    full_html_content = self.driver.page_source
                    if full_html_content:
                        # Self.current_Url should already be updated to Get_Url
                        logger.info(f"Успешно получен HTML для URL: {self.current_url}") 
                    else:
                        # The case when Get_url could return True, but page_source is empty (unlikely, but possible)
                        logger.warning(f"get_url вернул успех (или не вызывался), но self.driver.page_source пуст для {self.current_url}")
                        # Solution: Return False if Page_Source is empty, even if Get_url was successful
                        return '&nbsp;' 
                except Exception as ex_http:
                    # Processing of exceptions arising in self.get_url or when accessing page_source
                    logger.error(f"Исключение при получении URL {effective_url} или его HTML:", ex_http, True)
                    return '&nbsp;'

            else:
                # Processing of unsupported protocols
                logger.error(f"Ошибка fetch_html: Неподдерживаемый протокол для URL: {effective_url}")
                return '&nbsp;'

            # --- Completion of processing: preservation and return html ---
            if full_html_content is not None: # Check that Full_html_content is not None
                self.html_content = full_html_content # Preservation of the full HTML in the class attribute
                return full_html_content # SUCCESS! Return Full HTML.
            else:
                # This block should not be achieved if the logic is above correct,
                # But serves as an additional check.
                 logger.error(f"Ошибка внутреннего состояния fetch_html: HTML контент не был получен для {effective_url}, но предыдущая ошибка не была обработана.")
                 return '&nbsp;'

        except Exception as e_critical:
             # Capture of any truly unexpected critical errors at the upper level
             logger.exception(f"Неожиданная критическая ошибка во время fetch_html для {effective_url}: {e_critical}")
             return False


# --- an example of use (if it starts as a script) ---
if __name__ == '__main__':
    import tempfile # To create temporary files
    import os       # To delete temporary files

    # Mock WebDriver for testing Fetch_html
    class MockWebDriverFetch:
        def __init__(self):
            self._current_url_prop = '' # Changed to avoid conflict of names
            self.page_source_content = '' # Changed to avoid conflict of names

        def get(self, url_param: str) -> bool: # The name of the parameter has been changed
            print(f"[MockWebDriver] Вызов get({url_param})")
            if "error_in_get" in url_param: # Imitation of error directly to Get
                raise SeleniumWebDriverException(f"Имитация WebDriverException в get для {url_param}")
            if "notfound_page" in url_param: # Imitation of the page that Get_url will consider unsuccessful
                self._current_url_prop = url_param
                self.page_source_content = "<html><head><title>Not Found Page</title></head><body><h1>404 Not Found</h1></body></html>"
                print(f"[MockWebDriver] Имитация неудачной загрузки (например, readyState не complete) для {url_param}")
                # In real get_url, the ReadyState check cycle would end in failure.
                # Here we are just a FALSE return to simulate it.
                return False 
            if "no_body_tag_page" in url_param: # Page without a BODY BODY but get_url successful
                 self._current_url_prop = url_param
                 self.page_source_content = "<!DOCTYPE html><html><head><title>No Body Tag Page</title></head><p>Content outside body</p></html>"
                 print(f"[MockWebDriver] Успешная загрузка (без тега body): {url_param}")
                 return True # Get_url successful
            if "empty_page_source_page" in url_param: # Get_url successful but page_source desolate
                self._current_url_prop = url_param
                self.page_source_content = "" # Empty page_source
                print(f"[MockWebDriver] Успешная загрузка (но пустой page_source): {url_param}")
                return True # Get_url successful
            
            # Successful case for Get
            self._current_url_prop = url_param
            self.page_source_content = f"<!DOCTYPE html>\n<html><head><title>Test Page</title></head>" \
                               f"<body class='main-body'>\n<h1>Success Title</h1><p>Content for {url_param}</p>\n</body></html>"
            print(f"[MockWebDriver] Успешная загрузка: {url_param}")
            return True 

        def execute_script(self, script_param: str) -> Optional[str]: # The name of the parameter has been changed
            if 'readyState' in script_param:
                # We imitate various ReadyState for testing get_url
                if "notfound_page" in self._current_url_prop: # If the URL contains "notfound_page"
                    print(f"[MockWebDriver] execute_script('{script_param}') -> 'loading' (для {self._current_url_prop})")
                    return 'loading' # We imitate that the page is still loading
                print(f"[MockWebDriver] execute_script('{script_param}') -> 'complete' (для {self._current_url_prop})")
                return 'complete'
            print(f"[MockWebDriver] execute_script('{script_param}')")
            return None

        @property
        def current_url(self) -> str:
            return self._current_url_prop

        @property # Added property page_source
        def page_source(self) -> str:
            return self.page_source_content

        # Other mock methods for completeness of the Driver class
        def get_cookies(self): return [] 
        def find_element(self, by, value): raise SeleniumWebDriverException("Not Found in Mock") 
        def switch_to(self): return self
        def window(self, handle): pass
        @property
        def window_handles(self): return ['h1_mock']


    # Creation of Driver instance with Mock WebDriver
    test_instance = Driver(MockWebDriverFetch)
    test_instance.current_url = 'http://default.example.com/initial' # Installation of the initial URL

    print("\n--- Тестирование fetch_html с Веб URL ---")
    # 1. Successful loading web url
    html_web_good = test_instance.fetch_html('https://good.example.com/webpage')
    print(f"Результат (Успех Веб): {type(html_web_good)}")
    if isinstance(html_web_good, str):
        print(f"Полученный HTML (Веб):\n---\n{html_web_good[:150]}...\n---") # Conclusion of part HTML
    print(f"Сохраненный html_content: {test_instance.html_content is not None}")
    print("-" * 30)

    # 2. Using URL by default (Self.current_URL)
    # "Load" URL by default to update Page_Source in MOK
    print("Имитация загрузки URL по умолчанию через get_url...")
    test_instance.get_url(test_instance.current_url) # This will update Page_Source in MOK
    print("Вызов fetch_html() без аргументов (использует self.current_url)...")
    html_default_url = test_instance.fetch_html() 
    print(f"Результат (URL по умолчанию): {type(html_default_url)}")
    if isinstance(html_default_url, str):
        print(f"Полученный HTML (URL по умолчанию):\n---\n{html_default_url[:150]}...\n---")
    print(f"Сохраненный html_content: {test_instance.html_content is not None}")
    print("-" * 30)

    # 3. Error processing from Get_Url (for example, ReadyState not 'Complete')
    print("Тест URL, для которого get_url вернет False (имитация 'notfound_page')...")
    result_get_url_false = test_instance.fetch_html('http://example.com/notfound_page')
    print(f"Результат (get_url False): {result_get_url_false}") 
    print(f"Тип результата: {type(result_get_url_false)}")
    print(f"Сохраненный html_content: {test_instance.html_content is None}") # Should be None
    print("-" * 30)

    # 4. Processing the exclusion of WebDriverexception from Get_url
    print("Тест URL, который вызовет WebDriverException в get ('error_in_get')...")
    result_webdriver_ex = test_instance.fetch_html('http://error_in_get.example.com')
    print(f"Результат (WebDriverException в get): {result_webdriver_ex}")
    print(f"Тип результата: {type(result_webdriver_ex)}")
    print(f"Сохраненный html_content: {test_instance.html_content is None}")
    print("-" * 30)

    # 5. Processing of an unfinished protocol
    print("Тест URL с неподдерживаемым протоколом...")
    result_unsupported_protocol = test_instance.fetch_html('ftp://example.com/some_resource')
    print(f"Результат (Неподдерживаемый протокол): {result_unsupported_protocol}")
    print(f"Тип результата: {type(result_unsupported_protocol)}")
    print(f"Сохраненный html_content: {test_instance.html_content is None}")
    print("-" * 30)

    # 6. Successful loading (get_url = true), but html without a tag <body> (for Fetch_html, this is not a mistake, will return the full html)
    print("Тест URL с контентом, но без тега <body> (для fetch_html вернет полный HTML)...")
    html_no_body_tag = test_instance.fetch_html('http://no_body_tag_page.example.com')
    print(f"Результат (Нет тега body, но fetch_html успешен): {type(html_no_body_tag)}")
    if isinstance(html_no_body_tag, str):
        print(f"Полученный HTML (Нет тега body):\n---\n{html_no_body_tag[:150]}...\n---")
    print(f"Сохраненный html_content: {test_instance.html_content is not None}")
    print("-" * 30)
    
    # 6.1 Successful loading (get_url = true), but page_source is empty
    print("Тест URL с успешным get_url, но пустым page_source...")
    result_empty_source = test_instance.fetch_html('http://empty_page_source_page.example.com')
    print(f"Результат (Пустой page_source): {result_empty_source}")
    print(f"Тип результата: {type(result_empty_source)}")
    print(f"Сохраненный html_content: {test_instance.html_content is None}") # Should be None if page_source is empty
    print("-" * 30)


    print("\n--- Тестирование fetch_html с Локальными Файлами ---")
    # 7. Successful download of a local file with a tag Body
    temp_file_path_good = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".html", encoding='utf-8') as tmp_html_file:
            tmp_html_file.write("<!DOCTYPE html><html><head><title>Local File Test</title></head>"
                           "<body class='local-body'><h1>Local Test Content</h1><p>Это содержимое локального файла.</p></bOdY></html>")
            temp_file_path_good = tmp_html_file.name

        file_uri_good = Path(temp_file_path_good).as_uri() 
        print(f"Попытка загрузить из URI локального файла: {file_uri_good}")
        html_local_file_good = test_instance.fetch_html(file_uri_good)
        print(f"Результат (Успех Локальный Файл): {type(html_local_file_good)}")
        if isinstance(html_local_file_good, str):
            print(f"Полученный HTML (Локальный Файл):\n---\n{html_local_file_good[:200]}...\n---")
        print(f"Сохраненный html_content: {test_instance.html_content is not None}")
    except Exception as e_local_good:
        print(f"Ошибка во время теста успешного локального файла: {e_local_good}")
    finally:
        if temp_file_path_good and os.path.exists(temp_file_path_good):
            os.remove(temp_file_path_good)
            print(f"Удален временный файл: {temp_file_path_good}")
    print("-" * 30)

    # 8. Local file without tag <body> (Fetch_html will return full html)
    temp_file_no_body_path = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".html", encoding='utf-8') as tmp_html_file_no_body:
            tmp_html_file_no_body.write("<html><head><title>Local No Body</title></head></html>")
            temp_file_no_body_path = tmp_html_file_no_body.name
        file_uri_no_body_local = Path(temp_file_no_body_path).as_uri()
        print(f"Попытка загрузить из URI локального файла (без body): {file_uri_no_body_local}")
        html_local_no_body = test_instance.fetch_html(file_uri_no_body_local)
        print(f"Результат (Файл без Body, но fetch_html успешен): {type(html_local_no_body)}")
        if isinstance(html_local_no_body, str):
             print(f"Полученный HTML (Файл без Body):\n---\n{html_local_no_body[:150]}...\n---")
        print(f"Сохраненный html_content: {test_instance.html_content is not None}")
    except Exception as e_local_no_body:
        print(f"Ошибка во время теста локального файла без body: {e_local_no_body}")
    finally:
        if temp_file_no_body_path and os.path.exists(temp_file_no_body_path):
            os.remove(temp_file_no_body_path)
            print(f"Удален временный файл: {temp_file_no_body_path}")
    print("-" * 30)


    # 9. Processing of a non -existent local file
    non_existent_file_path = Path(tempfile.gettempdir()) / "___this_file_does_not_exist___.html"
    non_existent_file_uri = non_existent_file_path.as_uri()
    print(f"Попытка загрузить несуществующий URI локального файла: {non_existent_file_uri}")
    result_non_existent_file = test_instance.fetch_html(non_existent_file_uri)
    print(f"Результат (Несуществующий Локальный Файл): {result_non_existent_file}")
    print(f"Тип результата: {type(result_non_existent_file)}")
    print(f"Сохраненный html_content: {test_instance.html_content is None}")
    print("-" * 30)

    # 10. Processing of an incorrect File URI format
    # (Urllib.parse must cope with spaces, but test for completeness)
    # В Windows, путь C:\Temp\file with space.html будет file:///C:/Temp/file%20with%20space.html
    # Let's create a span file in the name for the test
    temp_file_with_space_path = None
    try:
        # Creating a temporary space with a span in the name
        temp_dir = Path(tempfile.gettempdir())
        filename_with_space = "test file with space.html"
        temp_file_with_space_path = temp_dir / filename_with_space
        with open(temp_file_with_space_path, 'w', encoding='utf-8') as f_space:
            f_space.write("<html><body>Space Test</body></html>")
        
        # URI with a gap (manually formed incorrectly)
        # Correct URI would be with %20. Urlparse and Path (). as_uri () do this.
        # But we are testing how Fetch_html will cope with a “raw” way if it somehow gets.
        # However, Path (). As_uri () will always return the correct URI.
        # Therefore, for the test of incorrect URI, we will "break" it after Path (). As_uri ()
        # Or pass on the line that Path () can interpret incorrectly.

        # First, we test with the correctly formed URI through Path (). As_uri ()
        correct_uri_with_space = temp_file_with_space_path.as_uri()
        print(f"Попытка загрузить URI с пробелом (сформирован Path.as_uri()): {correct_uri_with_space}")
        html_space_correct = test_instance.fetch_html(correct_uri_with_space)
        print(f"Результат (URI с пробелом, корректный): {type(html_space_correct)}")
        if isinstance(html_space_correct, str):
             print(f"HTML (URI с пробелом, корректный):\n---\n{html_space_correct[:100]}...\n---")
        print(f"Сохраненный html_content: {test_instance.html_content is not None}")
        print("-" * 15)
        
        # Now we simulate the "incorrect" URI, which can come from the outside
        # Although Unquote in Fetch_html should cope with %20 if URI still came with him.
        # For a real test of "incorrect URI that does not pierce", you need something like "File: // \\ Invalid"
        invalid_format_uri = "file:////server/share/inaccessible_or_bad_format"
        print(f"Попытка загрузить некорректно сформированный URI: {invalid_format_uri}")
        result_invalid_format_uri = test_instance.fetch_html(invalid_format_uri)
        print(f"Результат (Некорректный формат URI): {result_invalid_format_uri}")
        print(f"Тип результата: {type(result_invalid_format_uri)}")
        print(f"Сохраненный html_content: {test_instance.html_content is None}")

    except Exception as e_space_test:
        print(f"Ошибка во время теста URI с пробелом / некорректного URI: {e_space_test}")
    finally:
        if temp_file_with_space_path and os.path.exists(temp_file_with_space_path):
            os.remove(temp_file_with_space_path)
            print(f"Удален временный файл с пробелом: {temp_file_with_space_path}")
    print("-" * 30)
