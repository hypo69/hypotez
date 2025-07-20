## \file src/endpoints/kazarinov/scenarios/scenario.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
Сценарий для Казаринова
=======================

Модуль содержит конфигурацию и исполнитель сценария для эндпоинта `kazarinov`.

```rst
.. module:: src.endpoints.kazarinov.scenarios.scenario
```
"""

import asyncio
from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace
from typing import List, Optional

import telebot
from bs4 import BeautifulSoup  # noqa: F401  # BeautifulSoup может понадобиться при расширении сценария
import requests  # noqa: F401  # requests может понадобиться при расширении сценария

# Всегда загружаются по умолчанию -------------------------------------------------
from header import __root__
from src import gs, USE_ENV

# Внутренние модули проекта --------------------------------------------------------
from src.credentials import j_loads_ns
from src.endpoints.kazarinov.report_generator.report_generator import ReportGenerator
from src.endpoints.kazarinov.scenarios.quotation_builder import QuotationBuilder
from src.endpoints.prestashop.product_fields.product_fields import ProductFields
from src.logger.logger import logger
#from src.suppliers.get_pydoll_graber_by_supplier import get_graber_by_supplier_url
from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_url
from src.utils.jjson import j_dumps
from src.webdriver.pydoll.driver import Driver

class Config:
    """Конфигурация сценария."""
    
    ENDPOINT: str = 'kazarinov'
    config: SimpleNamespace = j_loads_ns(__root__ / "src" / "endpoints" / ENDPOINT / f"{ENDPOINT}.json")
    if not config:
        raise RuntimeError("Configuration not found for Kazarinov endpoint")
    _driver_cfg = getattr(config.webdriver, config.webdriver.active_driver, 'pydoll')
    WINDOW_MODE = getattr(_driver_cfg, "WINDOW_MODE", "window")
    user_profile_path = getattr(_driver_cfg, "profile_path", None)


@dataclass(slots=True, kw_only=True)
class Scenario(QuotationBuilder):
    """Исполнитель сценария для Казаринова."""

    async def run_scenario_async(
        self,
        mexiron_name:str,
        urls: List[str],
        price: str = "",
        bot: Optional[telebot.TeleBot] = None,
        chat_id: int = 0,
        attempts: int = 3,
    ) -> bool:
        """Запускает сценарий.

        Args:
            urls: Ссылки на товары (или категории).
            price: Цена для отчёта.
            bot: Телеграм‑бот для отправки статуса.
            chat_id: Идентификатор чата.
            attempts: Количество попыток перезапуска драйвера.

        Returns:
            bool: ``True`` при успешном завершении сценария.
        """
        products_list: list[dict] = []  # Список собранных товаров
        required_fields: list[str] = [
            "id_supplier",
            "name",
            "price",
            "reference",
            "description",
            "description_short",
            "specification",
            "default_image_url",
        ]
        try:
            driver = Driver(
                window_mode = Config.WINDOW_MODE,
                user_profile_path = Config.user_profile_path,
            )
        except Exception as ex:
            logger.error("Ошибка создания Driver", ex, exc_info=True)
            raise RuntimeError("Driver initialization failed") from ex


        async with driver:

            # Запуск браузера ------------------------------------------------------
            try:
                await driver.start()
                await driver.async_init_page()
            except Exception as ex:  # pragma: no cover
                if bot:
                    bot.send_message(chat_id, f"❌  Ошибка запуска pydoll драйвера")
                logger.error("❌ Ошибка запуска pydoll драйвера", ex, exc_info=True)
                return False

            # Сбор товаров ---------------------------------------------------------
            for url in urls:
                logger.debug(f"Обработка URL: {url}", None, False)

                graber = get_graber_by_supplier_url(url, driver)

                if not graber:
                    logger.error(f"🤷‍♂️ Нет подходящего грабера для URL: {url}", None, True)
                    if bot:
                        bot.send_message(chat_id, f"❌ Нет обработчика для ссылки:\n{url}")
                    continue
            


                if bot:
                    bot.send_message(chat_id, f"⏳ Сбор полей товара со страницы:\n{url}")

                logger.info(f'⏳ Сбор полей товара со страницы {url}', ex = None, exc_info = False, text_color = "light_gray")
                try:
                    await self.driver.get_url(url)
                    product_fields: ProductFields = await graber.grab_page_async(required_fields = required_fields)
                except Exception as ex: 
                    logger.error(f"❌ Ошибка парсинга страницы:{url}", ex, exc_info = True)
                    if bot:
                        bot.send_message(chat_id, f"❌ Ошибка парсинга страницы:\n{url}\n{ex}")
                    continue

                if not product_fields or not product_fields.name:

                    if bot:
                        bot.send_message(chat_id, f"❌ Ошибка парсинга товара:\n{url}\nПроверьте локаторы.")
                    logger.error(f"""❌ Ошибка парсинга товара:{url}
                    Проверьте локаторы.""", None, False, text_color="light_gray", bg_color="light_gray")
                    continue

                try:
                    # Конвертиртация поля из объекта `ProductFields` в простой словарь для модели llm
                    product_data = self.convert_product_fields(product_fields)

                    # Индивидуальные настройки поставщиков
                    match(graber.supplier_prefix):
                        case 'morlevi.co.il':
                            product_data['default_image_url'] = fr'https"://"morlevi.co.il/' + product_data['default_image_url'] 
                            ...
                        case 'grandadvance.co.il':
                            ...
                        case 'ksp.co.il':
                            ...
                        case 'ivory.co.il':
                            ...

                except Exception as ex:  
                    logger.error("Ошибка конвертации данных", ex, exc_info=True)
                    if bot:
                        bot.send_message(chat_id, f"❌ Ошибка конвертации:\n{url}")
                    continue

                await self.save_product_data(product_data)
                products_list.append(product_data)

        # AI‑обработка ---------------------------------------------------------
        if not products_list:
            logger.warning(" 😒 Не собрано ни одного товара", None, False)
            if bot:
                bot.send_message(chat_id, "⚠️ Не удалось собрать информацию ни об одном товаре.")
            await driver.stop()
            return False

        for lang in ("he", "ru"):
            if bot:
                bot.send_message(chat_id, f"🤖 AI обработка ({lang})...")

            try:
                data = await self.process_llm_async(products_list, lang)
            except Exception as ex:  # pragma: no cover
                logger.error("🤖 AI‑обработка упала", ex, exc_info=False)
                if bot:
                    bot.send_message(chat_id, f"❌ AI ошибка ({lang}):\n{ex}")
                continue

            if not data or lang not in data:
                if bot:
                    bot.send_message(chat_id, f"🤖 AI f'AI вернула пустой результат\nязык: {lang}\n{products_list=}'\n...")

                logger.warning(f'AI вернула пустой результат \n язык {lang} \n {products_list=}')
                continue

            processed = data[lang]
            processed["price"] = price
            processed["currency"] = getattr(self.translations.currency, lang, "ש''ח")

            try:
                j_dumps(processed, self.export_path / f"{self.mexiron_name}_{lang}.json")
            except Exception as ex:  # pragma: no cover
                logger.error("Не удалось сохранить JSON", ex, exc_info=True)

            logger.info("Сохранён JSON: ", self.export_path / f"{self.mexiron_name}_{lang}.json")
            


            # Генерация отчёта ---------------------------------------------------

            if bot:
                bot.send_message(chat_id, f"📈 Создание отчёта ({lang})...")

            logger.info(f"📈 Создание отчёта ({lang})...", ex=None, exc_info=False, text_color = "light_gray",)

            reporter = ReportGenerator(if_need_docx=False)
            
            if not await reporter.create_reports_async(
                    bot=bot,
                    chat_id=chat_id,
                    data=processed,
                    lang=lang,
                    mexiron_name = mexiron_name,
                ):

                logger.error("Ошибка генерации отчёта", ex, exc_info=True)
                if bot:
                    bot.send_message(chat_id, f"❌ Ошибка отчёта ({lang}):\n{ex}")
                return 

        return True

    def convert_product_fields(self, f: ProductFields) -> dict:
        """
        Converts product fields into a dictionary. 
        Функция конвертирует поля из объекта `ProductFields` в простой словарь для модели llm.

        Args:
            f (ProductFields): Object containing parsed product data.

        Returns:
            dict: Formatted product data dictionary.

        Note: 
            Правила построения полей определяются в `ProductFields`
        """
        if not f.reference:
            logger.error(f"Сбой при получении полей товара. ")
            return {} # <- сбой при получении полей товара. Такое может произойти если вместо страницы товара попалась страница категории, при невнимательном составлении мехирона из комплектующих
        ...

        product_name = f.name['language']['value'] if f.name else ''
        description = f.description['language']['value'] if f.description else ''
        description_short = f.description_short['language']['value'] if f.description_short else ''
        specification = f.specification['language']['value']  if f.specification else ''
        
        if not product_name:
            return {}
        return {
            'product_name':product_name,
            'reference': f.reference,
            'description_short':description_short,
            'description': description,
            'specification': specification,
            'local_image_path': str(f.local_image_path),
        }



# ----------------------------------------------------------------------------------
#                               Пример запуска                                      
# ----------------------------------------------------------------------------------

def run_sample_scenario() -> None:
    """Пример локального теста сценария."""
    urls_list: list[str] = [
        "https://www.morlevi.co.il/product/21039",
        "https://www.morlevi.co.il/product/21018",
        "https://www.ivory.co.il/catalog.php?id=85473",
        "https://grandadvance.co.il/eng/?go=products&action=view&ties_ids=801&product_id=28457--SAMSUNG-SSD-1TB-990-EVO-PCle-4.0-x4--5.0-x2-NVMe",
    ]

    scenario = Scenario()
    logger.info("Запуск тестового сценария…")

    async def _runner() -> bool:
        if await scenario.run_scenario_async(
            urls=urls_list,
            mexiron_name="test_kazarinov_run",
            price="100.50",
            # bot=your_telebot_instance,
            # chat_id=your_chat_id,
            ):
            logger.info("Тестовый сценарий завершён")
            return True
        return

    asyncio.run(_runner())


if __name__ == "__main__":
    run_sample_scenario()
