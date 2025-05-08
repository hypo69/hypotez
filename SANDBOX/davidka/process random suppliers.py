## \file /sandbox/davidka/process random suppliers.py
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
  python process random suppliers.py [username]

Если `username` не указан, по умолчанию используется 'onela'.
Например:
  python process random suppliers.py               # Использует ключ 'onela'
  python process random suppliers.py kazarinov     # Использует ключ 'kazarinov'

```rst
 .. module:: sandbox.davidka.process random suppliers
```
"""


import argparse
from pathlib import Path
import random
from typing import Dict, Any, List
from types import SimpleNamespace
import sys
import time

# Стандартные импорты проекта
# Убедитесь, что эти импорты работают в вашем окружении
import header
from header import __root__ 
from src import gs

# --- Импорты WebDriver ---
from src.credentials import j_loads_ns
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
    # Конечная точка для файлов, связанных с этим скриптом davidka
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    config:SimpleNamespace = j_loads_ns(ENDPOINT / 'davidka.json')
    STORAGE:str = config.storage
    WINDOW_MODE: str = 'headless' 
    GEMINI_API_KEY: str | None = None 
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

    # Извлечение текущего текстового содержимого для ссылки
    text_content: str = current_data_for_link.get('text', '')

    # Проверка, является ли текстовое содержимое пустым или состоит только из пробельных символов
    if not text_content or text_content.isspace():
        logger.info(f"\n ---------------------------------\n Обработка записи для URL '{link}' с пустым полем 'text' в файле '{supplier_file_path=}'. \n --------------------------------\n")

        # Загрузка HTML-содержимого страницы по указанной ссылке
        raw_data_from_url: str | None = driver.fetch_html(link)

        # Проверка, удалось ли загрузить HTML
        if not raw_data_from_url:
            logger.error(f"Не удалось получить HTML для URL: {link}")
            # Возврат словаря с указанием типа страницы 'unknown' и ошибки
            return {'page_type':'unknown','error':'page not found'}

        # Извлечение структурированных данных из HTML
        extracted_page_content: Dict[str, Any] = extract_page_data(raw_data_from_url, link)
        
        # Проверка, были ли извлечены данные и не пуст ли текст
        if not extracted_page_content or not extracted_page_content.get('text'):
            logger.warning(f"Не удалось извлечь данные или текст пуст для URL: {link} из файла {supplier_file_path.name}")
            # Возврат словаря с указанием типа страницы 'unknown' и ошибки извлечения
            return {'page_type':'unknown','error':'error while extarct'}

        # Подготовка данных для запроса к LLM
        request_dict = extracted_page_content
        del(request_dict['html']) # Удаление HTML-кода из данных для LLM, чтобы не мешал
        # Формирование строки запроса для LLM
        q:str = f"""`{str(request_dict)}`"""

        # Отправка запроса к LLM и получение ответа в формате JSON
        a:dict = j_loads(llm.ask(q))
        # Обновление поля 'page_type' в извлеченных данных, если оно есть в ответе LLM
        if hasattr(a, 'page_type'): extracted_page_content['page_type'] = a.get('page_type', '') ; del(a['page_type'])
        # Проверка наличия поля 'category' в извлеченных данных
        if hasattr(extracted_page_content, 'category'): 
            #extracted_page_content['categoty_name'] = getattr(extracted_page_content,'category', '') # <- временная категория из начального набора данных
            # Удаление временного поля 'category'
            del(extracted_page_content['category']) 

        # Обновление или добавление ссылок на продукты
        if hasattr(a, 'product_links'): 
            if extracted_page_content['product_links'] and isinstance(extracted_page_content['product_links'], list):
               # Добавление новых ссылок и удаление дубликатов
               extracted_page_content['product_links'].append(getattr(a,'product_links',[]))
               extracted_page_content['product_links'] = list(set(extracted_page_content))
            else:                                                  
                # Установка ссылок на продукты из ответа LLM
                extracted_page_content['product_links'] = getattr(a,'product_links',[])
            # Удаление поля 'product_links' из ответа LLM после использования
            del(a['product_links'])

        # Обновление полей на основе ответа LLM
        if hasattr(a, 'categoty_name'): extracted_page_content['categoty_name'] = a.get('categoty_name', '') ; del(a['categoty_name'])
        if hasattr(a, 'parent_category'): extracted_page_content['parent_category'] = a.get('parent_category', '') ; del(a['parent_category'])
        if hasattr(a, 'title'): extracted_page_content['title'] = a.get('title', '') ; del(a['title'])
        if hasattr(a, 'summary'): extracted_page_content['summary'] = a.get('summary', '') ; del(a['summary'])
        if hasattr(a, 'descrition'): extracted_page_content['descrition'] = a.get('descrition', '') ; del(a['descrition'])
        if hasattr(a, 'specification'): extracted_page_content['specification'] = a.get('specification', '') ; del(a['specification'])
        if hasattr(a, 'notes'): extracted_page_content['notes'] = a.get('notes', '') ; del(a['notes'])
        if hasattr(a, 'price'): extracted_page_content['price'] = a.get('price', '') ; del(a['price'])

        # Сохранение полного ответа LLM (за вычетом уже обработанных полей)
        extracted_page_content['ai_analized_content'] = a 
        ...
        # Обновление исходного словаря данных `current_data_for_link` извлеченными и обогащенными данными
        for key_from_extraction, value_from_extraction in extracted_page_content.items():
            current_data_for_link[key_from_extraction] = value_from_extraction
        
        logger.info(f"Данные для URL '{link}' извлечены и словарь обновлен.")
        # Задержка для предотвращения блокировок со стороны веб-сайтов при частых запросах
        time.sleep(15) 
        return current_data_for_link # Возврат обновленного словаря
    else:
        # Эта ветка не должна достигаться, так как проверка text_content выполняется перед вызовом этой функции.
        # Оставлено для дополнительной защиты.
        logger.debug(f"URL '{link}' в файле '{supplier_file_path.name}' уже содержит данные (внутренняя проверка). Пропуск.")
        # Возврат None, так как обновления не производились
        return None


# ==============================================================================
# Основной блок выполнения скрипта
# ==============================================================================
if __name__ == '__main__':
    # Определение имени текущего скрипта
    script_name = Path(__file__).name
    # Создание парсера аргументов командной строки
    parser = argparse.ArgumentParser(
        description="Сбор данных по ссылкам поставщиков. По умолчанию используется Gemini API ключ для 'onela'.",
        usage=f"python {script_name} [username]",
        epilog=f"Примеры:\n"
               f"  python {script_name}                  # Использует ключ пользователя 'onela'\n"
               f"  python {script_name} kazarinov        # Использует ключ пользователя 'kazarinov'",
        formatter_class=argparse.RawTextHelpFormatter
    )
    # Добавление аргумента 'user' для указания имени пользователя
    parser.add_argument(
        'user',
        type=str,
        nargs='?', # Аргумент необязательный
        default='onela', # Значение по умолчанию
        help="Имя пользователя для выбора Gemini API ключа (например, 'kazarinov'). \n"
             "Если не указано, по умолчанию используется 'onela'. \n"
             "Ключ будет взят из gs.credentials.gemini.<user>.api_key."
    )
    # Парсинг аргументов командной строки
    args = parser.parse_args()
    # Извлечение имени пользователя из аргументов
    username = args.user

    logger.info(f"--- Начало работы скрипта {script_name} для пользователя '{username}' ---")

    # Попытка получения API ключа Gemini для указанного пользователя
    try:
        # Динамическое получение конфигурации пользователя из `gs.credentials.gemini`
        user_gemini_config = getattr(gs.credentials.gemini, username)
        # Установка API ключа в конфигурацию скрипта
        Config.GEMINI_API_KEY = getattr(user_gemini_config, 'api_key')
        logger.info(f"Успешно получен и установлен Gemini API ключ для пользователя: '{username}'")
    except AttributeError:
        # Обработка ошибки, если API ключ для пользователя не найден
        logger.critical(f"Ошибка: не удалось найти API ключ для пользователя '{username}'. "
                        f"Проверьте, существует ли 'gs.credentials.gemini.{username}.api_key'.")
        sys.exit(1) # Завершение работы скрипта с кодом ошибки

    # Проверка, что API ключ не пустой
    if not Config.GEMINI_API_KEY:
        logger.critical(f"Ошибка: API ключ для пользователя '{username}' пустой.")
        sys.exit(1) # Завершение работы скрипта с кодом ошибки

    # Инициализация переменных для LLM и драйвера
    llm_instance: GoogleGenerativeAi | None = None
    # Попытка инициализации экземпляра GoogleGenerativeAi
    try:
        llm_instance = GoogleGenerativeAi(
            Config.GEMINI_API_KEY, 
            Config.GEMINI_MODEL_NAME, 
            {'response_mime_type':'application/json'}, # Параметры для LLM
            Config.system_instructuction) # Системная инструкция для LLM
        logger.info("Инстанс GoogleGenerativeAi успешно инициализирован.")
    except Exception as e:
        # Обработка ошибки инициализации LLM
        logger.critical(f"Не удалось инициализировать GoogleGenerativeAi: {e}", None, exc_info=True)
        sys.exit(1) # Завершение работы скрипта с кодом ошибки

    # Инициализация переменных для статистики и состояния
    driver_instance: Driver | None = None
    processed_files_count: int = 0 # Счетчик обработанных файлов
    text_updated_in_files_count: int = 0  # Счетчик файлов, в которых были обновлены данные
    error_files_count: int = 0 # Счетчик файлов, при обработке которых произошла ошибка
    total_links_processed_for_update_attempt: int = 0  # Общее количество ссылок, для которых была предпринята попытка обновления
    total_links_successfully_updated: int = 0  # Общее количество успешно обновленных ссылок
    
    total_discovered_files_count: int = 0 # Общее количество обнаруженных файлов
    suppliers_dirs_list: List[str] = [] # Список директорий поставщиков

    logger.info(f"Поиск файлов поставщиков в: {Config.data_by_supplier_dir}")
    # Основной цикл обработки
    while True:
        try:
            # Инициализация веб-драйвера
            driver_instance = Driver(Firefox, window_mode=Config.WINDOW_MODE)
            logger.info('Драйвер успешно инициализирован.')


            # # ---------------------------- DEBUG ------------------
            # # Закомментированный блок для отладки на конкретной ссылке или файле
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
            # Получение списка имен директорий из configured data_by_supplier_dir
            suppliers_dirs_list = get_directory_names(Config.data_by_supplier_dir)
            # Проверка, найдены ли директории
            if not suppliers_dirs_list:
                logger.warning(f'Не найдено директорий поставщиков в {Config.data_by_supplier_dir}')
                sys.exit() # Завершение, если директорий нет
            else:
                logger.info(f'Найдено {len(suppliers_dirs_list)} директорий поставщиков. Перемешивание...')
                # Перемешивание списка директорий для случайного порядка обработки
                random.shuffle(suppliers_dirs_list)

            # Итерация по каждой директории поставщика
            for supplier_dir_name in suppliers_dirs_list:
                supplier_dir_path = Config.data_by_supplier_dir / supplier_dir_name
                logger.info(f"Обработка директории: {supplier_dir_path}")
            
                # Получение списка JSON-файлов в текущей директории поставщика
                supplier_file_names: List[str] = get_filenames_from_directory(supplier_dir_path, 'json') 
                # Проверка, найдены ли JSON-файлы
                if not supplier_file_names:
                    logger.info(f"Не найдено JSON файлов в директории: {supplier_dir_path}")
                    continue # Переход к следующей директории
            
                # Увеличение общего счетчика обнаруженных файлов
                total_discovered_files_count += len(supplier_file_names)

                # Итерация по каждому JSON-файлу
                for supplier_file_name in supplier_file_names:
                    supplier_file_path = supplier_dir_path / supplier_file_name
                    logger.debug(f"Обработка файла: {supplier_file_path}")

                    # Загрузка содержимого JSON-файла
                    supplier_data_content = j_loads(supplier_file_path)

                    # Проверка, успешно ли загружены данные
                    if not supplier_data_content:
                        logger.warning(f"Не удалось загрузить данные или файл пуст: {supplier_file_path}. Пропуск файла.")
                        error_files_count += 1
                        continue # Переход к следующему файлу

                    # Инициализация списка ссылок и данных для обработки
                    links_and_data_to_process = []
                    # Проверка, является ли корневой элемент JSON словарем
                    is_top_level_dict = isinstance(supplier_data_content, dict)
                
                    # Обработка данных в зависимости от структуры JSON
                    if is_top_level_dict:
                        # Если JSON - это словарь URL -> данные
                        for key, value_dict in supplier_data_content.items():
                            if isinstance(value_dict, dict):
                                links_and_data_to_process.append((key, value_dict))
                            else:
                                logger.warning(f"Значение для ключа '{key}' в файле '{supplier_file_path}' не является словарем. Пропуск элемента.")
                    elif isinstance(supplier_data_content, list):
                        # Если JSON - это список словарей (каждый словарь URL -> данные)
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
                        # Если структура JSON неизвестна
                        logger.error(f"Неожиданный тип данных ({type(supplier_data_content)}) после загрузки файла {supplier_file_path}. Пропуск файла.")
                        error_files_count += 1
                        continue # Переход к следующему файлу

                    # Флаг, указывающий, был ли файл обновлен и сохранен
                    file_was_updated_and_saved = False 

                    # Итерация по ссылкам и их данным из текущего файла
                    for link_key, original_value_dict in links_and_data_to_process:
                        # Проверка, не была ли ссылка уже обновлена ранее
                        if link_key in Config.updated_links.keys():
                            continue # Пропуск уже обработанной ссылки

                        # Извлечение текстового содержимого перед обработкой (для проверки на пустоту)
                        text_content_before_processing: str = original_value_dict.get('text', '')
                        # --------------- debug
                        # Условие для принудительной обработки или обработки только пустых 'text'
                        if True: # В текущей версии обрабатываются все (кроме updated_links)
                        #if not text_content_before_processing or text_content_before_processing.isspace(): # Оригинальное условие: обрабатывать только если 'text' пуст
                            total_links_processed_for_update_attempt += 1
                            # Вызов основной функции обработки ссылки
                            updated_dict_result = process_supplier_link(
                                driver_instance, 
                                link_key, 
                                original_value_dict, # Передача словаря, который будет изменен "на месте"
                                supplier_file_path, 
                                llm_instance
                            )
                        
                            # Проверка, были ли данные обновлены
                            if updated_dict_result:
                                logger.info(f"Данные для ссылки '{link_key}' в файле {supplier_file_path} обновлены. Сохранение файла...")
                                # Сохранение обновленных данных в JSON-файл
                                if not j_dumps(supplier_data_content, supplier_file_path): # supplier_data_content был изменен "на месте" через original_value_dict
                                    logger.error(f"Ошибка сохранения файла: {supplier_file_path}")
                                else:
                                    # Обновление списка обработанных ссылок
                                    Config.updated_links.update({link_key:getattr(original_value_dict,'page_type', '')}) # Используем original_value_dict, так как он был обновлен
                                    # Сохранение обновленного списка updated_links
                                    j_dumps(Config.updated_links, Config.ENDPOINT / 'updated_links.json')
                                    text_updated_in_files_count += 1
                                    total_links_successfully_updated += 1
                                    
                                    logger.info(f"Данные успешно обновлены")
                                    ...
                                # Установка флага, что файл был обновлен
                                file_was_updated_and_saved = True
                                break # Переход к следующему файлу после обновления одной ссылки в текущем файле
                        else:
                            logger.debug(f"URL '{link_key}' в файле '{supplier_file_path.name}' уже содержит данные. Пропуск обработки этой ссылки.")
                
                    # Увеличение счетчика обработанных файлов
                    processed_files_count += 1

                    # Логирование, если в файле не было найдено ссылок для обновления
                    if not file_was_updated_and_saved:
                         logger.debug(f"В файле {supplier_file_path} не было найдено ссылок для обновления или обновления не были успешными (все ссылки уже имели текст или обработка не удалась). Переход к следующему файлу.")

            # Вывод итоговой статистики после обработки всех директорий
            logger.info('Статистика:')
            logger.info(f" - Всего директорий поставщиков найдено: {len(suppliers_dirs_list) if suppliers_dirs_list else 0}")
            logger.info(f" - Всего файлов JSON обнаружено: {total_discovered_files_count}")
            logger.info(f" - Файлов JSON загружено и обработано (сделана попытка): {processed_files_count}")
            logger.info(f" - Файлов, в которых реально обновлены данные и файл сохранен: {text_updated_in_files_count}")
            logger.info(f" - Всего ссылок, для которых предпринята попытка обновления (текст был пуст или debug=True): {total_links_processed_for_update_attempt}")
            logger.info(f" - Всего ссылок, для которых успешно извлечены и обновлены новые данные: {total_links_successfully_updated}")
            logger.info(f" - Ошибок при загрузке/обработке файлов (не удалось загрузить JSON): {error_files_count}")
                         
        except KeyboardInterrupt:
            # Обработка прерывания пользователем (Ctrl+C)
            logger.warning("Обработка прервана пользователем (KeyboardInterrupt).")
            break # Выход из основного цикла `while True`
        except Exception as ex:
            # Обработка других критических ошибок
            logger.critical('Критическая ошибка во время выполнения (вне цикла обработки файлов):', ex, exc_info=True)
            ... # Место для дополнительной обработки или очистки, если необходимо
            break # Выход из основного цикла `while True`

    # Завершение работы веб-драйвера
    if driver_instance:
        logger.info('Завершение работы драйвера...')
        try:
            driver_instance.quit() # Закрытие браузера и освобождение ресурсов
        except Exception as ex_quit:
            logger.error('Ошибка при закрытии драйвера:', ex_quit, exc_info=True)

    logger.info('--- Обработка файлов завершена ---')

    logger.info(f"--- Работа скрипта {script_name} завершена ---")
