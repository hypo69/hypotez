# Module: `apps/search.py`

## Overview

This module provides functionality for searching for movies and TV series using the Kinopoisk website. It utilizes Google Search to retrieve relevant results, then parses the HTML response to extract key information such as the movie's title, description, and Kinopoisk link.

## Details

This module is part of the `hypotez` project and is designed to be integrated into the `movie_bot-main` application for Telegram. The `search_query` function is the core component of this module and leverages Google Search to locate relevant information for movie and TV series titles.

## Classes

### `search_query`

**Description**: This function performs a search query for movies or TV series using Google Search and retrieves information about the results from the Kinopoisk website.

**Parameters**:

- `query` (str): The search term (movie or TV series title) to be used in the Google Search query.
- `type_movie` (str): The type of movie or TV series to search for (either `series` or `movie`). Defaults to `series`.

**Returns**:

- `dict | None`:  If successful, it returns a dictionary containing the title, description, and Kinopoisk link of the movie or TV series. If no relevant results are found, it returns `None`.

**Raises Exceptions**:

- `Exception`: If there is an error during the web request or HTML parsing process.

**How the Function Works**:

1. **Formulates a search query**: It constructs a search term specifically for Kinopoisk using the provided `query` and `type_movie` arguments.
2. **Sends a Google Search request**: It utilizes the `requests` library to send a GET request to Google Search with the formulated search term and relevant headers.
3. **Parses the HTML response**: It uses `BeautifulSoup` to parse the HTML content returned from Google Search.
4. **Extracts relevant information**: The parsed HTML is then analyzed to identify and extract the title, description, and link to the movie or TV series on the Kinopoisk website.
5. **Returns the result**: The extracted information is packaged into a dictionary and returned. If no relevant results are found, it returns `None`.

**Examples**:

```python
>>> print(search_query('теория большого взрыва')) # Searching for the TV series 'The Big Bang Theory'
{'link': 'https://w2.kpfr.wiki/series/8246', 'title': 'Теория большого взрыва', 'description': '«Теория большого взрыва» — американский ситком о жизни группы молодых людей, работающих в Калифорнийском технологическом институте в ...'}
```
```python
>>> print(search_query('Властелин колец', type_movie='movie')) # Searching for the movie 'The Lord of the Rings'
{'link': 'https://w2.kpfr.wiki/movie/1075', 'title': 'Властелин колец: Братство Кольца', 'description': 'Война за Средиземье приближается. Темный властелин Саурон, желающий захватить ...'}
```

## Inner Functions

This module does not contain any inner functions.

## Parameter Details

- `query` (str): The search term (movie or TV series title) to be used in the Google Search query.
- `type_movie` (str): The type of movie or TV series to search for (either `series` or `movie`). Defaults to `series`.


## Examples

```python
>>> print(search_query('теория большого взрыва'))
{'link': 'https://w2.kpfr.wiki/series/8246', 'title': 'Теория большого взрыва', 'description': '«Теория большого взрыва» — американский ситком о жизни группы молодых людей, работающих в Калифорнийском технологическом институте в ...'}
```

```python
>>> print(search_query('Властелин колец', type_movie='movie'))
{'link': 'https://w2.kpfr.wiki/movie/1075', 'title': 'Властелин колец: Братство Кольца', 'description': 'Война за Средиземье приближается. Темный властелин Саурон, желающий захватить ...'}
```