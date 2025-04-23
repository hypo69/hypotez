### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Данный код предоставляет класс `AliCampaignEditor`, предназначенный для редактирования рекламных кампаний, таких как добавление, удаление и обновление продуктов, категорий и других параметров кампании. Этот класс расширяет класс `AliPromoCampaign` и включает методы для работы с данными, хранящимися в файлах JSON и текстовых файлах.

Шаги выполнения
-------------------------
1. **Инициализация `AliCampaignEditor`**:
   - Создается экземпляр класса `AliCampaignEditor` с указанием имени кампании, языка и валюты.
   - Функция `__init__` вызывает конструктор родительского класса `AliPromoCampaign` для инициализации основных параметров кампании.

2. **Удаление продукта (`delete_product`)**:
   - Вызывается метод `delete_product` с указанием `product_id` продукта, который нужно удалить.
   - Функция проверяет наличие аффилиатной ссылки и удаляет продукт из списка `sources.txt` или переименовывает HTML-файл продукта, если аффилиатной ссылки нет.

3. **Обновление продукта (`update_product`)**:
   - Вызывается метод `update_product` с указанием имени категории, языка и словаря с данными продукта.
   - Функция вызывает метод `dump_category_products_files` для обновления данных о продукте в соответствующей категории.

4. **Обновление кампании (`update_campaign`)**:
   - Вызывается метод `update_campaign` для обновления общих свойств кампании, таких как описание и теги.

5. **Обновление категории (`update_category`)**:
   - Вызывается метод `update_category` с указанием пути к JSON-файлу и объекта категории `SimpleNamespace`.
   - Функция загружает данные из JSON-файла, обновляет информацию о категории и сохраняет изменения обратно в файл.

6. **Получение категории (`get_category`)**:
   - Вызывается метод `get_category` с указанием имени категории.
   - Функция возвращает объект `SimpleNamespace`, представляющий категорию, или `None`, если категория не найдена.

7. **Получение списка категорий (`list_categories`)**:
   - Вызывается метод `list_categories` для получения списка категорий в текущей кампании.
   - Функция возвращает список имен категорий или `None`, если категории не найдены.

8. **Получение продуктов категории (`get_category_products`)**:
   - Вызывается асинхронный метод `get_category_products` с указанием имени категории.
   - Функция считывает данные о товарах из JSON-файлов для указанной категории и возвращает список объектов `SimpleNamespace`, представляющих товары.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.campaign.ali_campaign_editor import AliCampaignEditor
from pathlib import Path
from types import SimpleNamespace

# 1. Инициализация редактора кампании
editor = AliCampaignEditor(campaign_name="Summer Sale", language="EN", currency="USD")

# 2. Удаление продукта
editor.delete_product(product_id="12345")

# 3. Обновление продукта
editor.update_product(category_name="Electronics", lang="EN", product={"product_id": "12345", "title": "Smartphone"})

# 4. Обновление категории
category = SimpleNamespace(name="New Category", description="Updated description")
result = editor.update_category(json_path=Path("category.json"), category=category)
print(result)

# 5. Получение категории
category = editor.get_category(category_name="Electronics")
print(category)

# 6. Получение списка категорий
categories = editor.list_categories
print(categories)

# 7. Получение продуктов категории (асинхронный вызов)
async def main():
    products = await editor.get_category_products(category_name="Electronics")
    if products:
        print(len(products))

# Запуск асинхронной функции
import asyncio
asyncio.run(main())
```