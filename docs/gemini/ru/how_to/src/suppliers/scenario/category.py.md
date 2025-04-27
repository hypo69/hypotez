## Как использовать класс `Category`
=========================================================================================

### Описание
-------------------------

Класс `Category` реализует функционал для работы с категориями товаров, преимущественно в контексте PrestaShop. 
Он наследует функционал от `PrestaCategoryAsync` и обеспечивает асинхронное сканирование категорий сайта с построением иерархической структуры категорий в виде словаря.

### Шаги выполнения
-------------------------

1. **Инициализация объекта**:
    - Создайте объект `Category` с передачей API-ключа доступа к данным категорий.
2. **Асинхронное сканирование**:
    - Используйте метод `crawl_categories_async` для асинхронного сканирования категорий с указанием URL, глубины рекурсии, веб-драйвера, локатора для ссылок на категории, файла для сохранения результатов, идентификатора категории по умолчанию и (опционально) существующего словаря категорий.
3. **Синхронное сканирование**:
    - Используйте метод `crawl_categories` для синхронного сканирования категорий с теми же параметрами, что и в асинхронном варианте.
4. **Проверка на дубликаты**:
    - Метод `_is_duplicate_url` проверяет, существует ли URL в словаре категорий.
5. **Сравнение и печать отсутствующих ключей**:
    - Функция `compare_and_print_missing_keys` сравнивает текущий словарь с данными из файла и печатает отсутствующие ключи.

### Пример использования
-------------------------

```python
from src.suppliers.scenario.category.category import Category

# Инициализация объекта Category с API-ключами
category_handler = Category(api_credentials={'key': 'your_api_key'})

# Параметры для сканирования
url = 'https://www.example.com/categories/'
depth = 2  # Глубина рекурсии
locator = {'by': 'XPATH', 'selector': '//a[contains(@class, "category-link")]'}
dump_file = 'categories.json'
default_category_id = 100

# Асинхронное сканирование
categories = asyncio.run(category_handler.crawl_categories_async(url, depth, driver, locator, dump_file, default_category_id))

# Синхронное сканирование
categories = category_handler.crawl_categories(url, depth, driver, locator, dump_file, default_category_id)

# Проверка на дубликаты
is_duplicate = category_handler._is_duplicate_url(categories, 'https://www.example.com/categories/new-category')

# Сравнение и печать отсутствующих ключей
compare_and_print_missing_keys(categories, 'categories_old.json')
```