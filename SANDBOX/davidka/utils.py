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
from typing import List, Optional, Generator, Union, Dict, Set, Any # Добавлены Generator, Union, Dict, Set, Any

# --- Импорты проекта ---
# Предполагается, что эти модули всегда доступны
import header
from header import __root__
# from src import gs # Не используется напрямую в этих функциях
from src.utils.jjson import j_loads, j_dumps, sanitize_json_files
from src.utils.file import get_filenames_from_directory 
from src.logger.logger import logger
from src.utils.file import  recursively_read_text_files, recursively_get_file_path, read_text_file
from src.utils.printer import pprint as print 
from src.utils.file import save_text_file
from src.utils.url import get_domain

class Config:
    ENDPOINT:Path = __root__/'SANDBOX'/'davidka'
    output_dir:Path = Path("F:/llm/filtered_urls")
    #sanitize_json_files(output_dir) # <- очистка от битых словарей
    checked_urls:list = read_text_file(output_dir/'checked_urls.txt', as_list=True) or []
    checked_urls = list(set(checked_urls))


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


def get_categories_from_files(
    mining_data_path: Path,
    crawl_files_list: Optional[List[str]] = None
) -> List[str]:
    """
    Извлекает все уникальные названия категорий из файлов словарей JSON.

    Читает файлы из указанной директории `mining_data_path`. Если передан
    список `crawl_files_list`, обрабатываются только файлы из этого списка,
    иначе обрабатываются все JSON-файлы в директории. Из данных каждого товара
    пытается извлечь значения по ключам 'parent_category' и 'category_name'.
    Собирает все найденные категории в один список, удаляет дубликаты,
    перемешивает и возвращает.

    Args:
        mining_data_path (Path): Путь к директории с файлами данных.
        crawl_files_list (Optional[List[str]], optional): Список имен файлов
            для обработки. Если None, обрабатываются все .json файлы
            в `mining_data_path`. По умолчанию None.

    Returns:
        List[str]: Перемешанный список уникальных названий категорий.
    """
    # Объявление переменных
    categories_set: Set[str] = set() # Используем set для автоматической дедупликации
    target_files: List[str]
    filename: str
    file_path: Path
    crawl_data: Union[Dict[str, Any], List[Any]]
    products_data: List[Any] = [] # Инициализация
    product_item: Dict[str, Any] # Переименована переменная цикла

    # Определяем список файлов для обработки
    if crawl_files_list is None:
        target_files = get_filenames_from_directory(mining_data_path, 'json') # Ищем json по умолчанию
        logger.debug(f'Обработка категорий из всех json файлов {mining_data_path}')
    else:
        target_files = crawl_files_list
        logger.debug(f'Обработка категорий из файлов списка: {len(target_files)} шт.')

    # Обработка каждого файла
    for filename in target_files:
        try:
            file_path = mining_data_path / filename
            # Загрузка данных
            crawl_data = j_loads(file_path)

            # Извлечение списка товаров
            if isinstance(crawl_data, dict) and 'products' in crawl_data:
                 products_data = crawl_data['products']
            elif isinstance(crawl_data, list):
                 products_data = crawl_data
                 logger.debug(f"Файл {filename} содержит список товаров напрямую (категории).")
            else:
                logger.warning(f"Файл {filename} не содержит ключ 'products' или не является списком (категории). Переход к следующему файлу", None, False)
                continue # Переход к следующему файлу

            # Проверка типа извлеченных товаров
            if not isinstance(products_data, list):
                logger.warning(f"Извлеченные 'products' в файле {filename} не являются списком (категории, тип: {type(products_data)}).", None, False)
                continue # Переход к следующему файлу

            # Извлечение категорий из каждого товара
            for product_item in products_data:
                if not isinstance(product_item, dict):
                     logger.warning(f"Элемент в файле {filename} не является словарем (категории): {product_item}", None, False)
                     continue
                # Пытаемся добавить категории в set, проверяя тип и наличие значения
                parent_category = product_item.get('parent_category')
                category_name = product_item.get('category_name')
                if isinstance(parent_category, str) and parent_category:
                    categories_set.add(parent_category)
                if isinstance(category_name, str) and category_name:
                    categories_set.add(category_name)

        except FileNotFoundError:
             logger.error(f'Файл не найден (категории): {file_path}', None, False)
             continue
        except Exception as ex:
            # Логирование ошибки обработки файла
            logger.error(f'Ошибка при обработке файла {filename=} для извлечения категорий', ex, exc_info=True)
            continue # Используем continue

    # Преобразование set в list и перемешивание
    categories_list: list = list(set(categories_set))
    random.shuffle(categories_list)
    logger.info(f"Собрано {len(categories_list)} уникальных категорий.")
    return categories_list


def fetch_urls_from_all_mining_files(dir_path: Path| List[Path]  = ['random_urls','output_product_data_set1']) -> List[str]: 
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
