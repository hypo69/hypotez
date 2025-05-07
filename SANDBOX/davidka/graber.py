## \file /sandbox/davidka/graber.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для сбора данных со страниц товаров с различных сайтов
=====================================================
Использует WebDriver для взаимодействия со страницами через Driver(Firefox)
"""
import re
from pathlib import Path
from bs4 import BeautifulSoup, Comment, NavigableString
from urllib.parse import urljoin, urlparse
import sys 
import random 

import header 
from header import __root__
from src import gs 
from src.utils.file import read_text_file
from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox
from src.utils.jjson import j_loads, j_dumps
from SANDBOX.davidka import utils 
from src.logger import logger

ALLOWED_ATTRIBUTES = [
    'href', 'src', 'alt', 'title', 'id', 'lang', 'name', 
    'data-*', 
    'class', 
]

FORBIDDEN_KEYWORDS = [
    "google.", "facebook.", "twitter.", "youtube.", "instagram.", "linkedin.",
    "pinterest.", "amazon.", "aliexpress.", "ebay.", "wikipedia.org", "vk.com",
    "ok.ru", "yandex.ru", "mail.ru", "livejournal.com", "blogspot.com", "wordpress.com",
    "microsoft.com", "apple.com", "adobe.com", "archive.org", "wa.me", "t.me", "tel:",
    "mailto:", "skype:", "javascript:", "data:", "ftp:", "file:", "android-app:", "ios-app:",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp",
    ".zip", ".rar", ".tar.gz", ".7z", ".exe", ".msi", ".dmg",
    ".mp3", ".wav", ".ogg", ".mp4", ".avi", ".mov", ".wmv", ".mkv",
    ".css", ".js"
]


def is_internal(base_url_str: str, link_url_str: str) -> bool:
    if not base_url_str or not link_url_str: return False
    try:
        base_url_parsed = urlparse(base_url_str)
        resolved_link_url_str = urljoin(base_url_str, link_url_str.strip())
        link_url_parsed = urlparse(resolved_link_url_str)
        if link_url_parsed.scheme not in ('http', 'https'): return False
        if not link_url_parsed.netloc: return False
        if base_url_parsed.netloc.lower() == link_url_parsed.netloc.lower():
            if base_url_parsed.path == link_url_parsed.path and link_url_parsed.fragment and not link_url_parsed.query:
                return False 
            return True
        return False
    except ValueError: 
        logger.debug(f"Ошибка парсинга URL при проверке is_internal: base='{base_url_str}', link='{link_url_str}'")
        return False


def extract_page_data(html_content: str, base_url: str) -> dict:
    global ALLOWED_ATTRIBUTES

    cleaned_html_output = ''
    plain_text_output = ''
    internal_links_output = []
    title_tag_content_output = ''
    meta_description_output = ''
    meta_keywords_output = ''
    meta_name_title_output = ''
    meta_og_title_output = ''

    empty_result_template = {
        'html': cleaned_html_output, 'text': plain_text_output, 
        'internal_links': internal_links_output, 'title_tag_content': title_tag_content_output,
        'meta_description': meta_description_output, 'meta_keywords': meta_keywords_output, 
        'meta_name_title': meta_name_title_output, 'meta_og_title': meta_og_title_output
    }

    if not html_content:
        logger.warning(f"HTML контент для {base_url} пуст.")
        return empty_result_template

    try:
        soup = BeautifulSoup(html_content, 'html5lib')

        title_tag = soup.find('title')
        if title_tag: title_tag_content_output = title_tag.get_text(strip=True)
        
        meta_desc_tag = soup.find('meta', attrs={'name': re.compile(r'^description$', re.I)})
        if meta_desc_tag and meta_desc_tag.get('content'): meta_description_output = meta_desc_tag['content'].strip()

        meta_keywords_tag = soup.find('meta', attrs={'name': re.compile(r'^keywords$', re.I)})
        if meta_keywords_tag and meta_keywords_tag.get('content'): meta_keywords_output = meta_keywords_tag['content'].strip()
        
        meta_name_title_tag = soup.find('meta', attrs={'name': re.compile(r'^title$', re.I)})
        if meta_name_title_tag and meta_name_title_tag.get('content'): meta_name_title_output = meta_name_title_tag['content'].strip()

        meta_og_title_tag = soup.find('meta', attrs={'property': 'og:title'})
        if meta_og_title_tag and meta_og_title_tag.get('content'): meta_og_title_output = meta_og_title_tag['content'].strip()

        tags_to_remove_completely_initial = [ # Теги, удаляемые до сбора ссылок
            'script', 'style', 'head', 'meta', 'link', 'noscript', 
            'iframe', 'embed', 'object', 'applet', 'audio', 'video',
            'svg', 'canvas', 'map', 'area', 'dialog', 'figure', 'figcaption', 'details', 'summary',
            # Пока не удаляем header, footer, nav, aside, form, button, input, textarea, select, option
            # чтобы ссылки из них могли быть собраны, если они важны
        ]
        for tag_name_to_remove in tags_to_remove_completely_initial:
            for tag_object in soup.find_all(tag_name_to_remove):
                tag_object.decompose()

        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()
            
        # --- ШАГ A: СБОР ВНУТРЕННИХ ССЫЛОК ---
        # Ссылки собираются до основного этапа очистки атрибутов и удаления тегов <a>
        # Но после удаления script, style и т.д.
        search_scope_for_links_initial = soup.body if soup.body else soup
        if search_scope_for_links_initial:
            all_a_tags_for_collection = search_scope_for_links_initial.find_all('a', href=True)
            unique_links_hrefs = set() 
            for link_tag_collect in all_a_tags_for_collection:
                href_value_collect = link_tag_collect.get('href')
                # Абсолютизируем href для проверки is_internal и для сохранения
                if href_value_collect:
                    try:
                        abs_href_collect = urljoin(base_url, href_value_collect.strip())
                        parsed_abs_href_collect = urlparse(abs_href_collect)
                        if parsed_abs_href_collect.scheme not in ('http', 'https'):
                            continue # Пропускаем не HTTP/HTTPS ссылки
                    except ValueError:
                        continue # Пропускаем, если URL не может быть обработан urljoin/urlparse
                else:
                    continue # Пропускаем теги <a> без href

                text_content_of_link_collect = link_tag_collect.get_text(separator=' ', strip=True)
                
                if abs_href_collect and text_content_of_link_collect: 
                    if is_internal(base_url, abs_href_collect): # Проверяем абсолютизированный URL
                        if abs_href_collect not in unique_links_hrefs:
                            internal_links_output.append({"link": {"href": abs_href_collect, "text": text_content_of_link_collect}})
                            unique_links_hrefs.add(abs_href_collect)
        
        # --- ШАГ B: ОСНОВНАЯ ОЧИСТКА HTML (ТЕПЕРЬ МОЖНО УДАЛЯТЬ <a> И ДРУГИЕ) ---
        # Добавляем теги, которые могли содержать ссылки, но теперь не нужны в cleaned_html
        tags_to_remove_after_link_collection = [
             'header', 'footer', 'nav', 'aside', 
             'form', 'button', 'input', 'textarea', 'select', 'option',
             'a' # <--- Удаляем все теги <a>
        ]
        for tag_name_to_remove in tags_to_remove_after_link_collection:
            for tag_object in soup.find_all(tag_name_to_remove):
                tag_object.decompose()


        # --- 2. Очистка атрибутов у ОСТАВШИХСЯ тегов ---
        # (теги <a> уже удалены, так что их атрибуты не будут обрабатываться здесь)
        for tag in list(soup.find_all(True)): 
            if not tag.name or not tag.parent: continue
            
            is_meaningful_media = tag.name == 'img' and (tag.get('src') or tag.get('alt'))
            # is_link_with_href больше не актуален, так как теги <a> удалены
            
            has_significant_content = False
            if is_meaningful_media: # img сохраняем, если есть src/alt
                has_significant_content = True
            elif tag.get_text(strip=True): # Любой другой тег сохраняем, если в нем есть текст
                has_significant_content = True
            
            if has_significant_content:
                current_attrs = dict(tag.attrs) 
                new_attrs = {}
                for attr_name, attr_value in current_attrs.items():
                    attr_name_lower = attr_name.lower()
                    
                    allowed_by_list = attr_name_lower in ALLOWED_ATTRIBUTES
                    allowed_by_data_pattern = False
                    if not allowed_by_list:
                        allowed_by_data_pattern = any(
                            allowed_pattern == 'data-*' and attr_name_lower.startswith('data-')
                            for allowed_pattern in ALLOWED_ATTRIBUTES
                        )
                    
                    if allowed_by_list or allowed_by_data_pattern:
                        val_to_process = ""
                        if isinstance(attr_value, list):
                            if attr_value and isinstance(attr_value[0], str):
                                val_to_process = attr_value[0].strip()
                        elif isinstance(attr_value, str):
                            val_to_process = attr_value.strip()
                        else: continue

                        if not val_to_process and attr_name_lower not in ('alt'): continue
                        
                        # href здесь обрабатывать не нужно, т.к. <a> удалены
                        if attr_name_lower == 'src' and tag.name == 'img':
                            if not val_to_process.startswith(('data:')):
                                try: 
                                    abs_url = urljoin(base_url, val_to_process)
                                    parsed_abs_url = urlparse(abs_url)
                                    if parsed_abs_url.scheme in ('http', 'https'): new_attrs[attr_name] = abs_url
                                    else: logger.debug(f"Пропущен src с невалидной схемой: '{abs_url}' для {base_url}")
                                except ValueError: logger.debug(f"Не удалось обработать src '{val_to_process}' для {base_url}")
                        elif allowed_by_data_pattern: new_attrs[attr_name] = attr_value 
                        else: new_attrs[attr_name] = val_to_process 
                tag.attrs = new_attrs
            else: 
                if tag.name not in ('body', 'html', 'br'): 
                    tag.decompose()

        # --- 3. Получаем очищенный HTML из body и извлекаем из него текст ---
        body_tag = soup.body
        if body_tag:
            # Финальная очистка пустых тегов (кроме img, br)
            for tag_to_clean in list(body_tag.find_all(True)): 
                if tag_to_clean.name not in ('img', 'br') and not tag_to_clean.attrs and not tag_to_clean.contents and not tag_to_clean.get_text(strip=True): 
                    if tag_to_clean.name != 'body': tag_to_clean.decompose()
            
            cleaned_html_output = "".join(str(c) for c in body_tag.contents).strip()
            cleaned_html_output = cleaned_html_output.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
            cleaned_html_output = re.sub(r'\s{2,}', ' ', cleaned_html_output).strip()
            
            if cleaned_html_output:
                # Для извлечения текста из HTML, который уже НЕ СОДЕРЖИТ <a>
                temp_soup_for_text = BeautifulSoup(cleaned_html_output, 'html5lib')
                for br_tag in temp_soup_for_text.find_all("br"): br_tag.replace_with("\n")
                # Блочные теги, оставшиеся после всех чисток
                block_tags_for_text_formatting = ['p', 'div', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'table', 'tr', 'section', 'article', 'main', 'address']
                for block_tag_name in block_tags_for_text_formatting:
                    for bt in temp_soup_for_text.find_all(block_tag_name):
                        bt.append("\n") 

                plain_text_output = temp_soup_for_text.get_text(separator=' ', strip=False) 
                plain_text_output = re.sub(r'[ \t]*\n[ \t\n]*', '\n', plain_text_output) 
                plain_text_output = re.sub(r'\s{2,}', ' ', plain_text_output).strip()
        
        if not plain_text_output.strip(): 
            logger.info(f"Извлеченный ТЕКСТ (без тегов) для {base_url} оказался пустым после очистки.")
        
        return {
            'html': cleaned_html_output,
            'text': plain_text_output,
            'title_tag_content': title_tag_content_output,
            'meta_description': meta_description_output,
            'meta_keywords': meta_keywords_output,
            'meta_name_title': meta_name_title_output,
            'meta_og_title': meta_og_title_output,
            'internal_links': internal_links_output,
        }   

    except Exception as e:
        import traceback
        logger.error(f"Критическая ошибка при обработке HTML для {base_url}: {e}\n{traceback.format_exc()}")
        return {
            'html': cleaned_html_output, 'text': plain_text_output, 
            'internal_links': internal_links_output, 'title_tag_content': title_tag_content_output,
            'meta_description': meta_description_output, 'meta_keywords': meta_keywords_output, 
            'meta_name_title': meta_name_title_output, 'meta_og_title': meta_og_title_output
        }


def update_output_dict(data_dict: dict, timestamp:str, url:str) -> bool:
    try:
        parsed_url = urlparse(url)
        domain_name = parsed_url.netloc.replace('.', '_') 
        if not domain_name: domain_name = "unknown_domain"
    except Exception: domain_name = "parse_error_domain"

    date_str = timestamp.split('_')[0] if '_' in timestamp else timestamp
    date_folder = Path(rf"F:/llm/filtered_urls/{date_str}") 
    domain_folder = date_folder / domain_name
    domain_folder.mkdir(parents=True, exist_ok=True) 

    path_part = (parsed_url.path + parsed_url.query).strip('/') 
    safe_url_part = re.sub(r'[^a-zA-Z0-9_-]', '_', path_part)[:100] 
    if not safe_url_part: safe_url_part = "index"
    
    output_file_name = f"{timestamp}_{safe_url_part}.json"
    output_file = domain_folder / output_file_name
    
    data_dict_to_save = {'url': url, **data_dict} 

    if not j_dumps(data_dict_to_save, output_file, indent=4): 
        logger.error(f"Ошибка записи в файл {output_file}")
        return False

    logger.success(f'Файл {output_file} - Записан!')
    utils.update_checked_urls_file(url) 
    return True


# --- Основной блок выполнения ---
if __name__ == "__main__":
    driver = None 
    urls_successfully_processed_count = 0
    try:
        driver = Driver(Firefox, window_mode='headless')
        
        checked_urls_path = Path(rf"F:/llm/filtered_urls/checked_urls.txt")
        checked_urls: list = []
        try:
            if checked_urls_path.exists():
                 checked_urls = read_text_file(checked_urls_path, as_list=True)
            else:
                logger.info(f"Файл {checked_urls_path} не найден, будет создан новый.")
        except Exception as e:
            logger.warning(f"Не удалось прочитать файл checked_urls.txt: {e}. Список проверенных URL будет пуст.")

        fetched_urls_list: list = []
        try:
            fetched_urls_list = utils.fetch_urls_from_all_mining_files(
                ['source_urls_1.txt', 'source_urls_2.txt'] # Пример имен
            ) 
        except Exception as e:
            logger.error(f"Ошибка при получении списка URL из mining_files: {e}")

        cleaned_fetched_urls = {u.strip() for u in fetched_urls_list if u and u.strip()}
        cleaned_checked_urls = {u.strip() for u in checked_urls if u and u.strip()}
        actual_urls: list = list(cleaned_fetched_urls - cleaned_checked_urls)
        random.shuffle(actual_urls)

        if not actual_urls:
            logger.info("Нет новых URL для обработки.")
            sys.exit(0)

        logger.info(f"Найдено {len(actual_urls)} новых URL для обработки.")
        
        max_urls_to_process_per_run = 100 

        for current_url in actual_urls:
            if urls_successfully_processed_count >= max_urls_to_process_per_run:
                logger.info(f"Достигнут лимит обработки ({max_urls_to_process_per_run} URL) за этот запуск.")
                break

            logger.info(f"Обработка URL: {current_url}")

            if not current_url.startswith(('http://', 'https://')):
                logger.warning(f"URL '{current_url}' пропущен (не начинается с http:// или https://).")
                utils.update_checked_urls_file(current_url) 
                continue

            try:
                parsed_url_check = urlparse(current_url)
                domain_check = parsed_url_check.netloc.lower()

                if not domain_check:
                    logger.warning(f"URL '{current_url}' пропущен (не удалось определить домен).")
                    utils.update_checked_urls_file(current_url)
                    continue

                is_forbidden = False
                for keyword in FORBIDDEN_KEYWORDS:
                    if keyword in current_url.lower():
                        is_forbidden = True
                        logger.info(f"Фильтр: URL '{current_url}' пропущен (содержит запрещенное слово/паттерн '{keyword}').")
                        break
                if is_forbidden:
                    utils.update_checked_urls_file(current_url)
                    continue

            except Exception as e: 
                logger.error(f"Ошибка анализа URL '{current_url}': {e}")
                utils.update_checked_urls_file(current_url)
                continue

            if not driver.fetch_html(current_url): 
                logger.error(f"Не удалось получить HTML для {current_url}")
                utils.update_checked_urls_file(current_url)
                continue
            
            if not driver.html_content: 
                logger.error(f"HTML контент для {current_url} пуст после fetch_html.")
                utils.update_checked_urls_file(current_url)
                continue

            logger.info(f"Извлечение данных для {current_url}...")
            
            file_timestamp = gs.now_До_секунд() if hasattr(gs, 'now_До_секунд') else gs.now()

            page_data_dict = extract_page_data(driver.html_content, current_url)
            
            if page_data_dict and page_data_dict.get('text', '').strip():
                logger.success(f"Данные для {current_url} успешно извлечены (текст не пуст).")
                if update_output_dict(page_data_dict, file_timestamp, current_url): 
                    urls_successfully_processed_count += 1
            else:
                logger.warning(f"Не удалось извлечь значимые данные (текст без тегов пуст или ошибка) для {current_url}.")
                utils.update_checked_urls_file(current_url)

    except KeyboardInterrupt:
        logger.warning("Обработка прервана пользователем (KeyboardInterrupt).")
    except Exception as ex_main:
        logger.critical(f"Критическая ошибка в основном блоке выполнения: {ex_main}", exc_info=True)
    finally:
        if driver:
            logger.info("Завершение работы драйвера...")
            driver.quit()
        logger.info(f"Скрипт {Path(__file__).name} завершил работу. Успешно обработано URL: {urls_successfully_processed_count}.")