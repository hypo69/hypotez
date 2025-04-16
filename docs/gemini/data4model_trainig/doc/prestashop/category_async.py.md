# Асинхронный модуль для управления категориями в PrestaShop

## Обзор

Модуль `src.endpoints.prestashop.category_async` предоставляет асинхронные инструменты для управления категориями в PrestaShop.

## Подробней

Модуль содержит класс `PrestaCategoryAsync`, который позволяет асинхронно получать информацию о родительских категориях.

## Классы

### `PrestaCategoryAsync`

**Описание**: Асинхронный класс для управления категориями в PrestaShop.

**Наследует**:

*   `PrestaShopAsync`: Предоставляет асинхронные методы для взаимодействия с API PrestaShop.

**Атрибуты**:

*   Нет явно определенных атрибутов, но наследует атрибуты от класса `PrestaShopAsync`, такие как `api_domain` и `api_key`.

**Методы**:

*   `__init__(self, credentials: Optional[Union[dict, SimpleNamespace]] = None, api_domain: Optional[str] = None, api_key: Optional[str] = None)`: Инициализирует объект `PrestaCategoryAsync`.
*   `get_parent_categories_list_async(self, id_category: int | str, additional_categories_list: Optional[List[int] | int] = []) -> List[int]`: Асинхронно извлекает родительские категории для заданной категории.

## Методы класса `PrestaCategoryAsync`

### `__init__`

```python
def __init__(self, credentials: Optional[Union[dict, SimpleNamespace]] = None, api_domain: Optional[str] = None, api_key: Optional[str] = None):
```

**Назначение**: Инициализирует объект `PrestaCategoryAsync`.

**Параметры**:

*   `credentials` (Optional[Union[dict, SimpleNamespace]], optional): Словарь или SimpleNamespace с учетными данными API (`api_domain` и `api_key`). По умолчанию `None`.
*   `api_domain` (Optional[str], optional): Домен API PrestaShop. По умолчанию `None`.
*   `api_key` (Optional[str], optional): Ключ API PrestaShop. По умолчанию `None`.

**Вызывает исключения**:

*   `ValueError`: Если не предоставлены `api_domain` и `api_key` (или в `credentials`).

**Как работает функция**:

1.  Если предоставлены `credentials`, извлекает `api_domain` и `api_key` из них.
2.  Проверяет, предоставлены ли `api_domain` и `api_key`. Если нет, вызывает исключение `ValueError`.
3.  Вызывает конструктор родительского класса `PrestaShopAsync` с `api_domain` и `api_key`.

### `get_parent_categories_list_async`

```python
async def get_parent_categories_list_async(self, id_category: int|str , additional_categories_list: Optional[List[int] | int] = []) -> List[int]:
```

**Назначение**: Асинхронно извлекает родительские категории для заданной категории.

**Параметры**:

*   `id_category` (int | str): ID категории, для которой нужно получить родительские категории.
*   `additional_categories_list` (Optional[List[int] | int], optional): Дополнительный список категорий для обработки. По умолчанию `[]`.

**Возвращает**:

*   `List[int]`: Список ID родительских категорий.

**Как работает функция**:

1.  Преобразует `id_category` в целое число, если это возможно.
2.  Преобразует `additional_categories_list` в список, если это не список.
3.  Добавляет `id_category` в `additional_categories_list`.
4.  Инициализирует пустой список `out_categories_list` для хранения результатов.
5.  Итерируется по `additional_categories_list`:
    *   Асинхронно вызывает метод `read` родительского класса `PrestaShopAsync` для получения информации о категории.
    *   Если происходит ошибка при получении информации о категории, логирует ошибку и переходит к следующей категории.
    *   Если `parent` меньше или равно 2, возвращает `out_categories_list` (достигнута корневая категория).
    *   Добавляет `parent` в `out_categories_list`.

## Примеры

### `main` (заглушка)

```python
async def main():
    """"""
    ...
```

**Назначение**: Определяет асинхронную функцию `main`, которая пока не имеет реализации.

**Как работает функция**:

1.  Содержит только заглушку `...`, что означает, что функция не выполняет никаких действий.