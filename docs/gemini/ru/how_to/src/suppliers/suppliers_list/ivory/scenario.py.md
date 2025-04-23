### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код отвечает за сбор списка товаров с веб-страницы категории поставщика, а также за навигацию по страницам категорий, если требуется перелистывание.

Шаги выполнения
-------------------------
1. **Инициализация**: Функция `get_list_products_in_category` принимает объект `Supplier` (поставщика) в качестве аргумента. Из объекта извлекаются необходимые параметры, такие как драйвер веб-браузера (`d`), локаторы элементов (`l`) и текущий сценарий.
2. **Ожидание и закрытие баннера**: Код ожидает 1 секунду (`d.wait(1)`) и пытается закрыть баннер, используя локатор `close_banner` (`d.execute_locator(s.locators['product']['close_banner'])`).
3. **Прокрутка страницы**: Выполняется прокрутка страницы (`d.scroll()`).
4. **Извлечение ссылок на товары**: Извлекаются ссылки на товары с текущей страницы категории с использованием локатора `product_links` (`list_products_in_category: List = d.execute_locator(l['product_links'])`). Если ссылки не найдены, функция логирует предупреждение и завершается.
5. **Пагинация**: Если на странице есть пагинация, код переходит на следующую страницу и добавляет новые ссылки на товары в общий список. Это происходит до тех пор, пока URL текущей страницы не изменится. Функция `paginator` используется для переключения страниц. Она нажимает на кнопку "следующая страница" (`locator['pagination']['<-']`). Если кнопка не найдена, функция завершается.
6. **Формирование списка**: Преобразует результат в список, если это строка.
7. **Логирование количества товаров**: В конце функция логирует количество найденных товаров в текущей категории.
8. **Возврат списка**: Возвращает список URL товаров.

Пример использования
-------------------------

```python
from src.suppliers.suppliers import Supplier  # Предполагаемый путь к классу Supplier
from src.webdriver.driver import Driver  # Предполагаемый путь к классу Driver
from selenium import webdriver
from src.config import Config

def example_usage(supplier_url: str):
    """
    Пример использования функции get_list_products_in_category.
    """
    # 1. Создание экземпляра Supplier (пример)
    config = Config()
    driver_instance = Driver(webdriver.Chrome, config)  # Инициализация вашего драйвера
    supplier = Supplier(driver_instance)
    supplier.url = supplier_url
    supplier.driver.get_page(supplier.url)
    supplier.locators = {
        'category': {
            'product_links': {
                'by': 'css selector',
                'selector': '.product a',
                'attribute': 'href'
            },
            'pagination': {
                '<-': {
                    'by': 'css selector',
                    'selector': '.next-page a',
                    'attribute': 'href'
                }
            }
        },
        'product': {
            'close_banner': {
                'by': 'css selector',
                'selector': '.close-banner',
                'event': 'click()'
            }
        }
    }

    # 2. Вызов функции
    product_links = get_list_products_in_category(supplier)

    # 3. Обработка полученных ссылок
    if product_links:
        print(f"Найдено {len(product_links)} ссылок на товары.")
        for link in product_links:
            print(link)
    else:
        print("Не удалось получить ссылки на товары.")

# Пример вызова
example_usage("https://ivory.co.il/catalog.php?id=289")