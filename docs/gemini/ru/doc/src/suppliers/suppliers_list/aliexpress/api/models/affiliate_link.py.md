# Модуль: src.suppliers.suppliers_list.aliexpress.api.models.affiliate_link

## Обзор

Модуль содержит описание класса `AffiliateLink`, предназначенного для хранения информации о партнерской ссылке, включая саму ссылку и значение источника.

## Подробнее

Этот модуль определяет структуру данных для представления партнерской ссылки, полученной от AliExpress. Он включает в себя URL партнерской ссылки и значение, идентифицирующее источник этой ссылки.

## Классы

### `AffiliateLink`

**Описание**: Класс `AffiliateLink` используется для представления информации о партнерской ссылке.

**Атрибуты**:
- `promotion_link` (str): URL партнерской ссылки.
- `source_value` (str): Значение, идентифицирующее источник ссылки.

**Принцип работы**:
Класс `AffiliateLink` служит контейнером для хранения двух строковых значений: самой партнерской ссылки (`promotion_link`) и идентификатора источника этой ссылки (`source_value`). Он не содержит никакой логики, кроме хранения данных.

## Параметры класса

- `promotion_link` (str): URL партнерской ссылки.
- `source_value` (str): Значение, идентифицирующее источник ссылки.

**Примеры**:

```python
# Пример создания экземпляра класса AffiliateLink
affiliate_link = AffiliateLink()
affiliate_link.promotion_link = "https://example.com/promotion"
affiliate_link.source_value = "aliexpress"

print(affiliate_link.promotion_link)  # Вывод: https://example.com/promotion
print(affiliate_link.source_value)  # Вывод: aliexpress