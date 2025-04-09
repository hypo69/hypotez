# Модуль для сокращения партнерских ссылок AliExpress
## Обзор

Модуль `affiliate_links_shortener.py` предназначен для сокращения партнерских ссылок AliExpress. Он содержит класс `AffiliateLinksShortener`, который позволяет сокращать длинные партнерские ссылки до более коротких и удобных для использования.

## Подробней

Этот модуль является экспериментальным и предназначен для использования внутри проекта `hypotez`. Он предоставляет функциональность для работы с партнерскими ссылками AliExpress, упрощая их распространение и отслеживание.

## Классы

### `AffiliateLinksShortener`

**Описание**: Класс для сокращения партнерских ссылок AliExpress.

**Наследует**:

Нет

**Атрибуты**:

Нет

**Методы**:

- `short_affiliate_link(url: str) -> str | None`: Сокращает партнерскую ссылку AliExpress.

**Принцип работы**:

Класс `AffiliateLinksShortener` содержит метод `short_affiliate_link`, который принимает URL партнерской ссылки AliExpress и возвращает ее сокращенную версию.

## Методы класса

### `short_affiliate_link`

```python
def short_affiliate_link(url: str) -> str | None:
    """
    Сокращает партнерскую ссылку AliExpress.
    Args:
        url (str): URL партнерской ссылки AliExpress.

    Returns:
        str | None: Сокращенная версия партнерской ссылки или None в случае ошибки.

    Raises:
        Exception: Если возникает ошибка при сокращении ссылки.

    Example:
        >>> a = AffiliateLinksShortener()
        >>> url = 'https://aliexpress.com'
        >>> link = a.short_affiliate_link(url)
        >>> print(link)
        <сокращенная ссылка>
    """
    ...
```

**Назначение**: Сокращение партнерской ссылки AliExpress.

**Параметры**:

- `url` (str): URL партнерской ссылки AliExpress.

**Возвращает**:

- `str | None`: Сокращенная версия партнерской ссылки или `None` в случае ошибки.

**Как работает функция**:

Функция `short_affiliate_link` принимает URL партнерской ссылки AliExpress и возвращает ее сокращенную версию. Если при сокращении ссылки возникает ошибка, функция возвращает `None`.

## Параметры класса

- `url` (str): URL-адрес, который необходимо сократить. Этот параметр обязателен.

**Примеры**:

```python
from src.suppliers.aliexpress import AffiliateLinksShortener

a = AffiliateLinksShortener()
url = 'https://aliexpress.com'
link = a.short_affiliate_link(url)
if link:
    print(f'Сокращенная ссылка: {link}')
else:
    print('Не удалось сократить ссылку')