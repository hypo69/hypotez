## Как использовать этот блок кода
=========================================================================================

### Описание
-------------------------
Этот блок кода реализует процесс обновления данных кампании AliExpress с помощью Google Sheets. 
Он позволяет редактировать информацию о категориях кампании, обновлять список товаров в каждой категории и сохранять изменения в объекте кампании. 

### Шаги выполнения
-------------------------
1. **Получение данных кампании:**
    - Инициализируется объект `AliCampaignEditor` для указанной кампании с заданным названием, языком и валютой.
    - Получаются данные кампании с помощью `campaign_editor.campaign`.
    - Извлекаются данные о категориях из объекта кампании (`_categories`).
2. **Преобразование категорий в формат Google Sheets:**
    - Создается словарь `categories_dict`, где ключ - имя категории, значение - объект `CategoryType` из данных кампании.
    - Преобразуется словарь `categories_dict` в список `categories_list`, содержащий объекты `CategoryType`.
3. **Обновление категорий в Google Sheet:**
    - Используется объект `AliCampaignGoogleSheet` для работы с Google Sheet.
    - Устанавливаются категории в Google Sheet с помощью `gs.set_categories(categories_list)`.
    - Извлекаются отредактированные категории из Google Sheet с помощью `gs.get_categories()`.
4. **Обновление данных кампании:**
    - Перебираются отредактированные категории из Google Sheet.
    - Создается объект `SimpleNamespace` `_cat_ns` для каждой категории с обновленными данными.
    - Обновляется словарь `categories_dict` данными из `_cat_ns`.
    - Извлекаются товары для каждой категории с помощью `campaign_editor.get_category_products()`.
    - Устанавливаются обновленные товары в Google Sheet с помощью `gs.set_category_products()`.
5. **Создание объекта кампании с обновленными данными:**
    - Преобразуется словарь `categories_dict` обратно в объект `SimpleNamespace` `_updated_categories`.
    - Создается словарь `campaign_dict` для кампании, содержащий обновленные данные, включая название, заголовок, язык, валюту и обновленные категории.
    - Преобразуется словарь `campaign_dict` в объект `SimpleNamespace` `edited_campaign`.
6. **Обновление данных кампании:**
    - Обновляются данные кампании с помощью `campaign_editor.update_campaign(edited_campaign)`.

### Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress import campaign
from src.suppliers.suppliers_list.aliexpress.campaign import AliCampaignGoogleSheet , AliCampaignEditor
from src.suppliers.suppliers_list.aliexpress.campaign.ttypes import CampaignType, CategoryType, ProductType

# Инициализация объекта кампании
campaign_name = "lighting"
language = 'EN'
currency = 'USD'
campaign_editor = AliCampaignEditor(campaign_name, language, currency)

# Получение данных кампании
campaign_data = campaign_editor.campaign
_categories = campaign_data.category

# Обновление данных категорий
gs = AliCampaignGoogleSheet('1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0')  # ID Google Sheet
categories_dict = {category_name: getattr(_categories, category_name) for category_name in vars(_categories)}
categories_list = list(categories_dict.values())
gs.set_categories(categories_list)
edited_categories = gs.get_categories()

# Обновление данных кампании
for _cat in edited_categories:
    # ... [оставшийся код для обновления данных]
```