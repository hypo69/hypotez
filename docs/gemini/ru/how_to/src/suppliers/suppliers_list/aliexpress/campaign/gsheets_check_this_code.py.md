### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предоставляет класс `AliCampaignGoogleSheet` для работы с Google Sheets в контексте управления рекламными кампаниями AliExpress. Он позволяет автоматизировать создание и обновление листов Google Sheets с данными о кампаниях, категориях и товарах, а также предоставляет функции для форматирования этих листов.

Шаги выполнения
-------------------------
1. **Инициализация класса `AliCampaignGoogleSheet`**:
   - Создается экземпляр класса `AliCampaignGoogleSheet` с указанием имени кампании, языка и валюты.
   - При инициализации происходит очистка существующих данных, создание листов для кампании и категорий, а также открытие Google Sheets в браузере.

2. **Очистка данных**:
   - Метод `clear` удаляет все листы продуктов, чтобы начать с чистого листа.

3. **Установка данных кампании**:
   - Метод `set_campaign_worksheet` записывает данные о кампании (имя, заголовок, язык, валюта, описание) в лист 'campaign' в Google Sheets.

4. **Установка данных категорий**:
   - Метод `set_categories_worksheet` записывает данные о категориях (имя, заголовок, описание, теги, количество продуктов) в лист 'categories' в Google Sheets.

5. **Установка данных товаров**:
   - Метод `set_products_worksheet` копирует лист 'product' и переименовывает его в соответствии с именем категории, затем записывает данные о товарах в этот лист.

6. **Форматирование листов**:
   - Методы `_format_categories_worksheet` и `_format_category_products_worksheet` форматируют листы категорий и товаров, устанавливая ширину столбцов, высоту строк и стили заголовков.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.campaign.gsheets_check_this_code import AliCampaignGoogleSheet

# Инициализация класса для работы с Google Sheets кампании AliExpress
campaign_name = "Test Campaign"
language = "EN"
currency = "USD"
ali_campaign_google_sheet = AliCampaignGoogleSheet(campaign_name=campaign_name, language=language, currency=currency)

# (Опционально) Получение данных из таблицы Google Sheets
data = ali_campaign_google_sheet.get_categories()
print(data)

# (Опционально) Установка данных о товарах для определенной категории
category_name = "Example Category"
products = [{"product_id": "123", "product_title": "Example Product"}]
ali_campaign_google_sheet.set_category_products(category_name=category_name, products=products)