### Как использовать блок кода `get_list_products_in_category`
=========================================================================================

Описание
-------------------------
Функция `get_list_products_in_category` извлекает список URL товаров со страницы категории. Она использует объект `Supplier` для доступа к драйверу веб-браузера и локаторам элементов на странице. Функция также обрабатывает пагинацию, прокручивая страницу и собирая ссылки на товары, пока не будут собраны все товары в категории.

Шаги выполнения
-------------------------
1. **Инициализация**:
   - Функция принимает объект `Supplier` (`s`) в качестве аргумента, содержащий информацию о поставщике, включая драйвер веб-браузера и локаторы элементов.
   - Извлекает драйвер (`d`) и локаторы (`l`) из объекта `Supplier`.

2. **Ожидание и закрытие баннера**:
   - Выполняется ожидание в течение 1 секунды (`d.wait(1)`), чтобы убедиться, что страница загружена.
   - Функция пытается закрыть всплывающий баннер, используя локатор `close_banner` (`d.execute_locator(s.locators['product']['close_banner'])`).
   - Выполняется прокрутка страницы (`d.scroll()`), чтобы загрузить все элементы, видимые на странице.

3. **Извлечение ссылок на товары**:
   - Извлекаются ссылки на товары с использованием локатора `product_links` (`list_products_in_category: List = d.execute_locator(l['product_links'])`).
   - Если ссылки не найдены, функция логирует предупреждение и возвращает `None`.

4. **Обработка пагинации**:
   - Функция проверяет, изменился ли текущий URL страницы (`d.current_url != d.previous_url`). Если URL изменился, значит, произошел переход на следующую страницу пагинации.
   - Функция вызывает функцию `paginator` для перехода на следующую страницу и добавления новых ссылок на товары в список `list_products_in_category`.
   - Цикл продолжается до тех пор, пока функция `paginator` возвращает `True` и URL страницы меняется.

5. **Форматирование результата**:
   - Если `list_products_in_category` является строкой, она преобразуется в список, чтобы обеспечить единообразный формат возвращаемого значения.

6. **Логирование и возврат результата**:
   - Функция логирует количество найденных товаров в категории.
   - Функция возвращает список URL товаров (`list_products_in_category`).

Пример использования
-------------------------

```python
from src.suppliers.suppliers import Supplier
from src.webdriver.driver import Driver
from typing import Dict

def get_list_products_in_category(s: Supplier) -> list[str]:
    """Возвращает список URL товаров со страницы категории."""
    d: Driver = s.driver
    l: Dict = s.locators['category']

    d.wait(1)
    d.execute_locator(s.locators['product']['close_banner'])
    d.scroll()

    list_products_in_category: list[str] = d.execute_locator(l['product_links'])

    if not list_products_in_category:
        print('Нет ссылок на товары.')
        return []

    while d.current_url != d.previous_url:
        if paginator(d, l, list_products_in_category):
            new_products = d.execute_locator(l['product_links'])
            if isinstance(new_products, str):
                list_products_in_category.append(new_products)
            elif isinstance(new_products, list):
                list_products_in_category.extend(new_products)
        else:
            break

    print(f"Найдено {len(list_products_in_category)} товаров в категории.")
    return list_products_in_category

def paginator(d: Driver, locator: dict, list_products_in_category: list) -> bool:
    """Листалка"""
    response = d.execute_locator(locator['pagination']['<-'])
    if not response or (isinstance(response, list) and len(response) == 0):
        return False
    return True

# Пример использования:
# Предположим, что у вас есть объект Supplier `supplier_instance`
# product_urls = get_list_products_in_category(supplier_instance)
# if product_urls:
#     for url in product_urls:
#         print(url)