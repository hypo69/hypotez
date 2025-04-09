# Модуль для сокращения партнерских ссылок AliExpress
## Обзор

Модуль `affiliate_links_shortener.py` предназначен для сокращения партнерских ссылок AliExpress. Он содержит класс `AffiliateLinksShortener`, который позволяет генерировать короткие партнерские ссылки на товары AliExpress.

## Подробней

Этот код является экспериментальным и предоставляет функциональность для работы с партнерскими ссылками AliExpress. Он использует класс `AffiliateLinksShortener` для сокращения длинных URL-адресов в более короткие, что может быть полезно для удобства распространения ссылок.
Импортирует модуль `header` и класс `AffiliateLinksShortener` из модуля `src.suppliers.aliexpress`.

## Классы

### `AffiliateLinksShortener`

**Описание**:
Класс предназначен для сокращения партнерских ссылок AliExpress.

**Принцип работы**:
Класс `AffiliateLinksShortener` содержит методы, необходимые для генерации коротких партнерских ссылок на товары AliExpress. Экземпляр класса создается, вызывается метод `short_affiliate_link` для сокращения URL.

## Функции

В данном коде функции отсутствуют. Вместо них используется метод класса `AffiliateLinksShortener`.

## Пример использования

```python
import header
from src.suppliers.aliexpress import AffiliateLinksShortener

a = AffiliateLinksShortener()
url = 'https://aliexpress.com'
link = a.short_affiliate_link(url)
...