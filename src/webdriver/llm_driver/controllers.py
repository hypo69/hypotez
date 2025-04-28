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
from playwright.async_api import (async_playwright, Page, Browser, Playwright, # ИСПОЛЬЗУЕМ ASYNC API
                                  BrowserContext, Error as PlaywrightError, Download) # Добавлены Download, BrowserContext
# ================================

# === Data Extraction Imports ===
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE: bool = True
except ImportError:
    BS4_AVAILABLE = False
# ==========================

# === Internal/Project Imports ===
import header # pylint: disable=unused-import # Импортируется для сайд-эффектов (sys.path)
# Импорт __root__ для корректных относительных путей проекта
from header import __root__
# from src import gs # gs может быть не нужен в этом конкретном файле
from src.logger import logger # Импортируем настроенный логгер проекта
# ===============================

# Определяем псевдонимы типов для Async API
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
    playwright: ContextPlaywright = None
    browser: ContextBrowser = None
    page: ContextPage = None
    context: ContextBrowserContext = None
    headless: bool
    default_timeout: int
    _is_started: bool = False # Флаг для отслеживания асинхронной инициализации

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
        self._is_started = False
        logger.info(f'BrowserController создан (Headless={self.headless}, Timeout={self.default_timeout}ms). Вызовите start() для инициализации.')

    async def start(self) -> bool:
        """
        Асинхронно инициализирует Playwright, запускает браузер и создает страницу.
        Должен быть вызван с `await` перед использованием других методов.

        Returns:
            bool: True, если инициализация прошла успешно, иначе False.

        Raises:
            RuntimeError: Если не удается инициализировать Playwright или браузер (но сейчас возвращает False).

        Example:
            >>> controller = BrowserController()
            >>> if await controller.start():
            ...    # Работа с контроллером
            ...    await controller.close()
        """
        # Проверка, не был ли контроллер уже запущен
        if self._is_started:
            logger.warning('BrowserController уже инициализирован.')
            return True

        logger.info('Асинхронная инициализация BrowserController...')
        try:
            # Асинхронный запуск Playwright
            self.playwright = await async_playwright().start()
            # Асинхронный запуск браузера
            self.browser = await self.playwright.chromium.launch(headless=self.headless)
            # Асинхронное создание контекста
            self.context = await self.browser.new_context()
            # Асинхронное создание страницы
            self.page = await self.context.new_page()
            # Установка таймаута
            self.page.set_default_timeout(self.default_timeout)
            # Установка флага успешного запуска
            self._is_started = True
            logger.info('Playwright запущен, браузер открыт, контекст и страница созданы (Async).')
            return True
        except Exception as ex:
            logger.error('КРИТИЧЕСКАЯ ОШИБКА Async: Не удалось инициализировать Playwright/Браузер.', ex, exc_info=True)
            # Попытка асинхронного закрытия при ошибке
            await self.close()
            # Возвращаем False вместо исключения, чтобы основной код мог это обработать
            return False

    async def navigate(self, url: str) -> str:
        """
        Асинхронно переводит страницу браузера на указанный URL.

        Args:
            url (str): URL для навигации.

        Returns:
            str: Статусное сообщение об успехе или ошибке.

        Example:
            >>> status = await controller.navigate('https://example.com')
        """
        # Проверка инициализации и состояния страницы
        if not self._is_started or not self.page or self.page.is_closed():
             logger.error('Ошибка навигации: Контроллер не инициализирован или страница закрыта.')
             return 'Ошибка: Контроллер/страница не инициализированы или закрыты.'

        logger.info(f'Переход на: {url}')
        try:
            # Асинхронный переход
            response = await self.page.goto(url, wait_until='domcontentloaded')
            if response and response.ok:
                title: str = await self.page.title()
                logger.info(f"Успешный переход на {url}. Статус: {response.status}. Заголовок: '{title[:100]}'")
                try:
                    # Асинхронное получение текста
                    body_text: str = await self.page.locator('body').inner_text(timeout=5000)
                    return f'Успешный переход на {url}. Заголовок: {title}. Начало текста: {body_text[:200]}...'
                except Exception as text_ex:
                    logger.warning(f'Не удалось быстро получить текст после навигации на {url}.', text_ex, exc_info=False)
                    return f'Успешный переход на {url}. Заголовок: {title}. (Текст не получен)'
            else:
                status: Union[int, str] = response.status if response else 'N/A'
                logger.warning(f'Ошибка навигации для {url}. Статус: {status}')
                return f'Не удалось перейти на {url}. Статус: {status}'
        except PlaywrightError as ex:
            error_msg: str = ex.message.splitlines()[0]
            logger.error(f'Ошибка Playwright при переходе на {url}: {error_msg}', exc_info=False)
            return f'Ошибка навигации на {url}: {error_msg}'
        except Exception as ex:
            logger.error(f'Неожиданная ошибка при переходе на {url}.', ex, exc_info=True)
            return f'Неожиданная ошибка навигации на {url}: {str(ex)}'

    async def scrape_text(self, selector: Optional[str] = None) -> str:
        """
        Асинхронно извлекает текстовое содержимое с текущей страницы.

        Args:
            selector (Optional[str]): CSS селектор. Если None, извлекает текст всего body. По умолчанию None.

        Returns:
            str: Извлеченный текст или сообщение об ошибке.

        Example:
            >>> text = await controller.scrape_text()
            >>> heading_text = await controller.scrape_text('h1')
        """
        # Проверка инициализации и состояния страницы
        if not self._is_started or not self.page or self.page.is_closed():
             logger.error('Ошибка извлечения текста: Контроллер не инициализирован или страница закрыта.')
             return 'Ошибка: Контроллер/страница не инициализированы или закрыты.'

        action: str = f'Извлечение текста (Селектор: {selector})' if selector else 'Извлечение текста (Body)'
        logger.info(action)
        content: str = ''
        cleaned_content: str = ''
        try:
            if selector:
                elements = self.page.locator(selector)
                # Асинхронное получение количества элементов
                count: int = await elements.count()
                if count == 0:
                    logger.warning(f"Элементы не найдены для селектора: '{selector}'")
                    return f"Элементы не найдены для селектора: {selector}"
                # Асинхронное получение текстов всех элементов
                all_texts: List[str] = await elements.all_inner_texts()
                content = '\n\n'.join(t.strip() for t in all_texts if t.strip())
                logger.info(f'Извлечен текст из {count} элемент(ов) по селектору "{selector}". Длина: {len(content)}')
            else:
                # Асинхронное получение текста body
                content = await self.page.locator('body').inner_text()
                logger.info(f'Извлечен текст из body. Длина: {len(content)}')

            # Очистка текста
            cleaned_content = '\n'.join([line.strip() for line in content.splitlines() if line.strip()])
            return cleaned_content
        except PlaywrightError as ex:
            error_msg: str = ex.message.splitlines()[0]
            logger.error(f'Ошибка Playwright при извлечении текста (Селектор: {selector}): {error_msg}', exc_info=False)
            return f'Ошибка извлечения текста: {error_msg}'
        except Exception as ex:
            logger.error(f'Неожиданная ошибка при извлечении текста (Селектор: {selector}).', ex, exc_info=True)
            return f'Неожиданная ошибка извлечения текста: {str(ex)}'

    async def scrape_html(self, selector: Optional[str] = None) -> str:
        """
        Асинхронно извлекает HTML содержимое с текущей страницы или элемента.

        Args:
            selector (Optional[str]): CSS селектор элемента. Если None, извлекает HTML всей страницы. По умолчанию None.

        Returns:
            str: Строка с HTML содержимым или сообщение об ошибке.

        Example:
            >>> html = await controller.scrape_html()
            >>> element_html = await controller.scrape_html('#my-element')
        """
        # Проверка инициализации и состояния страницы
        if not self._is_started or not self.page or self.page.is_closed():
             logger.error('Ошибка извлечения HTML: Контроллер не инициализирован или страница закрыта.')
             return 'Ошибка: Контроллер/страница не инициализированы или закрыты.'

        action: str = f'Извлечение HTML (Селектор: {selector})' if selector else 'Извлечение HTML (Body)'
        logger.info(action)
        html_content: str = ''
        try:
            if selector:
                 # Асинхронное выполнение JS для получения outerHTML
                 html_content = await self.page.locator(selector).first.evaluate('element => element.outerHTML', timeout=10000)
            else:
                 # Асинхронное получение контента всей страницы
                 html_content = await self.page.content()
            logger.info(f'Извлечен HTML. Длина: {len(html_content)}')
            return html_content
        except PlaywrightError as ex:
            error_msg: str = ex.message.splitlines()[0]
            logger.error(f'Ошибка Playwright при извлечении HTML (Селектор: {selector}): {error_msg}', exc_info=False)
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
            str: Статусное сообщение об успехе или ошибке.

        Example:
            >>> status = await controller.click_element('button#submit')
        """
        # Проверка инициализации и состояния страницы
        if not self._is_started or not self.page or self.page.is_closed():
             logger.error('Ошибка клика: Контроллер не инициализирован или страница закрыта.')
             return 'Ошибка: Контроллер/страница не инициализированы или закрыты.'
        if not selector:
            logger.warning('Ошибка клика: Не предоставлен селектор.')
            return 'Ошибка: Не указан селектор для клика.'

        logger.info(f"Попытка клика по элементу с селектором: '{selector}'")
        try:
            element_locator = self.page.locator(selector)
            # Асинхронное получение количества
            count: int = await element_locator.count()
            if count == 0:
                logger.warning(f"Не удалось кликнуть: Элемент не найден по селектору '{selector}'")
                return f"Ошибка: Элемент не найден по селектору '{selector}'"
            if count > 1:
                logger.warning(f"Найдено несколько элементов ({count}) по селектору '{selector}'. Клик по первому видимому.")

            # Асинхронное ожидание видимости
            await element_locator.first.wait_for(state='visible', timeout=self.default_timeout // 3)
            # Асинхронный клик
            await element_locator.first.click(timeout=self.default_timeout // 3)
            logger.info(f"Успешный клик по первому элементу с селектором: '{selector}'")
            return f"Успешный клик по элементу: {selector}"
        except PlaywrightError as ex:
            error_msg: str = ex.message.splitlines()[0]
            logger.error(f"Ошибка Playwright при клике по '{selector}': {error_msg}", exc_info=False)
            if 'Timeout' in error_msg:
                 return f"Ошибка (таймаут) при клике/ожидании элемента '{selector}'. Возможно, он не появился или не кликабелен."
            return f"Ошибка клика по '{selector}': {error_msg}"
        except Exception as ex:
            logger.error(f"Неожиданная ошибка при клике по '{selector}'.", ex, exc_info=True)
            return f"Неожиданная ошибка клика по '{selector}': {str(ex)}"

    def get_current_url(self) -> str:
        """
        Синхронно возвращает текущий URL страницы.
        (Получение URL не требует асинхронности).

        Returns:
            str: Строка с текущим URL или сообщение об ошибке.
        """
        if not self._is_started or not self.page or self.page.is_closed():
            logger.error('Ошибка получения URL: Контроллер не инициализирован или страница закрыта.')
            return 'Ошибка: Контроллер/страница не инициализированы или закрыты.'
        return self.page.url

    async def close(self) -> None:
        """
        Асинхронно закрывает страницу, контекст, браузер и останавливает Playwright.
        Освобождает все связанные ресурсы.

        Example:
            >>> await controller.close()
        """
        logger.info('Асинхронное закрытие BrowserController...')
        # Закрытие ресурсов в обратном порядке их создания
        if self.page and not self.page.is_closed():
            try: await self.page.close(); logger.debug('Страница закрыта (Async).')
            except Exception as ex: logger.warning('Ошибка при закрытии страницы (Async).', ex, exc_info=False)
        if self.context and not self.context.is_closed():
             try: await self.context.close(); logger.debug('Контекст закрыт (Async).')
             except Exception as ex: logger.warning('Ошибка при закрытии контекста (Async).', ex, exc_info=False)
        if self.browser and self.browser.is_connected():
            try: await self.browser.close(); logger.debug('Браузер закрыт (Async).')
            except Exception as ex: logger.warning('Ошибка при закрытии браузера (Async).', ex, exc_info=False)
        if self.playwright:
            # playwright.stop() не async, но закрытия браузера достаточно
            logger.debug('Playwright объект существует, stop() не вызывается в async close.')
            # try: self.playwright.stop(); logger.debug('Playwright остановлен.') # Не нужно в async
            # except Exception as ex: logger.warning('Ошибка при остановке playwright.', ex, exc_info=False)

        # Обнуление ссылок
        self.page = None; self.context = None; self.browser = None; self.playwright = None
        self._is_started = False # Сброс флага
        logger.info('Ресурсы BrowserController освобождены (Async).')

# =============================================================

# === DataExtractionController Class Definition ===
class DataExtractionController:
    """
    Извлекает структурированную информацию из HTML или текста (синхронно).
    Методы этого класса не требуют `await`, так как работают с уже полученными данными.
    """
    def __init__(self) -> None:
        """ Инициализирует контроллер и проверяет доступность BeautifulSoup. """
        if not BS4_AVAILABLE:
            logger.warning('Библиотека BeautifulSoup4 не найдена. Функции DataExtractionController будут ограничены.')
        logger.debug('DataExtractionController инициализирован.')

    # Методы extract_product_details, extract_contact_info, find_links
    # остаются СИНХРОННЫМИ, так как работают с данными в памяти.
    def extract_product_details(self, html_content: str) -> Dict[str, Any]:
        """ Извлекает данные о товаре из HTML (плейсхолдер). """
        # (Код метода без изменений)
        extracted_data: Dict[str, Any]; soup: BeautifulSoup; title_tag: Optional[Any]
        logger.info(f'Попытка извлечения данных о товаре (Длина HTML: {len(html_content)})...')
        if not BS4_AVAILABLE: return {'error': 'BeautifulSoup4 not available'}
        if not html_content or not isinstance(html_content, str): return {'error': 'Invalid HTML content provided'}
        extracted_data = {'product_name': 'not found', 'url': 'not found', 'product_sku': 'not found', 'category_name': 'not found', 'parent_category': 'not found', 'brand_name': 'not found', 'brand_url': 'not found', 'product_image': 'not found', 'product_price': 'not found', 'product_description': 'not found', 'specifications': 'not found', 'product_params': {}, 'available_for_order': 'unknown', 'condition': 'not found'}
        try:
            soup = BeautifulSoup(html_content, 'lxml')
            title_tag = soup.find('h1')
            if title_tag: extracted_data['product_name'] = title_tag.get_text(strip=True)
            # --- ДРУГИЕ ПРАВИЛА ИЗВЛЕЧЕНИЯ ---
            logger.warning('Извлечение данных о товаре ЗАВЕРШЕНО (базовая логика).')
            return extracted_data
        except Exception as ex: logger.error('Ошибка при извлечении данных о товаре.', ex, exc_info=True); return {'error': f'Extraction failed: {str(ex)}'}

    def extract_contact_info(self, text_content: str) -> Dict[str, List[str]]:
        """ Извлекает email и телефоны из текста. """
        # (Код метода без изменений)
        contacts: Dict[str, List[str]] = {'emails': [], 'phones': []}; email_pattern: str; phone_pattern: str
        logger.info(f'Попытка извлечения контактов (Длина текста: {len(text_content)})...')
        if not text_content or not isinstance(text_content, str): return {'error': 'Invalid text content provided'}
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'; phone_pattern = r'\(?\+?\d{1,4}?\)?[-\s\.]?\(?\d{1,4}?\)?[\d\s\.-]{7,}'
        try:
            contacts['emails'] = sorted(list(set(re.findall(email_pattern, text_content)))); contacts['phones'] = sorted(list(set(re.findall(phone_pattern, text_content))))
            logger.info(f"Найдено контактов: Emails={len(contacts['emails'])}, Phones={len(contacts['phones'])}")
            return contacts
        except Exception as ex: logger.error('Ошибка при извлечении контактов.', ex, exc_info=True); return {'error': f'Contact extraction failed: {str(ex)}'}

    def find_links(self, html_content: str, base_url: Optional[str] = None) -> Union[List[str], Dict[str, str]]:
        """ Находит все ссылки в HTML. """
        # (Код метода без изменений)
        links: List[str] = []; soup: BeautifulSoup; a_tag: Any; href: str; absolute_url: str; unique_links: List[str]
        logger.info(f'Поиск ссылок (Длина HTML: {len(html_content)})...')
        if not BS4_AVAILABLE: return {'error': 'BeautifulSoup4 not available'}
        if not html_content or not isinstance(html_content, str): return {'error': 'Invalid HTML content provided'}
        try:
            soup = BeautifulSoup(html_content, 'lxml')
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href'].strip()
                if href and not href.startswith('#') and not href.startswith('javascript:'):
                     if base_url and not href.startswith(('http://', 'https://', '//')):
                         try: absolute_url = urljoin(base_url, href); links.append(absolute_url)
                         except Exception as url_ex: logger.warning(f'Не удалось сделать URL абсолютным: {href} (base: {base_url}).', url_ex, exc_info=False); links.append(href)
                     else: links.append(href)
            unique_links = sorted(list(set(links))); logger.info(f'Найдено {len(unique_links)} уникальных ссылок.'); return unique_links
        except Exception as ex: logger.error('Ошибка при поиске ссылок.', ex, exc_info=True); return {'error': f'Link extraction failed: {str(ex)}'}

# =============================================================

# === FormController Class Definition (Async Version) ===
class FormController:
    """ Управляет заполнением и отправкой HTML-форм (Async Version). """
    page: Page
    def __init__(self, page: Page) -> None:
        if not page or page.is_closed(): raise ValueError('FormController требует активный объект страницы.')
        self.page = page; logger.debug('FormController инициализирован.')

    async def fill_input_field(self, selector: str, value: str) -> str:
        """ Асинхронно находит поле ввода и вводит значение. """
        field: Any # Playwright Locator
        logger.info(f"Заполнение поля '{selector}' значением '{value[:20]}...'")
        if not self.page or self.page.is_closed(): return 'Ошибка: Страница закрыта.'
        try:
            field = self.page.locator(selector).first
            await field.wait_for(state='visible', timeout=10000)
            await field.fill(value)
            logger.info(f"Поле '{selector}' успешно заполнено.")
            return f"Поле '{selector}' заполнено."
        except PlaywrightError as ex: error_msg=ex.message.splitlines()[0]; logger.error(f"Ошибка Playwright при заполнении '{selector}': {error_msg}", exc_info=False); return f"Ошибка заполнения '{selector}': {error_msg}"
        except Exception as ex: logger.error(f"Ошибка при заполнении '{selector}'.", ex, exc_info=True); return f"Ошибка заполнения '{selector}': {str(ex)}"

    async def select_dropdown_option(self, selector: str, value: Optional[str] = None, label: Optional[str] = None) -> str:
        """ Асинхронно выбирает опцию в выпадающем списке. """
        if not value and not label: return 'Ошибка: Нужно указать value или label.'
        target: str = f"value='{value}'" if value else f"label='{label}'"
        logger.info(f"Выбор опции {target} в списке '{selector}'")
        if not self.page or self.page.is_closed(): return 'Ошибка: Страница закрыта.'
        try:
            dropdown = self.page.locator(selector).first
            await dropdown.wait_for(state='visible', timeout=10000)
            if value: await dropdown.select_option(value=value)
            elif label: await dropdown.select_option(label=label)
            logger.info(f"Опция {target} успешно выбрана в '{selector}'.")
            return f"Опция {target} выбрана в '{selector}'."
        except PlaywrightError as ex: error_msg=ex.message.splitlines()[0]; logger.error(f"Ошибка Playwright при выборе в '{selector}': {error_msg}", exc_info=False); return f"Ошибка выбора в '{selector}': {error_msg}"
        except Exception as ex: logger.error(f"Ошибка при выборе в '{selector}'.", ex, exc_info=True); return f"Ошибка выбора в '{selector}': {str(ex)}"

    async def submit_form(self, form_selector: Optional[str] = None, submit_button_selector: Optional[str] = None) -> str:
        """ Асинхронно отправляет форму (без ожидания навигации по умолчанию). """
        if not form_selector and not submit_button_selector: return 'Ошибка: Укажите селектор формы или кнопки.'
        target: str = f"кнопку '{submit_button_selector}'" if submit_button_selector else f"форму '{form_selector}'"
        logger.info(f"Отправка {target}")
        if not self.page or self.page.is_closed(): return 'Ошибка: Страница закрыта.'
        try:
            if submit_button_selector:
                button = self.page.locator(submit_button_selector).first
                await button.wait_for(state='visible', timeout=10000)
                await button.click() # Простой клик без ожидания навигации
            elif form_selector:
                 form = self.page.locator(form_selector).first
                 submit_btn = form.locator('button[type="submit"], input[type="submit"]').first
                 is_visible: bool = await submit_btn.is_visible(timeout=5000)
                 if not is_visible: return f"Ошибка: Не найдена видимая кнопка отправки в форме '{form_selector}'"
                 await submit_btn.click() # Простой клик
            logger.info(f"Форма/кнопка {target} успешно отправлена (клик выполнен).")
            return f"Форма/кнопка {target} отправлена."
        except PlaywrightError as ex: error_msg=ex.message.splitlines()[0]; logger.error(f"Ошибка Playwright при отправке {target}: {error_msg}", exc_info=False); return f"Ошибка отправки {target}: {error_msg}"
        except Exception as ex: logger.error(f"Ошибка при отправке {target}.", ex, exc_info=True); return f"Ошибка отправки {target}: {str(ex)}"

# =============================================================

# === ScreenshotController Class Definition (Async Version) ===
class ScreenshotController:
    """ Делает скриншоты страницы или ее частей (Async Version). """
    page: Page
    def __init__(self, page: Page) -> None:
        if not page or page.is_closed(): raise ValueError('ScreenshotController требует активный объект страницы.')
        self.page = page; logger.debug('ScreenshotController инициализирован.')

    async def take_screenshot(self, save_path: str, full_page: bool = True, selector: Optional[str] = None) -> str:
        """ Асинхронно делает скриншот. """
        path_obj: Path = Path(save_path)
        try: path_obj.parent.mkdir(parents=True, exist_ok=True)
        except Exception as ex: logger.error(f'Не удалось создать директорию: {path_obj.parent}', ex, exc_info=True); return f'Ошибка создания директории {path_obj.parent}'
        target: str = f"элемента '{selector}'" if selector else ("всей страницы" if full_page else "видимой части")
        logger.info(f'Создание скриншота {target} в файл: {path_obj}')
        if not self.page or self.page.is_closed(): return 'Ошибка: Страница закрыта.'
        try:
             if selector:
                 element = self.page.locator(selector).first
                 await element.wait_for(state='visible', timeout=10000)
                 await element.screenshot(path=path_obj)
             else:
                 await self.page.screenshot(path=path_obj, full_page=full_page)
             logger.info(f'Скриншот {target} успешно сохранен в {path_obj}')
             return f'Скриншот сохранен: {path_obj}'
        except PlaywrightError as ex: error_msg=ex.message.splitlines()[0]; logger.error(f'Ошибка Playwright при создании скриншота {target}: {error_msg}', exc_info=False); return f'Ошибка скриншота {target}: {error_msg}'
        except Exception as ex: logger.error(f'Ошибка при создании скриншота {target}.', ex, exc_info=True); return f'Ошибка скриншота {target}: {str(ex)}'

# =============================================================

# === DownloadController Class Definition (Async Version) ===
class DownloadController:
    """ Управляет скачиванием файлов (Async Version). """
    page: Page
    def __init__(self, page: Page) -> None:
        if not page or page.is_closed(): raise ValueError('DownloadController требует активный объект страницы.')
        self.page = page; logger.debug('DownloadController инициализирован.')

    async def click_and_download(self, click_selector: str, save_directory: str, timeout: int = 60000) -> str:
        """ Асинхронно кликает по элементу и ожидает/сохраняет скачанный файл. """
        save_dir_path: Path = Path(save_directory)
        try: save_dir_path.mkdir(parents=True, exist_ok=True)
        except Exception as ex: logger.error(f'Не удалось создать директорию: {save_dir_path}', ex, exc_info=True); return f'Ошибка создания директории {save_dir_path}'
        logger.info(f"Попытка скачивания после клика на '{click_selector}' в {save_dir_path} (Таймаут: {timeout}ms)")
        if not self.page or self.page.is_closed(): return 'Ошибка: Страница закрыта.'
        try:
            # Ожидание события скачивания одновременно с кликом
            async with self.page.expect_download(timeout=timeout) as download_info:
                button_or_link = self.page.locator(click_selector).first
                await button_or_link.wait_for(state='visible', timeout=10000)
                await button_or_link.click()

            download: Download = await download_info.value
            suggested_filename: str = download.suggested_filename
            save_path: Path = save_dir_path / suggested_filename
            await download.save_as(save_path)
            logger.info(f"Файл '{suggested_filename}' успешно скачан в {save_path}")
            return f'Файл скачан: {save_path}'
        except PlaywrightError as ex: error_msg=ex.message.splitlines()[0]; logger.error(f"Ошибка Playwright при скачивании '{click_selector}': {error_msg}", exc_info=False); return f"Ошибка скачивания '{click_selector}': {error_msg}"
        except Exception as ex: logger.error(f"Ошибка при скачивании '{click_selector}'.", ex, exc_info=True); return f"Ошибка скачивания '{click_selector}': {str(ex)}"

# =============================================================

# === JavaScriptExecutionController Class Definition (Async Version) ===
class JavaScriptExecutionController:
    """ Выполняет произвольный JavaScript на странице (Async Version). """
    page: Page
    def __init__(self, page: Page) -> None:
        if not page or page.is_closed(): raise ValueError('JavaScriptExecutionController требует активный объект страницы.')
        self.page = page; logger.debug('JavaScriptExecutionController инициализирован.')

    async def execute_script(self, script: str) -> Union[str, Any]:
        """ Асинхронно выполняет JS-код и возвращает результат. """
        logger.warning(f'Выполнение JavaScript (ОСТОРОЖНО!): {script[:100]}...')
        if not self.page or self.page.is_closed(): return 'Ошибка: Страница закрыта.'
        try:
            result: Any = await self.page.evaluate(script)
            logger.info(f'JavaScript выполнен успешно. Результат: {str(result)[:100]}...')
            try: return json.dumps(result) # Попытка вернуть JSON
            except TypeError: return str(result) # Возврат строки, если не JSON
        except PlaywrightError as ex: error_msg=ex.message.splitlines()[0]; logger.error(f'Ошибка Playwright при выполнении JS: {error_msg}', exc_info=False); return f'Ошибка выполнения JS: {error_msg}'
        except Exception as ex: logger.error('Ошибка при выполнении JS.', ex, exc_info=True); return f'Ошибка выполнения JS: {str(ex)}'

# =============================================================

# === StateManager Class Definition (Async Version) ===
class StateManager:
    """ Управляет состоянием сессии (Async Version). """
    context: BrowserContext
    page: ContextPage # Опционально
    def __init__(self, context: BrowserContext, page: ContextPage = None) -> None:
         if not context or context.is_closed(): raise ValueError('StateManager требует активный контекст браузера.')
         self.context = context; self.page = page; logger.debug('StateManager инициализирован.')

    async def get_cookies(self, url: Optional[str] = None) -> Union[List[Dict[str, Any]], str]:
        """ Асинхронно возвращает куки для текущего контекста. """
        logger.info(f"Получение cookies (URL: {url or 'Все'})")
        if not self.context or self.context.is_closed(): return 'Ошибка: Контекст браузера закрыт.'
        try: cookies: List[Dict[str, Any]] = await self.context.cookies(urls=[url] if url else None); logger.info(f'Получено {len(cookies)} cookies.'); return cookies
        except Exception as ex: logger.error('Ошибка при получении cookies.', ex, exc_info=True); return f'Ошибка получения cookies: {str(ex)}'

    async def add_cookies(self, cookies: List[Dict[str, Any]]) -> str:
        """ Асинхронно добавляет куки в текущий контекст. """
        count: int = len(cookies); logger.info(f'Добавление {count} cookies...')
        if not self.context or self.context.is_closed(): return 'Ошибка: Контекст браузера закрыт.'
        try: await self.context.add_cookies(cookies); logger.info(f'{count} cookies успешно добавлены.'); return f'{count} cookies добавлены.'
        except Exception as ex: logger.error('Ошибка при добавлении cookies.', ex, exc_info=True); return f'Ошибка добавления cookies: {str(ex)}'

    async def clear_cookies(self) -> str:
        """ Асинхронно очищает все куки в текущем контексте. """
        logger.info('Очистка cookies...')
        if not self.context or self.context.is_closed(): return 'Ошибка: Контекст браузера закрыт.'
        try: await self.context.clear_cookies(); logger.info('Cookies очищены.'); return 'Cookies очищены.'
        except Exception as ex: logger.error('Ошибка при очистке cookies.', ex, exc_info=True); return f'Ошибка очистки cookies: {str(ex)}'

    async def clear_storage(self) -> str:
        """ Асинхронно очищает localStorage и sessionStorage. """
        logger.info('Очистка localStorage и sessionStorage...')
        if not self.page or self.page.is_closed(): return 'Ошибка: Страница закрыта для очистки storage.'
        try: await self.page.evaluate('() => { localStorage.clear(); sessionStorage.clear(); }'); logger.info('localStorage и sessionStorage очищены.'); return 'localStorage и sessionStorage очищены.'
        except Exception as ex: logger.error('Ошибка при очистке storage.', ex, exc_info=True); return f'Ошибка очистки storage: {str(ex)}'

    # login остается синхронной заглушкой
    def login(self, *args: Any, **kwargs: Any) -> str:
         """ Метод-заглушка для выполнения входа на сайт. """
         logger.warning('Метод login в StateManager является заглушкой.'); return 'Заглушка: Вход не реализован.'

# =============================================================
