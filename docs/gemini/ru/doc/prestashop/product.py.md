### Анализ кода модуля `src/endpoints/prestashop/product.py`

## Обзор

Этот модуль предназначен для взаимодействия с товарами в PrestaShop. Он содержит класс `PrestaProduct`, который позволяет получать информацию о товарах, добавлять новые товары и выполнять другие операции.

## Подробней

Модуль `src/endpoints/prestashop/product.py` определяет класс `PrestaProduct`, который предоставляет методы для взаимодействия с API PrestaShop для управления товарами. Он включает в себя функциональность для получения схемы товара, получения информации о товаре по ID и добавления новых товаров.

## Классы

### `PrestaProduct`

**Описание**: Класс для управления товарами в PrestaShop.

**Наследует**:

-   `src.endpoints.prestashop.api.PrestaShop`

**Методы**:

-   `__init__(self, api_key: Optional[str] = '', api_domain: Optional[str] = '', *args, **kwargs) -> None`: Инициализирует объект `PrestaProduct`.
-   `get_product_schema(self, resource_id: Optional[str | int] = None, schema: Optional[str] = None) -> dict`: Получает схему для ресурса продукта из PrestaShop.
-   `get_parent_category(self, id_category: int) -> Optional[int]`: Получает родительские категории из PrestaShop для заданной категории рекурсивно.
-   `_add_parent_categories(self, f: ProductFields) -> None`: Вычисляет и добавляет все родительские категории для списка ID категорий к объекту ProductFields.
-   `get_product(self, id_product: int, **kwards) -> dict`: Возвращает словарь полей товара из магазина PrestaShop.
-   `add_new_product(self, f: ProductFields) -> dict`: Добавляет новый продукт в PrestaShop.

#### `__init__`

**Назначение**: Инициализирует объект `PrestaProduct`.

```python
def __init__(self, api_key: Optional[str] = '', api_domain: Optional[str] = '', *args, **kwargs) -> None:
    """Initializes a Product object.

    Args:
        api_key (Optional[str], optional): PrestaShop API key. Defaults to ''.
        api_domain (Optional[str], optional): PrestaShop API domain. Defaults to ''.

    Returns:
        None
    """
    ...
```

**Параметры**:

-   `api_key` (Optional[str]): Ключ API для доступа к PrestaShop.
-   `api_domain` (Optional[str]): Доменное имя PrestaShop.
-    `*args`: Произвольные позиционные аргументы, передаваемые в конструктор базового класса.
-   `**kwargs`: Произвольные именованные аргументы, передаваемые в конструктор базового класса.

**Как работает функция**:

1.  Вызывает конструктор базового класса `PrestaShop`, передавая ему ключ API и доменное имя.

#### `get_product_schema`

**Назначение**: Получает схему для ресурса продукта из PrestaShop.

```python
def get_product_schema(self, resource_id: Optional[str | int] = None, schema: Optional[str] = None) -> dict:
    """Get the schema for the product resource from PrestaShop.

    Args:
        resource_id (Optional[str  |  int], optional): The ID of the product resource. Defaults to None.
        schema (Optional[str], optional): The schema type. Defaults to 'blank'.
            - blank	Пустой шаблон ресурса: все поля присутствуют, но без значений. Обычно используется для создания нового объекта.
            - synopsis	Минимальный набор полей: только обязательные поля и краткая структура. Подходит для быстрого обзора.
            - null / не передавать параметр	Возвращает полную схему ресурса со всеми возможными полями, типами и ограничениями.

    Returns:
        dict: The schema for the product resource.
    """
    ...
```

**Параметры**:

-   `resource_id` (Optional[str | int]): ID ресурса продукта. По умолчанию `None`.
-   `schema` (Optional[str]): Тип схемы. По умолчанию `'blank'`. Может принимать значения 'blank', 'synopsis' или `None`.

**Возвращает**:

-   `dict`: Схема ресурса продукта.

**Как работает функция**:

1.  Вызывает метод `get_schema` базового класса `PrestaShop` для получения схемы продукта из API PrestaShop.

#### `get_parent_category`

**Назначение**: Получает родительские категории из PrestaShop для заданной категории рекурсивно.

```python
def get_parent_category(self, id_category: int) -> Optional[int]:
    """Retrieve parent categories from PrestaShop for a given category recursively.

    Args:
        id_category (int): The category ID.

    Returns:
        Optional[int]: parent category id (int).
    """
    ...
```

**Параметры**:

-   `id_category` (int): ID категории.

**Возвращает**:

-   `Optional[int]`: ID родительской категории или `None` в случае ошибки.

**Как работает функция**:

1.  Получает данные о категории из PrestaShop, используя метод `self.read`.
2.  Извлекает ID родительской категории из полученных данных.
3.  Возвращает ID родительской категории.
4.  Логирует информацию об ошибках, используя `logger.error`.

#### `_add_parent_categories`

**Назначение**: Вычисляет и добавляет все родительские категории для списка ID категорий к объекту `ProductFields`.

```python
def _add_parent_categories(self, f: ProductFields) -> None:
    """Calculates and appends all parent categories for a list of category IDs to the ProductFields object.

    Args:
        f (ProductFields): The ProductFields object to append parent categories to.
    """
    ...
```

**Параметры**:

-   `f` (ProductFields): Объект `ProductFields`, к которому нужно добавить родительские категории.

**Как работает функция**:

1.  Перебирает категории в списке `f.additional_categories`.
2.  Для каждой категории, если ее ID не равен 1 или 2 (корневые категории), рекурсивно получает ID родительской категории, используя функцию `self.get_parent_category`.
3.  Добавляет полученные ID родительских категорий в список `f.additional_categories`.

#### `get_product`

**Назначение**: Возвращает словарь полей товара из магазина PrestaShop.

```python
def get_product(self, id_product: int, **kwards) -> dict:
    """Возваращает словарь полей товара из магазина Prestasop

    Args:
        id_product (int): значение поля ID в таблице `product` Preastashop

    Returns:
        dict:
        {
            'product':
                {... product fields}
        }
    """
    ...
```

**Параметры**:

-   `id_product` (int): Значение поля ID в таблице `product` Preastashop.
-    `**kwards`: Произвольные именованные аргументы.

**Возвращает**:

-   `dict`: Словарь, содержащий поля товара.

**Как работает функция**:

1.  Формирует словарь параметров запроса `kwards` с указанием формата данных (`JSON`).
2.  Вызывает функцию `self.read` с указанием ресурса `products` и идентификатором товара `id_product`.

#### `add_new_product`

**Назначение**: Добавляет новый продукт в PrestaShop.

```python
def add_new_product(self, f: ProductFields) -> dict:
    """Add a new product to PrestaShop.

    Преобразовывает объект `ProducFields` в словарь формата `Prestashop` и отрапавлет его в API Престашоп

    Args:
        f (ProductFields): An instance of the ProductFields data class containing the product information.

    Returns:
        dict: Returns the `ProductFields` object with `id_product` set, if the product was added successfully, `None` otherwise.
    """
    ...
```

**Параметры**:

-   `f` (ProductFields): Объект `ProductFields`, содержащий информацию о товаре.

**Возвращает**:

-   `dict`: Объект `ProductFields` с установленным `id_product`, если товар был успешно добавлен, `None` в противном случае.

**Как работает функция**:

1.  Добавляет `id_category_default` в поле `additional_categories` для поиска его родительских категорий.
2.  Вызывает функцию `_add_parent_categories` для добавления родительских категорий к объекту `ProductFields`.
3.  Получает схему продукта, используя функцию `self.get_product_schema`.
4.  Преобразует объект `ProductFields` в словарь формата PrestaShop.
5.  Преобразует словарь в XML формат, используя функцию `dict2xml`.
6.  Отправляет XML данные в API PrestaShop для создания нового продукта, используя метод `self.create`.
7.  Сохраняет XML представление данных в файл.
8.  Если добавление прошло успешно, извлекает ID добавленного товара из ответа сервера и сохраняет его в объекте `ProductFields`.
9.  Логирует информацию об успехе или ошибке, используя `logger.info` и `logger.error`.

## Переменные модуля

-  В модуле отсутствуют переменные модуля как таковые, но используются локальные переменные внутри функций:

## Пример использования

```python
from src.endpoints.prestashop.product import PrestaProduct
from src.endpoints.prestashop.product_fields import ProductFields
import asyncio
import pathlib
from pathlib import Path

# Пример использования
async def main():
    # Укажите свои учетные данные PrestaShop
    api_credentials = {'api_domain': 'your_api_domain', 'api_key': 'your_api_key'}
    
    # Создаем экземпляр класса PrestaProduct
    product = PrestaProduct(api_key=api_credentials['api_key'], api_domain=api_credentials['api_domain'])
    
    # Подготовка данных для создания нового продукта
    product_fields = ProductFields(
        name='Test Product',
        price=19.99,
        quantity=100,
        description='A test product for demonstration.',
        id_category_default=2,  # Укажите ID категории по умолчанию
        additional_categories=[{'id': '3'}]  # Укажите дополнительные категории
    )
    
    # Устанавливаем путь для сохранения изображений
    img_path = pathlib.Path('путь_к_локальному_изображению')
    product_fields.local_image_path = img_path
    # Добавляем продукт
    new_product = product.add_new_product(product_fields)
    
    if new_product:
        print(f"Product added successfully with ID: {new_product.id}")
    else:
        print("Failed to add product.")

if __name__ == "__main__":
    asyncio.run(main())
```

## Взаимосвязь с другими частями проекта

-   Модуль `src/endpoints/prestashop/product.py` зависит от библиотеки `selenium` для управления браузером Chrome, от модуля `src.webdriver.executor` для выполнения действий с веб-элементами, от модуля `src.webdriver.js` для выполнения JavaScript-кода, от модуля `fake_useragent` для генерации случайных User-Agent, от модуля `src.logger.logger` для логирования и от модуля `src.utils.jjson` для загрузки конфигурации.
- Он также зависит от модуля `src.webdriver.proxy` для настройки прокси.
-   Он предоставляет класс `Chrome`, который используется в других модулях для создания и управления веб-драйвером Chrome.

Зависимости:

-   `src.endpoints.prestashop.api`: Для взаимодействия с API PrestaShop.
-   `src.endpoints.prestashop.category`: Для получения родительских категорий.
-   `src.endpoints.prestashop.product_fields`: Для представления данных о товаре.
-   `src.utils.convertors.dict`: Для преобразования словарей в XML.
-   `src.utils.xml`: Для сохранения XML в файл.
-   `src.utils.file`: Для сохранения текста в файл.
-   `src.utils.jjson`: Для загрузки и сохранения JSON данных.
-   `src.logger.logger`: Для логирования.