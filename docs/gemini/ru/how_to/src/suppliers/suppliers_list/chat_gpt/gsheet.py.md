## Как использовать класс `GptGs`
=========================================================================================

Описание
-------------------------
Класс `GptGs` предоставляет функционал для работы с Google Sheets, интегрированный с кампаниями AliExpress. 
Класс наследует методы от `SpreadSheet` и `AliCampaignEditor` для управления Google Sheets, 
записи данных о категориях и продуктах, а также форматирования листов.

Шаги выполнения
-------------------------
1. **Инициализация**: Создайте экземпляр класса `GptGs`. При создании экземпляра класс автоматически инициализирует подключение к Google Sheets с использованием определенного идентификатора электронной таблицы (`'1nu4mNNFMzSePlggaaL_QM2vdKVP_NNBl2OG7R9MNrs0'`).
2. **Очистка**: Вызовите метод `clear()` для удаления листов с продуктами и очистки данных на листах категорий, кампании и других заданных листах.
3. **Обновление листа чата**: Используйте метод `update_chat_worksheet()` для записи данных о разговоре в лист Google Sheets. 
    - В качестве аргумента передайте данные в формате `SimpleNamespace`, `dict` или `list`.
    - Укажите название разговора (`conversation_name`) и язык (`language`) по желанию. 
4. **Получение листа кампании**: Метод `get_campaign_worksheet()` извлекает данные о кампании из листа `'campaign'`.
    - Возвращает данные в формате `SimpleNamespace`.
5. **Установка листа категории**: Используйте метод `set_category_worksheet()` для записи данных о категории в лист `'category'`.
    - В качестве аргумента передайте данные в формате `SimpleNamespace`.
6. **Получение листа категории**: Метод `get_category_worksheet()` извлекает данные о категории из листа `'category'`.
    - Возвращает данные в формате `SimpleNamespace`.
7. **Установка листа категорий**: Используйте метод `set_categories_worksheet()` для записи данных о нескольких категориях в лист `'categories'`.
    - В качестве аргумента передайте данные в формате `SimpleNamespace`.
8. **Получение листа категорий**: Метод `get_categories_worksheet()` извлекает данные о категориях из листа `'categories'`.
    - Возвращает данные в формате `List[List[str]]`.
9. **Установка листа продукта**: Используйте метод `set_product_worksheet()` для записи данных о продукте в новый лист Google Sheets.
    - Укажите имя категории (`category_name`) и передайте данные о продукте в формате `SimpleNamespace`.
10. **Получение листа продукта**: Метод `get_product_worksheet()` извлекает данные о продукте из листа `'products'`.
    - Возвращает данные в формате `SimpleNamespace`.
11. **Установка листа продуктов**: Используйте метод `set_products_worksheet()` для записи данных о нескольких продуктах в лист `'products'`.
    - В качестве аргумента передайте название категории (`category_name`).
12. **Удаление листов продуктов**: Метод `delete_products_worksheets()` удаляет все листы из электронной таблицы Google Sheets, кроме `'categories'`, `'product'`, `'category'` и `'campaign'`.
13. **Сохранение категорий из листа**: Метод `save_categories_from_worksheet()` извлекает измененные данные о категориях из листа `'categories'`, обновляет объект `self.campaign.category` и по желанию обновляет данные о кампании с помощью метода `update_campaign()`.
14. **Сохранение кампании из листа**: Метод `save_campaign_from_worksheet()` сохраняет данные о кампании из листа `'campaign'`, обновляет объект `self.campaign` и обновляет данные о кампании с помощью метода `update_campaign()`.

Пример использования
-------------------------

```python
from src.suppliers.chat_gpt.gsheet import GptGs

# Создаем экземпляр класса GptGs
gsheet = GptGs()

# Очищаем листы
gsheet.clear()

# Записываем данные о разговоре
conversation_data = {
    "name": "Conversation 1",
    "title": "Example conversation",
    "description": "Conversation about AliExpress products",
    "tags": ["AliExpress", "Products", "Chat"],
    "products_count": 10
}
gsheet.update_chat_worksheet(conversation_data, "conversation_1")

# Получаем данные о кампании
campaign_data = gsheet.get_campaign_worksheet()

# Записываем данные о категории
category_data = {
    "name": "Category A",
    "title": "Category A Title",
    "description": "Description for Category A",
    "tags": ["Category", "A", "Products"],
    "products_count": 20
}
gsheet.set_category_worksheet(category_data)

# Получаем данные о категории
category_data = gsheet.get_category_worksheet()

# Записываем данные о нескольких категориях
categories_data = {
    "Category B": {
        "name": "Category B",
        "title": "Category B Title",
        "description": "Description for Category B",
        "tags": ["Category", "B", "Products"],
        "products_count": 30
    },
    "Category C": {
        "name": "Category C",
        "title": "Category C Title",
        "description": "Description for Category C",
        "tags": ["Category", "C", "Products"],
        "products_count": 40
    }
}
gsheet.set_categories_worksheet(categories_data)

# Получаем данные о категориях
categories_data = gsheet.get_categories_worksheet()

# Записываем данные о продукте
product_data = {
    "product_id": "123456789",
    "app_sale_price": "10.00",
    "original_price": "15.00",
    "sale_price": "12.00",
    # ... другие поля продукта
}
gsheet.set_product_worksheet(product_data, "Category A")

# Получаем данные о продукте
product_data = gsheet.get_product_worksheet()

# Записываем данные о нескольких продуктах
gsheet.set_products_worksheet("Category A")

# Удаляем листы продуктов
gsheet.delete_products_worksheets()

# Сохраняем категории из листа
gsheet.save_categories_from_worksheet()

# Сохраняем кампанию из листа
gsheet.save_campaign_from_worksheet()
```