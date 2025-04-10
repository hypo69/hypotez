# Модуль `via_webdriver`

## Обзор

Модуль `via_webdriver` предназначен для парсинга данных с сайта Kualastyle с использованием веб-драйвера. Он содержит функции для получения списка URL продуктов из определенной категории.

## Подробней

Этот модуль является частью системы сбора данных о товарах от поставщиков. Он использует веб-драйвер для взаимодействия с веб-страницами и извлечения необходимой информации. Расположение файла в структуре проекта указывает на его роль как компонента, отвечающего за взаимодействие с конкретным поставщиком - Kualastyle.

## Функции

### `get_list_products_in_category`

```python
def get_list_products_in_category(s) -> list[str,str,None]:
    """ Returns list of products urls from category page
    Attrs:
        s - Suplier
    @returns
        list of products urls or None
    """
    d = s.driver
    l: dict = s.locators.get('category')
    d.scroll(scroll_count = 10, direction = "forward")

    _ = d.execute_locator
    list_products_in_category = _(l['product_links'])
    #pprint(list_products_in_category)
    return list_products_in_categoryy
```

**Назначение**: Возвращает список URL продуктов со страницы категории.

**Параметры**:
- `s`: Объект поставщика (Suplier), содержащий информацию о драйвере и локаторах.

**Возвращает**:
- `list[str,str,None]`: Список URL продуктов или `None` в случае ошибки.

**Как работает функция**:
1. Извлекает драйвер из объекта поставщика `s`.
2. Получает локаторы категории из объекта поставщика `s`.
3. Прокручивает страницу вниз 10 раз для подгрузки всех товаров.
4. Использует локатор `product_links` для извлечения списка элементов, соответствующих ссылкам на продукты.
5. Возвращает список URL продуктов.

**Примеры**:

Предположим, у нас есть объект поставщика `supplier` с настроенным веб-драйвером и определенными локаторами.

```python
from src.suppliers.kualastyle.via_webdriver import get_list_products_in_category
from unittest.mock import MagicMock

# Мокируем объект поставщика и его атрибуты
supplier = MagicMock()
supplier.driver = MagicMock()
supplier.locators = MagicMock()
supplier.locators.get.return_value = {'product_links': 'locator_value'}
supplier.driver.execute_locator.return_value = ['http://example.com/product1', 'http://example.com/product2']

# Вызываем функцию
product_urls = get_list_products_in_category(supplier)

# Проверяем результат
print(product_urls)
# ['http://example.com/product1', 'http://example.com/product2']