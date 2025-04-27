## Как использовать блок кода `get_list_products_in_category` 
=========================================================================================

### Описание
-------------------------
Функция `get_list_products_in_category` извлекает ссылки на товары со страницы категории на сайте поставщика.

### Шаги выполнения
-------------------------
1. Получает драйвер веб-браузера (`s.driver`) и локаторы для элементов страницы категории (`s.locators['category']`).
2. Выполняет локатор для закрытия всплывающих окон (`s.locators['product']['close_banner']`).
3. Проверяет наличие локаторов. Если локаторы не найдены, выводит ошибку и завершает работу функции.
4. Прокручивает страницу вниз (`d.scroll()`).
5. Получает список ссылок на товары (`d.execute_locator(l['product_links'])`). 
6. Проверяет наличие ссылок на товары. Если ссылки не найдены, выводит предупреждение и завершает работу функции.
7. Форматирует список ссылок на товары (`list_products_in_category = [list_products_in_category] if isinstance(list_products_in_category, str) else list_products_in_category`). 
8. Выводит сообщение о количестве найденных товаров (`logger.info(f""" Найдено {len(list_products_in_category)} товаров """)`). 
9. Возвращает список ссылок на товары.


### Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.gearbest.scenario import get_list_products_in_category
from src.suppliers.suppliers_list.gearbest.supplier import Gearbest

supplier = Gearbest()  # Создаем экземпляр класса Gearbest

# Получаем список товаров из категории
products_urls = get_list_products_in_category(supplier)

# Проверяем результат
if products_urls:
    print(f"Найдено {len(products_urls)} товаров")
    for url in products_urls:
        print(url)
else:
    print("Товары не найдены")
```