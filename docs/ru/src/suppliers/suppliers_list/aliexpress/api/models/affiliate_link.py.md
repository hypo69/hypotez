# Модуль: src.suppliers.suppliers_list.aliexpress.api.models.affiliate_link

## Обзор

Модуль определяет структуру данных для представления партнерской ссылки AliExpress.
Он содержит класс `AffiliateLink`, который хранит информацию о рекламной ссылке и источнике ее получения.

## Подробнее

Этот модуль используется для организации данных, связанных с партнерскими ссылками, полученными от AliExpress.
Он предоставляет простой класс для хранения URL партнерской ссылки и идентификатора источника, из которого она была получена.

## Классы

### `AffiliateLink`

**Описание**: Класс `AffiliateLink` предназначен для хранения информации о партнерской ссылке AliExpress и источнике ее получения.

**Атрибуты**:

- `promotion_link` (str): URL партнерской ссылки.
- `source_value` (str): Идентификатор источника, из которого была получена ссылка.

**Методы**:
*   `__init__`: Конструктор класса `AffiliateLink`.

#### `__init__`
```python
def __init__(self, promotion_link: str, source_value: str) -> None:
    """Инициализирует новый экземпляр класса AffiliateLink.

    Args:
        promotion_link (str): URL партнерской ссылки.
        source_value (str): Идентификатор источника, из которого была получена ссылка.

    Returns:
        None

    """
```

**Параметры**:

- `promotion_link` (str): URL партнерской ссылки.
- `source_value` (str): Идентификатор источника, из которого была получена ссылка.

**Примеры**:

```python
affiliate_link = AffiliateLink(promotion_link="https://example.com/aliexpress_link", source_value="some_source")
print(affiliate_link.promotion_link)
print(affiliate_link.source_value)