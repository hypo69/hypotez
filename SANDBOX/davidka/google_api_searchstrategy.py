## \file /SANDBOX/davidka/google_search_links_graber_via_api.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3


# -----------------------------------------------------------------------------------------------
#
#           В этом модуле находятся стратергии поиска. 
#           Реализацию см в experiments/custom_search_google_search_api.py
#
# ------------------------------------------------------------------------------------------------


"""
Скрипт для извлечения ссылок из Google Search с использованием API и различных стратегий.
=========================================================================================
Использует Google Custom Search JSON API для выполнения поиска по заданной категории товаров,
применяя одну из выбранных стратегий для повышения вероятности нахождения ссылок
именно на страницы товаров. Реализован в виде класса GoogleApiSearcher.

Требования:
    - Установленные переменные окружения или конфигурация в gs.credentials:
        - `GOOGLE_API_KEY`: Ваш API ключ из Google Cloud Console.
        - `GOOGLE_CSE_ID`: ID вашей Custom Search Engine.
    - Зависимости: requests
    - Наличие модулей logger и printer в проекте hypotez. Модуль 'gs' также должен быть доступен.

Стратегии поиска:
-----------------
1.  **Стратегия 1: Ключевые слова (Keywords)**
    - Ищет страницы, содержащие категорию и слова, указывающие на намерение
      покупки или нахождение в магазине (купить, заказать, цена, интернет-магазин).
    - Пример запроса: `купить "{CATEGORY_NAME}" онлайн`

2.  **Стратегия 2: Оператор `inurl:`**
    - Ищет страницы, URL которых содержит слова, типичные для страниц
      товаров (product, item, p, dp, good). Считается одной из самых эффективных.
    - Пример запроса: `"{CATEGORY_NAME}" inurl:product`

3.  **Стратегия 3: Оператор `intitle:`**
    - Ищет страницы, заголовок (title) которых содержит категорию и слова,
      характерные для товарных страниц (купить, цена, характеристики).
    - Пример запроса: `intitle:"купить {CATEGORY_NAME}"`

4.  **Стратегия 4: Комбинация операторов (Combined)**
    - Совмещает ключевые слова и операторы (`inurl:`, `intitle:`) для
      повышения специфичности запросов.
    - Пример запроса: `купить "{CATEGORY_NAME}" inurl:product`

5.  **Стратегия 5: Исключения (Exclusions)**
    - Использует оператор `-` для исключения страниц, содержащих слова,
      характерные для нетоварного контента (обзор, блог, форум, категория),
      в сочетании с `inurl:` или ключевыми словами.
    - Пример запроса: `"{CATEGORY_NAME}" inurl:product -обзор -блог`

Принцип работы:
1.  Создается экземпляр класса `GoogleApiSearcher`, который загружает ключи API.
2.  Пользователь вводит категорию и выбирает номер стратегии.
3.  Вызывается соответствующий метод стратегии у экземпляра класса.
4.  Метод генерирует набор поисковых запросов согласно выбранной стратегии.
5.  Для каждого запроса выполняется несколько вызовов API с пагинацией
    (параметр `start`), чтобы собрать достаточное количество результатов.
6.  Все уникальные ссылки из ответов API собираются в единый список.
7.  Результат выводится пользователю.

```rst
.. module:: SANDBOX.davidka.google_search_links_graber_via_api
```
"""

import sys
import time
import os
from pathlib import Path
from typing import Optional, List, Dict, Any, Set, Callable

import requests

# --- Импорты проекта ---
# Предполагается, что эти модули всегда доступны в окружении проекта
import header
from header import __root__
from src import gs

from src.logger.logger import logger
from src.utils.printer import pprint as print
from src.utils.jjson import find_keys
#from SANDBOX.davidka import 


class GoogleApiSearcher:
    """
    Класс для выполнения поиска ссылок через Google Custom Search API с использованием
    различных стратегий.
    """
    # --- Атрибуты Класса (Конфигурация) ---
    API_ENDPOINT: str = 'https://www.googleapis.com/customsearch/v1'
    MAX_RESULTS_PER_PAGE: int = 10
    TARGET_RESULTS_PER_SUBQUERY: int = 20 # Желаемое кол-во на каждый подзапрос
    API_CALL_DELAY: float = 0.5 # Задержка между вызовами API
    API_KEY = gs.credentials.google_custom_search.onela.api_key  # Получить здесь👉 https://developers.google.com/custom-search/v1/introduction
    CSE_ID = gs.credentials.google_custom_search.onela.cse_id  # Создать здесь 👉 https://programmablesearchengine.google.com/about/ 

    def __init__(self, api_key: Optional[str] = None, cse_id: Optional[str] = None):
        """
        Инициализирует экземпляр поисковика.

        Загружает API ключ и CSE ID, отдавая приоритет переданным аргументам,
        затем конфигурации 'gs.credentials', и в последнюю очередь
        переменным окружения.

        Args:
            api_key (Optional[str], optional): API ключ Google. Если None, будет произведена попытка загрузки. По умолчанию None.
            cse_id (Optional[str], optional): ID Custom Search Engine. Если None, будет произведена попытка загрузки. По умолчанию None.

        Raises:
            ValueError: Если не удалось найти API ключ или CSE ID ни одним из способов.
            AttributeError: Если структура 'gs.credentials...' отсутствует или некорректна.
        """


        # 1. Попытка загрузки из gs (без try-except для ImportError)
        # Используем getattr для безопасного доступа к атрибутам, если они могут отсутствовать
        if api_key: self.API_KEY = api_key
        if cse_id: self.CSE_ID = cse_id
        if not self.API_KEY:
            raise ValueError("API_KEY не найден. Убедитесь, что он задан в gs.credentials или в переменных окружения.")

        logger.info(f"GoogleApiSearcher инициализирован. API_KEY: {'***'}, CSE_ID: {'***'}")


    def _fetch_single_api_page(self, query: str, start_index: int) -> Optional[List[str]]:
        """
        Приватный метод: выполняет один вызов API для одной страницы результатов.

        Args:
            query (str): Поисковый запрос.
            start_index (int): Индекс первого результата для этой страницы (1, 11, 21...).

        Returns:
            Optional[List[str]]: Список URL-адресов для этой страницы или None в случае ошибки.
        """
        # Объявление переменных
        params: Dict[str, Any]
        response: Optional[requests.Response] = None
        results_json: Optional[Dict[str, Any]] = None
        items: Optional[List[Dict[str, Any]]] = None
        links: List[str] = []

        # Используем ключи из атрибутов экземпляра
        params = {
            'key': self.API_KEY,
            #'cx': self.CSE_ID,
            'q': query,
            'num': self.MAX_RESULTS_PER_PAGE,
            'start': start_index
        }
        # Логирование параметров без ключа API
        log_params: Dict[str, Any] = {k: v for k, v in params.items() if k != 'key'}
        logger.debug(f"Вызов API: start={start_index}, params={log_params}")

        try:
            # Выполнение GET-запроса
            response = requests.get(self.API_ENDPOINT, params=params, timeout=15)
            # Проверка HTTP-статуса
            response.raise_for_status()
            # Парсинг JSON
            results_json = response.json()

            # Проверка на ошибки бизнес-логики API Google
            if 'error' in results_json:
                error_details: Dict[str, Any] = results_json.get('error', {})
                error_message: str = error_details.get('message', 'Неизвестная ошибка API')
                logger.error(f"Ошибка API Google (start={start_index}): {error_message}", None, False)
                if 'errors' in error_details:
                     logger.error(f"Детали ошибки API: {error_details['errors']}", None, False)
                return None # Возврат None при ошибке API

            # Извлечение ссылок из 'items'
            items = results_json.get('items')
            if items:
                # Обработка каждого элемента результата
                item: Dict[str, Any]
                for item in items:
                    print(f"Заголовок: {item['title']}")
                    print(f"Ссылка: {item['link']}")
                    print(f"Описание: {item.get('snippet', 'Нет описания')}\n")

                    link: Optional[str] = item.get('link')
                    if link:
                        links.append(link)
                logger.debug(f"API (start={start_index}): получено {len(links)} ссылок.")
                return links # Возврат списка ссылок
            else:
                # Результатов на этой странице нет, но ошибки не было
                logger.debug(f"API (start={start_index}): не найдено результатов ('items' отсутствуют).")
                return [] # Возврат пустого списка

        # Обработка исключений при запросе
        except requests.exceptions.Timeout as ex:
            logger.error(f'Тайм-аут при запросе к API (start={start_index})', ex, exc_info=False)
            return None
        except requests.exceptions.HTTPError as ex:
            status_code: int = ex.response.status_code if ex.response is not None else 0
            logger.error(f'HTTP ошибка {status_code} при запросе к API (start={start_index})', ex, exc_info=False)
            return None
        except requests.exceptions.RequestException as ex:
            logger.error(f'Ошибка сети/запроса к API (start={start_index})', ex, exc_info=True)
            return None
        except ValueError as ex: # Ошибка парсинга JSON
             logger.error(f'Ошибка парсинга JSON ответа от API (start={start_index})', ex, exc_info=True)
             return None
        except Exception as ex:
            logger.error(f'Неожиданная ошибка при работе с API (start={start_index})', ex, exc_info=True)
            return None


    def _execute_api_queries(self, queries: List[str], target_total_links: int = 50) -> List[str]:
        """
        Приватный метод: выполняет список поисковых запросов через API с пагинацией.

        Args:
            queries (List[str]): Список поисковых запросов для выполнения.
            target_total_links (int, optional): Примерное общее количество уникальных
                                                 ссылок, которое нужно постараться собрать.
                                                 По умолчанию 50.

        Returns:
            List[str]: Список уникальных URL-адресов, собранных по всем запросам.
        """
        # Множество для хранения уникальных ссылок
        all_found_links: Set[str] = set()
        # Расчет количества страниц API для каждого подзапроса
        pages_per_subquery: int = (self.TARGET_RESULTS_PER_SUBQUERY + self.MAX_RESULTS_PER_PAGE - 1) // self.MAX_RESULTS_PER_PAGE
        # Желаемое количество ссылок с запасом для досрочного выхода
        target_with_buffer: int = int(target_total_links * 1.5)

        logger.info(f"Выполнение {len(queries)} запросов. Цель: ~{target_total_links} ссылок. Запрос {pages_per_subquery} стр. на подзапрос.")

        # Итерация по списку запросов
        query: str
        for query in queries:
            logger.info(f"--- Обработка запроса: '{query}' ---")
            # Итерация по страницам API для текущего запроса
            page_num: int
            for page_num in range(pages_per_subquery):
                start_index: int = page_num * self.MAX_RESULTS_PER_PAGE + 1
                # Вызов метода для получения одной страницы
                page_links: Optional[List[str]] = self._fetch_single_api_page(
                    query=query,
                    start_index=start_index
                )

                # Обработка результата
                if page_links is not None:
                    if page_links: # Список не пустой
                        count_before: int = len(all_found_links)
                        all_found_links.update(page_links) # Добавление во множество (дедупликация)
                        count_after: int = len(all_found_links)
                        added_count: int = count_after - count_before
                        logger.info(f"Запрос '{query}', стр. {page_num + 1}: Найдено {len(page_links)} ссылок. Добавлено {added_count} уник. Всего: {count_after}")
                    else:
                        # API вернул пустой список - больше результатов нет
                        logger.info(f"Запрос '{query}', стр. {page_num + 1}: Больше результатов нет.")
                        break # Прерываем пагинацию для этого запроса

                    # Проверка на достижение цели с буфером
                    if len(all_found_links) >= target_with_buffer:
                         logger.info(f"Собрано достаточно ссылок ({len(all_found_links)} >= {target_with_buffer}). Переход к следующему запросу.")
                         break # Прерываем пагинацию для этого запроса
                else:
                    # Ошибка при получении страницы
                    logger.warning(f"Ошибка при получении стр. {page_num + 1} для запроса '{query}'. Пропуск страницы.")
                    # Можно решить прервать пагинацию для запроса при ошибке: # break

                # Пауза между вызовами API
                time.sleep(self.API_CALL_DELAY)

            logger.info(f"--- Завершение обработки запроса: '{query}' ---")
            # Проверка на достижение цели после завершения всех страниц для запроса
            if len(all_found_links) >= target_with_buffer:
                 logger.info(f"Собрано достаточно ссылок ({len(all_found_links)}). Завершение поиска по всем запросам.")
                 break # Прерываем цикл по всем запросам

        # Преобразование множества в список и возврат
        final_links: List[str] = list(all_found_links)
        logger.info(f"Общий поиск завершен. Собрано {len(final_links)} уникальных ссылок.")
        return final_links

    # --- Публичные Методы для Стратегий ---

    def search_strategy1_keywords(self, category_name: str, target_links: int = 50) -> List[str]:
        """
        Выполняет поиск по Стратегии 1: Ключевые слова.

        Args:
            category_name (str): Название категории для поиска.
            target_links (int, optional): Примерное целевое количество ссылок. По умолчанию 50.

        Returns:
            List[str]: Список уникальных URL-адресов.
        """
        logger.info("Запуск стратегии 1: Ключевые слова")
        queries: List[str] = [
            f'купить "{category_name}" онлайн',
            f'заказать "{category_name}" цена',
            f'"{category_name}" интернет-магазин',
            f'"{category_name}" товары купить',
            f'"{category_name}" стоимость',
        ]
        return self._execute_api_queries(queries, target_links)

    def search_strategy2_inurl(self, category_name: str, target_links: int = 50) -> List[str]:
        """
        Выполняет поиск по Стратегии 2: Оператор `inurl:`.

        Args:
            category_name (str): Название категории для поиска.
            target_links (int, optional): Примерное целевое количество ссылок. По умолчанию 50.

        Returns:
            List[str]: Список уникальных URL-адресов.
        """
        try:
            logger.info("Запуск стратегии 2: Оператор 'inurl:'")
            inurl_patterns: List[str] = ['product', 'item', 'p', 'dp', 'good', 'catalog']
            queries: List[str] = [f'"{category_name}" inurl:{pattern}' for pattern in inurl_patterns]
            return self._execute_api_queries(queries, target_links)
        except Exception as ex:
            logger.error(ex)

    def search_strategy3_intitle(self, category_name: str, target_links: int = 50) -> List[str]:
        """
        Выполняет поиск по Стратегии 3: Оператор `intitle:`.

        Args:
            category_name (str): Название категории для поиска.
            target_links (int, optional): Примерное целевое количество ссылок. По умолчанию 50.

        Returns:
            List[str]: Список уникальных URL-адресов.
        """
        logger.info("Запуск стратегии 3: Оператор 'intitle:'")
        queries: List[str] = [
            f'intitle:"купить {category_name}"',
            f'intitle:"{category_name}" intitle:цена',
            f'intitle:"{category_name}" intitle:характеристики',
            f'intitle:"{category_name}" intitle:заказать',
        ]
        return self._execute_api_queries(queries, target_links)

    def search_strategy4_combined(self, category_name: str, target_links: int = 50) -> List[str]:
        """
        Выполняет поиск по Стратегии 4: Комбинация операторов и ключевых слов.

        Args:
            category_name (str): Название категории для поиска.
            target_links (int, optional): Примерное целевое количество ссылок. По умолчанию 50.

        Returns:
            List[str]: Список уникальных URL-адресов.
        """
        logger.info("Запуск стратегии 4: Комбинация")
        queries: List[str] = [
            f'купить "{category_name}" inurl:product',
            f'"{category_name}" цена inurl:item',
            f'intitle:"{category_name}" inurl:product',
            f'"{category_name}" заказать inurl:p',
            f'"{category_name}" интернет-магазин inurl:catalog',
        ]
        return self._execute_api_queries(queries, target_links)

    def search_strategy5_exclusions(self, category_name: str, target_links: int = 50) -> List[str]:
        """
        Выполняет поиск по Стратегии 5: Исключение нежелательных слов.

        Args:
            category_name (str): Название категории для поиска.
            target_links (int, optional): Примерное целевое количество ссылок. По умолчанию 50.

        Returns:
            List[str]: Список уникальных URL-адресов.
        """
        logger.info("Запуск стратегии 5: Исключения")
        base_queries_inurl: List[str] = [
            f'"{category_name}" inurl:product',
            f'"{category_name}" inurl:item',
            f'"{category_name}" inurl:p',
        ]
        exclusions: str = '-обзор -блог -форум -категория -отзывы -review -blog -forum -category'
        queries: List[str] = [f'{base_query} {exclusions}' for base_query in base_queries_inurl]
        queries.append(f'купить "{category_name}" {exclusions} -inurl:blog')
        return self._execute_api_queries(queries, target_links)


# --- Точка входа при запуске скрипта ---
if __name__ == '__main__':
    # Объявление переменных
    searcher: Optional[GoogleApiSearcher] = None
    category_input: str = ''
    strategy_choice: str = ''
    selected_strategy_method: Optional[Callable[[str, int], List[str]]] = None # Тип для метода экземпляра
    final_result_links: Optional[List[str]] = None
    target_link_count: int = 50 # Желаемое количество ссылок

    # 1. Создание экземпляра поисковика (обработка ошибки инициализации)
    try:
        searcher = GoogleApiSearcher()
    except ValueError as ex:
        print(f"Ошибка инициализации: {ex}")
        sys.exit(1)
    # Добавлена проверка на None после try-except, хотя ValueError должен прервать выполнение
    if searcher is None:
         print("Критическая ошибка: Не удалось создать экземпляр GoogleApiSearcher.")
         sys.exit(1)

    #categories:list = find_keys(DICT?)

    # 2. Получение категории от пользователя
    category_input = input('Введите название категории товаров: ')
    if not category_input:
        print("Ошибка: Название категории не может быть пустым.")
        sys.exit(1)

    # 3. Выбор стратегии
    print("\nДоступные стратегии поиска:")
    print("  1: Ключевые слова (купить, цена, ...)")
    print("  2: Оператор 'inurl:' (product, item, ...)")
    print("  3: Оператор 'intitle:' (купить, цена, ...)")
    print("  4: Комбинация операторов и слов")
    print("  5: Исключение слов (обзор, блог, ...)")

    # Словарь для связи выбора пользователя с методами экземпляра searcher
    strategy_map: Dict[str, Callable[[str, int], List[str]]] = {
        '1': searcher.search_strategy1_keywords,
        '2': searcher.search_strategy2_inurl,
        '3': searcher.search_strategy3_intitle,
        '4': searcher.search_strategy4_combined,
        '5': searcher.search_strategy5_exclusions,
    }

    # Цикл запроса выбора стратегии
    while not selected_strategy_method:
        strategy_choice = input("Выберите номер стратегии (1-5): ")
        selected_strategy_method = strategy_map.get(strategy_choice)
        if not selected_strategy_method:
            print("Неверный ввод. Пожалуйста, введите число от 1 до 5.")

    # 4. Вызов выбранного метода стратегии
    # Передаем аргументы в выбранный метод
    final_result_links = selected_strategy_method(
        category_name=category_input,
        target_links=target_link_count
    )

    # 5. Вывод результата
    if final_result_links is not None: # Проверка, что метод вернул список
        if final_result_links: # Проверка, что список не пустой
            print(f'\n--- Найдено {len(final_result_links)} уникальных ссылок (стратегия {strategy_choice}, цель ~{target_link_count}) ---')
            i: int
            link: str
            for i, link in enumerate(final_result_links, 1):
                print(f'{i}. {link}')
            # Информационные сообщения о количестве
            if len(final_result_links) > target_link_count:
                 print(f"\nПримечание: Получено больше {target_link_count} ссылок для обеспечения полноты.")
            elif len(final_result_links) < target_link_count:
                 print(f"\nПримечание: Найдено меньше {target_link_count} ссылок. Возможно, для данной категории/стратегии больше нет результатов в пределах лимитов API.")
        else:
            # Список пуст, но ошибки во время выполнения не было
            print(f'\n--- Результаты ---')
            print(f'Не найдено ссылок для категории "{category_input}" с использованием стратегии {strategy_choice}.')
    else:
        # Метод вернул None (маловероятно, но возможно при критических ошибках)
        print('\n--- Ошибка ---')
        print('Не удалось получить результаты поиска из-за внутренней ошибки. Проверьте логи.')

    # 6. Финальное примечание
    print('\n--- Важное замечание ---')
    print('Использовался метод Google Custom Search API.')
    print('Точность результатов (ссылки только на товары) не гарантирована на 100%.')
    print('Помните о дневных квотах на использование Google API.')
