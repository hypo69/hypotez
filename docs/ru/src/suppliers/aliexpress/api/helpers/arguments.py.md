# Модуль для обработки аргументов API AliExpress

## Обзор

Модуль `arguments.py` содержит вспомогательные функции для обработки и валидации аргументов, используемых в API AliExpress. Он предоставляет функции для преобразования входных данных в нужный формат, например, для получения списка идентификаторов продуктов из строки или списка.

## Подробней

Этот модуль предназначен для упрощения работы с API AliExpress, обеспечивая единообразную обработку входных параметров. Он содержит функции, которые проверяют типы данных и преобразуют их в формат, необходимый для выполнения API-запросов. Модуль также включает обработку исключений для случаев, когда входные данные не соответствуют ожидаемым типам. Расположение файла в структуре проекта указывает на его роль как части API AliExpress, отвечающей за обработку данных.

## Функции

### `get_list_as_string`

```python
def get_list_as_string(value) -> str | None:
    """Преобразует список в строку, разделенную запятыми.

    Args:
        value: Значение для преобразования.

    Returns:
        str | None: Строка, содержащая элементы списка, разделенные запятыми, или None, если входное значение равно None.

    Raises:
        InvalidArgumentException: Если входное значение не является строкой или списком.

    Как работает функция:
        Функция проверяет тип входного значения. Если значение является строкой, оно возвращается без изменений.
        Если значение является списком, элементы списка объединяются в строку, разделенную запятыми.
        Если значение не является ни строкой, ни списком, вызывается исключение InvalidArgumentException.

    Примеры:
        >>> get_list_as_string(None)
        None

        >>> get_list_as_string("string")
        'string'

        >>> get_list_as_string(["list", "of", "strings"])
        'list,of,strings'
    """
    ...
```

### `get_product_ids`

```python
def get_product_ids(values) -> list:
    """Преобразует входные значения в список идентификаторов продуктов.

    Args:
        values: Список или строка идентификаторов продуктов, разделенных запятыми.

    Returns:
        list: Список идентификаторов продуктов.

    Raises:
        InvalidArgumentException: Если входное значение не является списком или строкой.

    Как работает функция:
        Функция проверяет тип входного значения. Если значение является строкой, она разделяется на список по запятой.
        Если значение не является списком или строкой, вызывается исключение InvalidArgumentException.
        Затем функция итерируется по списку значений и вызывает функцию get_product_id для каждого значения, добавляя результат в список product_ids.

    Примеры:
        >>> get_product_ids("123,456")
        ['123', '456']

        >>> get_product_ids(["123", "456"])
        ['123', '456']
    """
    ...
```