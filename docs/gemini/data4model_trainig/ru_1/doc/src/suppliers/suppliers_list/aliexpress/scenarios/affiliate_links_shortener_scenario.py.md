# Модуль `affiliate_links_shortener_scenario.py`

## Обзор

Модуль предназначен для сокращения партнерских ссылок AliExpress с использованием веб-браузера. Он содержит функцию `get_short_affiliate_link`, которая автоматизирует процесс получения короткой ссылки через веб-интерфейс.

## Подробнее

Этот модуль предоставляет функциональность для автоматического сокращения длинных партнерских ссылок AliExpress до более удобного и короткого формата. Это достигается путем взаимодействия с веб-сайтом AliExpress через веб-драйвер, автоматического ввода длинной ссылки и получения короткой версии.

## Функции

### `get_short_affiliate_link`

**Назначение**: Получение сокращенной партнерской ссылки для заданного URL.

```python
def get_short_affiliate_link(d: Driver, url: str) -> str:
    """ Script for generating a shortened affiliate link
    @param url `str`: Full URL
    @returns `str`: Shortened URL
    """
    ...
```

**Параметры**:

-   `d` (`Driver`): Инстанс веб-драйвера для управления браузером.
-   `url` (`str`): Полный URL, который требуется сократить.

**Возвращает**:

-   `str`: Сокращенный URL или None в случае ошибки.

**Как работает функция**:

1.  Вводит URL в текстовое поле на странице.
2.  Нажимает кнопку для получения короткой ссылки.
3.  Ждет обновления страницы.
4.  Извлекает короткую ссылку из соответствующего элемента на странице.
5.  Открывает новую вкладку с полученной короткой ссылкой.
6.  Проверяет, не ведет ли короткая ссылка на страницу ошибки.
7.  Закрывает новую вкладку.
8.  Возвращается на основную вкладку.

**Внутренние функции**:

Внутри данной функции нет внутренних функций.

**Примеры**:

```python
from src.webdriver.driver import Driver, Chrome
from src.suppliers.suppliers_list.aliexpress.scenarios.affiliate_links_shortener_scenario import get_short_affiliate_link

# Пример использования с Chrome
driver = Driver(Chrome)
long_url = "https://aliexpress.ru/item/1005003609402541.html"
short_url = get_short_affiliate_link(driver, long_url)
print(f"Сокращенная ссылка: {short_url}")

#Пример с неправильным URL
try:
    driver = Driver(Chrome)
    long_url = "https://error.taobao.com"
    short_url = get_short_affiliate_link(driver, long_url)
    print(f"Сокращенная ссылка: {short_url}")
except ValueError as ex:
    print(f"Возникла ошибка: {ex}")