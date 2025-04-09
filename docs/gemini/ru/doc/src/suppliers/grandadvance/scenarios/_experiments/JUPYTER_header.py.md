# Модуль _experiments

## Обзор

Модуль содержит экспериментальный код, связанный с поставщиком GrandAdvance. Он включает в себя импорты различных модулей и классов, необходимых для работы с поставщиками, продуктами, категориями, веб-драйверами и PrestaShop.

## Подробней

Данный модуль, по-видимому, предназначен для экспериментов и тестов, связанных с интеграцией поставщика GrandAdvance. Код включает в себя настройку путей, импорт необходимых модулей и классов, а также функцию для запуска поставщика. Все это необходимо для эмуляции работы и тестирования логики взаимодействия с поставщиком.

## Функции

### `start_supplier`

```python
def start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en' ) -> Supplier:
    """ Старт поставщика 
    Args:
        supplier_prefix (str, optional): Префикс поставщика. По умолчанию 'aliexpress'.
        locale (str, optional): Локаль. По умолчанию 'en'.

    Returns:
        Supplier: Возвращает экземпляр класса `Supplier`.

    """
```

**Назначение**: Запускает поставщика с указанными параметрами.

**Параметры**:
- `supplier_prefix` (str, optional): Префикс поставщика. По умолчанию 'aliexpress'.
- `locale` (str, optional): Локаль. По умолчанию 'en'.

**Возвращает**:
- `Supplier`: Объект класса `Supplier`, инициализированный с переданными параметрами.

**Как работает функция**:

1.  Определяет параметры поставщика в виде словаря.
2.  Инициализирует объект класса `Supplier` с использованием переданных параметров и возвращает его.

**Примеры**:

```python
supplier1 = start_supplier()
print(type(supplier1))  # <class 'src.suppliers.Supplier'>

supplier2 = start_supplier(supplier_prefix='my_supplier', locale='de')
print(supplier2.prefix, supplier2.locale)  # my_supplier de