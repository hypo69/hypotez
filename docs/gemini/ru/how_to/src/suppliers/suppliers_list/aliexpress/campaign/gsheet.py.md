### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код предназначен для работы с Google Sheets, в частности, для управления рекламными кампаниями AliExpress. Он включает в себя методы для очистки, удаления листов, записи данных о кампаниях, категориях и товарах, а также для форматирования листов Google Sheets.

Шаги выполнения
-------------------------
1. **Инициализация класса `AliCampaignGoogleSheet`**:
   - Создание экземпляра класса `AliCampaignGoogleSheet` с указанием имени кампании, языка и валюты.
   - Вызов конструктора родительского класса `SpreadSheet` с указанием ID таблицы Google Sheets.

   ```python
   from src.suppliers.suppliers_list.aliexpress.campaign.gsheet import AliCampaignGoogleSheet

   campaign_name = "test_campaign"
   language = "en"
   currency = "USD"
   aliexpress_gsheet = AliCampaignGoogleSheet(campaign_name=campaign_name, language=language, currency=currency)
   ```

2. **Очистка данных**:
   - Вызов метода `clear` для удаления всех листов продуктов и очистки данных на листе категорий и других указанных листах.
   - Функция вызывает `self.delete_products_worksheets()` для удаления листов продуктов.
   ```python
   aliexpress_gsheet.clear()
   ```

3. **Удаление листов продуктов**:
   - Вызов метода `delete_products_worksheets` для удаления всех листов, кроме 'categories', 'product', 'category' и 'campaign'.
   - Функция перебирает все листы в Google Sheets и удаляет те, чьи названия не входят в список исключений.

   ```python
   aliexpress_gsheet.delete_products_worksheets()
   ```

4. **Запись данных о кампании**:
   - Создание объекта `SimpleNamespace` с данными о кампании (название, заголовок, язык, валюта, описание).
   - Вызов метода `set_campaign_worksheet` для записи данных в лист 'campaign'.
   - Функция подготавливает данные для вертикальной записи и выполняет пакетное обновление ячеек листа 'campaign'.

   ```python
   from types import SimpleNamespace

   campaign_data = SimpleNamespace(
       campaign_name="Summer Sale",
       title="Up to 50% off",
       language="en",
       currency="USD",
       description="Discounts on selected items"
   )
   aliexpress_gsheet.set_campaign_worksheet(campaign_data)
   ```

5. **Запись данных о категориях**:
   - Создание объекта `SimpleNamespace` с данными о категориях (название, заголовок, описание, теги, количество товаров).
   - Вызов метода `set_categories_worksheet` для записи данных в лист 'categories'.
   - Функция очищает лист 'categories', подготавливает данные для записи и выполняет обновление ячеек.

   ```python
   from types import SimpleNamespace

   categories_data = SimpleNamespace(**{
       "electronics": SimpleNamespace(
           name="electronics",
           title="Electronics",
           description="Latest electronics gadgets",
           tags=["gadgets", "electronics", "tech"],
           products_count=100
       ),
       "clothing": SimpleNamespace(
           name="clothing",
           title="Clothing",
           description="Fashionable clothing for all seasons",
           tags=["fashion", "clothing", "apparel"],
           products_count=200
       )
   })
   aliexpress_gsheet.set_categories_worksheet(categories_data)
   ```

6. **Получение данных о категориях**:
   - Вызов метода `get_categories` для получения данных из листа 'categories'.
   - Функция возвращает данные в виде списка словарей.

   ```python
   categories = aliexpress_gsheet.get_categories()
   print(categories)
   ```

7. **Запись данных о товарах**:
   - Определение имени категории и списка товаров (в виде словарей).
   - Вызов метода `set_category_products` для записи данных о товарах в новый лист Google Sheets, скопированный с листа 'product'.
   - Функция копирует лист 'product', формирует заголовки и данные о товарах, а затем обновляет лист.

   ```python
   category_name = "electronics"
   products_data = [
       {"product_id": "123", "app_sale_price": "100", "original_price": "120", "sale_price": "110", "discount": "10",
        "product_main_image_url": "url1", "local_image_path": "path1", "product_small_image_urls": ["url2", "url3"],
        "product_video_url": "url4", "local_video_path": "path2", "first_level_category_id": "cat1",
        "first_level_category_name": "Electronics", "second_level_category_id": "subcat1",
        "second_level_category_name": "Smartphones", "target_sale_price": "90", "target_sale_price_currency": "USD",
        "target_app_sale_price_currency": "USD", "target_original_price_currency": "USD",
        "original_price_currency": "USD", "product_title": "Smartphone X", "evaluate_rate": "4.5",
        "promotion_link": "link1", "shop_url": "url5", "shop_id": "shop1", "tags": ["tag1", "tag2"]},
       {"product_id": "456", "app_sale_price": "200", "original_price": "240", "sale_price": "220", "discount": "8",
        "product_main_image_url": "url6", "local_image_path": "path3", "product_small_image_urls": ["url7", "url8"],
        "product_video_url": "url9", "local_video_path": "path4", "first_level_category_id": "cat2",
        "first_level_category_name": "Electronics", "second_level_category_id": "subcat2",
        "second_level_category_name": "Laptops", "target_sale_price": "180", "target_sale_price_currency": "USD",
        "target_app_sale_price_currency": "USD", "target_original_price_currency": "USD",
        "original_price_currency": "USD", "product_title": "Laptop Y", "evaluate_rate": "4.2",
        "promotion_link": "link2", "shop_url": "url10", "shop_id": "shop2", "tags": ["tag3", "tag4"]}
   ]
   aliexpress_gsheet.set_category_products(category_name, products_data)
   ```

8. **Форматирование листов**:
   - Внутренние методы `_format_categories_worksheet` и `_format_category_products_worksheet` используются для форматирования листов 'categories' и листов с продуктами категорий соответственно.
   - Они устанавливают ширину столбцов, высоту строк, форматирование заголовков и другие параметры форматирования.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.campaign.gsheet import AliCampaignGoogleSheet
from types import SimpleNamespace

# Инициализация класса
campaign_name = "test_campaign"
language = "en"
currency = "USD"
aliexpress_gsheet = AliCampaignGoogleSheet(campaign_name=campaign_name, language=language, currency=currency)

# Очистка данных
aliexpress_gsheet.clear()

# Данные о кампании
campaign_data = SimpleNamespace(
    campaign_name="Summer Sale",
    title="Up to 50% off",
    language="en",
    currency="USD",
    description="Discounts on selected items"
)

# Запись данных о кампании
aliexpress_gsheet.set_campaign_worksheet(campaign_data)

# Данные о категориях
categories_data = SimpleNamespace(**{
    "electronics": SimpleNamespace(
        name="electronics",
        title="Electronics",
        description="Latest electronics gadgets",
        tags=["gadgets", "electronics", "tech"],
        products_count=100
    ),
    "clothing": SimpleNamespace(
        name="clothing",
        title="Clothing",
        description="Fashionable clothing for all seasons",
        tags=["fashion", "clothing", "apparel"],
        products_count=200
    )
})

# Запись данных о категориях
aliexpress_gsheet.set_categories_worksheet(categories_data)

# Получение данных о категориях
categories = aliexpress_gsheet.get_categories()
print(categories)

# Данные о товарах
category_name = "electronics"
products_data = [
    {"product_id": "123", "app_sale_price": "100", "original_price": "120", "sale_price": "110", "discount": "10",
     "product_main_image_url": "url1", "local_image_path": "path1", "product_small_image_urls": ["url2", "url3"],
     "product_video_url": "url4", "local_video_path": "path2", "first_level_category_id": "cat1",
     "first_level_category_name": "Electronics", "second_level_category_id": "subcat1",
     "second_level_category_name": "Smartphones", "target_sale_price": "90", "target_sale_price_currency": "USD",
     "target_app_sale_price_currency": "USD", "target_original_price_currency": "USD",
     "original_price_currency": "USD", "product_title": "Smartphone X", "evaluate_rate": "4.5",
     "promotion_link": "link1", "shop_url": "url5", "shop_id": "shop1", "tags": ["tag1", "tag2"]},
    {"product_id": "456", "app_sale_price": "200", "original_price": "240", "sale_price": "220", "discount": "8",
     "product_main_image_url": "url6", "local_image_path": "path3", "product_small_image_urls": ["url7", "url8"],
     "product_video_url": "url9", "local_video_path": "path4", "first_level_category_id": "cat2",
     "first_level_category_name": "Electronics", "second_level_category_id": "subcat2",
     "second_level_category_name": "Laptops", "target_sale_price": "180", "target_sale_price_currency": "USD",
     "target_app_sale_price_currency": "USD", "target_original_price_currency": "USD",
     "original_price_currency": "USD", "product_title": "Laptop Y", "evaluate_rate": "4.2",
     "promotion_link": "link2", "shop_url": "url10", "shop_id": "shop2", "tags": ["tag3", "tag4"]}
]

# Запись данных о товарах
aliexpress_gsheet.set_category_products(category_name, products_data)