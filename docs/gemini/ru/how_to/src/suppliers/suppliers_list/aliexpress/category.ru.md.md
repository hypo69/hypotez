## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Модуль предназначен для управления категориями товаров на платформе Aliexpress. Он предоставляет функции для получения ссылок на товары в категории, обновления категорий на основе данных с сайта и операций с базой данных.

Шаги выполнения
-------------------------
1. **Получение списка товаров из категории**:
   - Используйте функцию `get_list_products_in_category(s)` для получения списка URL товаров из указанной категории.
   - Функция автоматически перелистывает страницы с товарами, если их несколько.

2. **Обновление категорий в файле сценария**:
   - Используйте функцию `update_categories_in_scenario_file(s, scenario_filename)` для проверки и обновления категорий в файле сценария на основе данных с сайта Aliexpress.

3. **Операции с базой данных**:
   - Используйте класс `DBAdaptor` для выполнения операций с базой данных, таких как выборка, вставка, обновление и удаление данных о категориях.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress import category
from src.suppliers.supplier import Supplier  # Предполагается, что класс Supplier определен в этом модуле
from src.db.db_ адаптор import DBAdaptor  # Предполагается, что DBAdaptor определен в этом модуле

# Пример создания объекта Supplier (замените параметры реальными значениями)
supplier_data = {
    'id': 1,
    'name': 'aliexpress',
    'domain': 'aliexpress.com',
    'token': 'your_token',
    ' main_category': 'electronics',
    'file_name': 'aliexpress.json'
}
supplier = Supplier(**supplier_data)

# 1. Получение списка товаров из категории
products = category.get_list_products_in_category(supplier)
if products:
    print(f"Получен список товаров: {products}")
else:
    print("Не удалось получить список товаров.")

# 2. Обновление категорий в файле сценария
scenario_filename = "scenario_file.json"  # Укажите имя вашего файла сценария
updated = category.update_categories_in_scenario_file(supplier, scenario_filename)
if updated:
    print("Файл сценария успешно обновлен.")
else:
    print("Не удалось обновить файл сценария.")

# 3. Операции с базой данных
db = DBAdaptor()

# Пример выборки данных
db.select(cat_id=123)

# Пример вставки данных
db.insert()

# Пример обновления данных
db.update()

# Пример удаления данных
db.delete()