## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода демонстрирует использование класса `AffiliateLinksShortener` из модуля `src.suppliers.suppliers_list.aliexpress` для сокращения аффилиатных ссылок на AliExpress. 

Шаги выполнения
-------------------------
1. Импортировать модуль `header` и класс `AffiliateLinksShortener` из модуля `src.suppliers.suppliers_list.aliexpress`.
2. Создать экземпляр класса `AffiliateLinksShortener`.
3. Вызвать метод `short_affiliate_link` экземпляра `AffiliateLinksShortener`, передавая в него URL-адрес, который нужно сократить.
4. Получить сокращенную ссылку как результат вызова метода.

Пример использования
-------------------------

```python
import header
from src.suppliers.suppliers_list.aliexpress import AffiliateLinksShortener

# Создаем экземпляр класса
a = AffiliateLinksShortener()

# Исходный URL
url = 'https://aliexpress.com'

# Сокращаем ссылку
link = a.short_affiliate_link(url)

# Выводим сокращенную ссылку
print(link)
```