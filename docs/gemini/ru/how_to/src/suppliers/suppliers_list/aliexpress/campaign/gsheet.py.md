## Как использовать класс `AliCampaignGoogleSheet`
=========================================================================================

Описание
-------------------------
Класс `AliCampaignGoogleSheet` предназначен для работы с Google Sheets в контексте рекламных кампаний AliExpress. 

Он предоставляет методы для:

-  **Создания и управления листами**: создание, удаление, копирование и выбор листов.
-  **Записи данных**: запись информации о кампании, категориях и товарах в таблицы Google Sheets.
-  **Форматирования листов**: настройка ширины столбцов и высоты строк, применение стилей к заголовкам.

Шаги выполнения
-------------------------
1. **Инициализация класса**: Создайте экземпляр класса `AliCampaignGoogleSheet`, указав имя кампании, язык и валюту:
   ```python
   sheet = AliCampaignGoogleSheet(campaign_name='Название кампании', language='ru', currency='RUB')
   ```
2. **Очистка листов**:  Очистите существующие данные на листах, удалив листы с товарами:
   ```python
   sheet.clear()  # Удаление всех листов, кроме 'categories', 'product', 'category', 'campaign'
   ```
3. **Запись данных о кампании**: Заполните лист `campaign` информацией о кампании:
   ```python
   campaign = SimpleNamespace(
       campaign_name='Название кампании',
       title='Заголовок кампании',
       language='ru',
       currency='RUB',
       description='Описание кампании' 
   )
   sheet.set_campaign_worksheet(campaign)
   ```
4. **Запись данных о категориях**:  Запишите информацию о категориях и их товарах на соответствующие листы:
   ```python
   categories = SimpleNamespace(
       category1=SimpleNamespace(
           name='Название категории 1',
           title='Название категории 1',
           description='Описание категории 1',
           tags=['тег1', 'тег2'],
           products_count=10,
           products=[
               # Данные о товарах
           ]
       ),
       category2=SimpleNamespace(
           # Данные о категории 2
       )
   )
   sheet.set_categories_worksheet(categories)
   sheet.set_products_worksheet('Название категории 1')  # Записать товары для категории 1
   ```

Пример использования
-------------------------

```python
from src.suppliers.aliexpress.campaign.gsheet import AliCampaignGoogleSheet
from types import SimpleNamespace

sheet = AliCampaignGoogleSheet(campaign_name='Моя кампания', language='ru', currency='RUB')
sheet.clear()

campaign = SimpleNamespace(
    campaign_name='Моя кампания',
    title='Заголовок кампании',
    language='ru',
    currency='RUB',
    description='Описание кампании'
)

categories = SimpleNamespace(
    category1=SimpleNamespace(
        name='Одежда',
        title='Одежда',
        description='Красивая одежда для всех',
        tags=['мода', 'стиль', 'одежда'],
        products_count=20,
        products=[
            SimpleNamespace(
                product_id='123456789',
                app_sale_price=10.99,
                original_price=15.99,
                # ... и другие данные о товаре
            ),
            # Другие товары
        ]
    )
)

sheet.set_campaign_worksheet(campaign)
sheet.set_categories_worksheet(categories)
sheet.set_products_worksheet('Одежда')
```