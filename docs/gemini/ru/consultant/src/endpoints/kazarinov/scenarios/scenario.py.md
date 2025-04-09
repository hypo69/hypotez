### **Анализ кода модуля `scenario.py`**

## Качество кода:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код структурирован и разделен на функции и классы, что облегчает понимание и поддержку.
  - Используются аннотации типов, что повышает читаемость и облегчает отладку.
  - Присутствует логирование ошибок с использованием модуля `logger`.
  - Используется асинхронный код для неблокирующих операций.
- **Минусы**:
  - Есть смешанные стили кавычек (используются как одинарные, так и двойные кавычки).
  - Не все функции и классы имеют подробные docstring, особенно это касается внутренних функций.
  - В некоторых местах используются `...` вместо реализации, что затрудняет понимание полного функционала.
  - Не везде используется `logger.error` с передачей исключения `ex` и `exc_info=True`.
  - Не все переменные аннотированы типами.

## Рекомендации по улучшению:
- [ ] **Форматирование**:
  - Заменить все двойные кавычки на одинарные.
  - Обеспечить единообразное форматирование кода в соответствии с PEP8.
- [ ] **Docstring**:
  - Добавить подробные docstring для всех функций и классов, включая описание параметров, возвращаемых значений и возможных исключений.
  - Перевести все docstring на русский язык.
- [ ] **Логирование**:
  - Убедиться, что все ошибки логируются с использованием `logger.error` и передачей исключения `ex` и `exc_info=True`.
- [ ] **Обработка исключений**:
  - Использовать `ex` вместо `e` в блоках обработки исключений.
- [ ] **Аннотации типов**:
  - Добавить аннотации типов для всех переменных, где это необходимо.
- [ ] **Использовать `j_loads` или `j_loads_ns`**:
   - Для чтения JSON или конфигурационных файлов замените стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns`.
- [ ] **webdriver**:
    - В коде используется webdriver. Он импртируется из модуля `webdriver` проекта `hypotez`
```python
from src.webdirver import Driver, Chrome, Firefox, Playwright, ...
driver = Driver(Firefox)

После чего может использоваться как

close_banner = {
  "attribute": null,
  "by": "XPATH",
  "selector": "//button[@id = 'closeXButton']",
  "if_list": "first",
  "use_mouse": false,
  "mandatory": false,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": "click()",
  "locator_description": "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
}

result = driver.execute_locator(close_banner)
```

## Оптимизированный код:
```python
                ## \file /src/endpoints/kazarinov/scenarios/scenario.py
# -*- coding: utf-8 -*-\n
#! .pyenv/bin/python3
"""
Модуль сценария для Казаринова
==============================

Этот модуль содержит класс :class:`Scenario`, который используется для выполнения сценариев сбора информации
с веб-страниц, обработки данных с использованием AI и формирования отчетов.

Пример использования:
----------------------

>>> s = Scenario(window_mode='headless')
>>> asyncio.run(s.run_scenario_async(urls=['https://example.com'], mexiron_name='test_quotation'))
"""

from bs4 import BeautifulSoup
import requests
import telebot
import asyncio
from pathlib import Path
from typing import Optional, List

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

##############################################################

ENDPOINT: str = 'kazarinov'

#############################################################


def fetch_target_urls_onetab(one_tab_url: str) -> tuple[str, str, list[str]] | bool:
    """
    Извлекает целевые URL из OneTab URL.

    Args:
        one_tab_url (str): URL OneTab для парсинга.

    Returns:
        tuple[str, str, list[str]] | bool: Кортеж, содержащий цену, имя Mexiron и список URL,
        или False, False, False в случае ошибки.

    Raises:
        requests.exceptions.RequestException: Если возникает ошибка при выполнении запроса.
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
        # Обработка ошибки при выполнении запроса
        return False, False, False


class Scenario(QuotationBuilder):
    """
    Исполнитель сценария для Казаринова.

    Этот класс наследуется от QuotationBuilder и предназначен для сбора информации о товарах,
    обработки данных с использованием AI и формирования отчетов.
    """

    def __init__(self, mexiron_name: Optional[str] = gs.now, driver: Optional[Firefox | Playwrid | str] = None, **kwards):
        """
        Инициализирует сценарий сбора информации.

        Args:
            mexiron_name (Optional[str], optional): Имя Mexiron. По умолчанию gs.now.
            driver (Optional[Firefox | Playwrid | str], optional): Драйвер для управления браузером. По умолчанию None.
            **kwards: Дополнительные параметры.
        """
        # Установка режима окна, если он не задан
        if 'window_mode' not in kwards:
            kwards['window_mode'] = 'normal'

        self.driver = Driver(Firefox, **kwards) if not driver else driver

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
        Выполняет сценарий: парсит продукты, обрабатывает их с помощью AI и сохраняет данные.

        Args:
            urls (List[str]): Список URL для парсинга.
            price (Optional[str], optional): Цена. По умолчанию ''.
            mexiron_name (Optional[str], optional): Имя Mexiron. По умолчанию gs.now.
            bot (Optional[telebot.TeleBot], optional): Telegram бот для отправки сообщений. По умолчанию None.
            chat_id (Optional[int], optional): ID чата Telegram для отправки сообщений. По умолчанию 0.
            attempts (int, optional): Количество попыток парсинга. По умолчанию 3.

        Returns:
            bool: True, если выполнение успешно, иначе False.
        """

        products_list: list = []

        # -------------------------------------------------
        # 1. Сбор товаров

        lang_index: int = 2
        for url in urls:
            kwards: dict = {}
            graber = get_graber_by_supplier_url(self.driver, url, lang_index, **kwards)

            if not graber:
                logger.error(f'Нет грабера для: {url}')
                if bot:
                    bot.send_message(chat_id, f'Нет грабера для: {url}')
                # Пропуск URL, если грабер не найден
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
                    #  пропустить этот язык
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
            await reporter.create_reports_async(
                bot=bot,
                chat_id=chat_id,
                data=data,
                lang=lang,
                mexiron_name=self.mexiron_name
            )

        return True  # Возвращаем True в конце


def run_sample_scenario():
    """"""
    ...
    urls_list: list[str] = [
        'https://www.morlevi.co.il/product/21039',
        'https://www.morlevi.co.il/product/21018',
        'https://www.ivory.co.il/catalog.php?id=85473',
        'https://grandadvance.co.il/eng/?go=products&action=view&ties_ids=801&product_id=28457--SAMSUNG-SSD-1TB-990-EVO-PCle-4.0-x4--5.0-x2-NVMe',
        'https://www.ivory.co.il/catalog.php?id=85473',
        'https://www.morlevi.co.il/product/21018'
    ]

    s = Scenario(window_mode='headless')
    asyncio.run(s.run_scenario_async(urls=urls_list, mexiron_name='test price quotation', ))


if __name__ == '__main__':
    run_sample_scenario()