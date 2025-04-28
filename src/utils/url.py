## \file /src/utils/string/url.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для работы с URL строками.
=================================
Предоставляет функции для извлечения параметров запроса, проверки валидности URL,
сокращения ссылок и извлечения базового домена (схема + домен).

Зависимости:
    - validators (pip install validators)
    - requests (pip install requests)

```rst
.. module:: src.utils.string.url
```
"""

from urllib.parse import urlparse, parse_qs
from typing import Optional, Dict, Any, Union, List 

# Используем стандартную библиотеку для валидации URL, если она подходит.
# Если требуется более строгая или специфичная валидация, можно использовать regex или другие подходы.

# Стандартные библиотеки
from urllib.parse import urlparse, parse_qs
from typing import Optional, Dict, Any # Добавлен Optional, Dict, Any

# Сторонние библиотеки
import validators # Для проверки URL
import requests   # Для запроса к TinyURL


import header
from src.logger import logger

# --- Исключения для кастомной обработки ---
class URLError(ValueError):
    """ Базовое исключение для ошибок, связанных с URL в этом модуле. """
    pass
class ShorteningError(URLError):
    """ Исключение для ошибок при сокращении URL. """
    pass




# --- Функции работы с URL ---

def extract_url_params(url: Optional[str]) -> Optional[Dict[str, Any]]:
    """
    Извлекает параметры из строки запроса URL.

    Args:
        url (Optional[str]): Строка URL для парсинга. Может быть None.

    Returns:
        Optional[Dict[str, Any]]: Словарь параметров запроса и их значений
                                   или `None`, если URL невалиден, пуст или не содержит параметров.
                                   Значения параметров - строки или списки строк.

    Example:
        >>> extract_url_params('https://example.com/?a=1&b=2&b=3')
        {'a': '1', 'b': ['2', '3']}
        >>> extract_url_params('https://example.com')
        None
        >>> extract_url_params(None)
        None
    """
    # Объявление переменных
    parsed_url: Any
    params: Optional[Dict[str, Any]] = None

    if not url or not isinstance(url, str):
        return None

    try:
        parsed_url = urlparse(url)
        # parse_qs возвращает список значений для каждого ключа
        params_raw: Dict[str, List[str]] = parse_qs(parsed_url.query)

        # Преобразуем значения из списка в строку, если параметр имеет только одно значение
        if params_raw:
            params = {}
            for k, v in params_raw.items():
                if len(v) == 1:
                    params[k] = v[0]
                elif len(v) > 1:
                    params[k] = v # Оставляем список, если значений несколько
                # Если v пустой (параметр без значения), можно пропустить или добавить как ''/None
            return params if params else None # Возвращаем None, если словарь пуст после обработки

    except Exception as ex:
        # В реальном коде используйте ваш logger
        logger.error(f"Ошибка при парсинге параметров URL '{url}':",ex)
        return None

    return None


def get_domain(url: Optional[str]) -> Optional[str]:
    """
    Извлекает схему и доменное имя (без префикса 'www.') из URL.

    Args:
        url (Optional[str]): Входной URL в виде строки или None.

    Returns:
        Optional[str]: Строка вида "схема://домен[:порт]" (например, "https://example.com", "http://sub.test.co.uk:8080")
                       или None, если URL некорректен, пуст или не содержит схемы/домена.

    Example:
        >>> get_scheme_and_domain("https://www.example.com/path/to/page?query=1#fragment")
        'https://example.com'
        >>> get_scheme_and_domain("http://sub.example.co.uk:8080/test")
        'http://sub.example.co.uk:8080'
        >>> get_scheme_and_domain("ftp://example.com")
        'ftp://example.com'
        >>> get_scheme_and_domain("invalid-url")
        None
        >>> get_scheme_and_domain(None)
        None
        >>> get_scheme_and_domain("https://example.com")
        'https://example.com'
    """
    # Объявление переменных
    parsed_url: Any
    netloc: str
    domain_part: str
    base_url: str

    if not url or not isinstance(url, str):
        return None

    try:
        # Парсинг URL на компоненты
        parsed_url = urlparse(url)

        # Проверяем наличие необходимых частей: схемы и сетевого расположения (домена/хоста)
        if not parsed_url.scheme or not parsed_url.netloc:
            # logger.warning(f"Не удалось извлечь схему/домен из URL: {url}") # Опционально: логирование
            return None

        # Получаем сетевое расположение (может включать www. и порт)
        netloc = parsed_url.netloc

        # Удаляем префикс 'www.', если он есть, игнорируя регистр
        if netloc.lower().startswith('www.'):
            domain_part = netloc[4:]
        else:
            domain_part = netloc

        # Собираем итоговый URL из схемы и обработанного домена (с портом, если он был)
        base_url = f'{parsed_url.scheme}://{domain_part}'
        return base_url

    except Exception as ex:
        # Ловим неожиданные ошибки при парсинге
        # В реальном коде используйте ваш logger
        logger.error(f"Неожиданная ошибка при обработке URL '{url}': ",ex)
        return None


def is_url(text: Optional[str]) -> bool:
    """
    Проверяет, является ли переданный текст валидным URL.

    Использует библиотеку `validators`.

    Args:
        text (Optional[str]): Строка для проверки. Может быть None.

    Returns:
        bool: `True` если строка является валидным URL, иначе `False`.

    Example:
        >>> is_url('https://example.com')
        True
        >>> is_url('not a url')
        False
        >>> is_url(None)
        False
    """
    if not text or not isinstance(text, str):
        return False
    # validators.url возвращает ValidationFailure или True
    validation_result = validators.url(text)
    return validation_result is True


def url_shortener(long_url: Optional[str]) -> Optional[str]:
    """
    Сокращает длинный URL с использованием сервиса TinyURL.

    Args:
        long_url (Optional[str]): Длинный URL для сокращения. Может быть None.

    Returns:
        Optional[str]: Сокращённый URL или `None`, если URL невалиден или произошла ошибка запроса.

    Example:
        >>> short = url_shortener('https://www.google.com/search?q=long+query')
        >>> print(short) # Вывод будет вида 'http://tinyurl.com/xxxxxx'
    """
    # Объявление переменных
    url: str
    response: requests.Response

    if not long_url or not is_url(long_url): # Проверяем валидность перед запросом
        print(f'Невалидный URL для сокращения: {long_url}')
        return None

    try:
        url = f'http://tinyurl.com/api-create.php?url={long_url}'
        response = requests.get(url, timeout=10) # Добавлен таймаут

        # Проверка успешности ответа
        if response.status_code == 200:
            return response.text
        else:
            logger.error(f'Ошибка от TinyURL: Статус {response.status_code}, Ответ: {response.text}')
            return None
    except requests.exceptions.RequestException as ex:
        logger.error(f'Ошибка сети при запросе к TinyURL:',ex)
        return None
    except Exception as ex:
        logger.error(f'Неожиданная ошибка при сокращении URL: ',ex)
        return None



def extract_url_params(url: str) -> Dict[str, Union[str, List[str]]]:
    """
    Извлекает параметры запроса из строки URL.

    Args:
        url (str): Строка URL для парсинга.

    Returns:
        Dict[str, Union[str, List[str]]]: Словарь параметров запроса.
            Ключи - имена параметров (str).
            Значения - значения параметров (str, если значение одно; List[str], если значений несколько).
            Возвращает пустой словарь, если параметров нет.

    Raises:
        InvalidURLError: Если входная строка не является валидным URL.

    Example:
        >>> extract_url_params('https://example.com?a=1&b=2&b=3')
        {'a': '1', 'b': ['2', '3']}
        >>> extract_url_params('https://example.com')
        {}
    """
    # Предварительная проверка валидности URL
    if not is_url(url):
        # Можно либо вернуть пустой словарь, либо вызвать исключение
        # raise InvalidURLError(f"Невалидный URL для извлечения параметров: {url}")
        return {} # Возвращаем пустой словарь для невалидных URL

    params_dict: Dict[str, Union[str, List[str]]] = {}
    try:
        parsed_url = urlparse(url)
        # parse_qs всегда возвращает список значений для каждого ключа
        raw_params: Dict[str, List[str]] = parse_qs(parsed_url.query)

        # Преобразуем значения из списка в строку, если параметр имеет только одно значение
        if raw_params:
            params_dict = {k: v[0] if len(v) == 1 else v for k, v in raw_params.items()}
        return params_dict
    except Exception as ex:
        # Логирование или обработка неожиданных ошибок парсинга
        # logger.error(f"Ошибка парсинга URL '{url}' для извлечения параметров.", exc_info=True)
        logger.error(f"[WARN] Ошибка парсинга URL '{url}' для извлечения параметров: ",ex)
        return {} # Возвращаем пустой словарь при ошибке

def is_url(text: Optional[str]) -> bool:
    """
    Проверяет, является ли переданный текст валидным URL.

    Использует библиотеку `validators`. Учитывает различные схемы (http, https, ftp и т.д.).

    Args:
        text (Optional[str]): Строка для проверки.

    Returns:
        bool: `True` если строка является валидным URL, иначе `False`.

    Example:
        >>> is_url('https://google.com')
        True
        >>> is_url('just text')
        False
        >>> is_url(None)
        False
    """
    # Проверка на None и пустую строку
    if not text:
        return False
    # Использование валидатора
    # `validators.url` возвращает True или ValidationFailure (который bool() -> False)
    return bool(validators.url(text))


# def url_shortener(long_url: str) -> Optional[str]:
#     """
#     Сокращает длинный URL с использованием сервиса TinyURL.

#     Args:
#         long_url (str): Длинный URL для сокращения.

#     Returns:
#         Optional[str]: Сокращённый URL или `None`, если произошла ошибка
#                        (невалидный исходный URL, ошибка сети, ошибка сервиса).

#     Raises:
#         InvalidURLError: Если входной `long_url` не является валидным URL.
#         ShorteningError: Если произошла ошибка при взаимодействии с сервисом TinyURL.

#     Example:
#         >>> short = url_shortener('https://www.google.com/search?q=very+long+query')
#         >>> print(short) # Выведет что-то вроде 'http://tinyurl.com/xxxxxxx'
#     """
#     # Проверка валидности исходного URL
#     if not is_url(long_url):
#         # raise InvalidURLError(f"Невалидный URL для сокращения: {long_url}")
#         logger.warning(f"[WARN] Невалидный URL для сокращения: {long_url}")
#         return None

#     # Формирование URL для запроса к API TinyURL
#     api_url: str = f'http://tinyurl.com/api-create.php?url={long_url}'
#     short_url: Optional[str] = None
#     response: Optional[requests.Response] = None # Объявление переменной

#     try:
#         # Выполнение GET-запроса
#         response = requests.get(api_url, timeout=10) # Добавлен таймаут
#         # Проверка успешности ответа
#         response.raise_for_status() # Вызовет HTTPError для плохих статусов (4xx, 5xx)

#         # Проверка, что ответ не пустой и содержит ожидаемый префикс
#         if response.text and response.text.startswith('http'):
#             short_url = response.text
#             return short_url
#         else:
#             # Неожиданный ответ от сервиса
#             # raise ShorteningError(f"TinyURL вернул неожиданный ответ: {response.text}")
#             logger.warning(f"[WARN] TinyURL вернул неожиданный ответ: {response.text}") 


#         # Извлекаем и выводим параметры
#         params: Optional[Dict[str, Any]] = extract_url_params(test_url)
#         if params:
#             print('Параметры URL:')
#             # Используем безопасный доступ к элементам словаря
#             for key, value in params.items():
#                 print(f'  {key}: {value}')
#         else:
#             print('URL не содержит параметров.')

#         # Предлагаем пользователю сократить URL
#         shorten_input: str = input('Хотите сократить этот URL? (y/n): ').strip().lower()
#         if shorten_input == 'y':
#             short_url: Optional[str] = url_shortener(test_url)
#             if short_url:
#                 print(f'Сокращённый URL: {short_url}')
#             else:
#                 print('Ошибка при сокращении URL.')
#     else:
#         print(f'"{test_url}" не является валидным URL.')
