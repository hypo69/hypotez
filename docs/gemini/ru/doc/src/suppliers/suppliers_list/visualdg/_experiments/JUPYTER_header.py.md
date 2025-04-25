# Модуль для запуска поставщика

## Обзор

Модуль содержит функцию `start_supplier`, которая запускает процесс извлечения данных о товарах от выбранного поставщика. 

## Подробнее

Модуль `src.suppliers.visualdg._experiments/JUPYTER_header.py`  занимается инициализацией поставщика данных о товарах. 
Он импортирует необходимые модули, определяет корневой путь к проекту и запускает функцию `start_supplier`. 

## Функции

### `start_supplier`

```python
def start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en' ):
    """ Старт поставщика 
    Args:
        supplier_prefix (str, optional): Префикс поставщика (например, 'aliexpress'). По умолчанию 'aliexpress'.
        locale (str, optional): Локаль для сбора данных (например, 'en'). По умолчанию 'en'.
        
    Returns:
        Supplier: Экземпляр класса Supplier с настроенными параметрами.
    """
    params: dict = \
    {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params)
```

**Назначение**: Функция запускает процесс извлечения данных от поставщика.
**Параметры**:
- `supplier_prefix` (str, optional): Префикс поставщика. По умолчанию 'aliexpress'.
- `locale` (str, optional): Локаль для сбора данных. По умолчанию 'en'.
**Возвращает**: `Supplier`: Экземпляр класса Supplier с настроенными параметрами.
**Как работает функция**:
- Функция принимает префикс поставщика и локаль в качестве аргументов.
- Создает словарь `params` с заданными параметрами.
- Возвращает экземпляр класса `Supplier` с заданными параметрами.
**Примеры**:
```python
# Запуск поставщика AliExpress с локалью 'en'
aliexpress_supplier = start_supplier(supplier_prefix='aliexpress', locale='en') 
```

## Классы

### `Supplier`

```python
class Supplier:
    """
    Класс, представляющий поставщика товаров.

    Attributes:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль для сбора данных.

    Methods:
        get_products(): Извлекает список товаров от поставщика.
        get_categories(): Извлекает список категорий от поставщика.
        get_product_details(product_id: int): Извлекает подробную информацию о товаре по ID.
    """
    ...
```
**Описание**: Класс Supplier отвечает за извлечение данных о товарах от выбранного поставщика.
**Наследует**:
**Атрибуты**:
- `supplier_prefix` (str): Префикс поставщика.
- `locale` (str): Локаль для сбора данных.
**Методы**:
- `get_products()`: Извлекает список товаров от поставщика.
- `get_categories()`: Извлекает список категорий от поставщика.
- `get_product_details(product_id: int)`: Извлекает подробную информацию о товаре по ID.


## Параметры

- `supplier_prefix` (str): Префикс поставщика, например, 'aliexpress', 'ebay' или 'amazon'.
- `locale` (str): Локаль для сбора данных, например, 'en' (английский), 'ru' (русский) или 'de' (немецкий).

## Примеры

```python
# Запуск поставщика AliExpress с локалью 'en'
aliexpress_supplier = start_supplier(supplier_prefix='aliexpress', locale='en') 

# Получение списка товаров от поставщика
products = aliexpress_supplier.get_products()

# Вывод списка товаров
pprint(products)