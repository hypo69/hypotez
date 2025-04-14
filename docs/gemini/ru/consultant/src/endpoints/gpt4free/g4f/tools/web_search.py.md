### **Анализ кода модуля `web_search.py`**

**Качество кода**:
- **Соответствие стандартам**: 6/10
- **Плюсы**:
  - Использование `asyncio` для асинхронных операций.
  - Кэширование результатов поиска для повышения производительности.
  - Разбиение кода на логические блоки (функции, классы).
  - Использование `JsonMixin` для удобной работы с JSON.
- **Минусы**:
  - Недостаточное количество аннотаций типов.
  - Смешанный стиль кавычек (используются как одинарные, так и двойные кавычки).
  - Отсутствие документации для некоторых функций и классов.
  - Не везде используется `logger` для логирования ошибок.
  - Не все переменные аннотированы типами.

**Рекомендации по улучшению**:

1.  **Добавить аннотации типов**:
    - Добавить аннотации типов для всех переменных и возвращаемых значений функций.

2.  **Улучшить документацию**:
    - Добавить docstring для функций `scrape_text`, `fetch_and_scrape`, `spacy_get_keywords`.
    - Описать параметры и возвращаемые значения в docstring.

3.  **Унифицировать стиль кавычек**:
    - Использовать только одинарные кавычки (`'`) для строк.

4.  **Использовать `logger` для логирования**:
    - Заменить `print` на `logger.debug` или `logger.info` для отладочной информации.
    - Логировать ошибки с использованием `logger.error`.

5.  **Улучшить обработку исключений**:
    - Использовать `ex` вместо `e` в блоках `except`.
    - Добавить логирование ошибок с использованием `logger.error(..., exc_info=True)`.

6.  **Переработать кэширование**:
    - Использовать `j_loads` и `j_dumps` для работы с кэш-файлами.

7.  **Удалить неиспользуемый код**:
    - Удалить закомментированные строки кода (например, `print("Keyword:", keywords)`).

8.  **Перевести комментарии на русский язык**:
    - Перевести все комментарии и docstring на русский язык.

9. **Улучшить читаемость**:
    - Добавить пробелы вокруг операторов присваивания.

**Оптимизированный код**:

```python
"""
Модуль для выполнения веб-поиска с использованием DuckDuckGo Search.
=====================================================================

Модуль содержит классы и функции для выполнения веб-поиска, извлечения текста из веб-страниц
и кэширования результатов для повышения производительности.
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
    has_requirements: bool = True  # Указывает, установлены ли необходимые зависимости
except ImportError:
    has_requirements: bool = False
try:
    import spacy

    has_spacy: bool = True
except:
    has_spacy: bool = False

from typing import Iterator, Optional, List
from ..cookies import get_cookies_dir
from ..providers.response import format_link, JsonMixin, Sources
from ..errors import MissingRequirementsError
from .. import debug
from src.logger import logger

DEFAULT_INSTRUCTIONS: str = """
Используя предоставленные результаты веб-поиска, напишите исчерпывающий ответ на запрос пользователя.
Обязательно добавьте источники цитат, используя обозначение [[Номер]](Url) после ссылки. Пример: [[0]](http://google.com)
"""


class SearchResults(JsonMixin):
    """
    Класс для хранения результатов поиска.
    """

    def __init__(self, results: list, used_words: int):
        """
        Инициализирует экземпляр класса SearchResults.

        Args:
            results (list): Список результатов поиска.
            used_words (int): Количество использованных слов.
        """
        self.results: list = results
        self.used_words: int = used_words

    @classmethod
    def from_dict(cls, data: dict) -> SearchResults:
        """
        Создает экземпляр класса SearchResults из словаря.

        Args:
            data (dict): Словарь с данными для создания SearchResults.

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
        search: str = ''
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
    Класс для хранения отдельной записи результата поиска.
    """

    def __init__(self, title: str, url: str, snippet: str, text: Optional[str] = None):
        """
        Инициализирует экземпляр класса SearchResultEntry.

        Args:
            title (str): Заголовок результата поиска.
            url (str): URL результата поиска.
            snippet (str): Краткое описание результата поиска.
            text (Optional[str]): Полный текст результата поиска. По умолчанию None.
        """
        self.title: str = title
        self.url: str = url
        self.snippet: str = snippet
        self.text: Optional[str] = text

    def set_text(self, text: str):
        """
        Устанавливает полный текст результата поиска.

        Args:
            text (str): Полный текст результата поиска.
        """
        self.text: str = text


def scrape_text(html: str, max_words: Optional[int] = None, add_source: bool = True, count_images: int = 2) -> Iterator[str]:
    """
    Извлекает текст из HTML-кода веб-страницы.

    Args:
        html (str): HTML-код веб-страницы.
        max_words (Optional[int]): Максимальное количество слов для извлечения. По умолчанию None.
        add_source (bool): Добавлять ли источник в конце извлеченного текста. По умолчанию True.
        count_images (int): Количество изображений для включения в результат. По умолчанию 2.

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
    yield_words: list[str] = []
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
    Асинхронно извлекает и очищает текст с веб-страницы.

    Args:
        session (ClientSession): Асинхронная сессия для выполнения HTTP-запросов.
        url (str): URL веб-страницы.
        max_words (Optional[int]): Максимальное количество слов для извлечения. По умолчанию None.
        add_source (bool): Добавлять ли источник в конце извлеченного текста. По умолчанию False.

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
        logger.error('Ошибка при получении или обработке веб-страницы', ex, exc_info=True)
        return None


async def search(query: str, max_results: int = 5, max_words: int = 2500, backend: str = 'auto', add_text: bool = True, timeout: int = 5, region: str = 'wt-wt') -> SearchResults:
    """
    Выполняет поиск в DuckDuckGo.

    Args:
        query (str): Поисковый запрос.
        max_results (int): Максимальное количество результатов. По умолчанию 5.
        max_words (int): Максимальное количество слов для извлечения из каждого результата. По умолчанию 2500.
        backend (str): Бэкенд для поиска. По умолчанию 'auto'.
        add_text (bool): Добавлять ли текст из веб-страниц в результаты. По умолчанию True.
        timeout (int): Время ожидания для HTTP-запросов. По умолчанию 5.
        region (str): Регион поиска. По умолчанию 'wt-wt'.

    Returns:
        SearchResults: Результаты поиска.

    Raises:
        MissingRequirementsError: Если не установлены необходимые зависимости.
    """
    if not has_requirements:
        raise MissingRequirementsError('Установите пакет "duckduckgo-search" и "beautifulsoup4" | pip install -U g4f[search]')

    results: list[SearchResultEntry] = []
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
        requests: list[asyncio.Task] = []
        async with ClientSession(timeout=ClientTimeout(timeout)) as session:
            for entry in results:
                requests.append(fetch_and_scrape(session, entry.url, int(max_words / (max_results - 1)), False))
            texts: list[Optional[str]] = await asyncio.gather(*requests)

    formatted_results: list[SearchResultEntry] = []
    used_words: int = 0
    left_words: int = max_words
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


async def do_search(prompt: str, query: Optional[str] = None, instructions: str = DEFAULT_INSTRUCTIONS, **kwargs) -> tuple[str, Optional[Sources]]:
    """
    Выполняет поиск и форматирует результаты для использования в запросе.

    Args:
        prompt (str): Исходный запрос пользователя.
        query (Optional[str]): Поисковый запрос. Если None, используется первая строка запроса. По умолчанию None.
        instructions (str): Инструкции для форматирования результатов. По умолчанию DEFAULT_INSTRUCTIONS.
        **kwargs: Дополнительные параметры для функции search.

    Returns:
        tuple[str, Optional[Sources]]: Отформатированный запрос и источники результатов поиска.
    """
    if instructions and instructions in prompt:
        return prompt, None  # Мы уже добавили результаты поиска
    if prompt.startswith('##') and query is None:
        return prompt, None  # У нас нет поискового запроса
    if query is None:
        query = prompt.strip().splitlines()[0]  # Используйте первую строку в качестве поискового запроса
    json_bytes = json.dumps({'query': query, **kwargs}, sort_keys=True).encode(errors='ignore')
    md5_hash = hashlib.md5(json_bytes).hexdigest()
    bucket_dir: Path = Path(get_cookies_dir()) / '.scrape_cache' / f'web_search' / f'{datetime.date.today()}'
    bucket_dir.mkdir(parents=True, exist_ok=True)
    cache_file = bucket_dir / f'{quote_plus(query[:20])}.{md5_hash}.cache'
    search_results: Optional[SearchResults] = None
    if cache_file.exists():
        with cache_file.open('r') as f:
            search_results = f.read()
        try:
            search_results = SearchResults.from_dict(json.loads(search_results))
        except json.JSONDecodeError:
            search_results = None
    if search_results is None:
        search_results = await search(query, **kwargs)
        if search_results.results:
            with cache_file.open('w') as f:
                f.write(json.dumps(search_results.get_dict()))
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
    debug.log(f'Web search: \'{query.strip()[:50]}...\'')
    debug.log(f'with {len(search_results.results)} Results {search_results.used_words} Words')
    return new_prompt, search_results.get_sources()


def get_search_message(prompt: str, raise_search_exceptions: bool = False, **kwargs) -> str:
    """
    Выполняет поиск и возвращает отформатированное сообщение.

    Args:
        prompt (str): Исходный запрос пользователя.
        raise_search_exceptions (bool): Выбрасывать ли исключения, связанные с поиском. По умолчанию False.
        **kwargs: Дополнительные параметры для функции do_search.

    Returns:
        str: Отформатированное сообщение.
    """
    try:
        return asyncio.run(do_search(prompt, **kwargs))[0]
    except (DuckDuckGoSearchException, MissingRequirementsError) as ex:
        if raise_search_exceptions:
            raise ex
        debug.error(f'Не удалось выполнить веб-поиск: {ex.__class__.__name__}: {ex}')
        return prompt


def spacy_get_keywords(text: str) -> list[str]:
    """
    Извлекает ключевые слова из текста с использованием spaCy.

    Args:
        text (str): Исходный текст.

    Returns:
        list[str]: Список ключевых слов.
    """
    if not has_spacy:
        return text

    # Load the spaCy language model
    nlp = spacy.load('en_core_web_sm')

    # Process the query
    doc = nlp(text)

    # Extract keywords based on POS and named entities
    keywords: list[str] = []
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