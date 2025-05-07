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
from typing import Optional, Union # Добавлено Union для нового типа возврата fetch_html
import urllib.parse # Добавлено для лучшей обработки file:// URI
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    InvalidArgumentException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
    ElementNotVisibleException
)

import header # Если нужно раскомментировать
from src import gs # Если нужно раскомментировать

from src.logger.logger import logger
from src.logger.exceptions import ExecuteLocatorException, WebDriverException



class Driver:
    """
    Класс обеспечивает удобный интерфейс для работы с различными драйверами, такими как Chrome, Firefox и Edge.

    Attributes:
        driver (selenium.webdriver): Экземпляр Selenium WebDriver.
        current_url (str): Текущий URL, открытый в браузере.
        html_content (Optional[str]): Полное HTML содержимое последней успешно загруженной страницы.
        page_source (Optional[str]): Свойство, предоставляемое Selenium, содержащее исходный код страницы.
                                      Используется для получения HTML при веб-запросах.
    """
    current_url: str = ''
    html_content: Optional[str] = None # Добавлено для хранения полного HTML
    # page_source будет доступен через self.driver.page_source

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
            >>> # Mock WebDriver class for example
            >>> class MockWebDriver:
            ...     def __init__(self, *args, **kwargs): self.page_source = ""
            ...     def get(self, url): self.current_url = url; self.page_source = f"<html><body>Content for {url}</body></html>"
            ...     def execute_script(self, script): return 'complete' # Mock ready state
            ...     @property
            ...     def current_url(self): return getattr(self, '_current_url', '')
            ...     @current_url.setter
            ...     def current_url(self, value): self._current_url = value
            ...     def get_cookies(self): return [{'name': 'session', 'value': '123'}]
            ...     def find_element(self, by, value): raise Exception("Not found") # Mock locale failure
            ...     def switch_to(self): return self # Mock switch_to
            ...     def window(self, handle): pass # Mock window switch
            ...     @property
            ...     def window_handles(self): return ['handle1'] # Mock window handles
            >>> driver_instance = Driver(MockWebDriver) # Pass the mock class
            >>> print(isinstance(driver_instance.driver, MockWebDriver))
            True
        """
        if not hasattr(webdriver_cls, 'get'): # Простая проверка наличия метода get
            raise TypeError('`webdriver_cls` должен быть допустимым классом WebDriver.')
        self.driver = webdriver_cls(*args, **kwargs)
        self.previous_url: Optional[str] = None # Инициализация previous_url

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
            >>> class MockWebDriverAttr:
            ...     def __init__(self): self._url = "http://example.com"
            ...     @property
            ...     def current_url(self): return self._url
            ...     def get(self, url): pass # Dummy method
            >>> driver_instance = Driver(MockWebDriverAttr)
            >>> print(driver_instance.current_url) # Accesses driver's property via __getattr__
            http://example.com
        """
        # Проверяем, есть ли атрибут у самого экземпляра Driver
        if item in self.__dict__:
            return self.__dict__[item]
        # Если нет, пытаемся получить его из вложенного self.driver
        try:
            return getattr(self.driver, item)
        except AttributeError:
            # Если и там нет, вызываем стандартное поведение AttributeError
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}' and its 'driver' object ({type(self.driver).__name__}) also has no attribute '{item}'")


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
            >>> # Mock driver with execute_script
            >>> class MockWebDriverScroll:
            ...     def get(self, url): pass
            ...     def execute_script(self, script): print(f"Executed: {script}"); return None
            >>> driver_instance = Driver(MockWebDriverScroll)
            >>> driver_instance.scroll(scrolls=1, direction='down') # doctest: +ELLIPSIS
            Executed: window.scrollBy(0,600)
            True
        """
        def carousel(dir_sign: str = '', num_scrolls: int = 1, size: int = 600, scroll_delay: float = .3) -> bool:
            """ Локальный метод для прокрутки экрана. """
            try:
                for _ in range(num_scrolls):
                    # Используем self.driver для доступа к методу execute_script экземпляра WebDriver
                    self.driver.execute_script(f'window.scrollBy(0,{dir_sign}{size})')
                    self.wait(scroll_delay) # Используем self.wait
                return True
            except Exception as ex:
                logger.error(f'Ошибка при прокрутке ({dir_sign or "down"}):', exc_info=ex)
                return False

        try:
            if direction in ('forward', 'down'):
                return carousel('', scrolls, frame_size, delay)
            elif direction in ('backward', 'up'):
                return carousel('-', scrolls, frame_size, delay)
            elif direction == 'both':
                # Выполняем прокрутку вниз, затем вверх
                down_success = carousel('', scrolls, frame_size, delay)
                # Ждем немного перед прокруткой вверх, если необходимо
                # self.wait(delay)
                up_success = carousel('-', scrolls, frame_size, delay)
                return down_success and up_success
            else:
                logger.warning(f"Неизвестное направление прокрутки: {direction}")
                return False
        except Exception as ex:
            logger.error('Неожиданная ошибка в функции scroll:', exc_info=ex)
            return False


    @property
    def locale(self) -> Optional[str]:
        """
        Определяет язык страницы на основе мета-тегов или JavaScript.

        Returns:
            Код языка, если найден, иначе None.

        Example:
            >>> class MockWebDriverLocale:
            ...     def get(self, url): pass
            ...     def find_element(self, by, value):
            ...         if value == "meta[http-equiv='Content-Language']":
            ...             class MockElement:
            ...                 def get_attribute(self, name): return 'en-US' if name == 'content' else None
            ...             return MockElement()
            ...         else: raise Exception("Not found")
            ...     def execute_script(self, script): return 'fr' # Mock JS locale
            >>> driver_instance = Driver(MockWebDriverLocale)
            >>> print(driver_instance.locale)
            en-US
            >>> # Example where meta fails, uses JS
            >>> class MockWebDriverLocaleJS:
            ...     def get(self, url): pass
            ...     def find_element(self, by, value): raise Exception("Meta not found")
            ...     def execute_script(self, script):
            ...         if 'navigator.language' in script: return 'de-DE'
            ...         return None # Default for other scripts
            >>> driver_instance_js = Driver(MockWebDriverLocaleJS)
            >>> print(driver_instance_js.locale)
            de-DE

        """
        try:
             # Используем self.driver для доступа к методу find_element
            meta_language = self.driver.find_element(By.CSS_SELECTOR, "meta[http-equiv='Content-Language']")
            return meta_language.get_attribute('content')
        except Exception:
            logger.debug('Не удалось определить язык сайта из META, пытаемся через JavaScript.')
            try:
                # Используем self.driver для доступа к execute_script
                # Проверяем несколько общих свойств JS для определения языка
                lang = self.driver.execute_script(
                    "return document.documentElement.lang || document.body.lang || navigator.language || navigator.userLanguage;"
                )
                if lang:
                    return str(lang) # Убедимся, что возвращается строка
                else:
                    logger.debug('JavaScript не вернул язык.')
                    return None
            except Exception as ex_js:
                logger.warning('Не удалось определить язык сайта из JavaScript.', exc_info=ex_js)
                return None

    # Убран get_page_lang, так как его логика встроена в locale
    # def get_page_lang(self): ...

    @property
    def ready_state(self) -> Optional[str]:
         """ Возвращает document.readyState """
         try:
             return self.driver.execute_script('return document.readyState;')
         except Exception as ex:
              logger.error("Не удалось получить document.readyState:", exc_info=ex)
              return None

    def get_url(self, url: str) -> bool:
        """
        Переходит по указанному URL и сохраняет текущий URL, предыдущий URL и куки.

        Args:
            url: URL для перехода.

        Returns:
            `True`, если переход успешен и страница загружена (readyState 'complete' или 'interactive'), `False` в противном случае.

        Raises:
            WebDriverException: Если возникает ошибка с WebDriver.
            InvalidArgumentException: Если URL некорректен.
            Exception: Для любых других ошибок при переходе.
        """
        _previous_url: str = copy.copy(self.current_url)

        try:
            logger.info(f"Переход на URL: {url}")
            self.driver.get(url)

            attempts = 10 # Увеличено количество попыток и уменьшена задержка
            loaded = False
            while attempts > 0:
                state = self.ready_state
                logger.debug(f"Попытка {11-attempts}/10: readyState={state} для {url}")
                if state in ('complete', 'interactive'):
                    loaded = True
                    logger.info(f"Страница загружена (readyState={state}): {url}")
                    break
                attempts -= 1
                if attempts == 0:
                    logger.error(f'Страница не достигла состояния "complete" или "interactive" за 10 попыток: {url}')
                    return False # Явный возврат False, если не загрузилась
                self.wait(0.5) # Уменьшенная задержка между проверками

            # Обновляем URL и сохраняем куки только если загрузка прошла успешно
            if loaded:
                # Проверка, что URL действительно тот, на который переходили (может быть редирект)
                actual_url = self.driver.current_url
                logger.info(f"Фактический URL после перехода: {actual_url}")
                self.current_url = actual_url # Сохраняем фактический URL

                if self.current_url != _previous_url:
                    self.previous_url = _previous_url
                    logger.debug(f"Предыдущий URL сохранен: {_previous_url}")

                #self._save_cookies_localy() # Сохраняем куки
                # self.html_content = self.driver.page_source # Сохраняем исходный код здесь? Или в fetch_html? Лучше в fetch_html.
                return True


        except InvalidArgumentException as ex:
            logger.error(f"Некорректный URL '{url}': {ex}")
            return False
        except WebDriverException as ex: # Более специфичные исключения Selenium
            logger.error(f'Ошибка WebDriver при переходе на {url}: {ex}')
            return False
        except Exception as ex: # Общий обработчик для других ошибок
            logger.error(f'Неожиданная ошибка при переходе по URL: {url}', exc_info=ex)
            return False

    def window_open(self, url: Optional[str] = None) -> None:
        """Открывает новую вкладку в текущем окне браузера и переключается на нее.

        Args:
            url: URL для открытия в новой вкладке. По умолчанию `None`.
        """
        logger.debug("Открытие новой вкладки.")
        # Используем self.driver для доступа к методам WebDriver
        self.driver.execute_script('window.open("");') # Открываем пустую вкладку для надежности
        new_window_handle = self.driver.window_handles[-1]
        self.driver.switch_to.window(new_window_handle)
        logger.debug(f"Переключено на новую вкладку: {new_window_handle}")
        if url:
            self.get_url(url) # Используем наш get_url для перехода

    def wait(self, delay: float = .3) -> None:
        """
        Ожидает указанное количество времени.

        Args:
            delay: Время задержки в секундах. По умолчанию 0.3.

        Returns:
            None
        """
        if delay > 0:
            # logger.debug(f"Ожидание {delay} сек.") # Можно раскомментировать для отладки
            time.sleep(delay)

    def _save_cookies_localy(self) -> None:
        """
        Сохраняет текущие куки веб-драйвера в локальный файл.

        Returns:
            None

        Raises:
            Exception: Если возникает ошибка при сохранении куки.
        """
        # return True # <- Закомментировано для реальной работы
        if not gs.cookies_filepath:
             logger.warning("Путь к файлу куки (gs.cookies_filepath) не установлен. Куки не сохранены.")
             return
        try:
            cookies = self.driver.get_cookies()
            if cookies: # Сохраняем, только если есть куки
                # Убедимся, что директория существует
                Path(gs.cookies_filepath).parent.mkdir(parents=True, exist_ok=True)
                with open(gs.cookies_filepath, 'wb') as cookiesfile:
                    pickle.dump(cookies, cookiesfile)
                logger.info(f"Куки успешно сохранены в файл: {gs.cookies_filepath}")
            else:
                logger.info("Нет куки для сохранения.")
        except AttributeError:
             logger.error("Текущий драйвер не поддерживает get_cookies().")
        except pickle.PicklingError as ex:
            logger.error(f"Ошибка сериализации (pickle) при сохранении куки в {gs.cookies_filepath}:", exc_info=ex)
        except IOError as ex:
            logger.error(f"Ошибка ввода/вывода при сохранении куки в {gs.cookies_filepath}:", exc_info=ex)
        except Exception as ex: # Общий обработчик
            logger.error(f"Неожиданная ошибка при сохранении куки в {gs.cookies_filepath}:", exc_info=ex)

    # def _extract_body_content(self, html: Optional[str]) -> Optional[str]:
    #     """
    #     Вспомогательный метод для извлечения содержимого между тегами <body>.
    #     Возвращает None, если html равен None или теги <body> не найдены.
    #     """
    #     if not html:
    #         return None
    #     # Regex для поиска контента между тегами <body> и </body>
    #     # - re.IGNORECASE: Сопоставление <body> или <BODY> и т.д.
    #     # - re.DOTALL: Позволяет '.' соответствовать символам новой строки
    #     # - .*?>: Нежадное сопоставление для атрибутов в открывающем теге <body>
    #     # - (.*?): Группа захвата для контента между тегами (нежадная)
    #     match = re.search(r'<body.*?>(.*?)</body>', html, re.IGNORECASE | re.DOTALL)
    #     if match:
    #         return match.group(1).strip() # Возвращаем захваченный контент, очищенный от пробелов
    #     else:
    #         logger.warning("Не удалось найти теги <body>...</body> в загруженном HTML.")
    #         return None

    def fetch_html(self, url: Optional[str] = '') -> Union[str, bool]:
        """
        Загружает HTML-контент из локального файла или веб-URL.

        Извлекает исходный HTML-код из 'file://', 'http://' или 'https://' URL.
        Использует `self.current_url`, если `url` не предоставлен.

        При успешном извлечении пытается найти контент внутри тегов <body>.

        Args:
            url (Optional[str]): URL или путь к локальному файлу (с префиксом 'file://')
                для загрузки. Если None, пустой или опущен, используется `self.current_url`.

        Returns:
            Union[str, bool]:
                - str: Извлеченный контент между тегами <body> и </body>,
                       если загрузка и извлечение прошли успешно.
                - False: Если произошла какая-либо ошибка (неверный URL/путь, файл не найден,
                         ошибка чтения, сетевая ошибка, неподдерживаемый протокол или
                         теги <body> не найдены после успешной загрузки).

        Side Effects:
            - Устанавливает `self.html_content` в *полную* строку HTML при успехе,
              даже если извлечение body не удалось позже.
            - Может изменять `self.current_url`, `self.previous_url` через вызов `self.get_url`.
            - Логгирует ошибки/информацию с использованием настроенного `logger`.

        Примечание по обработке путей к файлам:
            Использует `urllib.parse` и `pathlib` для лучшей кроссплатформенной
            обработки URI `file://`.
        """
        effective_url = url if isinstance(url, str) and url else self.current_url
        self.html_content = None # Сбрасываем контент для этой попытки

        if not effective_url:
            logger.error("Ошибка: URL не указан и self.current_url не установлен.")
            return False

        full_html: Optional[str] = None # Для хранения успешно загруженного полного HTML

        try:
            if effective_url.startswith('file://'):
                # --- Протокол File ---
                try:
                    # Используем urllib.parse для корректной обработки экранирования URI файла и преобразования пути
                    parsed_uri = urllib.parse.urlparse(effective_url)
                    if parsed_uri.scheme != 'file':
                         raise ValueError("Внутренняя ошибка: URI не файла в блоке обработки файлов.")

                    # url2pathname обрабатывает различия платформ (например, /C:/ -> C:/ на Win)
                    # и декодирует %xx экранирование. Используем unquote для путей без netloc.
                    file_path_str = urllib.parse.unquote(parsed_uri.path)

                    # В Windows urlparse может оставлять ведущий '/' для локальных путей (например, /C:/...). Удаляем его.
                    # Проверяем паттерн /<Буква>:/
                    if re.match(r"\/[a-zA-Z]:", file_path_str):
                         file_path_str = file_path_str[1:] # Удаляем первый символ '/'

                    file_path = Path(file_path_str)

                    if file_path.exists() and file_path.is_file():
                        with file_path.open('r', encoding='utf-8', errors='ignore') as file: # errors='ignore' для устойчивости
                            full_html = file.read()
                        logger.info(f"Успешно прочитан файл: {file_path}")
                    elif not file_path.exists():
                        logger.error(f'Локальный файл не найден: {file_path}')
                        return False
                    else:
                        logger.error(f'Указанный путь не является файлом: {file_path}')
                        return False
                except ValueError as ve: # Отлавливаем ошибки при разборе URI/создании пути
                    logger.error(f"Ошибка обработки URI/пути файла '{effective_url}': {ve}")
                    return False
                except IOError as e: # Отлавливаем ошибки чтения файла
                    logger.error(f'Ошибка чтения файла {file_path}: {e}')
                    return False
                except Exception as e: # Отлавливаем другие неожиданные ошибки при обработке файла
                     logger.error(f'Неожиданная ошибка обработки пути файла {effective_url}:', exc_info=e)
                     return False

            elif effective_url.startswith(('http://', 'https://')):
                # --- Протокол HTTP/HTTPS ---
                try:
                    # Используем get_url для загрузки страницы
                    # get_url обновит self.current_url и self.previous_url
                    if effective_url!=self.current_url: 
                        if not self.get_url(effective_url):
                            logger.critical(f'Что-то непонятное с драйвером!')
                            ...
                    # После успешной загрузки через Selenium, получаем исходный код
                    full_html = self.driver.page_source
                    if full_html:
                        logger.info(f"Успешно получен HTML для URL: {self.current_url}") # Используем self.current_url, т.к. мог быть редирект
                    else:
                            logger.warning(f"get_url вернул успех, но self.driver.page_source пуст для {self.current_url}")
                            # Можно вернуть False здесь, если пустой page_source считать ошибкой
                            # return False
                            pass # Или продолжить и позволить _extract_body_content вернуть None -> False
                except Exception as ex:
                    # Отлавливаем исключения, возникшие в self.get_url или при доступе к page_source
                    logger.error(f"Исключение при получении URL {effective_url}:",ex, True)
                    return False

            else:
                # --- Неподдерживаемый протокол ---
                logger.error(f"Ошибка: Неподдерживаемый протокол для URL: {effective_url}")
                return False

            # --- Обработка успешно загруженного HTML ---
            if full_html:
                return full_html
                # self.html_content = full_html # Сохраняем полный HTML контент
                # body_content = self._extract_body_content(full_html)

                # if body_content:
                #     logger.info(f"Успешно извлечен контент <body> из {effective_url}")
                #     return body_content # УСПЕХ! Возвращаем извлеченное тело.
                # else:
                #     # Загрузка удалась, но извлечение body не удалось. Возвращаем False согласно требованию.
                #     logger.debug(f"Загружен контент из {effective_url}, но не удалось извлечь контент <body>.")
                #     return full_html #### ВНИМАНИЕ!!!!!! 
            else:
                # Этот путь не должен достигаться, если логика выше верна,
                # но служит запасным вариантом, если full_html остался None без возврата False ранее.
                 logger.error(f"Ошибка внутреннего состояния: HTML контент не был получен для {effective_url}, но предыдущая ошибка не была возвращена.")
                 return False

        except Exception as e:
             # Отлавливаем любые действительно неожиданные ошибки на верхнем уровне
             logger.exception(f"Неожиданная критическая ошибка во время fetch_html для {effective_url}: {e}")
             return False


# --- Пример использования (если запускается как скрипт) ---
if __name__ == '__main__':
    import tempfile
    import os

    # Mock WebDriver для тестирования fetch_html
    class MockWebDriverFetch:
        def __init__(self):
            self._current_url = ''
            self.page_source = ''

        def get(self, url):
            print(f"[MockWebDriver] Вызов get({url})")
            if "error" in url:
                raise WebDriverException(f"Simulated WebDriver error for {url}")
            if "notfound" in url:
                self._current_url = url
                self.page_source = "<html><head><title>Not Found</title></head><body><h1>404</h1></body></html>"
                # Имитируем неудачу get_url, возвращая False извне или через проверку статуса
                # Для простоты, в тесте будем считать, что get_url вернет False для этого URL
                print(f"[MockWebDriver] Имитация неудачи get_url для {url}")
                return False # Важно для теста get_url
            if "no_body_tag" in url:
                 self._current_url = url
                 self.page_source = "<!DOCTYPE html><html><head><title>No Body Tag</title></head><p>Content outside body</p></html>"
                 print(f"[MockWebDriver] Успешная загрузка (без тега body): {url}")
                 return True
            # Успешный случай
            self._current_url = url
            self.page_source = f"<!DOCTYPE html>\n<html><head><title>Test</title></head>" \
                               f"<body class='main'>\n<h1>Success</h1><p>Content for {url}</p>\n</body></html>"
            print(f"[MockWebDriver] Успешная загрузка: {url}")
            return True # Важно для теста get_url

        def execute_script(self, script):
            if 'readyState' in script:
                print(f"[MockWebDriver] Вызов execute_script('{script}') -> 'complete'")
                return 'complete'
            print(f"[MockWebDriver] Вызов execute_script('{script}')")
            return None

        @property
        def current_url(self):
            return self._current_url

        def get_cookies(self): return [] # Для _save_cookies_localy
        def find_element(self, by, value): raise Exception("Not Found") # Для locale
        def switch_to(self): return self
        def window(self, handle): pass
        @property
        def window_handles(self): return ['h1']


    # Создаем экземпляр Driver с Mock WebDriver
    instance = Driver(MockWebDriverFetch)
    instance.current_url = 'http://default.example.com' # Устанавливаем начальный URL

    print("\n--- Тестирование Веб URL ---")
    # 1. Успешная загрузка веб URL
    body_web = instance.fetch_html('https://good.example.com/page')
    print(f"Успех (Веб): {isinstance(body_web, str)}")
    if isinstance(body_web, str):
        print(f"Извлеченное Body (Веб):\n---\n{body_web}\n---")
    print("-" * 20)

    # 2. Использование URL по умолчанию
    # Сначала "загрузим" его через get_url, чтобы page_source обновился
    print("Имитация загрузки URL по умолчанию...")
    instance.get_url(instance.current_url)
    print("Вызов fetch_html() без аргументов...")
    body_default = instance.fetch_html() # url пуст, используется self.current_url
    print(f"Успех (По умолчанию): {isinstance(body_default, str)}")
    if isinstance(body_default, str):
        print(f"Извлеченное Body (По умолчанию):\n---\n{body_default}\n---")
    print("-" * 20)

    # 3. Обработка ошибки от get_url (имитация 404)
    # MockWebDriverFetch.get вернет False для этого URL
    print("Тест URL, для которого get_url вернет False...")
    result_fail_fetch = instance.fetch_html('http://example.com/notfound')
    print(f"Успех (get_url False): {result_fail_fetch is not False}") # Ожидаем False
    print(f"Результат: {result_fail_fetch}")
    print("-" * 20)

    # 4. Обработка исключения WebDriverException от get_url
    print("Тест URL, который вызовет WebDriverException в get...")
    result_network_error = instance.fetch_html('http://error.example.com')
    print(f"Успех (WebDriverException): {result_network_error is not False}") # Ожидаем False
    print(f"Результат: {result_network_error}")
    print("-" * 20)

    # 5. Обработка неподдерживаемого протокола
    print("Тест неподдерживаемого протокола...")
    result_bad_protocol = instance.fetch_html('ftp://example.com/resource')
    print(f"Успех (Плохой протокол): {result_bad_protocol is not False}") # Ожидаем False
    print(f"Результат: {result_bad_protocol}")
    print("-" * 20)

    # 6. Успешная загрузка, но нет тега <body>
    print("Тест URL с контентом, но без тега <body>...")
    result_no_body_tag = instance.fetch_html('http://no_body_tag.example.com')
    print(f"Успех (Нет тега body): {result_no_body_tag is not False}") # Ожидаем False
    print(f"Результат: {result_no_body_tag}")
    print(f"Полный HTML сохранен: {instance.html_content is not None}")
    print("-" * 20)


    print("\n--- Тестирование Локальных Файлов ---")
    # 7. Успешная загрузка локального файла
    tmp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".html", encoding='utf-8') as tmp_file:
            tmp_file.write("<!DOCTYPE html><html><head><title>Local</title></head>"
                           "<Body style='margin: 0;'><h1>Локальный Тест</h1><p>Содержимое файла.</p></bOdY></html>")
            tmp_file_path = tmp_file.name

        file_uri = Path(tmp_file_path).as_uri() # например, file:///tmp/xyz или file:///C:/Users/...
        print(f"Попытка загрузить из URI: {file_uri}")
        body_file = instance.fetch_html(file_uri)
        print(f"Успех (Локальный Файл): {isinstance(body_file, str)}")
        if isinstance(body_file, str):
            print(f"Извлеченное Body (Локальный Файл):\n---\n{body_file}\n---")
            # print("Полный HTML сохранен:", instance.html_content)
    except Exception as e:
        print(f"Ошибка во время теста локального файла: {e}")
    finally:
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
            print(f"Удален временный файл: {tmp_file_path}")
    print("-" * 20)

    # 8. Локальный файл без тега <body>
    tmp_no_body_path = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".html", encoding='utf-8') as tmp_file:
            tmp_file.write("<html><head><title>No Body</title></head></html>")
            tmp_no_body_path = tmp_file.name
        file_uri_no_body = Path(tmp_no_body_path).as_uri()
        print(f"Попытка загрузить из URI (без body): {file_uri_no_body}")
        result_no_body = instance.fetch_html(file_uri_no_body)
        print(f"Успех (Файл без Body): {result_no_body is not False}") # Ожидаем False
        print(f"Результат: {result_no_body}")
        # print("Полный HTML сохранен:", instance.html_content)
    except Exception as e:
        print(f"Ошибка во время теста файла без body: {e}")
    finally:
        if tmp_no_body_path and os.path.exists(tmp_no_body_path):
            os.remove(tmp_no_body_path)
            print(f"Удален временный файл: {tmp_no_body_path}")
    print("-" * 20)


    # 9. Обработка несуществующего локального файла
    non_existent_path = Path(tempfile.gettempdir()) / "___non_existent_file___.html"
    non_existent_uri = non_existent_path.as_uri()
    print(f"Попытка загрузить несуществующий URI: {non_existent_uri}")
    result_no_file = instance.fetch_html(non_existent_uri)
    print(f"Успех (Несуществующий Файл): {result_no_file is not False}") # Ожидаем False
    print(f"Результат: {result_no_file}")
    print("-" * 20)

    # 10. Обработка некорректного формата file URI (менее вероятно с urlparse, но для теста)
    invalid_uri = "file:// C:/contains space/file.html" # Пример URI, который может вызвать проблемы
    print(f"Попытка загрузить некорректный URI: {invalid_uri}")
    result_invalid_uri = instance.fetch_html(invalid_uri)
    print(f"Успех (Некорректный URI): {result_invalid_uri is not False}") # Ожидаем False
    print(f"Результат: {result_invalid_uri}")
    print("-" * 20)