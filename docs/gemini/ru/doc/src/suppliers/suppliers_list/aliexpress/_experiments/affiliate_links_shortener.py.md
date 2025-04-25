# Модуль `aliexpress/_experiments/affiliate_links_shortener.py`

## Обзор

Модуль `aliexpress/_experiments/affiliate_links_shortener.py` содержит код для сокращения партнерских ссылок на AliExpress. 
Он использует класс `AffiliateLinksShortener` для преобразования длинных URL-адресов в короткие партнерские ссылки. 

## Подробней

Модуль используется для сокращения партнерских ссылок на AliExpress. 
Он импортирует класс `AffiliateLinksShortener` из модуля `src.suppliers.suppliers_list.aliexpress`. 
Этот класс содержит логику для преобразования длинных URL-адресов в короткие партнерские ссылки. 

## Классы

### `AffiliateLinksShortener`

**Описание**: Класс `AffiliateLinksShortener` предоставляет методы для сокращения партнерских ссылок на AliExpress.

**Наследует**: Не наследует.

**Атрибуты**: Отсутствуют

**Методы**:

#### `short_affiliate_link(url: str) -> str` 

**Назначение**: Метод `short_affiliate_link` сокращает партнерскую ссылку на AliExpress.

**Параметры**:

- `url` (str): Длинная партнерская ссылка AliExpress.

**Возвращает**:

- `str`: Сокращенная партнерская ссылка.

**Примеры**:

```python
from src.suppliers.suppliers_list.aliexpress import AffiliateLinksShortener

a = AffiliateLinksShortener()
url = 'https://aliexpress.com/item/1000000000000000.html'  # Замените на актуальную ссылку
link = a.short_affiliate_link(url)
print(link)
```

## Функции

Отсутствуют.

## Параметры

Отсутствуют.

## Примеры

```python
from src.suppliers.suppliers_list.aliexpress import AffiliateLinksShortener

a = AffiliateLinksShortener()
url = 'https://aliexpress.com/item/1000000000000000.html'  # Замените на актуальную ссылку
link = a.short_affiliate_link(url)
print(link)
```