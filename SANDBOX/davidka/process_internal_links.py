# /sandbox/davidka/process_internal_links.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для сбора информации по ОДНОЙ внутренней ссылке (internal_links)
=============================================================================================
из КАЖДОГО JSON файла поставщика за один проход.
Лог обработанных ссылок ('processed_internal_links.json') ведется ВНУТРИ каждой директории поставщика.
Также логирует обработанные внутренние ссылки в общий 'updated_links.json'.
Новый JSON-файл для каждой обработанной ссылки имеет структуру: { <url>: { <данные> } }.

```rst
 .. module:: sandbox.davidka.process_internal_links
```

"""

import argparse
from pathlib import Path
import random
from typing import Dict, Any, List, Optional
from types import SimpleNamespace
import sys
import time
from datetime import datetime

# Стандартные импорты проекта
import header
from header import __root__
from src import gs

# --- Импорты WebDriver ---
from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox
# -------------------------
from src.llm.gemini import GoogleGenerativeAi
# -------------------------
from src.utils.jjson import j_loads, j_loads_ns, j_dumps
from src.utils.file import get_filenames_from_directory, get_directory_names, read_text_file
from src.logger import logger
from src.utils.printer import pprint as print
from SANDBOX.davidka.graber import extract_page_data

class Config:
    """Класс конфигурации скрипта."""

    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    config:SimpleNamespace = j_loads_ns(ENDPOINT / 'davidka.json')
    STORAGE:Path = Path(config.storage)
    WINDOW_MODE: str = 'headless'
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL_NAME = 'gemini-2.0-flash-exp' # Используйте актуальное имя модели
    system_instructuction: str = read_text_file(ENDPOINT / 'instructions/analize_html.md')
    processed_internal_links_file_name:str =  'processed_internal_links_file_name.json' 
    DELAY_AFTER_LINK_PROCESSING: int = 15

def generate_timestamp_filename() -> str:
    """Генерирует имя файла на основе текущей временной метки с миллисекундами."""
    return datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3] + ".json"

def process_single_internal_link(
    driver: Driver,
    internal_link_url: str,
    llm: GoogleGenerativeAi
) -> Optional[Dict[str, Any]]:
    """
    Обрабатывает одну внутреннюю ссылку. (Логика этой функции остается такой же)
    """
    logger.info(f"\n--- Обработка внутренней ссылки: {internal_link_url} ---\n")

    if not internal_link_url or not internal_link_url.startswith(('http://', 'https://')):
        logger.error(f"Некорректный URL внутренней ссылки: {internal_link_url}")
        return None

    raw_data_from_url: Optional[str] = driver.fetch_html(internal_link_url)
    if not raw_data_from_url:
        logger.error(f"Не удалось получить HTML для внутреннего URL: {internal_link_url}")
        return {'page_type': 'unknown', 'error': 'page not found', 'original_url': internal_link_url, 'processed_at': datetime.now().isoformat()}

    extracted_page_content: Dict[str, Any] = extract_page_data(raw_data_from_url, internal_link_url)
    if not extracted_page_content or not extracted_page_content.get('text'):
        logger.warning(f"Не удалось извлечь данные или текст пуст для внутреннего URL: {internal_link_url}")
        return {'page_type': 'unknown', 'error': 'error while extract', 'original_url': internal_link_url, 'processed_at': datetime.now().isoformat()}

    request_dict = extracted_page_content.copy()
    if 'text' in request_dict:
        del request_dict['text']
    if 'internal_links' in request_dict:
        del request_dict['internal_links']

    q: str = f"`{str(request_dict)}`"
    llm_response_data: Dict[str, Any] = {}
    #llm_response_str_for_log: str = "N/A"


    # --------------------- LLM ---------------------
    try:
        a = llm.ask(q)
        #llm_response_str_for_log = llm_response_str if llm_response_str else "empty_response"
        if a:
            parsed_llm_response = j_loads(a)
            if parsed_llm_response:
                if isinstance(parsed_llm_response, dict):
                    llm_response_data = parsed_llm_response
                else:
                    logger.error(f"Ответ LLM для {internal_link_url} не является валидным JSON объектом: {a}")
                    logger.debug(f"Орвет записан как `str`")
                    llm_response_data = {'response_data': a}
        else:
            logger.error(f"LLM вернул пустой ответ для {internal_link_url}")
    except Exception as e:
        logger.error(f"Ошибка парсинга ответа LLM для {internal_link_url}:. Ответ: {a}", ex, True)

    
    determined_page_type = llm_response_data.pop('page_type', extracted_page_content.get('page_type', ''))
    if not determined_page_type: 
        determined_page_type = 'unknown'
    extracted_page_content['page_type'] = determined_page_type
    


    if 'product_links' in llm_response_data:
        new_product_links = llm_response_data.pop('product_links', [])
        if isinstance(new_product_links, list):
            current_product_links = extracted_page_content.get('product_links', [])
            if not isinstance(current_product_links, list): current_product_links = []
            current_product_links.extend(new_product_links)
            extracted_page_content['product_links'] = list(set(filter(None, current_product_links)))

    fields_from_llm = ['categoty_name', 'parent_category', 'title', 'summary', 
                       'descrition', 'specification', 'notes', 'price','specification']
    for field in fields_from_llm:
        if field in llm_response_data:
            extracted_page_content[field] = llm_response_data.pop(field, extracted_page_content.get(field, ''))

    extracted_page_content['ai_analized_content'] = llm_response_data
    extracted_page_content['original_internal_url'] = internal_link_url # Это поле теперь может дублировать ключ верхнего уровня
    extracted_page_content['processed_at'] = datetime.now().isoformat()

    return extracted_page_content

# ==============================================================================
# Основной блок выполнения скрипта
# ==============================================================================
if __name__ == '__main__':
    script_name = Path(__file__).name
    parser = argparse.ArgumentParser(
        description="Сбор данных по ОДНОЙ внутренней ссылке на каждый JSON файл поставщика. Лог в директории поставщика. Выходной JSON: {url: {data}}.",
        usage=f"python {script_name} [username]",
        epilog=f"Примеры:\n"
               f"  python {script_name}                  # Использует ключ 'onela'\n"
               f"  python {script_name} kazarinov        # Использует ключ 'kazarinov'",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'user', type=str, nargs='?', default='onela',
        help="Имя пользователя для выбора Gemini API ключа."
    )
    args = parser.parse_args()
    username = args.user

    logger.info(f"--- Начало работы скрипта {script_name} для пользователя '{username}' (обработка internal_links, одна на файл, лог в директории, выход: {{url:data}}) ---")


    # ------------------------- GEMINI --------------------------

    try:
        user_gemini_config = getattr(gs.credentials.gemini, username)
        Config.GEMINI_API_KEY = getattr(user_gemini_config, 'api_key')
        logger.info(f"Успешно получен и установлен Gemini API ключ для пользователя: '{username}'")
    except AttributeError:
        logger.critical(f"Ошибка: не удалось найти API ключ для пользователя '{username}'.")
        sys.exit(1)

    if not Config.GEMINI_API_KEY:
        logger.critical(f"Ошибка: API ключ для пользователя '{username}' пустой.")
        sys.exit(1)

    llm_instance: Optional[GoogleGenerativeAi] = None
    try:
        llm_instance = GoogleGenerativeAi(
            Config.GEMINI_API_KEY,
            Config.GEMINI_MODEL_NAME,
            {'response_mime_type': 'application/json'},
            Config.system_instructuction
        )
        logger.info("Инстанс GoogleGenerativeAi успешно инициализирован.")
    except Exception as e:
        logger.critical(f"Не удалось инициализировать GoogleGenerativeAi: {e}", exc_info=True)
        sys.exit(1)

    driver_instance: Optional[Driver] = None
    
    total_source_files_scanned: int = 0
    internal_links_processed_this_run: int = 0
    error_loading_source_files_count: int = 0
    
    try:
        driver_instance = Driver(Firefox, window_mode=Config.WINDOW_MODE)
        logger.info('Драйвер успешно инициализирован.')

        logger.info(f"Поиск файлов поставщиков в: {Config.STORAGE}")
        suppliers_dirs_list = get_directory_names(Config.STORAGE) # <- Список директорий поставщиков

        if not suppliers_dirs_list:
            logger.warning(f'Не найдено директорий поставщиков в {Config.STORAGE}')
            sys.exit(0) 
        else:
            logger.info(f'Найдено {len(suppliers_dirs_list)} директорий поставщиков. Перемешивание...')
            random.shuffle(suppliers_dirs_list)

        for supplier_dir_name in suppliers_dirs_list:  
            supplier_dir_path:str = Config.STORAGE / supplier_dir_name  # <- Вот поставщик
            journal: Dict[str, Any] = j_loads(supplier_dir_path / Config.processed_internal_links_file_name) or {}
            
            supplier_file_names: List[str] = get_filenames_from_directory(supplier_dir_path, 'json')
            if not supplier_file_names:
                continue
            
            random.shuffle(supplier_file_names) 

            for supplier_file_name in supplier_file_names:
                if supplier_file_name == Config.processed_internal_links_file_name:  # <- В этом файле находится лог обработанных ссылок
                    continue


                supplier_file_path = supplier_dir_path / supplier_file_name
                logger.info(f"Сканирование исходного файла: {supplier_file_path.relative_to(Config.STORAGE)}")
                total_source_files_scanned += 1
                
                one_internal_link_processed_for_this_file = False 

                supplier_data_content = j_loads(supplier_file_path)
                if not supplier_data_content:
                    logger.warning(f"Не удалось загрузить данные или файл пуст: {supplier_file_path}. Пропуск файла.")
                    error_loading_source_files_count += 1
                    continue
                
                if not isinstance(supplier_data_content, dict):
                    logger.warning(f"Содержимое файла {supplier_file_path} не является словарем. Пропуск.")
                    error_loading_source_files_count += 1
                    continue

                for source_url_key, data_for_source_url in supplier_data_content.items():
                    if one_internal_link_processed_for_this_file:
                        break 

                    if not isinstance(data_for_source_url, dict):
                        continue 

                    internal_links_list = data_for_source_url.get('internal_links')
                    if not internal_links_list or not isinstance(internal_links_list, list):
                        continue 
                    
                    for internal_link_item in internal_links_list:
                        if one_internal_link_processed_for_this_file:
                            break 

                        if not isinstance(internal_link_item, dict) or 'link' not in internal_link_item:
                            continue 
                        
                        link_obj = internal_link_item.get('link')
                        if not isinstance(link_obj, dict) or 'href' not in link_obj:
                            continue 

                        internal_url_to_process = link_obj.get('href')
                        if not internal_url_to_process or not isinstance(internal_url_to_process, str):
                            continue 
                        
                        if internal_url_to_process in journal:
                            logger.debug(f"Внутренняя ссылка {internal_url_to_process} (из {supplier_file_path.name}) уже обработана ранее (согласно логу директории '{supplier_dir_name}'). Поиск следующей.")
                            continue 

                        logger.info(f"Найдена необработанная внутренняя ссылка: {internal_url_to_process} из файла {supplier_file_path.name}")
                        
                        processed_page_data: Optional[Dict[str, Any]] = process_single_internal_link(
                            driver_instance,
                            internal_url_to_process,
                            llm_instance
                        )

                        if processed_page_data:
                            new_data_filename = generate_timestamp_filename()
                            output_path = supplier_dir_path / new_data_filename 
                            
                            # **ФОРМИРОВАНИЕ ВЫХОДНОГО СЛОВАРЯ В НУЖНОМ ФОРМАТЕ**
                            output_data_for_json_file = {
                                internal_url_to_process: processed_page_data
                            }
                            
                            if j_dumps(output_data_for_json_file, output_path): # Сохраняем новый структурированный словарь
                                logger.info(f"Успешно сохранена информация для {internal_url_to_process} в файл: {output_path} (структура: {{url: data}})")
                                
                                journal[internal_url_to_process] = {
                                    "processed_at": datetime.now().isoformat(),
                                    "source_file_name": supplier_file_name, 
                                    "output_file_name": new_data_filename,
                                    "page_type": processed_page_data.get('page_type', 'unknown'), # Берем page_type из обработанных данных
                                    "page_url": internal_url_to_process,
                                }
                                if not j_dumps(journal, supplier_dir_path / Config.processed_internal_links_file_name):
                                    logger.error(f"Критическая ошибка: не удалось сохранить обновленный лог директории '{dir_specific_log_path}'")
                                    break

                                internal_links_processed_this_run += 1
                                one_internal_link_processed_for_this_file = True 

                        time.sleep(Config.DELAY_AFTER_LINK_PROCESSING)  # Задержка между обработкой ссылок
                        logger.info(f"Задержка на {Config.DELAY_AFTER_LINK_PROCESSING} секунд...")
                        
                    
                    if one_internal_link_processed_for_this_file:
                        break 
                
                if one_internal_link_processed_for_this_file:
                    logger.info(f"Обработана одна внутренняя ссылка из {supplier_file_path.name}. Переход к следующему исходному файлу в директории '{supplier_dir_name}'.")
                else:
                    logger.debug(f"В файле {supplier_file_path.name} (директория '{supplier_dir_name}') не найдено необработанных внутренних ссылок для обработки в этом прогоне.")
            
            logger.info(f"Завершена обработка файлов в директории '{supplier_dir_name}'.")

        logger.info("--- Сканирование всех директорий и файлов завершено для этого прогона ---")

    except KeyboardInterrupt:
        logger.warning("Обработка прервана пользователем (KeyboardInterrupt).")
    except Exception as ex:
        logger.critical('Критическая ошибка во время основного цикла обработки:', ex, exc_info=True)
    finally:
        if driver_instance:
            logger.info('Завершение работы драйвера...')
            try:
                driver_instance.quit()
            except Exception as ex_quit:
                logger.error('Ошибка при закрытии драйвера:', ex_quit, exc_info=True)

        logger.info('Итоговая статистика за этот прогон:')
        logger.info(f" - Всего исходных файлов поставщиков просканировано: {total_source_files_scanned}")
        logger.info(f" - Ошибок при загрузке/чтении исходных файлов: {error_loading_source_files_count}")
        logger.info(f" - Внутренних ссылок успешно обработано и сохранено в этом прогоне (добавлено в логи директорий): {internal_links_processed_this_run}")
        logger.info(f"--- Работа скрипта {script_name} (обработка internal_links, одна на файл, лог в директории, выход: {{url:data}}) завершена ---")