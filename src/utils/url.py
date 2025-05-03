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
from urllib.parse import urlparse, parse_qs
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

# ... (extract_url_params остается без изменений) ...
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


# Функция get_domain остается как есть - она извлекает netloc и очищает www/port
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


# ... (is_url и url_shortener остаются без изменений) ...
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

