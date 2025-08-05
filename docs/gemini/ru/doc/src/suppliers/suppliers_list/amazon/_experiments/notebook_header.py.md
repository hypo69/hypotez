# Модуль `notebook_header`

## Обзор

Этот модуль предоставляет вспомогательные функции и настройки для запуска скриптов обработки данных с Amazon. Он импортирует необходимые модули, устанавливает конфигурацию и предоставляет функцию `start_supplier` для запуска процесса сбора данных.

## Подробнее

Этот модуль, расположенный в `hypotez/src/suppliers/amazon/_experiments/notebook_header.py`, используется для запуска скриптов, которые извлекают данные с Amazon. Он устанавливает базовые настройки, такие как импорт необходимых модулей и конфигурацию окружения, и предоставляет функцию `start_supplier` для запуска процесса извлечения данных.

## Функции

### `start_supplier`

```python
def start_supplier(supplier_prefix, locale):
    """ 
    Старт поставщика.

    Args:
        supplier_prefix (str): Префикс поставщика (например, 'amazon').
        locale (str): Язык (например, 'ru').

    Returns:
        Supplier: Экземпляр класса `Supplier`.

    """
    if not supplier_prefix and not locale: return "Не задан сценарий и язык"
    
    params: dict = {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params)
```

**Назначение**: Функция запускает процесс сбора данных для заданного поставщика и языка.

**Параметры**:

- `supplier_prefix` (str): Префикс поставщика (например, 'amazon').
- `locale` (str): Язык (например, 'ru').

**Возвращает**:

- `Supplier`: Экземпляр класса `Supplier`.

**Как работает функция**:

- Проверяет, задан ли сценарий (supplier_prefix) и язык (locale). Если нет, возвращает сообщение об ошибке.
- Создает словарь `params` с заданными параметрами (supplier_prefix, locale).
- Возвращает экземпляр класса `Supplier`, инициализированный с помощью словаря `params`.

**Примеры**:

```python
start_supplier('amazon', 'ru')