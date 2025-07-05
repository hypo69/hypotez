# -*- coding: utf-8 -*-
#! .pyenv/bin/python3
"""
Сценарий для Казаринова
=========================

.. module:: src.endpoints.kazarinov.scenarios.scenario 
	:platform: Windows, Unix
	:synopsis: Сценарий для Казаринова

"""

from bs4 import BeautifulSoup
import requests
import telebot
import asyncio
from pathlib import Path
from typing import Optional, List

import header
from src import gs

# Предполагается, что Driver из use_pydoll возвращает объект с атрибутом 'page'
from src.webdriver.driverless.use_pydoll import Driver

from src.endpoints.kazarinov.report_generator.report_generator import ReportGenerator
from src.endpoints.kazarinov.scenarios.quotation_builder import QuotationBuilder
from src.endpoints.prestashop.product_fields.product_fields import ProductFields
from src.suppliers.get_pydoll_graber_by_supplier import get_graber_by_supplier_url

from src.utils.jjson import j_dumps
from src.logger.logger import logger
from dataclasses import dataclass, field

@dataclass
class Config:

    ENDPOINT:str = "kazarinov"


class Scenario(QuotationBuilder):
    """Исполнитель сценария для Казаринова"""

    def __init__(self, mexiron_name:Optional[str] = gs.now,  **kwargs):
        """Сценарий сбора информации."""

        if 'window_mode' not in kwargs:
            kwargs['window_mode'] = 'normal'

        # Важно: Конструктор Driver сам управляет своим жизненным циклом и окном.
        # Если передается внешний драйвер, то нужно передавать его сюда.
        # В данном случае, Driver() создается внутри run_scenario_async.
        # self.driver = Driver(Firefox,**kwargs) if not driver else driver # Эта строка, похоже, не нужна здесь, если Driver создается в run_scenario_async

        super().__init__(mexiron_name = mexiron_name)
        

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
        Executes the scenario: parses products, processes them via AI, and stores data.
        """

        driver_instance = None # Инициализируем переменную для экземпляра драйвера
        try:
            # Создаем новый экземпляр драйвера здесь, для каждой операции сценария
            driver_instance = Driver() # Возможно, тут нужно передавать конфиг или параметры окна
            await driver_instance.start()
            
            # Получаем объект страницы из экземпляра драйвера
            page_obj = driver_instance.page 
            logger.info(f'pydoll driver started ')
        except Exception as ex:
            logger.error(f'Ошибка запуска pygoll вебдрайвера', exc_info=ex, extra={'chat_id': chat_id, 'bot': bot}) # Добавляем контекст для логгирования
            if bot: bot.send_message(chat_id, f"❌ Ошибка запуска вебдрайвера. Отмена сценария.")
            return False

        products_list = [] # Список для собранных продуктов

        # -------------------------------------------------
        # 1. Сбор товаров
        lang_index: int = 2 # Эта переменная не используется в цикле
        
        # Если в 'urls' переданы URL категорий, то нужно сначала получить список URL товаров.
        # Текущий код предполагает, что в 'urls' уже есть URL конкретных товаров.
        # Если это не так, то понадобится дополнительный цикл для обработки категорий.
        
        # Проверим, что у нас есть page_obj (экземпляр драйвера) перед началом.
        if not page_obj:
            logger.error("page_obj не был инициализирован. Невозможно продолжить сбор товаров.")
            if bot: bot.send_message(chat_id, "❌ Внутренняя ошибка: вебдрайвер не инициализирован.")
            # В случае, если драйвер не стартанул, нужно его корректно закрыть
            if driver_instance:
                try:
                    await driver_instance.stop()
                except Exception as e:
                    logger.error(f"Ошибка при остановке драйвера: {e}")
            return False

        for url in urls:
            # Важно: Здесь предполагается, что 'url' это URL КОНКРЕТНОГО товара.
            # Если это URL КАТЕГОРИИ, то код get_graber_by_supplier_url и далее grab_product_page не подойдет.
            # В таком случае, нужно сначала получить список URL товаров из категории, используя yield_all_scenarios или yield_scenario.
            
            logger.info(f"Обработка URL: {url}")

            # Пытаемся получить грабер для данного URL
            graber: 'Graber' = get_graber_by_supplier_url(url)
            
            if not graber:
                logger.error(f"Нет подходящего грабера для URL: {url}")
                if bot: bot.send_message(chat_id, f"❌ Не найден обработчик для ссылки: {url}")
                continue # Переход к следующему URL

            # Определяем поля, которые хотим извлечь.
            # В данном случае, это фиксированный список.
            required_fields: list[str]  = ['id_product',
                        'name',
                        'price',
                        'id_supplier',
                        'description_short',
                        'description',
                        'specification',
                        'local_image_path',
                        'default_image_url']

            if bot: 
                try:
                    bot.send_message(chat_id, f"⏳ Обработка товара:\n{url}") 
                except Exception as e:
                    logger.error(f"Ошибка отправки сообщения ботом: {e}")

            try:
                # --- ИСПРАВЛЕННЫЙ ВЫЗОВ ---
                # Передаем URL, экземпляр page_obj (драйвер), и список требуемых полей.
                f: ProductFields = await graber.grab_product_page(
                    product_url=url, 
                    driver_instance=page_obj, # <-- Передаем здесь экземпляр Page
                    actual_fields=required_fields
                )
                # --- КОНЕЦ ИСПРАВЛЕННОГО ВЫЗОВА ---

                # Проверка, что поля были успешно извлечены
                if not f or not f.name: # Простая проверка, что хоть какое-то основное поле было заполнено
                    logger.error(f"Не удалось получить основные поля товара для URL: {url}. Проверьте локаторы.")
                    if bot: bot.send_message(chat_id, f"❌ Ошибка парсинга товара:\n{url}\nПроверьте локаторы.") 
                    continue # Переход к следующему URL

                # Конвертация и сохранение данных
                product_data = self.convert_product_fields(f)
                if not product_data:
                    logger.error(f"Не удалось конвертировать извлеченные поля товара для URL: {url}. Получены некорректные данные: {f}")
                    if bot: bot.send_message(chat_id, f"❌ Ошибка конвертации данных для товара:\n{url}") 
                    continue # Переход к следующему URL

                await self.save_product_data(product_data) 
                products_list.append(product_data)
                
                # Если нужно закрывать драйвер после каждого товара, то здесь:
                # driver.close() # Но обычно драйвер держат открытым для всей сессии
                
            except Exception as ex:
                logger.error(f"Произошла ошибка при обработке товара по URL {url}:", ex, )
                if bot: bot.send_message(chat_id, f"❌ Произошла ошибка при обработке товара {url}:\n{ex}") 
                continue # Если хотим пропустить только этот товар, но продолжить остальные

        # --- ВАЖНОЕ ЗАМЕЧАНИЕ ПО ПОВОДУ ДРАЙВЕРА ---
        # Если ваш цикл по URL'ам очень длинный, и вы не закрываете драйвер,
        # то может закончиться память. В данном коде драйвер не закрывается.
        # Если вы обрабатываете URL'ы категорий, а не конкретные товары,
        # то этот цикл будет работать иначе.
        # В текущем виде, driver_instance будет закрыт только после всего сценария.
        # Если бы вы обрабатывали URL'ы категорий, то внутри цикла вы могли бы использовать yield_all_scenarios,
        # который бы возвращал генератор товаров, и вы бы итерировались по нему.
        
        # --- Пересмотрел логику драйвера ---
        # Если сценарий состоит из обработки множества товаров, и каждый товар может быть 
        # на отдельном сайте (т.е. нужен новый грабер/драйвер), то
        # driver_instance лучше создавать внутри цикла для каждого URL, если graber_via_pydoll
        # не переиспользует драйвер между вызовами.
        # Но если get_graber_by_supplier_url возвращает один и тот же класс Graber,
        # и grab_product_page умеет работать с разными сайтами на одном драйвере,
        # то текущий подход (один драйвер на все URL'ы в этом сценарии) более эффективен.
        # Я оставил один драйвер на весь run_scenario_async, но добавил условие выхода из цикла
        # если драйвер не работает.

        # Если сбор товаров был успешным и есть хотя бы один продукт
        if not products_list:
             logger.warning("Не было собрано ни одного товара для этого сценария.")
             # Если бот был предоставлен, отправляем уведомление
             if bot and chat_id:
                 try:
                     bot.send_message(chat_id, "⚠️ Не удалось собрать информацию ни об одном товаре.")
                 except Exception as e:
                     logger.error(f"Ошибка отправки сообщения ботом: {e}")
             # Можно вернуть False, если отсутствие товаров считается ошибкой сценария
             # return False 

        # -----------------------------------------------------
        # 2. AI processing

        """ список компонентов сборки компьютера уходит в обработку моделью (`gemini`) ->
        модель парсит данные, делает перевод на `ru`, `he` и возвращает кортеж словарей по языкам.
        Внимание! модель может ошибаться"""

        langs_list: list = ["he", "ru"]

        for lang in langs_list:
            if bot and chat_id: 
                try:
                    bot.send_message( 
                        chat_id,
                        f"""AI обработка ({lang})... 🤖""",
                    )
                except Exception as e:
                    logger.error(f"Ошибка отправки сообщения ботом: {e}")
            
            # Проверяем, что у нас есть собранные продукты для обработки AI
            if not products_list:
                logger.warning(f"Нет собранных продуктов для AI обработки на языке {lang}.")
                if bot and chat_id: bot.send_message(chat_id, f"⚠️ Нет данных для AI обработки на языке {lang}.")
                continue

            try:
                # process_llm_async ожидает список собранных product_data, не ProductFields
                data: dict = await self.process_llm_async(products_list, lang)
                if not data:
                    logger.error(f"AI обработка для {lang=} вернула пустые данные.")
                    if bot and chat_id: bot.send_message(chat_id, f"❌ AI обработка для {lang=} не дала результатов.")
                    continue # Пропустить этот язык
            except Exception as ex:
                logger.exception(f"AI обработка не удалась для {lang=}:") # Используем exception для стека
                if bot and chat_id: bot.send_message(chat_id, f"❌ Ошибка AI обработки для {lang=}: {ex}")
                continue


            # -----------------------------------------------------------------
            # 3. Report creating

            if bot and chat_id: 
                try:
                    bot.send_message(chat_id, f"📈 Создание отчета ({lang})...")
                except Exception as e:
                    logger.error(f"Ошибка отправки сообщения ботом: {e}")

            # Проверяем, что data для текущего языка существует
            if lang not in data or not data[lang]:
                logger.warning(f"Отсутствуют данные для языка '{lang}' после обработки AI.")
                if bot and chat_id: bot.send_message(chat_id, f"⚠️ Отсутствуют данные для AI отчета на языке '{lang}'.")
                continue

            processed_data_for_lang = data[lang]
            processed_data_for_lang["price"] = price
            # Используем getattr с default на случай, если валюты для языка нет
            processed_data_for_lang["currency"] = getattr(self.translations.currency, lang, "ש''ח") # Предполагается, что self.translations и currency доступны

            # Сохраняем сырые данные после AI обработки
            try:
                j_dumps(processed_data_for_lang, self.export_path / f'{self.mexiron_name}_{lang}.json')
            except Exception as ex:
                logger.error(f"Не удалось сохранить JSON файл для {self.mexiron_name}_{lang}.json", exc_info=ex)


            # Создание отчетов
            reporter = ReportGenerator(if_need_docx=False) # Если нужно, передайте параметры
            try:
                await reporter.create_reports_async(
                    bot = bot, 
                    chat_id = chat_id,
                    data = processed_data_for_lang, # Передаем обработанные данные для текущего языка
                    lang = lang,
                    mexiron_name = self.mexiron_name
                )
            except Exception as ex:
                logger.error(f"Ошибка при создании отчета для {lang=}:", exc_info=ex)
                if bot and chat_id: bot.send_message(chat_id, f"❌ Ошибка создания отчета для {lang=}: {ex}")


        # --- ВАЖНО: Остановка драйвера ---
        # Драйвер, созданный в начале, должен быть остановлен в конце работы сценария,
        # чтобы освободить ресурсы (браузер, порты и т.д.).
        if driver_instance:
            try:
                logger.info("Остановка pydoll драйвера...")
                await driver_instance.stop()
                logger.info("pydoll драйвер успешно остановлен.")
            except Exception as ex:
                logger.error(f"Ошибка при остановке pydoll драйвера:", exc_info=ex)

        # Возвращаем True только если сценарий в целом завершился без критических ошибок,
        # даже если некоторые товары могли быть пропущены.
        # Если полное отсутствие товаров является ошибкой, можно добавить проверку `if not products_list: return False`
        return True # Возвращаем True в конце, если все прошло без фатальных ошибок


# --- Пример вызова ---
# Этот блок __main__ для тестирования сценария
def run_sample_scenario():
    """"""
    # Пример списка URL товаров. Для этого нужно, чтобы get_graber_by_supplier_url
    # правильно определял поставщика по этим URL и возвращал соответствующий Graber.
    urls_list:list[str] = [
        'https://www.morlevi.co.il/product/21039', # morlevi
        'https://www.morlevi.co.il/product/21018', # morlevi
        'https://www.ivory.co.il/catalog.php?id=85473', # ivory (это URL категории, если graber_via_pydoll его обрабатывает как товар)
        'https://grandadvance.co.il/eng/?go=products&action=view&ties_ids=801&product_id=28457--SAMSUNG-SSD-1TB-990-EVO-PCle-4.0-x4--5.0-x2-NVMe', # grandadvance
        # 'https://www.ivory.co.il/catalog.php?id=85473', # Дубликат
        # 'https://www.morlevi.co.il/product/21018' # Дубликат
        ]

    # Если вы хотите тестировать AI и генерацию отчетов, вам нужно будет настроить:
    # - telebot: например, создать фиктивного бота или использовать реального с тестовым токеном.
    # - self.translations.currency: убедитесь, что это доступно и правильно настроено.
    # - self.export_path: убедитесь, что эта директория существует.
    # - Возможно, потребуется мокать некоторые части process_llm_async и ReportGenerator для юнит-тестирования.
    
    # Пример запуска без бота (сообщения не будут отправляться)
    s = Scenario(window_mode = 'normal')
    print("Запуск тестового сценария...")
    # Если вы хотите видеть логи, убедитесь, что уровень логирования установлен на INFO или DEBUG
    # logger.setLevel(logging.INFO) 
    
    # run_sample_scenario вызывает run_scenario_async внутри себя, но сам run_sample_scenario
    # не является async функцией. Для корректного запуска asyncio.run() нужен async вызов.
    # Поэтому, run_sample_scenario должен быть обернут в async функцию, либо сам быть async.
    
    async def main_test_run():
        # Убедитесь, что для этого теста настроены пути и необходимые данные
        # для Scenario, ReportGenerator, и т.д.
        # Если вы передаете бота и chat_id, убедитесь, что они действительны.
        # Если нет, то сообщения ботом не будут работать.
        await s.run_scenario_async(
            urls=urls_list, 
            mexiron_name='test_kazarinov_run', 
            # bot=your_telebot_instance, # Раскомментируйте и настройте, если нужно
            # chat_id=your_chat_id # Раскомментируйте и настройте, если нужно
            price="100.50" # Пример цены
        )
        print("Тестовый сценарий завершен.")

    asyncio.run(main_test_run())


if __name__ == '__main__':
    # Запуск при выполнении скрипта напрямую
    run_sample_scenario()