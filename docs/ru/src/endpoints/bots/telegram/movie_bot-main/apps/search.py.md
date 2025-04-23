# Модуль для поиска фильмов и сериалов на Kinopoisk

## Обзор

Модуль `search.py` предназначен для поиска фильмов и сериалов на сайте Kinopoisk через поисковую систему Google. Он использует библиотеку `BeautifulSoup` для парсинга HTML-ответа и извлечения необходимой информации о фильме или сериале. Модуль также использует `requests` для выполнения HTTP-запросов.

## Подробнее

Модуль выполняет поиск на Kinopoisk, формируя поисковый запрос для Google, а затем извлекает релевантную информацию о фильмах или сериалах. Основная функция модуля - `search_query`.

## Функции

### `search_query`

```python
def search_query(query: str, type_movie: str = 'series') -> dict | None:
    """
    Выполняет поиск фильма или сериала на Kinopoisk через Google.

    Args:
        query (str): Поисковый запрос.
        type_movie (str, optional): Тип искомого контента ('series' или 'movie'). По умолчанию 'series'.

    Returns:
        dict | None: Словарь с информацией о фильме/сериале (ссылка, заголовок, описание) или None, если ничего не найдено.

    Raises:
        RequestException: Если возникает ошибка при выполнении HTTP-запроса.
        HTTPError: Если HTTP-запрос возвращает код ошибки.
        ConnectionError: Если не удаётся установить соединение.
        Timeout: Если время ожидания истекло.

    Внутренние функции:
        отсутствуют

    Как работает функция:
    1. Формирует поисковый запрос для Google, включающий указанный `query` и тип контента (`type_movie`).
    2. Выполняет HTTP-запрос к Google с использованием библиотеки `requests`.
    3. Использует `BeautifulSoup` для парсинга HTML-ответа, полученного от Google.
    4. Ищет блоки с результатами поиска (`div` с классом "g").
    5. Перебирает найденные блоки, извлекая ссылку, заголовок и описание.
    6. Проверяет, что ссылка ведет на страницу Kinopoisk, идентифицируя её по числовому идентификатору в URL.
    7. Если все условия выполнены, возвращает словарь с извлеченной информацией.
    8. Если ничего не найдено, возвращает `None`.

    Примеры:
    >>> search_query('теория большого взрыва')
    {'link': 'https://w2.kpfr.wiki/series/666', 'title': 'Теория большого взрыва (сериал 2007 – 2019) — The Big Bang ...', 'description': 'The Big Bang Theory. 2007–2019 16+. 21 мин. ... Смотрите сериал «Теория большого взрыва» онлайн в отличном качестве'}

    >>> search_query('matrix', type_movie='movie')
    {'link': 'https://w2.kpfr.wiki/movie/355', 'title': 'Матрица (1999) — The Matrix — Кинопоиск', 'description': 'The Matrix. 1999. США, Австралия. 136 мин. ... Неожиданно для себя программист Томас Андерсон узнает, что все вокруг него — нереально.'}
    """
    term = f'site:www.kinopoisk.ru/{type_movie} {query}'
    resp = get(
        url="https://www.google.com/search",
        headers={"User-Agent": get_useragent()},
        params={"q": term, "hl": "ru"},
        timeout=5
    )
    soup = BeautifulSoup(resp.text, "html.parser")
    result_block = soup.find_all("div", attrs={"class": "g"})
    if result_block:
        for result in result_block:
            link = result.find("a", href=True)
            title = result.find("h3")
            description = result.find("div", {"style": "-webkit-line-clamp:2"})
            if link and title and description:
                if link["href"].split("/")[-2].isdigit():
                    return {
                        'link': f'https://w2.kpfr.wiki/{type_movie}/'
                                f'{link["href"].split("/")[-2]}',
                        'title': title.text,
                        'description': description.text[:-4] + '...',
                    }
    return None