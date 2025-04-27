## Как использовать класс `AliApi`

=========================================================================================

Описание
-------------------------
Класс `AliApi` - это кастомный класс для работы с API AliExpress. 
Он расширяет базовый класс `AliexpressApi` и предоставляет дополнительные функции для получения данных о товарах и генерации партнерских ссылок. 

Шаги выполнения
-------------------------
1. **Инициализация класса:**
    - Создайте экземпляр класса `AliApi`, передав в конструктор следующие аргументы:
        - `language`: Язык для API-запросов (по умолчанию 'en').
        - `currency`: Валюта для API-запросов (по умолчанию 'usd').
    - Конструктор класса автоматически загружает учетные данные из конфигурационного файла `gs.credentials.aliexpress` и инициализирует базовый класс `AliexpressApi`.
2. **Получение данных о товарах:**
    - Используйте метод `retrieve_product_details_as_dict(product_ids)` для получения информации о товарах по их ID.
    - Метод принимает список ID товаров (`product_ids`) и возвращает список словарей с описанием каждого товара. 
    - Метод `retrieve_product_details_as_dict` использует метод `retrieve_product_details` базового класса для получения данных о товарах в формате `SimpleNamespace`. 
    - Затем он конвертирует данные из `SimpleNamespace` в словарь.
3. **Генерация партнерских ссылок:**
    - Используйте метод `get_affiliate_links(links, link_type)` для генерации партнерских ссылок для заданных товаров.
    - Метод принимает строку или список URL товаров (`links`) и тип партнерской ссылки (`link_type`).
    - Он использует метод `get_affiliate_links` базового класса для получения списка `SimpleNamespace` объектов с партнерскими ссылками.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.aliapi import AliApi

# Инициализация класса AliApi
api = AliApi(language='ru', currency='rub')

# Получение данных о товарах
product_ids = [1234567890, 9876543210]
product_details = api.retrieve_product_details_as_dict(product_ids)

# Вывод данных о товарах
print(product_details)

# Генерация партнерских ссылок
product_links = ['https://www.aliexpress.com/item/1234567890.html', 'https://www.aliexpress.com/item/9876543210.html']
affiliate_links = api.get_affiliate_links(product_links)

# Вывод партнерских ссылок
pprint(affiliate_links)
```