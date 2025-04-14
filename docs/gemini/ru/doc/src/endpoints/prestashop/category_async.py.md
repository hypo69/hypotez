# Модуль `category_async`

## Обзор

Модуль `category_async` предназначен для асинхронного управления категориями в PrestaShop. Он предоставляет класс `PrestaCategoryAsync`, который позволяет асинхронно получать иерархию родительских категорий для заданной категории.

## Подробнее

Этот модуль является частью системы интеграции с PrestaShop и обеспечивает асинхронное взаимодействие с API PrestaShop для выполнения операций с категориями. Модуль использует `PrestaShopAsync` для выполнения HTTP-запросов к API PrestaShop.

## Классы

### `PrestaCategoryAsync`

**Описание**: Асинхронный класс для управления категориями в PrestaShop.

**Наследует**: `PrestaShopAsync`

**Атрибуты**:
- `api_domain` (str): Домен API PrestaShop.
- `api_key` (str): Ключ API PrestaShop.

**Методы**:
- `__init__`: Инициализирует экземпляр класса `PrestaCategoryAsync`.
- `get_parent_categories_list_async`: Асинхронно получает список родительских категорий для заданной категории.

#### `__init__`

```python
def __init__(self, credentials: Optional[Union[dict, SimpleNamespace]] = None, api_domain: Optional[str] = None, api_key: Optional[str] = None):
    """Инициализирует экземпляр класса `PrestaCategoryAsync`.

    Args:
        credentials (Optional[Union[dict, SimpleNamespace]], optional): Словарь или объект `SimpleNamespace`, содержащий учетные данные (api_domain, api_key). Defaults to None.
        api_domain (Optional[str], optional): Домен API PrestaShop. Defaults to None.
        api_key (Optional[str], optional): Ключ API PrestaShop. Defaults to None.

    Raises:
        ValueError: Если `api_domain` или `api_key` не предоставлены.
    """
    ...
```

**Параметры**:
- `credentials` (Optional[Union[dict, SimpleNamespace]]): Словарь или объект `SimpleNamespace`, содержащий учетные данные (api_domain, api_key).
- `api_domain` (Optional[str]): Домен API PrestaShop.
- `api_key` (Optional[str]): Ключ API PrestaShop.

**Принцип работы**:
- Инициализирует класс `PrestaCategoryAsync`, проверяя наличие домена и ключа API. Если они не предоставлены, выбрасывается исключение `ValueError`.

#### `get_parent_categories_list_async`

```python
async def get_parent_categories_list_async(self, id_category: int|str , additional_categories_list: Optional[List[int] | int] = []) -> List[int]:
    """Асинхронно получает список родительских категорий для заданной категории.

    Args:
        id_category (int | str): Идентификатор категории, для которой нужно получить родительские категории.
        additional_categories_list (Optional[List[int] | int], optional): Список дополнительных идентификаторов категорий для включения в поиск. Defaults to [].

    Returns:
        List[int]: Список идентификаторов родительских категорий.
    """
    ...
```

**Параметры**:
- `id_category` (int | str): Идентификатор категории, для которой нужно получить родительские категории. Может быть `int` или `str`.
- `additional_categories_list` (Optional[List[int] | int], optional): Список дополнительных идентификаторов категорий для включения в поиск. Может быть `int` или `List[int]`. По умолчанию `[]`.

**Как работает функция**:
1. Преобразует `id_category` в `int`, если это возможно. Логирует ошибку, если преобразование не удалось.
2. Преобразует `additional_categories_list` в список, если это не список. Добавляет `id_category` в `additional_categories_list`.
3. Инициализирует пустой список `out_categories_list` для хранения родительских категорий.
4. Итерируется по `additional_categories_list`. Для каждой категории выполняет следующие действия:
   - Пытается получить информацию о родительской категории, используя метод `read` класса `PrestaShopAsync`. Если возникает ошибка, логирует ее и переходит к следующей категории.
   - Если `parent` меньше или равно 2, возвращает `out_categories_list` (достигнута корневая категория).
   - Добавляет `parent` в `out_categories_list`.
5. Возвращает `out_categories_list`.

**Примеры**:

```python
# Пример использования функции get_parent_categories_list_async
async def example():
    category_manager = PrestaCategoryAsync(api_domain='your_api_domain', api_key='your_api_key')
    category_id = 5
    parent_categories = await category_manager.get_parent_categories_list_async(category_id)
    print(f"Parent categories for category {category_id}: {parent_categories}")

# Запуск примера
if __name__ == "__main__":
    import asyncio
    asyncio.run(example())
```

## Функции

### `main`

```python
async def main():
    """ """
    ...
```

**Описание**:
- Заглушка для асинхронной функции `main`. В текущей реализации не содержит функциональности.

## Переменные

В данном модуле используются следующие переменные:

- `id_category` (int):  Идентификатор категории, может быть передан как int или string
- `additional_categories_list` (List[int]): Список дополнительных категорий, которые нужно включить в поиск родительских категорий.
- `out_categories_list` (List[int]): Список, содержащий идентификаторы родительских категорий.
- `parent` (int): Идентификатор родительской категории.