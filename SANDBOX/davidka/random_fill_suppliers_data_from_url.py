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
файла он ищет первую запись с пустым 'text', загружает HTML по её URL,
извлекаются данные (`extract_page_data`), и запись обновляется в файле,
заполняя поля 'text', 'internal_links' и другие извлеченные данные.
Предполагается, что URL-ключи в файлах уже валидны и не требуют проверки.

Основные шаги обработки одного файла:
1.  Чтение и базовая валидация JSON-файла (с использованием `j_loads`).
2.  Поиск записи с пустым полем 'text'.
3.  Получение HTML и извлечение данных (с использованием `extract_page_data`).
4.  Обновление данных найденной записи (text, internal_links и др.) и сохранение файла (потребует `j_dumps`).

Основная функция `process_supplier_link` - вызывается для каждой такой записи.

```rst
 .. module:: sandbox.davidka.random_fill_suppliers_data_from_url
```
"""

##########################################################################################################################################
##########################################################################################################################################
##                                                                                                                                      ##
##                                  ВНИМАНИЕ!!! словарь поставщика `3m.com.json` ОТЛИЧАЕТСЯ ПО СВОЕЙ СТРУКТУРЕ                          ##
##                                                                                                                                      ##
##########################################################################################################################################
##########################################################################################################################################

"""
Стандартный словарь:
```json
{
    "https://aaronia.com/spectrum-analyzer/real-time-analyzer-spectran-xfr-pro/": {
        "category": "",
        "text": "",
        "internal_links": []
    },
    "https://aaronia.com/spectrum-analyzer/real-time-analyzer-spectran-v6/": {
        "category": "",
        "text": "",
        "internal_links": []
    },...
}
```
Не стандартный словарь (пример для 3m.com):
```json
{
    "https://www.3m.com/3M/en_US/p/d/b40065688/": {
        "category": "",
        "text": "",
        "internal_links": []
    },
    "https://www.3m.com/3M/en_US/p/d/b40069425/": {
        "category": "",
        "text": "",
        "internal_links": []
    },...
}
```
"""


from pathlib import Path
import random # Оставлен, так как используется для random.shuffle
from typing import Dict, Any, List

# Стандартные импорты проекта
import header
from header import __root__
# from src import gs # Не используется в этом модуле

# --- Импорты WebDriver ---
from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox
# -------------------------
from src.utils.jjson import j_loads, j_dumps # j_dumps может понадобиться для сохранения
from src.utils.file import get_filenames_from_directory, get_directory_names
from src.logger import logger
from src.utils.printer import pprint as print # Используем кастомный print
from SANDBOX.davidka.graber import extract_page_data

class Config:
    """Класс конфигурации скрипта."""
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    # Директория с файлами поставщиков (результат работы crawl_suppliers...)
    data_by_supplier_dir: Path = Path('F:/llm/data_by_supplier')
    # Настройка для драйвера
    WINDOW_MODE: str = 'headless'


# ==============================================================================
# Основная функция
# ==============================================================================
def process_supplier_link(
    driver: Driver,
    link: str,
    data: Dict[str, Any],
    supplier_file_path: Path
) -> bool:
    """
    Обрабатывает одну ссылку из файла JSON поставщика: если поле 'text' пусто,
    загружает HTML, извлекает данные и подготавливает их к обновлению.
    Сохранение файла должно происходить после обработки всех ссылок в нем.

    Args:
        driver (Driver): Инстанс веб-драйвера для получения HTML.
        link (str): URL для обработки.
        data (Dict[str, Any]): Словарь данных, соответствующий этому URL.
        supplier_file_path (Path): Путь к файлу JSON поставщика (для логирования и потенциального сохранения).

    Returns:
        bool: True, если данные для 'text', 'internal_links' и др. были извлечены.
              False в случае ошибки или если обновление не требуется.

    Raises:
        Не генерирует исключений напрямую, ошибки логируются.
    
    Example:
        >>> # Пример вызова (требует мокирования Driver, extract_page_data)
        >>> # mock_driver = Driver(Firefox) 
        >>> # result = process_supplier_link(mock_driver, 'http://example.com', {}, Path('supplier.json'))
        >>> # print(result) # Ожидаемо False или True в зависимости от моков
    """
    # Функция извлекает текущие значения 'text' и 'internal_links'
    text_content: str = data.get('text', '')
    # internal_links_list: List[str] = data.get('internal_links', []) # Закомментировано, так как не используется в текущем фрагменте

    # Проверка, что поле 'text' действительно пустое (или состоит только из пробельных символов)
    if not text_content or text_content.isspace():
        logger.info(f"Обработка записи для URL '{link}' с пустым полем 'text' в файле '{supplier_file_path.name}'.")
        # Функция получает HTML-содержимое страницы
        raw_data_from_url: str | None = driver.fetch_html(link)

        if not raw_data_from_url:
            logger.error(f"Не удалось получить HTML для URL: {link}")
            return False

        # Функция извлекает данные из HTML
        extracted_data: Dict[str, Any] = extract_page_data(raw_data_from_url,link)

        if not extracted_data or not extracted_data.get('text'):
            logger.warning(f"Не удалось извлечь данные или текст пуст для URL: {link}")
            return False
        
        # TODO: Обновить словарь `data` из `extracted_data`
        # Например:
        # data['text'] = extracted_data.get('text')
        # data['internal_links'] = extracted_data.get('internal_links', [])
        # ... другие поля ...
        logger.info(f"Данные для URL '{link}' извлечены. Требуется обновление и сохранение файла.")
        ... # Заполнитель для логики обновления `data` и последующего сохранения файла JSON.
            # Сохранение файла (j_dumps) лучше делать один раз после обработки всех ссылок в файле.
        return True # Указывает, что данные были извлечены
    else:
        logger.debug(f"URL '{link}' в файле '{supplier_file_path.name}' уже содержит данные в поле 'text'. Пропуск.")
        return False


# ==============================================================================
# Основной блок выполнения скрипта
# ==============================================================================
if __name__ == '__main__':
    driver_instance: Driver | None = None
    processed_files_count: int = 0
    text_updated_in_files_count: int = 0 # Счетчик файлов, в которых хотя бы одна запись была обновлена
    error_files_count: int = 0
    total_links_processed_count: int = 0
    total_links_updated_count: int = 0
    
    # Переменные для цикла
    supplier_dir_path: Path
    supplier_file_path: Path
    supplier_data: dict | list
    
    # Счетчик всех обнаруженных файлов для статистики
    total_discovered_files_count: int = 0


    logger.info(f"--- Начало работы скрипта {Path(__file__).name} ---")
    logger.info(f"Поиск файлов поставщиков в: {Config.data_by_supplier_dir}")
    # logger.info(f"Файл для логирования обновленных поставщиков: {Config.ENDPOINT / 'updated_suppliers.txt'}") # Эта функциональность не реализована

    # --- Инициализация драйвера ---
    try:
        driver_instance = Driver(Firefox, window_mode=Config.WINDOW_MODE)
        logger.info('Драйвер успешно инициализирован.')

        logger.info('Получение списка директорий поставщиков...')
        suppliers_dirs_list: List[str] = get_directory_names(Config.data_by_supplier_dir) # БАГ! Функция не принимает `*.json` (комментарий сохранен)
        if not suppliers_dirs_list:
            logger.warning(f'Не найдено директорий поставщиков в {Config.data_by_supplier_dir}')
        else:
            logger.info(f'Найдено {len(suppliers_dirs_list)} директорий поставщиков. Перемешивание...')
            random.shuffle(suppliers_dirs_list) # Перемешивание списка директорий

        for supplier_dir_name in suppliers_dirs_list:
            supplier_dir_path = Config.data_by_supplier_dir / supplier_dir_name
            logger.info(f"Обработка директории: {supplier_dir_path}")
            
            supplier_file_names: List[str] = get_filenames_from_directory(supplier_dir_path)
            if not supplier_file_names:
                logger.info(f"Не найдено JSON файлов в директории: {supplier_dir_path}")
                continue
            
            total_discovered_files_count += len(supplier_file_names)

            for supplier_file_name in supplier_file_names:
                supplier_file_path = supplier_dir_path / supplier_file_name
                logger.debug(f"Обработка файла: {supplier_file_path}")
                # total_files_attempted += 1 # Заменено на processed_files_count или error_files_count

                # Функция загружает данные из JSON файла
                supplier_data = j_loads(supplier_file_path)

                if not supplier_data:
                    # j_loads уже залогировал ошибку и вернул пустую структуру
                    logger.warning(f"Не удалось загрузить данные или файл пуст: {supplier_file_path}. Пропуск файла.")
                    error_files_count += 1
                    continue # Переход к следующему файлу

                # Флаг, что в текущем файле были обновления
                current_file_had_updates: bool = False

                if isinstance(supplier_data, dict):
                    for key, value_dict in supplier_data.items():
                        if isinstance(value_dict, dict):
                            total_links_processed_count +=1
                            if process_supplier_link(driver_instance, key, value_dict, supplier_file_path):
                                current_file_had_updates = True
                                total_links_updated_count +=1
                        else:
                            logger.warning(f"Значение для ключа '{key}' в файле '{supplier_file_path}' не является словарем. Пропуск элемента.")
                elif isinstance(supplier_data, list):
                    for item in supplier_data:
                        if isinstance(item, dict):
                            for key, value_dict in item.items():
                                if isinstance(value_dict, dict):
                                    total_links_processed_count +=1
                                    if process_supplier_link(driver_instance, key, value_dict, supplier_file_path):
                                        current_file_had_updates = True
                                        total_links_updated_count +=1
                                else:
                                    logger.warning(f"Значение для ключа '{key}' в элементе списка в файле '{supplier_file_path}' не является словарем. Пропуск элемента.")
                        else:
                             logger.warning(f"Элемент в списке в файле '{supplier_file_path}' не является словарем. Пропуск элемента.")
                else:
                    # Эта ветка не должна достигаться, если j_loads всегда возвращает dict или list (включая пустые при ошибке)
                    logger.error(f"Неожиданный тип данных ({type(supplier_data)}) после загрузки файла {supplier_file_path}. Пропуск файла.")
                    error_files_count += 1
                    continue # Переход к следующему файлу
                
                processed_files_count += 1
                if current_file_had_updates:
                    text_updated_in_files_count += 1
                    # TODO: Здесь должна быть логика сохранения обновленного supplier_data в supplier_file_path
                    # logger.info(f"Файл {supplier_file_path} был обновлен и требует сохранения.")
                    # if not j_dumps(supplier_data, supplier_file_path, indent=4):
                    #     logger.error(f"Ошибка сохранения файла: {supplier_file_path}")
                    # else:
                    #     logger.info(f"Файл {supplier_file_path} успешно сохранен.")
                    ... # Заполнитель для логики сохранения

    except Exception as ex:
        logger.critical('Критическая ошибка во время выполнения (вне цикла обработки файлов):', ex, exc_info=True)
    finally:
        if driver_instance:
            logger.info('Завершение работы драйвера...')
            try:
                driver_instance.quit()
            except Exception as ex_quit:
                logger.error('Ошибка при закрытии драйвера:', ex_quit, exc_info=True)

    logger.info('--- Обработка файлов завершена ---')
    logger.info('Статистика:')
    logger.info(f" - Всего директорий поставщиков обработано: {len(suppliers_dirs_list) if 'suppliers_dirs_list' in locals() else 0}")
    logger.info(f" - Всего файлов JSON обнаружено: {total_discovered_files_count}")
    logger.info(f" - Файлов JSON успешно загружено и обработано: {processed_files_count}")
    logger.info(f" - Файлов, в которых обновлены данные (хотя бы одна ссылка): {text_updated_in_files_count}") # TODO: Этот счетчик зависит от логики в `...`
    logger.info(f" - Всего ссылок обработано: {total_links_processed_count}")
    logger.info(f" - Всего ссылок, для которых извлечены новые данные: {total_links_updated_count}") # TODO: Этот счетчик зависит от логики в `...`
    logger.info(f" - Ошибок при загрузке/обработке файлов: {error_files_count}")
    logger.info(f"--- Работа скрипта {Path(__file__).name} завершена ---")
