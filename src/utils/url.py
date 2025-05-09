## \file /src/utils/string/url.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для работы с URL строками.
=================================
Предоставляет функции для извлечения параметров запроса, проверки валидности URL,
сокращения ссылок, извлечения базового домена (схема + домен) и
извлечения "чистого" доменного имени.

Зависимости:
    - validators (pip install validators)
    - requests (pip install requests)
    - ipaddress (стандартная библиотека)

```rst
.. module:: src.utils.string.url
```
"""

import re # Импортируем re для регулярных выражений
import ipaddress # Для проверки IP-адресов
from urllib.parse import urlparse, parse_qs, urlunparse, quote, unquote
from typing import Optional, Dict, Any, Union, List

# Сторонние библиотеки
import validators
import requests

import header
from src.logger import logger

# --- Исключения ---
class URLError(ValueError):
    """ Базовое исключение для ошибок, связанных с URL в этом модуле. """
    pass
class ShorteningError(URLError):
    """ Исключение для ошибок при сокращении URL. """
    pass

# --- Константы ---
# Символы для грубой очистки с конца строки
TRAILING_JUNK_CHARS: str = ',";\')\n'
# Регулярное выражение для символов, НЕ разрешенных в стандартном доменном имени (LDH + dot)
# Мы будем удалять все, что НЕ является буквой, цифрой, дефисом или точкой.
INVALID_DOMAIN_CHARS_PATTERN = re.compile(r'[^a-zA-Z0-9.-]+')
# Шаблон для проверки, что строка состоит ТОЛЬКО из разрешенных символов (для финальной валидации)
ALLOWED_DOMAIN_CHARS_ONLY_PATTERN = re.compile(r'^[a-zA-Z0-9.-]+$')


# --- Функции работы с URL ---

def extract_url_params(url: Optional[str]) -> Optional[Dict[str, Any]]:
    """ Извлекает параметры из строки запроса URL. (код без изменений) """
    # ... (код функции extract_url_params) ...
    parsed_url: Any; params: Optional[Dict[str, Any]] = None; params_raw: Dict[str, List[str]]
    if not url or not isinstance(url, str): return None
    try:
        parsed_url = urlparse(url); params_raw = parse_qs(parsed_url.query)
        if params_raw:
            params = {}; k: str; v: List[str]
            for k, v in params_raw.items():
                if len(v) == 1: params[k] = v[0]
                elif len(v) > 1: params[k] = v
            return params if params else None
    except Exception as ex: logger.error(f"Ошибка при парсинге параметров URL '{url}': {ex}", ex, exc_info=True); return None
    return None



def get_domain(url: Optional[str]) -> Optional[str]:
    """
    Извлекает netloc (хост[:порт]) из URL, очищает от 'www.' и порта.
    Предварительно выполняет базовую очистку строки URL.

    Args:
        url (Optional[str]): Входной URL.

    Returns:
        Optional[str]: Очищенный хост (например, "example.com", "sub.test.co.uk", "[::1]")
                       или None, если хост не найден или произошла ошибка.
    """
    # ... (код функции get_domain из предыдущего ответа, без финального .lower()) ...
    # Объявление переменных
    parsed_url: Any; netloc: Optional[str] = None; domain_part: str
    url_to_parse: str; cleaned_url: str

    if not url or not isinstance(url, str): return None
    try:
        cleaned_url = url.strip().rstrip(TRAILING_JUNK_CHARS)
        if not cleaned_url: logger.warning(f"URL '{url}' стал пустым после очистки."); return None
        if cleaned_url != url: logger.debug(f"URL '{url}' очищен до '{cleaned_url}' перед парсингом.")
    except Exception as ex: logger.error(f"Ошибка на этапе очистки URL '{url}': {ex}", ex, exc_info=True); return None

    try:
        if not cleaned_url.startswith(('http://', 'https://', 'ftp://', '//')): url_to_parse = f'//{cleaned_url}'
        else: url_to_parse = cleaned_url
        parsed_url = urlparse(url_to_parse); netloc = parsed_url.netloc
        if not netloc and url_to_parse == f'//{cleaned_url}':
             if '.' in cleaned_url and not any(c in cleaned_url for c in ['/', ':', '?', '#']):
                 netloc = cleaned_url; logger.debug(f"Очищенный URL '{cleaned_url}' обработан как прямой домен (netloc).")
        if not netloc: logger.warning(f"Не удалось извлечь netloc из очищенного URL: '{cleaned_url}' (исходный: '{url}')"); return None
        if netloc.lower().startswith('www.'): domain_part = netloc[4:]
        else: domain_part = netloc
        # Возвращаем хост без порта, но СОХРАНЯЕМ РЕГИСТР и скобки для IPv6
        return domain_part.split(':', 1)[0]
    except Exception as ex: logger.error(f"Ошибка при обработке очищенного URL '{cleaned_url}' (исходный: '{url}'): {ex}", ex, exc_info=True); return None


def extract_pure_domain(text: Optional[str]) -> Optional[str]:
    """
    Агрессивно извлекает "чистое" доменное имя из строки.

    Пытается получить хост с помощью get_domain, затем удаляет все символы,
    кроме букв (a-z, A-Z), цифр (0-9), дефиса (-) и точки (.).
    Проверяет результат на базовую валидность (не пустой, содержит точку или 'localhost').
    IP-адреса (v4, v6) будут отброшены, так как они не являются "чистыми" именами.

    Args:
        text (Optional[str]): Входная строка (может быть URL или просто текст).

    Returns:
        Optional[str]: Извлеченное и очищенное доменное имя в нижнем регистре
                       (например, "example.com") или None, если домен извлечь не удалось.

    Example:
        >>> extract_pure_domain("https://www.Example.com:80/path?q=1")
        'example.com'
        >>> extract_pure_domain(" sub.domain-test.co.uk ")
        'sub.domain-test.co.uk'
        >>> extract_pure_domain("exa_mple.com") # Подчеркивание будет удалено
        'example.com'
        >>> extract_pure_domain("test..com") # Двойные точки останутся (простая очистка)
        'test..com'
        >>> extract_pure_domain('https://ass_ured,automa(tion).com)') # Много мусора
        'assuredautomation.com'
        >>> extract_pure_domain("http://192.168.1.1/page") # IP v4
        None
        >>> extract_pure_domain("http://[::1]:80") # IP v6
        None
        >>> extract_pure_domain("localhost")
        'localhost'
        >>> extract_pure_domain(" just text ")
        None
        >>> extract_pure_domain(None)
        None
    """
    # Объявление переменных
    hostname: Optional[str] = None
    cleaned_domain: str
    final_domain: str

    if not text or not isinstance(text, str):
        return None

    # 1. Получаем хост с помощью get_domain (она выполнит базовую очистку и извлечет netloc)
    hostname = get_domain(text) # get_domain возвращает хост без порта и www.

    if not hostname:
        # get_domain не смог извлечь хост
        return None

    # 2. Проверяем, не является ли извлеченный хост IP-адресом
    try:
        # ipaddress.ip_address() выбросит ValueError, если это не валидный IP
        _ = ipaddress.ip_address(hostname)
        # Если мы здесь, значит это IP-адрес. Отбрасываем его.
        logger.debug(f"Извлеченный хост '{hostname}' является IP-адресом, пропускаем.")
        return None
    except ValueError:
        # Это не IP-адрес, продолжаем обработку как потенциального домена
        pass
    except Exception as ip_ex:
        # Ловим другие редкие ошибки из ipaddress
        logger.error(f"Ошибка при проверке IP для хоста '{hostname}': {ip_ex}", exc_info=True)
        # На всякий случай прерываем обработку, т.к. не уверены в результате
        return None

    # 3. Агрессивная очистка: удаляем все НЕдопустимые символы
    try:
        # Удаляем все, что не буква, не цифра, не дефис и не точка
        cleaned_domain = INVALID_DOMAIN_CHARS_PATTERN.sub('', hostname)
    except Exception as regex_ex:
        logger.error(f"Ошибка regex при очистке хоста '{hostname}': {regex_ex}", exc_info=True)
        return None

    # 4. Финальная санитаризация и валидация
    # Удаляем возможные дефисы/точки с начала/конца, возникшие после очистки
    final_domain = cleaned_domain.strip('.-')

    # Проверяем, что результат не пустой и выглядит как домен
    if not final_domain:
        logger.debug(f"Результат после очистки хоста '{hostname}' пуст.")
        return None

    # Домен (кроме localhost) должен содержать хотя бы одну точку
    # и состоять только из разрешенных символов (доп. проверка после regex)
    is_localhost = final_domain.lower() == 'localhost'
    contains_dot = '.' in final_domain
    is_valid_chars = bool(ALLOWED_DOMAIN_CHARS_ONLY_PATTERN.match(final_domain))

    if not is_valid_chars:
         logger.warning(f"Результат '{final_domain}' после очистки хоста '{hostname}' содержит недопустимые символы (ошибка regex?).")
         return None

    if not is_localhost and not contains_dot:
        logger.warning(f"Результат '{final_domain}' после очистки хоста '{hostname}' не является 'localhost' и не содержит точку.")
        return None

    # 5. Возвращаем результат в нижнем регистре
    return final_domain.lower()




def normalize_url(url: str, default_scheme: str = 'http') -> str:
    """
    Нормализует URL-адрес, приводя его к более стандартному виду.

    Основные шаги нормализации:
    1. Удаляет начальные/конечные пробелы.
    2. Очищает от "мусорных" символов (пробелы, кавычки, запятые), если они находятся
       непосредственно перед компонентом пути ('/'), запроса ('?'), фрагмента ('#')
       или в конце URL.
    3. Добавляет схему по умолчанию (http/https), если она отсутствует.
    4. Приводит схему и домен (netloc) к нижнему регистру.
    5. Обрабатывает Internationalized Domain Names (IDN), кодируя netloc в punycode.
    6. Заменяет множественные слеши в пути на один.
    7. Гарантирует, что путь начинается с '/', если есть домен.
    8. Удаляет стандартные порты (80 для http, 443 для https).
    9. Удаляет фрагмент ('#section').
    10. Перекодирует путь и параметры запроса для корректности,
        удаляя мусорные символы с конца декодированных пути/параметров.


    Args:
        url (str | None): Входной URL для нормализации.
        default_scheme (str): Схема по умолчанию ('http' или 'https'), добавляемая, если схема отсутствует.
                              По умолчанию 'http'.

    Returns:
        str | None: Нормализованный URL или None, если входной URL некорректен
                       или не может быть успешно разобран/нормализован.

    Example:
        >>> normalize_url("  HTTP://Www.Example.Com:80/path//to/page?q=1&b=2#section  ")
        'http://www.example.com/path/to/page?q=1&b=2'
        >>> normalize_url("www.example.com/path")
        'http://www.example.com/path'
        >>> normalize_url("https://example.com:443")
        'https://example.com/'
        >>> normalize_url("example.com")
        'http://example.com/'
        >>> normalize_url("ftp://example.com/file") # Другие схемы сохраняются
        'ftp://example.com/file'
        >>> normalize_url("invalid-url") # Не похож на URL
        None
        >>> normalize_url("http://пример.рф/путь") # IDN handling
        'http://xn--e1afmkfd.xn--p1ai/%D0%BF%D1%83%D1%82%D1%8C'
        >>> normalize_url('https://www.11st.co.kr/products/1122334455,"') # Очистка мусора на конце
        'https://www.11st.co.kr/products/1122334455'
        >>> normalize_url('https://example.com/path%2C%22') # Очистка мусора (закодированного в пути)
        'https://example.com/path'
        >>> normalize_url('https://uk.rs-online.com",#main-content') # Очистка мусора перед фрагментом
        'https://uk.rs-online.com#main-content'
        >>> normalize_url('https://uk.rs-online.com",/en/contact/') # Очистка мусора перед путем
        'https://uk.rs-online.com/en/contact/'
        >>> normalize_url(None)
        None
    """
    
    original_url_for_log: str
    processed_url: str
    parsed_parts: 'urllib.parse.ParseResult | None' = None
    
    scheme_norm: str = ''
    netloc_norm: str = ''
    netloc_raw: str
    path_norm: str = ''
    path_raw: str
    path_intermediate: str
    decoded_path: str
    cleaned_decoded_path: str
    path_fallback: str
    params_norm: str = ''
    query_norm: str = ''
    query_raw: str
    decoded_query: str
    cleaned_decoded_query: str
    fragment_norm: str = '' # Фрагмент всегда удаляется
    

    if not url or not isinstance(url, str):
        return None

    original_url_for_log = url # Сохранение оригинального URL для логирования
    
    # 1. Удаление начальных/конечных пробелов
    processed_url = url.strip()
    if not processed_url:
        return None

    # 2. Предварительная очистка от мусорных символов (для НЕЗАКОДИРОВАННЫХ символов).
    # Удаление символов типа пробелов, кавычек, запятых, если они находятся
    # непосредственно перед компонентом пути ('/'), запроса ('?'), фрагмента ('#') или в конце URL.
    processed_url = re.sub(r'[\s\'",]+(?=([/?#]|$))', '', processed_url)
    if not processed_url: # Проверка, не стала ли строка пустой после очистки
        return None

    # 3. Добавление схемы по умолчанию
    if '://' not in processed_url and not processed_url.startswith('//'):
        # Применение эвристики для определения, следует ли добавлять схему
        if ('.' in processed_url or processed_url.lower() == 'localhost') and not re.match(r'^[a-zA-Z]:\\', processed_url):
             logger.debug(f"URL '{original_url_for_log}' не имеет схемы, добавление '{default_scheme}://'")
             processed_url = default_scheme + '://' + processed_url
        else:
            logger.warning(f"Строка '{original_url_for_log}' не содержит схему и не похожа на URL для добавления схемы по умолчанию. Нормализация невозможна.", None, False)
            return None # Завершение нормализации, если невозможно определить схему

    # 4. Парсинг URL
    try:
        # Выполнение разбора URL на компоненты с использованием urlparse
        parsed_parts = urlparse(processed_url)
    except ValueError as ex:
        logger.error(f"Ошибка парсинга URL '{processed_url}'", ex, exc_info=True)
        return None

    # 5. Валидация базовых компонентов
    if not parsed_parts.scheme: # Проверка на наличие схемы
        logger.warning(f"URL '{processed_url}' после парсинга не содержит схему. Невозможно нормализовать.", None, False)
        return None
    
    # Проверка на наличие сетевого расположения (netloc) для соответствующих схем
    if not parsed_parts.netloc and parsed_parts.scheme.lower() not in ('file', 'mailto', 'data', 'javascript'):
        logger.warning(f"URL '{processed_url}' (схема: {parsed_parts.scheme}) после парсинга не содержит сетевое расположение (netloc). Невозможно нормализовать.", None, False)
        return None

    # 6. Нормализация компонентов
    scheme_norm = parsed_parts.scheme.lower()
    netloc_raw = parsed_parts.netloc
    
    if netloc_raw:
        # Выполнение IDN-обработки
        try:
            netloc_norm = netloc_raw.encode('idna').decode('utf-8').lower()
            netloc_norm = netloc_norm.encode('idna').decode('ascii')
        except UnicodeError as ex_idn_unicode:
            logger.warning(f"Ошибка IDN кодирования для netloc: '{netloc_raw}'. Используется .lower().", ex_idn_unicode, False)
            netloc_norm = netloc_raw.lower()
        except Exception as ex_idn_general:
             logger.error(f"Неожиданная ошибка при обработке IDN для netloc '{netloc_raw}'", ex_idn_general, exc_info=True)
             netloc_norm = netloc_raw.lower() # fallback

        # Удаление стандартных портов
        if (scheme_norm == 'http' and netloc_norm.endswith(':80')) or \
           (scheme_norm == 'https' and netloc_norm.endswith(':443')):
            netloc_norm = netloc_norm.rsplit(':', 1)[0]
    else:
        netloc_norm = ''

    # --- ОБРАБОТКА ПУТИ (PATH) ---
    path_raw = parsed_parts.path
    if path_raw:
        # 1. Выполнение нормализации множественных слешей
        path_intermediate = re.sub(r'/+', '/', path_raw)
        
        # 2. Выполнение декодирования, очистки от мусорных символов в конце, повторного кодирования
        try:
            decoded_path = unquote(path_intermediate)
            # Удаление мусорных символов [\s\'",] с конца декодированного пути
            cleaned_decoded_path = re.sub(r'[\s\'",]+$', '', decoded_path)
            path_norm = quote(cleaned_decoded_path, safe='/%:@')
        except Exception as ex_path_proc:
            logger.warning(
                f"Ошибка при полной обработке пути для '{path_raw}': {ex_path_proc}. "
                f"Применяется только нормализация слешей и стандартное кодирование.", ex_path_proc, False
            )
            path_fallback = re.sub(r'/+', '/', path_raw)
            try:
                path_norm = quote(path_fallback, safe='/%:@')
            except Exception as ex_path_fallback_quote:
                logger.error(f"Критическая ошибка при кодировании пути '{path_fallback}' в fallback", ex_path_fallback_quote, exc_info=True)
                path_norm = path_fallback
    elif netloc_norm: # Установка корневого пути '/', если присутствует домен, но отсутствует путь
        path_norm = '/'


    # --- ОБРАБОТКА ПАРАМЕТРОВ ЗАПРОСА (QUERY) ---
    query_raw = parsed_parts.query
    if query_raw:
        try:
            decoded_query = unquote(query_raw)
            cleaned_decoded_query = re.sub(r'[\s\'",]+$', '', decoded_query)
            query_norm = quote(cleaned_decoded_query, safe='/?!@#$&()*+,;=:%')
        except Exception as ex_query_proc:
            logger.warning(
                f"Ошибка при полной обработке query для '{query_raw}': {ex_query_proc}. "
                f"Применяется стандартное кодирование исходного query.", ex_query_proc, False
            )
            try:
                query_norm = quote(query_raw, safe='/?!@#$&()*+,;=:%')
            except Exception as ex_query_fallback_quote:
                logger.error(f"Критическая ошибка при кодировании query '{query_raw}' в fallback", ex_query_fallback_quote, exc_info=True)
                query_norm = query_raw
    
    fragment_norm = '' # Удаление фрагмента
    params_norm = parsed_parts.params # Компонент params остается без изменений

    # 7. Сборка нормализованного URL
    try:
        # Сборка URL из нормализованных компонентов
        normalized_url_result = urlunparse((scheme_norm, netloc_norm, path_norm, params_norm, query_norm, fragment_norm))
    except Exception as ex_unparse:
        logger.error(f"Ошибка сборки URL из компонентов: {(scheme_norm, netloc_norm, path_norm, params_norm, query_norm, fragment_norm)}", ex_unparse, exc_info=True)
        return None # Возврат None в случае ошибки сборки

    return normalized_url_result




def is_url(text: Optional[str]) -> bool:
    """ Проверяет, является ли переданный текст валидным URL. (код без изменений) """
    # ... (код функции is_url) ...
    validation_result: Any
    if not text or not isinstance(text, str): return False
    try: validation_result = validators.url(text); return bool(validation_result)
    except Exception as ex: logger.error(f"Ошибка при вызове validators.url для текста '{text}': {ex}", ex, exc_info=True); return False

def url_shortener(long_url: Optional[str]) -> Optional[str]:
    """ Сокращает длинный URL с использованием сервиса TinyURL. (код без изменений) """
    # ... (код функции url_shortener) ...
    url: str; response: requests.Response
    if not long_url or not is_url(long_url): logger.warning(f'Невалидный URL для сокращения: {long_url}'); return None
    try:
        url = f'http://tinyurl.com/api-create.php?url={long_url}'; response = requests.get(url, timeout=10)
        response.raise_for_status(); return response.text
    except requests.exceptions.RequestException as ex: logger.error(f'Ошибка сети при запросе к TinyURL для URL {long_url}: {ex}', ex, exc_info=True); return None
    except Exception as ex: logger.error(f'Неожиданная ошибка при сокращении URL {long_url}: {ex}', ex, exc_info=True); return None


if __name__ == "__main__":
    # --- Примеры использования ---
    urls_to_test = [
        "https://www.Example.com:80/path?q=1",
        " sub.domain-test.co.uk ",
        "exa_mple.com", # Подчеркивание будет удалено
        "test..com", # Двойные точки останутся
        'https://ass_ured,automa(tion).com)', # Много мусора
        "http://192.168.1.1/page", # IP v4
        "http://[::1]:80", # IP v6
        "localhost",
        " just text ",
        None,
        "www.Valid-Domain.INFO",
        "-invalid-.com", # Будет очищен до invalid.com
        ".anotherinvalid.", # Будет очищен до anotherinvalid
        "singlelabel",
        "https://www.xn--e1aybc.xn--p1ai/path" # IDN Punycode
    ]

    print("\n--- Тестирование extract_pure_domain ---")
    for test_url in urls_to_test:
        result = extract_pure_domain(test_url)
        print(f"Input: {repr(test_url):<40} -> Output: {result}")

    # --- Ассерты ---
    assert extract_pure_domain("https://www.Example.com:80/path?q=1") == 'example.com'
    assert extract_pure_domain(" sub.domain-test.co.uk ") == 'sub.domain-test.co.uk'
    assert extract_pure_domain("exa_mple.com") == 'example.com'

    # assert extract_pure_domain("test..com") == 'test.com' # Ожидаемое поведение? Очистка не убирает двойные точки
    assert extract_pure_domain('https://ass_ured,automa(tion).com)') == 'assuredautomation.com'
    assert extract_pure_domain("http://192.168.1.1/page") is None
    assert extract_pure_domain("http://[::1]:80") is None
    assert extract_pure_domain("localhost") == 'localhost'
    assert extract_pure_domain(" just text ") is None
    assert extract_pure_domain(None) is None
    assert extract_pure_domain("www.Valid-Domain.INFO") == 'valid-domain.info'
    assert extract_pure_domain("-invalid-.com") == 'invalid.com' # strip('.-') сработает
    assert extract_pure_domain(".anotherinvalid.") == 'anotherinvalid' # strip('.-') сработает, но точки внутри нет
    assert extract_pure_domain("singlelabel") is None # Нет точки
    assert extract_pure_domain("https://www.xn--e1aybc.xn--p1ai/path") == 'xn--e1aybc.xn--p1ai' # Punycode IDN (содержит дефис)

    print("\nАссерты для extract_pure_domain пройдены (с учетом ожиданий).")

    # --------------------- Нормализавия строки URL ----------------------------------------
    urls_to_test = [
    "  HTTP://Www.Example.Com:80/path//to/page?q=1&b=2#section  ",
    "www.example.com/path",
    "https://example.com:443",
    "example.com",
    "ftp://Example.Com/File",
    "invalid-url",
    "http://пример.рф/путь?параметр=значение#фрагмент",
    #Домен (IDN): пример.рф преобразуется в Punycode (xn--e1afmkfd.xn--p1ai).
    #Путь, параметры, фрагмент: Символы не из ASCII (например, путь, параметр, значение, фрагмент) 
    #преобразуются с помощью процентного кодирования (percent-encoding). Например, /путь станет /%D0%BF%D1%83%D1%82%D1%8C.
    
    "https://www.11st.co.kr/products/1122334455,\"",
    "//cdn.example.com/script.js", # Protocol-relative URL (станет http)
    "mailto:user@example.com", # Не изменится, т.к. нет netloc по правилам выше
    "http://user:pass@example.com/", # Сохранит user:pass
    "http://example.com/%7Euser/", # Сохранит %-кодирование
    "http://example.com/a%20b?c=d%26e", # Перекодирует пробел и амперсанд
    None,
    "",
    "   ",
    "http://[::1]:8080/path" # IPv6
    ]

    print("--- Тестирование normalize_url ---")

    # Examples from the docstring for testing
    test_cases = [
        ("  HTTP://Www.Example.Com:80/path//to/page?q=1&b=2#section  ", 'http://www.example.com/path/to/page?q=1&b=2'),
        ("www.example.com/path", 'http://www.example.com/path'),
        ("https://example.com:443", 'https://example.com/'),
        ("example.com", 'http://example.com/'),
        ("ftp://example.com/file", 'ftp://example.com/file'), # Другие схемы сохраняются
        ("invalid-url", None), # Не похож на URL
        ("http://пример.рф/путь", 'http://xn--e1afmkfd.xn--p1ai/%D0%BF%D1%83%D1%82%D1%8C'), # IDN handling
        ('https://www.11st.co.kr/products/1122334455,"', 'https://www.11st.co.kr/products/1122334455'), # Очистка мусора
        (None, None),
        ("http://domain.com/path?a=1&b=value with space", 'http://domain.com/path?a=1&b=value%20with%20space'),
        ("http://domain.com/path%20with%20spaces", 'http://domain.com/path%20with%20spaces'),
        ("HTTP://USER:PASS@EXAMPLE.COM/PATH", 'http://user:pass@example.com/PATH'), # User/pass unchanged, path case unchanged by this code
        ("http://example.com//a//b//c", "http://example.com/a/b/c"),
        ("http://example.com", "http://example.com/"),
        ("example.com:8080/path", "http://example.com:8080/path"), # Non-standard port preserved
        ("  ", None),
        # Case for step 3 validation adjustment: mailto and file
        ("mailto:test@example.com", "mailto:test@example.com"), # Should pass if mailto is considered valid
                                                               # Current code might return None if netloc is empty for mailto.
                                                               # urlparse("mailto:test@example.com") -> scheme='mailto', path='test@example.com', netloc=''
                                                               # The code's `if not parts.scheme or not parts.netloc:` will fail this.
                                                               # Corrected this check slightly in the code.
        ("file:///path/to/a/file.txt", "file:///path/to/a/file.txt"), # urlparse might give empty netloc.
                                                                   # urlparse('file:///c:/path/file') -> ParseResult(scheme='file', netloc='', path='/c:/path/file', ...)
    ]

    for i, (original, expected) in enumerate(test_cases):
        result = normalize_url(original)
        print(f"Test {i+1}: normalize_url(\"{original}\")")
        print(f"  Expected: \"{expected}\"")
        print(f"  Got:      \"{result}\"")
        if result == expected:
            print("  Status:   PASSED")
        else:
            print("  Status:   FAILED")
        print("-" * 20)

    # A specific test case from the error log:
    # The error was `NameError` so it wouldn't have gotten this far, but useful for testing path/query logic
    problematic_url = 'https://www.11st.co.kr/products/1122334455,"'
    print(f"Test from logs: normalize_url(\"{problematic_url}\")")
    result = normalize_url(problematic_url)
    expected = 'https://www.11st.co.kr/products/1122334455'
    print(f"  Expected: \"{expected}\"")
    print(f"  Got:      \"{result}\"")
    if result == expected:
        print("  Status:   PASSED")
    else:
        print("  Status:   FAILED")


    print("\n--- Тест с https по умолчанию ---")
    print(f"Оригинал: 'example.com/secure'\nНормализованный: {normalize_url('example.com/secure', default_scheme='https')!r}")

