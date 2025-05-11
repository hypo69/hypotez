## \file /sandbox/davidka/crawler_simple_driver.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для сбора данных со страниц товаров через SimpleDriver
=====================================================
(адаптация исходного crawler.py)

.. module:: sandbox.davidka.crawler_simple_driver
"""
import sys
import asyncio
from filelock import AsyncFileLock
import random
from urllib.parse import urlparse
from typing import List, Dict, Union
from types import SimpleNamespace
from pathlib import Path
from typing import Optional

import header
from header import __root__
from src import gs
from src.webdriver.llm_driver.simple_driver import SimpleDriver
from src.utils.jjson import j_loads, j_loads_ns, j_dumps, find_keys
from src.utils.file import read_text_file, save_text_file, get_filenames_from_directory, recursively_yield_file_path, read_text_file_async, save_text_file_async
from src.utils.url import get_domain
from src.utils.string.ai_string_utils import normalize_answer
from src.utils.printer import pprint as print
from src.logger import logger
from SANDBOX.davidka.utils.utils import yield_product_urls_from_files, get_categories_from_random_urls, files_mixer, sort_by_page_type




class Config:
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    config:SimpleNamespace = j_loads_ns(ENDPOINT / 'davidka.json')
    STORAGE:Path = Path(config.storage)
    mining_data_path: Path = ENDPOINT / 'random_urls'
    train_data_products_dir: Path = ENDPOINT / 'train_data_products'
    output_product_data_dir: Path = ENDPOINT / 'output_product_data'

    crawl_files_list: list = get_filenames_from_directory(mining_data_path, 'json')
    checked_domains: list = read_text_file(ENDPOINT / 'checked_domains.txt', as_list=True)

    # Инструкции
    instruction_grab_product_page_simple_driver: str = (
        ENDPOINT / 'instructions' / 'grab_product_page_simple_driver.md'
    ).read_text(encoding='utf-8')  or ''

    instruction_get_supplier_categories: str = (
        ENDPOINT / 'instructions' / 'get_supplier_categories.md'
    ).read_text(encoding='utf-8') or ''

    instruction_find_product_in_supplier_domain: str = (
        ENDPOINT / 'instructions' / 'find_product_in_supplier_domain.md'
    ).read_text(encoding='utf-8') or ''

    instruction_for_products_urls_one_product: str = (
        ENDPOINT / 'instructions' / 'get_product_links_one_product.md'
    ).read_text(encoding='utf-8') or ''

    instruction_links_from_search: str = (
        ENDPOINT / 'instructions' / 'links_from_search.md'
    ).read_text(encoding='utf-8') or ''

    instruction_links_from_searh_page: str = (
        ENDPOINT / 'instructions' / 'links_from_searh_page.md'
    ).read_text(encoding='utf-8') or ''

    system_instructuction: str = read_text_file(ENDPOINT / 'instructions/analize_html.md') or ''

    config: SimpleNamespace = j_loads_ns(ENDPOINT / 'davidka.json')

    try:
        STORAGE: Path = Path(config.storage)
    except Exception as ex:
        raise ValueError("Ошибка загрузки пути к хранилищу", ex)

    TRAIN_STORAGE: Path = Path(config.train_storage)
    UZZIPPED_STORAGE: Path = Path(config.unzipped_storage)

    # Параметры Gemini
    GEMINI_API_KEY: Optional[str] = gs.credentials.gemini.onela.api_key  # или katia.api_key
    GEMINI_MODEL_NAME: str = config.gemini_model_name
    driver: SimpleDriver = SimpleDriver(
        gemini_model_name='gemini-1.5-flash-8b-exp-0924',
        GEMINI_API_KEY=GEMINI_API_KEY
    )

    # Прочее
    updated_links_file_name: str = 'updated_links.json'
    DELAY_AFTER_LINK_PROCESSING: int = 15
    WINDOW_MODE: str = 'headless'

    # Список плохих доменов
    BLACKLIST_DOMAINS = [
        "youtube.com", "youtu.be", "facebook.com", "twitter.com", "tiktok.com",
        "linkedin.com", "instagram.com", "vk.com", "pinterest.com", "reddit.com",
        "snapchat.com", "weibo.com", "medium.com", "blogspot.com", "github.com",
        "google.com",
    ]

    # Заблокированные шаблоны ссылок
    BLOCKED_PATTERNS = [".pdf", "/login", "/register", "/signin", "/signup"]

def is_link_allowed(url: str) -> bool:
    try:
        parsed = urlparse(url.lower())
        domain = parsed.netloc.replace("www.", "")

        # Отфильтровать по домену
        if any(bad in domain for bad in Config.BLACKLIST_DOMAINS):
            return False

        # Отфильтровать по пути
        if any(pattern in parsed.path for pattern in Config.BLOCKED_PATTERNS):
            return False

        return True
    except Exception:
        return False

async def fetch_product_data(driver: SimpleDriver, data_dir: str | Path) -> List[Dict]:
    """
    Асинхронный сбор данных о товаре с использованием SimpleDriver и блокировкой файла обработанных ссылок.

    Функция использует `yield_product_urls_from_files` для получения ссылок на страницы товаров.
    Сохраняет данные о каждом товаре в формате JSON в директорию, указанную в `Config.output_product_data_dir`.
    Файл `processed_links.txt` (путь определяется `Config.ENDPOINT`) блокируется на время операций
    чтения-изменения-записи для предотвращения конфликтов при одновременном запуске нескольких процессов.

    Args:
        driver (SimpleDriver): Экземпляр SimpleDriver для взаимодействия со страницей.
        data_dir (str | Path): Директория с файлами, содержащими URL товаров.

    Returns:
        List[Dict]: Список словарей с данными о каждом успешно обработанном товаре.
                    Возвращает пустой список в случае общей ошибки или если ни один товар не был обработан.
    
    Example:
        >>> # Этот пример требует настройки окружения и asyncio loop
        >>> # import asyncio
        >>> # my_driver = SimpleDriver()
        >>> # # Настройка Config и gs для теста
        >>> # Config.ENDPOINT.mkdir(parents=True, exist_ok=True)
        >>> # Config.output_product_data_dir.mkdir(parents=True, exist_ok=True)
        >>> # def mock_gs_now(): import time; return f"product_{int(time.time()*1000)}"
        >>> # gs.now = mock_gs_now 
        >>> # results = asyncio.run(fetch_product_data(my_driver, Config.ENDPOINT))
        >>> # pprint(f"Собрано данных: {len(results)}")
        >>> # for item in results:
        >>> #     pprint(item)
    """
    all_collected_data: List[Dict] = []
    processed_links_file_path: Path = Config.ENDPOINT / 'processed_links.txt'
    # Формирование пути к файлу блокировки рядом с основным файлом
    lock_file_path: Path = processed_links_file_path.with_suffix(processed_links_file_path.suffix + '.lock')
    file_lock: AsyncFileLock = AsyncFileLock(lock_file_path)

    # Объявление переменных, используемых в цикле
    product_url: str
    current_processed_links: List[str]
    task_instruction: str
    driver_response: Optional[Dict]
    product_data: Union[Dict, List] # j_loads может вернуть dict или list
    output_filename_base: str
    output_file_path: Path


    try:
        for product_url in yield_product_urls_from_files(Path(data_dir)):
            try:
                async with file_lock: # Блокировка на время работы с processed_links.txt
                    # Шаг 1: Чтение списка уже обработанных URL
                    # read_text_file_async должен вернуть List[str] или None при ошибке.
                    # Если файл не найден, ожидается пустой список [].
                    read_result = await read_text_file_async(processed_links_file_path, as_list=True)
                    
                    if read_result is None:
                        logger.error(f'Ошибка чтения файла обработанных ссылок: {processed_links_file_path}. Пропуск URL: {product_url}')
                        continue # Переход к следующему URL, блокировка будет освобождена

                    current_processed_links = read_result if isinstance(read_result, list) else []


                    # Шаг 2: Проверка, был ли URL уже обработан
                    if product_url in current_processed_links:
                        logger.info(f'URL уже обработан (найден в {processed_links_file_path.name}): {product_url}')
                        continue # Переход к следующему URL, блокировка будет освобождена

                    # Шаг 3: Обработка нового URL (основная логика остается под блокировкой,
                    # чтобы гарантировать запись в processed_links.txt только после успешной обработки)
                    logger.info(f'Обработка нового URL: {product_url=}')
                    task_instruction = Config.instruction_grab_product_page_simple_driver.replace('{PRODUCT_URL}', product_url)
                    
                    driver_response = await driver.simple_process_task_async(task_instruction)
                    if not driver_response:
                        logger.warning(f'SimpleDriver не вернул результат для {product_url=}. URL не будет добавлен в обработанные.')
                        continue # Переход к следующему URL

                    # Предполагается, что driver_response['output'] содержит JSON-строку или сам словарь
                    # j_loads должен корректно это обработать
                    product_data_source = driver_response.get('output') if isinstance(driver_response, dict) else driver_response
                    product_data = j_loads(product_data_source) 

                    if not product_data: # j_loads вернул {} или [] при ошибке, или пустой результат
                        logger.warning(f'j_loads не вернул валидных данных для {product_url=}. Ответ драйвера: {str(product_data_source)[:200]}...')
                        continue # Переход к следующему URL

                    print(product_data)

                    # Шаг 4: Сохранение данных о товаре
                    # Уникальное имя файла на основе gs.now()
                    unique_id: str = gs.now() if callable(gs.now) else str(gs.now) # type: ignore
                    output_filename_base = f'product_data_{unique_id}' # Более осмысленное имя
                    output_file_path = Config.output_product_data_dir / f'{output_filename_base}.json'
                    
                    if not j_dumps(product_data, output_file_path):
                        logger.error(f'Не удалось сохранить данные JSON для {product_url=} в {output_file_path}. URL не будет добавлен в обработанные.')
                        continue # Переход к следующему URL

                    # Шаг 5: Обновление файла обработанных ссылок
                    current_processed_links.append(product_url)
                    if not await save_text_file_async(current_processed_links, processed_links_file_path):
                        logger.error(f'КРИТИЧЕСКАЯ ОШИБКА: Не удалось обновить файл {processed_links_file_path.name} для {product_url}. Данные товара сохранены в {output_file_path}, но URL не помечен как обработанный и может быть обработан повторно.')
                        # В этой ситуации данные товара сохранены, но processed_links.txt не обновлен.
                        # Это может привести к повторной обработке. Можно решить удалить output_file_path
                        # или добавить более сложную логику отката/повтора.
                        # Пока что, просто логируем и НЕ добавляем в all_collected_data, чтобы отразить частичный сбой.
                        continue # Переход к следующему URL
                    
                    logger.info(f'URL {product_url} успешно обработан и данные сохранены. {processed_links_file_path.name} обновлен.')
                    all_collected_data.append(product_data if isinstance(product_data, dict) else {'data': product_data})

            # Блокировка `file_lock` автоматически освобождается здесь (при выходе из `async with file_lock`)
            except Exception as ex_inner_loop:
                # Ошибка при обработке конкретного URL, но вне ожидаемых проверок (например, ошибка в логике)
                logger.error(f'Неожиданная ошибка при обработке URL: {product_url=}', ex_inner_loop, exc_info=True)
                # Продолжаем со следующим URL
                continue
        
        return all_collected_data

    except Exception as ex_outer_loop:
        # Общая ошибка при итерации по URL-ам или инициализации
        logger.error('Общая ошибка в функции fetch_product_data', ex_outer_loop, exc_info=True)
        return [] # Возвращаем пустой список в случае серьезной ошибки

async def find_products_urls_by_category(driver:SimpleDriver, category: str, task:str = '', num_of_links: str = '1') -> str:
    """Получить товары по категории через `SimpleDriver`"""
    try:
        
        task = task or Config.instruction_links_from_searh_page.replace('{PRODUCT_CATEGORY}', category).replace('{NUM_LINKS}', num_of_links)
        #ipdb.set_trace()
        answer = await driver.simple_process_task_async(task)
        if not answer:
            return ''
        j_dumps(answer, Config.ENDPOINT/'train_data_products'/f'product_links_{gs.now}.json') # Сборник ссылок
    except Exception as ex:
        logger.error(f'Ошибка при обработке {category=}', ex, exc_info=True)
        return ''

def sanitize(dir_path:Path|str):
    """Очистка полученных данныx. Функция проверяет 
    валидность JSON, пытается исправить ошибки в битых файлах.
    В случае неудачи функция переименовывает файл в .sanitized
    """
    for file_path in recursively_yield_file_path(Config.STORAGE /'data_by_supplier','*.json'):
        if file_path.stem == 'updated_links': continue
        file_dict = j_loads(file_path)
        if not file_dict:
            logger.warning(f'Файл {file_path} пуст или невалиден. Файл исключается из валидных')
            new_name = f"{file_path.stem}.sanitized{file_path.suffix}"

            # Создаем новый объект Path с новым именем в той же директории
            new_file_path = file_path.with_name(new_name)

            try:
                # Переименовываем файл
                file_path.rename(new_file_path)
                print(f"Переименовано: '{file_path}' -> '{new_file_path}'")
                continue
            except FileNotFoundError:
                # Это не должно произойти, если is_file() прошло, но на всякий случай
                print(f"Ошибка: Исходный файл '{file_path}' не найден при попытке переименования.")
                continue
            except FileExistsError:
                print(f"Ошибка: Файл с именем '{new_file_path.name}' уже существует в директории.")
                continue
            except OSError as e:
                print(f"Ошибка при переименовании '{file_path}' в '{new_file_path}': {e}")
                continue

def sort_data_by_page_type():
    """Сортировка полученных данных по 
    типу вебстрнаиц (product, information, about, conracts, errors, ...)"""
    input_dir:Path = Config.STORAGE / 'data_by_supplier'
    output_dir:Path = Config.STORAGE / 'sorted_data_by_page_type'
    chunk_limit:int = 70

    sort_by_page_type(input_dir, output_dir, chunk_size=chunk_limit)


async def main():
    """Основная функция запуска"""
    driver = Config.driver

    # Парсинг страниц товаров
    # await fetch_product_data(driver, Config.STORAGE)
    ...
    # Очистка от бытых файлов
    # sanitize(Config.STORAGE/'data_by_supplier')

    # Пример: обработка товаров по категориям
    # for category in get_categories_from_random_urls(all_in_one_data):
    #     await get_products_urls(driver,category)
        ...
    # Краулер
    for file in files_mixer(Config.STORAGE/'data_by_supplier'):



    # Пример: обработка файлов товаров
    # await fetch_product_data(driver, file)
        ...`
    # # Пример: обработка доменов
    # domains_list:list = read_text_file(Config.ENDPOINT / 'checked_domains.txt', as_list=True)
    # output_dict:dict = {}
    # timestamp:str = gs.now
    # for domain in domains_list:
    #     try:
    #         logger.info(f'Обработка домена: {domain}')
    #         print(f"\n------------------------\n Start find products in {domain}\n -----------------------------\n")
    #         task = Config.instruction_grab_product_page_simple_driver.replace('{INPUT_URL}', domain)
    #         res = await driver.simple_process_task_async(task)
    #         if not res:
    #             continue
    #         normalized_res:str = normalize_answer(res.get('output', ''))
    #         res_dict:dict = j_loads(normalized_res)
    #         output_dict.update({domain: res_dict})
    #         j_dumps(output_dict, Config.ENDPOINT / f'output_{timestamp}.json')
    #     except Exception as ex:
    #         logger.error(f'Ошибка при обработке {domain=}', ex, exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
