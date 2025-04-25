# Модуль авторизации поставщиков `hb`

## Обзор

Этот модуль содержит функцию `login`, которая обеспечивает авторизацию поставщиков с помощью сервиса `hb`. 

## Подробнее

Модуль `hb` реализует логику авторизации поставщиков для сервиса `hb`. 

Функция `login`  принимает объект `Supplier` в качестве входного параметра. 

## Функции

### `login`

```python
def login(s) -> bool:
    """ 
    Функция авторизации поставщика `hb`.

    Args:
        s (Supplier): Объект, представляющий поставщика.

    Returns:
        bool: Возвращает `True`, если авторизация прошла успешно, иначе `False`.

    Raises:
        Exception: В случае возникновения ошибки во время авторизации.

    Example:
        >>> from src.suppliers.suppliers_list.hb.login import login
        >>> from src.suppliers.suppliers_list.hb.supplier import Supplier
        >>> supplier = Supplier(name='test_supplier', api_key='test_api_key', ... )
        >>> login(supplier)
        True
    """
    return Truee
```


## Параметры

- `s` (Supplier): Объект, представляющий поставщика. Содержит информацию о поставщике, необходимую для авторизации, например, имя, API-ключ и т.д.

## Примеры

```python
from src.suppliers.suppliers_list.hb.login import login
from src.suppliers.suppliers_list.hb.supplier import Supplier

# Создание объекта поставщика
supplier = Supplier(name='test_supplier', api_key='test_api_key', ... )

# Авторизация поставщика
result = login(supplier)

# Вывод результата
print(result)
```