# Модуль: src.suppliers.suppliers_list.amazon.scenario

## Обзор

Модуль предназначен для сбора информации о товарах со страниц категорий поставщика amazon.com с использованием веб-драйвера.

## Подробней

Модуль содержит функции для сбора списка категорий со страниц продавца, списка товаров в каждой категории и передачи управления для обработки полей товара. Он также включает логику для проверки наличия товаров в базе данных магазина.

## Функции

### `get_list_products_in_category`

**Назначение**: Извлекает список URL товаров со страницы категории.

```python
async def get_list_products_in_category(d:'Driver', l:dict) -> list[str,str,None]:
    """ Returns list of products urls from category page
    Если надо пролистстать - страницы категорий - листаю ??????

    Attrs:
    @param s: Supplier - Supplier intstance
    @returns list or one of products urls or None
    """
    ...
```

**Параметры**:

-   `d` (`Driver`): Инстанс драйвера веб-браузера, используемый для взаимодействия со страницей.
-   `l` (`dict`): Словарь, содержащий локаторы элементов для поиска на странице.

**Возвращает**:

-   `list[str,str,None]`: Список URL товаров, найденных на странице категории. Может возвращать `None`, если товары не найдены.

**Как работает функция**:

1.  Выполняет скроллинг страницы.
2.  Использует локатор `'product_links'` для извлечения ссылок на товары.
3.  Если ссылки не найдены, логирует предупреждение и возвращает `None`.
4.  Приводит полученные ссылки к типу списка, если они представлены строкой.
5.  Логирует количество найденных товаров.
6.  Возвращает список URL товаров.

**Примеры**:

```python
from src.webdirver import Driver, Chrome
from src.suppliers.suppliers_list.amazon.scenario import get_list_products_in_category

# Пример использования функции
d = Driver(Chrome)  # Инициализация драйвера Chrome
l = {'product_links': {'by': 'XPATH', 'selector': '//a[@class="product-link"]'}}  # Пример локатора
products = await get_list_products_in_category(d, l)
if products:
    print(f"Найдено {len(products)} товаров")
    for product_url in products:
        print(product_url)
else:
    print("Товары не найдены")
```
```python
products = get_list_products_in_category(d, {'product_links': {'by': 'CSS_SELECTOR', 'selector': '.product-item a'}})