## Как использовать этот блок кода
=========================================================================================

### Описание
-------------------------
Этот блок кода представляет собой класс `AliAffiliatedProducts`, который предназначен для получения полной информации о товаре с AliExpress Affiliate API. Он основывается на классе `AliApi` и позволяет получить информацию о товаре по его URL или ID, включая сохранение изображений, видео и JSON-данных.

### Шаги выполнения
-------------------------
1. **Инициализация класса `AliAffiliatedProducts`**: Создайте экземпляр класса `AliAffiliatedProducts`, передав в качестве аргументов имя кампании (`campaign_name`), категорию кампании (`campaign_category`), язык (`language`) и валюту (`currency`).
2. **Вызов метода `process_affiliate_products`**: Передайте список URL или ID товаров в метод `process_affiliate_products` класса `AliAffiliatedProducts`.
3. **Обработка результата**: Метод `process_affiliate_products` вернет список объектов `SimpleNamespace`, каждый из которых представляет собой обработанный товар. Этот список содержит информацию о товаре, включая его аффилированный линк, изображения, видео и JSON-данные.

### Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress import AliAffiliatedProducts

# Инициализация класса AliAffiliatedProducts
parser = AliAffiliatedProducts(
    campaign_name='MyCampaign',
    campaign_category='Electronics',
    language='EN',
    currency='USD'
)

# Список URL или ID товаров
prod_urls = ['https://www.aliexpress.com/item/123456789.html', '987654321']

# Получение информации о товарах
products = parser.process_affiliate_products(prod_urls)

# Вывод информации о товарах
for product in products:
    print(f"Product ID: {product.product_id}")
    print(f"Affiliate link: {product.promotion_link}")
    print(f"Product title: {product.product_title}")
    # ... и так далее для других свойств товара
```