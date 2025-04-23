# Модуль `search`

## Обзор

Модуль `search` предназначен для выполнения поисковых запросов к сайту Kinopoisk через поисковую систему Google и извлечения результатов поиска. Он использует библиотеки `BeautifulSoup` для парсинга HTML-кода и `requests` для выполнения HTTP-запросов. Модуль позволяет искать фильмы и сериалы на Kinopoisk, получая ссылки, заголовки и описания найденных ресурсов.

## Более детально

Этот модуль играет роль поискового инструмента, который позволяет пользователям находить информацию о фильмах и сериалах на сайте Kinopoisk, используя поисковую систему Google. Он отправляет поисковой запрос, анализирует полученный HTML-код и извлекает необходимые данные. Это может быть полезно для автоматизации поиска информации о фильмах и сериалах, например, для создания ботов или скриптов, собирающих данные о кинопродукции.

## Функции

### `search_query`

```python
def search_query(query, type_movie='series'):
    """
    Выполняет поисковой запрос к сайту Kinopoisk через поисковую систему Google и извлекает результаты.

    Args:
        query (str): Поисковой запрос.
        type_movie (str): Тип искомого контента ('series' или 'movie'). По умолчанию 'series'.

    Returns:
        dict | None: Словарь с информацией о найденном фильме/сериале (ссылка, заголовок, описание) или None, если ничего не найдено.

    Raises:
        requests.exceptions.RequestException: Если возникает ошибка при выполнении HTTP-запроса.
        bs4.exceptions.BeautifulSoup: Если возникает ошибка при парсинге HTML-кода.

    Принцип работы:
        - Формирует поисковой запрос для Google с указанием сайта Kinopoisk и типа контента.
        - Отправляет HTTP-запрос к Google с использованием случайного User-Agent.
        - Парсит HTML-код ответа с помощью BeautifulSoup.
        - Находит блоки с результатами поиска.
        - Извлекает ссылку, заголовок и описание из каждого результата.
        - Проверяет, является ли ссылка ссылкой на Kinopoisk.
        - Если все условия выполнены, возвращает словарь с информацией о фильме/сериале.
        - Если ничего не найдено, возвращает None.

    Примеры:
        >>> search_query('теория большого взрыва')
        {'link': 'https://w2.kpfr.wiki/series/666', 'title': 'Теория большого взрыва', 'description': 'Описание сериала...'}

        >>> search_query('Игра престолов', type_movie='series')
        {'link': 'https://w2.kpfr.wiki/series/46131', 'title': 'Игра престолов', 'description': 'Описание сериала...'}

        >>> search_query('Звездные войны', type_movie='movie')
        {'link': 'https://w2.kpfr.wiki/movie/111', 'title': 'Звездные войны', 'description': 'Описание фильма...'}
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

```
## Параметры функции `search_query`

-   `query` (str): Поисковой запрос.
-   `type_movie` (str, optional): Тип искомого контента ('series' или 'movie'). По умолчанию 'series'.

## Примеры вызова функции `search_query`

```python
search_query('теория большого взрыва')
# {'link': 'https://w2.kpfr.wiki/series/666', 'title': 'Теория большого взрыва', 'description': 'Описание сериала...'}

search_query('Игра престолов', type_movie='series')
# {'link': 'https://w2.kpfr.wiki/series/46131', 'title': 'Игра престолов', 'description': 'Описание сериала...'}

search_query('Звездные войны', type_movie='movie')
# {'link': 'https://w2.kpfr.wiki/movie/111', 'title': 'Звездные войны', 'description': 'Описание фильма...'}