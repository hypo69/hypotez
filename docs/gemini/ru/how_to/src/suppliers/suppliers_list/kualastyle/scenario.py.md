### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Функция `get_list_products_in_category(s: Supplier) -> list[str, str, None]` извлекает список URL товаров со страницы категории, предоставленной поставщиком (`Supplier`). Она также обрабатывает пролистывание страниц категорий, если это необходимо.

Шаги выполнения
-------------------------
1. **Инициализация**:
   - Извлекает драйвер (`d: Driver`) и локаторы (`l: dict`) из объекта поставщика (`s: Supplier`).
2. **Ожидание и закрытие баннера**:
   - Ожидает 1 секунду (`d.wait(1)`).
   - Выполняет локатор для закрытия баннера (`d.execute_locator(s.locators['product']['close_banner'])`).
3. **Прокрутка страницы**:
   - Выполняет прокрутку страницы (`d.scroll()`).
4. **Извлечение ссылок на товары**:
   - Извлекает список ссылок на товары (`list_products_in_category: List`) с использованием локатора `l['product_links']`.
   - Если список ссылок пуст, записывает предупреждение в лог (`logger.warning('Нет ссылок на товары. Так бывает')`) и возвращает `None`.
5. **Пагинация (пролистывание страниц)**:
   - Проверяет, изменился ли текущий URL (`d.current_url`) по сравнению с предыдущим (`d.previous_url`).
   - Если URL изменился, вызывает функцию `paginator(d, l, list_products_in_category)` для обработки пагинации.
   - Если `paginator` возвращает `True`, добавляет новые ссылки на товары в `list_products_in_category`.
   - Если `paginator` возвращает `False`, прекращает пролистывание.
6. **Обработка списка товаров**:
   - Преобразует `list_products_in_category` в список, если это строка.
7. **Логирование и возврат результата**:
   - Записывает в лог количество найденных товаров в категории (`logger.debug(f"Found {len(list_products_in_category)} items in category {s.current_scenario['name']}")`).
   - Возвращает список URL товаров (`list_products_in_category`).

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.kualastyle.scenario import get_list_products_in_category
from src.supplier import Supplier
from src.webdriver.driver import Driver
from typing import Dict

# Пример объекта Supplier (может потребоваться адаптация под реальную структуру)
class MockSupplier(Supplier):
    def __init__(self, driver: Driver, locators: Dict, current_scenario: Dict):
        self.driver = driver
        self.locators = locators
        self.current_scenario = current_scenario
        self.previous_url = None
        self.current_url = None

# Создаем мок-объект Driver и Supplier
# driver = Driver(browser_name="chrome")  # Раскомментируйте, если нужен реальный драйвер
locators = {
    'category': {
        'product_links': {
            'by': 'CSS_SELECTOR',
            'selector': '.product-item a',
            'attribute': 'href'
        },
        'pagination': {
            '<-': {
                'by': 'CSS_SELECTOR',
                'selector': '.next-page',
                'attribute': 'href'
            }
        }
    },
    'product': {
        'close_banner': {
            'by': 'XPATH',
            'selector': '//button[@id="closeXButton"]',
            'event': 'click()'
        }
    }
}
current_scenario = {'name': 'Example Category'}

# supplier = MockSupplier(driver, locators, current_scenario)
# urls = get_list_products_in_category(supplier)

# if urls:
#     print(f"Найдено {len(urls)} URL товаров.")
#     for url in urls:
#         print(url)
# else:
#     print("Не удалось получить список URL товаров.")
```