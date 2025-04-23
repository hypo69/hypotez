### Как использовать этот блок кода

=========================================================================================

Описание
-------------------------
Данный код выполняет поиск фильма или сериала на сайте Kinopoisk.ru через поисковую систему Google. Он формирует поисковый запрос, отправляет его в Google, анализирует полученные результаты и извлекает ссылку, заголовок и описание фильма/сериала.

Шаги выполнения
-------------------------
1. **Импорт необходимых библиотек**: Импортируются библиотеки `os`, `BeautifulSoup`, `load_dotenv`, `get` и `get_useragent`.
2. **Загрузка переменных окружения**: Вызывается функция `load_dotenv()` для загрузки переменных окружения из файла `.env`.
3. **Определение функции `search_query`**:
   - Функция принимает два аргумента: `query` (поисковый запрос) и `type_movie` (тип контента: "series" или "movie", по умолчанию "series").
   - Формируется поисковый запрос `term` для Google, включающий указание сайта Kinopoisk.ru и поисковый запрос пользователя.
   - Отправляется GET-запрос к Google с использованием библиотеки `requests`:
     - URL: `"https://www.google.com/search"`
     - Заголовки: `{"User-Agent": get_useragent()}` (используется случайный User-Agent для избежания блокировок).
     - Параметры: `{"q": term, "hl": "ru"}` (поисковый запрос и язык результатов).
     - `timeout=5` (максимальное время ожидания ответа - 5 секунд).
   - Полученный HTML-код страницы передается в библиотеку `BeautifulSoup` для парсинга.
   - Выполняется поиск всех блоков `div` с классом `"g"`, которые содержат результаты поиска.
   - Если блоки результатов найдены, выполняется итерация по каждому блоку:
     - Извлекается ссылка `a` с атрибутом `href`.
     - Извлекается заголовок `h3`.
     - Извлекается описание `div` с атрибутом `style` в виде `-webkit-line-clamp:2`.
     - Проверяется наличие ссылки, заголовка и описания.
     - Проверяется, является ли предпоследний элемент URL-адреса числом (идентификатором фильма/сериала на Kinopoisk).
     - Если все условия выполнены, формируется словарь с данными о фильме/сериале:
       - `'link'`: Ссылка на фильм/сериал на сайте `w2.kpfr.wiki` с использованием идентификатора.
       - `'title'`: Заголовок фильма/сериала.
       - `'description'`: Описание фильма/сериала (обрезается до определенной длины и добавляется "...")
     - Возвращается словарь с результатами.
   - Если результаты не найдены, возвращается `None`.
4. **Пример использования**:
   - Если скрипт запущен как главный (`if __name__ == '__main__':`), вызывается функция `search_query` с запросом "теория большого взрыва".
   - Результат выводится в консоль с помощью функции `print`.

Пример использования
-------------------------

```python
import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from requests import get

from apps.useragent import get_useragent

load_dotenv()


def search_query(query, type_movie='series'):
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


if __name__ == '__main__':
    print(search_query('теория большого взрыва'))