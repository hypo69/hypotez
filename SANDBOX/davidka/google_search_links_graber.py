## \file /SANDBOX/davidka/google_search_links_graber.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Скрипт для извлечения ссылок из результатов поиска Google.
===========================================================
Приоритетно использует Google Custom Search JSON API для надежного
получения результатов. Если API-ключ или CSE ID не настроены
в переменных окружения, скрипт переключается на веб-скрапинг
в качестве запасного варианта.

Методы:
1.  **Google Custom Search JSON API (Рекомендуемый):**
    - Требует наличия переменных окружения:
        - `GOOGLE_API_KEY`: Ваш API ключ из Google Cloud Console.
        - `GOOGLE_CSE_ID`: ID вашей Custom Search Engine.
    - Более надежен и соответствует условиям использования Google.
    - Имеет квоты на использование (бесплатные и платные).
2.  **Веб-скрапинг (Запасной вариант):**
    - Используется, если переменные окружения для API не найдены.
    - Менее надежен из-за изменений HTML и мер защиты Google.
    - Может нарушать условия использования Google.

Зависимости:
    - requests (pip install requests)
    - beautifulsoup4 (pip install beautifulsoup4) - для режима скрапинга
    - Наличие модулей logger и printer в проекте hypotez.


Примечание:
Create google custom search api 👉 https://developers.google.com/custom-search/v1/introduction?hl=ru
Google CSE ID 👉 https://programmablesearchengine.google.com/

```rst
.. module:: SANDBOX.davidka.google_search_links_graber
```
"""

import sys
import time
import random
import os 
from pathlib import Path
from typing import Optional, List, Dict, Any
from urllib.parse import urlparse, parse_qs, urlencode

import requests
from bs4 import BeautifulSoup # Нужен только для скрапинга
from bs4.element import Tag # Нужен только для скрапинга


import header
from header import __root__
from src import gs
from src.logger.logger import logger
from src.utils.printer import pprint as print


# --- Конфигурация ---
class Config:
    """
    Класс для хранения конфигурационных параметров.
    """
    # --- Параметры API ---
    # Чтение ключей из переменных окружения
    API_KEY:str = gs.credentials.google_custom_search.onela.api_key or os.getenv('GOOGLE_API_KEY')
    CSE_ID: str = gs.credentials.google_custom_search.onela.cse_id or os.getenv('GOOGLE_CSE_ID')
    # Базовый URL для Google Custom Search API
    API_ENDPOINT: str = 'https://www.googleapis.com/customsearch/v1'

    # --- Параметры Скрапинга (используются только при откате) ---
    # Заголовки для имитации браузера
    SCRAPER_HEADERS: Dict[str, str] = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    # Желаемое количество результатов (Google может игнорировать)
    # Для API 'num' может быть до 10. Для скрапинга оставляем 10.
    NUM_RESULTS: int = 10


# --- Функции API ---
def fetch_search_results_api(query: str, api_key: str, cse_id: str, num_results: int = 10) -> Optional[List[str]]:
    """
    Получает результаты поиска с использованием Google Custom Search JSON API.

    Args:
        query (str): Поисковый запрос.
        api_key (str): API ключ Google Cloud.
        cse_id (str): ID Custom Search Engine.
        num_results (int, optional): Количество запрашиваемых результатов (макс. 10 за раз). По умолчанию 10.

    Returns:
        Optional[List[str]]: Список URL-адресов из результатов поиска или None в случае ошибки.
    """
    # Объявление переменных
    params: Dict[str, Any]
    response: Optional[requests.Response] = None
    results_json: Optional[Dict[str, Any]] = None
    items: Optional[List[Dict[str, Any]]] = None
    links: List[str] = []

    # Параметры запроса к API
    params = {
        'key': api_key,
        'cx': cse_id,
        'q': query,
        'num': min(num_results, 10) # API поддерживает до 10 результатов за запрос
        # 'start': 1 # Можно добавить для пагинации (1, 11, 21, ...)
    }
    logger.debug(f"Запрос к API: {Config.API_ENDPOINT} с параметрами: { {k: v for k, v in params.items() if k != 'key'} }") # Лог без ключа

    try:
        # Выполнение GET-запроса к API
        response = requests.get(Config.API_ENDPOINT, params=params, timeout=15)
        # Проверка на HTTP ошибки
        response.raise_for_status()
        # Парсинг JSON ответа
        results_json = response.json()

        # Проверка на ошибки в ответе API
        if 'error' in results_json:
            error_details = results_json.get('error', {})
            error_message = error_details.get('message', 'Неизвестная ошибка API')
            error_code = error_details.get('code', 'N/A')
            logger.error(f"Ошибка API Google Custom Search: {error_message} (Код: {error_code})", None, False)
            return None

        # Извлечение ссылок из поля 'items'
        items = results_json.get('items')
        if items:
            for item in items:
                link = item.get('link')
                if link:
                    links.append(link)
            logger.info(f"API вернуло {len(links)} ссылок.")
            return links
        else:
            logger.info("API не вернуло результатов (поле 'items' отсутствует или пусто).")
            return [] # Возврат пустой список, если результатов нет

    except requests.exceptions.Timeout as ex:
        logger.error(f'Тайм-аут при запросе к API Google: {Config.API_ENDPOINT}', ex, exc_info=False)
        return None
    except requests.exceptions.HTTPError as ex:
        http_status_code: int = ex.response.status_code if ex.response is not None else 0
        logger.error(f'HTTP ошибка при запросе к API Google: {Config.API_ENDPOINT} (Статус: {http_status_code})', ex, exc_info=False)
        try:
            # Попытка извлечь сообщение об ошибке из тела ответа
            error_content = response.json() if response else {'message': 'Нет тела ответа'}
            logger.error(f"Содержимое ошибки API: {error_content.get('error', error_content)}", None, False)
        except Exception:
            logger.error("Не удалось разобрать тело ошибки API.", None, False)
        return None
    except requests.exceptions.RequestException as ex:
        logger.error(f'Ошибка при выполнении запроса к API Google: {Config.API_ENDPOINT}', ex, exc_info=True)
        return None
    except ValueError as ex: # Ошибка парсинга JSON
         logger.error(f'Ошибка парсинга JSON ответа от API Google: {Config.API_ENDPOINT}', ex, exc_info=True)
         return None
    except Exception as ex:
        logger.error(f'Неожиданная ошибка при работе с API Google: {Config.API_ENDPOINT}', ex, exc_info=True)
        return None


# --- Функции Скрапинга (Запасной вариант) ---
def get_google_search_url_scraper(query: str, num_results: int = 10, lang: str = 'ru') -> str:
    """
    Формирует URL для поискового запроса в Google (для скрапинга).

    Args:
        query (str): Поисковый запрос пользователя.
        num_results (int, optional): Желаемое количество результатов на странице. По умолчанию 10.
        lang (str, optional): Код языка для интерфейса и результатов поиска. По умолчанию 'ru'.

    Returns:
        str: Сформированный URL для Google Search.
    """
    params: Dict[str, Any] = {'q': query, 'num': num_results, 'hl': lang}
    encoded_params: str = urlencode(params)
    search_url: str = f'https://www.google.com/search?{encoded_params}'
    return search_url

def fetch_search_results_scraper(url: str, headers: Dict[str, str]) -> Optional[str]:
    """
    Выполняет HTTP GET запрос для получения HTML (для скрапинга).

    Args:
        url (str): URL страницы Google Search.
        headers (Dict[str, str]): HTTP заголовки для запроса.

    Returns:
        Optional[str]: HTML-содержимое страницы или None в случае ошибки/блокировки.
    """
    html_content: Optional[str] = None
    try:
        response: requests.Response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        html_content = response.text
        if 'CAPTCHA' in html_content or 'Our systems have detected unusual traffic' in html_content:
             logger.warning(f'[Скрапинг] Google заблокировал запрос или требует CAPTCHA для URL: {url}')
             return None
        return html_content
    except requests.exceptions.Timeout as ex:
        logger.error(f'[Скрапинг] Тайм-аут при запросе к URL: {url}', ex, exc_info=False)
        return None
    except requests.exceptions.HTTPError as ex:
        http_status_code: int = ex.response.status_code if ex.response is not None else 0
        logger.error(f'[Скрапинг] HTTP ошибка при запросе к URL: {url} (Статус: {http_status_code})', ex, exc_info=False)
        return None
    except requests.exceptions.RequestException as ex:
        logger.error(f'[Скрапинг] Ошибка при выполнении запроса к URL: {url}', ex, exc_info=True)
        return None
    except Exception as ex:
        logger.error(f'[Скрапинг] Неожиданная ошибка при получении страницы: {url}', ex, exc_info=True)
        return None

def parse_links_scraper(html_content: Optional[str]) -> List[str]:
    """
    Извлекает органические ссылки из HTML (для скрапинга).

    Args:
        html_content (Optional[str]): Строка с HTML-кодом страницы.

    Returns:
        List[str]: Список уникальных URL-адресов.
    """
    links: List[str] = []
    found_urls: set[str] = set()
    if not html_content:
        return links
    soup: BeautifulSoup = BeautifulSoup(html_content, 'html.parser')
    result_blocks: List[Tag] = soup.find_all('div', class_=lambda x: x and isinstance(x, str) and ('g ' in x or x == 'g'))
    if not result_blocks:
        logger.debug("[Скрапинг] Стандартные блоки ('div.g') не найдены. Поиск 'a > h3'.")
        potential_links: List[Tag] = soup.find_all('a')
        result_blocks = [a for a in potential_links if a.find('h3') is not None]

    block: Tag
    for block in result_blocks:
        link_tag: Optional[Tag] = None
        href: Optional[str] = None
        try:
            if block.name == 'a':
                link_tag = block
            else:
                link_tag = block.find('a')
            if link_tag and link_tag.has_attr('href'):
                href = link_tag['href']
                if href.startswith('/url?q='):
                    parsed_url = urlparse(href)
                    query_params = parse_qs(parsed_url.query)
                    actual_url: Optional[str] = query_params.get('q', [None])[0]
                    if actual_url and actual_url.startswith(('http://', 'https://')):
                        found_urls.add(actual_url)
                elif href.startswith(('http://', 'https://')):
                    parsed_href = urlparse(href)
                    if 'google.com' not in parsed_href.netloc:
                        found_urls.add(href)
        except Exception as ex:
            logger.warning(f'[Скрапинг] Ошибка обработки блока или извлечения ссылки из href="{href}"', ex, exc_info=False)
            continue
    links = list(found_urls)
    return links


# --- Точка входа при запуске скрипта ---
if __name__ == '__main__':
    # Объявление переменных
    search_query: str = ''
    extracted_links: Optional[List[str]] = None # Может быть None при ошибке API/скрапинга
    use_api: bool = False # Флаг использования API

    # Проверка наличия ключей API
    if Config.API_KEY and Config.CSE_ID:
        use_api = True
        logger.info("Обнаружены GOOGLE_API_KEY и GOOGLE_CSE_ID. Используется Google Custom Search API.")
    else:
        logger.warning("Переменные окружения GOOGLE_API_KEY и/или GOOGLE_CSE_ID не найдены.")
        logger.warning("Переключение на запасной метод: веб-скрапинг (менее надежный).")
        logger.warning("Для использования рекомендованного метода API установите переменные окружения.")
        use_api = False

    # Получение поискового запроса от пользователя
    search_query = input('Введите поисковый запрос: ')
    logger.info(f"Поиск по запросу: '{search_query}'...")

    # --- Выбор метода и выполнение поиска ---
    if use_api:
        # Использование API
        extracted_links = fetch_search_results_api(
            query=search_query,
            api_key=Config.API_KEY, # type: ignore (проверено выше)
            cse_id=Config.CSE_ID,   # type: ignore (проверено выше)
            num_results=Config.NUM_RESULTS
        )
    else:
        # Использование Скрапинга (запасной вариант)
        scraper_url: str = get_google_search_url_scraper(search_query, Config.NUM_RESULTS)
        logger.info(f'[Скрапинг] URL запроса: {scraper_url}')
        # Пауза перед скрапингом
        sleep_time: float = random.uniform(1.5, 4.0)
        logger.debug(f'[Скрапинг] Пауза перед запросом: {sleep_time:.2f} сек.')
        time.sleep(sleep_time)
        html: Optional[str] = fetch_search_results_scraper(scraper_url, Config.SCRAPER_HEADERS)
        if html:
            extracted_links = parse_links_scraper(html)
        else:
            logger.error('[Скрапинг] Не удалось получить HTML для парсинга.')
            extracted_links = None # Явное указывание на на неудачу

    # --- Вывод результата ---
    if extracted_links is not None: # Проверка, что список не None (ошибки не было)
        if extracted_links:
            # Вывод заголовка
            print('\n--- Найденные ссылки ---')
            # Нумерация и вывод каждой ссылки
            i: int
            link: str
            for i, link in enumerate(extracted_links, 1):
                print(f'{i}. {link}')
        else:
            # Сообщение, если список пуст (но ошибки не было)
            logger.info('Поиск завершен. Ссылки по данному запросу не найдены.')
            print('\n--- Результаты ---')
            print('Ссылки не найдены.')
    else:
        # Сообщение, если произошла ошибка при получении/обработке данных
        logger.error('Поиск завершился с ошибкой. Ссылки не были получены.')
        print('\n--- Ошибка ---')
        print('Не удалось получить результаты поиска. Проверьте логи для деталей.')

    # --- Финальное примечание ---
    # Используется кастомный print
    print('\n--- Важное замечание ---')
    if not use_api:
        print('Использовался метод веб-скрапинга. Он ненадежен и может быть заблокирован.')
        print('Настоятельно рекомендуется настроить Google Custom Search API (см. переменные окружения).')
    else:
         print('Использовался метод Google Custom Search API.')
    print('Помните о квотах и условиях использования Google при работе с API или скрапинге.')
