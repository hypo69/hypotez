## \file src/webdriver/llm_driver/controllers.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль контроллеров для управления веб-браузером и обработки контента.
=======================================================================
Предоставляет классы для низкоуровневого управления браузером (BrowserController),
извлечения структурированных данных (DataExtractionController), работы с формами (FormController),
управления загрузками (DownloadController), создания скриншотов (ScreenshotController),
выполнения JavaScript (JavaScriptExecutionController) и управления сессией (StateManager).
Эти контроллеры используют **асинхронное** API Playwright и предназначены для
создания инструментов в асинхронных агентах LangChain.

```rst
.. module:: src.webdriver.llm_driver.controllers
```
"""

# Стандартные библиотеки
import json
import re # Для извлечения контактов
import asyncio # Для async sleep и управления циклом
import time # Может быть удален или использован для редких синхронных пауз
from pathlib import Path
from types import SimpleNamespace # Может не использоваться здесь
from typing import (Any, AsyncIterator, Callable, Dict, List, Optional, Tuple, # pylint: disable=unused-import
                    Type, Union, TypeAlias, Coroutine) # Добавлен Coroutine
from urllib.parse import urljoin # Для обработки относительных ссылок

# === Playwright Async Imports ===
# Импорт асинхронных компонентов Playwright
from playwright.async_api import (async_playwright, Page, Browser, Playwright, # ИСПОЛЬЗУЕМ ASYNC API
                                  BrowserContext, Error as PlaywrightError, Download) # Добавлены Download, BrowserContext
# ================================

# === Data Extraction Imports ===
# Попытка импорта BeautifulSoup для извлечения данных
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE: bool = True # Флаг доступности BeautifulSoup
except ImportError:
    BS4_AVAILABLE = False # Флаг недоступности BeautifulSoup
# ==========================

# === Internal/Project Imports ===
import header # pylint: disable=unused-import # Импортируется для сайд-эффектов (sys.path)
# Импорт __root__ для корректных относительных путей проекта
from header import __root__
# from src import gs # gs может быть не нужен в этом конкретном файле
from src.logger import logger # Импортируем настроенный логгер проекта
# ===============================

# Определяем псевдонимы типов для Async API Playwright для улучшения читаемости
ContextPage: TypeAlias = Optional[Page]
ContextBrowser: TypeAlias = Optional[Browser]
ContextPlaywright: TypeAlias = Optional[Playwright]
ContextBrowserContext: TypeAlias = Optional[BrowserContext]


# === BrowserController Class Definition (Async Version) ===
class BrowserController:
    """
    Управляет экземпляром браузера с использованием **асинхронного** API Playwright
    для навигации, извлечения данных и кликов по элементам.
    """
    # Атрибуты класса с аннотациями типов
    playwright: ContextPlaywright = None # Экземпляр Playwright
    browser: ContextBrowser = None       # Экземпляр браузера
    page: ContextPage = None             # Текущая активная страница
    context: ContextBrowserContext = None # Контекст браузера (для изоляции сессий)
    headless: bool                       # Флаг запуска браузера в безголовом режиме
    default_timeout: int                 # Таймаут по умолчанию для операций
    _is_started: bool = False            # Флаг для отслеживания асинхронной инициализации

    def __init__(self, headless: bool = True, timeout: int = 30000) -> None:
        """
        Синхронно инициализирует контроллер, сохраняя параметры.
        Асинхронный запуск Playwright и браузера выполняется методом `start()`.

        Args:
            headless (bool): Запускать браузер в headless-режиме (без UI). По умолчанию True.
            timeout (int): Таймаут по умолчанию для навигации/действий в миллисекундах. По умолчанию 30000 (30с).
        """
        # Инициализация атрибутов экземпляра
        self.playwright = None
        self.browser = None
        self.page = None
        self.context = None
        self.headless = headless
        self.default_timeout = timeout
        self._is_started = False # Установка начального состояния "не запущен"
        logger.info(f'BrowserController создан (Headless={self.headless}, Timeout={self.default_timeout}ms). Вызовите start() для инициализации.')

    async def start(self) -> bool:
        """
        Асинхронно инициализирует Playwright, запускает браузер и создает страницу.
        Должен быть вызван с `await` перед использованием других методов.

        Returns:
            bool: True, если инициализация прошла успешно, иначе False.

        Raises:
            RuntimeError: Если не удается инициализировать Playwright или браузер (в текущей реализации возвращает False).

        Example:
            >>> controller = BrowserController()
            >>> if await controller.start():
            ...    # Работа с контроллером
            ...    await controller.close()
        """
        # Проверка, не был ли контроллер уже запущен
        if self._is_started:
            logger.warning('BrowserController уже инициализирован.')
            return True # Если уже запущен, возвращаем True

        logger.info('Асинхронная инициализация BrowserController...')
        try:
            # Асинхронный запуск Playwright
            self.playwright = await async_playwright().start()
            # Асинхронный запуск браузера (Chromium по умолчанию)
            self.browser = await self.playwright.chromium.launch(headless=self.headless)
            # Асинхронное создание нового контекста браузера
            self.context = await self.browser.new_context()
            # Асинхронное создание новой страницы в контексте
            self.page = await self.context.new_page()
            # Установка таймаута по умолчанию для страницы
            if self.page: # Добавлена проверка, что page не None
                self.page.set_default_timeout(self.default_timeout)
            # Установка флага успешного запуска
            self._is_started = True
            logger.info('Playwright запущен, браузер открыт, контекст и страница созданы (Async).')
            return True
        except Exception as ex:
            # Логирование критической ошибки при инициализации
            logger.error('КРИТИЧЕСКАЯ ОШИБКА Async: Не удалось инициализировать Playwright/Браузер.', ex, exc_info=True)
            # Попытка асинхронного закрытия ресурсов при ошибке
            await self.close()
            # Возвращаем False вместо исключения, чтобы основной код мог это обработать
            return False

    async def navigate(self, url: str) -> str:
        """
        Асинхронно переводит страницу браузера на указанный URL.

        Args:
            url (str): URL для навигации.

        Returns:
            str: Статусное сообщение об успехе или ошибке навигации.

        Example:
            >>> status = await controller.navigate('https://example.com')
            >>> print(status)
            Успешный переход на https://example.com. Заголовок: Example Domain. Начало текста: This domain is for use in illustrative examples in documents...
        """
        # Проверка инициализации контроллера и состояния страницы
        if not self._is_started or not self.page or self.page.is_closed():
             logger.error('Ошибка навигации: Контроллер не инициализирован или страница закрыта.')
             return 'Ошибка: Контроллер/страница не инициализированы или закрыты.'

        logger.info(f'Переход на: {url}')
        try:
            # Асинхронный переход на URL, ожидание загрузки DOM
            response = await self.page.goto(url, wait_until='domcontentloaded')
            # Проверка успешности ответа сервера
            if response and response.ok:
                title: str = await self.page.title() # Асинхронное получение заголовка страницы
                logger.info(f"Успешный переход на {url}. Статус: {response.status}. Заголовок: '{title[:100]}'")
                try:
                    # Асинхронное получение текстового содержимого body для предпросмотра
                    body_text: str = await self.page.locator('body').inner_text(timeout=5000) # Таймаут для извлечения текста
                    return f'Успешный переход на {url}. Заголовок: {title}. Начало текста: {body_text[:200]}...'
                except Exception as text_ex:
                    # Логирование предупреждения, если не удалось быстро получить текст
                    logger.warning(f'Не удалось быстро получить текст после навигации на {url}.', text_ex, exc_info=False)
                    return f'Успешный переход на {url}. Заголовок: {title}. (Текст не получен)'
            else:
                # Обработка неуспешного ответа
                status_code: Union[int, str] = response.status if response else 'N/A'
                logger.warning(f'Ошибка навигации для {url}. Статус: {status_code}')
                return f'Не удалось перейти на {url}. Статус: {status_code}'
        except PlaywrightError as ex:
            # Обработка ошибок Playwright
            error_msg: str = ex.message.splitlines()[0] # Извлечение первой строки сообщения об ошибке
            logger.error(f'Ошибка Playwright при переходе на {url}: {error_msg}', None, exc_info=False)
            return f'Ошибка навигации на {url}: {error_msg}'
        except Exception as ex:
            # Обработка других неожиданных ошибок
            logger.error(f'Неожиданная ошибка при переходе на {url}.', ex, exc_info=True)
            return f'Неожиданная ошибка навигации на {url}: {str(ex)}'

    async def scrape_text(self, selector: Optional[str] = None) -> str:
        """
        Асинхронно извлекает текстовое содержимое с текущей страницы.
        Если указан селектор, извлекает текст из элементов, соответствующих селектору.
        В противном случае извлекает текст всего тега `<body>`.

        Args:
            selector (Optional[str]): CSS селектор. Если None, извлекает текст всего body. По умолчанию None.

        Returns:
            str: Извлеченный и очищенный текст или сообщение об ошибке.

        Example:
            >>> text_all = await controller.scrape_text()
            >>> heading_text = await controller.scrape_text('h1.main-title')
        """
        # Проверка инициализации и состояния страницы
        if not self._is_started or not self.page or self.page.is_closed():
             logger.error('Ошибка извлечения текста: Контроллер не инициализирован или страница закрыта.')
             return 'Ошибка: Контроллер/страница не инициализированы или закрыты.'

        action_description: str = f'Извлечение текста (Селектор: {selector})' if selector else 'Извлечение текста (Body)'
        logger.info(action_description)
        content_raw: str = '' # Сырое извлеченное содержимое
        cleaned_content: str = '' # Очищенное содержимое
        try:
            if selector:
                # Работа с указанным селектором
                elements = self.page.locator(selector)
                count: int = await elements.count() # Асинхронное получение количества найденных элементов
                if count == 0:
                    logger.warning(f"Элементы не найдены для селектора: '{selector}'")
                    return f"Элементы не найдены для селектора: {selector}"
                # Асинхронное получение текстов всех найденных элементов
                all_texts: List[str] = await elements.all_inner_texts()
                # Объединение текстов, удаление лишних пробелов
                content_raw = '\n\n'.join(t.strip() for t in all_texts if t.strip())
                logger.info(f'Извлечен текст из {count} элемент(ов) по селектору "{selector}". Длина: {len(content_raw)}')
            else:
                # Извлечение текста всего body
                content_raw = await self.page.locator('body').inner_text()
                logger.info(f'Извлечен текст из body. Длина: {len(content_raw)}')

            # Очистка извлеченного текста: удаление пустых строк и лишних пробелов в каждой строке
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
        """
        Асинхронно извлекает HTML содержимое с текущей страницы или указанного элемента.

        Args:
            selector (Optional[str]): CSS селектор элемента. Если None, извлекает HTML всей страницы. По умолчанию None.

        Returns:
            str: Строка с HTML содержимым или сообщение об ошибке.

        Example:
            >>> page_html = await controller.scrape_html()
            >>> element_html = await controller.scrape_html('#unique-element')
        """
        # Проверка инициализации и состояния страницы
        if not self._is_started or not self.page or self.page.is_closed():
             logger.error('Ошибка извлечения HTML: Контроллер не инициализирован или страница закрыта.')
             return 'Ошибка: Контроллер/страница не инициализированы или закрыты.'

        action_description: str = f'Извлечение HTML (Селектор: {selector})' if selector else 'Извлечение HTML (Body)'
        logger.info(action_description)
        html_content: str = ''
        try:
            if selector:
                 # Асинхронное выполнение JavaScript для получения outerHTML первого элемента по селектору
                 html_content = await self.page.locator(selector).first.evaluate('element => element.outerHTML', timeout=10000)
            else:
                 # Асинхронное получение HTML-контента всей страницы
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
        """
        Асинхронно кликает по первому видимому элементу, соответствующему CSS селектору.

        Args:
            selector (str): CSS селектор элемента для клика.

        Returns:
            str: Статусное сообщение об успехе или ошибке клика.

        Example:
            >>> status = await controller.click_element('button#submit-form')
        """
        # Проверка инициализации и состояния страницы
        if not self._is_started or not self.page or self.page.is_closed():
             logger.error('Ошибка клика: Контроллер не инициализирован или страница закрыта.')
             return 'Ошибка: Контроллер/страница не инициализированы или закрыты.'
        # Проверка наличия селектора
        if not selector:
            logger.warning('Ошибка клика: Не предоставлен селектор.')
            return 'Ошибка: Не указан селектор для клика.'

        logger.info(f"Попытка клика по элементу с селектором: '{selector}'")
        try:
            element_locator = self.page.locator(selector)
            count: int = await element_locator.count() # Асинхронное получение количества элементов
            if count == 0:
                logger.warning(f"Не удалось кликнуть: Элемент не найден по селектору '{selector}'")
                return f"Ошибка: Элемент не найден по селектору '{selector}'"
            if count > 1:
                # Предупреждение, если найдено несколько элементов (будет выбран первый)
                logger.warning(f"Найдено несколько элементов ({count}) по селектору '{selector}'. Клик по первому видимому.")

            # Асинхронное ожидание видимости первого элемента
            await element_locator.first.wait_for(state='visible', timeout=self.default_timeout // 3) # Таймаут для ожидания
            # Асинхронный клик по первому элементу
            await element_locator.first.click(timeout=self.default_timeout // 3) # Таймаут для клика
            logger.info(f"Успешный клик по первому элементу с селектором: '{selector}'")
            return f"Успешный клик по элементу: {selector}"
        except PlaywrightError as ex:
            error_msg: str = ex.message.splitlines()[0]
            logger.error(f"Ошибка Playwright при клике по '{selector}': {error_msg}", None, exc_info=False)
            # Специальная обработка ошибки таймаута
            if 'Timeout' in error_msg:
                 return f"Ошибка (таймаут) при клике/ожидании элемента '{selector}'. Возможно, он не появился или не кликабелен."
            return f"Ошибка клика по '{selector}': {error_msg}"
        except Exception as ex:
            logger.error(f"Неожиданная ошибка при клике по '{selector}'.", ex, exc_info=True)
            return f"Неожиданная ошибка клика по '{selector}': {str(ex)}"

    def get_current_url(self) -> str:
        """
        Синхронно возвращает текущий URL страницы.
        Получение URL является свойством объекта `page` и не требует асинхронности.

        Returns:
            str: Строка с текущим URL или сообщение об ошибке, если страница/контроллер не готовы.
        """
        if not self._is_started or not self.page or self.page.is_closed():
            logger.error('Ошибка получения URL: Контроллер не инициализирован или страница закрыта.')
            return 'Ошибка: Контроллер/страница не инициализированы или закрыты.'
        return self.page.url # Доступ к свойству page.url

    async def close(self) -> None:
        """
        Асинхронно закрывает страницу, контекст, браузер и останавливает Playwright.
        Освобождает все связанные ресурсы в правильном порядке.

        Example:
            >>> await controller.close()
        """
        logger.info('Асинхронное закрытие BrowserController...')
        # Закрытие ресурсов в обратном порядке их создания для предотвращения ошибок
        if self.page and not self.page.is_closed():
            try: await self.page.close(); logger.debug('Страница закрыта (Async).')
            except Exception as ex: logger.warning('Ошибка при закрытии страницы (Async).', ex, exc_info=False)
        self.page = None # Обнуление ссылки

        if self.context: # Playwright Context не имеет метода is_closed() как такового, проверяем просто наличие
             try: await self.context.close(); logger.debug('Контекст закрыт (Async).')
             except Exception as ex: logger.warning('Ошибка при закрытии контекста (Async).', ex, exc_info=False)
        self.context = None # Обнуление ссылки

        if self.browser and self.browser.is_connected():
            try: await self.browser.close(); logger.debug('Браузер закрыт (Async).')
            except Exception as ex: logger.warning('Ошибка при закрытии браузера (Async).', ex, exc_info=False)
        self.browser = None # Обнуление ссылки
        
        # Playwright.stop() является синхронным и предназначен для остановки процесса Playwright,
        # обычно не требуется вызывать его явно при каждом закрытии браузера, если приложение продолжает работать.
        # Playwright сам управляет своим жизненным циклом.
        # if self.playwright:
        # logger.debug('Playwright объект существует, stop() не вызывается в async close.')
        self.playwright = None # Обнуление ссылки

        self._is_started = False # Сброс флага инициализации
        logger.info('Ресурсы BrowserController освобождены (Async).')

# =============================================================

# === DataExtractionController Class Definition ===
class DataExtractionController:
    """
    Извлекает структурированную информацию из HTML или текста (синхронно).
    Методы этого класса не требуют `await`, так как работают с уже полученными данными (строками).
    """
    def __init__(self) -> None:
        """ 
        Инициализирует контроллер и проверяет доступность библиотеки BeautifulSoup.
        """
        if not BS4_AVAILABLE:
            # Предупреждение, если BeautifulSoup не доступен
            logger.warning('Библиотека BeautifulSoup4 не найдена. Функции DataExtractionController будут ограничены.')
        logger.debug('DataExtractionController инициализирован.')

    # Методы extract_product_details, extract_contact_info, find_links
    # остаются СИНХРОННЫМИ, так как они обрабатывают строки HTML/текста в памяти.
    def extract_product_details(self, html_content: str) -> Dict[str, Any]:
        """ 
        Извлекает данные о товаре из предоставленного HTML-контента (реализация-плейсхолдер). 
        Для полноценной работы требует наличия BeautifulSoup.
        """
        # Переменные для хранения данных и объектов парсинга
        extracted_data: Dict[str, Any]
        soup: BeautifulSoup
        title_tag: Optional[Any] # Тип зависит от BeautifulSoup

        logger.info(f'Попытка извлечения данных о товаре (Длина HTML: {len(html_content)})...')
        # Проверка доступности BeautifulSoup
        if not BS4_AVAILABLE: return {'error': 'BeautifulSoup4 not available'}
        # Проверка валидности входного HTML
        if not html_content or not isinstance(html_content, str): return {'error': 'Invalid HTML content provided'}
        
        # Инициализация словаря для извлеченных данных с значениями по умолчанию
        extracted_data = {
            'product_name': 'not found', 'url': 'not found', 'product_sku': 'not found', 
            'category_name': 'not found', 'parent_category': 'not found', 
            'brand_name': 'not found', 'brand_url': 'not found', 'product_image': 'not found', 
            'product_price': 'not found', 'product_description': 'not found', 
            'specifications': 'not found', 'product_params': {}, 
            'available_for_order': 'unknown', 'condition': 'not found'
        }
        try:
            # Парсинг HTML с использованием lxml (быстрый парсер)
            soup = BeautifulSoup(html_content, 'lxml')
            # Пример: извлечение названия товара из тега <h1>
            title_tag = soup.find('h1')
            if title_tag: extracted_data['product_name'] = title_tag.get_text(strip=True)
            # --- ДРУГИЕ ПРАВИЛА ИЗВЛЕЧЕНИЯ МОГУТ БЫТЬ ДОБАВЛЕНЫ ЗДЕСЬ ---
            # Например, поиск цены, описания, SKU и т.д. по специфичным селекторам.
            logger.warning('Извлечение данных о товаре ЗАВЕРШЕНО (базовая логика). Для реальных данных нужны специфичные парсеры.')
            return extracted_data
        except Exception as ex: 
            # Логирование ошибки при извлечении
            logger.error('Ошибка при извлечении данных о товаре.', ex, exc_info=True)
            return {'error': f'Extraction failed: {str(ex)}'}

    def extract_contact_info(self, text_content: str) -> Dict[str, List[str]]:
        """ 
        Извлекает email-адреса и телефонные номера из предоставленного текстового контента.
        Использует регулярные выражения для поиска.
        """
        # Инициализация словаря для хранения контактов
        contacts: Dict[str, List[str]] = {'emails': [], 'phones': []}
        # Паттерны регулярных выражений для email и телефонов
        email_pattern: str
        phone_pattern: str
        logger.info(f'Попытка извлечения контактов (Длина текста: {len(text_content)})...')
        # Проверка валидности входного текста
        if not text_content or not isinstance(text_content, str): return {'error': 'Invalid text content provided'}
        
        # Паттерн для email-адресов
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        # Паттерн для телефонных номеров (упрощенный, может требовать доработки для разных форматов)
        phone_pattern = r'\(?\+?\d{1,4}?\)?[-\s\.]?\(?\d{1,4}?\)?[\d\s\.-]{7,}'
        try:
            # Поиск всех email и телефонов, удаление дубликатов и сортировка
            contacts['emails'] = sorted(list(set(re.findall(email_pattern, text_content))))
            contacts['phones'] = sorted(list(set(re.findall(phone_pattern, text_content))))
            logger.info(f"Найдено контактов: Emails={len(contacts['emails'])}, Phones={len(contacts['phones'])}")
            return contacts
        except Exception as ex: 
            # Логирование ошибки при извлечении
            logger.error('Ошибка при извлечении контактов.', ex, exc_info=True)
            return {'error': f'Contact extraction failed: {str(ex)}'}

    def find_links(self, html_content: str, base_url: Optional[str] = None) -> Union[List[str], Dict[str, str]]:
        """ 
        Находит все уникальные ссылки (теги `<a>` с атрибутом `href`) в HTML-контенте.
        Относительные ссылки преобразуются в абсолютные, если предоставлен `base_url`.
        """
        # Инициализация списка для хранения ссылок
        links: List[str] = []
        soup: BeautifulSoup
        a_tag: Any # Тип зависит от BeautifulSoup
        href: str
        absolute_url: str
        unique_links: List[str]
        logger.info(f'Поиск ссылок (Длина HTML: {len(html_content)})...')
        # Проверка доступности BeautifulSoup
        if not BS4_AVAILABLE: return {'error': 'BeautifulSoup4 not available'}
        # Проверка валидности входного HTML
        if not html_content or not isinstance(html_content, str): return {'error': 'Invalid HTML content provided'}
        try:
            # Парсинг HTML
            soup = BeautifulSoup(html_content, 'lxml')
            # Поиск всех тегов <a> с атрибутом href
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href'].strip() # Получение значения href и удаление пробелов
                # Фильтрация пустых ссылок, якорных ссылок и javascript-ссылок
                if href and not href.startswith('#') and not href.startswith('javascript:'):
                     # Преобразование относительных URL в абсолютные, если есть base_url
                     if base_url and not href.startswith(('http://', 'https://', '//')):
                         try: 
                             absolute_url = urljoin(base_url, href)
                             links.append(absolute_url)
                         except Exception as url_ex: 
                             # Логирование ошибки преобразования URL
                             logger.warning(f'Не удалось сделать URL абсолютным: {href} (base: {base_url}).', url_ex, exc_info=False)
                             links.append(href) # Добавление как есть при ошибке
                     else:
                         links.append(href) # Добавление абсолютных или протокол-относительных ссылок
            # Удаление дубликатов и сортировка
            unique_links = sorted(list(set(links)))
            logger.info(f'Найдено {len(unique_links)} уникальных ссылок.')
            return unique_links
        except Exception as ex: 
            # Логирование ошибки при поиске ссылок
            logger.error('Ошибка при поиске ссылок.', ex, exc_info=True)
            return {'error': f'Link extraction failed: {str(ex)}'}

# =============================================================

# === FormController Class Definition (Async Version) ===
class FormController:
    """ 
    Управляет заполнением и отправкой HTML-форм на странице с использованием
    асинхронного API Playwright.
    """
    page: Page # Активная страница Playwright
    def __init__(self, page: Page) -> None:
        """
        Инициализирует FormController.

        Args:
            page (Page): Активный объект страницы Playwright.

        Raises:
            ValueError: Если `page` не предоставлена или закрыта.
        """
        if not page or page.is_closed(): 
            raise ValueError('FormController требует активный объект страницы Playwright.')
        self.page = page
        logger.debug('FormController инициализирован.')

    async def fill_input_field(self, selector: str, value: str) -> str:
        """ 
        Асинхронно находит поле ввода по селектору и вводит в него указанное значение.

        Args:
            selector (str): CSS селектор поля ввода.
            value (str): Значение для ввода в поле.

        Returns:
            str: Статусное сообщение об успехе или ошибке.
        """
        field: Any # Playwright Locator
        logger.info(f"Заполнение поля '{selector}' значением '{value[:20]}...'")
        # Проверка состояния страницы
        if not self.page or self.page.is_closed(): return 'Ошибка: Страница закрыта.'
        try:
            # Получение первого элемента по селектору
            field = self.page.locator(selector).first
            # Ожидание видимости элемента
            await field.wait_for(state='visible', timeout=10000)
            # Заполнение поля
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
        """ 
        Асинхронно выбирает опцию в выпадающем списке по значению (`value`) или тексту (`label`).

        Args:
            selector (str): CSS селектор выпадающего списка.
            value (Optional[str]): Значение опции для выбора.
            label (Optional[str]): Текст (метка) опции для выбора.

        Returns:
            str: Статусное сообщение об успехе или ошибке.
        """
        # Проверка, что указан хотя бы один критерий выбора (value или label)
        if not value and not label: return 'Ошибка: Нужно указать value или label.'
        target_selection: str = f"value='{value}'" if value else f"label='{label}'"
        logger.info(f"Выбор опции {target_selection} в списке '{selector}'")
        # Проверка состояния страницы
        if not self.page or self.page.is_closed(): return 'Ошибка: Страница закрыта.'
        try:
            # Получение первого элемента (выпадающего списка) по селектору
            dropdown = self.page.locator(selector).first
            # Ожидание видимости списка
            await dropdown.wait_for(state='visible', timeout=10000)
            # Выбор опции по значению или метке
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
        """ 
        Асинхронно отправляет форму. Может либо кликнуть по указанной кнопке отправки,
        либо попытаться найти и кликнуть стандартную кнопку отправки внутри указанной формы.
        Этот метод по умолчанию НЕ ожидает завершения навигации после отправки.

        Args:
            form_selector (Optional[str]): CSS селектор HTML-формы.
            submit_button_selector (Optional[str]): CSS селектор кнопки отправки.

        Returns:
            str: Статусное сообщение об успехе или ошибке.
        """
        # Проверка, что указан хотя бы один селектор (формы или кнопки)
        if not form_selector and not submit_button_selector: return 'Ошибка: Укажите селектор формы или кнопки.'
        target_action: str = f"кнопку '{submit_button_selector}'" if submit_button_selector else f"форму '{form_selector}'"
        logger.info(f"Отправка {target_action}")
        # Проверка состояния страницы
        if not self.page or self.page.is_closed(): return 'Ошибка: Страница закрыта.'
        try:
            if submit_button_selector:
                # Если указан селектор кнопки, кликаем по ней
                button = self.page.locator(submit_button_selector).first
                await button.wait_for(state='visible', timeout=10000)
                await button.click() # Простой клик, не ожидающий навигации
            elif form_selector:
                 # Если указан селектор формы, ищем стандартную кнопку отправки внутри нее
                 form_element = self.page.locator(form_selector).first
                 # Поиск кнопки типа submit или input type submit
                 submit_btn_locator = form_element.locator('button[type="submit"], input[type="submit"]').first
                 is_btn_visible: bool = await submit_btn_locator.is_visible(timeout=5000)
                 if not is_btn_visible: 
                     return f"Ошибка: Не найдена видимая кнопка отправки в форме '{form_selector}'"
                 await submit_btn_locator.click() # Простой клик
            logger.info(f"Форма/кнопка {target_action} успешно отправлена (клик выполнен).")
            return f"Форма/кнопка {target_action} отправлена."
        except PlaywrightError as ex: 
            error_msg=ex.message.splitlines()[0]
            logger.error(f"Ошибка Playwright при отправке {target_action}: {error_msg}", None, exc_info=False)
            return f"Ошибка отправки {target_action}: {error_msg}"
        except Exception as ex: 
            logger.error(f"Ошибка при отправке {target_action}.", ex, exc_info=True)
            return f"Ошибка отправки {target_action}: {str(ex)}"

# =============================================================

# === ScreenshotController Class Definition (Async Version) ===
class ScreenshotController:
    """ 
    Создает скриншоты текущей страницы или ее отдельных элементов
    с использованием асинхронного API Playwright.
    """
    page: Page # Активная страница Playwright
    def __init__(self, page: Page) -> None:
        """
        Инициализирует ScreenshotController.

        Args:
            page (Page): Активный объект страницы Playwright.

        Raises:
            ValueError: Если `page` не предоставлена или закрыта.
        """
        if not page or page.is_closed(): 
            raise ValueError('ScreenshotController требует активный объект страницы Playwright.')
        self.page = page
        logger.debug('ScreenshotController инициализирован.')

    async def take_screenshot(self, save_path: str, full_page: bool = True, selector: Optional[str] = None) -> str:
        """ 
        Асинхронно делает скриншот. Может сделать скриншот всей страницы, видимой части
        или указанного элемента.

        Args:
            save_path (str): Путь для сохранения файла скриншота.
            full_page (bool): Делать ли скриншот всей страницы (если `selector` не указан). По умолчанию True.
            selector (Optional[str]): CSS селектор элемента для скриншота. Если указан, `full_page` игнорируется.

        Returns:
            str: Статусное сообщение об успехе или ошибке.
        """
        path_obj: Path = Path(save_path) # Преобразование строки пути в объект Path
        try:
            # Создание родительской директории, если она не существует
            path_obj.parent.mkdir(parents=True, exist_ok=True)
        except Exception as ex: 
            logger.error(f'Не удалось создать директорию: {path_obj.parent}', ex, exc_info=True)
            return f'Ошибка создания директории {path_obj.parent}'
        
        # Определение объекта скриншота для логирования
        target_description: str = f"элемента '{selector}'" if selector else ("всей страницы" if full_page else "видимой части")
        logger.info(f'Создание скриншота {target_description} в файл: {path_obj}')
        # Проверка состояния страницы
        if not self.page or self.page.is_closed(): return 'Ошибка: Страница закрыта.'
        try:
             if selector:
                 # Скриншот конкретного элемента
                 element_locator = self.page.locator(selector).first
                 await element_locator.wait_for(state='visible', timeout=10000) # Ожидание видимости элемента
                 await element_locator.screenshot(path=path_obj) # Создание скриншота элемента
             else:
                 # Скриншот страницы (всей или видимой части)
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

# =============================================================

# === DownloadController Class Definition (Async Version) ===
class DownloadController:
    """ 
    Управляет скачиванием файлов, инициируемым действиями на странице,
    с использованием асинхронного API Playwright.
    """
    page: Page # Активная страница Playwright
    def __init__(self, page: Page) -> None:
        """
        Инициализирует DownloadController.

        Args:
            page (Page): Активный объект страницы Playwright.

        Raises:
            ValueError: Если `page` не предоставлена или закрыта.
        """
        if not page or page.is_closed(): 
            raise ValueError('DownloadController требует активный объект страницы Playwright.')
        self.page = page
        logger.debug('DownloadController инициализирован.')

    async def click_and_download(self, click_selector: str, save_directory: str, timeout: int = 60000) -> str:
        """ 
        Асинхронно кликает по элементу (например, ссылке или кнопке) и ожидает начала
        скачивания файла. Скачанный файл сохраняется в указанную директорию.

        Args:
            click_selector (str): CSS селектор элемента, клик по которому инициирует скачивание.
            save_directory (str): Директория для сохранения скачанного файла.
            timeout (int): Таймаут ожидания начала скачивания в миллисекундах. По умолчанию 60000 (60с).

        Returns:
            str: Статусное сообщение об успехе или ошибке скачивания.
        """
        save_dir_path: Path = Path(save_directory) # Преобразование строки пути в объект Path
        try:
            # Создание директории для сохранения, если она не существует
            save_dir_path.mkdir(parents=True, exist_ok=True)
        except Exception as ex: 
            logger.error(f'Не удалось создать директорию: {save_dir_path}', ex, exc_info=True)
            return f'Ошибка создания директории {save_dir_path}'
        
        logger.info(f"Попытка скачивания после клика на '{click_selector}' в {save_dir_path} (Таймаут: {timeout}ms)")
        # Проверка состояния страницы
        if not self.page or self.page.is_closed(): return 'Ошибка: Страница закрыта.'
        try:
            # Использование менеджера контекста `expect_download` для ожидания события скачивания
            # одновременно с выполнением действия (клика)
            async with self.page.expect_download(timeout=timeout) as download_info:
                # Находим элемент и кликаем по нему
                button_or_link = self.page.locator(click_selector).first
                await button_or_link.wait_for(state='visible', timeout=10000) # Ожидание видимости элемента
                await button_or_link.click() # Клик для инициации скачивания

            # Получение объекта Download после завершения ожидания
            download: Download = await download_info.value
            suggested_filename: str = download.suggested_filename # Получение предлагаемого имени файла
            save_path: Path = save_dir_path / suggested_filename # Полный путь для сохранения файла
            # Сохранение скачанного файла
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

# =============================================================

# === JavaScriptExecutionController Class Definition (Async Version) ===
class JavaScriptExecutionController:
    """ 
    Выполняет произвольный JavaScript-код на текущей странице
    с использованием асинхронного API Playwright.
    """
    page: Page # Активная страница Playwright
    def __init__(self, page: Page) -> None:
        """
        Инициализирует JavaScriptExecutionController.

        Args:
            page (Page): Активный объект страницы Playwright.

        Raises:
            ValueError: Если `page` не предоставлена или закрыта.
        """
        if not page or page.is_closed(): 
            raise ValueError('JavaScriptExecutionController требует активный объект страницы Playwright.')
        self.page = page
        logger.debug('JavaScriptExecutionController инициализирован.')

    async def execute_script(self, script: str) -> Union[str, Any]:
        """ 
        Асинхронно выполняет предоставленный JavaScript-код на странице и возвращает результат.
        Результат выполнения скрипта сериализуется в JSON, если это возможно.

        Args:
            script (str): Строка с JavaScript-кодом для выполнения.

        Returns:
            Union[str, Any]: Результат выполнения скрипта (сериализованный в JSON или как строка) 
                             или сообщение об ошибке.
        """
        logger.warning(f'Выполнение JavaScript (ОСТОРОЖНО!): {script[:100]}...') # Предупреждение о потенциальной опасности
        # Проверка состояния страницы
        if not self.page or self.page.is_closed(): return 'Ошибка: Страница закрыта.'
        try:
            # Асинхронное выполнение скрипта
            result: Any = await self.page.evaluate(script)
            logger.info(f'JavaScript выполнен успешно. Результат: {str(result)[:100]}...')
            try: 
                # Попытка сериализации результата в JSON
                return json.dumps(result) 
            except TypeError: 
                # Если сериализация в JSON не удалась, возвращаем как строку
                return str(result) 
        except PlaywrightError as ex: 
            error_msg=ex.message.splitlines()[0]
            logger.error(f'Ошибка Playwright при выполнении JS: {error_msg}', None, exc_info=False)
            return f'Ошибка выполнения JS: {error_msg}'
        except Exception as ex: 
            logger.error('Ошибка при выполнении JS.', ex, exc_info=True)
            return f'Ошибка выполнения JS: {str(ex)}'

# =============================================================

# === StateManager Class Definition (Async Version) ===
class StateManager:
    """ 
    Управляет состоянием сессии браузера (cookies, localStorage, sessionStorage)
    с использованием асинхронного API Playwright.
    """
    context: BrowserContext # Контекст браузера Playwright
    page: ContextPage       # Опциональная активная страница (для операций с localStorage/sessionStorage)
    def __init__(self, context: BrowserContext, page: ContextPage = None) -> None:
        """
        Инициализирует StateManager.

        Args:
            context (BrowserContext): Активный контекст браузера Playwright.
            page (ContextPage, optional): Активная страница Playwright (необходима для `clear_storage`).
                                           По умолчанию None.

        Raises:
            ValueError: Если `context` не предоставлен или закрыт.
        """
        # Playwright BrowserContext не имеет is_closed(), проверяем только на None
        if not context: 
            raise ValueError('StateManager требует активный контекст браузера Playwright.')
        self.context = context
        self.page = page
        logger.debug('StateManager инициализирован.')

    async def get_cookies(self, url: Optional[str] = None) -> Union[List[Dict[str, Any]], str]:
        """ 
        Асинхронно возвращает список cookies для текущего контекста браузера.
        Можно указать URL для фильтрации cookies.

        Args:
            url (Optional[str]): URL для фильтрации cookies. Если None, возвращает все cookies.

        Returns:
            Union[List[Dict[str, Any]], str]: Список словарей с данными cookies или сообщение об ошибке.
        """
        logger.info(f"Получение cookies (URL: {url or 'Все'})")
        # Проверка состояния контекста (нет is_closed(), проверяем на None)
        if not self.context: return 'Ошибка: Контекст браузера закрыт или не инициализирован.'
        try: 
            # Асинхронное получение cookies
            cookies_list: List[Dict[str, Any]] = await self.context.cookies(urls=[url] if url else None)
            logger.info(f'Получено {len(cookies_list)} cookies.'); return cookies_list
        except Exception as ex: 
            logger.error('Ошибка при получении cookies.', ex, exc_info=True)
            return f'Ошибка получения cookies: {str(ex)}'

    async def add_cookies(self, cookies: List[Dict[str, Any]]) -> str:
        """ 
        Асинхронно добавляет список cookies в текущий контекст браузера.

        Args:
            cookies (List[Dict[str, Any]]): Список словарей, каждый из которых представляет cookie.

        Returns:
            str: Статусное сообщение об успехе или ошибке.
        """
        cookies_count: int = len(cookies)
        logger.info(f'Добавление {cookies_count} cookies...')
        # Проверка состояния контекста
        if not self.context: return 'Ошибка: Контекст браузера закрыт или не инициализирован.'
        try: 
            # Асинхронное добавление cookies
            await self.context.add_cookies(cookies)
            logger.info(f'{cookies_count} cookies успешно добавлены.'); return f'{cookies_count} cookies добавлены.'
        except Exception as ex: 
            logger.error('Ошибка при добавлении cookies.', ex, exc_info=True)
            return f'Ошибка добавления cookies: {str(ex)}'

    async def clear_cookies(self) -> str:
        """ 
        Асинхронно очищает все cookies в текущем контексте браузера.

        Returns:
            str: Статусное сообщение об успехе или ошибке.
        """
        logger.info('Очистка cookies...')
        # Проверка состояния контекста
        if not self.context: return 'Ошибка: Контекст браузера закрыт или не инициализирован.'
        try: 
            # Асинхронная очистка cookies
            await self.context.clear_cookies()
            logger.info('Cookies очищены.'); return 'Cookies очищены.'
        except Exception as ex: 
            logger.error('Ошибка при очистке cookies.', ex, exc_info=True)
            return f'Ошибка очистки cookies: {str(ex)}'

    async def clear_storage(self) -> str:
        """ 
        Асинхронно очищает localStorage и sessionStorage для текущей активной страницы.
        Требует, чтобы атрибут `page` был установлен и страница была активна.

        Returns:
            str: Статусное сообщение об успехе или ошибке.
        """
        logger.info('Очистка localStorage и sessionStorage...')
        # Проверка наличия и состояния страницы
        if not self.page or self.page.is_closed(): return 'Ошибка: Страница закрыта или не доступна для очистки storage.'
        try: 
            # Выполнение JavaScript для очистки localStorage и sessionStorage
            await self.page.evaluate('() => { localStorage.clear(); sessionStorage.clear(); }')
            logger.info('localStorage и sessionStorage очищены.'); return 'localStorage и sessionStorage очищены.'
        except Exception as ex: 
            logger.error('Ошибка при очистке storage.', ex, exc_info=True)
            return f'Ошибка очистки storage: {str(ex)}'

    # login остается синхронной заглушкой, так как логика входа сильно зависит от конкретного сайта
    # и обычно требует последовательности асинхронных действий, которые лучше реализовать в агенте.
    def login(self, *args: Any, **kwargs: Any) -> str:
         """ 
         Метод-заглушка для выполнения входа на сайт.
         Реальная логика входа должна быть реализована с использованием других методов контроллера
         (например, навигация, заполнение полей, клик) в рамках агента.
         """
         logger.warning('Метод login в StateManager является заглушкой и не выполняет реальных действий.'); return 'Заглушка: Вход не реализован.'

# =============================================================
