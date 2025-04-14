# Модуль для работы с партнерскими ссылками AliExpress
## Обзор

Модуль `affiliate_link.py` содержит класс `AffiliateLink`, который используется для хранения информации о партнерской ссылке AliExpress, включая саму ссылку и источник значения.
## Классы

### `AffiliateLink`

**Описание**: Класс `AffiliateLink` предназначен для представления партнерской ссылки, полученной от AliExpress.

**Атрибуты**:

- `promotion_link` (str): Партнерская ссылка.
- `source_value` (str): Источник значения ссылки.

**Принцип работы**:
Класс предназначен для хранения и передачи информации о партнерской ссылке и источнике, из которого она была получена.

**Пример**:

```python
affiliate_link = AffiliateLink()
affiliate_link.promotion_link = "https://aliexpress.com/..."
affiliate_link.source_value = "admitad"
print(affiliate_link.promotion_link)
print(affiliate_link.source_value)
```
## Параметры класса

- `promotion_link` (str):  Строка, содержащая URL партнерской ссылки.
- `source_value` (str): Строка, определяющая источник, из которого была получена партнерская ссылка.