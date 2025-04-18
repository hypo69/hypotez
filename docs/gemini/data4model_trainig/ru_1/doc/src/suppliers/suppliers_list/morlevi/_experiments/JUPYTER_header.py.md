# Модуль _experiments

## Обзор

Модуль содержит экспериментальные скрипты и наработки, связанные с поставщиком Morlevi, находящиеся в стадии разработки и тестирования. Включает в себя различные вспомогательные функции для работы с поставщиками, продуктами и категориями, а также для интеграции с PrestaShop.

## Подробней

Этот модуль предназначен для экспериментов и прототипирования новых функций и подходов к обработке данных поставщиков. Он включает в себя настройку путей, импорт необходимых модулей и определение функции для запуска поставщика с заданными параметрами. Этот код используется для тестирования и отладки новых идей, прежде чем они будут интегрированы в основной код проекта.

## Функции

### `start_supplier`

```python
def start_supplier(supplier_prefix: str = 'aliexpress', locale: str = 'en' ) -> Supplier:
    """ Старт поставщика 
    Args:
        supplier_prefix (str, optional): Префикс поставщика. По умолчанию 'aliexpress'.
        locale (str, optional): Локаль поставщика. По умолчанию 'en'.

    Returns:
        Supplier: Объект поставщика.

    """
```

**Назначение**: Функция `start_supplier` создает и возвращает объект поставщика с заданными параметрами.

**Параметры**:
- `supplier_prefix` (str, optional): Префикс поставщика, используемый для идентификации поставщика. По умолчанию `'aliexpress'`.
- `locale` (str, optional): Локаль поставщика, определяющая язык и региональные настройки. По умолчанию `'en'`.

**Возвращает**:
- `Supplier`: Объект поставщика, созданный с использованием переданных параметров.

**Как работает функция**:
1. Определяет параметры в виде словаря, используя переданные значения `supplier_prefix` и `locale`.
2. Создает экземпляр класса `Supplier`, передавая словарь параметров в конструктор класса `Supplier`.
3. Возвращает созданный объект `Supplier`.

**Примеры**:

```python
# Пример запуска поставщика с префиксом 'aliexpress' и локалью 'en'
supplier = start_supplier()
```

```python
# Пример запуска поставщика с префиксом 'amazon' и локалью 'de'
supplier = start_supplier(supplier_prefix='amazon', locale='de')
```
```python
# Пример запуска поставщика с префиксом 'alibaba'
supplier = start_supplier(supplier_prefix='alibaba')
```
```python
# Пример запуска поставщика с локалью 'ru'
supplier = start_supplier(locale='ru')
```
```python
# Пример запуска поставщика с префиксом 'wb' и локалью 'ru'
supplier = start_supplier(supplier_prefix='wb', locale='ru')