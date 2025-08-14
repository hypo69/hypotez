# # \file /src/utils/string/url.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

"""Module for working with URL lines.
====================================
Provides functions to extract the parameters of the request, check the validity of the URL,
Contractions of links, extracting the basic domain (scheme + domain) and
extracting a "clean" domain name.

Dependencies:
    - Validators (Pip Install Validators)
    - REQUESTS (PIP Install Reques)
    - iPaddress (standard library)

`` `RST
.. Module :: src.utils.string.url
`` `"""

import re # I import re for regular expressions
import ipaddress # To check the IP addresses
from urllib.parse import urlparse, parse_qs, urlunparse, quote, unquote
from typing import Optional, Dict, Any, Union, List
from pathlib import Path
# Forter libraries
import validators
import requests

import header
from src.logger import logger

# --- exceptions ---
class URLError(ValueError):
    """The basic exception for errors associated with the URL in this module."""
    pass
class ShorteningError(URLError):
    """An exception for errors when reducing the URL."""
    pass

# --- Constants ---
# Symbols for rough cleaning from the end of the line
TRAILING_JUNK_CHARS: str = ',";\')\n'
# Regular expression for symbols not allowed in a standard domain name (LDH + DOT)
# Everything that is not a letter, number, hyphen or point will be removed.
INVALID_DOMAIN_CHARS_PATTERN = re.compile(r'[^a-zA-Z0-9.-]+')
# The template to verify that the line consists only of the allowed characters (for final validation)
ALLOWED_DOMAIN_CHARS_ONLY_PATTERN = re.compile(r'^[a-zA-Z0-9.-]+$')


# --- functions of working with URL ---

def extract_url_params(url: Optional[str]) -> Optional[Dict[str, Any]]:
    """Fill the parameter from the query of the URL. (code without change)"""
    # ... (EXTRACT_URL_PARAMS) ...
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
    """Removes NetLOC (host [: port]) from the URL, cleanses of 'www.' and port.
    Previously performs the basic cleaning of the URL line.

    Args:
        URL (Optional [str]): input url.

    Returns:
        Optional [str]: a purified host (for example, "Example.com", "Sub.test.co.uk", "[: 1]")
                       Or None if the host is not found or an error has occurred."""
    # ... (Code of the Get_Domain function from the previous answer, without the final .Lower ()) ...
    # Ads of variables
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
             if '.' in cleaned_url and not any(c in cleaned_url for c in ['/', ':', '?', '# None
                 netloc = cleaned_url; logger.debug(f"Очищенный URL '{cleaned_url}' обработан как прямой домен (netloc).")
        if not netloc: logger.warning(f"Не удалось извлечь netloc из очищенного URL: '{cleaned_url}' (исходный: '{url}')"); return None
        if netloc.lower().startswith('www.'): domain_part = netloc[4:]
        else: domain_part = netloc
        # Return host without a port, but save the register and brackets for IPV6
        return domain_part.split(':', 1)[0]
    except Exception as ex: logger.error(f"Ошибка при обработке очищенного URL '{cleaned_url}' (исходный: '{url}'): {ex}", ex, exc_info=True); return None


def extract_pure_domain(text: Optional[str]) -> Optional[str]:
    """Aggressively extracts a "pure" domain name from a line.

    Tries to get a host with get_domain, then removes all the characters,
    In addition to letters (A-Z, A-Z), numbers (0-9), hyphen (-) and points (.).
    Checks the result for basic validity (not empty, contains a point or 'localhost').
    IP addresses (V4, V6) will be discarded, since they are not "pure" names.

    Args:
        Text (Optional [str]): input line (there may be a URL or just text).

    Returns:
        Optional [Str]: Eliminated and purified domain name in the lower register
                       (for example, "Example.com") or None if the domain could not be extracted.

    Example:
        >>> Extract_pure_domain ("https://wwww.example.com:80/path?q=1")
        'Example.com'
        >>> Extract_pure_domain ("Sub.domain-test.co.uk")
        'sub.domain-test.co.uk'
        >>> extract_pure_domain ("exa_mple.com") # Emphasizing will be deleted
        'Example.com'
        >>> Extract_pure_domain ("test..com") # double points will remain (simple cleaning)
        'test..com'
        >>> Extract_pure_domain ('https: // ass_ured, automa (tion) .com)') # a lot of garbage
        'assurodomation.com'
        >>> Extract_pure_domain ("http://192.168.1/page") # IP v4
        None
        >>> Extract_pure_domain ("http: // [:: 1]: 80") # IP v6
        None
        >>> Extract_pure_domain ("Localhost")
        'Localhost'
        >>> Extract_pure_domain ("Just Text")
        None
        >>> Extract_pure_domain (None)
        None"""
    # Ads of variables
    hostname: Optional[str] = None
    cleaned_domain: str
    final_domain: str

    if not text or not isinstance(text, str):
        return None

    # 1. We get a host using get_domain (it will perform basic cleaning and extract NetLOC)
    hostname = get_domain(text) # Get_Domain returns a host without a port and www.

    if not hostname:
        # Get_Domain could not extract a host
        return None

    # 2. Check, is the extracted host IP address
    try:
        # ipaddress.ip_address () will throw away Valueerror, if this is not a valid IP
        _ = ipaddress.ip_address(hostname)
        # If we are here, then this is an IP address. We discard it.
        logger.debug(f"Извлеченный хост '{hostname}' является IP-адресом, Пропуск.")
        return None
    except ValueError:
        # This is not an IP address, we continue to process as a potential domain
        pass
    except Exception as ip_ex:
        # We catch other rare errors from iPaddress
        logger.error(f"Ошибка при проверке IP для хоста '{hostname}': {ip_ex}", exc_info=True)
        # Just in case, interrupt the processing, because not sure of
        return None

    # 3. Aggressive cleaning: delete all unacceptable characters
    try:
        # We delete everything that is not a letter, not a figure, not a hyphen and not a point
        cleaned_domain = INVALID_DOMAIN_CHARS_PATTERN.sub('', hostname)
    except Exception as regex_ex:
        logger.error(f"Ошибка regex при очистке хоста '{hostname}': {regex_ex}", exc_info=True)
        return None

    # 4. Final sanitation and validation
    # We delete possible definitions/points from the beginning/end that arose after cleaning
    final_domain = cleaned_domain.strip('.-')

    # Check that the result is not empty and looks like a domain
    if not final_domain:
        logger.debug(f"Результат после очистки хоста '{hostname}' пуст.")
        return None

    # The domain (except Localhost) should contain at least one point
    # and consist only of permitted characters (additional check after regex)
    is_localhost = final_domain.lower() == 'localhost'
    contains_dot = '.' in final_domain
    is_valid_chars = bool(ALLOWED_DOMAIN_CHARS_ONLY_PATTERN.match(final_domain))

    if not is_valid_chars:
         logger.warning(f"Результат '{final_domain}' после очистки хоста '{hostname}' содержит недопустимые символы (ошибка regex?).")
         return None

    if not is_localhost and not contains_dot:
        logger.warning(f"Результат '{final_domain}' после очистки хоста '{hostname}' не является 'localhost' и не содержит точку.")
        return None

    # 5. Return result in the lower register
    return final_domain.lower()

# A list of frequently found file extensions that are usually not web pages.
# It can be used as the basis for the Excluded_Extensions parameter.
# This list is not used directly by a function, but serves as reference information.
COMMON_NON_HTML_EXTENSIONS: List[str] = [
    # Documents
    'pdf', 'doc', 'docx', 'odt', 'rtf', 'txt', 'tex', 'wpd',
    'xls', 'xlsx', 'ods', 'csv',
    'ppt', 'pptx', 'odp',
    # Images
    'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'tif', 'svg', 'webp', 'ico',
    # Archives
    'zip', 'rar', '7z', 'tar', 'gz', 'bz2', 'xz', 'iso', 'dmg',
    # Audio
    'mp3', 'wav', 'ogg', 'aac', 'flac', 'm4a',
    # Video
    'mp4', 'mkv', 'avi', 'mov', 'wmv', 'flv', 'webm',
    # Executable files and installers
    'exe', 'msi', 'apk', 'bat', 'sh', 'com', 'jar', 'pkg',
    # Fonts
    'woff', 'woff2', 'ttf', 'otf', 'eot',
    # Other
    'ics', 'vcf', 'xml', # XML can be a page, but often it is data
    'json', # Analogous XML
    'rss', 'atom',
    'psd', 'ai', 'eps', # Graphic formats of source
    'sql', 'db', 'mdb', # Database files
    'torrent', 'swf', 'fla', # Flash (outdated)
]


def normalize_url(
    url: str | None,
    default_scheme: str = 'http',
    excluded_extensions: Optional[List[str]] = None
) -> str | None:
    """It normalizes the URL, leading it to a more standard form.

    The main steps of normalization:
    1. Removes the initial/final gaps.
    2. It cleanses of "garbage" characters (gaps, quotes, commas), if they are located
       Immediately in front of the path component ('/'), request ('?'), fragment ('# None
       Or at the end of the URL.
    3. Adds the default circuit (http/https), if it is absent.
    4. Curses the scheme and the domain (NetLOC) to the lower register.
    5. Processes Internationalized Domain Names (IDN), encoding NetLOC in Punycode.
    6. Replaces multiple slas on the way to one.
    7. guarantees that the path begins with '/', if there is a domain.
    8. Removes standard ports (80 for HTTP, 443 for HTTPS).
    9. removes the fragment ('# sSction').
    10. transcodes the path and request parameters for correctness,
        Removing garbage symbols from the end of the decoded paths/parameters.
    11. (Optionally) If the list is `Excluded_Extens`, the URL is cut to the directory containing it,
        If the extension of the file on the way is included in this list. Files without extension
        Or the URL indicating the directory (ending on '/') are not affected by this filtration.

    Args:
        URL (str | none): input URL for normalization.
        Default_Scheme (str): default circuit ('http' or 'https'), added if the scheme is absent.
                              By default 'http'.
        Excluded_EXTensions (Optional [List [str]], Optional): List of excluded file extensions
            (for example, ['pdf', 'jpg', 'zip']). Expansion should be indicated without a point.
            If the extension of the file in the URL is included in this list, the URL will be circumcised to the directory containing it.
            If NONE or an empty list, filtering on extensions is not used. By default None.
            Examples of frequently excluded extensions can be found in `Common_NON_HTML_EXTensions`.

    Returns:
        Str | None: normalized URL or None if the input URL is incorrect
                       Or cannot be successfully disassembled/normalized.

    Example:
        >>> Normalize_url ("http://www.example.com:80/path//to/page?q=1&b=2# Section")
        'http://www.example.com/path/to/page?q=1&b=2'
        >>> normalize_url ("www.example.com/path")
        'http://www.example.com/path'
        >>> normalize_url ("https://toscrape.com:443")
        'https://toscrape.com//'
        >>> Normalize_url (None)
        None
        >>> normalize_url ("http: // example.rf/put")
        'http: //xn--e1afmkfd.xn--p1ai/%D0%BF%D1%83%D1%82%D1%8C'
        >>> normalize_url ("http://example.com/path/file.pdf", excluded_EXTensions = ['pdf', 'jpg'])
        'http://example.com/path/'
        >>> normalize_url ("http://example.com/path/image.jpg", excluded_extensions = ['pdf', 'jpg'])
        'http://example.com/path/'
        >>> normalize_url ("http://example.com/archive.zip", excloud_extensions = ['zip', 'rar'])
        'http://example.com/'
        >>> normalize_url ("http://example.com/page.html", excluded_extensions = ['pdf', 'jpg'])
        'http://example.com/page.html'
        >>> normalize_url ("http://example.com/product", excloud_extensions = ['pdf']) # file without extension, is not filtered
        'http://example.com/product'
        >>> normalize_url ("http://example.com/some.folder/", excluded_EXTensions = ['pdf']) # Directory, not filtered
        'http://example.com/some.folder/'
        >>> normalize_url ("http://example.com/file.pdf", excluded_Extensions = ['. PDF']) # with a point in Excluded_EXTensions
        'http://example.com/'
        >>> normalize_url ("http://example.com/downloads/document.docx", excluded_EXTensions = comon_NON_HTML_EXTENSIONS)
        'http://example.com/downloads/'"""
    # Ads of variables
    original_url_for_log: str = ''
    processed_url: str = ''
    parsed_parts: ParseResult | None = None
    
    scheme_norm: str = ''
    netloc_norm: str = ''
    netloc_raw: str = ''
    path_norm: str = ''
    path_raw: str = ''
    path_intermediate: str = ''
    decoded_path: str = ''
    cleaned_decoded_path: str = ''
    path_fallback: str = '' # Used for errors of path processing
    params_norm: str = ''
    query_norm: str = ''
    query_raw: str = ''
    decoded_query: str = ''
    cleaned_decoded_query: str = ''
    fragment_norm: str = '' # The fragment is always removed

    # Variables for filtering extensions
    normalized_excluded_extensions: List[str] = []
    p_path: Path
    filename_from_path: str = ''
    file_suffix_from_path: str = ''
    parent_dir_of_path: Path

    if not url or not isinstance(url, str):
        return None

    original_url_for_log = url # Preservation of the original URL for logging
    
    # 1. Removing the initial/final gaps
    processed_url = url.strip()
    if not processed_url: # Check for an empty line after Strip
        return None

    # 2. Preliminary cleaning of garbage characters
    # The function removes symbols such as gaps, quotes, commas, if they are
    # Immediately in front of the path component ('/'), request ('?'), fragment ('#') or at the end of the URL.
    processed_url = re.sub(r'[\s\'",]+(?=([/?# ]|$))', '', processed_url)
    if not processed_url: # Check if the line of empty after cleaning
        return None

    # 3. Adding a default scheme
    if '://' not in processed_url and not processed_url.startswith('//'):
        # The use of heuristics to determine whether to add a scheme
        if ('.' in processed_url or processed_url.lower() == 'localhost') and \
           not re.match(r'^[a-zA-Z]:\\', processed_url): # Checking whether Windows is local
             logger.debug(f"URL-адрес '{original_url_for_log}' не содержит схему. Функция добавляет схему по умолчанию '{default_scheme}://'.")
             processed_url = default_scheme + '://' + processed_url
        else:
            logger.warning(
                f"Строка '{original_url_for_log}' не содержит схему и не выглядит как URL-адрес "
                f"для добавления схемы по умолчанию. Нормализация невозможна.",
                None,
                False
            )
            return None # Completion of normalization, if it is impossible to determine the scheme

    # 4. Parsing URL
    try:
        # URL analysis of components using urlparse
        parsed_parts = urlparse(processed_url)
    except ValueError as ex: # Parsing's specific error interception
        logger.error(f"Ошибка при разборе URL-адреса '{processed_url}'.", ex, exc_info=True)
        return None

    # 5. Validation of basic components
    if not parsed_parts.scheme: # Checking for the presence of a diagram
        logger.warning(f"URL-адрес '{processed_url}' после разбора не содержит схему. Нормализация невозможна.", None, False)
        return None
    
    # Verification (NETLOC) for common schemes
    if not parsed_parts.netloc and parsed_parts.scheme.lower() not in ('file', 'mailto', 'data', 'javascript', 'tel', 'sms', 'urn'):
        logger.warning(
            f"URL-адрес '{processed_url}' (схема: {parsed_parts.scheme}) после разбора не содержит сетевое "
            f"расположение (netloc), что нехарактерно для данной схемы. Нормализация невозможна.",
            None,
            False
        )
        return None

    # 6. Normalization of components
    scheme_norm = parsed_parts.scheme.lower()
    netloc_raw = parsed_parts.netloc # Preservation of the initial NetLOC for IDN
    
    if netloc_raw:
        # IDN-processing (Internationalized Domain Names)
        try:
            hostname_parts: List[str] = netloc_raw.split(':', 1)
            domain_part: str = hostname_parts[0]
            port_part: str = f":{hostname_parts[1]}" if len(hostname_parts) > 1 else ""
            
            # The function encodes the domain part in IDNA (PunyCode), then decodes in ASCII and leads to the lower register
            normalized_domain: str = domain_part.encode('idna').decode('ascii')
            netloc_norm = normalized_domain.lower() + port_part

        except UnicodeError as ex_idn_unicode: # IDN coding error
            logger.warning(f"Ошибка IDN кодирования для netloc: '{netloc_raw}'. Используется netloc.lower().", ex_idn_unicode, False)
            netloc_norm = netloc_raw.lower() # Spare option: just bringing to the lower register
        except Exception as ex_idn_general: # Other unexpected IDN mistakes
             logger.error(f"Неожиданная ошибка при обработке IDN для netloc '{netloc_raw}'.", ex_idn_general, exc_info=True)
             netloc_norm = netloc_raw.lower() # Spare option

        # Removing standard ports (80 for HTTP, 443 for https)
        if (scheme_norm == 'http' and netloc_norm.endswith(':80')) or \
           (scheme_norm == 'https' and netloc_norm.endswith(':443')):
            netloc_norm = netloc_norm.rsplit(':', 1)[0]
    else:
        netloc_norm = '' # NetLOC remains empty if it was not

    # --- path processing (PATH) ---
    path_raw = parsed_parts.path # The original path from a disassembled url
    if path_raw:
        # 1. Normalization of multiple slashes (e.g. // to ->/path/to)
        path_intermediate = re.sub(r'/+', '/', path_raw)
        
        # 2. Decoding, cleaning of garbage characters at the end, re -encoding
        try:
            decoded_path = unquote(path_intermediate) # Decoding %XX sequences
            # The function removes garbage symbols [\ s \ '", from the end of the decoded path
            cleaned_decoded_path = re.sub(r'[\s\'",]+$', '', decoded_path)
            path_norm = quote(cleaned_decoded_path, safe='/%:@') # Coding back, preserving safe characters
        except Exception as ex_path_proc: # Way error
            logger.warning(
                f"Ошибка при полной обработке пути для '{path_raw}': {ex_path_proc}. "
                f"Применяется только нормализация слешей и стандартное кодирование.", ex_path_proc, False
            )
            # Spare option: only normalization of slashes and standard coding
            path_fallback = re.sub(r'/+', '/', path_raw)
            try:
                path_norm = quote(path_fallback, safe='/%:@')
            except Exception as ex_path_fallback_quote: # A critical error of coding
                logger.error(f"Критическая ошибка при кодировании пути '{path_fallback}' в запасном варианте.", ex_path_fallback_quote, exc_info=True)
                path_norm = path_fallback # In extreme cases, a partially processed path is used
    elif netloc_norm: # If there is a domain, but there is no way, the root path is set '/'
        path_norm = '/'
    # Else: Path_norm left, if there is neither NetLOC nor Path_RAW (for example, "Mailto: user@example.com")


    # --- filtering on the excluded extension of files ---
    if excluded_extensions and path_norm: # The use of the filter, if there are excluded extensions and the path
        # Normalization of the list of excluded extensions (lower register, removal of the starting point)
        normalized_excluded_extensions = [
            ext.lower().lstrip('.') for ext in excluded_extensions if isinstance(ext, str)
        ]

        if normalized_excluded_extensions: # Continuation only if the extension list is not empty after cleaning
            p_path = Path(path_norm.strip('/')) # We remove the final slash, if any, for the correct Path.name
            
            # Extracting a file name or last track component
            # For the path type "/foo/bar/", Path (Path_norm) .name will be "bar", and Path (Path_norm.strip ('/')). Name will be "bar"
            # For "/foo/file.txt", Path (Path_norm) .name will be "File.txt"
            # For "/", path (path_norm.strip ('/')). Name will be "" "(empty line)
            filename_from_path = p_path.name 
            
            # Extracting the extension from the file name (without a point, in the lower register)
            # An empty extension if the file name is empty or not a point.
            if filename_from_path and '.' in filename_from_path:
                file_suffix_from_path = filename_from_path.split('.')[-1].lower()
            else:
                file_suffix_from_path = ''

            if file_suffix_from_path and file_suffix_from_path in normalized_excluded_extensions:
                # If the file extension exists and is included in the list of excluded,
                # URL is cut to the parent directory of the file.
                parent_dir_of_path = p_path.parent
                
                # Determination of the new Path_norm based on the parent directory
                if str(parent_dir_of_path) == '.': 
                    # The source path was a relative file in the root of the type 'File.ext' (after urlparse it will be /file.ext)
                    # Or something like 'foo/file.ext', where P_Path.pAnd will be 'foo'
                    # If there is a NetLOC, then there must be an absolute path that begins with /
                    path_norm = '/'
                elif str(parent_dir_of_path) == '/': 
                    # The initial path was the absolute file in the root, such as '/file.ext'
                    path_norm = '/' # Root
                else: # The initial path was the type '/dir/file.ext' or 'Dir/File.ext'
                    path_norm = parent_dir_of_path.as_posix() + '/' # The path to the Directory with the final '/'
                
                # We guarantee that the path begins with '/', if there is a domain and the path is not empty
                if netloc_norm and path_norm and not path_norm.startswith('/'):
                    path_norm = '/' + path_norm
                
                # And once again we normalize the slash, because P_Path.as_POSIX () could return something without the initial slash if P_PATH was relative.
                path_norm = re.sub(r'/+', '/', path_norm)


                logger.debug(
                    f"URL-путь для '{original_url_for_log}' был сокращен до '{path_norm}' "
                    f"из-за исключенного расширения '{file_suffix_from_path}'."
                )

    # --- processing of request parameters (Query) ---
    query_raw = parsed_parts.query # The initial parameters of the request
    if query_raw:
        try:
            decoded_query = unquote(query_raw) # Decoding parameters
            # The function removes garbage symbols [\ s \ '", from the end of the decoded parameters
            cleaned_decoded_query = re.sub(r'[\s\'",]+$', '', decoded_query)
            query_norm = quote(cleaned_decoded_query, safe='/?!@# $ & ()*+,; =:%') # Coding back
        except Exception as ex_query_proc: # Error when processing request parameters
            logger.warning(
                f"Ошибка при полной обработке параметров запроса для '{query_raw}': {ex_query_proc}. "
                f"Применяется стандартное кодирование исходных параметров.", ex_query_proc, False
            )
            # Spare option: standard coding of the source parameters
            try:
                query_norm = quote(query_raw, safe='/?!@# None
            except Exception as ex_query_fallback_quote: # A critical error of coding
                logger.error(f"Критическая ошибка при кодировании параметров запроса '{query_raw}' в запасном варианте.", ex_query_fallback_quote, exc_info=True)
                query_norm = query_raw # In extreme cases, the initial parameters are used
    # Else: query_norm left ''

    fragment_norm = '' # Removing the fragment ('#sSction') according to step 9
    params_norm = parsed_parts.params # The component Params (for Matrix Uris) remains unchanged

    # 7. Assembly of a normalized URL
    try:
        # Assembly URL from normalized components
        normalized_url_result: str = urlunparse((scheme_norm, netloc_norm, path_norm, params_norm, query_norm, fragment_norm))
    except Exception as ex_unparse: # Error when assembling url
        logger.error(
            f"Ошибка при сборке URL-адреса из компонентов: "
            f"{(scheme_norm, netloc_norm, path_norm, params_norm, query_norm, fragment_norm)}",
            ex_unparse, exc_info=True
        )
        return None # None return in case of assembly error

    return normalized_url_result


def is_url(text: Optional[str]) -> bool:
    """Checks whether the transmitted text is valid URL. (code without changes)"""
    # ... (Code of the function is_url) ...
    validation_result: Any
    if not text or not isinstance(text, str): return False
    try: validation_result = validators.url(text); return bool(validation_result)
    except Exception as ex: logger.error(f"Ошибка при вызове validators.url для текста '{text}': {ex}", ex, exc_info=True); return False

def url_shortener(long_url: Optional[str]) -> Optional[str]:
    """Reduces a long URL using the TinyURL service. (code without changes)"""
    # ... (Code of the function url_shortener) ...
    url: str; response: requests.Response
    if not long_url or not is_url(long_url): logger.warning(f'Невалидный URL для сокращения: {long_url}'); return None
    try:
        url = f'http://tinyurl.com/api-create.php?url={long_url}'; response = requests.get(url, timeout=10)
        response.raise_for_status(); return response.text
    except requests.exceptions.RequestException as ex: logger.error(f'Ошибка сети при запросе к TinyURL для URL {long_url}: {ex}', ex, exc_info=True); return None
    except Exception as ex: logger.error(f'Неожиданная ошибка при сокращении URL {long_url}: {ex}', ex, exc_info=True); return None


if __name__ == "__main__":
    # --- examples of use ---
    urls_to_test = [
        "https://www.Example.com:80/path?q=1",
        " sub.domain-test.co.uk ",
        "exa_mple.com", # The emphasis will be deleted
        "test..com", # Double points will remain
        'https://ass_ured,automa(tion).com)', # A lot of garbage
        "http://192.168.1.1/page", # IP v4
        "http://[::1]:80", # IP v6
        "localhost",
        " just text ",
        None,
        "www.Valid-Domain.INFO",
        "-invalid-.com", # Will be cleared to invalid.com
        ".anotherinvalid.", # Will be cleared to Anotherinvalid
        "singlelabel",
        "https://www.xn--e1aybc.xn--p1ai/path" # IDN Punycode
    ]

    print("\n--- Тестирование extract_pure_domain ---")
    for test_url in urls_to_test:
        result = extract_pure_domain(test_url)
        print(f"Input: {repr(test_url):<40} -> Output: {result}")

    # --- Assertes ---
    assert extract_pure_domain("https://www.Example.com:80/path?q=1") == 'example.com'
    assert extract_pure_domain(" sub.domain-test.co.uk ") == 'sub.domain-test.co.uk'
    assert extract_pure_domain("exa_mple.com") == 'example.com'

    # Assert Extract_Pure_Domain ("Test..com") == 'Test.com' # Expected behavior? Cleaning does not remove double points
    assert extract_pure_domain('https://ass_ured,automa(tion).com)') == 'assuredautomation.com'
    assert extract_pure_domain("http://192.168.1.1/page") is None
    assert extract_pure_domain("http://[::1]:80") is None
    assert extract_pure_domain("localhost") == 'localhost'
    assert extract_pure_domain(" just text ") is None
    assert extract_pure_domain(None) is None
    assert extract_pure_domain("www.Valid-Domain.INFO") == 'valid-domain.info'
    assert extract_pure_domain("-invalid-.com") == 'invalid.com' # Strip ('.-') will work
    assert extract_pure_domain(".anotherinvalid.") == 'anotherinvalid' # Strip ('.-') will work, but there is no point inside
    assert extract_pure_domain("singlelabel") is None # There is no point
    assert extract_pure_domain("https://www.xn--e1aybc.xn--p1ai/path") == 'xn--e1aybc.xn--p1ai' # PunyCode IDN (contains a hyphen)

    print("\nАссерты для extract_pure_domain пройдены (с учетом ожиданий).")

    # -----------------
    urls_to_test = [
    "  HTTP://Www.Example.Com:80/path//to/page?q=1&b=2# section  ",
    "www.example.com/path",
    "https://toscrape.com/:443",
    "example.com",
    "ftp://Example.Com/File",
    "invalid-url",
    "http://пример.рф/путь?параметр=значение# fragment",
    # Domain (IDN): Examples.rf is transformed into punycode (xn--e1afmkfd.xn-p1ai).
    # Way, parameters, fragment: symbols not from Ascii (for example, the path, parameter, meaning, fragment)
    # The percentage coding (percent -encoding) is converted. For example, /the path will become /%D0%BF%D1%83%D1%82%D1%8C.
    
    "https://www.11st.co.kr/products/1122334455,\"",
    "//cdn.example.com/script.js", # Protocol-RELATIVE URL (will become http)
    "mailto:user@example.com", # It will not change, because No NetLOC according to the rules above
    "http://user:pass@example.com/", # Save user: pass
    "http://example.com/%7Euser/", # Save the %coding
    "http://example.com/a%20b?c=d%26e", # Transcodes the gap and ampersand
    None,
    "",
    "   ",
    "http://[::1]:8080/path" # IPV6
    ]

    print("--- Тестирование normalize_url ---")

    # Examples from the docstring for testing
    test_cases = [
        ("  HTTP://Www.Example.Com:80/path//to/page?q=1&b=2# section  ", 'http://www.example.com/path/to/page?q=1&b=2'),
        ("www.example.com/path", 'http://www.example.com/path'),
        ("https://toscrape.com/:443", 'https://toscrape.com//'),
        ("example.com", 'http://example.com/'),
        ("ftp://example.com/file", 'ftp://example.com/file'), # Other schemes are preserved
        ("invalid-url", None), # Not like url
        ("http://пример.рф/путь", 'http://xn--e1afmkfd.xn--p1ai/%D0%BF%D1%83%D1%82%D1%8C'), # IDN handling
        ('https://www.11st.co.kr/products/1122334455,"', 'https://www.11st.co.kr/products/1122334455'), # Drive cleaning
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

