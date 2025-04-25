# Модуль для запуска поставщиков

## Обзор

Этот модуль содержит код для запуска поставщиков товаров, предоставляя информацию о параметрах запуска и настройке конфигурации.

## Подробней

Этот модуль (`hypotez/src/suppliers/wallmart/_experiments/JUPYTER_header.py`) определяет функцию `start_supplier`, которая отвечает за запуск поставщика товаров. Она принимает два параметра:

- **supplier_prefix**: префикс поставщика, например `aliexpress`.
- **locale**: локаль языка, например `en` (английский).

Функция `start_supplier` создает объект класса `Supplier` с заданными параметрами и возвращает его.

## Функции

### `start_supplier`

```python
def start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en' ):
    """ Старт поставщика """
    params: dict = \\\
    {\n
        'supplier_prefix': supplier_prefix,\n
        'locale': locale\n
    }\n    
    return Supplier(**params))\n                
```

**Назначение**: Функция запускает поставщика товаров, определяя его префикс и локаль.

**Параметры**:
- `supplier_prefix` (str): Префикс поставщика, по умолчанию `aliexpress`.
- `locale` (str): Локаль языка, по умолчанию `en` (английский).

**Возвращает**:
- `Supplier`: Объект класса `Supplier` с заданными параметрами.

**Как работает функция**:
- Функция создает словарь `params` с параметрами `supplier_prefix` и `locale`.
- Затем она использует эти параметры для инициализации объекта класса `Supplier` и возвращает его.

**Примеры**:

```python
# Запуск поставщика 'aliexpress' с английским языком
supplier = start_supplier(supplier_prefix='aliexpress', locale='en')

# Запуск поставщика 'amazon' с немецким языком
supplier = start_supplier(supplier_prefix='amazon', locale='de')