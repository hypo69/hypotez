### Как использовать класс `AffiliateLink`
=========================================================================================

Описание
-------------------------
Класс `AffiliateLink` предназначен для хранения информации о партнерской ссылке, включая саму ссылку и источник этой ссылки. Это полезно для отслеживания и управления партнерскими программами, например, при работе с API AliExpress.

Шаги выполнения
-------------------------
1. **Импорт класса**: Импортируйте класс `AffiliateLink` в ваш модуль.
2. **Создание экземпляра класса**: Создайте экземпляр класса `AffiliateLink`, передав значения для `promotion_link` и `source_value`.
3. **Использование атрибутов**: Используйте атрибуты `promotion_link` и `source_value` для доступа к информации о партнерской ссылке.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.api.models import AffiliateLink

# Создание экземпляра класса AffiliateLink
affiliate_link = AffiliateLink(
    promotion_link="https://s.click.aliexpress.com/e/_DDIYvVz",
    source_value="aliexpress"
)

# Доступ к атрибутам экземпляра класса
print(f"Партнерская ссылка: {affiliate_link.promotion_link}")
print(f"Источник ссылки: {affiliate_link.source_value}")
```