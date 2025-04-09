### **Анализ кода модуля `web_search.py`**

**Расположение файла в проекте:** `hypotez/src/endpoints/gpt4free/g4f/tools/web_search.py`

**Назначение модуля:** Модуль предоставляет функциональность для выполнения веб-поиска с использованием DuckDuckGoSearch, извлечения текста из веб-страниц и форматирования результатов для использования в запросах к языковым моделям.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Четкая структура кода, разделение на функции и классы.
  - Использование `JsonMixin` для сериализации и десериализации данных.
  - Кэширование результатов веб-поиска для повышения производительности.
  - Обработка исключений при веб-поиске и извлечении данных.
  - Наличие аннотаций типов.
- **Минусы**:
  - Не все функции и классы имеют подробные docstring.
  - Отсутствуют логи.
  - Смешанный стиль кавычек (используются как одинарные, так и двойные кавычки).
  - Не все переменные аннотированы типами.
  - Использование `Union` вместо `|`.

**Рекомендации по улучшению:**

1.  **Документация**:
    - Добавить docstring для всех функций, классов и методов, включая подробное описание аргументов, возвращаемых значений и возможных исключений.
    - Перевести существующие docstring на русский язык.
    - Документировать внутренние функции, например, `scrape_text`.
    - Для класса `SearchResults` необходимо добавить пример использования в docstring.
    - Описание модуля в начале файла.

2.  **Логирование**:
    - Добавить логирование для отслеживания хода выполнения программы, особенно в функциях `search`, `fetch_and_scrape` и `do_search`.
    - Логировать ошибки с использованием `logger.error` и передавать информацию об исключении (`exc_info=True`).

3.  **Форматирование**:
    - Привести весь код к единому стилю кавычек (использовать только одинарные кавычки).
    - Добавить пробелы вокруг операторов присваивания.
    - Использовать `|` вместо `Union`.

4.  **Обработка исключений**:
    - Использовать `ex` вместо `e` в блоках обработки исключений.
    - Добавить обработку исключений в функции `scrape_text`.

5.  **Использование `j_loads` или `j_loads_ns`**:
    - Заменить стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns` при чтении кэшированных файлов.

6.  **Аннотации**:
    - Добавить аннотации типов для всех переменных, где это необходимо.

7.  **Улучшение производительности**:
    - Рассмотреть возможность использования асинхронных операций для параллельного выполнения веб-поиска и извлечения данных.

8.  **Безопасность**:
    - Проверить код на наличие уязвимостей безопасности, таких как SQL-инъекции или межсайтовый скриптинг (XSS).

9.  **Вебдрайвер**:
    - В данном коде вебдрайвер не используется.

**Оптимизированный код:**

```python
"""
Модуль для выполнения веб-поиска и извлечения информации из веб-страниц.
=======================================================================

Модуль содержит классы и функции для выполнения веб-поиска с использованием DuckDuckGoSearch,
извлечения текста из веб-страниц и форматирования результатов для использования в запросах к языковым моделям.

Пример использования:
----------------------

>>> from g4f.tools import web_search
>>> asyncio.run(web_search.do_search("Что такое Python?"))
"""
from __future__ import annotations

from aiohttp import ClientSession, ClientTimeout, ClientError
import json
import hashlib
from pathlib import Path
from urllib.parse import urlparse, quote_plus
from datetime import datetime
import datetime
import asyncio

try:
    from duckduckgo_search import DDGS
    from duckduckgo_search.exceptions import DuckDuckGoSearchException
    from bs4 import BeautifulSoup

    ddgs = DDGS()
    has_requirements = True
except ImportError:
    has_requirements = False
try:
    import spacy

    has_spacy = True
except:
    has_spacy = False

from typing import Iterator
from ..cookies import get_cookies_dir
from ..providers.response import format_link, JsonMixin, Sources
from ..errors import MissingRequirementsError
from .. import debug
from src.logger import logger

DEFAULT_INSTRUCTIONS = """
Using the provided web search results, to write a comprehensive reply to the user request.
Make sure to add the sources of cites using [[Number]](Url) notation after the reference. Example: [[0]](http://google.com)
"""


class SearchResults(JsonMixin):
    """
    Класс для хранения результатов веб-поиска.

    Args:
        results (list): Список объектов SearchResultEntry.
        used_words (int): Количество использованных слов.

    Returns:
        None

    Example:
        >>> results = [SearchResultEntry(title='Example', url='http://example.com', snippet='Example snippet')]
        >>> search_results = SearchResults(results=results, used_words=10)
        >>> print(search_results)
        Title: Example

        Example snippet

        Source: [[0]](http://example.com)
    """

    def __init__(self, results: list, used_words: int):
        self.results = results
        self.used_words = used_words

    @classmethod
    def from_dict(cls, data: dict):
        """
        Создает экземпляр класса из словаря.

        Args:
            data (dict): Словарь с данными.

        Returns:
            SearchResults: Экземпляр класса SearchResults.
        """
        return cls(
            [SearchResultEntry(**item) for item in data['results']],
            data['used_words']
        )

    def __iter__(self):
        """
        Возвращает итератор по результатам поиска.

        Yields:
            SearchResultEntry: Объект SearchResultEntry.
        """
        yield from self.results

    def __str__(self) -> str:
        """
        Форматирует результаты поиска в строку.

        Returns:
            str: Отформатированная строка с результатами поиска.
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
            Sources: Объект Sources с источниками.
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
    Класс для хранения отдельного результата веб-поиска.

    Args:
        title (str): Заголовок результата.
        url (str): URL результата.
        snippet (str): Сниппет результата.
        text (str, optional): Полный текст результата. По умолчанию None.
    """

    def __init__(self, title: str, url: str, snippet: str, text: str = None):
        self.title = title
        self.url = url
        self.snippet = snippet
        self.text = text

    def set_text(self, text: str):
        """
        Устанавливает полный текст результата.

        Args:
            text (str): Полный текст результата.
        """
        self.text = text


def scrape_text(html: str, max_words: int = None, add_source: bool = True, count_images: int = 2) -> Iterator[str]:
    """
    Извлекает текст из HTML-кода веб-страницы.

    Args:
        html (str): HTML-код веб-страницы.
        max_words (int, optional): Максимальное количество слов для извлечения. По умолчанию None.
        add_source (bool, optional): Добавлять ли источник в конце текста. По умолчанию True.
        count_images (int, optional): Максимальное количество изображений для извлечения. По умолчанию 2.

    Yields:
        str: Извлеченный текст.
    """
    try:
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
                        yield f'!{format_link(image['src'], title)}\\n'
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
                yield words + '\\n'
                yield_words.append(words)

        if add_source:
            canonical_link = source.find('link', rel='canonical')
            if canonical_link and 'href' in canonical_link.attrs:
                link = canonical_link['href']
                domain = urlparse(link).netloc
                yield f'\\nSource: [{domain}]({link})'
    except Exception as ex:
        logger.error('Error while scraping text', ex, exc_info=True)


async def fetch_and_scrape(session: ClientSession, url: str, max_words: int = None, add_source: bool = False) -> str | None:
    """
    Асинхронно загружает веб-страницу и извлекает из нее текст.

    Args:
        session (ClientSession): Сессия aiohttp.
        url (str): URL веб-страницы.
        max_words (int, optional): Максимальное количество слов для извлечения. По умолчанию None.
        add_source (bool, optional): Добавлять ли источник в конце текста. По умолчанию False.

    Returns:
        str | None: Извлеченный текст или None в случае ошибки.
    """
    try:
        bucket_dir: Path = Path(get_cookies_dir()) / '.scrape_cache' / 'fetch_and_scrape'
        bucket_dir.mkdir(parents=True, exist_ok=True)
        md5_hash = hashlib.md5(url.encode(errors='ignore')).hexdigest()
        cache_file = bucket_dir / f"{quote_plus(url.split('?')[0].split('//')[1].replace('/', ' ')[:48])}.{datetime.date.today()}.{md5_hash[:16]}.cache"
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
        logger.error('Error while fetching and scraping', ex, exc_info=True)
        return None


async def search(query: str, max_results: int = 5, max_words: int = 2500, backend: str = 'auto', add_text: bool = True, timeout: int = 5, region: str = 'wt-wt') -> SearchResults:
    """
    Выполняет веб-поиск с использованием DuckDuckGoSearch.

    Args:
        query (str): Поисковый запрос.
        max_results (int, optional): Максимальное количество результатов. По умолчанию 5.
        max_words (int, optional): Максимальное количество слов для извлечения из каждого результата. По умолчанию 2500.
        backend (str, optional): Бэкенд DuckDuckGoSearch. По умолчанию 'auto'.
        add_text (bool, optional): Извлекать ли текст из веб-страниц. По умолчанию True.
        timeout (int, optional): Таймаут для HTTP-запросов. По умолчанию 5.
        region (str, optional): Регион поиска. По умолчанию 'wt-wt'.

    Returns:
        SearchResults: Объект SearchResults с результатами поиска.

    Raises:
        MissingRequirementsError: Если не установлены необходимые пакеты.
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


async def do_search(prompt: str, query: str = None, instructions: str = DEFAULT_INSTRUCTIONS, **kwargs) -> tuple[str, Sources | None]:
    """
    Выполняет веб-поиск и форматирует результаты для использования в запросах к языковым моделям.

    Args:
        prompt (str): Исходный запрос пользователя.
        query (str, optional): Поисковый запрос. Если None, используется первая строка запроса пользователя. По умолчанию None.
        instructions (str, optional): Инструкции для языковой модели. По умолчанию DEFAULT_INSTRUCTIONS.
        **kwargs: Дополнительные аргументы для функции search.

    Returns:
        tuple[str, Sources | None]: Отформатированный запрос и источники результатов поиска.
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
    cache_file = bucket_dir / f"{quote_plus(query[:20])}.{md5_hash}.cache"
    search_results: SearchResults | None = None
    if cache_file.exists():
        try:
            search_results = SearchResults.from_dict(json.loads(cache_file.read_text()))
        except (json.JSONDecodeError, OSError) as ex:
            logger.error('Error while reading cache file', ex, exc_info=True)
            search_results = None
    if search_results is None:
        search_results = await search(query, **kwargs)
        if search_results.results:
            try:
                with open(cache_file, 'w') as f:
                    f.write(json.dumps(search_results.get_dict()))
            except OSError as ex:
                logger.error('Error while writing cache file', ex, exc_info=True)
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


def get_search_message(prompt: str, raise_search_exceptions=False, **kwargs) -> str:
    """
    Выполняет веб-поиск и возвращает отформатированный запрос.

    Args:
        prompt (str): Исходный запрос пользователя.
        raise_search_exceptions (bool, optional): Поднимать ли исключения при веб-поиске. По умолчанию False.
        **kwargs: Дополнительные аргументы для функции do_search.

    Returns:
        str: Отформатированный запрос.
    """
    try:
        return asyncio.run(do_search(prompt, **kwargs))[0]
    except (DuckDuckGoSearchException, MissingRequirementsError) as ex:
        if raise_search_exceptions:
            raise ex
        debug.error(f"Couldn't do web search: {ex.__class__.__name__}: {ex}")
        return prompt


def spacy_get_keywords(text: str) -> list[str] | str:
    """
    Извлекает ключевые слова из текста с использованием spaCy.

    Args:
        text (str): Исходный текст.

    Returns:
        list[str] | str: Список ключевых слов или исходный текст, если spaCy не установлен.
    """
    if not has_spacy:
        return text

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