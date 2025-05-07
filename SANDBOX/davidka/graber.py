## \file /sandbox/davidka/graber.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для сбора данных со страниц товаров с различных сайтов
=====================================================
Использует WebDriver для взаимодействия со страницами через Driver(Firefox)

```rst
 .. module:: sandbox.davidka.graber
```
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

# Список разрешенных HTML атрибутов для сохранения в очищенном HTML.
# Атрибуты, не входящие в этот список, будут удалены, за исключением data-* атрибутов.
ALLOWED_ATTRIBUTES: list[str] = [
    'href', 'src', 'alt', 'title', 'id', 'lang', 'name', 
    'data-*', # Позволяет сохранять все атрибуты, начинающиеся с 'data-'
    'class', 
]

# Список ключевых слов и паттернов, указывающих на нежелательные URL.
# URL, содержащие любое из этих слов/паттернов, будут отфильтрованы и не будут обрабатываться.
FORBIDDEN_KEYWORDS: list[str] = [
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
    """
    Проверяет, является ли `link_url_str` внутренней ссылкой относительно `base_url_str`.

    Args:
        base_url_str (str): Базовый URL текущей страницы.
        link_url_str (str): URL ссылки для проверки.

    Returns:
        bool: `True`, если ссылка внутренняя, иначе `False`.

    Example:
        >>> is_internal('http://example.com/path/', '/page.html')
        True
        >>> is_internal('http://example.com/path/', 'http://othersite.com')
        False
        >>> is_internal('http://example.com/path/', '#anchor')
        False
    """
    # Проверка на пустые входные строки
    if not base_url_str or not link_url_str: return False
    try:
        # Парсинг базового URL
        base_url_parsed: urlparse = urlparse(base_url_str)
        # Построение абсолютного URL из базового и относительной ссылки
        resolved_link_url_str: str = urljoin(base_url_str, link_url_str.strip())
        # Парсинг абсолютизированного URL ссылки
        link_url_parsed: urlparse = urlparse(resolved_link_url_str)
        
        # Проверка схемы URL ссылки (должна быть http или https)
        if link_url_parsed.scheme not in ('http', 'https'): return False
        # Проверка наличия сетевой локации (домена) в URL ссылки
        if not link_url_parsed.netloc: return False
        
        # Сравнение сетевых локаций (доменов) базового URL и URL ссылки
        if base_url_parsed.netloc.lower() == link_url_parsed.netloc.lower():
            # Если ссылка является якорной ссылкой на той же странице (только fragment, без query),
            # она не считается внутренней в контексте навигации на новую страницу.
            if base_url_parsed.path == link_url_parsed.path and link_url_parsed.fragment and not link_url_parsed.query:
                return False 
            return True # Ссылка внутренняя
        return False # Ссылка внешняя
    except ValueError: 
        # Логирование ошибки при невозможности парсинга URL
        logger.debug(f"Ошибка парсинга URL при проверке is_internal: base='{base_url_str}', link='{link_url_str}'")
        return False


def extract_page_data(html_content: str, base_url: str) -> dict:
    """
    Извлекает структурированные данные из HTML-контента страницы.
    Функция очищает HTML, извлекает текстовое содержимое, внутренние ссылки и метаданные.

    Args:
        html_content (str): Строка с HTML-содержимым страницы.
        base_url (str): Базовый URL страницы, используется для разрешения относительных ссылок.

    Returns:
        dict: Словарь с извлеченными данными, включающий:
            'html' (str): Очищенный HTML-код (из тега body).
            'text' (str): Извлеченный текст без тегов.
            'internal_links' (list): Список словарей внутренних ссылок ({"link": {"href": "...", "text": "..."}}).
            'title_tag_content' (str): Содержимое тега <title>.
            'meta_description' (str): Содержимое мета-тега description.
            'meta_keywords' (str): Содержимое мета-тега keywords.
            'meta_name_title' (str): Содержимое мета-тега name="title".
            'meta_og_title' (str): Содержимое мета-тега property="og:title".

    Example:
        >>> html = "<html><head><title>Test</title></head><body><p>Hello</p><a href='/page'>Link</a></body></html>"
        >>> data = extract_page_data(html, 'http://example.com')
        >>> print(data['title_tag_content'])
        Test
        >>> print(data['text'])
        Hello
    """
    # Примечание: 'global ALLOWED_ATTRIBUTES' здесь не изменяет переменную, а лишь указывает на её использование.
    # В Python для чтения глобальных переменных 'global' не требуется.
    global ALLOWED_ATTRIBUTES

    # Инициализация переменных для хранения результатов
    cleaned_html_output: str = ''
    plain_text_output: str = ''
    internal_links_output: list = []
    title_tag_content_output: str = ''
    meta_description_output: str = ''
    meta_keywords_output: str = ''
    meta_name_title_output: str = ''
    meta_og_title_output: str = ''

    # Шаблон для возврата пустого результата в случае ошибки или отсутствия контента
    empty_result_template: dict = {
        'html': cleaned_html_output, 'text': plain_text_output, 
        'internal_links': internal_links_output, 'title_tag_content': title_tag_content_output,
        'meta_description': meta_description_output, 'meta_keywords': meta_keywords_output, 
        'meta_name_title': meta_name_title_output, 'meta_og_title': meta_og_title_output
    }

    # Проверка на пустой HTML контент
    if not html_content:
        logger.warning(f"HTML контент для {base_url} пуст.")
        return empty_result_template

    try:
        # Парсинг HTML с использованием html5lib для лучшей обработки "грязного" HTML
        soup: BeautifulSoup = BeautifulSoup(html_content, 'html5lib')

        # Извлечение содержимого тега <title>
        title_tag: NavigableString | None = soup.find('title')
        if title_tag: title_tag_content_output = title_tag.get_text(strip=True)
        
        # Извлечение содержимого мета-тега description
        meta_desc_tag: NavigableString | None = soup.find('meta', attrs={'name': re.compile(r'^description$', re.I)})
        if meta_desc_tag and meta_desc_tag.get('content'): meta_description_output = meta_desc_tag['content'].strip()

        # Извлечение содержимого мета-тега keywords
        meta_keywords_tag: NavigableString | None = soup.find('meta', attrs={'name': re.compile(r'^keywords$', re.I)})
        if meta_keywords_tag and meta_keywords_tag.get('content'): meta_keywords_output = meta_keywords_tag['content'].strip()
        
        # Извлечение содержимого мета-тега name="title"
        meta_name_title_tag: NavigableString | None = soup.find('meta', attrs={'name': re.compile(r'^title$', re.I)})
        if meta_name_title_tag and meta_name_title_tag.get('content'): meta_name_title_output = meta_name_title_tag['content'].strip()

        # Извлечение содержимого мета-тега property="og:title"
        meta_og_title_tag: NavigableString | None = soup.find('meta', attrs={'property': 'og:title'})
        if meta_og_title_tag and meta_og_title_tag.get('content'): meta_og_title_output = meta_og_title_tag['content'].strip()

        # Теги, которые удаляются полностью перед сбором ссылок и основной очисткой
        tags_to_remove_completely_initial: list[str] = [ 
            'script', 'style', 'head', 'meta', 'link', 'noscript', 
            'iframe', 'embed', 'object', 'applet', 'audio', 'video',
            'svg', 'canvas', 'map', 'area', 'dialog', 'figure', 'figcaption', 'details', 'summary',
        ]
        # Удаление начального набора тегов
        for tag_name_to_remove in tags_to_remove_completely_initial:
            for tag_object in soup.find_all(tag_name_to_remove):
                tag_object.decompose() # Полное удаление тега и его содержимого

        # Удаление HTML комментариев
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract() # Извлечение комментария из дерева
            
        # --- ШАГ A: СБОР ВНУТРЕННИХ ССЫЛОК ---
        # Ссылки собираются до основного этапа очистки атрибутов и удаления тегов <a>,
        # но после удаления <script>, <style> и т.д.
        search_scope_for_links_initial: BeautifulSoup | NavigableString | None = soup.body if soup.body else soup
        if search_scope_for_links_initial:
            # Поиск всех тегов <a> с атрибутом href
            all_a_tags_for_collection: list = search_scope_for_links_initial.find_all('a', href=True)
            unique_links_hrefs: set = set() # Множество для хранения уникальных абсолютных URL
            for link_tag_collect in all_a_tags_for_collection:
                href_value_collect: str | None = link_tag_collect.get('href')
                
                abs_href_collect: str = ''
                if href_value_collect:
                    try:
                        # Преобразование относительного URL в абсолютный
                        abs_href_collect = urljoin(base_url, href_value_collect.strip())
                        parsed_abs_href_collect: urlparse = urlparse(abs_href_collect)
                        # Пропуск ссылок с не-HTTP/HTTPS схемами
                        if parsed_abs_href_collect.scheme not in ('http', 'https'):
                            continue 
                    except ValueError:
                        continue # Пропуск, если URL не может быть обработан
                else:
                    continue # Пропуск тегов <a> без атрибута href

                # Извлечение текстового содержимого ссылки
                text_content_of_link_collect: str = link_tag_collect.get_text(separator=' ', strip=True)
                
                # Добавление внутренней ссылки в результат, если она валидна и уникальна
                if abs_href_collect and text_content_of_link_collect: 
                    if is_internal(base_url, abs_href_collect): # Проверка, является ли ссылка внутренней
                        if abs_href_collect not in unique_links_hrefs:
                            internal_links_output.append({"link": {"href": abs_href_collect, "text": text_content_of_link_collect}})
                            unique_links_hrefs.add(abs_href_collect)
        
        # --- ШАГ B: ОСНОВНАЯ ОЧИСТКА HTML (ТЕПЕРЬ МОЖНО УДАЛЯТЬ <a> И ДРУГИЕ) ---
        # Теги, удаляемые после сбора ссылок. Они могли содержать ссылки, но теперь не нужны в очищенном HTML.
        tags_to_remove_after_link_collection: list[str] = [
             'header', 'footer', 'nav', 'aside', 
             'form', 'button', 'input', 'textarea', 'select', 'option',
             'a' # <--- Удаление всех тегов <a>
        ]
        # Удаление указанных тегов
        for tag_name_to_remove in tags_to_remove_after_link_collection:
            for tag_object in soup.find_all(tag_name_to_remove):
                tag_object.decompose()


        # --- 2. Очистка атрибутов у ОСТАВШИХСЯ тегов ---
        # (теги <a> уже удалены, так что их атрибуты не будут обрабатываться здесь)
        for tag in list(soup.find_all(True)): # Итерация по всем оставшимся тегам
            # Пропуск тегов без имени или родителя (например, корневой элемент BeautifulSoup)
            if not tag.name or not tag.parent: continue
            
            # Проверка, является ли тег значащим медиа-элементом (img с src или alt)
            is_meaningful_media: bool = tag.name == 'img' and (tag.get('src') or tag.get('alt'))
            
            has_significant_content: bool = False
            if is_meaningful_media: # img сохраняется, если есть src/alt
                has_significant_content = True
            elif tag.get_text(strip=True): # Любой другой тег сохраняется, если в нем есть текст
                has_significant_content = True
            
            if has_significant_content:
                current_attrs: dict = dict(tag.attrs) 
                new_attrs: dict = {} # Словарь для новых, разрешенных атрибутов
                for attr_name, attr_value in current_attrs.items():
                    attr_name_lower: str = attr_name.lower()
                    
                    # Проверка, разрешен ли атрибут по списку или по data-* паттерну
                    allowed_by_list: bool = attr_name_lower in ALLOWED_ATTRIBUTES
                    allowed_by_data_pattern: bool = False
                    if not allowed_by_list:
                        allowed_by_data_pattern = any(
                            allowed_pattern == 'data-*' and attr_name_lower.startswith('data-')
                            for allowed_pattern in ALLOWED_ATTRIBUTES
                        )
                    
                    if allowed_by_list or allowed_by_data_pattern:
                        val_to_process: str = ""
                        # Обработка значения атрибута (может быть строкой или списком)
                        if isinstance(attr_value, list):
                            if attr_value and isinstance(attr_value[0], str):
                                val_to_process = attr_value[0].strip()
                        elif isinstance(attr_value, str):
                            val_to_process = attr_value.strip()
                        else: continue # Пропуск, если значение не строка или не список строк

                        # Пропуск пустых значений атрибутов, кроме 'alt'
                        if not val_to_process and attr_name_lower not in ('alt'): continue
                        
                        # Специальная обработка для 'src' у 'img' (абсолютизация URL)
                        if attr_name_lower == 'src' and tag.name == 'img':
                            if not val_to_process.startswith(('data:')): # Игнорирование data URI
                                try: 
                                    abs_url: str = urljoin(base_url, val_to_process)
                                    parsed_abs_url: urlparse = urlparse(abs_url)
                                    if parsed_abs_url.scheme in ('http', 'https'): new_attrs[attr_name] = abs_url
                                    else: logger.debug(f"Пропущен src с невалидной схемой: '{abs_url}' для {base_url}")
                                except ValueError: logger.debug(f"Не удалось обработать src '{val_to_process}' для {base_url}")
                        elif allowed_by_data_pattern: new_attrs[attr_name] = attr_value # Сохранение data-* атрибутов как есть
                        else: new_attrs[attr_name] = val_to_process # Сохранение других разрешенных атрибутов
                tag.attrs = new_attrs # Обновление атрибутов тега
            else: 
                # Удаление тега, если он не содержит значимого контента и не является 'body', 'html' или 'br'
                if tag.name not in ('body', 'html', 'br'): 
                    tag.decompose()

        # --- 3. Получаем очищенный HTML из body и извлекаем из него текст ---
        body_tag: NavigableString | None = soup.body
        if body_tag:
            # Финальная очистка пустых тегов (кроме img, br) из body
            for tag_to_clean in list(body_tag.find_all(True)): 
                if tag_to_clean.name not in ('img', 'br') and \
                   not tag_to_clean.attrs and \
                   not tag_to_clean.contents and \
                   not tag_to_clean.get_text(strip=True): 
                    if tag_to_clean.name != 'body': tag_to_clean.decompose()
            
            # Формирование строки очищенного HTML из содержимого body
            cleaned_html_output = "".join(str(c) for c in body_tag.contents).strip()
            # Нормализация пробелов и переносов строк в HTML
            cleaned_html_output = cleaned_html_output.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
            cleaned_html_output = re.sub(r'\s{2,}', ' ', cleaned_html_output).strip()
            
            if cleaned_html_output:
                # Для извлечения текста из HTML, который уже НЕ СОДЕРЖИТ <a>
                temp_soup_for_text: BeautifulSoup = BeautifulSoup(cleaned_html_output, 'html5lib')
                # Замена <br> на перенос строки для лучшего форматирования текста
                for br_tag in temp_soup_for_text.find_all("br"): br_tag.replace_with("\n")
                
                # Добавление переносов строк после блочных тегов для улучшения читаемости текста
                block_tags_for_text_formatting: list[str] = ['p', 'div', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'table', 'tr', 'section', 'article', 'main', 'address']
                for block_tag_name in block_tags_for_text_formatting:
                    for bt in temp_soup_for_text.find_all(block_tag_name):
                        bt.append("\n") 

                # Извлечение текста
                plain_text_output = temp_soup_for_text.get_text(separator=' ', strip=False) 
                # Нормализация множественных переносов строк и пробелов
                plain_text_output = re.sub(r'[ \t]*\n[ \t\n]*', '\n', plain_text_output) 
                plain_text_output = re.sub(r'\s{2,}', ' ', plain_text_output).strip()
        
        # Логирование, если извлеченный текст оказался пустым
        if not plain_text_output.strip(): 
            logger.info(f"Извлеченный ТЕКСТ (без тегов) для {base_url} оказался пустым после очистки.")
        
        # Возврат словаря с извлеченными данными
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
        # Логирование критической ошибки при обработке HTML
        import traceback
        logger.error(f"Критическая ошибка при обработке HTML для {base_url}: {e}\n{traceback.format_exc()}")
        # Возврат пустого шаблона в случае ошибки
        return empty_result_template


def update_output_dict(data_dict: dict, timestamp:str, url:str) -> bool:
    """
    Сохраняет словарь данных `data_dict` в JSON-файл и обновляет список проверенных URL.
    Имя файла и путь формируются на основе URL и временной метки.

    Args:
        data_dict (dict): Словарь с данными для сохранения.
        timestamp (str): Временная метка для использования в имени файла (например, YYYYMMDD_HHMMSS).
        url (str): URL, для которого были собраны данные.

    Returns:
        bool: `True` в случае успешного сохранения, иначе `False`.
    """
    domain_name: str
    try:
        # Парсинг URL для извлечения домена и пути
        parsed_url: urlparse = urlparse(url)
        domain_name = parsed_url.netloc.replace('.', '_') 
        if not domain_name: domain_name = "unknown_domain"
    except Exception: domain_name = "parse_error_domain" # Обработка ошибки парсинга домена

    # Формирование пути к папке на основе даты и домена
    date_str: str = timestamp.split('_')[0] if '_' in timestamp else timestamp
    date_folder: Path = Path(rf"F:/llm/filtered_urls/{date_str}") 
    domain_folder: Path = date_folder / domain_name
    # Создание директорий, если они не существуют
    domain_folder.mkdir(parents=True, exist_ok=True) 

    # Формирование безопасной части имени файла из пути URL
    path_part: str = (parsed_url.path + parsed_url.query).strip('/') 
    safe_url_part: str = re.sub(r'[^a-zA-Z0-9_-]', '_', path_part)[:100] # Ограничение длины и замена небезопасных символов
    if not safe_url_part: safe_url_part = "index" # Использование "index" для корневых URL
    
    # Формирование полного имени выходного файла
    output_file_name: str = f"{timestamp}_{safe_url_part}.json"
    output_file: Path = domain_folder / output_file_name
    
    # Добавление URL в сохраняемый словарь
    data_dict_to_save: dict = {'url': url, **data_dict} 

    # Сохранение данных в JSON файл
    if not j_dumps(data_dict_to_save, output_file, indent=4): 
        logger.error(f"Ошибка записи в файл {output_file}")
        return False

    logger.success(f'Файл {output_file} - Записан!')
    # Обновление файла со списком уже обработанных URL
    utils.update_checked_urls_file(url) 
    return True


# --- Основной блок выполнения ---
if __name__ == "__main__":
    # Инициализация переменных
    driver: Driver | None = None 
    urls_successfully_processed_count: int = 0
    try:
        # Инициализация веб-драйвера Firefox в безголовом режиме
        driver = Driver(Firefox, window_mode='headless')
        
        # Определение пути к файлу со списком уже проверенных URL
        checked_urls_path: Path = Path(rf"F:/llm/filtered_urls/checked_urls.txt")
        checked_urls: list = [] # Список для хранения проверенных URL
        try:
            # Чтение файла проверенных URL, если он существует
            if checked_urls_path.exists():
                 checked_urls = read_text_file(checked_urls_path, as_list=True) or [] # Обеспечение списка в случае ошибки чтения
            else:
                logger.info(f"Файл {checked_urls_path} не найден, будет создан новый.")
        except Exception as e:
            logger.warning(f"Не удалось прочитать файл checked_urls.txt: {e}. Список проверенных URL будет пуст.")

        fetched_urls_list: list = [] # Список для URL, извлеченных из исходных файлов
        try:
            # Извлечение URL из файлов-источников
            fetched_urls_list = utils.fetch_urls_from_all_mining_files(
                ['source_urls_1.txt', 'source_urls_2.txt'] # Пример имен файлов
            ) 
        except Exception as e:
            logger.error(f"Ошибка при получении списка URL из mining_files: {e}")

        # Очистка и получение уникальных URL
        cleaned_fetched_urls: set = {u.strip() for u in fetched_urls_list if u and u.strip()}
        cleaned_checked_urls: set = {u.strip() for u in checked_urls if u and u.strip()}
        # Формирование списка URL для обработки (новые URL)
        actual_urls: list = list(cleaned_fetched_urls - cleaned_checked_urls)
        # Перемешивание списка URL для случайного порядка обработки
        random.shuffle(actual_urls)

        # Проверка, есть ли новые URL для обработки
        if not actual_urls:
            logger.info("Нет новых URL для обработки.")
            sys.exit(0) # Завершение работы, если нет новых URL

        logger.info(f"Найдено {len(actual_urls)} новых URL для обработки.")
        
        # Максимальное количество URL для обработки за один запуск скрипта
        max_urls_to_process_per_run: int = 100 

        # Итерация по списку URL для обработки
        current_url: str
        for current_url in actual_urls:
            # Проверка лимита обработки URL за запуск
            if urls_successfully_processed_count >= max_urls_to_process_per_run:
                logger.info(f"Достигнут лимит обработки ({max_urls_to_process_per_run} URL) за этот запуск.")
                break

            logger.info(f"Обработка URL: {current_url}")

            # Проверка, что URL начинается с http:// или https://
            if not current_url.startswith(('http://', 'https://')):
                logger.warning(f"URL '{current_url}' пропущен (не начинается с http:// или https://).")
                utils.update_checked_urls_file(current_url) # Добавление в проверенные, чтобы не пытаться снова
                continue

            try:
                # Парсинг URL для проверки домена и применения фильтров
                parsed_url_check: urlparse = urlparse(current_url)
                domain_check: str = parsed_url_check.netloc.lower()

                # Проверка наличия домена в URL
                if not domain_check:
                    logger.warning(f"URL '{current_url}' пропущен (не удалось определить домен).")
                    utils.update_checked_urls_file(current_url)
                    continue

                # Фильтрация URL по запрещенным ключевым словам
                is_forbidden: bool = False
                keyword: str
                for keyword in FORBIDDEN_KEYWORDS:
                    if keyword in current_url.lower():
                        is_forbidden = True
                        logger.info(f"Фильтр: URL '{current_url}' пропущен (содержит запрещенное слово/паттерн '{keyword}').")
                        break
                if is_forbidden:
                    utils.update_checked_urls_file(current_url) # Добавление в проверенные
                    continue

            except Exception as e: 
                logger.error(f"Ошибка анализа URL '{current_url}': {e}")
                utils.update_checked_urls_file(current_url) # Добавление в проверенные при ошибке анализа
                continue

            # Получение HTML-контента страницы
            if not driver.fetch_html(current_url): 
                logger.error(f"Не удалось получить HTML для {current_url}")
                utils.update_checked_urls_file(current_url) # Добавление в проверенные при ошибке загрузки
                continue
            
            # Проверка, что HTML-контент не пуст
            if not driver.html_content: 
                logger.error(f"HTML контент для {current_url} пуст после fetch_html.")
                utils.update_checked_urls_file(current_url) # Добавление в проверенные, если контент пуст
                continue

            logger.info(f"Извлечение данных для {current_url}...")
            
            # Получение временной метки для имени файла
            file_timestamp: str = gs.now_До_секунд() if hasattr(gs, 'now_До_секунд') else gs.now()

            # Извлечение данных со страницы
            page_data_dict: dict = extract_page_data(driver.html_content, current_url)
            
            # Проверка, что данные извлечены и текстовое содержимое не пустое
            if page_data_dict and page_data_dict.get('text', '').strip():
                logger.success(f"Данные для {current_url} успешно извлечены (текст не пуст).")
                # Сохранение извлеченных данных
                if update_output_dict(page_data_dict, file_timestamp, current_url): 
                    urls_successfully_processed_count += 1 # Увеличение счетчика успешно обработанных URL
            else:
                logger.warning(f"Не удалось извлечь значимые данные (текст без тегов пуст или ошибка) для {current_url}.")
                utils.update_checked_urls_file(current_url) # Добавление в проверенные, если значимые данные не извлечены

    except KeyboardInterrupt:
        # Обработка прерывания скрипта пользователем
        logger.warning("Обработка прервана пользователем (KeyboardInterrupt).")
    except Exception as ex_main:
        # Логирование критических ошибок в основном блоке
        logger.critical(f"Критическая ошибка в основном блоке выполнения: {ex_main}", None, exc_info=True)
    finally:
        # Завершение работы драйвера в любом случае
        if driver:
            logger.info("Завершение работы драйвера...")
            driver.quit()
        logger.info(f"Скрипт {Path(__file__).name} завершил работу. Успешно обработано URL: {urls_successfully_processed_count}.")
