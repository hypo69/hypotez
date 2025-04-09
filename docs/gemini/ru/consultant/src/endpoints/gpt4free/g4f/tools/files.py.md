### **Анализ кода модуля `files.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 6/10
- **Плюсы**:
  - Код разбит на множество функций, что улучшает читаемость и упрощает отладку.
  - Обработка различных типов файлов (pdf, docx, odt, epub, xlsx, html, zip, txt и др.).
  - Использование `asyncio` для асинхронных операций, что позволяет повысить производительность при работе с сетью.
  - Реализована логика кэширования прочитанных данных.
- **Минусы**:
  - Отсутствие аннотаций типов для большинства переменных.
  - Не везде используется модуль `logger` для логирования.
  - Присутствуют конструкции `try...except` без указания конкретного типа исключения, что затрудняет отладку.
  - В некоторых местах используется небезопасное открытие файлов без указания кодировки.
  - Смешаны синхронные и асинхронные операции.
  - Не все функции имеют docstring.

#### **Рекомендации по улучшению**:
- Добавить аннотации типов для всех переменных и параметров функций.
- Использовать `logger` из `src.logger` для логирования ошибок и важной информации.
- Указывать конкретные типы исключений в блоках `try...except`.
- Явно указывать кодировку при открытии файлов (например, `encoding='utf-8'`).
- Привести весь код к асинхронному виду, используя `async` и `await` везде, где это возможно.
- Добавить docstring для всех функций и классов, включая описание параметров, возвращаемых значений и возможных исключений.
- Разбить большие функции на более мелкие, чтобы улучшить читаемость и упростить отладку.
- Улучшить обработку ошибок при работе с различными типами файлов.
- Избавиться от излишней вложенности в некоторых местах кода.
- Пересмотреть логику работы с кэшем, чтобы избежать потенциальных проблем с конкурентным доступом.

#### **Оптимизированный код**:

```python
"""
Модуль для работы с файлами различных форматов
================================================

Модуль содержит функции для чтения, обработки и скачивания файлов различных форматов,
включая .txt, .pdf, .docx, .odt, .epub, .xlsx, .html, .zip и другие.

Пример использования
----------------------

>>> from pathlib import Path
>>> bucket_dir = Path('./test_bucket')
>>> bucket_dir.mkdir(parents=True, exist_ok=True)
>>> # Пример использования функций модуля
"""
from __future__ import annotations

import re
import os
import json
from pathlib import Path
from typing import Iterator, Optional, AsyncIterator, List
from aiohttp import ClientSession, ClientError, ClientResponse, ClientTimeout
import urllib.parse
from urllib.parse import unquote
import time
import zipfile
import asyncio
import hashlib
import base64

from src.logger import logger # Импорт модуля logger

try:
    import PyPDF2
    from PyPDF2.errors import PdfReadError

    has_pypdf2: bool = True
except ImportError:
    has_pypdf2: bool = False
try:
    import pdfplumber

    has_pdfplumber: bool = True
except ImportError:
    has_pdfplumber: bool = False
try:
    from pdfminer.high_level import extract_text

    has_pdfminer: bool = True
except ImportError:
    has_pdfminer: bool = False
try:
    from docx import Document

    has_docx: bool = True
except ImportError:
    has_docx: bool = False
try:
    import docx2txt

    has_docx2txt: bool = True
except ImportError:
    has_docx2txt: bool = False
try:
    from odf.opendocument import load
    from odf.text import P

    has_odfpy: bool = True
except ImportError:
    has_odfpy: bool = False
try:
    import ebooklib
    from ebooklib import epub

    has_ebooklib: bool = True
except ImportError:
    has_ebooklib: bool = False
try:
    import pandas as pd

    has_openpyxl: bool = True
except ImportError:
    has_openpyxl: bool = False
try:
    import spacy

    has_spacy: bool = True
except:
    has_spacy: bool = False
try:
    from bs4 import BeautifulSoup

    has_beautifulsoup4: bool = True
except ImportError:
    has_beautifulsoup4: bool = False

from .web_search import scrape_text
from ..cookies import get_cookies_dir
from ..image import is_allowed_extension
from ..requests.aiohttp import get_connector
from ..providers.asyncio import to_sync_generator
from ..errors import MissingRequirementsError
from .. import debug

PLAIN_FILE_EXTENSIONS: List[str] = ["txt", "xml", "json", "js", "har", "sh", "py", "php", "css", "yaml", "sql", "log", "csv", "twig", "md", "arc"]
PLAIN_CACHE: str = "plain.cache"
DOWNLOADS_FILE: str = "downloads.json"
FILE_LIST: str = "files.txt"

def secure_filename(filename: str) -> str:
    """
    Очищает имя файла от небезопасных символов.

    Args:
        filename (str): Исходное имя файла.

    Returns:
        str: Очищенное имя файла.
    """
    if filename is None:
        return None
    # Keep letters, numbers, basic punctuation and all Unicode chars
    filename = re.sub(
        r'[^\\w.,_+-]+',
        '_',
        unquote(filename).strip(),
        flags=re.UNICODE
    )
    filename = filename[:100].strip(".,_-+")
    return filename


def supports_filename(filename: str) -> bool:
    """
    Проверяет, поддерживается ли указанный тип файла для обработки.

    Args:
        filename (str): Имя файла.

    Returns:
        bool: True, если файл поддерживается, иначе False.

    Raises:
        MissingRequirementsError: Если отсутствуют необходимые библиотеки для обработки файла.
    """
    if filename.endswith(".pdf"):
        if has_pypdf2:
            return True
        elif has_pdfplumber:
            return True
        elif has_pdfminer:
            return True
        raise MissingRequirementsError('Install "pypdf2" requirements | pip install -U g4f[files]')
    elif filename.endswith(".docx"):
        if has_docx:
            return True
        elif has_docx2txt:
            return True
        raise MissingRequirementsError('Install "docx" requirements | pip install -U g4f[files]')
    elif has_odfpy and filename.endswith(".odt"):
        return True
    elif has_ebooklib and filename.endswith(".epub"):
        return True
    elif has_openpyxl and filename.endswith(".xlsx"):
        return True
    elif filename.endswith(".html"):
        if not has_beautifulsoup4:
            raise MissingRequirementsError('Install "beautifulsoup4" requirements | pip install -U g4f[files]')
        return True
    elif filename.endswith(".zip"):
        return True
    elif filename.endswith("package-lock.json") and filename != FILE_LIST:
        return False
    else:
        extension = os.path.splitext(filename)[1][1:]
        if extension in PLAIN_FILE_EXTENSIONS:
            return True
    return False


def get_bucket_dir(*parts: str) -> str:
    """
    Формирует путь к директории бакета.

    Args:
        *parts (str): Части пути к бакету.

    Returns:
        str: Полный путь к директории бакета.
    """
    return os.path.join(get_cookies_dir(), "buckets", *[secure_filename(part) for part in parts if part])


def get_buckets() -> Optional[List[str]]:
    """
    Получает список директорий бакетов.

    Returns:
        Optional[List[str]]: Список директорий бакетов или None в случае ошибки.
    """
    buckets_dir: str = os.path.join(get_cookies_dir(), "buckets")
    try:
        return [d for d in os.listdir(buckets_dir) if os.path.isdir(os.path.join(buckets_dir, d))]
    except OSError as ex:
        logger.error('Error while getting buckets', ex, exc_info=True)
        return None


def spacy_refine_chunks(source_iterator: Iterator[str]) -> Iterator[str]:
    """
    Разбивает текст на чанки с использованием spaCy.

    Args:
        source_iterator (Iterator[str]): Итератор по страницам текста.

    Returns:
        Iterator[str]: Итератор по предложениям, выделенным с помощью spaCy.

    Raises:
        MissingRequirementsError: Если не установлен spaCy.
    """
    if not has_spacy:
        raise MissingRequirementsError('Install "spacy" requirements | pip install -U g4f[files]')

    nlp = spacy.load("en_core_web_sm")
    for page in source_iterator:
        doc = nlp(page)
        # for chunk in doc.noun_chunks:
        #    yield " ".join([token.lemma_ for token in chunk if not token.is_stop])
        # for token in doc:
        #     if not token.is_space:
        #         yield token.lemma_.lower()
        #         yield " "
        sentences = list(doc.sents)
        summary = sorted(sentences, key=lambda x: len(x.text), reverse=True)[:2]
        for sent in summary:
            yield sent.text


def get_filenames(bucket_dir: Path) -> List[str]:
    """
    Получает список имен файлов из файла `FILE_LIST` в указанной директории.

    Args:
        bucket_dir (Path): Директория бакета.

    Returns:
        List[str]: Список имен файлов.
    """
    files: Path = bucket_dir / FILE_LIST
    if files.exists():
        with files.open('r', encoding='utf-8') as f:
            return [filename.strip() for filename in f.readlines()]
    return []


def stream_read_files(bucket_dir: Path, filenames: list, delete_files: bool = False) -> Iterator[str]:
    """
    Читает содержимое файлов из указанной директории и возвращает итератор по строкам.

    Args:
        bucket_dir (Path): Директория бакета.
        filenames (list): Список имен файлов для чтения.
        delete_files (bool, optional): Удалять ли файлы после прочтения. По умолчанию False.

    Yields:
        str: Строка из файла.
    """
    for filename in filenames:
        file_path: Path = bucket_dir / filename
        if not file_path.exists() or file_path.lstat().st_size <= 0:
            continue
        extension: str = os.path.splitext(filename)[1][1:]
        if filename.endswith(".zip"):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(bucket_dir)
                try:
                    yield from stream_read_files(bucket_dir, [f for f in zip_ref.namelist() if supports_filename(f)], delete_files)
                except zipfile.BadZipFile as ex:
                    logger.error('Error while processing zip file', ex, exc_info=True)
                    pass
                finally:
                    if delete_files:
                        for unlink in zip_ref.namelist()[::-1]:
                            filepath: str = os.path.join(bucket_dir, unlink)
                            if os.path.exists(filepath):
                                if os.path.isdir(filepath):
                                    os.rmdir(filepath)
                                else:
                                    os.unlink(filepath)
            continue
        yield f"```{filename}\\n"

        if has_pypdf2 and filename.endswith(".pdf"):
            try:
                reader = PyPDF2.PdfReader(file_path)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    yield page.extract_text()
            except PdfReadError as ex:
                logger.error('Error while processing pdf file with PyPDF2', ex, exc_info=True)
                continue
        if has_pdfplumber and filename.endswith(".pdf"):
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    yield page.extract_text()
        if has_pdfminer and filename.endswith(".pdf"):
            yield extract_text(file_path)
        elif has_docx and filename.endswith(".docx"):
            doc = Document(file_path)
            for para in doc.paragraphs:
                yield para.text
        elif has_docx2txt and filename.endswith(".docx"):
            yield docx2txt.process(file_path)
        elif has_odfpy and filename.endswith(".odt"):
            textdoc = load(file_path)
            allparas = textdoc.getElementsByType(P)
            for p in allparas:
                yield p.firstChild.data if p.firstChild else ""
        elif has_ebooklib and filename.endswith(".epub"):
            book = epub.read_epub(file_path)
            for doc_item in book.get_items():
                if doc_item.get_type() == ebooklib.ITEM_DOCUMENT:
                    yield doc_item.get_content().decode(errors='ignore')
        elif has_openpyxl and filename.endswith(".xlsx"):
            df = pd.read_excel(file_path)
            for row in df.itertuples(index=False):
                yield " ".join(str(cell) for cell in row)
        elif has_beautifulsoup4 and filename.endswith(".html"):
            yield from scrape_text(file_path.read_text(errors="ignore"))
        elif extension in PLAIN_FILE_EXTENSIONS:
            yield file_path.read_text(errors="ignore")
        yield f"\\n```\\n\\n"


def cache_stream(stream: Iterator[str], bucket_dir: Path) -> Iterator[str]:
    """
    Кэширует содержимое потока в файл.

    Args:
        stream (Iterator[str]): Итератор по строкам.
        bucket_dir (Path): Директория бакета.

    Yields:
        str: Строка из потока.
    """
    cache_file: Path = bucket_dir / PLAIN_CACHE
    tmp_file: Path = bucket_dir / f"{PLAIN_CACHE}.{time.time()}.tmp"
    if cache_file.exists():
        for chunk in read_path_chunked(cache_file):
            yield chunk
        return
    with open(tmp_file, "wb") as f:
        for chunk in stream:
            f.write(chunk.encode(errors="replace"))
            yield chunk
    tmp_file.rename(cache_file)


def is_complete(data: str) -> bool:
    """
    Проверяет, является ли блок данных полным.

    Args:
        data (str): Блок данных.

    Returns:
        bool: True, если блок данных полный, иначе False.
    """
    return data.endswith("\\n```\\n\\n") and data.count("```") % 2 == 0


def read_path_chunked(path: Path) -> Iterator[str]:
    """
    Читает файл по частям.

    Args:
        path (Path): Путь к файлу.

    Yields:
        str: Часть файла.
    """
    with path.open("r", encoding='utf-8') as f:
        current_chunk_size: int = 0
        buffer: str = ""
        for line in f:
            current_chunk_size += len(line.encode('utf-8'))
            buffer += line
            if current_chunk_size >= 4096:
                if is_complete(buffer) or current_chunk_size >= 8192:
                    yield buffer
                    buffer = ""
                    current_chunk_size = 0
        if current_chunk_size > 0:
            yield buffer


def read_bucket(bucket_dir: Path) -> Iterator[str]:
    """
    Читает данные из бакета.

    Args:
        bucket_dir (Path): Директория бакета.

    Yields:
        str: Данные из бакета.
    """
    bucket_dir = Path(bucket_dir)
    cache_file: Path = bucket_dir / PLAIN_CACHE
    spacy_file: Path = bucket_dir / f"spacy_0001.cache"
    if not spacy_file.is_file() and cache_file.is_file():
        yield cache_file.read_text(errors="replace")
    for idx in range(1, 1000):
        spacy_file = bucket_dir / f"spacy_{idx:04d}.cache"
        plain_file = bucket_dir / f"plain_{idx:04d}.cache"
        if spacy_file.is_file():
            yield spacy_file.read_text(errors="replace")
        elif plain_file.is_file():
            yield plain_file.read_text(errors="replace")
        else:
            break


def stream_read_parts_and_refine(bucket_dir: Path, delete_files: bool = False) -> Iterator[str]:
    """
    Читает части файла и уточняет их с помощью spaCy.

    Args:
        bucket_dir (Path): Директория бакета.
        delete_files (bool, optional): Удалять ли файлы после прочтения. По умолчанию False.

    Yields:
        str: Уточненные данные.
    """
    cache_file: Path = bucket_dir / PLAIN_CACHE
    space_file: Path = Path(bucket_dir) / f"spacy_0001.cache"
    part_one: Path = bucket_dir / f"plain_0001.cache"
    if not space_file.exists() and not part_one.exists() and cache_file.exists():
        split_file_by_size_and_newline(cache_file, bucket_dir)
    for idx in range(1, 1000):
        part: Path = bucket_dir / f"plain_{idx:04d}.cache"
        tmp_file: Path = Path(bucket_dir) / f"spacy_{idx:04d}.{time.time()}.tmp"
        cache_file: Path = Path(bucket_dir) / f"spacy_{idx:04d}.cache"
        if cache_file.exists():
            with open(cache_file, "r", encoding='utf-8') as f:
                yield f.read(errors="replace")
            continue
        if not part.exists():
            break
        with tmp_file.open("w", encoding='utf-8') as f:
            for chunk in spacy_refine_chunks(read_path_chunked(part)):
                f.write(chunk)
                yield chunk
        tmp_file.rename(cache_file)
        if delete_files:
            part.unlink()


def split_file_by_size_and_newline(input_filename: str, output_dir: str, chunk_size_bytes: int = 1024 * 1024) -> None: # 1MB
    """
    Разбивает файл на части заданного размера, разделяя только по символу новой строки.

    Args:
        input_filename (str): Путь к входному файлу.
        output_dir (str): Директория для выходных файлов.
        chunk_size_bytes (int, optional): Размер каждой части в байтах. По умолчанию 1MB.
    """
    split_filename: tuple[str, str] = os.path.splitext(os.path.basename(input_filename))
    output_prefix: str = os.path.join(output_dir, split_filename[0] + "_")

    with open(input_filename, 'r', encoding='utf-8') as infile:
        chunk_num: int = 1
        current_chunk: str = ""
        current_chunk_size: int = 0

        for line in infile:
            current_chunk += line
            current_chunk_size += len(line.encode('utf-8'))

            if current_chunk_size >= chunk_size_bytes:
                if is_complete(current_chunk) or current_chunk_size >= chunk_size_bytes * 2:
                    output_filename: str = f"{output_prefix}{chunk_num:04d}{split_filename[1]}"
                    with open(output_filename, 'w', encoding='utf-8') as outfile:
                        outfile.write(current_chunk)
                    current_chunk = ""
                    current_chunk_size = 0
                    chunk_num += 1

        # Write the last chunk
        if current_chunk:
            output_filename = f"{output_prefix}{chunk_num:04d}{split_filename[1]}"
            with open(output_filename, 'w', encoding='utf-8') as outfile:
                outfile.write(current_chunk)


async def get_filename(response: ClientResponse) -> Optional[str]:
    """
    Извлекает имя файла из ответа aiohttp.

    Args:
        response (ClientResponse): Ответ aiohttp.

    Returns:
        Optional[str]: Имя файла или None, если не удалось определить.
    """
    content_disposition: str = response.headers.get('Content-Disposition')
    if content_disposition:
        try:
            filename: str = content_disposition.split('filename=')[1].strip('"')
            if filename:
                return secure_filename(filename)
        except IndexError:
            pass

    content_type: str = response.headers.get('Content-Type')
    url: str = str(response.url)
    if content_type and url:
        extension: str = await get_file_extension(response)
        if extension:
            parsed_url = urllib.parse.urlparse(url)
            sha256_hash = hashlib.sha256(url.encode()).digest()
            base32_encoded = base64.b32encode(sha256_hash).decode()
            url_hash = base32_encoded[:24].lower()
            return f"{parsed_url.netloc}+{parsed_url.path[1:].replace('/', '_')}+{url_hash}{extension}"

    return None


async def get_file_extension(response: ClientResponse) -> Optional[str]:
    """
    Определяет расширение файла из ответа aiohttp.

    Args:
        response (ClientResponse): Ответ aiohttp.

    Returns:
        Optional[str]: Расширение файла или None, если не удалось определить.
    """
    content_type: str = response.headers.get('Content-Type')
    if content_type:
        if "html" in content_type.lower():
            return ".html"
        elif "json" in content_type.lower():
            return ".json"
        elif "pdf" in content_type.lower():
            return ".pdf"
        elif "zip" in content_type.lower():
            return ".zip"
        elif "text/plain" in content_type.lower():
            return ".txt"
        elif "markdown" in content_type.lower():
            return ".md"

    url: str = str(response.url)
    if url:
        return Path(url).suffix.lower()

    return None


def read_links(html: str, base: str) -> set[str]:
    """
    Извлекает ссылки из HTML-кода.

    Args:
        html (str): HTML-код.
        base (str): Базовый URL.

    Returns:
        set[str]: Множество ссылок.
    """
    soup = BeautifulSoup(html, "html.parser")
    for selector in [
            "main",
            ".main-content-wrapper",
            ".main-content",
            ".emt-container-inner",
            ".content-wrapper",
            "#content",
            "#mainContent",
        ]:
        select = soup.select_one(selector)
        if select:
            soup = select
            break
    urls = []
    for link in soup.select("a"):
        if "rel" not in link.attrs or "nofollow" not in link.attrs["rel"]:
            url = link.attrs.get("href")
            if url and url.startswith("https://") or url.startswith("/"):
                urls.append(url.split("#")[0])
    return set([urllib.parse.urljoin(base, link) for link in urls])


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
    Асинхронно скачивает файлы по URL.

    Args:
        bucket_dir (Path): Директория бакета.
        urls (list[str]): Список URL для скачивания.
        max_depth (int, optional): Максимальная глубина рекурсии для скачивания HTML-страниц. По умолчанию 0.
        loading_urls (set[str], optional): Множество URL, которые уже находятся в процессе скачивания. По умолчанию set().
        lock (asyncio.Lock, optional): Блокировка для синхронизации доступа к общим ресурсам. По умолчанию None.
        delay (int, optional): Задержка между запросами. По умолчанию 3.
        new_urls (list[str], optional): Список новых URL, обнаруженных в процессе скачивания. По умолчанию list().
        group_size (int, optional): Размер группы URL для одновременной загрузки. По умолчанию 5.
        timeout (int, optional): Максимальное время ожидания ответа от сервера. По умолчанию 10.
        proxy (Optional[str], optional): Прокси-сервер для использования. По умолчанию None.

    Yields:
        str: Имя скачанного файла.
    """
    if lock is None:
        lock = asyncio.Lock()
    async with ClientSession(
        connector=get_connector(proxy=proxy),
        timeout=ClientTimeout(timeout)
    ) as session:
        async def download_url(url: str, max_depth: int) -> Optional[str]:
            """
            Асинхронно скачивает один файл по URL.

            Args:
                url (str): URL для скачивания.
                max_depth (int): Максимальная глубина рекурсии.

            Returns:
                Optional[str]: Имя скачанного файла или None в случае ошибки.
            """
            try:
                async with session.get(url) as response:
                    response.raise_for_status()
                    filename: str = await get_filename(response)
                    if not filename:
                        print(f"Failed to get filename for {url}")
                        return None
                    if not is_allowed_extension(filename) and not supports_filename(filename) or filename == DOWNLOADS_FILE:
                        return None
                    if filename.endswith(".html") and max_depth > 0:
                        add_urls = read_links(await response.text(), str(response.url))
                        if add_urls:
                            async with lock:
                                add_urls = [add_url for add_url in add_urls if add_url not in loading_urls]
                                [loading_urls.add(add_url) for add_url in add_urls]
                                [new_urls.append(add_url) for add_url in add_urls if add_url not in new_urls]
                    if is_allowed_extension(filename):
                        target: Path = bucket_dir / "media" / filename
                        target.parent.mkdir(parents=True, exist_ok=True)
                    else:
                        target: Path = bucket_dir / filename
                    with target.open("wb") as f:
                        async for chunk in response.content.iter_any():
                            if filename.endswith(".html") and b'<link rel="canonical"' not in chunk:
                                f.write(chunk.replace(b'</head>', f'<link rel="canonical" href="{response.url}">\\n</head>'.encode()))
                            else:
                                f.write(chunk)
                    return filename
            except (ClientError, asyncio.TimeoutError) as ex:
                debug.log(f"Download failed: {ex.__class__.__name__}: {ex}")
                logger.error('Error while downloading url', ex, exc_info=True)
            return None
        for filename in await asyncio.gather(*[download_url(url, max_depth) for url in urls]):
            if filename:
                yield filename
            else:
                await asyncio.sleep(delay)
        while new_urls:
            next_urls: list[str] = list()
            for i in range(0, len(new_urls), group_size):
                chunked_urls: list[str] = new_urls[i:i + group_size]
                async for filename in download_urls(bucket_dir, chunked_urls, max_depth - 1, loading_urls, lock, delay + 1, next_urls):
                    yield filename
                await asyncio.sleep(delay)
            new_urls = next_urls


def get_downloads_urls(bucket_dir: Path, delete_files: bool = False) -> Iterator[dict]:
    """
    Извлекает URL для скачивания из файла `DOWNLOADS_FILE`.

    Args:
        bucket_dir (Path): Директория бакета.
        delete_files (bool, optional): Удалять ли файл после прочтения. По умолчанию False.

    Yields:
        dict: Словарь с URL для скачивания и дополнительными параметрами.
    """
    download_file: Path = bucket_dir / DOWNLOADS_FILE
    if download_file.exists():
        with download_file.open('r', encoding='utf-8') as f:
            data: list[dict] = json.load(f)
        if delete_files:
            download_file.unlink()
        if isinstance(data, list):
            for item in data:
                if "url" in item:
                    yield {"urls": [item.pop("url")], **item}
                elif "urls" in item:
                    yield item


def read_and_download_urls(bucket_dir: Path, delete_files: bool = False, event_stream: bool = False) -> Iterator[str]:
    """
    Читает и скачивает файлы по URL из файла `DOWNLOADS_FILE`.

    Args:
        bucket_dir (Path): Директория бакета.
        delete_files (bool, optional): Удалять ли файл `DOWNLOADS_FILE` после прочтения. По умолчанию False.
        event_stream (bool, optional): Включить ли потоковую передачу событий. По умолчанию False.

    Yields:
        str: Событие в формате JSON или имя скачанного файла.
    """
    urls: Iterator[dict] = get_downloads_urls(bucket_dir, delete_files)
    if urls:
        count: int = 0
        with open(os.path.join(bucket_dir, FILE_LIST), 'a', encoding='utf-8') as f:
            for url in urls:
                for filename in to_sync_generator(download_urls(bucket_dir, **url)):
                    f.write(f"{filename}\\n")
                    if event_stream:
                        count += 1
                        yield f'data: {json.dumps({"action": "download", "count": count})}\\n\\n'


async def async_read_and_download_urls(bucket_dir: Path, delete_files: bool = False, event_stream: bool = False) -> AsyncIterator[str]:
    """
    Асинхронно читает и скачивает файлы по URL из файла `DOWNLOADS_FILE`.

    Args:
        bucket_dir (Path): Директория бакета.
        delete_files (bool, optional): Удалять ли файл `DOWNLOADS_FILE` после прочтения. По умолчанию False.
        event_stream (bool, optional): Включить ли потоковую передачу событий. По умолчанию False.

    Yields:
        str: Событие в формате JSON или имя скачанного файла.
    """
    urls: Iterator[dict] = get_downloads_urls(bucket_dir, delete_files)
    if urls:
        count: int = 0
        with open(os.path.join(bucket_dir, FILE_LIST), 'a', encoding='utf-8') as f:
            async for filename in download_urls(bucket_dir, urls):
                f.write(f"{filename}\\n")
                if event_stream:
                    count += 1
                    yield f'data: {json.dumps({"action": "download", "count": count})}\\n\\n'


def stream_chunks(bucket_dir: Path, delete_files: bool = False, refine_chunks_with_spacy: bool = False, event_stream: bool = False) -> Iterator[str]:
    """
    Читает содержимое файлов из бакета и возвращает итератор по частям.

    Args:
        bucket_dir (Path): Директория бакета.
        delete_files (bool, optional): Удалять ли файлы после прочтения. По умолчанию False.
        refine_chunks_with_spacy (bool, optional): Использовать ли spaCy для уточнения частей текста. По умолчанию False.
        event_stream (bool, optional): Включить ли потоковую передачу событий. По умолчанию False.

    Yields:
        str: Часть текста