## \file /sandbox/davidka/graber.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для сбора данных со страниц товаров с различных сайтов
=====================================================
Использует WebDriver для взаимодействия со страницами через Driver(Firefox)
"""
import asyncio
import requests
from pathlib import Path
import requests
from bs4 import BeautifulSoup, Comment, NavigableString
from urllib.parse import urljoin, urlparse # urlparse используется ниже и в фильтрации
import sys # Для выхода, если URL не найден

import header
from header import __root__
from src import gs
from src.utils.file import read_text_file, save_text_file
from src.webdriver import Driver
from src.webdriver.firefox import Firefox
#from src.webdriver.chrome import Chrome
from src.utils.jjson import j_loads, j_dumps
from SANDBOX.davidka import utils
from src.logger import logger




# Множество запрещенных ключевых слов (пока не используется в логике, но оставлено)
FORBIDDEN_KEYWORDS = {
    'google', 'youtube', 'amazon', 'ebay', 'aliexpress', 'facebook', 'fb',
    'vk', 'twitter',  'instagram', 'linkedin', 'pinterest', 'tiktok',
    'wildberries', 'ozon', 'etsy', 'marketplace', 'wikipedia', 'wikimedia',
    'bestbuy','avito'
    # 't.co',
}

# Множество разрешенных атрибутов для оставляемых тегов
ALLOWED_ATTRIBUTES = {'name', 'id', 'label'}

def is_internal(base_url, link_url):
    """Проверяет, является ли ссылка внутренней по отношению к базовому URL."""
    if not base_url or not link_url: # Добавим проверку на пустые URL
        return False
    try:
        absolute_link_url = urljoin(base_url, link_url)
        base_parts = urlparse(base_url)
        link_parts = urlparse(absolute_link_url)

        # Считаем внутренними только http/https схемы
        if link_parts.scheme not in ('http', 'https'):
            return False
        # Сравниваем только 'сетевое расположение' (домен + порт)
        return base_parts.netloc.lower() == link_parts.netloc.lower()
    except ValueError: # urljoin или urlparse могут вызвать ValueError на некорректных строках
        # print(f"Warning: Could not parse URL: base='{base_url}', link='{link_url}'")
        return False
    except Exception as e: # Ловим другие возможные ошибки парсинга URL
        # print(f"Warning: Error checking internal link (base='{base_url}', link='{link_url}'): {e}")
        return False


def extract_page_data(html_content, base_url):
    """
    Извлекает очищенный HTML и внутренние ссылки со страницы.

    Args:
        base_url (str): Базовый URL страницы для разрешения относительных ссылок.
        html_content (str): HTML-содержимое страницы.

    Returns:
        dict: Словарь с ключами 'text' (строка с очищенным HTML)
              и 'internal_links' (список словарей внутренних ссылок).
              Возвращает {'text': '', 'internal_links': []} в случае ошибки.
    """
    if not html_content:
        return {'text': '', 'internal_links': []}

    try:
        # Используем html5lib для большей надежности с "диким" HTML
        # Если html5lib не установлен (pip install html5lib), можно вернуться к 'html.parser'
        soup = BeautifulSoup(html_content, 'html5lib')
        # soup = BeautifulSoup(html_content, 'html.parser') # Альтернатива

        # --- 1. Предварительная очистка: удаляем ненужные секции и комментарии ---
        # Удаляем теги, которые почти всегда не нужны для контента
        tags_to_remove_completely = ['script', 'style', 'head', 'meta', 'link', 'noscript', 'header', 'footer', 'nav', 'aside', 'form', 'button', 'input', 'textarea', 'select', 'option']
        for tag in soup.find_all(tags_to_remove_completely):
            tag.decompose()

        # Удаляем комментарии
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        # --- 2. Основная логика: оставляем значащие теги и чистим атрибуты ---
        tags_to_evaluate = list(soup.find_all(True)) # Получаем все оставшиеся теги (копируем список)

        for tag in tags_to_evaluate:
            # Пропускаем теги, которые могли быть удалены на предыдущих шагах
            if not tag.parent:
                continue

            # Проверяем "значимость" тега: есть ли внутри непустой текст
            # Используем генератор для текста, чтобы проверить без создания большой строки
            has_significant_text = False
            for text_node in tag.find_all(string=True, recursive=True):
                if isinstance(text_node, NavigableString) and text_node.strip():
                    has_significant_text = True
                    break # Нашли текст, дальше проверять не нужно

            if has_significant_text:
                # Тег значащий: очищаем атрибуты, оставляя только разрешенные
                current_attrs = dict(tag.attrs) # Копируем атрибуты
                new_attrs = {}
                for attr_name, attr_value in current_attrs.items():
                    # Приводим имя атрибута к нижнему регистру для унификации
                    if attr_name.lower() in ALLOWED_ATTRIBUTES:
                        new_attrs[attr_name] = attr_value
                tag.attrs = new_attrs
            else:
                # Тег незначащий (нет текста внутри или только пробелы): удаляем его
                tag.decompose()

        # --- 3. Получаем очищенный HTML ---
        # Часто имеет смысл взять только содержимое body после очистки
        body_content = soup.body
        if body_content:
             # Используем str() для компактного вывода, prettify() для отладки
            body_content_as_string:str = str(body_content)
            # Дополнительно убираем теги <body> и </body> из строки, если они есть
            cleaned_html:str = body_content_as_string
            if cleaned_html.startswith('<body>'):
                cleaned_html = cleaned_html[len('<body>'):]
            if cleaned_html.endswith('</body>'):
                cleaned_html = cleaned_html[:-len('</body>')]
            cleaned_html = cleaned_html.strip().replace('\n','').replace('\t','')# Убираем пробелы по краям
        else:
            cleaned_html = "" # Если body не найден или пуст

        # --- 4. Извлечение внутренних ссылок из *очищенного* дерева ---
        internal_links = []
        # Ищем ссылки в модифицированном 'soup', т.к. body_content - это строка
        body:str = soup.body
        if len(body)>0: # Искать только если body существует
            all_links = soup.body.find_all('a', href=True)
            for link in all_links:
                href = link.get('href')
                # Получаем текст ссылки как он есть в очищенном HTML
                text = link.get_text(strip=True) or "Ссылка без текста"

                if href:
                    # Проверяем, является ли ссылка внутренней
                    if is_internal(base_url, href):
                        absolute_href = urljoin(base_url, href)

                        # >>> Место для  проверки FORBIDDEN_KEYWORDS <<<
                        # Если нужно фильтровать ссылки по доменам из FORBIDDEN_KEYWORDS:
                        # link_parts = urlparse(absolute_href)
                        # domain = link_parts.netloc.lower()
                        # is_forbidden = False
                        # for keyword in FORBIDDEN_KEYWORDS:
                        #     if keyword in domain:
                        #         is_forbidden = True
                        #         break
                        # if not is_forbidden:
                        #     link_data = {"link": {"href": absolute_href, "text": text}}
                        #     internal_links.append(link_data)
                        # else: # Если проверка не нужна:
                        link_data = {"link": {"href": absolute_href, "text": text}}
                        internal_links.append(link_data)

            return {'text': cleaned_html, 'internal_links': internal_links}

    except Exception as ex:
        # Логируем ошибку для отладки
        import traceback
        print(f"Ошибка при обработке HTML для {base_url}: {ex}")
        print(traceback.format_exc()) # Печатаем traceback для деталей
        
    return {'text': '', 'internal_links': []} # Возвращаем пустую структуру


def update_output_dict(data:str, timestamp:str, url:str) -> bool:
    output_file = Path(rf"F:/llm/filtered_urls/{gs.now}.json")
    data_dict:dict = {'url':url, 'data':data}
    if not j_dumps(data_dict,output_file):
        logger.error(f"Ошибка записи в файл {output_file}")
        return False

    logger.success(f'Файл {output_file} - Записан!')
    utils.update_checked_urls_file(url)
    return True


# --- Основной блок выполнения ---
if __name__ == "__main__":
    driver = Driver(Firefox, window_mode = 'headless')
    timestamp: str = gs.now
    actual_urls: list = []
    

    # 1. Получаем список URL 
    try:
        checked_urls:list = read_text_file(Path(rf"F:/llm/filtered_urls/checked_urls.txt"), as_list=True)
        fetched_urls_list:list = utils.fetch_urls_from_all_mining_files(['random_urls','output_product_data_set1']) 
        actual_urls:list = list(set(fetched_urls_list) - set (checked_urls))  

    except Exception as ex:
        print(f"Ошибка при получении списка URL: ",ex)
        actual_urls = [] # Пустой список в случае ошибки

    
    # 2. Ищем ПЕРВЫЙ подходящий URL с учетом ФИЛЬТРАЦИИ
    target_url = None

    print("Поиск первого подходящего URL с фильтрацией...")


    for url in actual_urls:

        url = url.strip()

        # Шаг 2.1: Исходная проверка на 'http'
        if not url.startswith('http'):
            continue

        # Шаг 2.2: ДОПОЛНИТЕЛЬНАЯ ПРОВЕРКА (Фильтрация)
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()

            if not domain: # Пропускаем URL без домена
                continue

            is_forbidden = False
            for keyword in FORBIDDEN_KEYWORDS:
                if keyword in domain:
                    is_forbidden = True
                    print(f"--- Фильтр: URL '{url}' пропущен (содержит '{keyword}')")
                    break # Нашли запрещенное слово, переходим к следующему URL в списке

            # Если URL запрещен (is_forbidden == True), пропускаем его
            if is_forbidden:
                continue

            # Шаг 2.3: Если URL прошел все проверки (http и не запрещен) - выбираем его
            target_url = url
            #print(f"+++ Найден подходящий URL: {target_url}")
           
        except Exception as e:
            print(f"Ошибка парсинга или проверки URL '{url}': {e}")
            continue # Пропускаем URL при ошибке обработки

        # --- Конец цикла поиска target_url ---

        # 3. Проверяем, найден ли URL, и продолжаем как в вашем коде
        if not target_url:
            print("\nПодходящий URL не найден в списке после применения фильтров.")
            ...
            raise

        # 4. Создаем драйвер 
        
        try:

            # driver.get_url(target_url) # Если используете get_url
            if not driver.fetch_html(target_url):
                logger.critical(f"Ошибка получения HTML для {target_url} \n Необходимо как - то обработать эту ошибку", None, True)
                ...
            #print("HTML страницы получен.")

            # 6. Извлекаем данные (как в вашем коде, передавая target_url)
            print("Извлечение данных...")
            data = extract_page_data(driver.html_content, target_url) # Передаем target_url
            print("Извлечение данных завершено.")

            # 7. Вывод результатов (как в вашем коде)
            if data:
                update_output_dict(data, timestamp, target_url)
            else:
                logger.error("\nНе удалось извлечь данные со страницы (extract_page_data не вернул результат).", None, False)

        except Exception as ex:
            print(f"\nПроизошла ошибка во время работы WebDriver или обработки данных: ", ex)



