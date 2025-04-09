### **Анализ кода модуля `web_search.py`**

**Качество кода**:
- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Использование `JsonMixin` для работы с JSON.
    - Наличие кеширования результатов поиска.
    - Использование `asyncio` для асинхронных операций.
- **Минусы**:
    - Смешанный стиль кавычек (используются как одинарные, так и двойные).
    - Отсутствие документации для многих функций и классов.
    - Не все переменные аннотированы типами.
    - Использование устаревшего `Union[]`.
    - Отсутствие логирования ошибок с использованием `logger` из `src.logger`.
    - Не везде используется `j_loads` или `j_loads_ns` для чтения JSON.
    - Отсутствуют комментарии, объясняющие назначение кода.

**Рекомендации по улучшению**:

1. **Исправить стиль кавычек**:
   - Заменить все двойные кавычки на одинарные.

2. **Добавить документацию**:
   - Добавить docstring для всех функций и классов, включая описание аргументов, возвращаемых значений и возможных исключений.
   - Добавить комментарии, объясняющие логику работы кода.

3. **Добавить аннотации типов**:
   - Добавить аннотации типов для всех переменных.

4. **Использовать `|` вместо `Union[]`**:
   - Заменить все `Union[]` на `|`.

5. **Добавить логирование**:
   - Добавить логирование ошибок с использованием `logger` из `src.logger`.

6. **Использовать `j_loads` или `j_loads_ns`**:
   - Заменить стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns`.

7. **Улучшить обработку исключений**:
   - Использовать `ex` вместо `e` в блоках обработки исключений.

8. **Улучшить читаемость кода**:
   - Добавить пробелы вокруг операторов присваивания.
   - Следовать стандартам PEP8.

9. **Использовать вебдрайвер**:
   - Если в коде используется вебдрайвер, использовать `driver.execute_locator(l:dict)` для взаимодействия с веб-элементами.

**Оптимизированный код**:

```python
from __future__ import annotations

from aiohttp import ClientSession, ClientTimeout, ClientError
import json
import hashlib
from pathlib import Path
from urllib.parse import urlparse, quote_plus
from datetime import datetime
import asyncio
from typing import Iterator, Optional, List

from src.logger import logger  # Подключаем модуль logger
try:
    from duckduckgo_search import DDGS
    from duckduckgo_search.exceptions import DuckDuckGoSearchException
    from bs4 import BeautifulSoup

    ddgs = DDGS()
    has_requirements = True
except ImportError as ex:
    has_requirements = False
    logger.error('Failed to import duckduckgo-search or beautifulsoup4', ex, exc_info=True)

try:
    import spacy

    has_spacy = True
except ImportError as ex:
    has_spacy = False
    logger.error('Failed to import spacy', ex, exc_info=True)


from ..cookies import get_cookies_dir
from ..providers.response import format_link, JsonMixin, Sources
from ..errors import MissingRequirementsError
from .. import debug

DEFAULT_INSTRUCTIONS = """
Using the provided web search results, to write a comprehensive reply to the user request.
Make sure to add the sources of cites using [[Number]](Url) notation after the reference. Example: [[0]](http://google.com)
"""


class SearchResults(JsonMixin):
    """
    Класс для хранения результатов поиска.
    """

    def __init__(self, results: list, used_words: int) -> None:
        """
        Инициализирует экземпляр класса SearchResults.

        Args:
            results (list): Список результатов поиска.
            used_words (int): Количество использованных слов.
        """
        self.results = results
        self.used_words = used_words

    @classmethod
    def from_dict(cls, data: dict) -> SearchResults:
        """
        Создает экземпляр класса SearchResults из словаря.

        Args:
            data (dict): Словарь с данными.

        Returns:
            SearchResults: Экземпляр класса SearchResults.
        """
        return cls(
            [SearchResultEntry(**item) for item in data['results']],
            data['used_words']
        )

    def __iter__(self) -> Iterator[SearchResultEntry]:
        """
        Возвращает итератор по результатам поиска.

        Yields:
            SearchResultEntry: Результат поиска.
        """
        yield from self.results

    def __str__(self) -> str:
        """
        Возвращает строковое представление результатов поиска.

        Returns:
            str: Строковое представление результатов поиска.
        """
        search = ''
        for idx, result in enumerate(self.results):
            if search:
                search += '\n\n\n'
            search += f'Title: {result.title}\n\n'
            if result.text:
                search += result.text
            else:
                search += result.snippet
            search += f'\n\nSource: [[{idx}]]({result.url})'
        return search

    def __len__(self) -> int:
        """
        Возвращает количество результатов поиска.

        Returns:
            int: Количество результатов поиска.
        """
        return len(self.results)

    def get_sources(self) -> Sources:
        """
        Возвращает источники результатов поиска.

        Returns:
            Sources: Источники результатов поиска.
        """
        return Sources([{'url': result.url, 'title': result.title} for result in self.results])

    def get_dict(self) -> dict:
        """
        Возвращает словарь с данными результатов поиска.

        Returns:
            dict: Словарь с данными результатов поиска.
        """
        return {
            'results': [result.get_dict() for result in self.results],
            'used_words': self.used_words
        }


class SearchResultEntry(JsonMixin):
    """
    Класс для хранения отдельного результата поиска.
    """

    def __init__(self, title: str, url: str, snippet: str, text: Optional[str] = None) -> None:
        """
        Инициализирует экземпляр класса SearchResultEntry.

        Args:
            title (str): Заголовок результата поиска.
            url (str): URL результата поиска.
            snippet (str): Краткое описание результата поиска.
            text (Optional[str], optional): Полный текст результата поиска. По умолчанию None.
        """
        self.title = title
        self.url = url
        self.snippet = snippet
        self.text = text

    def set_text(self, text: str) -> None:
        """
        Устанавливает полный текст результата поиска.

        Args:
            text (str): Полный текст результата поиска.
        """
        self.text = text


def scrape_text(html: str, max_words: Optional[int] = None, add_source: bool = True, count_images: int = 2) -> Iterator[str]:
    """
    Извлекает текст из HTML-кода.

    Args:
        html (str): HTML-код страницы.
        max_words (Optional[int], optional): Максимальное количество слов для извлечения. По умолчанию None.
        add_source (bool, optional): Добавлять ли источник в конце текста. По умолчанию True.
        count_images (int, optional): Максимальное количество изображений для извлечения. По умолчанию 2.

    Yields:
        str: Извлеченный текст.
    """
    source = BeautifulSoup(html, 'html.parser')
    soup = source
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
    # Zdnet
    for remove in ['.c-globalDisclosure']:
        select = soup.select_one(remove)
        if select:
            select.extract()

    image_select = 'img[alt][src^=http]:not([alt=\'\']):not(.avatar):not([width])'
    image_link_select = f'a:has({image_select})'
    yield_words = []
    for paragraph in soup.select(f'h1, h2, h3, h4, h5, h6, p, pre, table:not(:has(p)), ul:not(:has(p)), {image_link_select}'):
        if count_images > 0:
            image = paragraph.select_one(image_select)
            if image:
                title = str(paragraph.get('title', paragraph.text))
                if title:
                    yield f'!{format_link(image['src'], title)}\n'
                    if max_words is not None:
                        max_words -= 10
                    count_images -= 1
                continue

        for line in paragraph.get_text(' ').splitlines():
            words = [word for word in line.split() if word]
            count = len(words)
            if not count:
                continue
            words = ' '.join(words)
            if words in yield_words:
                continue
            if max_words:
                max_words -= count
                if max_words <= 0:
                    break
            yield words + '\n'
            yield_words.append(words)

    if add_source:
        canonical_link = source.find('link', rel='canonical')
        if canonical_link and 'href' in canonical_link.attrs:
            link = canonical_link['href']
            domain = urlparse(link).netloc
            yield f'\nSource: [{domain}]({link})'


async def fetch_and_scrape(session: ClientSession, url: str, max_words: Optional[int] = None, add_source: bool = False) -> Optional[str]:
    """
    Асинхронно извлекает текст из веб-страницы и применяет scrape_text.

    Args:
        session (ClientSession): Сессия aiohttp.
        url (str): URL веб-страницы.
        max_words (Optional[int], optional): Максимальное количество слов для извлечения. По умолчанию None.
        add_source (bool, optional): Добавлять ли источник в конце текста. По умолчанию False.

    Returns:
        Optional[str]: Извлеченный текст или None в случае ошибки.
    """
    try:
        bucket_dir: Path = Path(get_cookies_dir()) / '.scrape_cache' / 'fetch_and_scrape'
        bucket_dir.mkdir(parents=True, exist_ok=True)
        md5_hash = hashlib.md5(url.encode(errors='ignore')).hexdigest()
        cache_file = bucket_dir / f'{quote_plus(url.split('?')[0].split('//')[1].replace('/', ' ')[:48])}.{datetime.date.today()}.{md5_hash[:16]}.cache'
        if cache_file.exists():
            return cache_file.read_text()
        async with session.get(url) as response:
            if response.status == 200:
                html = await response.text(errors='replace')
                text = ''.join(scrape_text(html, max_words, add_source))
                with open(cache_file, 'wb') as f:
                    f.write(text.encode(errors='replace'))
                return text
    except (ClientError, asyncio.TimeoutError) as ex:
        logger.error(f'Error while fetching and scraping {url}', ex, exc_info=True)
        return None


async def search(query: str, max_results: int = 5, max_words: int = 2500, backend: str = 'auto', add_text: bool = True, timeout: int = 5, region: str = 'wt-wt') -> SearchResults:
    """
    Выполняет поиск в DuckDuckGo.

    Args:
        query (str): Поисковый запрос.
        max_results (int, optional): Максимальное количество результатов. По умолчанию 5.
        max_words (int, optional): Максимальное количество слов для извлечения из каждой страницы. По умолчанию 2500.
        backend (str, optional): Бэкенд для поиска. По умолчанию 'auto'.
        add_text (bool, optional): Извлекать ли полный текст из результатов поиска. По умолчанию True.
        timeout (int, optional): Таймаут для запросов. По умолчанию 5.
        region (str, optional): Регион поиска. По умолчанию 'wt-wt'.

    Returns:
        SearchResults: Результаты поиска.

    Raises:
        MissingRequirementsError: Если не установлены необходимые библиотеки.
    """
    if not has_requirements:
        raise MissingRequirementsError('Install "duckduckgo-search" and "beautifulsoup4" package | pip install -U g4f[search]')

    results = []
    for result in ddgs.text(
        query,
        region=region,
        safesearch='moderate',
        timelimit='y',
        max_results=max_results,
        backend=backend,
    ):
        if '.google.' in result['href']:
            continue
        results.append(SearchResultEntry(
            result['title'],
            result['href'],
            result['body']
        ))

    if add_text:
        requests = []
        async with ClientSession(timeout=ClientTimeout(timeout)) as session:
            for entry in results:
                requests.append(fetch_and_scrape(session, entry.url, int(max_words / (max_results - 1)), False))
            texts = await asyncio.gather(*requests)

    formatted_results = []
    used_words = 0
    left_words = max_words
    for i, entry in enumerate(results):
        if add_text:
            entry.text = texts[i]
        if max_words:
            left_words -= entry.title.count(' ') + 5
            if entry.text:
                left_words -= entry.text.count(' ')
            else:
                left_words -= entry.snippet.count(' ')
            if 0 > left_words:
                break
        used_words = max_words - left_words
        formatted_results.append(entry)

    return SearchResults(formatted_results, used_words)


async def do_search(prompt: str, query: Optional[str] = None, instructions: str = DEFAULT_INSTRUCTIONS, **kwargs) -> tuple[str, Sources]:
    """
    Выполняет поиск и формирует prompt для языковой модели.

    Args:
        prompt (str): Исходный prompt.
        query (Optional[str], optional): Поисковый запрос. Если None, используется первая строка prompt. По умолчанию None.
        instructions (str, optional): Инструкции для языковой модели. По умолчанию DEFAULT_INSTRUCTIONS.
        **kwargs: Дополнительные аргументы для функции search.

    Returns:
        tuple[str, Sources]: Новый prompt и источники результатов поиска.
    """
    if instructions and instructions in prompt:
        return prompt, None  # We have already added search results
    if prompt.startswith('##') and query is None:
        return prompt, None  # We have no search query
    if query is None:
        query = prompt.strip().splitlines()[0]  # Use the first line as the search query
    json_bytes = json.dumps({'query': query, **kwargs}, sort_keys=True).encode(errors='ignore')
    md5_hash = hashlib.md5(json_bytes).hexdigest()
    bucket_dir: Path = Path(get_cookies_dir()) / '.scrape_cache' / f'web_search' / f'{datetime.date.today()}'
    bucket_dir.mkdir(parents=True, exist_ok=True)
    cache_file = bucket_dir / f'{quote_plus(query[:20])}.{md5_hash}.cache'
    search_results = None
    if cache_file.exists():
        try:
            search_results = SearchResults.from_dict(json.loads(cache_file.read_text()))
        except (json.JSONDecodeError, OSError) as ex:
            logger.error(f'Error while reading cache file {cache_file}', ex, exc_info=True)
            search_results = None
    if search_results is None:
        search_results = await search(query, **kwargs)
        if search_results.results:
            try:
                with open(cache_file, 'w') as f:
                    f.write(json.dumps(search_results.get_dict()))
            except OSError as ex:
                logger.error(f'Error while writing cache file {cache_file}', ex, exc_info=True)
    if instructions:
        new_prompt = f"""
{search_results}

Instruction: {instructions}

User request:
{prompt}
"""
    else:
        new_prompt = f"""
{search_results}

{prompt}
"""
    debug.log(f"Web search: '{query.strip()[:50]}...'")
    debug.log(f"with {len(search_results.results)} Results {search_results.used_words} Words")
    return new_prompt, search_results.get_sources()


def get_search_message(prompt: str, raise_search_exceptions: bool = False, **kwargs) -> str:
    """
    Выполняет поиск и возвращает новый prompt.

    Args:
        prompt (str): Исходный prompt.
        raise_search_exceptions (bool, optional): Выбрасывать ли исключения, связанные с поиском. По умолчанию False.
        **kwargs: Дополнительные аргументы для функции do_search.

    Returns:
        str: Новый prompt.
    """
    try:
        return asyncio.run(do_search(prompt, **kwargs))[0]
    except (DuckDuckGoSearchException, MissingRequirementsError) as ex:
        if raise_search_exceptions:
            raise ex
        logger.error(f"Couldn't do web search: {ex.__class__.__name__}: {ex}", exc_info=True)
        return prompt


def spacy_get_keywords(text: str) -> list[str]:
    """
    Извлекает ключевые слова из текста с помощью spaCy.

    Args:
        text (str): Текст для извлечения ключевых слов.

    Returns:
        list[str]: Список ключевых слов.
    """
    if not has_spacy:
        return [text]

    # Load the spaCy language model
    nlp = spacy.load('en_core_web_sm')

    # Process the query
    doc = nlp(text)

    # Extract keywords based on POS and named entities
    keywords = []
    for token in doc:
        # Filter for nouns, proper nouns, and adjectives
        if token.pos_ in {'NOUN', 'PROPN', 'ADJ'} and not token.is_stop:
            keywords.append(token.lemma_)

    # Add named entities as keywords
    for ent in doc.ents:
        keywords.append(ent.text)

    # Remove duplicates and print keywords
    keywords = list(set(keywords))
    # print("Keyword:", keywords)

    # keyword_freq = Counter(keywords)
    # keywords = keyword_freq.most_common()
    # print("Keyword Frequencies:", keywords)

    keywords = [chunk.text for chunk in doc.noun_chunks if not chunk.root.is_stop]
    # print("Phrases:", keywords)

    return keywords