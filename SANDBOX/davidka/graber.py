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
from bs4 import BeautifulSoup, Comment
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




FORBIDDEN_KEYWORDS = {
    'google', 'youtube', 'amazon', 'ebay', 'aliexpress', 'facebook', 'fb',
    'vk', 'twitter',  'instagram', 'linkedin', 'pinterest', 'tiktok',
    'wildberries', 'ozon', 'etsy', 'marketplace', 'wikipedia', 'wikimedia' 
    # Добавьте другие ключевые слова или домены по необходимости
    # 't.co',
}



def is_internal(base_url, link_url):
    """Проверяет, является ли ссылка внутренней по отношению к базовому URL."""
    try:
        absolute_link_url = urljoin(base_url, link_url)
        base_parts = urlparse(base_url)
        link_parts = urlparse(absolute_link_url)
        if link_parts.scheme not in ('http', 'https'):
            return False
        return base_parts.netloc == link_parts.netloc
    except Exception:
        return False

def extract_page_data(base_url, html_content): # Убедитесь, что base_url передается
    """
    Извлекает основной текст и внутренние ссылки со страницы.
    (Код функции остается как в вашем примере)
    """
    if not html_content:
        return {'text': '', 'internal_links': []}

    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # --- 1. Извлечение текста (как в вашем коде) ---
        tags_to_remove = ['script', 'style', 'head', 'meta', 'link', 'noscript', 'nav', 'footer', 'header', 'aside']
        for tag in soup.find_all(tags_to_remove):
            tag.decompose()
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()
        page_text = soup.get_text(separator=' ', strip=True)
        page_text = ' '.join(page_text.split())

        # --- 2. Извлечение внутренних ссылок (как в вашем коде, используя base_url) ---
        internal_links = []
        all_links = soup.find_all('a', href=True)
        for link in all_links:
            href = link.get('href')
            text = link.get_text(strip=True) or "Ссылка без текста"
            if href:
                # Используем переданный base_url для проверки и разрешения ссылок
                if is_internal(base_url, href):
                    absolute_href = urljoin(base_url, href)
                    link_data = {"link": {"href": absolute_href, "text": text}}
                    internal_links.append(link_data)

        return {'text': page_text, 'internal_links': internal_links}
    except Exception as e:
        print(f"Ошибка при разборе HTML для {base_url}: {e}")
        return {'text': '', 'internal_links': []}

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
    driver = Driver(Firefox, window_mode= 'headless')
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
            data = extract_page_data(target_url, driver.html_content) # Передаем target_url
            print("Извлечение данных завершено.")

            # 7. Вывод результатов (как в вашем коде)
            if data:
                update_output_dict(data, timestamp, target_url)
            else:
                logger.error("\nНе удалось извлечь данные со страницы (extract_page_data не вернул результат).", None, False)

        except Exception as ex:
            print(f"\nПроизошла ошибка во время работы WebDriver или обработки данных: ", ex)



