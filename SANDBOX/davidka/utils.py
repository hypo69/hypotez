## \file /sandbox/davidka/utils.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Вспомогательные утилиты для проекта crawler.py
===============================================
Содержит функции для чтения и обработки данных из файлов,
используемых для сбора информации о товарах.

```rst
.. module:: sandbox.davidka.utils
```
"""
import re
import random
from pathlib import Path
from typing import List, Optional, Generator, Union, Dict, Set, Any
from types import SimpleNamespace

# -----------------

import header
from header import __root__
from src import gs
from src.utils.jjson import j_loads, j_loads_ns, j_dumps, sanitize_json_files
from src.utils.file import get_filenames_from_directory 
from src.logger.logger import logger
from src.utils.file import  recursively_read_text_files, recursively_get_file_path, read_text_file
from src.utils.printer import pprint as print 
from src.utils.file import save_text_file
from src.utils.url import get_domain

class Config:
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    config:SimpleNamespace = j_loads_ns(ENDPOINT/'davidka.json')
    mining_data_path: Path= Path(config.random_urls)

    #train_data_supplier_categories_path: Path = ENDPOINT / 'train_data_supplier_categories'
    #checked_domains: list = read_text_file(ENDPOINT / 'checked_domains.txt', as_list=True)
    crawl_files_list: list = get_filenames_from_directory(mining_data_path, 'json')
    instruction_grab_product_page_simple_driver: str = (ENDPOINT / 'instructions' / 'grab_product_page_simple_driver.md').read_text(encoding='utf-8')
    instruction_get_supplier_categories: str = (ENDPOINT / 'instructions' / 'get_supplier_categories.md').read_text(encoding='utf-8')
    instruction_find_product_in_supplier_domain: str = (ENDPOINT / 'instructions' / 'find_product_in_supplier_domain.md').read_text(encoding='utf-8')
    instruction_for_products_urls_one_product: str = (ENDPOINT / 'instructions' / 'get_product_links_one_product.md').read_text(encoding='utf-8')
    instruction_links_from_search: str = (ENDPOINT / 'instructions' / 'links_from_search.md').read_text(encoding='utf-8')
    instruction_links_from_searh_page: str = (ENDPOINT / 'instructions' / 'links_from_searh_page.md').read_text(encoding='utf-8')
    GEMINI_API_KEY = gs.credentials.gemini.onela.api_key


def build_list_of_checked_urls() -> bool:
    """
    Собираю список проверенных url, из `random_urls`. Это адреса поставщиков, которые я сгенерировал через gemini
    в список проверенных url, чтобы не проверять их повторно. Оперция одноразовая, но может пригодиться в будущем.
    """

    ...
    datafiles_list:list = j_loads(Config.output_dir)
    for datafile in datafiles_list:
        try:
            if hasattr(datafile, 'url'):
                if  datafile['url'] in Config.checked_urls:
                    logger.info(f'URL уже в списке проверенных: {datafile["url"]}')
                    continue

                Config.checked_urls.append(datafile['url'])
                save_text_file(Config.checked_urls, Config.output_dir/'checked_urls.txt')

        except Exception as ex:
            logger.error(f'Ошибка при обработке файла {datafile}', ex, exc_info=True)
            continue
        
def update_checked_urls_file(url:str) -> bool:
    """Функция добавляет `URL` в список проверенных"""
    Config.checked_urls.append(url)
    if not save_text_file(Config.checked_urls,Config.output_dir/'checked_urls.txt'):
        logger.error(f'Ошибка записи в файл {Config.output_dir/"checked_urls.txt"}', None, True)
        return False
    logger.success(f'URL {url} добавлен в список проверенных.')
    return True

def extract_domain_from_products_urls() -> bool:
    """
    Функция вытаскивает домен из url в дiректории  `random_urls`
    """
    files_list:list = get_filenames_from_directory(Config.ENDPOINT/'random_urls', 'json')
    checked_domains:list = read_text_file(Config.ENDPOINT/'checked_domains.txt',as_list=True)
    for file in files_list:
        products_dict:dict = j_loads(Config.ENDPOINT/'random_urls'/file)
        if not products_dict: continue
        for product in products_dict['products']:
            product_url = product['product_url']
            domain = get_domain(product_url)
            if domain not in checked_domains:
                checked_domains.append(domain)
                save_text_file(checked_domains, Config.ENDPOINT/'checked_domains.txt')
                j_dumps(checked_domains, Config.ENDPOINT/'checked_domains.json')
    return True


def get_products_urls_list_from_files(
    mining_data_path: Path,
    crawl_files_list: Optional[List[str]] = None
) -> List[str]:
    """
    Функция читает URL товаров из файлов словарей JSON.

    Читает файлы из указанной директории `mining_data_path`. Если передан
    список `crawl_files_list`, обрабатываются только файлы из этого списка,
    иначе обрабатываются все JSON-файлы в директории. Из каждого файла
    извлекается список товаров (ключ 'products'), а из него - URL
    (ключ 'product_url'). Все URL собираются в один список, перемешиваются
    и возвращаются.

    Args:
        mining_data_path (Path): Путь к директории с файлами данных.
        crawl_files_list (Optional[List[str]], optional): Список имен файлов
            для обработки. Если None, обрабатываются все .json файлы
            в `mining_data_path`. По умолчанию None.

    Returns:
        List[str]: Перемешанный список URL товаров.
    """
    # Объявление переменных
    products_urls_list: List[str] = []
    target_files: List[str]
    filename: str
    file_path: Path
    crawl_data: Dict[str, Any] | List[Any] # Тип данных после j_loads
    products_data: List[Any] = [] # Инициализация
    product: Dict[str, Any] # Элемент списка crawl_data

    # Определяем список файлов для обработки
    if not crawl_files_list:
        target_files = get_filenames_from_directory(mining_data_path, '*.json') # Ищем json по умолчанию
        logger.debug(f'Обработка всех json файлов из {mining_data_path}')
    else:
        target_files = crawl_files_list
        logger.debug(f'Обработка файлов из переданного списка: {len(target_files)} шт.')

    # Обработка каждого файла
    for filename in target_files:
        try:
            file_path = mining_data_path / filename
            # Загрузка данных из JSON файла
            crawl_data = j_loads(file_path)
            # Проверка и извлечение списка товаров
            if isinstance(crawl_data, dict) and 'products' in crawl_data:
                products_data = crawl_data['products'] # Тип будет проверен ниже
            elif isinstance(crawl_data, list): # Допускаем файл как список товаров
                products_data = crawl_data
                logger.debug(f"Файл {filename} содержит список товаров напрямую.")
            else:
                logger.warning(f"Файл {filename} не содержит ключ 'products' или не является списком.", None, False)
                continue # Переход к следующему файлу

            # Проверка типа извлеченных товаров
            if isinstance(products_data, list):
                 # Извлечение URL
                for product_item in products_data: # Переименована переменная цикла
                    if isinstance(product_item, dict) and 'product_url' in product_item:
                        # Проверка типа URL и его наличия
                        product_url = product_item['product_url']
                        if isinstance(product_url, str) and product_url:
                             products_urls_list.append(product_url)
                        else:
                            logger.warning(f"Значение 'product_url' в файле {filename} не является строкой или пустое: {product_url}", None, False)
                    else:
                         logger.warning(f"Элемент в файле {filename} не словарь или отсутствует 'product_url': {product_item}", None, False)
            else:
                 logger.warning(f"Извлеченные 'products' в файле {filename} не являются списком (тип: {type(products_data)}).", None, False)

        except FileNotFoundError:
             logger.error(f'Файл не найден: {file_path}', None, False)
             continue
        except Exception as ex:
            # Логирование ошибки обработки файла
            logger.error(f'Ошибка при обработке файла {filename=}', ex, exc_info=True)
            # Продолжаем обработку следующих файлов
            continue

    # Перемешивание списка URL
    random.shuffle(products_urls_list)
    logger.info(f"Собрано и перемешано {len(products_urls_list)} URL товаров.")
    # Возвращаем список (даже если пустой)
    return products_urls_list


def yield_product_urls_from_files(
    directory: Path,
    pattern: str = '*.json' # Используем стандартный паттерн glob
) -> Generator[str, None, None]:
    """
    Функция возвращает генератор URL товаров из файлов директории.

    Используется для обработки больших объемов данных без загрузки всех URL
    в память одновременно. Находит файлы по паттерну в указанной директории,
    читает каждый файл, извлекает URL товаров и выдает их по одному через yield.

    Args:
        directory (Path): Путь к директории с файлами данных.
        pattern (str, optional): Паттерн для поиска файлов (glob).
                                  По умолчанию '*.json'.

    Yields:
        Generator[str, None, None]: Генератор, возвращающий URL товаров по одному.
    """
    # Объявление переменных
    filenames: List[Path]
    filename: Path
    crawl_data: Union[Dict[str, Any], List[Any]]
    products_data: List[Any] = [] # Инициализация
    product_item: Dict[str, Any] # Переименована переменная цикла

    logger.debug(f"Запуск генератора URL из {directory} по паттерну '{pattern}'")
    # Получение списка файлов по абсолютному пути
    try:
        filenames = list(directory.glob(pattern))
        logger.info(f"Найдено {len(filenames)} файлов для обработки генератором.")
    except Exception as ex:
         logger.error(f"Ошибка при поиске файлов в директории {directory} по паттерну {pattern}", ex, exc_info=True)
         return # Завершаем генератор при ошибке поиска файлов

    # Обработка каждого файла
    for filename in filenames:
        try:
            # Загрузка данных из JSON файла
            crawl_data = j_loads(filename) # Передаем Path объект

            # Извлечение списка товаров
            if isinstance(crawl_data, dict) and 'products' in crawl_data:
                products_data = crawl_data['products']
            elif isinstance(crawl_data, list):
                products_data = crawl_data
                logger.debug(f"Файл {filename.name} содержит список товаров напрямую (генератор).")
            else:
                logger.warning(f"Файл {filename.name} не содержит ключ 'products' или не является списком (генератор).", None, False)
                continue # Переход к следующему файлу

            # Проверка типа извлеченных товаров
            if isinstance(products_data, list):
                # Извлечение и возврат URL через yield
                for product_item in products_data:
                    if isinstance(product_item, dict) and 'product_url' in product_item:
                        product_url = product_item['product_url']
                        if isinstance(product_url, str) and product_url:
                            yield product_url # Возвращаем URL
                        else:
                            logger.warning(f"Значение 'product_url' в файле {filename.name} не строка или пустое (генератор): {product_url}", None, False)
                    else:
                        logger.warning(f"Элемент в файле {filename.name} не словарь или отсутствует 'product_url' (генератор): {product_item}", None, False)
            else:
                 logger.warning(f"Извлеченные 'products' в файле {filename.name} не являются списком (генератор, тип: {type(products_data)}).", None, False)

        except FileNotFoundError:
             logger.error(f'Файл не найден (генератор): {filename}', None, False)
             continue
        except Exception as ex:
            # Логирование ошибки обработки файла
            logger.error(f'Ошибка при обработке файла {filename.name} в генераторе', ex, exc_info=True)
            # Продолжаем обработку следующих файлов
            continue


def get_categories_from_random_urls(crawl_files_list: list = None) -> list:
    """Возвращает все категории из файлов в директории 'random_urls' 
    Директория собрана из словарей, полученных вручную через gemini aiu studio (katia).
    """
    categories_list = []
    for filename in crawl_files_list or Config.crawl_files_list:
        try:
            file_path = Config.mining_data_path / filename
            crawl_data = j_loads(file_path)
            crawl_data = crawl_data.get('products', [])
            for product in crawl_data:
                if 'parent_category' in product:
                    categories_list.append(product['parent_category'])
                if 'category_name' in product:
                    categories_list.append(product['category_name'])
        except Exception as ex:
            logger.error(f'Ошибка при обработке файла {filename=}', ex, exc_info=True)
    categories_list = list(filter(None, set(categories_list)))
    random.shuffle(categories_list)
    return categories_list



def fetch_urls_from_all_mining_files(dir_path: Path| List[Path]  = ['mined_urls','random_urls','output_product_data_set1']) -> List[str]: 
    """
    Читает все файлы (рекурсивно, как определено в recursively_get_file_path)
    в указанных директориях (относительно Config.ENDPOINT)
    и возвращает список всех найденных URL (http:// или https://),
    которые могут находиться в любом месте строки и быть в кавычках.

    Args:
        dir_path (Union[Path, List[Path]]): Один или несколько объектов Path,
                 представляющих директории для поиска (относительно Config.ENDPOINT).

    Returns:
        List[str]: Список найденных URL строк. Возвращает пустой список в случае ошибки.
                   Может содержать дубликаты, если они найдены в разных местах.
                   Рассмотрите возможность добавления set() для уникальности, если нужно.
    """
    URL_PATTERN = re.compile(r'https?://\S+')
    found_urls = []
    files_list: list = []

    dir_path_list = [dir_path] if not isinstance(dir_path, list) else dir_path
    try:
        for dp in dir_path_list:
           
            files_list = recursively_get_file_path(Config.ENDPOINT / dp)
            # ----------------------------------------
            for file in files_list:
                # read_text_file возвращает список строк
                lines: list = read_text_file(file, as_list=True)
                # -----------------------------
                if len(lines)<1:
                    logger.warning(f"Файл {file} пустой или не содержит строк.", None, False)
                    continue
                
                for line in lines:
                    # Ищем все совпадения URL паттерна в текущей строке
                    matches = URL_PATTERN.findall(line)
                    for match in matches:
                        # Очищаем найденный URL от возможных окружающих кавычек и пробелов
                        cleaned_url = match.strip().strip('\'"')
                        # Добавляем очищенный URL в список результатов
                        # Проверка на startswith уже не нужна, т.к. regex это гарантирует
                        found_urls.append(cleaned_url)
              
    except OSError as ex:
        logger.error(f"Ошибка доступа к элементам директории '{dp}':", ex)
        # ----------------
    except TypeError as ex:
        logger.error(ex)
        # ----------------
    except Exception as ex:
        logger.error(ex)
        # ----------------

    found_urls = list(set(found_urls))
    random.shuffle(found_urls)
    return  found_urls

import os
import random

import os
import random

def files_mixer(base_path):
    """
    Генератор, который получает имена директорий из base_path,
    перемешивает их, затем из каждой директории выбирает один
    случайный файл и возвращает (yields) полный путь к этому файлу.
    """
    if not os.path.isdir(base_path):
        # Можно вывести сообщение об ошибке, если это критично для логики вызывающего кода
        # print(f"Ошибка: Базовый путь '{base_path}' не является директорией или не существует.")
        return # Завершаем генератор, он ничего не вернет

    # 1. Получаем имена всех элементов в базовой директории
    try:
        all_entries = os.listdir(base_path)
    except PermissionError:
        # print(f"Ошибка: Нет прав доступа к директории '{base_path}'.")
        return # Завершаем генератор

    # 2. Фильтруем, оставляя только директории
    directories = [d for d in all_entries if os.path.isdir(os.path.join(base_path, d))]

    if not directories:
        # print(f"В директории '{base_path}' не найдено поддиректорий.")
        return # Завершаем генератор

    # 3. Перемешиваем директории
    # Важно: перемешиваем копию, если планируется использовать оригинальный список `directories` где-то еще
    # или если генератор может быть вызван несколько раз с одним и тем же внутренним состоянием
    # (хотя для простого генератора, который отрабатывает один раз, это не так критично).
    # В данном случае, т.к. directories создается внутри функции, это не обязательно,
    # но хорошая практика, если есть сомнения.
    shuffled_directories = list(directories) # Создаем копию для перемешивания
    random.shuffle(shuffled_directories)
    # print(f"Перемешанный порядок директорий (для выбора файлов): {shuffled_directories}\n") # Для отладки

    # 4. Обрабатываем каждую директорию из перемешанного списка
    for dir_name in shuffled_directories:
        current_dir_path = os.path.join(base_path, dir_name)

        try:
            # Получаем список файлов в текущей директории
            # os.listdir() может вернуть пустой список, если директория пуста или содержит только поддиректории
            entries_in_subdir = os.listdir(current_dir_path)
            files_in_dir = [f for f in entries_in_subdir
                            if os.path.isfile(os.path.join(current_dir_path, f))]
        except PermissionError:
            # print(f"  Предупреждение: Нет прав доступа к файлам в директории '{current_dir_path}'. Пропускаем.")
            continue # Переходим к следующей директории из списка 'shuffled_directories'

        if not files_in_dir:
            # Если в директории нет файлов (но сама директория читаема)
            # print(f"  В директории '{current_dir_path}' нет файлов. Пропускаем.") # Для отладки
            continue # Переходим к следующей директории из списка 'shuffled_directories'

        # 5. Выбираем один случайный файл
        random_file_name = random.choice(files_in_dir)
        file_path = os.path.join(current_dir_path, random_file_name)

        yield file_path



# --- Основная часть скрипта ---
if __name__ == "__main__":

    res_dict:dict = build_list_of_checked_urls()
    ...

    # urls_for_mining:list = fetch_urls_from_all_mining_files(['random_urls','output_product_data_set1'])
    # print(urls_for_mining)
    ...

    # # Запрашиваем путь у пользователя
    # target_dir_str = input("Введите путь к директории (оставьте пустым для текущей директории): ").strip()

    # # Если пользователь ничего не ввел, используем текущую директорию
    # if not target_dir_str:
    #     target_dir_str = '.' # '.' означает текущую директорию

    # # Создаем объект Path из введенной строки
    # input_path = Path(target_dir_str)

    # # Получаем абсолютный (разрешенный) путь для надежности и понятных сообщений
    # # resolve() также проверяет существование пути на раннем этапе (хотя наша функция это тоже делает)
    # try:
    #     target_path_resolved = input_path.resolve(strict=True) # strict=True вызовет ошибку, если путь не существует
    # except FileNotFoundError:
    #     print(f"Ошибка: Директория '{input_path}' не найдена.", file=sys.stderr)
    #     target_path_resolved = None # Устанавливаем в None, чтобы не вызывать функцию
    # except Exception as e: # Ловим другие возможные ошибки resolve()
    #     print(f"Ошибка при обработке пути '{input_path}': {e}", file=sys.stderr)
    #     target_path_resolved = None


    # urls = None # Инициализируем результат
    # if target_path_resolved: # Проверяем, что путь был успешно разрешен
    #     # Вызываем функцию поиска URL, передавая объект Path
    #     urls = find_http_urls_in_directory_pathlib(target_path_resolved)

    # # Выводим итоговый результат
    # print(f"\n{'-'*30}\nИтоговый список найденных URL:\n{'-'*30}")
    # if urls is not None: # Проверяем, что функция выполнилась без ошибки директории
    #     if urls:
    #         for url in urls:
    #             print(url)
    #     else:
    #         print("URL, начинающиеся с http:// или https://, не найдены в файлах директории.")
    # else:
    #     # Сообщение об ошибке уже было выведено ранее (либо при resolve, либо в функции)
    #     print("Поиск не был выполнен из-за ошибки доступа к директории или её отсутствия.")


    # # Пример использования функции files_mixer

    #     # Укажите путь к вашей базовой директории
    # # Для примера, создадим ту же структуру, что и раньше:
    # base_test_dir = "my_base_test_directory_mixer"
    # os.makedirs(os.path.join(base_test_dir, "dir_one"), exist_ok=True)
    # os.makedirs(os.path.join(base_test_dir, "dir_two"), exist_ok=True)
    # os.makedirs(os.path.join(base_test_dir, "dir_three"), exist_ok=True)
    # os.makedirs(os.path.join(base_test_dir, "dir_four_empty"), exist_ok=True)

    # with open(os.path.join(base_test_dir, "dir_one", "file_1a.txt"), "w") as f: f.write("1A")
    # with open(os.path.join(base_test_dir, "dir_one", "file_1b.dat"), "w") as f: f.write("1B")
    # with open(os.path.join(base_test_dir, "dir_two", "file_2a.log"), "w") as f: f.write("2A")
    # with open(os.path.join(base_test_dir, "dir_three", "file_3a.conf"), "w") as f: f.write("3A")
    # with open(os.path.join(base_test_dir, "dir_three", "file_3b.ini"), "w") as f: f.write("3B")
    # with open(os.path.join(base_test_dir, "dir_three", "file_3c.json"), "w") as f: f.write("3C")
    # with open(os.path.join(base_test_dir, "some_other_file.txt"), "w") as f: f.write("This is not in a subdir")

    # # Запускаем основную функцию
    # random_paths = files_mixer(base_test_dir)

    # if random_paths:
    #     print(f"Перемешанный порядок директорий, из которых выбраны файлы (порядок соответствует списку ниже):")
    #     # Чтобы показать, из каких директорий брались файлы в каком порядке:
    #     ordered_parent_dirs = [os.path.dirname(p) for p in random_paths]
    #     # Убираем дубликаты, сохраняя порядок (Python 3.7+)
    #     unique_ordered_parent_dirs = list(dict.fromkeys(ordered_parent_dirs))
    #     for parent_dir in unique_ordered_parent_dirs:
    #         print(f" - {os.path.basename(parent_dir)}") # Выводим только имя директории

    #     print("\nСлучайно выбранные пути к файлам:")
    #     for path in random_paths:
    #         print(path)
    # else:
    #     print("Не удалось получить пути к файлам.")