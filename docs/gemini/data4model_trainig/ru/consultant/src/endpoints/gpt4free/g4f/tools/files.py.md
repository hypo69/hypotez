### **Анализ кода модуля `files.py`**

#### **Качество кода**:

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код разбит на множество функций, что облегчает понимание и поддержку.
    - Используются аннотации типов.
    - Обработка исключений присутствует.
- **Минусы**:
    - Многочисленные блоки `try...except` без логирования ошибок.
    - Смешанный стиль: где-то используется `os.path.join`, а где-то `/` для работы с путями.
    - Не все функции документированы.
    - Присутствуют конструкции `try...except` без указания конкретного типа исключения.
    - Многие функции содержат в себе много логики, что снижает их читаемость и усложняет поддержку.
    - Отсутствует логирование, необходимо использовать `logger` из `src.logger`.
    - В некоторых местах используется небезопасное открытие файлов без указания кодировки.
    - В некоторых функциях отсутствует аннотация типов для возвращаемого значения.

#### **Рекомендации по улучшению**:

1.  **Документирование**:
    - Добавить docstring для всех функций и классов, включая описание параметров, возвращаемых значений и возможных исключений.
2.  **Логирование**:
    - Добавить логирование во все блоки `try...except` с использованием `logger.error`.
3.  **Обработка исключений**:
    - Указывать конкретные типы исключений в блоках `except`, чтобы избежать перехвата нежелательных исключений.
4.  **Унификация работы с путями**:
    - Использовать `pathlib.Path` вместо `os.path.join` для единообразия и удобства.
5.  **Разделение ответственности**:
    - Разбить крупные функции на более мелкие, чтобы каждая выполняла одну конкретную задачу.
6.  **Кодировка файлов**:
    - При открытии файлов всегда указывать кодировку `encoding='utf-8'`.
7.  **Аннотации типов**:
    - Добавить аннотации типов для всех переменных и возвращаемых значений функций, где они отсутствуют.
8.  **Удалить неиспользуемые импорты**
9.  **Удалить импорты, которые уже есть в `requirements.txt`**
10. **Использовать `j_loads` или `j_loads_ns` для чтения JSON или конфигурационных файлов**

#### **Оптимизированный код**:

```python
from __future__ import annotations

import re
import os
import json
import hashlib
import base64
import time
import zipfile
import asyncio
import urllib.parse
from urllib.parse import unquote
from pathlib import Path
from typing import Iterator, Optional, AsyncIterator, List

import aiohttp
import pandas as pd
from bs4 import BeautifulSoup

from src.logger import logger # Добавлен импорт logger
from .web_search import scrape_text
from ..cookies import get_cookies_dir
from ..image import is_allowed_extension
from ..requests.aiohttp import get_connector
from ..providers.asyncio import to_sync_generator
from ..errors import MissingRequirementsError

# Константы для расширений файлов и имен файлов
PLAIN_FILE_EXTENSIONS: List[str] = ['txt', 'xml', 'json', 'js', 'har', 'sh', 'py', 'php', 'css', 'yaml', 'sql', 'log', 'csv', 'twig', 'md', 'arc']
PLAIN_CACHE: str = 'plain.cache'
DOWNLOADS_FILE: str = 'downloads.json'
FILE_LIST: str = 'files.txt'

def secure_filename(filename: str) -> str | None:
    """
    Очищает имя файла, удаляя небезопасные символы.

    Args:
        filename (str): Исходное имя файла.

    Returns:
        str | None: Очищенное имя файла или None, если filename равен None.
    """
    if filename is None:
        return None

    # Keep letters, numbers, basic punctuation and all Unicode chars
    filename = re.sub(r'[^\w.,_+-]+', '_', unquote(filename).strip(), flags=re.UNICODE)
    filename = filename[:100].strip('.,_-+')
    return filename

def supports_filename(filename: str) -> bool:
    """
    Проверяет, поддерживается ли данный тип файла для обработки.

    Args:
        filename (str): Имя файла.

    Returns:
        bool: True, если файл поддерживается, иначе False.

    Raises:
        MissingRequirementsError: Если отсутствуют необходимые зависимости.
    """
    if filename.endswith('.pdf'):
        try:
            import PyPDF2
            return True
        except ImportError:
            try:
                import pdfplumber
                return True
            except ImportError:
                try:
                    from pdfminer.high_level import extract_text
                    return True
                except ImportError:
                    msg = 'Install "pypdf2" requirements | pip install -U g4f[files]'
                    raise MissingRequirementsError(msg) from None

    elif filename.endswith('.docx'):
        try:
            from docx import Document
            return True
        except ImportError:
            try:
                import docx2txt
                return True
            except ImportError:
                msg = 'Install "docx" requirements | pip install -U g4f[files]'
                raise MissingRequirementsError(msg) from None

    elif filename.endswith('.odt'):
        try:
            from odf.opendocument import load
            return True
        except ImportError:
            pass

    elif filename.endswith('.epub'):
        try:
            import ebooklib
            return True
        except ImportError:
            pass

    elif filename.endswith('.xlsx'):
        try:
            import pandas as pd
            return True
        except ImportError:
            pass

    elif filename.endswith('.html'):
        try:
            from bs4 import BeautifulSoup
            return True
        except ImportError:
            msg = 'Install "beautifulsoup4" requirements | pip install -U g4f[files]'
            raise MissingRequirementsError(msg) from None

    elif filename.endswith('.zip'):
        return True

    elif filename.endswith('package-lock.json') and filename != FILE_LIST:
        return False

    else:
        extension = os.path.splitext(filename)[1][1:]
        if extension in PLAIN_FILE_EXTENSIONS:
            return True

    return False

def get_bucket_dir(*parts: str) -> str:
    """
    Формирует путь к каталогу bucket на основе переданных частей.

    Args:
        *parts (str): Части пути для объединения.

    Returns:
        str: Полный путь к каталогу bucket.
    """
    secure_parts = [secure_filename(part) for part in parts if part]
    return os.path.join(get_cookies_dir(), 'buckets', *secure_parts)

def get_buckets() -> Optional[List[str]]:
    """
    Получает список директорий bucket.

    Returns:
        Optional[List[str]]: Список имен директорий или None в случае ошибки.
    """
    buckets_dir = os.path.join(get_cookies_dir(), 'buckets')
    try:
        return [d for d in os.listdir(buckets_dir) if os.path.isdir(os.path.join(buckets_dir, d))]
    except OSError as ex:
        logger.error('Error while listing buckets directory', ex, exc_info=True)
        return None

def spacy_refine_chunks(source_iterator: Iterator[str]) -> Iterator[str]:
    """
    Обрабатывает текст с использованием spaCy для извлечения значимых фрагментов.

    Args:
        source_iterator (Iterator[str]): Итератор по текстовым фрагментам.

    Yields:
        str: Извлеченные фрагменты текста.

    Raises:
        MissingRequirementsError: Если библиотека spaCy не установлена.
    """
    try:
        import spacy
    except ImportError:
        msg = 'Install "spacy" requirements | pip install -U g4f[files]'
        raise MissingRequirementsError(msg) from None

    nlp = spacy.load('en_core_web_sm')
    for page in source_iterator:
        doc = nlp(page)
        sentences = list(doc.sents)
        summary = sorted(sentences, key=lambda x: len(x.text), reverse=True)[:2]
        for sent in summary:
            yield sent.text

def get_filenames(bucket_dir: Path) -> List[str]:
    """
    Получает список имен файлов из файла FILE_LIST в указанной директории.

    Args:
        bucket_dir (Path): Директория bucket.

    Returns:
        List[str]: Список имен файлов.
    """
    files = bucket_dir / FILE_LIST
    if files.exists():
        try:
            with files.open('r', encoding='utf-8') as f:
                return [filename.strip() for filename in f.readlines()]
        except Exception as ex:
            logger.error('Error while reading file list', ex, exc_info=True)
            return []
    return []

def stream_read_files(bucket_dir: Path, filenames: List[str], delete_files: bool = False) -> Iterator[str]:
    """
    Поточно считывает содержимое файлов из указанной директории.

    Args:
        bucket_dir (Path): Директория bucket.
        filenames (List[str]): Список имен файлов для чтения.
        delete_files (bool, optional): Удалять ли файлы после чтения. По умолчанию False.

    Yields:
        str: Содержимое файлов.
    """
    for filename in filenames:
        file_path: Path = bucket_dir / filename
        if not file_path.exists() or file_path.lstat().st_size <= 0:
            continue

        extension = os.path.splitext(filename)[1][1:]

        if filename.endswith('.zip'):
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(bucket_dir)
                    yield from stream_read_files(bucket_dir, [f for f in zip_ref.namelist() if supports_filename(f)], delete_files)
            except zipfile.BadZipFile as ex:
                logger.error(f'Error while processing zip file {filename}', ex, exc_info=True)
            finally:
                if delete_files:
                    for unlink in zip_ref.namelist()[::-1]:
                        filepath = os.path.join(bucket_dir, unlink)
                        if os.path.exists(filepath):
                            try:
                                if os.path.isdir(filepath):
                                    os.rmdir(filepath)
                                else:
                                    os.unlink(filepath)
                            except OSError as ex:
                                logger.error(f'Error while deleting file {filepath}', ex, exc_info=True)
            continue

        yield f'```{filename}\\n'

        try:
            if filename.endswith('.pdf'):
                try:
                    import PyPDF2
                    reader = PyPDF2.PdfReader(file_path)
                    for page_num in range(len(reader.pages)):
                        page = reader.pages[page_num]
                        yield page.extract_text()
                except (PyPDF2.errors.PdfReadError, ImportError) as ex:
                    logger.error(f'Error while processing pdf file {filename}', ex, exc_info=True)
                    continue
            elif filename.endswith('.docx'):
                try:
                    from docx import Document
                    doc = Document(file_path)
                    for para in doc.paragraphs:
                        yield para.text
                except ImportError:
                    try:
                        import docx2txt
                        yield docx2txt.process(file_path)
                    except Exception as ex:
                        logger.error(f'Error while processing docx file {filename}', ex, exc_info=True)
            elif filename.endswith('.odt'):
                try:
                    from odf.opendocument import load
                    textdoc = load(file_path)
                    allparas = textdoc.getElementsByType(odf.text.P)
                    for p in allparas:
                        yield p.firstChild.data if p.firstChild else ''
                except ImportError as ex:
                    logger.error(f'Error while processing odt file {filename}', ex, exc_info=True)
            elif filename.endswith('.epub'):
                try:
                    import ebooklib
                    book = ebooklib.epub.read_epub(file_path)
                    for doc_item in book.get_items():
                        if doc_item.get_type() == ebooklib.ITEM_DOCUMENT:
                            yield doc_item.get_content().decode(errors='ignore')
                except Exception as ex:
                    logger.error(f'Error while processing epub file {filename}', ex, exc_info=True)
            elif filename.endswith('.xlsx'):
                try:
                    import pandas as pd
                    df = pd.read_excel(file_path)
                    for row in df.itertuples(index=False):
                        yield ' '.join(str(cell) for cell in row)
                except Exception as ex:
                    logger.error(f'Error while processing xlsx file {filename}', ex, exc_info=True)
            elif filename.endswith('.html'):
                try:
                    from bs4 import BeautifulSoup
                    yield from scrape_text(Path(file_path).read_text(encoding='utf-8', errors='ignore'))
                except Exception as ex:
                    logger.error(f'Error while processing html file {filename}', ex, exc_info=True)
            elif extension in PLAIN_FILE_EXTENSIONS:
                yield Path(file_path).read_text(encoding='utf-8', errors='ignore')
        except Exception as ex:
            logger.error(f'Error while reading file {filename}', ex, exc_info=True)
        yield '\\n```\\n\\n'

def cache_stream(stream: Iterator[str], bucket_dir: Path) -> Iterator[str]:
    """
    Кэширует поток данных в файл.

    Args:
        stream (Iterator[str]): Поток данных для кэширования.
        bucket_dir (Path): Директория bucket.

    Yields:
        str: Фрагменты данных из потока.
    """
    cache_file = bucket_dir / PLAIN_CACHE
    tmp_file = bucket_dir / f'{PLAIN_CACHE}.{time.time()}.tmp'

    if cache_file.exists():
        try:
            for chunk in read_path_chunked(cache_file):
                yield chunk
            return
        except Exception as ex:
            logger.error('Error while reading cache file', ex, exc_info=True)

    try:
        with open(tmp_file, 'wb') as f:
            for chunk in stream:
                f.write(chunk.encode(errors='replace'))
                yield chunk
        tmp_file.rename(cache_file)
    except Exception as ex:
        logger.error('Error while caching stream', ex, exc_info=True)

def is_complete(data: str) -> bool:
    """
    Проверяет, является ли блок данных полным.

    Args:
        data (str): Блок данных для проверки.

    Returns:
        bool: True, если блок данных полный, иначе False.
    """
    return data.endswith('\\n```\\n\\n') and data.count('```') % 2 == 0

def read_path_chunked(path: Path) -> Iterator[str]:
    """
    Построчно считывает файл, выдавая фрагменты определенного размера.

    Args:
        path (Path): Путь к файлу.

    Yields:
        str: Фрагменты данных из файла.
    """
    try:
        with path.open('r', encoding='utf-8') as f:
            current_chunk_size = 0
            buffer = ''
            for line in f:
                current_chunk_size += len(line.encode('utf-8'))
                buffer += line
                if current_chunk_size >= 4096:
                    if is_complete(buffer) or current_chunk_size >= 8192:
                        yield buffer
                        buffer = ''
                        current_chunk_size = 0
            if current_chunk_size > 0:
                yield buffer
    except Exception as ex:
        logger.error('Error while reading path chunked', ex, exc_info=True)

def read_bucket(bucket_dir: Path) -> Iterator[str]:
    """
    Читает данные из bucket, сначала из spaCy-файлов, затем из обычных.

    Args:
        bucket_dir (Path): Директория bucket.

    Yields:
        str: Данные из файлов.
    """
    bucket_dir = Path(bucket_dir)
    cache_file = bucket_dir / PLAIN_CACHE
    spacy_file = bucket_dir / 'spacy_0001.cache'

    if not spacy_file.is_file() and cache_file.is_file():
        try:
            yield cache_file.read_text(encoding='utf-8', errors='replace')
        except Exception as ex:
            logger.error('Error while reading cache file', ex, exc_info=True)

    for idx in range(1, 1000):
        spacy_file = bucket_dir / f'spacy_{idx:04d}.cache'
        plain_file = bucket_dir / f'plain_{idx:04d}.cache'

        if spacy_file.is_file():
            try:
                yield spacy_file.read_text(encoding='utf-8', errors='replace')
            except Exception as ex:
                logger.error(f'Error while reading spacy file {spacy_file}', ex, exc_info=True)
        elif plain_file.is_file():
            try:
                yield plain_file.read_text(encoding='utf-8', errors='replace')
            except Exception as ex:
                logger.error(f'Error while reading plain file {plain_file}', ex, exc_info=True)
        else:
            break

def stream_read_parts_and_refine(bucket_dir: Path, delete_files: bool = False) -> Iterator[str]:
    """
    Считывает части файла и обрабатывает их с помощью spaCy.

    Args:
        bucket_dir (Path): Директория bucket.
        delete_files (bool, optional): Удалять ли файлы после обработки. По умолчанию False.

    Yields:
        str: Обработанные фрагменты текста.
    """
    cache_file = bucket_dir / PLAIN_CACHE
    space_file = Path(bucket_dir) / 'spacy_0001.cache'
    part_one = bucket_dir / 'plain_0001.cache'

    if not space_file.exists() and not part_one.exists() and cache_file.exists():
        split_file_by_size_and_newline(cache_file, bucket_dir)

    for idx in range(1, 1000):
        part = bucket_dir / f'plain_{idx:04d}.cache'
        tmp_file = Path(bucket_dir) / f'spacy_{idx:04d}.{time.time()}.tmp'
        cache_file = Path(bucket_dir) / f'spacy_{idx:04d}.cache'

        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    yield f.read()
                continue
            except Exception as ex:
                logger.error(f'Error while reading cache file {cache_file}', ex, exc_info=True)

        if not part.exists():
            break

        try:
            with tmp_file.open('w', encoding='utf-8') as f:
                for chunk in spacy_refine_chunks(read_path_chunked(part)):
                    f.write(chunk)
                    yield chunk
            tmp_file.rename(cache_file)
            if delete_files:
                part.unlink()
        except Exception as ex:
            logger.error('Error while refining chunks with spacy', ex, exc_info=True)

def split_file_by_size_and_newline(input_filename: Path, output_dir: Path, chunk_size_bytes: int = 1024 * 1024) -> None:
    """
    Разбивает файл на части заданного размера, разделяя только по символу новой строки.

    Args:
        input_filename (Path): Путь к входному файлу.
        output_dir (Path): Директория для выходных файлов.
        chunk_size_bytes (int, optional): Размер каждой части в байтах. По умолчанию 1MB.
    """
    split_filename = os.path.splitext(os.path.basename(input_filename))
    output_prefix = os.path.join(output_dir, split_filename[0] + '_')

    try:
        with open(input_filename, 'r', encoding='utf-8') as infile:
            chunk_num = 1
            current_chunk = ''
            current_chunk_size = 0

            for line in infile:
                current_chunk += line
                current_chunk_size += len(line.encode('utf-8'))

                if current_chunk_size >= chunk_size_bytes:
                    if is_complete(current_chunk) or current_chunk_size >= chunk_size_bytes * 2:
                        output_filename = f'{output_prefix}{chunk_num:04d}{split_filename[1]}'
                        with open(output_filename, 'w', encoding='utf-8') as outfile:
                            outfile.write(current_chunk)
                        current_chunk = ''
                        current_chunk_size = 0
                        chunk_num += 1

            # Write the last chunk
            if current_chunk:
                output_filename = f'{output_prefix}{chunk_num:04d}{split_filename[1]}'
                with open(output_filename, 'w', encoding='utf-8') as outfile:
                    outfile.write(current_chunk)
    except Exception as ex:
        logger.error('Error while splitting file', ex, exc_info=True)

async def get_filename(response: aiohttp.ClientResponse) -> Optional[str]:
    """
    Пытается извлечь имя файла из ответа aiohttp.

    Args:
        response (aiohttp.ClientResponse): Объект ответа aiohttp.

    Returns:
        Optional[str]: Имя файла или None, если не удалось определить.
    """
    content_disposition = response.headers.get('Content-Disposition')
    if content_disposition:
        try:
            filename = content_disposition.split('filename=')[1].strip('"')
            if filename:
                return secure_filename(filename)
        except IndexError:
            pass

    content_type = response.headers.get('Content-Type')
    url = str(response.url)
    if content_type and url:
        extension = await get_file_extension(response)
        if extension:
            parsed_url = urllib.parse.urlparse(url)
            sha256_hash = hashlib.sha256(url.encode()).digest()
            base32_encoded = base64.b32encode(sha256_hash).decode()
            url_hash = base32_encoded[:24].lower()
            return f'{parsed_url.netloc}+{parsed_url.path[1:].replace("/", "_")}+{url_hash}{extension}'

    return None

async def get_file_extension(response: aiohttp.ClientResponse) -> Optional[str]:
    """
    Пытается определить расширение файла из ответа aiohttp.

    Args:
        response (aiohttp.ClientResponse): Объект ответа aiohttp.

    Returns:
        Optional[str]: Расширение файла или None, если не удалось определить.
    """
    content_type = response.headers.get('Content-Type')
    if content_type:
        content_type_lower = content_type.lower()
        if 'html' in content_type_lower:
            return '.html'
        elif 'json' in content_type_lower:
            return '.json'
        elif 'pdf' in content_type_lower:
            return '.pdf'
        elif 'zip' in content_type_lower:
            return '.zip'
        elif 'text/plain' in content_type_lower:
            return '.txt'
        elif 'markdown' in content_type_lower:
            return '.md'

    url = str(response.url)
    if url:
        return Path(url).suffix.lower()

    return None

def read_links(html: str, base: str) -> set[str]:
    """
    Извлекает ссылки из HTML-кода.

    Args:
        html (str): HTML-код страницы.
        base (str): Базовый URL для объединения относительных ссылок.

    Returns:
        set[str]: Множество URL-адресов.
    """
    soup = BeautifulSoup(html, 'html.parser')
    for selector in [
        'main',
        '.main-content-wrapper',
        '.main-content',
        '.emt-container-inner',
        '.content-wrapper',
        '#content',
        '#mainContent',
    ]:
        select = soup.select_one(selector)
        if select:
            soup = select
            break

    urls = []
    for link in soup.select('a'):
        if 'rel' not in link.attrs or 'nofollow' not in link.attrs['rel']:
            url = link.attrs.get('href')
            if url and (url.startswith('https://') or url.startswith('/')):
                urls.append(url.split('#')[0])

    return set(urllib.parse.urljoin(base, link) for link in urls)

async def download_urls(
    bucket_dir: Path,
    urls: list[str],
    max_depth: int = 0,
    loading_urls: set[str] = set(),
    lock: asyncio.Lock = None,
    delay: int = 3,
    new_urls: list[str] = list(),
    group_size: int = 5,
    timeout: int = 10,
    proxy: Optional[str] = None
) -> AsyncIterator[str]:
    """
    Асинхронно загружает файлы по URL-адресам.

    Args:
        bucket_dir (Path): Директория bucket.
        urls (list[str]): Список URL-адресов для загрузки.
        max_depth (int, optional): Максимальная глубина рекурсии для HTML-страниц. По умолчанию 0.
        loading_urls (set[str], optional): Множество URL-адресов, находящихся в процессе загрузки. По умолчанию set().
        lock (asyncio.Lock, optional): Блокировка для синхронизации доступа к общим ресурсам. По умолчанию None.
        delay (int, optional): Задержка между запросами. По умолчанию 3.
        new_urls (list[str], optional): Список новых URL-адресов, найденных на загруженных страницах. По умолчанию list().
        group_size (int, optional): Размер группы URL-адресов для параллельной загрузки. По умолчанию 5.
        timeout (int, optional): Время ожидания для запроса. По умолчанию 10.
        proxy (Optional[str], optional): Прокси-сервер для использования. По умолчанию None.

    Yields:
        str: Имена загруженных файлов.
    """
    if lock is None:
        lock = asyncio.Lock()

    try:
        async with aiohttp.ClientSession(
            connector=get_connector(proxy=proxy),
            timeout=aiohttp.ClientTimeout(timeout)
        ) as session:
            async def download_url(url: str, max_depth: int) -> Optional[str]:
                """
                Загружает один URL-адрес.

                Args:
                    url (str): URL-адрес для загрузки.
                    max_depth (int): Максимальная глубина рекурсии.

                Returns:
                    Optional[str]: Имя загруженного файла или None в случае ошибки.
                """
                try:
                    async with session.get(url) as response:
                        response.raise_for_status()
                        filename = await get_filename(response)
                        if not filename:
                            logger.warning(f'Failed to get filename for {url}')
                            return None

                        if not is_allowed_extension(filename) and not supports_filename(filename) or filename == DOWNLOADS_FILE:
                            return None

                        if filename.endswith('.html') and max_depth > 0:
                            html = await response.text()
                            add_urls = read_links(html, str(response.url))
                            if add_urls:
                                async with lock:
                                    add_urls = [add_url for add_url in add_urls if add_url not in loading_urls]
                                    [loading_urls.add(add_url) for add_url in add_urls]
                                    [new_urls.append(add_url) for add_url in add_urls if add_url not in new_urls]

                        if is_allowed_extension(filename):
                            target = bucket_dir / 'media' / filename
                            target.parent.mkdir(parents=True, exist_ok=True)
                        else:
                            target = bucket_dir / filename

                        try:
                            with target.open('wb') as f:
                                async for chunk in response.content.iter_any():
                                    if filename.endswith('.html') and b'<link rel="canonical"' not in chunk:
                                        f.write(chunk.replace(b'</head>', f'<link rel="canonical" href="{response.url}">\\n</head>'.encode()))
                                    else:
                                        f.write(chunk)
                            return filename
                        except Exception as ex:
                            logger.error(f'Error while writing file {filename}', ex, exc_info=True)
                            return None

                except (aiohttp.ClientError, asyncio.TimeoutError) as ex:
                    logger.error(f'Download failed for {url}: {ex.__class__.__name__}: {ex}', exc_info=True)
                    return None

            # Start downloading urls
            for filename in await asyncio.gather(*[download_url(url, max_depth) for url in urls]):
                if filename:
                    yield filename
                else:
                    await asyncio.sleep(delay)

            while new_urls:
                next_urls = list()
                for i in range(0, len(new_urls), group_size):
                    chunked_urls = new_urls[i:i + group_size]
                    async for filename in download_urls(bucket_dir, chunked_urls, max_depth - 1, loading_urls, lock, delay + 1, next_urls, group_size, timeout, proxy):
                        yield filename
                    await asyncio.sleep(delay)
                new_urls = next_urls
    except Exception as ex:
        logger.error('Error while downloading URLs', ex, exc_info=True)

def get_downloads_urls(bucket_dir: Path, delete_files: bool = False) -> Iterator[dict]:
    """
    Получает список URL-адресов для загрузки из файла DOWNLOADS_FILE.

    Args:
        bucket_dir (Path): Директория bucket.
        delete_files (bool, optional): Удалять ли файл после чтения. По умолчанию False.

    Yields:
        dict: Словарь с URL-адресами и дополнительными параметрами.
    """
    download_file = bucket_dir / DOWNLOADS_FILE
    if download_file.exists():
        try:
            with download_file.open('r', encoding='utf-8') as f:
                data = json.load(f)
            if delete_files:
                try:
                    download_file.unlink()
                except Exception as ex:
                    logger.error(f'Error while deleting file {download_file}', ex, exc_info=True)
            if isinstance(data, list):
                for item in data:
                    if 'url' in item:
                        yield {'urls': [item.pop('url')], **item}
                    elif 'urls' in item:
                        yield item
        except (FileNotFoundError, json.JSONDecodeError) as ex:
            logger.error(f'Error while reading or parsing file {download_file}', ex, exc_info=True)

def read_and_download_urls(bucket_dir: Path, delete_files: bool = False, event_stream: bool = False) -> Iterator[str]:
    """
    Читает и загружает URL-адреса из файла конфигурации.

    Args:
        bucket_dir (Path): Директория bucket.
        delete_files (bool, optional): Удалять ли файлы конфигурации после загрузки. По умолчанию False.
        event_stream (bool, optional): Включить ли потоковую передачу событий. По умолчанию False.

    Yields:
        str: События в формате JSON, если включена потоковая передача, или None.
    """
    urls = get_downloads_urls(bucket_dir, delete_files)
    if urls:
        count = 0
        try:
            with open(os.path.join(bucket_dir, FILE_LIST), 'a', encoding='utf-8') as f:
                for url in urls:
                    for filename in to_sync_generator(download_urls(bucket_dir, **url)):
                        f.write(f'{filename}\\n')
                        if event_stream:
                            count += 1
                            yield f'data: {json.dumps({"action": "download", "count": count})}\\n\\n'
        except Exception as ex:
            logger.error('Error while reading and downloading URLs', ex, exc_info=True)

async def async_read_and_download_urls(bucket_dir: Path, delete_files: bool = False, event_stream: bool = False) -> AsyncIterator[str]:
    """
    Асинхронно считывает и загружает URL-адреса из файла конфигурации.