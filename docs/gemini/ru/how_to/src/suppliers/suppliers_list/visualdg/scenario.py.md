### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Функция `get_list_products_in_category` извлекает список URL товаров со страницы категории поставщика. Она использует веб-драйвер для взаимодействия со страницей, прокручивает страницу, чтобы загрузить все товары, и собирает ссылки на товары. Также реализована пагинация для обработки страниц категорий, которые разделены на несколько страниц. Функция возвращает список URL товаров или `None`, если ссылки не найдены.

Шаги выполнения
-------------------------
1. **Инициализация**:
   - Получение экземпляра веб-драйвера `d` из объекта поставщика `s`.
   - Получение локаторов `l` для элементов категории из объекта поставщика `s`.

2. **Ожидание и закрытие баннера**:
   - Ожидание в течение 1 секунды (`d.wait(1)`).
   - Выполнение локатора для закрытия баннера, если он есть (`d.execute_locator(s.locators['product']['close_banner'])`).

3. **Прокрутка страницы**:
   - Выполнение прокрутки страницы до конца для загрузки всех товаров (`d.scroll()`).

4. **Получение списка товаров**:
   - Извлечение списка ссылок на товары с использованием локатора `product_links` (`list_products_in_category: List = d.execute_locator(l['product_links'])`).

5. **Обработка отсутствия ссылок**:
   - Если список ссылок пуст, логируется предупреждение и возвращается `None`.

6. **Пагинация**:
   - Проверка, изменился ли URL текущей страницы (`while d.current_url != d.previous_url`).
   - Если URL изменился, вызывается функция `paginator` для перехода на следующую страницу.
   - Если `paginator` возвращает `True`, добавляются ссылки на товары со следующей страницы в `list_products_in_category`.
   - Если `paginator` возвращает `False`, цикл завершается.

7. **Преобразование результата**:
   - Преобразование `list_products_in_category` в список, если это строка.

8. **Логирование и возврат**:
   - Логирование количества найденных товаров в категории.
   - Возврат списка URL товаров.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.visualdg.scenario import get_list_products_in_category
from src.supplier import Supplier  # Предполагается, что Supplier класс определен в supplier.py
from src.webdriver.driver import Driver
from typing import Dict

# Mock класс Driver
class MockDriver(Driver):
    def __init__(self):
        pass
    def wait(self, sec):
        pass
    def execute_locator(self, locator):
        return ["https://example.com/product1", "https://example.com/product2"]
    def scroll(self):
        pass
    @property
    def current_url(self):
        return "https://example.com/category"
    @property
    def previous_url(self):
        return "https://example.com/category_old"


# Mock класс Supplier
class MockSupplier(Supplier):
    def __init__(self, driver: Driver, locators: Dict):
        self.driver = driver
        self.locators = locators
        self.current_scenario = {'name': 'test_category'}
    @property
    def current_url(self):
        return "https://example.com/category"
    @property
    def previous_url(self):
        return "https://example.com/category_old"

# Пример использования
driver = MockDriver()
locators = {
    'category': {
        'product_links': {'selector': 'a.product-link'}
    },
    'product': {
        'close_banner': {'selector': '#close-banner'}
    }
}
supplier = MockSupplier(driver, locators)

product_urls = get_list_products_in_category(supplier)
if product_urls:
    print(f"Found product URLs: {product_urls}")
else:
    print("No product URLs found.")
```
```markdown
### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Функция `paginator` отвечает за навигацию по страницам категорий товаров, когда результаты поиска разделены на несколько страниц. Она использует веб-драйвер для клика по кнопке пагинации (например, "следующая страница") и проверяет, был ли выполнен переход на новую страницу. Функция возвращает `True`, если переход был успешен, и `None`, если нет.

Шаги выполнения
-------------------------
1. **Выполнение локатора для пагинации**:
   - Попытка клика по кнопке "следующая страница" с использованием локатора `locator['pagination']['<-']` (`response = d.execute_locator(locator['pagination']['<-'])`).

2. **Проверка результата**:
   - Проверка, был ли получен ответ от выполнения локатора и не является ли ответ пустым списком (если `response` это список).
   - Если ответ отсутствует или является пустым списком, логируется отладочное сообщение и возвращается `None`.

3. **Возврат результата**:
   - Если переход на следующую страницу был успешен, возвращается `True`.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.visualdg.scenario import paginator
from src.webdriver.driver import Driver

# Mock класс Driver
class MockDriver(Driver):
    def __init__(self):
        pass
    def execute_locator(self, locator):
        # Имитация успешного клика по кнопке пагинации
        return True

# Пример использования
driver = MockDriver()
locator = {
    'pagination': {
        '<-': {'selector': '.next-page'}
    }
}
list_products_in_category = ["https://example.com/product1"]  # Пример списка товаров

result = paginator(driver, locator, list_products_in_category)
if result:
    print("Переход на следующую страницу выполнен успешно.")
else:
    print("Переход на следующую страницу не выполнен.")
```
```markdown
### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Функция `get_list_categories_from_site` отвечает за сбор актуального списка категорий с сайта поставщика. Она использует веб-драйвер для взаимодействия с сайтом, находит элементы, содержащие ссылки на категории, и извлекает эти ссылки.

Шаги выполнения
-------------------------
1. **Инициализация**:
   - Функция принимает объект поставщика `s`, содержащий информацию о драйвере и локаторах.

2. **Извлечение категорий**:
   - Функция использует драйвер `s.driver` для поиска элементов, соответствующих локаторам категорий на сайте.

3. **Обработка и возврат**:
   - Функция возвращает список найденных категорий.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.visualdg.scenario import get_list_categories_from_site
from src.supplier import Supplier  # Предполагается, что Supplier класс определен в supplier.py
from src.webdriver.driver import Driver
from typing import Dict

# Mock класс Driver
class MockDriver(Driver):
    def __init__(self):
        pass
    def execute_locator(self, locator):
        # Имитация успешного поиска категорий
        return ["https://example.com/category1", "https://example.com/category2"]

# Mock класс Supplier
class MockSupplier(Supplier):
    def __init__(self, driver: Driver, locators: Dict):
        self.driver = driver
        self.locators = locators

# Пример использования
driver = MockDriver()
locators = {
    'categories': {
        'category_links': {'selector': 'a.category-link'}
    }
}
supplier = MockSupplier(driver, locators)

category_urls = get_list_categories_from_site(supplier)
if category_urls:
    print(f"Found category URLs: {category_urls}")
else:
    print("No category URLs found.")