## Как использовать класс `AffiliateLink`
=========================================================================================

Описание
-------------------------
Класс `AffiliateLink` представляет собой модель для хранения информации о партнерской ссылке. Он содержит два поля:

- `promotion_link`:  Партнерская ссылка, которая используется для отслеживания переходов и продаж.
- `source_value`:  Дополнительная информация, связанная с источником партнерской ссылки.

Шаги выполнения
-------------------------
1. **Инициализация объекта:** Создайте экземпляр класса `AffiliateLink` и задайте значения атрибутов `promotion_link` и `source_value`.

Пример использования
-------------------------

```python
from src.suppliers.aliexpress.api.models.affiliate_link import AffiliateLink

# Создаем экземпляр класса AffiliateLink
affiliate_link = AffiliateLink(
    promotion_link='https://www.aliexpress.com/item/10000000000000.html?aff=12345678',  # Партнерская ссылка
    source_value='my_source'  # Дополнительная информация о источнике
)

# Используем атрибуты объекта
print(f"Партнерская ссылка: {affiliate_link.promotion_link}")
print(f"Источник: {affiliate_link.source_value}")
```