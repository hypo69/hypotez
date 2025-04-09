### **Анализ кода модуля `search.py`**

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код выполняет поиск информации о фильмах/сериалах на Kinopoisk через Google.
    - Используется `BeautifulSoup` для парсинга HTML, что упрощает извлечение данных.
    - Функция `search_query` возвращает словарь с информацией о фильме/сериале.
- **Минусы**:
    - Отсутствуют аннотации типов для переменных и функций.
    - Не используется модуль `logger` для логирования.
    - Не обрабатываются возможные исключения при запросе к Google.
    - Не используется `j_loads` для работы с `.env`.
    - Не указаны типы данных для параметров и возвращаемых значений функций.
    - Отсутствует документация модуля.
    - Смешанный стиль кавычек (используются как одинарные, так и двойные).
    - Не используется webdriver для работы с сайтом
    - Не корректно формируется `link`

**Рекомендации по улучшению:**

1.  **Добавить аннотации типов**:
    - Указать типы данных для всех переменных и параметров функций.
2.  **Использовать логирование**:
    - Заменить `print` на `logger.info` или `logger.debug` для отладочной информации.
    - Добавить логирование ошибок с использованием `logger.error`.
3.  **Обработка исключений**:
    - Обернуть запрос к Google в блок `try...except` для обработки возможных ошибок (например, `requests.exceptions.RequestException`).
4.  **Использовать `j_loads`**:
    - Заменить `load_dotenv()` на использование `j_loads` или `j_loads_ns` для загрузки переменных окружения.
5.  **Добавить документацию**:
    - Добавить docstring для модуля и каждой функции, описывающий их назначение, параметры и возвращаемые значения.
6.  **Форматирование кода**:
    - Использовать только одинарные кавычки.
    - Добавить пробелы вокруг операторов присваивания.
7.  **Исправить формирование `link`**:
    - Убедиться, что ссылка формируется корректно и ведет на страницу фильма/сериала на Kinopoisk.
8.  **Использовать webdriver**
    - Использовать webdriver для работы с сайтом, вместо парсинга HTML

**Оптимизированный код:**

```python
"""
Модуль для поиска фильмов и сериалов на Kinopoisk через Google.
==============================================================

Модуль содержит функцию :func:`search_query`, которая выполняет поиск информации о фильме или сериале
на сайте Kinopoisk через поисковую систему Google и возвращает словарь с результатами.

Пример использования:
----------------------

>>>search_query('теория большого взрыва')
{'link': 'https://w2.kpfr.wiki/series/12345/', 'title': 'Теория большого взрыва - Kinopoisk', 'description': 'Описание сериала...'}
"""
import os
from typing import Optional

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from requests import get
from src.logger import logger #Используем logger для логирования
from apps.useragent import get_useragent


load_dotenv()


def search_query(query: str, type_movie: str = 'series') -> Optional[dict]:
    """
    Выполняет поиск информации о фильме или сериале на Kinopoisk через Google.

    Args:
        query (str): Поисковой запрос.
        type_movie (str, optional): Тип контента ('series' или 'movie'). По умолчанию 'series'.

    Returns:
        Optional[dict]: Словарь с информацией о фильме/сериале, содержащий:
            - link (str): Ссылка на страницу фильма/сериала на Kinopoisk.
            - title (str): Заголовок страницы.
            - description (str): Краткое описание фильма/сериала.
            Возвращает None, если ничего не найдено.

    Raises:
        requests.exceptions.RequestException: Если происходит ошибка при выполнении запроса к Google.

    Example:
        >>> search_query('теория большого взрыва')
        {'link': 'https://w2.kpfr.wiki/series/12345/', 'title': 'Теория большого взрыва - Kinopoisk', 'description': 'Описание сериала...'}
    """
    term: str = f'site:www.kinopoisk.ru/{type_movie} {query}'  # Формируем поисковой запрос для Google
    try:
        resp = get( # Выполняем GET-запрос к Google
            url='https://www.google.com/search',
            headers={'User-Agent': get_useragent()},  # Используем User-Agent для имитации запроса от браузера
            params={'q': term, 'hl': 'ru'}, # Параметры запроса: поисковой запрос и язык
            timeout=5 #Задаем таймаут для запроса
        )
        resp.raise_for_status()  # Проверяем статус код ответа, чтобы убедиться, что запрос успешен

        soup = BeautifulSoup(resp.text, 'html.parser') # Создаем объект BeautifulSoup для парсинга HTML
        result_block = soup.find_all('div', attrs={'class': 'g'}) # Ищем все блоки с результатами поиска

        if result_block:
            for result in result_block: #Перебираем результаты поиска
                link = result.find('a', href=True) #Извлекаем ссылку
                title = result.find('h3') #Извлекаем заголовок
                description = result.find('div', {'style': '-webkit-line-clamp:2'}) #Извлекаем описание

                if link and title and description: #Проверяем, что все элементы найдены
                    try:
                        if link['href'].split('/')[-2].isdigit(): #Проверяем, что предпоследний элемент ссылки является числом (id фильма/сериала)
                            movie_id: str = link['href'].split('/')[-2] #Извлекаем id фильма/сериала
                            return { #Возвращаем словарь с информацией о фильме/сериале
                                'link': f'https://w2.kpfr.wiki/{type_movie}/{movie_id}/', #Формируем ссылку на страницу фильма/сериала
                                'title': title.text, #Заголовок страницы
                                'description': description.text[:-4] + '...', #Описание фильма/сериала
                            }
                    except Exception as ex:
                        logger.error('Error while processing link', ex, exc_info=True) #Логируем ошибку при обработке ссылки
        return None #Если ничего не найдено, возвращаем None
    except Exception as ex:
        logger.error('Error while making request to Google', ex, exc_info=True) #Логируем ошибку при выполнении запроса к Google
        return None


if __name__ == '__main__':
    print(search_query('теория большого взрыва'))