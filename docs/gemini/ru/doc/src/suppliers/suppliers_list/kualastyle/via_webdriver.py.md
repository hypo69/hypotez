# Модуль `via_webdriver.py`

## Обзор

Модуль `via_webdriver.py` предназначен для парсинга данных с сайта Kualastyle с использованием веб-драйвера. Он содержит функции для получения списка URL продуктов из категории на странице сайта.

## Подробней

Этот модуль является частью пакета `src.suppliers.kualastyle` и отвечает за автоматизированный сбор информации о продуктах с сайта Kualastyle. Он использует веб-драйвер для навигации по сайту, прокрутки страниц и извлечения URL продуктов.

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

**Назначение**: Функция извлекает список URL продуктов со страницы категории сайта Kualastyle.

**Параметры**:
- `s`: Объект поставщика (Supplier), содержащий информацию о драйвере веб-драйвера и локаторах элементов на странице.

**Возвращает**:
- `list[str, str, None]`: Список URL продуктов или `None` в случае неудачи.

**Как работает функция**:

1.  Извлекает драйвер веб-драйвера из объекта поставщика `s` и присваивает его переменной `d`.
2.  Извлекает локаторы для категории из объекта поставщика `s` и присваивает их переменной `l`.
3.  Выполняет прокрутку страницы вниз 10 раз для загрузки всех продуктов на странице.
4.  Использует метод `execute_locator` драйвера `d` для поиска элементов, соответствующих локатору `product_links` из словаря `l`.
5.  Возвращает список найденных URL продуктов.

**Примеры**:

Предположим, у нас есть объект `supplier`, представляющий поставщика Kualastyle.

```python
from src.suppliers.suppliers_list.kualastyle.via_webdriver import get_list_products_in_category
from src.webdriver import Driver, Chrome

# Пример объекта поставщика (необходимо настроить драйвер и локаторы)
class Supplier:
    def __init__(self):
        self.driver = Driver(Chrome)  # Инициализация драйвера (пример с Chrome)
        self.locators = {
            'category': {
                'product_links': {
                    'by': 'CSS_SELECTOR',
                    'selector': '.product-item a',
                    'attribute': 'href'
                }
            }
        }

supplier = Supplier()
product_list = get_list_products_in_category(supplier)

if product_list:
    print(f"Найдено {len(product_list)} продуктов")
    for product_url in product_list[:5]:  # Вывод первых 5 URL
        print(product_url)
else:
    print("Не удалось получить список продуктов")