### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код обрабатывает список ID товаров или URL-адресов, чтобы получить партнерские ссылки, сохранить изображения и видео товаров, а также сохранить данные о товарах в формате JSON.

Шаги выполнения
-------------------------
1. **Подготовка данных**:
   - Принимает список `prod_ids` (ID товаров или URL-адреса) и `category_root` (путь к корневой директории категории).
   - Нормализует URL-адреса товаров, приводя их к виду `https://aliexpress.com/item/<product_id>.html`.

2. **Получение партнерских ссылок**:
   - Для каждого нормализованного URL товара (`prod_url`) извлекает партнерские ссылки с использованием метода `super().get_affiliate_links(prod_url)`.
   - Если партнерская ссылка найдена, добавляет её в список `_promotion_links` и соответствующий URL товара в список `_prod_urls`.

3. **Извлечение деталей продукта**:
   - Использует метод `self.retrieve_product_details(_prod_urls)` для получения детальной информации о товарах на основе их URL-адресов.
   - Если детальная информация о товарах не найдена, функция возвращает `None`.

4. **Обработка и сохранение данных о товарах**:
   - Для каждого товара и соответствующей партнерской ссылки:
     - Устанавливает язык и партнерскую ссылку для товара.
     - Формирует путь для сохранения изображения товара.
     - Асинхронно сохраняет изображение товара, используя `save_image_from_url`.
     - Сохраняет локальный путь к изображению товара в атрибуте `product.local_image_path`.
     - Если у товара есть видео:
       - Извлекает URL видео.
       - Формирует путь для сохранения видео товара.
       - Асинхронно сохраняет видео товара, используя `save_video_from_url`.
       - Сохраняет локальный путь к видео товара в атрибуте `product.local_video_path`.
     - Сохраняет данные о товаре в формате JSON в файл.

5. **Сохранение списка заголовков товаров**:
   - Формирует путь к файлу `product_titles.txt` в директории категории.
   - Сохраняет список заголовков товаров в файл.

6. **Возврат результата**:
   - Возвращает список `affiliated_products_list`, содержащий обработанные товары с партнерскими ссылками и сохраненными изображениями/видео.

Пример использования
-------------------------

```python
import asyncio
from pathlib import Path
from types import SimpleNamespace

from src.suppliers.suppliers_list.aliexpress.affiliated_products_generator import AliAffiliatedProducts

async def main():
    # Пример использования класса AliAffiliatedProducts
    ali_products = AliAffiliatedProducts(language='RU', currency='RUB')
    
    # Список ID товаров или URL-адресов
    product_ids = [
        "https://aliexpress.ru/item/1005003845399909.html",
        "https://aliexpress.ru/item/1005004131558479.html"
    ]
    
    # Корневая директория категории
    category_root = Path("./data/test_category")
    category_root.mkdir(parents=True, exist_ok=True)
    
    # Обработка товаров
    products = await ali_products.process_affiliate_products(product_ids, category_root)
    
    # Вывод результатов
    if products:
        for product in products:
            print(f"Товар: {product.product_title}")
            print(f"Партнерская ссылка: {product.promotion_link}")
            print(f"Локальный путь к изображению: {product.local_image_path}")
            if hasattr(product, 'local_video_path'):
                print(f"Локальный путь к видео: {product.local_video_path}")
    else:
        print("Не удалось получить данные о товарах.")

if __name__ == "__main__":
    asyncio.run(main())