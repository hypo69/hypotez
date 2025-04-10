### **Анализ кода модуля `scenario.py`**

## Качество кода:

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Использование `logger` для логирования.
    - Наличие аннотаций типов.
    - Четкая структура кода, разделенная на функции и классы.
- **Минусы**:
    - Отсутствие документации модуля.
    - Использование смешанного стиля кавычек (в основном, двойные кавычки вместо одинарных).
    - Неполные docstring для функций и классов.
    - Отсутствие обработки исключений в некоторых местах.
    - Некоторые переменные не аннотированы типами.

## Рекомендации по улучшению:

1.  **Документация модуля**:
    - Добавить docstring в начале файла с описанием модуля, его назначения и примеров использования.
2.  **Форматирование кода**:
    - Привести все строки к использованию одинарных кавычек (`'`).
    - Добавить пробелы вокруг операторов присваивания (`=`).
3.  **Docstring**:
    - Заполнить docstring для всех функций и классов, включая описание аргументов, возвращаемых значений и возможных исключений.
    - Перевести все docstring на русский язык.
4.  **Обработка исключений**:
    - Убедиться, что все потенциально опасные операции обернуты в блоки `try...except` с логированием ошибок.
    - Использовать конкретные типы исключений вместо общего `Exception`.
5.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных, где это возможно.
6.  **Использование `j_dumps`**:
    - Убедиться, что `j_dumps` используется для записи JSON-файлов.
7.  **Комментарии**:
    - Пересмотреть и, при необходимости, уточнить существующие комментарии.
8.  **webdriver**:
    - Удостовериться, что webdriver создается через `Driver(Firefox)` или `Driver(Playwright)` и используется единообразно.

## Оптимизированный код:

```python
## \file /src/endpoints/kazarinov/scenarios/scenario.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
Модуль сценариев для endpoint-а kazarinov
==============================================

Модуль содержит класс :class:`Scenario`, который используется для выполнения сценариев сбора и обработки данных
для endpoint-а kazarinov.

Пример использования
----------------------

>>> s = Scenario(window_mode='headless')
>>> asyncio.run(s.run_scenario_async(urls=urls_list, mexiron_name='test price quotation'))
"""

from bs4 import BeautifulSoup
import requests
import telebot
import asyncio
from pathlib import Path
from typing import Optional, List, Tuple, TYPE_CHECKING

import header
from src import gs
from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox
from src.webdriver.playwright import Playwrid
from src.ai.gemini import GoogleGenerativeAI
from src.endpoints.kazarinov.report_generator.report_generator import ReportGenerator
from src.endpoints.kazarinov.scenarios.quotation_builder import QuotationBuilder
from src.endpoints.prestashop.product_fields.product_fields import ProductFields
from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_url
from src.utils.jjson import j_dumps
from src.logger.logger import logger

if TYPE_CHECKING:
    from src.grabber.base import Graber

##############################################################

ENDPOINT = 'kazarinov'

#############################################################


def fetch_target_urls_onetab(one_tab_url: str) -> Tuple[str, str, List[str]] | Tuple[bool, bool, bool]:
    """
    Извлекает целевые URL-адреса из OneTab URL.

    Args:
        one_tab_url (str): URL OneTab для парсинга.

    Returns:
        Tuple[str, str, List[str]] | Tuple[bool, bool, bool]: Кортеж, содержащий цену, имя Mexiron и список URL-адресов.
        Возвращает (False, False, False) в случае ошибки.

    Raises:
        requests.exceptions.RequestException: Если возникает ошибка при выполнении HTTP-запроса.

    Example:
        >>> url = 'http://example.com/onetab'
        >>> price, mexiron_name, urls = fetch_target_urls_onetab(url)
        >>> print(price, mexiron_name, urls)
        0, 'example', ['http://example.com']
    """
    try:
        response = requests.get(one_tab_url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Извлечение ссылок
        urls = [a['href'] for a in soup.find_all('a', class_='tabLink')]

        # Извлечение данных из div с классом 'tabGroupLabel'
        element = soup.find('div', class_='tabGroupLabel')
        data = element.get_text() if element else None

        if not data:
            price = ''
            mexiron_name = gs.now
        else:
            # Разбивка данных на цену и имя
            parts = data.split(maxsplit=1)
            price = int(parts[0]) if parts[0].isdigit() else ''
            mexiron_name = parts[1] if len(parts) > 1 else gs.now

        return price, mexiron_name, urls

    except requests.exceptions.RequestException as ex:
        logger.error(f'Ошибка при выполнении запроса: {one_tab_url=}', ex, exc_info=True)
        return False, False, False


class Scenario(QuotationBuilder):
    """Исполнитель сценария для Казаринова"""

    def __init__(self, mexiron_name: Optional[str] = gs.now, driver: Optional[Firefox | Playwrid | str] = None, **kwards):
        """
        Инициализирует сценарий сбора информации.

        Args:
            mexiron_name (Optional[str], optional): Имя Mexiron. По умолчанию gs.now.
            driver (Optional[Firefox | Playwrid | str], optional): Драйвер для использования. По умолчанию None.
            **kwards: Дополнительные параметры для передачи драйверу.
        """

        if 'window_mode' not in kwards:
            kwards['window_mode'] = 'normal'

        self.driver: Driver = Driver(Firefox, **kwards) if not driver else driver

        super().__init__(mexiron_name=mexiron_name, driver=self.driver, **kwards)

    async def run_scenario_async(
        self,
        urls: List[str],
        price: Optional[str] = '',
        mexiron_name: Optional[str] = gs.now,
        bot: Optional[telebot.TeleBot] = None,
        chat_id: Optional[int] = 0,
        attempts: int = 3,
    ) -> bool:
        """
        Выполняет сценарий: парсит продукты, обрабатывает их через AI и сохраняет данные.

        Args:
            urls (List[str]): Список URL-адресов продуктов для обработки.
            price (Optional[str], optional): Цена. По умолчанию ''.
            mexiron_name (Optional[str], optional): Имя Mexiron. По умолчанию gs.now.
            bot (Optional[telebot.TeleBot], optional): Telegram бот для отправки уведомлений. По умолчанию None.
            chat_id (Optional[int], optional): ID чата для отправки уведомлений. По умолчанию 0.
            attempts (int, optional): Количество попыток при сборе данных. По умолчанию 3.

        Returns:
            bool: True, если сценарий выполнен успешно, иначе False.
        """

        products_list: List[dict] = []

        # -------------------------------------------------
        # 1. Сбор товаров

        lang_index: int = 2
        for url in urls:
            kwards: dict = {}
            graber: 'Graber' = get_graber_by_supplier_url(self.driver, url, lang_index, **kwards)

            if not graber:
                logger.error(f'Нет грабера для: {url}')
                if bot:
                    bot.send_message(chat_id, f'Нет грабера для: {url}')
                continue

            f: ProductFields = None
            if bot:
                bot.send_message(chat_id, f'Process: {url}')
            try:
                f = await graber.grab_page_async(*self.required_fields)
            except Exception as ex:
                logger.error(f'Failed... Ошибка получения полей товара {url}:', ex, exc_info=True)
                if bot:
                    bot.send_message(chat_id, f'Failed... Ошибка получения полей товара {url}\\n{ex}')
                continue

            if not f:
                logger.error(f'Failed to parse product fields for URL: {url}')
                if bot:
                    bot.send_message(chat_id, f'Failed to parse product fields for URL: {url}')
                continue

            product_data = self.convert_product_fields(f)
            if not product_data:
                logger.error(f'Failed to convert product fields: {product_data}')
                if bot:
                    bot.send_message(chat_id, f'Failed to convert product fields {url} \\n {product_data}')
                continue

            await self.save_product_data(product_data)
            products_list.append(product_data)

        # -----------------------------------------------------
        # 2. AI processing

        """ список компонентов сборки компьютера уходит в обработку моделью (`gemini`) ->
        модель парсит данные, делает перевод на `ru`, `he` и возвращает кортеж словарей по языкам.
        Внимание! модель может ошибаться"""

        langs_list: list = ['he', 'ru']

        for lang in langs_list:
            if bot:
                bot.send_message(
                    chat_id,
                    f'AI processing {lang=}',
                )
            try:
                data: dict = await self.process_ai_async(products_list, lang)
                if not data:
                    if bot:
                        bot.send_message(chat_id, f'Ошибка модели для {lang=}')
                    # пропустить этот язык
                    continue
            except Exception as ex:
                logger.error(f'AI processing failed for {lang=}', ex, exc_info=True)
                if bot:
                    bot.send_message(chat_id, f'AI processing failed for {lang=}: {ex}')
                continue

            # -----------------------------------------------------------------
            # 3. Report creating

            if bot:
                bot.send_message(chat_id, f'Создаю файл')
            data = data[lang]
            data['price'] = price
            data['currency'] = getattr(self.translations.currency, lang, "ש''ח")

            j_dumps(data, self.export_path / f'{self.mexiron_name}_{lang}.json')

            reporter = ReportGenerator(if_need_docx=False)
            await reporter.create_reports_async(bot=bot, chat_id=chat_id, data=data, lang=lang, mexiron_name=self.mexiron_name)

        return True  # Возвращаем True в конце


def run_sample_scenario():
    """
    Запускает пример сценария.
    """
    ...
    urls_list: list[str] = [
        'https://www.morlevi.co.il/product/21039',
        'https://www.morlevi.co.il/product/21018',
        'https://www.ivory.co.il/catalog.php?id=85473',
        'https://grandadvance.co.il/eng/?go=products&action=view&ties_ids=801&product_id=28457--SAMSUNG-SSD-1TB-990-EVO-PCle-4.0-x4--5.0-x2-NVMe',
        'https://www.ivory.co.il/catalog.php?id=85473',
        'https://www.morlevi.co.il/product/21018',
    ]

    s = Scenario(window_mode='headless')
    asyncio.run(s.run_scenario_async(urls=urls_list, mexiron_name='test price quotation'))


if __name__ == '__main__':
    run_sample_scenario()