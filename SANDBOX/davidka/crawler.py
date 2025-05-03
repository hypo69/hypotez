## \file /sandbox/davidka/crawler.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для сбора данных со страниц товаров с различных сайтов
=====================================================
Использует WebDriver для взаимодействия со страницами и LLM для извлечения
структурированной информации на основе инструкций. Обрабатывает задачи
по сбору данных о товарах по URL, по категориям, извлечению категорий
с сайтов поставщиков и поиску товаров на заданных доменах.

```rst
.. module:: sandbox.davidka.crawler
```
"""
import asyncio
import random # Используется для перемешивания списков (хотя сейчас закомментировано)
from pathlib import Path
from types import SimpleNamespace
from typing import List, Optional, Dict, Any, Set # Добавлены Dict, Any, Optional, List, Set

# --- Импорты проекта ---
import header
from header import __root__
from src import gs
from src.webdriver.llm_driver import Driver # SimpleDriver не используется
from src.utils.jjson import j_loads, j_dumps # j_loads_ns не используется
from src.utils.file import read_text_file, save_text_file, get_filenames_from_directory
from src.utils.url import get_domain
from src.utils.string.ai_string_utils import normalize_answer

from src.utils.printer import pprint as print
from src.logger.logger import logger

# Импорт утилит из соседнего файла utils.py
from . import utils

# --- Конфигурация ---
class Config:
    """ Класс для хранения конфигурационных параметров Crawler """
    # --- Пути ---
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    MINING_DATA_PATH: Path = ENDPOINT / 'random_urls'
    TRAIN_DATA_SUPPLIER_CATEGORIES_PATH: Path = ENDPOINT / 'train_data_supplier_categories'
    INSTRUCTIONS_PATH: Path = ENDPOINT / 'instructions'
    CHECKED_DOMAINS_TXT_PATH: Path = ENDPOINT / 'checked_domains.txt'
    CHECKED_DOMAINS_JSON_PATH: Path = ENDPOINT / 'checked_domains.json'

    # --- Загружаемые данные (инициализируются в load_config) ---
    checked_domains: List[str] = []
    crawl_files_list: List[str] = []
    instruction_grab_product_page: str = ''
    instruction_get_supplier_categories: str = ''
    instruction_find_product_in_supplier_domain: str = ''

    # --- WebDriver ---
    driver: Optional[Driver] = None

    @classmethod
    def load_config(cls) -> None:
        """
        Метод для загрузки конфигурации из файлов и инициализации WebDriver.
        Вызывается один раз при старте.
        """
        logger.info("Загрузка конфигурации Crawler...")

        # Загрузка проверенных доменов
        cls.checked_domains = read_text_file(cls.CHECKED_DOMAINS_TXT_PATH, as_list=True) or []
        logger.info(f"Загружено {len(cls.checked_domains)} проверенных доменов.")

        # Загрузка списка файлов для обработки
        # Используем '*.json', чтобы найти все json файлы
        cls.crawl_files_list = get_filenames_from_directory(cls.MINING_DATA_PATH, '*.json')
        logger.info(f"Найдено {len(cls.crawl_files_list)} файлов для обработки в {cls.MINING_DATA_PATH}.")

        # Загрузка текстов инструкций
        try:
            cls.instruction_grab_product_page = (cls.INSTRUCTIONS_PATH / 'grab_product_page.md').read_text(encoding='utf-8')
            cls.instruction_get_supplier_categories = (cls.INSTRUCTIONS_PATH / 'get_supplier_categories.md').read_text(encoding='utf-8')
            cls.instruction_find_product_in_supplier_domain = (cls.INSTRUCTIONS_PATH / 'find_product_in_supplier_domain.md').read_text(encoding='utf-8')
            logger.info("Инструкции успешно загружены.")
        except FileNotFoundError as ex:
             logger.error("Не найден один или несколько файлов инструкций.", ex, exc_info=False)
             # В зависимости от критичности инструкций, можно либо выбросить исключение, либо продолжить
             # raise ValueError("Файлы инструкций не найдены, работа невозможна.") from ex
        except Exception as ex:
             logger.error("Неожиданная ошибка при чтении файлов инструкций.", ex, exc_info=True)
             # raise ValueError("Ошибка чтения файлов инструкций.") from ex

        # Инициализация WebDriver
        try:
            cls.driver = Driver()
            logger.info("WebDriver (Driver) успешно инициализирован.")
        except Exception as ex:
            logger.error("Не удалось инициализировать WebDriver.", ex, exc_info=True)
            cls.driver = None # Устанавливаем в None, чтобы проверки ниже работали

        logger.info("Конфигурация Crawler загружена.")




async def get_products_by_category(category: str, num_of_links: str = '2') -> Optional[Dict[str, Any]]:
    """
    Асинхронно получает данные о продуктах для указанной категории.

    Использует предопределенную инструкцию и WebDriver из `Config`.

    Args:
        category (str): Название категории для поиска.
        num_of_links (str, optional): Желаемое количество ссылок (передается в инструкцию).
                                     По умолчанию '2'.

    Returns:
        Optional[Dict[str, Any]]: Словарь с извлеченными данными или None в случае ошибки.
    """
    # Объявление переменных
    extracted_data: Optional[Dict[str, Any]] = None
    task: str = ''
    driver: Optional[Driver] = Config.driver # Получаем драйвер из конфига
    extracted_data_raw: Optional[str] = None # Явно инициализируем

    # Проверка наличия драйвера
    if not driver:
        logger.error(f"WebDriver не инициализирован. Невозможно обработать категорию {category=}", None, False)
        return None

    try:
        logger.info(f'Обработка категории: {category=}')
        # Формирование инструкции
        # Проверка наличия инструкции
        if not Config.instruction_grab_product_page:
             logger.error("Инструкция 'grab_product_page' не загружена.", None, False)
             return None
        task = Config.instruction_grab_product_page.replace('{PRODUCT_CATEGORY}', category).replace('{NUM_LINKS}', num_of_links)

        # Выполнение задачи через драйвер
        extracted_data_raw = await driver.run_task(task, use_gemini=True) # Предполагаем, что возвращает строку JSON

        # Нормализация и парсинг ответа
        if isinstance(extracted_data_raw, str) and extracted_data_raw.strip():
             extracted_data_norm: str = normalize_answer(extracted_data_raw)
             extracted_data = j_loads(extracted_data_norm) # Парсинг JSON
             if extracted_data:
                 print('\n -------------------------------- EXTRACTED DATA (Category) ------------------------------------------')
                 print(extracted_data) # Используем кастомный print
                 print('\n -------------------------------------------------------------------------------------------')
             else:
                  logger.warning(f"Не удалось распарсить JSON ответ для категории {category=}: {extracted_data_norm}", None, False)
                  extracted_data = None # Считаем это неудачей
        else:
             logger.warning(f"Получен пустой или неожиданный тип данных от driver.run_task для {category=}: {type(extracted_data_raw)}", None, False)
             extracted_data = None

        return extracted_data # Возврат словаря или None
    except Exception as ex:
        # Логирование ошибки
        logger.error(f'Ошибка при обработке категории {category=}', ex, exc_info=True)
        return None # Возврат None при любой ошибке


async def fetch_categories_from_suppliers_random_urls() -> None:
    """
    Асинхронно извлекает категории товаров с сайтов поставщиков.

    Проходит по списку файлов `Config.crawl_files_list`, извлекает домены
    из URL продуктов. Для каждого нового домена (не из `Config.checked_domains`)
    выполняет задачу по извлечению категорий с помощью WebDriver.
    Сохраняет результаты и обновляет список проверенных доменов.
    """
    # Объявление переменных
    # categories_dict: Dict[str, Any] = {} # Не используется для возврата, убираем
    driver: Driver = Config.driver
    filename: str
    file_path: Path
    crawl_data: Dict | List
    products_data: List
    product: Dict
    domain: str
    task: str
    res: str = None # Ответ от драйвера
    normilized_res: str = ''
    data: Optional[Dict] = None # Результат парсинга JSON
    processed_domains_in_run: Set[str] = set() # Отслеживаем домены в этом запуске

    if not driver:
        logger.error("WebDriver не инициализирован. Невозможно извлечь категории поставщиков.", None, False)
        return

    # Проверка наличия инструкции
    if not Config.instruction_get_supplier_categories:
        logger.error("Инструкция 'get_supplier_categories' не загружена.", None, False)
        return

    logger.info(f"Запуск извлечения категорий поставщиков из {len(Config.crawl_files_list)} файлов.")

    # Обработка каждого файла из списка
    for filename in Config.crawl_files_list:
        try:
            file_path = Config.MINING_DATA_PATH / filename # Используем константу пути
            crawl_data = j_loads(file_path)

            # Извлечение списка продуктов
            products_data = []
            if isinstance(crawl_data, dict) and 'products' in crawl_data:
                if isinstance(crawl_data['products'], list):
                     products_data = crawl_data['products']
                else:
                    logger.warning(f"Ключ 'products' в файле {filename} не содержит список.", None, False)
                    continue
            elif isinstance(crawl_data, list): # Допускаем список продуктов в файле
                 products_data = crawl_data
            else:
                logger.warning(f"Файл {filename} не содержит ключ 'products' или не является списком.", None, False)
                continue

            # Обработка продуктов в файле
            for product in products_data:
                if not isinstance(product, dict) or 'product_url' not in product:
                    logger.warning(f"Некорректный формат продукта в файле {filename}: {product}", None, False)
                    continue

                try:
                    domain = get_domain(product['product_url'])
                    if not domain: # Если get_domain вернул пустую строку или None
                         logger.warning(f"Не удалось извлечь домен из URL: {product['product_url']}", None, False)
                         continue
                except Exception as domain_ex:
                    logger.error(f"Ошибка извлечения домена из URL: {product['product_url']}", domain_ex, exc_info=False)
                    continue

                # Пропускаем уже проверенные домены (глобально или в этом запуске)
                if domain in Config.checked_domains or domain in processed_domains_in_run:
                    continue

                logger.info(f"Извлечение категорий для нового домена: {domain}")
                processed_domains_in_run.add(domain) # Отмечаем как обрабатываемый в этом запуске

                # Формирование и выполнение задачи
                task = Config.instruction_get_supplier_categories.replace('{INPUT_URL}', f'https://{domain}')
                res = await driver.run_task(task, use_gemini=True)

                # Обработка ответа
                if isinstance(res, str) and res.strip():
                    normilized_res = normalize_answer(res)
                    data = j_loads(normilized_res) # Пытаемся распарсить JSON

                    if data: # Если парсинг успешен
                        print(f"Категории для {domain}:") # Используем кастомный print
                        print(data)
                        # Сохранение результата для домена
                        save_path: Path = Config.TRAIN_DATA_SUPPLIER_CATEGORIES_PATH / f'{domain}.json' # Имя файла по домену
                        j_dumps(data, save_path)
                        logger.info(f"Категории для {domain} сохранены в {save_path}")

                        # Добавление домена в проверенные и сохранение списка
                        Config.checked_domains.append(domain) # Обновляем список в памяти
                        # Перезаписываем файлы
                        save_text_file(Config.checked_domains, Config.CHECKED_DOMAINS_TXT_PATH)
                        j_dumps(Config.checked_domains, Config.CHECKED_DOMAINS_JSON_PATH)
                        logger.info(f"Домен {domain} добавлен в проверенные.")
                    else:
                        logger.warning(f"Не удалось распарсить ответ для домена {domain}: {normilized_res}", None, False)
                        # Решаем, добавлять ли "неудачный" домен в проверенные, чтобы не повторять
                        # Config.checked_domains.append(domain) ...
                else:
                     logger.warning(f"Получен пустой или некорректный ответ для домена {domain}", None, False)

                # Пауза между обработкой доменов
                await asyncio.sleep(Config.API_CALL_DELAY) # Используем константу задержки

        except FileNotFoundError:
            logger.error(f"Файл не найден при извлечении категорий: {file_path}", None, False)
        except Exception as ex:
            # Логирование ошибки на уровне файла
            logger.error(f'Ошибка при обработке файла {filename=} для извлечения категорий', ex, exc_info=True)
            continue # Переход к следующему файлу

    logger.info("Извлечение категорий поставщиков завершено.")
    # return categories_dict # Функция теперь ничего не возвращает


async def find_products_in_domains() -> None:
    """
    Асинхронно ищет ссылки на товары на спискe доменов.

    Читает список доменов из `Config.checked_domains`. Для каждого домена
    выполняет задачу поиска ссылок на товары с помощью WebDriver.
    Результаты накапливаются и сохраняются в JSON файл.
    """
    # Объявление переменных
    driver: Optional[Driver] = Config.driver
    domains_list: List[str] = Config.checked_domains # Используем загруженный список
    output_dict: Dict[str, Any] = {}
    timestamp: str = gs.now # Получаем текущую метку времени
    # Имя файла формируется один раз
    output_filename: Path = Config.ENDPOINT / f'output_products_{timestamp}.json'
    domain: str
    task: str
    raw_res: Optional[str] = None
    clear_res: str = ''
    res_dict: Optional[Dict] = None

    if not driver:
        logger.error("WebDriver не инициализирован. Невозможно выполнить поиск товаров по доменам.", None, False)
        return

    # Проверка наличия инструкции
    if not Config.instruction_find_product_in_supplier_domain:
        logger.error("Инструкция 'find_product_in_supplier_domain' не загружена.", None, False)
        return

    if not domains_list:
        logger.warning("Список доменов для поиска пуст (`checked_domains`).", None, False)
        return

    logger.info(f"Запуск поиска товаров на {len(domains_list)} доменах. Результаты -> {output_filename}")

    # Итерация по доменам
    for domain in domains_list:
        try:
            logger.info(f'Обработка домена: {domain}')
            print(f"\n------------------------\n Start find products in the {domain}\n ------------------------------------\n") # Кастомный print

            # Формирование и выполнение задачи
            task = Config.instruction_find_product_in_supplier_domain.replace('{INPUT_URL}', f'https://{domain}')
            raw_res = await driver.run_task(task) # Предполагаем использование стандартного LLM

            # Обработка результата
            if isinstance(raw_res, str) and raw_res.strip():
                clear_res = normalize_answer(raw_res)
                res_dict = j_loads(clear_res) # Парсинг JSON

                if res_dict is not None: # Проверяем, что парсинг удался (j_loads вернет {} при ошибке)
                    output_dict[domain] = res_dict # Добавляем результат в общий словарь
                    logger.info(f"Найдены данные для {domain}.")
                else:
                    output_dict[domain] = {"error": "Failed to parse response", "raw_response": clear_res}
                    logger.warning(f"Не удалось распарсить ответ JSON для {domain}.", None, False)
            else:
                 output_dict[domain] = {"error": "Empty or invalid response from driver"}
                 logger.warning(f"Получен пустой или некорректный ответ для {domain}", None, False)

            # Периодическое сохранение результатов (например, после каждого домена)
            # Используем try-except для сохранения, чтобы ошибка записи не прервала весь процесс
            try:
                j_dumps(output_dict, output_filename)
                logger.debug(f"Промежуточные результаты сохранены в {output_filename}")
            except Exception as dump_ex:
                logger.error(f"Ошибка сохранения промежуточных результатов в {output_filename}", dump_ex, exc_info=True)

            # Пауза между обработкой доменов
            await asyncio.sleep(Config.API_CALL_DELAY)

        except Exception as ex:
            # Логирование ошибки на уровне домена
            logger.error(f'Ошибка при обработке домена {domain=}', ex, exc_info=True)
            output_dict[domain] = {"error": f"Processing error: {str(ex)}"}
            # Сохраняем ошибку и продолжаем
            try:
                j_dumps(output_dict, output_filename)
            except Exception as dump_ex:
                logger.error(f"Ошибка сохранения ошибки для домена {domain} в {output_filename}", dump_ex, exc_info=True)
            continue

    logger.info(f"Поиск товаров по доменам завершен. Финальные результаты сохранены в {output_filename}")



async def main() -> None:
    """ Основная асинхронная функция запуска """
    # --- Выбор режима работы ---
    # Раскомментируйте нужный блок для запуска соответствующей задачи

    # # === Режим 1: Обработка URL продуктов из файлов ===
    # logger.info("Запуск режима 1: Обработка URL продуктов...")
    # # Используем генератор для экономии памяти
    # url_generator = utils.yield_product_urls_from_files(Config.MINING_DATA_PATH)
    # # Или используем список, если данных не слишком много
    # # url_list = utils.get_products_urls_list_from_files(Config.MINING_DATA_PATH, Config.crawl_files_list)
    # product_url: str
    # for product_url in url_generator: # или for product_url in url_list:
    #     if not Config.driver:
    #         logger.critical("WebDriver не доступен, прерывание обработки URL.", None, False)
    #         break
    #     try:
    #         logger.info(f'Обработка URL: {product_url}')
    #         # Убедимся, что инструкция загружена
    #         if not Config.instruction_grab_product_page:
    #              logger.error("Инструкция 'grab_product_page' не загружена, пропуск URL.", None, False)
    #              continue
    #         task: str = Config.instruction_grab_product_page.replace('{PRODUCT_URL}', product_url) # Используем другой плейсхолдер
    #
    #         result_data: Optional[str] = await Config.driver.run_task(task, use_gemini=True)
    #         if isinstance(result_data, str) and result_data.strip():
    #              norm_data: str = normalize_answer(result_data)
    #              parsed_data: Optional[Dict] = j_loads(norm_data)
    #              if parsed_data:
    #                  print(f"Результат для {product_url}:")
    #                  print(parsed_data)
    #                  # TODO: Сохранение или дальнейшая обработка parsed_data
    #                  # Например: j_dumps(parsed_data, Config.ENDPOINT / 'processed_products' / f'{get_domain(product_url)}_{gs.now}.json')
    #              else:
    #                  logger.warning(f"Не удалось распарсить JSON для {product_url}: {norm_data}", None, False)
    #         else:
    #              logger.warning(f"Не получен строковый результат для {product_url}", None, False)
    #
    #         await asyncio.sleep(Config.API_CALL_DELAY) # Пауза между URL
    #
    #     except Exception as ex:
    #         logger.error(f'Ошибка при обработке {product_url=}', ex, exc_info=True)
    # logger.info("Режим 1 завершен.")

    # # === Режим 2: Поиск продуктов по категориям ===
    # logger.info("Запуск режима 2: Поиск продуктов по категориям...")
    # # Получаем список категорий из файлов, используя функцию из utils
    # categories: List[str] = utils.get_categories_from_files(Config.MINING_DATA_PATH, Config.crawl_files_list)
    # category: str
    # for category in categories:
    #     await get_products_by_category(category, '1') # Запрашиваем по 1 ссылке на категорию
    #     await asyncio.sleep(Config.API_CALL_DELAY) # Пауза между категориями
    # logger.info("Режим 2 завершен.")

    # # === Режим 3: Извлечение категорий с сайтов поставщиков ===
    # logger.info("Запуск режима 3: Извлечение категорий поставщиков...")
    # await fetch_categories_from_suppliers_random_urls()
    # logger.info("Режим 3 завершен.")

    # === Режим 4: Поиск ссылок на товары на известных доменах ===
    logger.info("Запуск режима 4: Поиск товаров на доменах...")
    await find_products_in_domains()
    logger.info("Режим 4 завершен.")

    # Закрытие драйвера после завершения всех задач
    if Config.driver:
        await Config.driver.quit()
        logger.info("WebDriver закрыт.")


if __name__ == "__main__":
    try:
        # Запускаем основной асинхронный цикл
        asyncio.run(main())
    except KeyboardInterrupt:
        # Обработка прерывания пользователем
        print("\nПрограмма прервана пользователем.")
        logger.warning("Выполнение прервано пользователем (KeyboardInterrupt).", None, False)
    except Exception as e:
         # Логирование критических ошибок в главном цикле
         logger.critical("Критическая ошибка в главном цикле выполнения.", e, exc_info=True)
    finally:
        # Попытка закрыть драйвер, если он еще открыт
        # Используем run_until_complete для синхронного вызова async quit в finally
        if Config.driver and Config.driver.browser: # Проверяем, что драйвер и браузер существуют
             logger.info("Попытка штатного/аварийного закрытия WebDriver в блоке finally...")
             try:
                 loop = asyncio.get_event_loop()
                 if loop.is_running():
                      # Если цикл еще работает (например, после KeyboardInterrupt)
                      loop.create_task(Config.driver.quit()) # Запускаем как задачу
                      # Даем немного времени на выполнение, но не блокируем надолго
                      # Это компромисс, полное ожидание в finally может быть сложным
                      # loop.run_until_complete(asyncio.sleep(1.0)) # Не лучший вариант
                      logger.warning("Запущена задача на закрытие WebDriver, но finally не будет ждать ее завершения.")
                 else:
                      # Если цикл остановлен, можно попробовать run_until_complete
                      loop.run_until_complete(Config.driver.quit())
                 logger.info("Команда на закрытие WebDriver отправлена.")
             except RuntimeError as rt_ex:
                  logger.error(f"Ошибка цикла событий при закрытии WebDriver: {rt_ex}", None, False)
             except Exception as final_ex:
                 logger.error("Ошибка при закрытии WebDriver в блоке finally.", final_ex, exc_info=True)
        logger.info("Завершение работы скрипта.")
