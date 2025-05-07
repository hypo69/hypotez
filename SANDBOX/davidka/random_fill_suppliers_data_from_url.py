## \file /sandbox/davidka/random_fill_suppliers_data_from_url.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль сбора информации по ссылкам из JSON файла поставщика (директория `data_by_supplier`).
==========================================================================================

Модуль для обхода существующих файлов JSON поставщиков, поиска непроверенных записей
(где не были собраны данные с целевого URL, что определяется по пустому полю 'text')
и заполнения полей 'text', 'internal_links' и других данными, полученными
с соответствующего URL с помощью веб-драйвера и функции `extract_page_data`.

Скрипт итерирует по файлам в `Config.data_by_supplier_dir`. Для каждого
файла он ищет ПЕРВУЮ запись с пустым 'text', загружает HTML по её URL,
извлекаются данные (`extract_page_data`), запись обновляется в файле,
файл сохраняется, и скрипт переходит к СЛЕДУЮЩЕМУ ФАЙЛУ.
Предполагается, что URL-ключи в файлах уже валидны и не требуют проверки.

Основная функция `process_supplier_link` - вызывается для каждой такой записи.

Для запуска:
  python random_fill_suppliers_data_from_url.py [username]

Если `username` не указан, по умолчанию используется 'onela'.
Например:
  python random_fill_suppliers_data_from_url.py               # Использует ключ 'onela'
  python random_fill_suppliers_data_from_url.py kazarinov     # Использует ключ 'kazarinov'

```rst
 .. module:: sandbox.davidka.random_fill_suppliers_data_from_url
```
"""


import argparse
from pathlib import Path
import random
from typing import Dict, Any, List
import sys

# Стандартные импорты проекта
# Убедитесь, что эти импорты работают в вашем окружении
import header
from header import __root__ 
from src import gs

# --- Импорты WebDriver ---
from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox
# -------------------------
from src.llm.gemini import GoogleGenerativeAi
# -------------------------
from src.utils.jjson import j_loads, j_dumps
from src.utils.file import get_filenames_from_directory, get_directory_names, read_text_file, save_text_file
from src.logger import logger
from src.utils.printer import pprint as print
from SANDBOX.davidka.graber import extract_page_data # Ваша функция

class Config:
    """Класс конфигурации скрипта."""
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    # Укажите актуальный путь к вашей директории с данными
    data_by_supplier_dir: Path = Path('F:/llm/data_by_supplier') # Пример пути, измените при необходимости
    WINDOW_MODE: str = 'headless' # 'normal' или 'headless'
    GEMINI_API_KEY: str | None = None # Будет установлен из аргументов
    GEMINI_MODEL_NAME = 'gemini-2.0-flash-exp'
    system_instructuction:str = read_text_file(ENDPOINT/'instructions/analize_html.md')
    updated_links:list = j_loads(ENDPOINT/'updated_links.json')

# ==============================================================================
# Основная функция обработки ссылки
# ==============================================================================
def process_supplier_link(
    driver: Driver,
    link: str,
    current_data_for_link: Dict[str, Any], # Это value_dict, который мы будем обновлять
    supplier_file_path: Path,
    llm: GoogleGenerativeAi
) -> dict: # Возвращаем обновленный словарь или None
    """
    Обрабатывает одну ссылку из файла JSON поставщика: если поле 'text' пусто,
    загружает HTML, извлекает данные и возвращает обновленный словарь для этой ссылки.
    Модифицирует current_data_for_link "на месте".

    Args:
        driver (Driver): Инстанс веб-драйвера для получения HTML.
        link (str): URL для обработки.
        current_data_for_link (Dict[str, Any]): Текущий словарь данных, соответствующий этому URL.
                                                Этот словарь будет изменен "на месте".
        supplier_file_path (Path): Путь к файлу JSON поставщика (для логирования).
        llm (GoogleGenerativeAi): Инициализированный экземпляр LLM.

    Returns:
        Dict[str, Any] | None: Модифицированный current_data_for_link, если обработка успешна 
                               и данные были обновлены, иначе None (в случае ошибки или если 'text' не был пуст).
    """

    # первый этап
    # обработка только ПУСТЫ значений 'text' в словаре!!!!

    text_content: str = current_data_for_link.get('text', '')

    if not text_content or text_content.isspace():
        logger.info(f"\n ---------------------------------\n Обработка записи для URL '{link}' с пустым полем 'text' в файле '{supplier_file_path=}'. \n --------------------------------\n")

        raw_data_from_url: str | None = driver.fetch_html(link)

        if not raw_data_from_url:
            logger.error(f"Не удалось получить HTML для URL: {link}")
            return {'page_type':'unknown','error':'page not found'}

        extracted_page_content: Dict[str, Any] = extract_page_data(raw_data_from_url, link)
        
        if not extracted_page_content or not extracted_page_content.get('text'):
            logger.warning(f"Не удалось извлечь данные или текст пуст для URL: {link} из файла {supplier_file_path.name}")
            return {'page_type':'unknown','error':'error while extarct'}

        request_dict = extracted_page_content
        del(request_dict['html']) # <- удаляем html, чтобы не мешал
        q:str = f"""`{str(request_dict)}`"""

        a:dict = j_loads(llm.ask(q))
        if hasattr(a, 'page_type'): extracted_page_content['page_type'] = a.get('page_type', '') ; del(a['page_type'])
        if hasattr(extracted_page_content, 'category'): 
            #extracted_page_content['categoty_name'] = getattr(extracted_page_content,'category', '') # <- временная категория из начального набора данных
            del(extracted_page_content['category']) # <- удаляем временную категорию

        if hasattr(a, 'product_links'): 
            if extracted_page_content['product_links'] and isinstance(extracted_page_content['product_links'], list):
               extracted_page_content['product_links'].append(getattr(a,'product_links',[]))
               extracted_page_content['product_links'] = list(set(extracted_page_content))
            else:                                                  
                extracted_page_content['product_links'] = getattr(a,'product_links',[])
            del(a['product_links'])

        if hasattr(a, 'categoty_name'): extracted_page_content['categoty_name'] = a.get('categoty_name', '') ; del(a['categoty_name'])
        if hasattr(a, 'parent_category'): extracted_page_content['parent_category'] = a.get('parent_category', '') ; del(a['parent_category'])
        if hasattr(a, 'title'): extracted_page_content['title'] = a.get('title', '') ; del(a['title'])
        if hasattr(a, 'summary'): extracted_page_content['summary'] = a.get('summary', '') ; del(a['summary'])
        if hasattr(a, 'descrition'): extracted_page_content['descrition'] = a.get('descrition', '') ; del(a['descrition'])
        if hasattr(a, 'specification'): extracted_page_content['specification'] = a.get('specification', '') ; del(a['specification'])
        if hasattr(a, 'notes'): extracted_page_content['notes'] = a.get('notes', '') ; del(a['notes'])
        if hasattr(a, 'price'): extracted_page_content['price'] = a.get('price', '') ; del(a['price'])


        extracted_page_content['ai_analized_content'] = a 
        ...
        for key_from_extraction, value_from_extraction in extracted_page_content.items():
            current_data_for_link[key_from_extraction] = value_from_extraction
        
        logger.info(f"Данные для URL '{link}' извлечены и словарь обновлен.")
        return current_data_for_link
    else:
        # Эта ветка больше не должна достигаться, так как проверка text_content делается перед вызовом
        # Но оставим на всякий случай для защиты
        logger.debug(f"URL '{link}' в файле '{supplier_file_path.name}' уже содержит данные (внутренняя проверка). Пропуск.")



# ==============================================================================
# Основной блок выполнения скрипта
# ==============================================================================
if __name__ == '__main__':
    script_name = Path(__file__).name
    parser = argparse.ArgumentParser(
        description="Сбор данных по ссылкам поставщиков. По умолчанию используется Gemini API ключ для 'onela'.",
        usage=f"python {script_name} [username]",
        epilog=f"Примеры:\n"
               f"  python {script_name}                  # Использует ключ пользователя 'onela'\n"
               f"  python {script_name} kazarinov        # Использует ключ пользователя 'kazarinov'",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'user',
        type=str,
        nargs='?',
        default='onela',
        help="Имя пользователя для выбора Gemini API ключа (например, 'kazarinov'). \n"
             "Если не указано, по умолчанию используется 'onela'. \n"
             "Ключ будет взят из gs.credentials.gemini.<user>.api_key."
    )
    args = parser.parse_args()
    username = args.user

    logger.info(f"--- Начало работы скрипта {script_name} для пользователя '{username}' ---")

    try:
        user_gemini_config = getattr(gs.credentials.gemini, username)
        Config.GEMINI_API_KEY = getattr(user_gemini_config, 'api_key')
        logger.info(f"Успешно получен и установлен Gemini API ключ для пользователя: '{username}'")
    except AttributeError:
        logger.critical(f"Ошибка: не удалось найти API ключ для пользователя '{username}'. "
                        f"Проверьте, существует ли 'gs.credentials.gemini.{username}.api_key'.")
        sys.exit(1)

    if not Config.GEMINI_API_KEY:
        logger.critical(f"Ошибка: API ключ для пользователя '{username}' пустой.")
        sys.exit(1)

    llm_instance: GoogleGenerativeAi | None = None
    try:
        llm_instance = GoogleGenerativeAi(
            Config.GEMINI_API_KEY, 
            Config.GEMINI_MODEL_NAME, 
            {'response_mime_type':'application/json'},
            Config.system_instructuction)
        logger.info("Инстанс GoogleGenerativeAi успешно инициализирован.")
    except Exception as e:
        logger.critical(f"Не удалось инициализировать GoogleGenerativeAi: {e}", exc_info=True)
        sys.exit(1)

    driver_instance: Driver | None = None
    processed_files_count: int = 0
    text_updated_in_files_count: int = 0 
    error_files_count: int = 0
    total_links_processed_for_update_attempt: int = 0 
    total_links_successfully_updated: int = 0 
    
    total_discovered_files_count: int = 0
    suppliers_dirs_list: List[str] = []

    logger.info(f"Поиск файлов поставщиков в: {Config.data_by_supplier_dir}")
    while True:
        try:
            driver_instance = Driver(Firefox, window_mode=Config.WINDOW_MODE)
            logger.info('Драйвер успешно инициализирован.')


            # # ---------------------------- DEBUG ------------------
            # link:str = 'https://tdspribor.ru/preobrazovateli-signalov' # <- пример страницы категорий
            # supplier_dir = Config.data_by_supplier_dir/'tdspribor.ru'
            # supplier_file_names: List[str] = get_filenames_from_directory(supplier_dir, 'json')
            # for f in supplier_file_names:
            #     supplier_data_content = j_loads(supplier_dir/f)
            #     if not supplier_data_content: # хз, почему не загрузился
            #         logger.warning(f"Не удалось загрузить данные: {f}. Пропуск файла.")
            #         #data_str:str = 
            #     for link_key, value_dict in supplier_data_content.items():
            #         supplier_data_content[link_key] = process_supplier_link(
            #                         driver_instance, 
            #                         link_key, 
            #                         value_dict, 
            #                         f, 
            #                         llm_instance
            #                     )

            #         j_dumps(supplier_data_content, supplier_dir/f)
            # # -----------------------------------------------------

            logger.info('Получение списка директорий поставщиков...')
            suppliers_dirs_list = get_directory_names(Config.data_by_supplier_dir)
            if not suppliers_dirs_list:
                logger.warning(f'Не найдено директорий поставщиков в {Config.data_by_supplier_dir}')
                sys.exit()
            else:
                logger.info(f'Найдено {len(suppliers_dirs_list)} директорий поставщиков. Перемешивание...')
                random.shuffle(suppliers_dirs_list)

            for supplier_dir_name in suppliers_dirs_list:
                supplier_dir_path = Config.data_by_supplier_dir / supplier_dir_name
                logger.info(f"Обработка директории: {supplier_dir_path}")
            
                supplier_file_names: List[str] = get_filenames_from_directory(supplier_dir_path, 'json') 
                if not supplier_file_names:
                    logger.info(f"Не найдено JSON файлов в директории: {supplier_dir_path}")
                    continue
            
                total_discovered_files_count += len(supplier_file_names)

                for supplier_file_name in supplier_file_names:
                    supplier_file_path = supplier_dir_path / supplier_file_name
                    logger.debug(f"Обработка файла: {supplier_file_path}")

                    supplier_data_content = j_loads(supplier_file_path)

                    if not supplier_data_content:
                        logger.warning(f"Не удалось загрузить данные или файл пуст: {supplier_file_path}. Пропуск файла.")
                        error_files_count += 1
                        continue

                    links_and_data_to_process = []
                    is_top_level_dict = isinstance(supplier_data_content, dict)
                
                    if is_top_level_dict:
                        for key, value_dict in supplier_data_content.items():
                            if isinstance(value_dict, dict):
                                links_and_data_to_process.append((key, value_dict))
                            else:
                                logger.warning(f"Значение для ключа '{key}' в файле '{supplier_file_path}' не является словарем. Пропуск элемента.")
                    elif isinstance(supplier_data_content, list):
                        for item_list_entry in supplier_data_content:
                            if isinstance(item_list_entry, dict):
                                for key, value_dict in item_list_entry.items():
                                    if isinstance(value_dict, dict):
                                        links_and_data_to_process.append((key, value_dict))
                                    else:
                                        logger.warning(f"Значение для ключа '{key}' во вложенном словаре списка в файле '{supplier_file_path}' не является словарем. Пропуск элемента.")
                            else:
                                logger.warning(f"Элемент в списке в файле '{supplier_file_path}' не является словарем. Пропуск элемента.")
                    else:
                        logger.error(f"Неожиданный тип данных ({type(supplier_data_content)}) после загрузки файла {supplier_file_path}. Пропуск файла.")
                        error_files_count += 1
                        continue

                    file_was_updated_and_saved = False 

                    for link_key, original_value_dict in links_and_data_to_process:
                        if link_key in Config.updated_links.keys():
                            continue

                        text_content_before_processing: str = original_value_dict.get('text', '')
                        # --------------- debug
                        if True:
                        #if not text_content_before_processing or text_content_before_processing.isspace():
                            total_links_processed_for_update_attempt += 1
                            updated_dict_result = process_supplier_link(
                                driver_instance, 
                                link_key, 
                                original_value_dict, 
                                supplier_file_path, 
                                llm_instance
                            )
                        
                            if updated_dict_result:
                                logger.info(f"Данные для ссылки '{link_key}' в файле {supplier_file_path} обновлены. Сохранение файла...")
                                if not j_dumps(supplier_data_content, supplier_file_path):
                                    logger.error(f"Ошибка сохранения файла: {supplier_file_path}")
                                else:
                                    Config.updated_links.update({link_key:getattr(supplier_data_content,'page_type', '')})
                                    j_dumps(Config.updated_links, Config.ENDPOINT / 'updated_links.json')
                                    text_updated_in_files_count += 1
                                    total_links_successfully_updated += 1
                                    
                                    logger.info(f"Данные успешно обновлены")
                                    ...
                                file_was_updated_and_saved = True
                                break 
                        else:
                            logger.debug(f"URL '{link_key}' в файле '{supplier_file_path.name}' уже содержит данные. Пропуск обработки этой ссылки.")
                
                    processed_files_count += 1

                    if not file_was_updated_and_saved:
                         logger.debug(f"В файле {supplier_file_path} не было найдено ссылок для обновления или обновления не были успешными (все ссылки уже имели текст или обработка не удалась). Переход к следующему файлу.")

            logger.info('Статистика:')
            logger.info(f" - Всего директорий поставщиков найдено: {len(suppliers_dirs_list) if suppliers_dirs_list else 0}")
            logger.info(f" - Всего файлов JSON обнаружено: {total_discovered_files_count}")
            logger.info(f" - Файлов JSON загружено и обработано (сделана попытка): {processed_files_count}")
            logger.info(f" - Файлов, в которых реально обновлены данные и файл сохранен: {text_updated_in_files_count}")
            logger.info(f" - Всего ссылок, для которых предпринята попытка обновления (текст был пуст): {total_links_processed_for_update_attempt}")
            logger.info(f" - Всего ссылок, для которых успешно извлечены и обновлены новые данные: {total_links_successfully_updated}")
            logger.info(f" - Ошибок при загрузке/обработке файлов (не удалось загрузить JSON): {error_files_count}")
                         
        except KeyboardInterrupt:
            logger.warning("Обработка прервана пользователем (KeyboardInterrupt).")
            break
        except Exception as ex:
            logger.critical('Критическая ошибка во время выполнения (вне цикла обработки файлов):', ex, exc_info=True)
            ...
            break

    if driver_instance:
        logger.info('Завершение работы драйвера...')
        try:
            driver_instance.quit()
        except Exception as ex_quit:
            logger.error('Ошибка при закрытии драйвера:', ex_quit, exc_info=True)

    logger.info('--- Обработка файлов завершена ---')

    logger.info(f"--- Работа скрипта {script_name} завершена ---")
