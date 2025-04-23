### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Функция `get_list_products_in_category` извлекает список URL товаров со страницы категории, используя веб-драйвер для взаимодействия с сайтом поставщика. Функция также обрабатывает пагинацию, прокручивая страницу и собирая ссылки на товары с каждой страницы.

Шаги выполнения
-------------------------
1. **Инициализация**:
   - Извлекает драйвер (`d`) и локаторы (`l`) из объекта поставщика (`s`). Локаторы используются для поиска элементов на странице.
2. **Ожидание и закрытие баннера**:
   - Ожидает 1 секунду, чтобы убедиться, что страница загрузилась.
   - Вызывает функцию `execute_locator` для закрытия баннера, если он есть. Использует локатор `close_banner` из настроек поставщика.
3. **Прокрутка страницы**:
   - Выполняет прокрутку страницы вниз, чтобы подгрузить все элементы, которые могут быть скрыты.
4. **Извлечение ссылок на товары**:
   - Использует `execute_locator` с локатором `product_links` для извлечения списка ссылок на товары.
5. **Обработка отсутствия ссылок**:
   - Проверяет, найдены ли ссылки на товары. Если нет, записывает предупреждение в лог и возвращает `None`.
6. **Пагинация**:
   - Запускает цикл, который продолжается, пока текущий URL не отличается от предыдущего (т.е. пока происходит переход на новую страницу).
   - Вызывает функцию `paginator` для перехода на следующую страницу. Если `paginator` возвращает `True`, добавляет новые ссылки на товары в список. Если `paginator` возвращает `False`, цикл завершается.
7. **Форматирование результата**:
   - Преобразует результат в список, если он является строкой.
8. **Логгирование и возврат**:
   - Записывает в лог количество найденных товаров в категории.
   - Возвращает список URL товаров.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.wallashop.scenario import Supplier
from src.webdriver.driver import Driver
from src.config.config import Config

def example_usage():
    # Создаем экземпляр драйвера (например, Chrome)
    driver = Driver(browser=Config.browser)

    # Определяем базовые локаторы
    locators = {
        'category': {
            'product_links': {
                'by': 'CSS_SELECTOR',
                'selector': '.product-item a',
                'attribute': 'href'
            },
            'close_banner': {
                'by': 'XPATH',
                'selector': '//button[@class="close-banner"]',
                'event': 'click()'
            },
            'pagination': {
                '<-': {
                    'by': 'CSS_SELECTOR',
                    'selector': '.next-page a',
                    'event': 'click()'
                }
            }
        },
        'product':{
            'close_banner':{
                'attribute': None,
                'by': 'XPATH',
                'selector': "//button[@id = 'closeXButton']",
                'if_list': 'first',
                'use_mouse': False,
                'mandatory': False,
                'timeout': 0,
                'timeout_for_event': "presence_of_element_located",
                'event': "click()",
                'locator_description': "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
        }
        }
    }

    # Создаем экземпляр поставщика
    supplier = Supplier(
        name='ExampleSupplier',
        start_urls=['https://example.com/category'],
        locators=locators,
        driver=driver,
        current_scenario={'name': 'ExampleCategory'}
    )

    # Получаем список товаров в категории
    product_urls = get_list_products_in_category(supplier)

    if product_urls:
        print(f"Found {len(product_urls)} product URLs:")
        for url in product_urls:
            print(url)
    else:
        print("No product URLs found.")

    # Закрываем драйвер
    driver.close()

# Запускаем пример использования
# example_usage() # раскомментируйте для запуска