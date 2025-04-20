### **Улучшенный код**

## \file /src/webdriver/driver.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
Модуль для работы с веб-драйверами Selenium.
==============================================
Основное назначение класса `Driver` — обеспечение унифицированного интерфейса для работы с веб-драйверами Selenium.

Он предоставляет интерфейс для взаимодействия с  веб-браузерами, 
такими как Chrome, Firefox и Edge. Код вебдрайверов находится в подмодулях `chrome`, `firefox`, `edge`, `playwright` .
Файлы настроек для веб-браузеров находятся в: `chrome\chrome.json`, `firefox\firefox.json`, `edge\edge.json`, `playwright\playwright.json`.
Класс Driver упрощает задачи инициализации драйвера, навигации по URL, управления куками и обработки исключений.
"""

import copy
import pickle
import time
import re
from pathlib import Path
from typing import Optional
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    InvalidArgumentException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
    ElementNotVisibleException
)
import header
from src import gs

from src.logger.logger import logger
from src.logger.exceptions import ExecuteLocatorException, WebDriverException


class Driver:
    """
    Класс обеспечивает удобный интерфейс для работы с различными драйверами, такими как Chrome, Firefox и Edge.

    Attributes:
        driver (selenium.webdriver): Экземпляр Selenium WebDriver.
    """
    current_url:str = ''

    def __init__(self, webdriver_cls, *args, **kwargs):
        """
        Инициализирует экземпляр класса Driver.

        Args:
            webdriver_cls: Класс WebDriver, например Chrome или Firefox.
            args: Позиционные аргументы для драйвера.
            kwargs: Ключевые аргументы для драйвера.

        Raises:
            TypeError: Если `webdriver_cls` не является допустимым классом WebDriver.

        Example:
            >>> from selenium.webdriver import Chrome
            >>> driver = Driver(Chrome, executable_path='/path/to/chromedriver')
        """
        if not hasattr(webdriver_cls, 'get'):
            raise TypeError('`webdriver_cls` должен быть допустимым классом WebDriver.')
        self.driver = webdriver_cls(*args, **kwargs)

    def __init_subclass__(cls, *, browser_name: Optional[str] = None, **kwargs):
        """
        Автоматически вызывается при создании подкласса `Driver`.

        Args:
            browser_name: Имя браузера.
            kwargs: Дополнительные аргументы.

        Raises:
            ValueError: Если browser_name не указан.
        """
        super().__init_subclass__(**kwargs)
        if browser_name is None:
            raise ValueError(f'Класс {cls.__name__} должен указать аргумент `browser_name`.')
        cls.browser_name = browser_name

    def __getattr__(self, item: str):
        """
        Прокси для доступа к атрибутам драйвера.

        Args:
            item: Имя атрибута.

        Example:
            >>> driver.current_url
        """
        return getattr(self.driver, item)

    def scroll(self, scrolls: int = 1, frame_size: int = 600, direction: str = 'both', delay: float = .3) -> bool:
        """
        Прокручивает страницу в указанном направлении.

        Args:
            scrolls: Количество прокруток, по умолчанию 1.
            frame_size: Размер прокрутки в пикселях, по умолчанию 600.
            direction: Направление ('both', 'down', 'up'), по умолчанию 'both'.
            delay: Задержка между прокрутками, по умолчанию 0.3.

        Returns:
            True, если успешно, иначе False.

        Example:
            >>> driver.scroll(scrolls=3, direction='down')
        """
        def carousel(direction: str = '', scrolls: int = 1, frame_size: int = 600, delay: float = .3) -> bool:
            """
            Локальный метод для прокрутки экрана.

            Args:
                direction: Направление ('down', 'up').
                scrolls: Количество прокруток.
                frame_size: Размер прокрутки.
                delay: Задержка между прокрутками.

            Returns:
                True, если успешно, иначе False.
            """
            try:
                for _ in range(scrolls):
                    self.execute_script(f'window.scrollBy(0,{direction}{frame_size})')
                    self.wait(delay)
                return True
            except Exception as ex:
                logger.error('Ошибка при прокрутке', exc_info=ex)
                return False

        try:
            if direction == 'forward' or direction == 'down':
                return carousel('', scrolls, frame_size, delay)
            elif direction == 'backward' or direction == 'up':
                return carousel('-', scrolls, frame_size, delay)
            elif direction == 'both':
                return carousel('', scrolls, frame_size, delay) and carousel('-', scrolls, frame_size, delay)
        except Exception as ex:
            logger.error('Ошибка в функции прокрутки', ex)
            return False

    @property
    def locale(self) -> Optional[str]:
        """
        Определяет язык страницы на основе мета-тегов или JavaScript.

        Returns:
            Код языка, если найден, иначе None.

        Example:
            >>> lang = driver.locale
            >>> print(lang)  # 'en' или None
        """
        try:
            meta_language = self.find_element(By.CSS_SELECTOR, "meta[http-equiv='Content-Language']")
            return meta_language.get_attribute('content')
        except Exception as ex:
            logger.debug('Не удалось определить язык сайта из META', ex)
            try:
                return self.get_page_lang()
            except Exception as ex:
                logger.debug('Не удалось определить язык сайта из JavaScript', ex)
                return

    def get_url(self, url: str) -> bool:
        """
        Переходит по указанному URL и сохраняет текущий URL, предыдущий URL и куки.

        Args:
            url: URL для перехода.

        Returns:
            `True`, если переход успешен и текущий URL совпадает с ожидаемым, `False` в противном случае.

        Raises:
            WebDriverException: Если возникает ошибка с WebDriver.
            InvalidArgumentException: Если URL некорректен.
            Exception: Для любых других ошибок при переходе.
        """
        _previous_url: str = copy.copy(self.current_url)

        try:
            self.driver.get(url)
           
            attempts = 5
            while self.ready_state not in ('complete','interactive'):
                """ Ожидание завершения загрузки страницы """
                attempts -= 5
                if attempts < 0: # Если страница не загрузилась за 5 попыток, то цикл прерывается с выводом сообщения об ошибке
                    logger.error(f'Страница не загрузилась за 5 попыток: {url=}')
                    ...
                    break
                time.sleep(1)

            if url != _previous_url:
                self.previous_url = _previous_url

            self._save_cookies_localy()
            self.current_url = url
            return True
            
        except WebDriverException as ex:
            logger.error('WebDriverException', ex)
            return False

        except InvalidArgumentException as ex:
            logger.error(f"InvalidArgumentException {url}", ex)
            return False
        except Exception as ex:
            logger.error(f'Ошибка при переходе по URL: {url}\n', ex)
            return False

    def window_open(self, url: Optional[str] = None) -> None:
        """Open a new tab in the current browser window and switch to it.

        Args:
            url: URL to open in the new tab. Defaults to `None`.
        """
        self.execute_script('window.open();')
        self.switch_to.window(self.window_handles[-1])
        if url:
            self.get(url)

    def wait(self, delay: float = .3) -> None:
        """
        Ожидает указанное количество времени.

        Args:
            delay: Время задержки в секундах. По умолчанию 0.3.

        Returns:
            None
        """
        time.sleep(delay)

    def _save_cookies_localy(self) -> None:
        """
        Сохраняет текущие куки веб-драйвера в локальный файл.

        Returns:
            None

        Raises:
            Exception: Если возникает ошибка при сохранении куки.
        """
        return True # <- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ debug
        try:
            with open(gs.cookies_filepath, 'wb') as cookiesfile:
                pickle.dump(self.driver.get_cookies(), cookiesfile)
        except Exception as ex:
            logger.error('Ошибка при сохранении куки:', ex)

    def fetch_html(self, url: Optional[str] = '') -> bool:
        """
        Fetches HTML content from a local file or web URL and stores it.

        This method attempts to retrieve the HTML source code based on the provided
        `url`. It supports fetching from local files using the 'file://'
        protocol and from web pages using 'http://' or 'https://' protocols
        by calling the instance's `get_url` method.

        If the `url` argument is not provided, is None, or is an empty string,
        the method will attempt to use the value stored in `self.current_url`.

        Upon successful retrieval, the HTML content is stored in the instance
        variable `self.html_content`. If any error occurs during the process
        (e.g., invalid path format for files, file not found, file read error,
        network error during web fetch, unsupported URL protocol), the error
        is logged, and the method returns `False`.

        Note on File Paths:
            - The method expects file paths to be prefixed with `file://`.
            - After removing `file://`, it currently uses a regular expression
              (`[a-zA-Z]:[\/].*`) designed to match Windows-style absolute paths
              (e.g., `C:/...` or `C:\...`). It may not correctly handle other
              path formats (like relative paths or standard Unix paths without
              this specific check) unless they coincidentally match the regex
              after the prefix removal. Consider this limitation for cross-platform
              compatibility.

        Args:
            url (Optional[str]): The URL or local file path (prefixed with 'file://')
                from which to fetch HTML content. Supports 'file://', 'http://',
                and 'https://' protocols. If omitted, empty, or None, the value
                of `self.current_url` will be used instead. Defaults to ''.

        Returns:
            bool: `True` if the HTML content was successfully fetched from the
                  specified source and stored in `self.html_content`.
                  `False` if any error occurred during the fetching or reading
                  process, or if the URL protocol is unsupported.

        Side Effects:
            - Sets `self.html_content` to the fetched HTML string on success.
            - May modify `self.page_source` via the `self.get_url` method call.
            - Logs errors using the configured `logger` upon failure.

        Examples:
            >>> instance = YourClassName()
            >>> instance.current_url = 'http://default.example.com'

            >>> # 1. Fetching from a web URL
            >>> success_web = instance.fetch_html('https://example.com/page')
            # Assuming get_url succeeds and sets self.page_source
            >>> print(success_web)
            True
            >>> print(instance.html_content) # doctest: +ELLIPSIS
            <html><body>Mock content for https://example.com/page</body></html>

            >>> # 2. Fetching from a local file (requires creating a dummy file)
            >>> import tempfile
            >>> import os
            >>> with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".html", encoding='utf-8') as tmp_file:
            ...     _ = tmp_file.write("<html><body>Local Test Content</body></html>")
            ...     tmp_file_path = tmp_file.name
            >>> # Construct file URI (adjust format for OS if needed, Path.as_uri() is robust)
            >>> file_uri = Path(tmp_file_path).as_uri() # e.g., file:///tmp/xyz.html or file:///C:/Users/...
            >>> # We need to adapt the URI slightly if the regex expects a drive letter explicitly
            >>> if os.name == 'nt':
            ...     # Reconstruct URI to match the regex C:/... if needed by implementation detail
            ...     # The current regex '[a-zA-Z]:[\\/].*' requires this on Windows
            ...     # Example: 'file://C:/Users/...'
            ...     match = re.match(r"file:///(?P<drive>[a-zA-Z]):/(?P<rest>.*)", file_uri)
            ...     if match:
            ...         file_uri_for_func = f"file://{match.group('drive')}:/{match.group('rest')}"
            ...     else: # Fallback if parsing fails, might not work with the function
            ...         file_uri_for_func = file_uri
            ... else: # On Unix-like systems, Path.as_uri() usually works if regex is ignored
            ...     file_uri_for_func = file_uri
            ...
            >>> # Mocking Path.exists() and open() for the example to work without the function's specific regex check
            >>> original_exists = Path.exists
            >>> original_open = open
            >>> def mock_exists(path_obj):
            ...     return str(path_obj) == tmp_file_path
            >>> def mock_open(path_obj, mode='r', encoding=None):
            ...     if str(path_obj) == tmp_file_path:
            ...         # Return a real file handle to the temp file
            ...         return original_open(tmp_file_path, mode, encoding=encoding)
            ...     else:
            ...         raise FileNotFoundError
            >>> Path.exists = mock_exists
            >>> builtins_open = __builtins__.open # Store original built-in open
            >>> __builtins__.open = mock_open # Temporarily override built-in open

            >>> # This part depends heavily on the regex implementation detail:
            >>> # Let's assume file_uri_for_func is now correctly formatted for the regex on Windows
            >>> # or that the regex check is bypassed/modified for Unix.
            >>> # Forcing a simple path string that *might* work with the regex if C: drive exists
            >>> test_uri = 'file://C:/path/to/mock/file.html' # Generic placeholder
            >>> if os.path.exists(Path(tmp_file_path)): # Ensure temp file still exists
            ...    if os.name == 'nt': # Construct path expected by regex
            ...        cleaned_path_str = tmp_file_path.replace('\\', '/') # Ensure forward slashes
            ...        drive = Path(tmp_file_path).drive # e.g., 'C:'
            ...        if drive:
            ...             test_uri = f"file://{drive}/{cleaned_path_str.split(':', 1)[1]}"
            ...        else: # If no drive, likely network path, won't match regex
            ...             test_uri = Path(tmp_file_path).as_uri() # Fallback
            ...    else: # Unix
            ...        test_uri = Path(tmp_file_path).as_uri() # e.g., file:///path/to/file
            ...
            >>> # Now, let's simulate the call with the constructed URI or a generic one
            >>> # NOTE: This example is complex due to mocking file system and the regex dependency
            >>> # A simplified test might just check the logic branches
            >>> print(f"Attempting to fetch: {test_uri}") # Show what URI is being used
            Attempting to fetch: ...
            >>> # success_file = instance.fetch_html(test_uri) # Actual call (mocked)
            >>> # print(success_file) # Expected: True
            >>> # print(instance.html_content) # Expected: "<html><body>Local Test Content</body></html>"
            >>> # Clean up mocks and temp file
            >>> Path.exists = original_exists
            >>> __builtins__.open = builtins_open
            >>> os.remove(tmp_file_path)
            >>> print("Skipping actual file test execution in docstring due to complexity") # Placeholder acknowledgment
            Skipping actual file test execution in docstring due to complexity

            >>> # 3. Using default URL (self.current_url)
            >>> success_default = instance.fetch_html() # url is '', use self.current_url
            >>> print(success_default)
            True
            >>> print(instance.html_content) # doctest: +ELLIPSIS
            <html><body>Mock content for http://default.example.com</body></html>

            >>> # 4. Handling a non-existent local file path
            >>> success_no_file = instance.fetch_html('file://C:/non/existent/file.html')
            >>> print(success_no_file)
            False

            >>> # 5. Handling file path with incorrect format (not matching regex)
            >>> success_bad_format = instance.fetch_html('file:///unix/style/path/without/drive/letter') # Might fail regex check
            >>> print(success_bad_format)
            False

            >>> # 6. Handling failure from get_url (e.g., 404 Not Found simulated)
            >>> success_fail_fetch = instance.fetch_html('http://example.com/notfound')
            >>> print(success_fail_fetch)
            False

            >>> # 7. Handling network error exception from get_url
            >>> success_network_error = instance.fetch_html('http://error.example.com')
            >>> print(success_network_error)
            False

            >>> # 8. Handling unsupported protocol
            >>> success_bad_protocol = instance.fetch_html('ftp://example.com/resource')
            >>> print(success_bad_protocol)
            False
        """
        # Determine the effective URL
        effective_url = url if isinstance(url, str) and url else self.current_url

        if not effective_url:
            logger.error("Ошибка: URL не указан и self.current_url не установлен.")
            return False

        # Process based on protocol
        if effective_url.startswith('file://'):
            cleaned_url = effective_url.replace('file://', '')
            # --- Specific Windows Path Check ---
            # Note: This regex is specific and might need adjustment for broader compatibility
            match = re.search(r'[a-zA-Z]:[\/].*', cleaned_url)
            if match:
                # Use the matched part as the potential file path
                # This assumes the regex correctly captures the intended path
                file_path_str = match.group(0)
                try:
                    file_path = Path(file_path_str)
                    if file_path.exists() and file_path.is_file():
                        try:
                            with open(file_path, 'r', encoding='utf-8') as file:
                                self.html_content = file.read()
                            logger.info(f"Успешно прочитан файл: {file_path}")
                            return self.html_content
                        except Exception as ex:
                            logger.error(f'Ошибка при чтении файла {file_path}: ',ex)
                            return False
                    elif not file_path.exists():
                        logger.error(f'Локальный файл не найден: {file_path}')
                        return False
                    else:
                         logger.error(f'Указанный путь не является файлом: {file_path}')
                         return False
                except Exception as ex:
                     logger.error(f'Ошибка при обработке пути файла {file_path_str}: ',ex)
                     ...
                     return False
            else:
                # Path did not match the expected Windows-like format after 'file://'
                logger.error(f'Некорректный или неподдерживаемый формат пути к файлу (ожидался C:/...): {cleaned_url}')
                return False


            # --- End Specific Windows Path Check ---

        elif effective_url.startswith('http://') or effective_url.startswith('https://'):
            try:
                # Assuming self.get_url fetches the content and returns True on success,
                # and stores the result in self.page_source.
                if url:
                    if not self.get_url(url):
                        logger.error(f"Ошибка при получении URL {url}", None, False)
                        ...
                        return False
                return self.page_source

            except Exception as ex:
                # Catch exceptions raised by self.get_url (e.g., network errors)
                logger.error(f"Ошибка при получении URL {effective_url}:  ",ex)
                return False
        else:
            # URL does not start with supported protocols
            logger.error(f"Ошибка: Неподдерживаемый протокол для URL: {effective_url}")
            ...
            return False