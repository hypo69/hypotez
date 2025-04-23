### **Как использовать блок кода `AliPromoCampaign`**

=========================================================================================

Описание
-------------------------
Этот код предоставляет набор функций для управления рекламными кампаниями на платформе AliExpress. Он включает в себя инициализацию кампании, обработку данных категорий и товаров, использование AI для генерации контента и создание HTML-страниц для представления кампании.

Шаги выполнения
-------------------------
1. **Инициализация кампании**:
   - Создается экземпляр класса `AliPromoCampaign` с указанием названия кампании, языка и валюты.
   - При инициализации проверяется наличие файла кампании (`.json`). Если файл отсутствует, запускается процесс создания новой кампании.

2. **Обработка категорий и товаров**:
   - Функция `process_campaign` итерируется по категориям кампании, извлекая названия категорий из директорий.
   - Для каждой категории вызывается функция `process_category_products`, которая обрабатывает товары категории и генерирует партнерские ссылки.

3. **Использование AI для генерации данных**:
   - Функция `process_llm_category` использует AI (Google Gemini или OpenAI) для генерации описаний и других данных для категорий.
   - AI модель получает список товаров в категории и генерирует соответствующие описания, которые затем добавляются в данные кампании.

4. **Создание HTML-страниц**:
   - Функция `generate_output` создает HTML-страницы для каждой категории, включая информацию о товарах и ссылки на них.
   - Создаются отдельные JSON-файлы для каждого товара, а также общие файлы с информацией о категории и кампании.

5. **Сохранение данных**:
   - Все сгенерированные данные (описания, ссылки, HTML-страницы) сохраняются в соответствующие файлы и директории в структуре кампании.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.campaign.ali_promo_campaign import AliPromoCampaign
from pathlib import Path
from src import gs

# 1. Инициализация рекламной кампании
campaign_name = "SummerSale"
language = "EN"
currency = "USD"
campaign = AliPromoCampaign(campaign_name=campaign_name, language=language, currency=currency)

# 2. Путь к корневой директории кампании
campaign_root = Path(gs.path.google_drive / "aliexpress" / "campaigns" / campaign_name)

# 3. Обработка категорий и товаров
if campaign.campaign:
    categories_names_list = campaign.campaign.category.__dict__.keys()  # Извлекаем названия категорий из объекта кампании
else:
    categories_names_list = campaign.set_categories_from_directories()  # Если объект кампании пустой, устанавливаем категории из директорий

for category_name in categories_names_list:
    print(f"Обработка категории: {category_name}")
    # 4. Обработка товаров в категории
    products = campaign.process_category_products(category_name)

    if products:
        print(f"Найдено {len(products)} товаров в категории {category_name}")
        # 5. Генерация HTML-страниц для товаров
        import asyncio
        asyncio.run(campaign.generate_output(campaign_name, campaign_root / "category" / category_name, products))
    else:
        print(f"Товары в категории {category_name} не найдены")

    # 6. Использование AI для генерации данных о категории
    campaign.process_llm_category(category_name)

# 7. Генерация общего HTML для кампании
campaign.generate_html_for_campaign(campaign_name)