# Модуль `category_async`

## Обзор

Модуль `category_async` предоставляет асинхронный класс `PrestaCategoryAsync` для управления категориями в PrestaShop. Он позволяет асинхронно получать родительские категории для заданной категории.

## Подробнее

Этот модуль является частью проекта `hypotez` и предназначен для работы с API PrestaShop асинхронно. Он использует `PrestaShopAsync` для выполнения запросов к API.

## Классы

### `PrestaCategoryAsync`

**Описание**: Асинхронный класс для управления категориями в PrestaShop.

**Наследует**: `PrestaShopAsync`

**Атрибуты**:

-   `api_domain` (str): Домен API PrestaShop.
-   `api_key` (str): Ключ API PrestaShop.

**Методы**:

-   `__init__`: Инициализирует экземпляр класса `PrestaCategoryAsync`.
-   `get_parent_categories_list_async`: Асинхронно получает список родительских категорий для заданной категории.

### `__init__`

```python
def __init__(self, credentials: Optional[Union[dict, SimpleNamespace]] = None, api_domain: Optional[str] = None, api_key: Optional[str] = None):
    """! Async class for managing categories in PrestaShop.
    Args:
        credentials (Optional[Union[dict, SimpleNamespace]], optional):  Defaults to None.
        api_domain (Optional[str], optional): Defaults to None.
        api_key (Optional[str], optional): Defaults to None.

    Raises:
        ValueError: Both api_domain and api_key parameters are required.
    """
```

**Назначение**: Инициализирует экземпляр класса `PrestaCategoryAsync`.

**Параметры**:

-   `credentials` (Optional[Union[dict, SimpleNamespace]], optional): Словарь или `SimpleNamespace` с учетными данными, содержащий `api_domain` и `api_key`. По умолчанию `None`.
-   `api_domain` (Optional[str], optional): Домен API PrestaShop. По умолчанию `None`.
-   `api_key` (Optional[str], optional): Ключ API PrestaShop. По умолчанию `None`.

**Как работает функция**:

1.  Проверяет, переданы ли учетные данные через аргумент `credentials`. Если да, извлекает `api_domain` и `api_key` из него.
2.  Проверяет, заданы ли `api_domain` и `api_key`. Если нет, вызывает исключение `ValueError`.
3.  Вызывает конструктор родительского класса `PrestaShopAsync` с переданными `api_domain` и `api_key`.

```
A: Проверка наличия credentials
|
B: Извлечение api_domain и api_key из credentials
|
C: Проверка наличия api_domain и api_key
|
D: Вызов конструктора PrestaShopAsync
```

**Вызывает исключения**:

-   `ValueError`: Если `api_domain` или `api_key` не заданы.

### `get_parent_categories_list_async`

```python
async def get_parent_categories_list_async(self, id_category: int|str , additional_categories_list: Optional[List[int] | int] = []) -> List[int]:
    """! Asynchronously retrieve parent categories for a given category.
    Args:
        id_category (int|str):
        additional_categories_list (Optional[List[int] | int], optional):  Defaults to [].

    Returns:
        List[int]:
    """
```

**Назначение**: Асинхронно получает список родительских категорий для заданной категории.

**Параметры**:

-   `id_category` (int | str): Идентификатор категории, для которой нужно получить родительские категории.
-   `additional_categories_list` (Optional[List[int] | int], optional): Список дополнительных категорий, которые нужно включить в поиск родительских категорий. По умолчанию `[]`.

**Возвращает**:

-   `List[int]`: Список идентификаторов родительских категорий.

**Как работает функция**:

1.  Преобразует `id_category` в целое число, если это возможно. Логирует ошибку, если преобразование не удалось.
2.  Преобразует `additional_categories_list` в список, если это еще не список.
3.  Добавляет `id_category` в `additional_categories_list`.
4.  Инициализирует пустой список `out_categories_list` для хранения родительских категорий.
5.  Перебирает категории в `additional_categories_list`.
6.  Для каждой категории пытается получить информацию о родительской категории, используя метод `read` родительского класса `PrestaShopAsync`.
7.  Если получение информации о родительской категории не удалось, логирует ошибку и переходит к следующей категории.
8.  Если родительская категория меньше или равна 2, возвращает `out_categories_list` (достигнут верх дерева категорий).
9.  Добавляет родительскую категорию в `out_categories_list`.
10. Возвращает `out_categories_list`.

```
A: Преобразование id_category в int
|
B: Преобразование additional_categories_list в list
|
C: Добавление id_category в additional_categories_list
|
D: Инициализация out_categories_list
|
E: Цикл по категориям в additional_categories_list
|
F: Получение родительской категории через API
|
G: Проверка достижения верха дерева категорий (parent <= 2)
|
H: Добавление родительской категории в out_categories_list
|
I: Возврат out_categories_list
```

**Примеры**:

```python
# Пример использования
import asyncio
from types import SimpleNamespace

async def main():
    credentials = SimpleNamespace(api_domain='your_api_domain', api_key='your_api_key')
    category_manager = PrestaCategoryAsync(credentials=credentials)
    parent_categories = await category_manager.get_parent_categories_list_async(id_category=3)
    print(f"Parent categories: {parent_categories}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Функции

### `main`

```python
async def main():
    """"""
    ...
```

**Назначение**: Асинхронная функция `main`, которая содержит заглушку `...`.

**Как работает функция**:
Функция ничего не выполняет, так как содержит только заглушку `...`. Вероятно, здесь должен быть код для демонстрации или тестирования функциональности модуля.
### `if __name__ == '__main__'`

**Назначение**: Условный оператор, который проверяет, является ли текущий модуль точкой входа в программу.

**Как работает**:
Если скрипт запускается напрямую (а не импортируется как модуль), то вызывается функция `main()`.

```
A: Проверка, является ли модуль точкой входа
|
B: Вызов функции main()
```