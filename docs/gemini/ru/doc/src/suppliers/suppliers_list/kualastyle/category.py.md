# Модуль для работы с категориями Kualastyle

## Обзор

Модуль предназначен для сбора информации о категориях и товарах с сайта поставщика Kualastyle с использованием веб-драйвера. Он включает в себя функции для получения списка категорий, списка товаров в каждой категории и итерации по страницам категорий.

## Подробней

Этот модуль является частью системы сбора данных о товарах от различных поставщиков в проекте `hypotez`. Он специализируется на поставщике Kualastyle, используя веб-драйвер для навигации по сайту и извлечения необходимой информации. Модуль предоставляет функции для автоматизации процесса сбора данных, такие как получение списка категорий и товаров, а также обработку пагинации на страницах категорий.

## Функции

### `get_list_products_in_category`

```python
def get_list_products_in_category (s: Supplier) -> list[str, str, None]:
    """ Returns list of products urls from category page
    Если надо пролистстать - страницы категорий - листаю ??????

    Attrs:
        s - Supplier
    @returns
        list or one of products urls or None
    """
    ...
```

**Назначение**: Извлекает список URL товаров со страницы категории.

**Параметры**:
- `s` (Supplier): Объект поставщика, содержащий информацию о текущем сценарии и настройки веб-драйвера.

**Возвращает**:
- `list[str, str, None]`: Список URL товаров или `None`, если список товаров не найден.

**Как работает функция**:
1.  Инициализирует драйвер и локаторы из объекта поставщика.
2.  Ожидает загрузки страницы.
3.  Закрывает баннер, если он отображается.
4.  Выполняет прокрутку страницы.
5.  Извлекает список URL товаров с использованием локатора `product_links`.
6.  Если список товаров не найден, логирует предупреждение и возвращает `None`.
7.  Проверяет, изменился ли текущий URL, и если да, то выполняет пагинацию для получения дополнительных товаров.
8.  Объединяет все найденные URL товаров в один список.
9.  Логирует количество найденных товаров в категории.

**Внутренние функции**:

-   `paginator`

**Примеры**:

```python
from src.suppliers import Supplier
from unittest.mock import MagicMock
# Пример вызова функции с использованием мок-объекта Supplier
s = MagicMock(spec=Supplier)
s.driver.execute_locator.return_value = ['https://example.com/product1', 'https://example.com/product2']  # Пример возвращаемого значения
s.locators = {
    'category': {
        'product_links': {'by': 'css', 'selector': '.product-link'}
    },
    'product': {
        'close_banner': {}
    }
}
s.current_scenario = {'name': 'test_category'}
result = get_list_products_in_category(s)
print(result)
# Вывод: ['https://example.com/product1', 'https://example.com/product2']
```

### `paginator`

```python
def paginator(d:Driver, locator: dict, list_products_in_category: list):
    """ Листалка """
    response = d.execute_locator(locator['pagination']['<-'])
    if not response or (isinstance(response, list) and len(response) == 0):
        ...
        return
    return True
```

**Назначение**: Осуществляет переход на следующую страницу категории, если это необходимо.

**Параметры**:
- `d` (Driver): Объект веб-драйвера.
- `locator` (dict): Словарь с локаторами элементов страницы.
- `list_products_in_category` (list): Список URL товаров в текущей категории.

**Возвращает**:
- `True`, если переход на следующую страницу выполнен успешно, иначе `None`.

**Как работает функция**:
1.  Пытается выполнить нажатие на кнопку пагинации (переход на предыдущую страницу) с использованием локатора `'pagination']['<-']`.
2.  Если кнопка не найдена или неактивна, возвращает `None`.
3.  В противном случае возвращает `True`, указывая на успешное выполнение пагинации.

**Примеры**:

```python
from src.webdriver.driver import Driver
from unittest.mock import MagicMock

# Пример вызова функции с использованием мок-объектов Driver и locator
d = MagicMock(spec=Driver)
locator = {'pagination': {'<-': {'by': 'css', 'selector': '.next-page'}}}
list_products_in_category = ['https://example.com/product1']
d.execute_locator.return_value = True  # Пример возвращаемого значения при успешной пагинации

result = paginator(d, locator, list_products_in_category)
print(result)
# Вывод: True
```

### `get_list_categories_from_site`

```python
def get_list_categories_from_site(s):
    """ сборщик актуальных категорий с сайта """
    ...
```

**Назначение**: Собирает актуальные категории с сайта.

**Параметры**:
- `s`: Параметр не документирован в предоставленном коде.

**Возвращает**:
-  Функция не возвращает значение.

**Как работает функция**:
-  Функция не документирована в предоставленном коде.
```