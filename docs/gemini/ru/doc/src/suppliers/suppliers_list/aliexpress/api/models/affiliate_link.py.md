# Модуль `AffiliateLink` 

## Обзор

Этот модуль содержит класс `AffiliateLink`, который представляет собой модель для хранения информации об аффилированной ссылке на AliExpress. 

## Классы

### `AffiliateLink`

**Описание**: Класс `AffiliateLink`  хранит данные об аффилированной ссылке AliExpress, такие как URL ссылки и источник трафика.

**Атрибуты**:

- `promotion_link` (str): URL аффилированной ссылки.
- `source_value` (str): Источник трафика, например, название партнерской программы.

**Пример**:

```python
from src.suppliers.aliexpress.api.models.affiliate_link import AffiliateLink

affiliate_link = AffiliateLink(
    promotion_link='https://aliexpress.com/item/1234567890',
    source_value='my_affiliate_program'
)

print(affiliate_link.promotion_link)  # Вывод: https://aliexpress.com/item/1234567890
print(affiliate_link.source_value)  # Вывод: my_affiliate_program