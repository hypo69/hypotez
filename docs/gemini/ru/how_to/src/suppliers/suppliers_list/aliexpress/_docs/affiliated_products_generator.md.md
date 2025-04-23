### Как использовать этот блок кода

=========================================================================================

Описание
-------------------------
`AliAffiliatedProducts` - это класс, предназначенный для сбора полной информации о товарах с использованием API Aliexpress Affiliate. Он позволяет получать данные о товарах по их URL или ID, включая партнерские ссылки, изображения и видео. Класс сохраняет полученные данные локально для дальнейшего использования в рекламных кампаниях.

Шаги выполнения
-------------------------
1. **Инициализация класса `AliAffiliatedProducts`**:
   - Создается экземпляр класса `AliAffiliatedProducts` с указанием названия кампании, категории (опционально), языка и валюты.
   - Пример:
     ```python
     parser = AliAffiliatedProducts(
         campaign_name="my_campaign",
         campaign_category="electronics",
         language="RU",
         currency="RUB"
     )
     ```

2. **Обработка списка URL товаров**:
   - Вызывается метод `process_affiliate_products` с передачей списка URL или ID товаров.
   - Метод выполняет следующие действия:
     - Получает партнерские ссылки для каждого товара.
     - Извлекает детали товара.
     - Сохраняет изображения и видео локально.
     - Создает JSON-файл с полной информацией о товаре.

3. **Получение партнерских ссылок**:
   - Для каждого URL товара вызывается метод `get_affiliate_links` из родительского класса `AliApi`.
   - Если партнерская ссылка найдена, она добавляется в список `_promotion_links`.

4. **Извлечение деталей товара**:
   - После получения списка партнерских ссылок вызывается метод `retrieve_product_details` для получения полной информации о товарах.

5. **Сохранение изображений и видео**:
   - Для каждого товара извлекается URL изображения и видео.
   - Изображения сохраняются с использованием функции `save_png_from_url`, а видео - с использованием `save_video_from_url`.
   - Локальные пути к сохраненным файлам добавляются в объект товара.

6. **Сохранение информации о товаре в JSON**:
   - Вся информация о товаре сохраняется в JSON-файл с использованием функции `j_dumps`.
   - Файл сохраняется в каталоге кампании, в подкаталоге, соответствующем языку и валюте.

7. **Удаление товара (если нет партнерской ссылки)**:
   - Если для товара не найдена партнерская ссылка, вызывается метод `delete_product` для удаления товара из списка источников.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.affiliated_products_generator import AliAffiliatedProducts
from pathlib import Path

# Пример использования:
campaign_name = "test_campaign"
campaign_category = "electronics"
language = "RU"
currency = "RUB"
prod_urls = [
    "https://www.aliexpress.com/item/1234567890.html",
    "9876543210"
]

# Укажите путь к google_drive
google_drive_path = Path("/path/to/your/google_drive")  # Замените на актуальный путь

# Инициализация класса AliAffiliatedProducts
parser = AliAffiliatedProducts(
    campaign_name=campaign_name,
    campaign_category=campaign_category,
    language=language,
    currency=currency
)

# Обработка списка URL товаров
products = parser.process_affiliate_products(prod_urls)

# Вывод информации о товарах
if products:
    for product in products:
        print(f"Product ID: {product.product_id}")
        print(f"Promotion Link: {product.promotion_link}")
        print(f"Local Image Path: {product.local_image_path}")
        print(f"Local Video Path: {product.local_video_path}")
else:
    print("No affiliate products found.")
```