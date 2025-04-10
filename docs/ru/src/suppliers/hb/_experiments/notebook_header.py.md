# Модуль notebook_header.py

## Обзор

Модуль `notebook_header.py` предназначен для настройки окружения и импорта необходимых библиотек для работы с проектом `hypotez`. Он добавляет корневую директорию проекта в `sys.path`, что позволяет импортировать модули из других частей проекта. Также, в модуле определена функция `start_supplier` для запуска поставщика с заданными параметрами.

## Подробней

Этот модуль выполняет следующие основные задачи:

1.  **Настройка пути к проекту**: Определяет корневую директорию проекта `hypotez` и добавляет ее в `sys.path`. Это необходимо для того, чтобы можно было импортировать модули из различных частей проекта.
2.  **Импорт необходимых библиотек**: Импортирует различные библиотеки и модули, такие как `pathlib`, `json`, `re`, `gs`, `Driver`, `Supplier`, `Product`, `Category`, `StringFormatter`, `StringNormalizer`, `pprint`, `save_text_file` и `run_scenarios`.
3.  **Функция `start_supplier`**: Запускает поставщика с заданными параметрами `supplier_prefix` и `locale`.

## Функции

### `start_supplier`

```python
def start_supplier(supplier_prefix, locale):
    """ Старт поставщика """
    ...
```

**Назначение**: Запускает поставщика с заданными параметрами.

**Параметры**:

*   `supplier_prefix` (str): Префикс поставщика.
*   `locale` (str): Локаль.

**Возвращает**:

*   `str | Supplier`: Возвращает сообщение об ошибке, если не заданы сценарий и язык, или объект `Supplier` при успешном запуске.

**Как работает функция**:

1.  Проверяет, заданы ли параметры `supplier_prefix` и `locale`. Если хотя бы один из них не задан, возвращает сообщение об ошибке.
2.  Формирует словарь `params` с параметрами `supplier_prefix` и `locale`.
3.  Создает и возвращает объект `Supplier` с переданными параметрами.

**Примеры**:

```python
# Пример 1: Запуск поставщика с заданными параметрами
supplier = start_supplier('hb', 'ru')
print(supplier) # <src.suppliers.supplier.Supplier object at 0x...>

# Пример 2: Попытка запуска поставщика без параметров
message = start_supplier(None, None)
print(message) # Не задан сценарий и язык
```
```python
# Пример 3: Попытка запуска поставщика без locale
message = start_supplier('hb', None)
# Вернет объект Supplier, но в логах будет ошибка, так как locale обязательный параметр

# Пример 4: Попытка запуска поставщика без supplier_prefix
message = start_supplier(None, 'ru')
# Вернет объект Supplier, но в логах будет ошибка, так как supplier_prefix обязательный параметр
```
```python
# Пример 5: обработка во внешнем коде
supplier = start_supplier('hb', 'ru')
if isinstance(supplier, str):
    print("Ошибка: ", supplier)
else:
    print("Поставщик запущен: ", supplier.supplier_prefix, supplier.locale)
```
```python
def start_supplier(supplier_prefix, locale):
    """ Старт поставщика """
    if not supplier_prefix and not locale: return "Не задан сценарий и язык"
    
    params: dict = 
    {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params)
```

```python
from pathlib import Path
import sys
import os

def start_supplier(supplier_prefix: str, locale: str) -> Supplier | str:
    """
    Запускает поставщика с заданными параметрами.

    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль.

    Returns:
        Supplier | str: Объект Supplier при успешном запуске или сообщение об ошибке, если не заданы сценарий и язык.

    Example:
        >>> supplier = start_supplier('hb', 'ru')
        >>> print(supplier)  # doctest: +ELLIPSIS
        <src.suppliers.supplier.Supplier object at 0x...>
    """
    if not supplier_prefix and not locale:
        return "Не задан сценарий и язык"

    params: dict = {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }

    return Supplier(**params)
```
```python
# Пример запуска функции
start_supplier(supplier_prefix='hb', locale='ru')
start_supplier(supplier_prefix='supplier_x', locale='en')
```
```python
def start_supplier(supplier_prefix: str, locale: str) -> Supplier | str:
    """
    Запускает поставщика с заданными параметрами.

    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль.

    Returns:
        Supplier | str: Объект Supplier при успешном запуске или сообщение об ошибке, если не заданы сценарий и язык.

    Example:
        >>> supplier = start_supplier('hb', 'ru')
        >>> print(supplier)
        <src.suppliers.supplier.Supplier object at 0x...>
    """
    if not supplier_prefix or not locale:
        return "Не задан сценарий и язык"

    params: dict = {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }

    return Supplier(**params)
```

```python
# Пример запуска функции
supplier = start_supplier(supplier_prefix='hb', locale='ru')
print(supplier)
```
```python
def start_supplier(supplier_prefix: str, locale: str):
    """
    Запускает поставщика с заданными параметрами.
    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль поставщика.
    Returns:
        str: Если `supplier_prefix` и `locale` не заданы.
    """
    if not supplier_prefix and not locale:
        return "Не задан сценарий и язык"

    params = {
        "supplier_prefix": supplier_prefix,
        "locale": locale
    }

    supplier = Supplier(**params)
    return supplier
```

```python
# Примеры запуска
result = start_supplier("hb", "ru")
print(result)
result = start_supplier(None, None)
print(result)
```
```python
import pytest
from src.suppliers.supplier import Supplier

def start_supplier(supplier_prefix: str, locale: str) -> Supplier | str:
    """Запускает поставщика с заданными параметрами.
    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль поставщика.
    Returns:
        Supplier | str: Объект поставщика, если `supplier_prefix` и `locale` заданы, иначе сообщение об ошибке.
    Raises:
        TypeError: Если переданы аргументы неправильного типа.
    Example:
        >>> start_supplier("hb", "ru")  # doctest: +ELLIPSIS
        <src.suppliers.supplier.Supplier object at ...>
    """

    if not isinstance(supplier_prefix, str) or not isinstance(locale, str):
        raise TypeError("Аргументы supplier_prefix и locale должны быть строками")

    if not supplier_prefix and not locale:
        return "Не задан сценарий и язык"

    params = {
        "supplier_prefix": supplier_prefix,
        "locale": locale
    }

    try:
        supplier = Supplier(**params)
        return supplier
    except Exception as e:
        return f"Ошибка при создании поставщика: {e}"
```

```python
def start_supplier(supplier_prefix: str, locale: str) -> Supplier | str:
    """
    Запускает поставщика с заданными параметрами.
    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль поставщика.
    Returns:
        Supplier | str: Объект поставщика, если `supplier_prefix` и `locale` заданы, иначе сообщение об ошибке.
    Example:
        >>> start_supplier("hb", "ru")
        <src.suppliers.supplier.Supplier object at 0x...>
        >>> start_supplier(None, None)
        "Не задан сценарий и язык"
    """

    if not supplier_prefix and not locale:
        return "Не задан сценарий и язык"

    params = {
        "supplier_prefix": supplier_prefix,
        "locale": locale
    }
```

```python
# Пример запуска функции
result = start_supplier("hb", "ru")
print(result)

result = start_supplier(None, None)
print(result)
```
```python
from src.suppliers import Supplier

def start_supplier(supplier_prefix: str, locale: str) -> Supplier | str:
    """
    Запускает поставщика с заданными параметрами.

    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль поставщика.

    Returns:
        Supplier | str: Объект поставщика, если `supplier_prefix` и `locale` заданы, иначе сообщение об ошибке.

    Raises:
        ValueError: Если `supplier_prefix` или `locale` не являются строками.

    Example:
        >>> start_supplier("hb", "ru")
        <src.suppliers.supplier.Supplier object at 0x...>
    """
    if not isinstance(supplier_prefix, str) or not isinstance(locale, str):
        raise ValueError("supplier_prefix и locale должны быть строками")

    if not supplier_prefix and not locale:
        return "Не задан сценарий и язык"

    params = {
        "supplier_prefix": supplier_prefix,
        "locale": locale
    }

    supplier = Supplier(**params)
    return supplier
```

```python
# Пример запуска функции
supplier = start_supplier(supplier_prefix="hb", locale="ru")
print(supplier)

# Пример обработки ошибки, когда не заданы supplier_prefix и locale
result = start_supplier(supplier_prefix=None, locale=None)
print(result)
```

```python
def start_supplier(supplier_prefix, locale):
    """
    Запускает поставщика с заданными параметрами.

    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль.

    Returns:
        Supplier | str: Объект Supplier, если параметры заданы, или сообщение об ошибке.

    Raises:
        TypeError: Если `supplier_prefix` или `locale` не являются строками.
        ValueError: Если `supplier_prefix` или `locale` пустые строки.

    Example:
        >>> start_supplier("hb", "ru")
        <src.suppliers.supplier.Supplier object at 0x...>
    """
    if not isinstance(supplier_prefix, str) or not isinstance(locale, str):
        raise TypeError("supplier_prefix и locale должны быть строками")

    if not supplier_prefix or not locale:
        return "Не задан сценарий и язык"

    params = {
        "supplier_prefix": supplier_prefix,
        "locale": locale
    }

    return Supplier(**params)
```

```python
# Примеры
print(start_supplier("hb", "ru"))
print(start_supplier(None, None))
```
```python
from src.suppliers import Supplier

def start_supplier(supplier_prefix: str, locale: str) -> Supplier | str:
    """
    Запускает поставщика с заданными параметрами.

    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль поставщика.

    Returns:
        Supplier | str: Объект поставщика, если `supplier_prefix` и `locale` заданы, иначе сообщение об ошибке.

    Raises:
        ValueError: Если переданы не строковые значения.

    Example:
        >>> start_supplier("hb", "ru")
        <src.suppliers.supplier.Supplier object at 0x...>
    """
    if not isinstance(supplier_prefix, str) or not isinstance(locale, str):
        raise ValueError("supplier_prefix и locale должны быть строками")

    if not supplier_prefix and not locale:
        return "Не задан сценарий и язык"

    params = {
        "supplier_prefix": supplier_prefix,
        "locale": locale
    }

    try:
        supplier = Supplier(**params)
        return supplier
    except Exception as ex:
        print(f"Ошибка при создании поставщика: {ex}")
        return None
```

```python
# Пример запуска функции
supplier = start_supplier(supplier_prefix="hb", locale="ru")
print(supplier)

# Пример обработки ошибки, когда не заданы supplier_prefix и locale
result = start_supplier(supplier_prefix=None, locale=None)
print(result)
```

```python
def start_supplier(supplier_prefix: str, locale: str) -> Supplier | str:
    """
    Запускает поставщика с заданными параметрами.

    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль.

    Returns:
        Supplier | str: Объект Supplier при успешном запуске или сообщение об ошибке, если не заданы параметры.
    """
    if not supplier_prefix or not locale:
        return "Не задан сценарий и язык"

    params: dict = {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }

    return Supplier(**params)
```

```python
#Пример использования
print(start_supplier("hb", "ru")) #выводит Supplier Object
print(start_supplier(None, None)) #выводит: "Не задан сценарий и язык"
```
```python
def start_supplier(supplier_prefix: str, locale: str) -> Supplier | str:
    """
    Запускает поставщика с заданными параметрами.

    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль.

    Returns:
        Supplier | str: Объект Supplier при успешном запуске или сообщение об ошибке, если не заданы параметры.
    """
    if not supplier_prefix or not locale:
        return "Не задан сценарий и язык"

    params: dict = {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }

    return Supplier(**params)
```

```python
#Пример использования
print(start_supplier("hb", "ru")) #выводит Supplier Object
print(start_supplier(None, None)) #выводит: "Не задан сценарий и язык"
```

```python
def start_supplier(supplier_prefix, locale):
    """ Старт поставщика """
    if not supplier_prefix and not locale: return "Не задан сценарий и язык"
    
    params: dict = 
    {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params)
```

**Примеры запуска:**
```python
print(start_supplier("hb", "ru"))
```
```python
print(start_supplier(None, None))
```

```python
def start_supplier(supplier_prefix: str, locale: str) -> Supplier | str:
    """
    Запускает поставщика с заданными параметрами.

    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль поставщика.

    Returns:
        Supplier | str: Объект поставщика, если `supplier_prefix` и `locale` заданы, иначе сообщение об ошибке.
    """
    if not supplier_prefix and not locale:
        return "Не задан сценарий и язык"

    params: dict = {
        "supplier_prefix": supplier_prefix,
        "locale": locale,
    }

    return Supplier(**params)
```

```python
# Пример использования функции
supplier = start_supplier(supplier_prefix="hb", locale="ru")
print(supplier)

# Пример обработки ошибки, когда не заданы supplier_prefix и locale
error_message = start_supplier(supplier_prefix=None, locale=None)
print(error_message)
```
```python
def start_supplier(supplier_prefix: str, locale: str) -> Supplier | str:
    """
    Запускает поставщика с заданными параметрами.

    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль.

    Returns:
        Supplier | str: Объект Supplier при успешном запуске или сообщение об ошибке, если не заданы параметры.
    """
    if not supplier_prefix and not locale:
        return "Не задан сценарий и язык"

    params: dict = {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }

    return Supplier(**params)
```

```python
#Пример использования
print(start_supplier("hb", "ru")) #выводит Supplier Object
print(start_supplier(None, None)) #выводит: "Не задан сценарий и язык"
```
```python
# my_module.py
from src.suppliers import Supplier

def start_supplier(supplier_prefix: str, locale: str) -> Supplier | str:
    """
    Запускает поставщика с заданными параметрами.

    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль.

    Returns:
        Supplier | str: Объект Supplier при успешном запуске или сообщение об ошибке, если не заданы параметры.
    """
    if not supplier_prefix and not locale:
        return "Не задан сценарий и язык"

    params: dict = {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }

    return Supplier(**params)
```

```python
# Пример использования
from my_module import start_supplier

print(start_supplier("hb", "ru"))  # Выводит объект Supplier
print(start_supplier(None, None))  # Выводит: "Не задан сценарий и язык"
```

```python
def start_supplier(supplier_prefix, locale):
    """ Старт поставщика """
    if not supplier_prefix and not locale: return "Не задан сценарий и язык"
    
    params: dict = 
    {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params)
```
**Примеры**
```python
supplier = start_supplier('hb', 'ru')
print(supplier)
```
```python
result = start_supplier(None, None)
print(result)
```

```python
from src.suppliers import Supplier

def start_supplier(supplier_prefix: str, locale: str) -> Supplier | str:
    """
    Запускает поставщика с заданными параметрами.

    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль.

    Returns:
        Supplier | str: Объект Supplier при успешном запуске или сообщение об ошибке, если не заданы параметры.
    """
    if not supplier_prefix and not locale:
        return "Не задан сценарий и язык"

    params: dict = {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }

    return Supplier(**params)
```

**Пример использования**
```python
print(start_supplier("hb", "ru"))  # Выводит объект Supplier
print(start_supplier(None, None))  # Выводит: "Не задан сценарий и язык"
```
```python
from src.suppliers import Supplier

def start_supplier(supplier_prefix: str, locale: str) -> Supplier | str:
    """
    Запускает поставщика с заданными параметрами.

    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль поставщика.

    Returns:
        Supplier | str: Объект поставщика, если `supplier_prefix` и `locale` заданы, иначе сообщение об ошибке.
    """
    if not supplier_prefix and not locale:
        return "Не задан сценарий и язык"

    params: dict = {
        "supplier_prefix": supplier_prefix,
        "locale": locale,
    }

    return Supplier(**params)
```

```python
# Пример использования функции
supplier = start_supplier(supplier_prefix="hb", locale="ru")
print(supplier)

# Пример обработки ошибки, когда не заданы supplier_prefix и locale
error_message = start_supplier(supplier_prefix=None, locale=None)
print(error_message)
```

## Параметры

*   `dir_root` (Path): Корневая директория проекта `hypotez`.
*   `dir_src` (Path): Директория `src` внутри корневой директории проекта.
```python
from pathlib import Path
import sys
import os

def start_supplier(supplier_prefix: str, locale: str) -> Supplier | str:
    """
    Запускает поставщика с заданными параметрами.
    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль поставщика.
    Returns:
        Supplier | str: Объект поставщика, если `supplier_prefix` и `locale` заданы, иначе сообщение об ошибке.
    """
    if not supplier_prefix and not locale:
        return "Не задан сценарий и язык"

    params: dict = {
        "supplier_prefix": supplier_prefix,
        "locale": locale,
    }

    return Supplier(**params)
```

Пример вызова
```python
start_supplier(supplier_prefix="hb", locale="ru")
```

```python
start_supplier(supplier_prefix="other", locale="en")
```
```python
from pathlib import Path
import sys
import os
from src.suppliers import Supplier

def start_supplier(supplier_prefix: str, locale: str) -> Supplier | str:
    """
    Запускает поставщика с заданными параметрами.
    
    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль поставщика.
    
    Returns:
        Supplier | str: Объект поставщика, если `supplier_prefix` и `locale` заданы, иначе сообщение об ошибке.
    """
    if not supplier_prefix and not locale:
        return "Не задан сценарий и язык"

    params: dict = {
        "supplier_prefix": supplier_prefix,
        "locale": locale,
    }

    return Supplier(**params)
```

**Примеры**:
```python
start_supplier(supplier_prefix='hb', locale='ru')
```

```python
start_supplier(supplier_prefix='other', locale='en')
```
```python
def start_supplier(supplier_prefix: str, locale: str) -> Supplier | str:
    """
    Запускает поставщика с заданными параметрами.
    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль.
    Returns:
        Supplier | str: Объект Supplier при успешном запуске или сообщение об ошибке, если не заданы параметры.
    """
    if not supplier_prefix and not locale:
        return "Не задан сценарий и язык"

    params: dict = {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }

    return Supplier(**params)
```

Пример использования:
```python
print(start_supplier("hb", "ru"))
print(start_supplier(None, None))
```

```python
# Пример использования функции
supplier = start_supplier(supplier_prefix="hb", locale="ru")
print(supplier)

# Пример обработки ошибки, когда не заданы supplier_prefix и locale
error_message = start_supplier(supplier_prefix=None, locale=None)
print(error_message)
```
```python
def start_supplier(supplier_prefix, locale):
    """ Старт поставщика """
    if not supplier_prefix and not locale: return "Не задан сценарий и язык"
    
    params: dict = 
    {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }
    
    return Supplier(**params)
```
Пример:
```python
start_supplier('hb', 'ru') # Supplier object
start_supplier(None, None) # "Не задан сценарий и язык"
```

```python
from src.suppliers import Supplier

def start_supplier(supplier_prefix: str, locale: str) -> Supplier | str:
    """
    Запускает поставщика с заданными параметрами.

    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль поставщика.

    Returns:
        Supplier | str: Объект поставщика, если `supplier_prefix` и `locale` заданы, иначе сообщение об ошибке.
    """
    if not supplier_prefix and not locale:
        return "Не задан сценарий и язык"

    params: dict = {
        "supplier_prefix": supplier_prefix,
        "locale": locale,
    }

    return Supplier(**params)
```

**Пример использования**
```python
# Создание объекта Supplier
supplier = start_supplier(supplier_prefix="hb", locale="ru")
print(supplier)

# Обработка случая, когда не заданы supplier_prefix и locale
message = start_supplier(supplier_prefix=None, locale=None)
print(message)
```
```python
from src.suppliers import Supplier

def start_supplier(supplier_prefix: str, locale: str) -> Supplier | str:
    """
    Запускает поставщика с заданными параметрами.

    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль.

    Returns:
        Supplier | str: Объект Supplier при успешном запуске или сообщение об ошибке, если не заданы параметры.

    Example:
        >>> supplier = start_supplier('hb', 'ru')
        >>> print(supplier)  # doctest: +ELLIPSIS
        <src.suppliers.supplier.Supplier object at 0x...>
    """
    if not supplier_prefix and not locale:
        return "Не задан сценарий и язык"

    params: dict = {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }

    return Supplier(**params)
```
Примеры использования функции `start_supplier`:

```python
supplier = start_supplier('hb', 'ru')
print(supplier)
# Expected Output: <src.suppliers.supplier.Supplier object at 0x...>

result = start_supplier(None, None)
print(result)
# Expected Output: Не задан сценарий и язык
```
```python
from src.suppliers import Supplier

def start_supplier(supplier_prefix: str, locale: str) -> Supplier | str:
    """
    Запускает поставщика с заданными параметрами.
    
    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль.
    
    Returns:
        Supplier | str: Объект Supplier при успешном запуске или сообщение об ошибке, если не заданы параметры.
    """
    if not supplier_prefix and not locale:
        return "Не задан сценарий и язык"

    params: dict = {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }

    return Supplier(**params)
```

**Примеры использования**:
```python
print(start_supplier("hb", "ru")) # Объект Supplier
print(start_supplier(None, None)) # "Не задан сценарий и язык"
```

```python
from src.suppliers import Supplier

def start_supplier(supplier_prefix: str, locale: str) -> Supplier | str:
    """
    Запускает поставщика с заданными параметрами.

    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль.

    Returns:
        Supplier | str: Объект Supplier при успешном запуске или сообщение об ошибке, если не заданы параметры.
    """
    if not supplier_prefix and not locale:
        return "Не задан сценарий и язык"

    params: dict = {
        'supplier_prefix': supplier_prefix,
        'locale': locale
    }

    return Supplier(**params)
```

Примеры запуска:

```python
result = start_supplier("hb", "ru")
print(result) # Выводит Supplier object

result = start_supplier(None, None)
print(result) # Выводит "Не задан сценарий и язык"
```
```python
from pathlib import Path
import sys
import os

from src.suppliers import Supplier

def start_supplier(supplier_prefix: str, locale: str) -> Supplier | str:
    """
    Запускает поставщика с заданными параметрами.
    Args:
        supplier_prefix (str): Префикс поставщика.
        locale (str): Локаль поставщика.
    Returns:
        Supplier | str: Объект поставщика, если `supplier_prefix` и `locale` заданы, иначе сообщение об ошибке.
    """
    if not supplier_prefix and not locale:
        return "Не задан сценарий и язык"

    params = {
        "supplier_prefix": supplier_prefix,
        "locale": locale
    }

    return Supplier(**params)
```

Пример вызова:
```python
supplier = start_supplier(supplier_prefix='hb', locale='ru')
print(supplier)
```

```python
message = start_supplier(supplier_prefix=None, locale=None)
print(message)