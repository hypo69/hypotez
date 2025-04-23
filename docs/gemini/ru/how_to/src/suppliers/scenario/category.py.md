### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предоставляет функциональность для асинхронного и синхронного обхода категорий на веб-сайте, с целью создания иерархического словаря категорий. Он использует Selenium WebDriver для навигации по страницам и извлечения ссылок на категории, а также сохраняет результаты в JSON-файл.

Шаги выполнения
-------------------------
1. **Инициализация Category**: Создание экземпляра класса `Category`, который наследуется от `PrestaCategoryAsync`. При инициализации передаются учетные данные API.
   ```python
   category_handler = Category(api_credentials={'api_url': 'your_api_url', 'api_key': 'your_api_key'})
   ```

2. **Асинхронный обход категорий (crawl_categories_async)**:
   - Функция `crawl_categories_async` асинхронно обходит категории, начиная с заданного URL, на указанную глубину.
   - Для каждой категории извлекаются ссылки с использованием XPath локатора.
   - Если URL новой категории не дублируется, создается задача для рекурсивного обхода этой категории.
   - Результаты сохраняются в иерархический словарь.
     ```python
   async def main():
       url = "https://example.com/categories"
       depth = 3
       driver = YourWebDriver()  # Инициализация вашего WebDriver
       locator = {"by": "XPATH", "selector": "//a[@class='category-link']"}
       dump_file = "categories.json"
       default_category_id = 1

       category_dict = await category_handler.crawl_categories_async(url, depth, driver, locator, dump_file, default_category_id)
       print(category_dict)
   ```

3. **Синхронный обход категорий (crawl_categories)**:
   - Функция `crawl_categories` выполняет аналогичные действия, но в синхронном режиме.
   - Она также обходит категории, начиная с заданного URL, на указанную глубину, извлекая ссылки с использованием XPath локатора.
   - Если URL новой категории не дублируется, выполняется рекурсивный обход этой категории.
   - Результаты сохраняются в иерархический словарь и записываются в JSON-файл.
     ```python
   url = "https://example.com/categories"
   depth = 2
   driver = YourWebDriver()  # Инициализация вашего WebDriver
   locator = {"by": "XPATH", "selector": "//a[@class='category-link']"}
   dump_file = "categories.json"
   default_category_id = 1

   category_dict = category_handler.crawl_categories(url, depth, driver, locator, dump_file, default_category_id)
   print(category_dict)
   ```

4. **Проверка на дубликаты URL (_is_duplicate_url)**:
   - Функция `_is_duplicate_url` проверяет, существует ли уже URL в словаре категорий, чтобы избежать повторного обхода одних и тех же категорий.
     ```python
   category_dict = {'Category1': {'url': 'https://example.com/category1'}}
   url_to_check = 'https://example.com/category1'
   is_duplicate = category_handler._is_duplicate_url(category_dict, url_to_check)
   print(is_duplicate)  # Вывод: True
   ```

5. **Сравнение и вывод отсутствующих ключей (compare_and_print_missing_keys)**:
   - Функция `compare_and_print_missing_keys` сравнивает ключи в текущем словаре с данными, загруженными из файла, и выводит отсутствующие ключи.
     ```python
   current_dict = {'key1': 'value1', 'key2': 'value2'}
   file_path = 'data.json'  # Предполагается, что data.json содержит {"key2": "old_value2", "key3": "value3"}
   compare_and_print_missing_keys(current_dict, file_path)  # Вывод: key3
   ```

Пример использования
-------------------------

```python
import asyncio
from src.suppliers.scenario.category import Category
from src.webdriver import Driver, Firefox

# Создание экземпляра класса Category с учетными данными API
category_handler = Category(api_credentials={'api_url': 'your_api_url', 'api_key': 'your_api_key'})

# Параметры для обхода категорий
url = "https://example.com/categories"
depth = 2
driver = Driver(Firefox)  # Инициализация вашего WebDriver
locator = {"by": "XPATH", "selector": "//a[@class='category-link']"}
dump_file = "categories.json"
default_category_id = 1


async def main():
    # Асинхронный обход категорий
    category_dict = await category_handler.crawl_categories_async(url, depth, driver, locator, dump_file, default_category_id)
    print(category_dict)

if __name__ == "__main__":
    asyncio.run(main())