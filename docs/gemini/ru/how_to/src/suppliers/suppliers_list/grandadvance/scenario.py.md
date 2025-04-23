### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код извлекает список URL-адресов товаров со страницы категории поставщика. Он также обрабатывает закрытие баннеров и прокрутку страницы.

Шаги выполнения
-------------------------
1. **Получение драйвера**:
   - Извлекает объект драйвера из объекта поставщика (`s.driver`).

2. **Получение локаторов**:
   - Извлекает локаторы для категории из объекта поставщика (`s.locators['category']`).

3. **Закрытие баннера**:
   - Вызывает метод `execute_locator` для закрытия баннера, используя локаторы из `s.locators['product']['close_banner']`.

4. **Проверка наличия локаторов**:
   - Проверяет, существуют ли локаторы. Если локаторы отсутствуют, записывает сообщение об ошибке в лог и возвращает `None`.

5. **Прокрутка страницы**:
   - Вызывает метод `scroll` для прокрутки страницы.

6. **Извлечение ссылок на товары**:
   - Вызывает метод `execute_locator` для извлечения списка URL-адресов товаров, используя локаторы из `l['product_links']`.

7. **Проверка наличия ссылок**:
   - Проверяет, найдены ли ссылки на товары. Если ссылки отсутствуют, записывает предупреждение в лог и возвращает `None`.

8. **Преобразование ссылок в список**:
   - Преобразует результат в список, если он является строкой.

9. **Логгирование количества найденных товаров**:
   - Записывает в лог количество найденных товаров.

10. **Возврат списка товаров**:
    - Возвращает список URL-адресов товаров.

Пример использования
-------------------------

```python
from src.suppliers.grandadvance.scenario import get_list_products_in_category
from src.suppliers.supplier import Supplier
from src.webdriver import Driver, Chrome  # Предполагается, что Chrome - один из доступных драйверов

# Инициализация объекта поставщика (Supplier)
driver = Driver(Chrome)
supplier = Supplier(
    name="GrandAdvance",
    home_url="https://grandadvance.com",
    driver=driver,
    # Другие необходимые параметры
)

# Определение структуры locators (временная структура, поскольку реальные локаторы отсутствуют)
supplier.locators = {
    'category': {
        'product_links': {
            'by': 'css',
            'selector': '.product-item a',  # пример селектора
            'if_list': 'all',
            'attribute': 'href'
        }
    },
    'product': {
        'close_banner': {
            'by': 'xpath',
            'selector': '//button[@class="close-banner"]',  # пример селектора
            'event': 'click()'
        }
    }
}

# Вызов функции для получения списка товаров
list_products = get_list_products_in_category(supplier)

if list_products:
    print(f"Найдено {len(list_products)} товаров.")
    for product_url in list_products:
        print(product_url)
else:
    print("Не удалось получить список товаров.")

```
```python
def get_list_products_in_category (s: Supplier) -> list[str] | None:    
    """
    Возвращает список URL товаров со страницы категории.

    Args:
        s (Supplier): Объект поставщика.

    Returns:
        list[str] | None: Список URL товаров или None в случае ошибки.
    """
    d = s.driver
    l: dict = s.locators['category']
    d.execute_locator(s.locators['product']['close_banner'])

    if not l:
        logger.error(f"Локаторы отсутствуют: {l}")
        return None

    d.scroll()
    list_products_in_category = d.execute_locator(l['product_links'])
    
    if not list_products_in_category:
        logger.warning('Список URL товаров пуст.')
        return None

    list_products_in_category = [list_products_in_category] if isinstance(list_products_in_category, str) else list_products_in_category

    logger.info(f"Найдено {len(list_products_in_category)} товаров")
    return list_products_in_category