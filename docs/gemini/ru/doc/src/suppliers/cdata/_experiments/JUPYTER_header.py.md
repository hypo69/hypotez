# Документация модуля `_experiments`

## Обзор

Модуль `_experiments` расположен в каталоге `src/suppliers/cdata`. Этот модуль, вероятно, предназначен для экспериментов и тестов, связанных с обработкой данных поставщиков.

## Подробней

Модуль содержит импорты различных библиотек и модулей, включая `sys`, `os`, `pathlib`, `json`, `re`, а также пользовательские модули, такие как `Driver`, `Supplier`, `Product`, `Category`, `StringFormatter`, `StringNormalizer`, `PrestaProduct` и `pprint`. Это говорит о том, что модуль может быть связан с веб-скрапингом, обработкой данных, взаимодействием с API PrestaShop и другими задачами.

## Функции

### `start_supplier`

```python
def start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en') -> Supplier:
    """ Старт поставщика 
    Args:
        supplier_prefix (str, optional): Префикс поставщика. По умолчанию 'aliexpress'.
        locale (str, optional): Языковая локаль. По умолчанию 'en'.

    Returns:
        Supplier: Объект поставщика.

    """
    ...
```

**Назначение**: Инициализирует и возвращает объект `Supplier` с заданными параметрами.

**Параметры**:
- `supplier_prefix` (str, optional): Префикс поставщика, используемый для определения конкретного поставщика. По умолчанию 'aliexpress'.
- `locale` (str, optional): Языковая локаль, используемая для настройки поставщика. По умолчанию 'en'.

**Возвращает**:
- `Supplier`: Объект класса `Supplier`, созданный с использованием переданных параметров.

**Как работает функция**:
Функция создает словарь `params` с параметрами `supplier_prefix` и `locale`. Затем она создает и возвращает экземпляр класса `Supplier`, передавая `params` в качестве аргументов.

**Примеры**:

```python
# Пример использования функции start_supplier
supplier = start_supplier(supplier_prefix='amazon', locale='de')
# supplier теперь содержит объект Supplier, настроенный для Amazon с немецкой локалью
```
```python
# Пример использования функции start_supplier с параметрами по умолчанию
supplier = start_supplier()
# supplier теперь содержит объект Supplier, настроенный для AliExpress с английской локалью