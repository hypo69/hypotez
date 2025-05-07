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

```rst
.. module:: src.webdriver.driver
```
"""

import copy
import pickle
import time
import re
from pathlib import Path
from typing import Optional, Union, Any
import urllib.parse # Добавлено для лучшей обработки file:// URI
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    InvalidArgumentException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
    ElementNotVisibleException,
    WebDriverException as SeleniumWebDriverException # Переименовано для ясности
)

import header # Если нужно раскомментировать
from src import gs # Если нужно раскомментировать

from src.logger.logger import logger
# Исключения ExecuteLocatorException, WebDriverException не используются в этом файле напрямую
# Оставлены, если они используются в других частях проекта, импортирующих этот модуль
from src.logger.exceptions import ExecuteLocatorException, WebDriverException 



class Driver:
    """
    Класс обеспечивает удобный интерфейс для работы с различными драйверами, такими как Chrome, Firefox и Edge.
    Обертывает экземпляр Selenium WebDriver, предоставляя дополнительные методы и управление состоянием.

    Attributes:
        driver (selenium.webdriver.remote.webdriver.WebDriver): Экземпляр Selenium WebDriver (или совместимый).
        current_url (str): Текущий URL, открытый в браузере. Инициализируется пустой строкой.
        html_content (Optional[str]): Полное HTML содержимое последней успешно загруженной страницы.
                                      Устанавливается методом `fetch_html`.
        previous_url (Optional[str]): URL, который был открыт до последнего успешного перехода.
                                      Инициализируется как None.
    """
    # Текущий URL, открытый в браузере
    current_url: str = ''
    # Полное HTML содержимое последней успешно загруженной страницы
    html_content: Optional[str] = None 
    # Предыдущий URL
    previous_url: Optional[str] = None 
    # Экземпляр WebDriver (аннотация типа для ясности)
    driver: SeleniumWebDriverException # Используем общее исключение Selenium, но лучше конкретный тип драйвера, если известен

    def __init__(self, webdriver_cls: type, *args: Any, **kwargs: Any) -> None: # webdriver_cls должен быть типом
        """
        Инициализирует экземпляр класса Driver, создавая экземпляр предоставленного WebDriver.

        Args:
            webdriver_cls (type): Класс WebDriver для инстанцирования (например, `selenium.webdriver.Chrome`).
            *args: Позиционные аргументы, передаваемые в конструктор `webdriver_cls`.
            **kwargs: Именованные аргументы, передаваемые в конструктор `webdriver_cls`.

        Raises:
            TypeError: Если `webdriver_cls` не является классом или не имеет необходимых атрибутов WebDriver.

        Example:
            >>> # Mock WebDriver class for example
            >>> class MockWebDriver:
            ...     def __init__(self, *args, **kwargs): self.page_source = ""
            ...     def get(self, url): self._current_url_prop = url; self.page_source = f"<html><body>Content for {url}</body></html>"
            ...     def execute_script(self, script): return 'complete' # Mock ready state
            ...     @property
            ...     def current_url(self): return getattr(self, '_current_url_prop', '') # Изменено на _current_url_prop
            ...     def get_cookies(self): return [{'name': 'session', 'value': '123'}]
            ...     def find_element(self, by, value): raise Exception("Not found")
            ...     def switch_to(self): return self 
            ...     def window(self, handle): pass 
            ...     @property
            ...     def window_handles(self): return ['handle1'] 
            >>> driver_instance = Driver(MockWebDriver) 
            >>> print(isinstance(driver_instance.driver, MockWebDriver))
            True
        """
        # Проверка, что webdriver_cls является классом и имеет метод 'get'
        if not isinstance(webdriver_cls, type) or not hasattr(webdriver_cls, 'get'): 
            raise TypeError('`webdriver_cls` должен быть допустимым классом WebDriver (например, selenium.webdriver.Chrome).')
        # Создание экземпляра WebDriver
        self.driver = webdriver_cls(*args, **kwargs)
        # Инициализация previous_url значением None
        self.previous_url: Optional[str] = None 

    def __init_subclass__(cls, *, browser_name: Optional[str] = None, **kwargs: Any) -> None:
        """
        Метод жизненного цикла Python, автоматически вызываемый при создании подкласса `Driver`.
        Используется для установки атрибута `browser_name` на уровне класса подкласса.

        Args:
            browser_name (Optional[str]): Имя браузера, которое должен указать подкласс.
            **kwargs (Any): Дополнительные именованные аргументы, передаваемые в `super().__init_subclass__`.

        Raises:
            ValueError: Если `browser_name` не указан при определении подкласса.
        """
        super().__init_subclass__(**kwargs)
        if browser_name is None:
            raise ValueError(f'Класс {cls.__name__} должен указать аргумент `browser_name` при наследовании от Driver.')
        # Установка имени браузера как атрибута класса
        cls.browser_name = browser_name

    def __getattr__(self, item: str) -> Any:
        """
        Магический метод для делегирования доступа к атрибутам.
        Если атрибут `item` не найден в экземпляре `Driver`, поиск передается
        вложенному объекту `self.driver` (экземпляру Selenium WebDriver).

        Args:
            item (str): Имя атрибута для доступа.

        Returns:
            Any: Значение запрошенного атрибута.

        Raises:
            AttributeError: Если атрибут не найден ни в `Driver`, ни во вложенном `self.driver`.

        Example:
            >>> class MockWebDriverAttr:
            ...     def __init__(self): self._url_prop = "http://example.com" # Изменено на _url_prop
            ...     @property
            ...     def current_url(self): return self._url_prop # Используем _url_prop
            ...     def get(self, url): pass 
            >>> driver_instance = Driver(MockWebDriverAttr)
            >>> print(driver_instance.current_url) # Доступ к driver.current_url через __getattr__
            http://example.com
        """
        # Сначала проверяем, есть ли атрибут у самого экземпляра Driver
        if item in self.__dict__:
            return self.__dict__[item]
        # Если нет, пытаемся получить его из вложенного self.driver
        try:
            return getattr(self.driver, item)
        except AttributeError:
            # Если атрибут не найден и там, генерируем стандартное исключение AttributeError
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}' and its 'driver' object ({type(self.driver).__name__}) also has no attribute '{item}'")


    def scroll(self, scrolls: int = 1, frame_size: int = 600, direction: str = 'both', delay: float = .3) -> bool:
        """
        Прокручивает текущую веб-страницу в указанном направлении.

        Args:
            scrolls (int): Количество отдельных прокруток для выполнения. По умолчанию 1.
            frame_size (int): Размер каждой прокрутки в пикселях. По умолчанию 600.
            direction (str): Направление прокрутки. Допустимые значения:
                             'down' или 'forward' (вниз),
                             'up' или 'backward' (вверх),
                             'both' (сначала вниз, затем вверх). По умолчанию 'both'.
            delay (float): Задержка в секундах между последовательными прокрутками. По умолчанию 0.3.

        Returns:
            bool: `True`, если все прокрутки в указанном направлении(ях) выполнены успешно, иначе `False`.

        Example:
            >>> class MockWebDriverScroll:
            ...     def get(self, url): pass
            ...     def execute_script(self, script): print(f"Executed: {script}"); return None
            >>> driver_instance = Driver(MockWebDriverScroll)
            >>> driver_instance.scroll(scrolls=1, direction='down') # doctest: +ELLIPSIS
            Executed: window.scrollBy(0,600)
            True
        """
        # Внутренняя вспомогательная функция для выполнения прокрутки
        def carousel(dir_sign: str = '', num_scrolls: int = 1, size: int = 600, scroll_delay: float = .3) -> bool:
            """ Локальный метод для выполнения серии прокруток в одном направлении. """
            try:
                for _ in range(num_scrolls):
                    # Выполнение JavaScript для прокрутки окна
                    self.driver.execute_script(f'window.scrollBy(0,{dir_sign}{size})')
                    # Использование метода self.wait для задержки
                    self.wait(scroll_delay)
                return True # Успешное выполнение
            except Exception as ex:
                # Логирование ошибки при прокрутке
                logger.error(f'Ошибка при прокрутке ({dir_sign or "down"}):', None, exc_info=ex)
                return False # Неудачное выполнение

        try:
            # Обработка различных направлений прокрутки
            if direction in ('forward', 'down'):
                return carousel('', scrolls, frame_size, delay)
            elif direction in ('backward', 'up'):
                return carousel('-', scrolls, frame_size, delay)
            elif direction == 'both':
                # Прокрутка вниз, затем вверх
                down_success: bool = carousel('', scrolls, frame_size, delay)
                # self.wait(delay) # Дополнительная задержка между "вниз" и "вверх" (опционально)
                up_success: bool = carousel('-', scrolls, frame_size, delay)
                return down_success and up_success # Успех, если оба направления успешны
            else:
                # Логирование предупреждения о неизвестном направлении
                logger.warning(f"Неизвестное направление прокрутки: {direction}")
                return False
        except Exception as ex:
            # Логирование неожиданной ошибки в основной функции scroll
            logger.error('Неожиданная ошибка в функции scroll:', None, exc_info=ex)
            return False


    @property
    def locale(self) -> Optional[str]:
        """
        Определяет язык (локаль) текущей веб-страницы.
        Пытается извлечь язык сначала из мета-тега 'Content-Language',
        затем из атрибутов `lang` тегов `<html>` или `<body>`,
        и наконец, из свойств JavaScript `navigator.language` или `navigator.userLanguage`.

        Returns:
            Optional[str]: Строка с кодом языка (например, 'en-US', 'fr'), если найден, иначе `None`.

        Example:
            >>> class MockWebDriverLocaleMeta:
            ...     def get(self, url): pass
            ...     def find_element(self, by, value):
            ...         if value == "meta[http-equiv='Content-Language']":
            ...             class MockElement:
            ...                 def get_attribute(self, name): return 'en-GB' if name == 'content' else None
            ...             return MockElement()
            ...         else: raise SeleniumWebDriverException("Meta not found") # Используем SeleniumWebDriverException
            ...     def execute_script(self, script): return 'fr-CA' 
            >>> driver_instance_meta = Driver(MockWebDriverLocaleMeta)
            >>> print(driver_instance_meta.locale)
            en-GB
            >>> class MockWebDriverLocaleJS:
            ...     def get(self, url): pass
            ...     def find_element(self, by, value): raise SeleniumWebDriverException("Meta not found")
            ...     def execute_script(self, script):
            ...         if 'document.documentElement.lang' in script: return 'de-DE'
            ...         return None 
            >>> driver_instance_js = Driver(MockWebDriverLocaleJS)
            >>> print(driver_instance_js.locale)
            de-DE
        """
        try:
             # Попытка найти мета-тег Content-Language
            meta_language_element = self.driver.find_element(By.CSS_SELECTOR, "meta[http-equiv='Content-Language']")
            lang_code: Optional[str] = meta_language_element.get_attribute('content')
            if lang_code: return lang_code
        except Exception: # Если мета-тег не найден или произошла другая ошибка
            logger.debug('Не удалось определить язык из META "Content-Language", попытка через JS.')
            pass # Продолжаем попытки другими способами

        try:
            # Попытка получить язык через JavaScript (атрибуты HTML, body, navigator)
            # Скрипт возвращает первое непустое значение из перечисленных свойств
            lang_code_js: Optional[str] = self.driver.execute_script(
                "return document.documentElement.lang || document.body.lang || navigator.language || navigator.userLanguage;"
            )
            if lang_code_js:
                return str(lang_code_js) # Возвращаем язык, если он найден через JS
            else:
                logger.debug('JavaScript не вернул информацию о языке.')
                return None # Если JS не вернул язык
        except Exception as ex_js:
            # Логирование предупреждения, если и через JS не удалось определить язык
            logger.warning('Не удалось определить язык сайта из JavaScript.', None, exc_info=ex_js)
            return None # Возвращаем None, если все попытки неудачны

    @property
    def ready_state(self) -> Optional[str]:
         """ 
         Возвращает состояние загрузки документа (`document.readyState`).
         Возможные значения: 'loading', 'interactive', 'complete'.

         Returns:
            Optional[str]: Строка с состоянием `document.readyState` или `None` в случае ошибки.
         """
         try:
             # Выполнение JavaScript для получения document.readyState
             return self.driver.execute_script('return document.readyState;')
         except Exception as ex:
              # Логирование ошибки, если не удалось получить readyState
              logger.error("Не удалось получить document.readyState:", None, exc_info=ex)
              return None

    def get_url(self, url: str) -> bool:
        """
        Переходит по указанному URL.
        Обновляет `self.current_url` и `self.previous_url`.
        Ожидает, пока `document.readyState` не станет 'complete' или 'interactive'.
        Сохраняет куки после успешного перехода (если логика `_save_cookies_localy` активна).

        Args:
            url (str): URL для навигации.

        Returns:
            bool: `True`, если переход успешен и страница загружена (readyState 'complete' или 'interactive'), 
                  `False` в противном случае (например, некорректный URL, ошибка WebDriver, таймаут загрузки).
        """
        # Сохранение текущего URL как предыдущего перед переходом
        _previous_url_local: str = copy.copy(self.current_url)

        try:
            logger.info(f"Переход на URL: {url}")
            # Выполнение перехода с помощью метода get драйвера
            self.driver.get(url)

            # Ожидание загрузки страницы (проверка readyState)
            attempts: int = 10 # Количество попыток проверки readyState
            loaded: bool = False # Флаг успешной загрузки
            while attempts > 0:
                state: Optional[str] = self.ready_state # Получение текущего readyState
                logger.debug(f"Попытка {11-attempts}/10: readyState={state} для {url}")
                # Проверка, достигла ли страница состояния 'complete' или 'interactive'
                if state in ('complete', 'interactive'):
                    loaded = True
                    logger.info(f"Страница загружена (readyState={state}): {url}")
                    break # Выход из цикла, если страница загружена
                attempts -= 1
                if attempts == 0:
                    # Логирование ошибки, если страница не загрузилась за все попытки
                    logger.error(f'Страница не достигла состояния "complete" или "interactive" за 10 попыток: {url}')
                    return False # Явный возврат False
                self.wait(0.5) # Короткая задержка между проверками

            # Обновление URL и сохранение куки только если загрузка прошла успешно
            if loaded:
                # Получение фактического URL после возможного редиректа
                actual_url_after_get: str = self.driver.current_url
                logger.info(f"Фактический URL после перехода: {actual_url_after_get}")
                self.current_url = actual_url_after_get # Обновление current_url

                # Обновление previous_url, если URL изменился
                if self.current_url != _previous_url_local:
                    self.previous_url = _previous_url_local
                    logger.debug(f"Предыдущий URL сохранен: {_previous_url_local}")

                # self._save_cookies_localy() # Раскомментировать для сохранения куки
                return True # Успешный переход и загрузка

        except InvalidArgumentException as ex_invalid_arg:
            # Обработка ошибки некорректного URL
            logger.error(f"Некорректный URL '{url}': {ex_invalid_arg}")
            return False
        except SeleniumWebDriverException as ex_webdriver: 
            # Обработка общих ошибок WebDriver
            logger.error(f'Ошибка WebDriver при переходе на {url}: {ex_webdriver}')
            return False
        except Exception as ex_other: 
            # Обработка любых других неожиданных ошибок
            logger.error(f'Неожиданная ошибка при переходе по URL: {url}', None, exc_info=ex_other)
            return False
        return False # Добавлено для случаев, когда loaded остается False, но исключения не было

    def window_open(self, url: Optional[str] = None) -> None:
        """
        Открывает новую вкладку в текущем окне браузера и переключается на нее.
        Если указан `url`, переходит по этому URL в новой вкладке.

        Args:
            url (Optional[str]): URL для открытия в новой вкладке. Если `None`, открывается пустая вкладка.
                                По умолчанию `None`.
        """
        logger.debug("Открытие новой вкладки.")
        # Выполнение JavaScript для открытия новой пустой вкладки
        self.driver.execute_script('window.open("");') 
        # Получение дескриптора последней открытой вкладки
        new_window_handle: str = self.driver.window_handles[-1]
        # Переключение на новую вкладку
        self.driver.switch_to.window(new_window_handle)
        logger.debug(f"Переключено на новую вкладку: {new_window_handle}")
        # Если URL предоставлен, переход по нему с использованием self.get_url
        if url:
            self.get_url(url) 

    def wait(self, delay: float = .3) -> None:
        """
        Приостанавливает выполнение на указанное количество времени.

        Args:
            delay (float): Время задержки в секундах. По умолчанию 0.3.
        """
        if delay > 0:
            # logger.debug(f"Ожидание {delay} сек.") # Можно раскомментировать для отладки
            time.sleep(delay) # Использование стандартной функции time.sleep

    def _save_cookies_localy(self) -> None:
        """
        Сохраняет текущие куки веб-драйвера в локальный файл с использованием `pickle`.
        Путь к файлу куки берется из `gs.cookies_filepath`.
        Если путь не установлен или возникают ошибки, куки не сохраняются и логируется соответствующее сообщение.
        """
        # Проверка, установлен ли путь к файлу куки
        if not hasattr(gs, 'cookies_filepath') or not gs.cookies_filepath: # Добавлена проверка hasattr
             logger.warning("Путь к файлу куки (gs.cookies_filepath) не установлен. Куки не сохранены.")
             return
        try:
            # Получение куки из драйвера
            cookies: list = self.driver.get_cookies()
            if cookies: # Сохранение, только если куки существуют
                # Гарантируем, что родительская директория для файла куки существует
                Path(gs.cookies_filepath).parent.mkdir(parents=True, exist_ok=True)
                # Открытие файла в бинарном режиме для записи (wb) и сохранение куки
                with open(gs.cookies_filepath, 'wb') as cookiesfile:
                    pickle.dump(cookies, cookiesfile)
                logger.info(f"Куки успешно сохранены в файл: {gs.cookies_filepath}")
            else:
                logger.info("Нет куки для сохранения.")
        except AttributeError:
             # Обработка случая, если драйвер не поддерживает get_cookies()
             logger.error("Текущий драйвер не поддерживает get_cookies().")
        except pickle.PicklingError as ex_pickle:
            # Обработка ошибок сериализации pickle
            logger.error(f"Ошибка сериализации (pickle) при сохранении куки в {gs.cookies_filepath}:", None, exc_info=ex_pickle)
        except IOError as ex_io:
            # Обработка ошибок ввода-вывода
            logger.error(f"Ошибка ввода/вывода при сохранении куки в {gs.cookies_filepath}:", None, exc_info=ex_io)
        except Exception as ex_other: 
            # Обработка других неожиданных ошибок
            logger.error(f"Неожиданная ошибка при сохранении куки в {gs.cookies_filepath}:", None, exc_info=ex_other)


    def fetch_html(self, url: Optional[str] = '') -> Union[str, bool]:
        """
        Загружает HTML-контент из локального файла (схема 'file://') или с веб-URL (схемы 'http://', 'https://').
        Если `url` не предоставлен, используется `self.current_url`.
        При успешной загрузке HTML-контента, он сохраняется в `self.html_content` и возвращается.

        Args:
            url (Optional[str]): URL (веб или file://) для загрузки. Если пустая строка или `None`,
                                 используется `self.current_url`. По умолчанию пустая строка.

        Returns:
            Union[str, bool]:
                - str: Полный HTML-контент страницы, если загрузка прошла успешно.
                - False: Если произошла ошибка (неверный URL/путь, файл не найден, ошибка чтения,
                         сетевая ошибка, неподдерживаемый протокол).

        Side Effects:
            - Устанавливает `self.html_content` в полную строку HTML при успехе.
            - Может изменять `self.current_url` и `self.previous_url` через вызов `self.get_url`
              при обработке веб-URL.
            - Логгирует информацию и ошибки с использованием `logger`.
        """
        # Определение эффективного URL для загрузки
        effective_url: str = url if isinstance(url, str) and url else self.current_url
        # Сброс html_content перед новой попыткой
        self.html_content = None 

        # Проверка, что URL для загрузки определен
        if not effective_url:
            logger.error("Ошибка fetch_html: URL не указан и self.current_url не установлен.")
            return False

        full_html_content: Optional[str] = None # Переменная для хранения загруженного HTML

        try:
            # Обработка локальных файлов (схема 'file://')
            if effective_url.startswith('file://'):
                try:
                    # Парсинг URI файла
                    parsed_uri: urllib.parse.ParseResult = urllib.parse.urlparse(effective_url)
                    if parsed_uri.scheme != 'file':
                         # Эта проверка здесь для полноты, хотя startswith уже проверил
                         raise ValueError("Внутренняя ошибка: URI не является file:// в блоке обработки файлов.")

                    # Преобразование URI в путь к файлу, учитывая особенности платформ и кодирование
                    file_path_str_decoded: str = urllib.parse.unquote(parsed_uri.path)
                    
                    # Удаление ведущего слеша для путей Windows (например, /C:/... -> C:/...)
                    if re.match(r"\/[a-zA-Z]:", file_path_str_decoded): # Паттерн для Windows путей
                         file_path_str_decoded = file_path_str_decoded[1:] 

                    file_path_obj: Path = Path(file_path_str_decoded) # Создание объекта Path

                    # Проверка существования и типа файла
                    if file_path_obj.exists() and file_path_obj.is_file():
                        # Чтение содержимого файла
                        with file_path_obj.open('r', encoding='utf-8', errors='ignore') as file_handle:
                            full_html_content = file_handle.read()
                        logger.info(f"Успешно прочитан файл: {file_path_obj}")
                    elif not file_path_obj.exists():
                        logger.error(f'Локальный файл не найден: {file_path_obj}')
                        return False
                    else: # Если путь существует, но это не файл (например, директория)
                        logger.error(f'Указанный путь не является файлом: {file_path_obj}')
                        return False
                except ValueError as ve_uri: 
                    # Обработка ошибок парсинга URI или создания пути
                    logger.error(f"Ошибка обработки URI/пути файла '{effective_url}': {ve_uri}")
                    return False
                except IOError as e_io_file: 
                    # Обработка ошибок чтения файла
                    logger.error(f'Ошибка чтения файла {file_path_obj}: {e_io_file}') # file_path_obj может быть не определен здесь
                    return False
                except Exception as e_file_other: 
                     # Обработка других неожиданных ошибок при работе с файлом
                     logger.error(f'Неожиданная ошибка обработки пути файла {effective_url}:', None, exc_info=e_file_other)
                     return False

            # Обработка веб-URL (схемы 'http://', 'https://')
            elif effective_url.startswith(('http://', 'https://')):
                try:
                    # Если запрашиваемый URL отличается от текущего, выполняем переход
                    # Это предотвращает ненужную перезагрузку, если URL уже открыт.
                    if effective_url != self.current_url: 
                        if not self.get_url(effective_url):
                            # Если get_url вернул False, значит произошла ошибка загрузки
                            logger.error(f'Ошибка при вызове get_url для {effective_url} внутри fetch_html.')
                            return False 
                    
                    # После успешного (или пропущенного) get_url, получаем исходный код страницы
                    full_html_content = self.driver.page_source
                    if full_html_content:
                        # self.current_url уже должен быть обновлен в get_url
                        logger.info(f"Успешно получен HTML для URL: {self.current_url}") 
                    else:
                        # Случай, когда get_url мог вернуть True, но page_source пуст (маловероятно, но возможно)
                        logger.warning(f"get_url вернул успех (или не вызывался), но self.driver.page_source пуст для {self.current_url}")
                        # Решение: возвращать False, если page_source пуст, даже если get_url был успешен
                        return False 
                except Exception as ex_http:
                    # Обработка исключений, возникших в self.get_url или при доступе к page_source
                    logger.error(f"Исключение при получении URL {effective_url} или его HTML:", ex_http, True)
                    return False

            else:
                # Обработка неподдерживаемых протоколов
                logger.error(f"Ошибка fetch_html: Неподдерживаемый протокол для URL: {effective_url}")
                return False

            # --- Завершение обработки: сохранение и возврат HTML ---
            if full_html_content is not None: # Проверяем, что full_html_content не None
                self.html_content = full_html_content # Сохранение полного HTML в атрибут класса
                return full_html_content # УСПЕХ! Возвращаем полный HTML.
            else:
                # Этот блок не должен достигаться, если логика выше корректна,
                # но служит дополнительной проверкой.
                 logger.error(f"Ошибка внутреннего состояния fetch_html: HTML контент не был получен для {effective_url}, но предыдущая ошибка не была обработана.")
                 return False

        except Exception as e_critical:
             # Отлов любых действительно неожиданных критических ошибок на верхнем уровне
             logger.exception(f"Неожиданная критическая ошибка во время fetch_html для {effective_url}: {e_critical}")
             return False


# --- Пример использования (если запускается как скрипт) ---
if __name__ == '__main__':
    import tempfile # Для создания временных файлов
    import os       # Для удаления временных файлов

    # Mock WebDriver для тестирования fetch_html
    class MockWebDriverFetch:
        def __init__(self):
            self._current_url_prop = '' # Изменено для избежания конфликта имен
            self.page_source_content = '' # Изменено для избежания конфликта имен

        def get(self, url_param: str) -> bool: # Изменено имя параметра
            print(f"[MockWebDriver] Вызов get({url_param})")
            if "error_in_get" in url_param: # Имитация ошибки непосредственно в get
                raise SeleniumWebDriverException(f"Имитация WebDriverException в get для {url_param}")
            if "notfound_page" in url_param: # Имитация страницы, которую get_url посчитает неудачной
                self._current_url_prop = url_param
                self.page_source_content = "<html><head><title>Not Found Page</title></head><body><h1>404 Not Found</h1></body></html>"
                print(f"[MockWebDriver] Имитация неудачной загрузки (например, readyState не complete) для {url_param}")
                # В реальном get_url, цикл проверки readyState завершился бы неудачей.
                # Здесь мы просто возвращаем False, чтобы имитировать это.
                return False 
            if "no_body_tag_page" in url_param: # Страница без тега body, но get_url успешен
                 self._current_url_prop = url_param
                 self.page_source_content = "<!DOCTYPE html><html><head><title>No Body Tag Page</title></head><p>Content outside body</p></html>"
                 print(f"[MockWebDriver] Успешная загрузка (без тега body): {url_param}")
                 return True # get_url успешен
            if "empty_page_source_page" in url_param: # get_url успешен, но page_source пуст
                self._current_url_prop = url_param
                self.page_source_content = "" # Пустой page_source
                print(f"[MockWebDriver] Успешная загрузка (но пустой page_source): {url_param}")
                return True # get_url успешен
            
            # Успешный случай для get
            self._current_url_prop = url_param
            self.page_source_content = f"<!DOCTYPE html>\n<html><head><title>Test Page</title></head>" \
                               f"<body class='main-body'>\n<h1>Success Title</h1><p>Content for {url_param}</p>\n</body></html>"
            print(f"[MockWebDriver] Успешная загрузка: {url_param}")
            return True 

        def execute_script(self, script_param: str) -> Optional[str]: # Изменено имя параметра
            if 'readyState' in script_param:
                # Имитируем различные readyState для тестирования get_url
                if "notfound_page" in self._current_url_prop: # Если URL содержит "notfound_page"
                    print(f"[MockWebDriver] execute_script('{script_param}') -> 'loading' (для {self._current_url_prop})")
                    return 'loading' # Имитируем, что страница все еще грузится
                print(f"[MockWebDriver] execute_script('{script_param}') -> 'complete' (для {self._current_url_prop})")
                return 'complete'
            print(f"[MockWebDriver] execute_script('{script_param}')")
            return None

        @property
        def current_url(self) -> str:
            return self._current_url_prop

        @property # Добавлено свойство page_source
        def page_source(self) -> str:
            return self.page_source_content

        # Другие мок-методы для полноты класса Driver
        def get_cookies(self): return [] 
        def find_element(self, by, value): raise SeleniumWebDriverException("Not Found in Mock") 
        def switch_to(self): return self
        def window(self, handle): pass
        @property
        def window_handles(self): return ['h1_mock']


    # Создаем экземпляр Driver с Mock WebDriver
    test_instance = Driver(MockWebDriverFetch)
    test_instance.current_url = 'http://default.example.com/initial' # Устанавливаем начальный URL

    print("\n--- Тестирование fetch_html с Веб URL ---")
    # 1. Успешная загрузка веб URL
    html_web_good = test_instance.fetch_html('https://good.example.com/webpage')
    print(f"Результат (Успех Веб): {type(html_web_good)}")
    if isinstance(html_web_good, str):
        print(f"Полученный HTML (Веб):\n---\n{html_web_good[:150]}...\n---") # Вывод части HTML
    print(f"Сохраненный html_content: {test_instance.html_content is not None}")
    print("-" * 30)

    # 2. Использование URL по умолчанию (self.current_url)
    # "Загрузим" URL по умолчанию, чтобы обновить page_source в моке
    print("Имитация загрузки URL по умолчанию через get_url...")
    test_instance.get_url(test_instance.current_url) # Это обновит page_source в моке
    print("Вызов fetch_html() без аргументов (использует self.current_url)...")
    html_default_url = test_instance.fetch_html() 
    print(f"Результат (URL по умолчанию): {type(html_default_url)}")
    if isinstance(html_default_url, str):
        print(f"Полученный HTML (URL по умолчанию):\n---\n{html_default_url[:150]}...\n---")
    print(f"Сохраненный html_content: {test_instance.html_content is not None}")
    print("-" * 30)

    # 3. Обработка ошибки от get_url (например, readyState не 'complete')
    print("Тест URL, для которого get_url вернет False (имитация 'notfound_page')...")
    result_get_url_false = test_instance.fetch_html('http://example.com/notfound_page')
    print(f"Результат (get_url False): {result_get_url_false}") 
    print(f"Тип результата: {type(result_get_url_false)}")
    print(f"Сохраненный html_content: {test_instance.html_content is None}") # Должен быть None
    print("-" * 30)

    # 4. Обработка исключения WebDriverException от get_url
    print("Тест URL, который вызовет WebDriverException в get ('error_in_get')...")
    result_webdriver_ex = test_instance.fetch_html('http://error_in_get.example.com')
    print(f"Результат (WebDriverException в get): {result_webdriver_ex}")
    print(f"Тип результата: {type(result_webdriver_ex)}")
    print(f"Сохраненный html_content: {test_instance.html_content is None}")
    print("-" * 30)

    # 5. Обработка неподдерживаемого протокола
    print("Тест URL с неподдерживаемым протоколом...")
    result_unsupported_protocol = test_instance.fetch_html('ftp://example.com/some_resource')
    print(f"Результат (Неподдерживаемый протокол): {result_unsupported_protocol}")
    print(f"Тип результата: {type(result_unsupported_protocol)}")
    print(f"Сохраненный html_content: {test_instance.html_content is None}")
    print("-" * 30)

    # 6. Успешная загрузка (get_url=True), но HTML без тега <body> (для fetch_html это не ошибка, вернет полный HTML)
    print("Тест URL с контентом, но без тега <body> (для fetch_html вернет полный HTML)...")
    html_no_body_tag = test_instance.fetch_html('http://no_body_tag_page.example.com')
    print(f"Результат (Нет тега body, но fetch_html успешен): {type(html_no_body_tag)}")
    if isinstance(html_no_body_tag, str):
        print(f"Полученный HTML (Нет тега body):\n---\n{html_no_body_tag[:150]}...\n---")
    print(f"Сохраненный html_content: {test_instance.html_content is not None}")
    print("-" * 30)
    
    # 6.1 Успешная загрузка (get_url=True), но page_source пуст
    print("Тест URL с успешным get_url, но пустым page_source...")
    result_empty_source = test_instance.fetch_html('http://empty_page_source_page.example.com')
    print(f"Результат (Пустой page_source): {result_empty_source}")
    print(f"Тип результата: {type(result_empty_source)}")
    print(f"Сохраненный html_content: {test_instance.html_content is None}") # Должен быть None, если page_source пуст
    print("-" * 30)


    print("\n--- Тестирование fetch_html с Локальными Файлами ---")
    # 7. Успешная загрузка локального файла с тегом body
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

    # 8. Локальный файл без тега <body> (fetch_html вернет полный HTML)
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


    # 9. Обработка несуществующего локального файла
    non_existent_file_path = Path(tempfile.gettempdir()) / "___this_file_does_not_exist___.html"
    non_existent_file_uri = non_existent_file_path.as_uri()
    print(f"Попытка загрузить несуществующий URI локального файла: {non_existent_file_uri}")
    result_non_existent_file = test_instance.fetch_html(non_existent_file_uri)
    print(f"Результат (Несуществующий Локальный Файл): {result_non_existent_file}")
    print(f"Тип результата: {type(result_non_existent_file)}")
    print(f"Сохраненный html_content: {test_instance.html_content is None}")
    print("-" * 30)

    # 10. Обработка некорректного формата file URI
    # (urllib.parse должен справляться с пробелами, но тестируем для полноты)
    # В Windows, путь C:\Temp\file with space.html будет file:///C:/Temp/file%20with%20space.html
    # Создадим файл с пробелом в имени для теста
    temp_file_with_space_path = None
    try:
        # Создание временного файла с пробелом в имени
        temp_dir = Path(tempfile.gettempdir())
        filename_with_space = "test file with space.html"
        temp_file_with_space_path = temp_dir / filename_with_space
        with open(temp_file_with_space_path, 'w', encoding='utf-8') as f_space:
            f_space.write("<html><body>Space Test</body></html>")
        
        # URI с пробелом (неправильно сформированный вручную)
        # Правильный URI был бы с %20. urlparse и Path().as_uri() это делают.
        # Но мы тестируем, как fetch_html справится с "сырым" путем, если он как-то попадет.
        # Однако, Path().as_uri() всегда вернет корректный URI.
        # Поэтому, для теста некорректного URI, мы его "сломаем" после Path().as_uri()
        # или передадим строку, которую Path() может неправильно интерпретировать.

        # Сначала протестируем с корректно сформированным URI через Path().as_uri()
        correct_uri_with_space = temp_file_with_space_path.as_uri()
        print(f"Попытка загрузить URI с пробелом (сформирован Path.as_uri()): {correct_uri_with_space}")
        html_space_correct = test_instance.fetch_html(correct_uri_with_space)
        print(f"Результат (URI с пробелом, корректный): {type(html_space_correct)}")
        if isinstance(html_space_correct, str):
             print(f"HTML (URI с пробелом, корректный):\n---\n{html_space_correct[:100]}...\n---")
        print(f"Сохраненный html_content: {test_instance.html_content is not None}")
        print("-" * 15)
        
        # Теперь симулируем "некорректный" URI, который может прийти извне
        # Хотя unquote в fetch_html должен справиться с %20, если URI все же пришел с ним.
        # Для настоящего теста "некорректного URI, который не парсится", нужно что-то вроде "file://\\invalid"
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
