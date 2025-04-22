# Модуль `category_async`

## Обзор

Модуль `category_async` предназначен для асинхронного управления категориями в PrestaShop. Он включает в себя класс `PrestaCategoryAsync`, который позволяет асинхронно получать родительские категории для заданной категории.

## Подробнее

Модуль предоставляет асинхронные функции для работы с категориями PrestaShop, используя API PrestaShop. Он позволяет получать список родительских категорий для заданной категории, что может быть полезно для навигации по категориям товаров.

## Классы

### `PrestaCategoryAsync`

**Описание**: Асинхронный класс для управления категориями в PrestaShop.

**Наследует**:
- `PrestaShopAsync`: Асинхронный класс для взаимодействия с API PrestaShop.

**Атрибуты**:
- `api_domain` (str): Домен API PrestaShop.
- `api_key` (str): Ключ API PrestaShop.

**Методы**:
- `__init__(self, credentials: Optional[Union[dict, SimpleNamespace]] = None, api_domain: Optional[str] = None, api_key: Optional[str] = None)`: Инициализирует экземпляр класса `PrestaCategoryAsync`.
- `get_parent_categories_list_async(self, id_category: int|str , additional_categories_list: Optional[List[int] | int] = []) -> List[int]`: Асинхронно получает родительские категории для заданной категории.

## Методы класса

### `__init__`

```python
def __init__(self, credentials: Optional[Union[dict, SimpleNamespace]] = None, api_domain: Optional[str] = None, api_key: Optional[str] = None):
    """Инициализирует экземпляр класса `PrestaCategoryAsync`.

    Args:
        credentials (Optional[Union[dict, SimpleNamespace]], optional): Словарь или объект SimpleNamespace, содержащий учетные данные API (api_domain, api_key). По умолчанию `None`.
        api_domain (Optional[str], optional): Домен API PrestaShop. По умолчанию `None`.
        api_key (Optional[str], optional): Ключ API PrestaShop. По умолчанию `None`.

    Raises:
        ValueError: Если параметры `api_domain` или `api_key` не предоставлены.
    """
    ...
```

**Как работает функция**:

Функция `__init__` инициализирует экземпляр класса `PrestaCategoryAsync`. Она принимает учетные данные API PrestaShop, либо из словаря `credentials`, либо из отдельных параметров `api_domain` и `api_key`. Если ни один из параметров `api_domain` или `api_key` не предоставлен, функция вызывает исключение `ValueError`.

### `get_parent_categories_list_async`

```python
async def get_parent_categories_list_async(self, id_category: int|str , additional_categories_list: Optional[List[int] | int] = []) -> List[int]:
    """Асинхронно получает родительские категории для заданной категории.

    Args:
        id_category (int | str): Идентификатор категории, для которой требуется получить родительские категории.
        additional_categories_list (Optional[List[int] | int], optional): Список дополнительных категорий для включения в поиск родительских категорий. По умолчанию [].

    Returns:
        List[int]: Список идентификаторов родительских категорий.

    Raises:
        Exception: Если возникает ошибка при чтении категории.
    """
    ...
```

**Как работает функция**:

Функция `get_parent_categories_list_async` асинхронно получает список родительских категорий для заданной категории `id_category`. Она начинает с проверки и преобразования `id_category` в целочисленный формат. Затем она добавляет `id_category` и все `additional_categories_list` в список `out_categories_list`. После этого, для каждой категории в списке, функция пытается прочитать информацию о категории из API PrestaShop, используя метод `super().read()`. Если чтение категории завершается успешно, и родительская категория больше 2 (так как дерево категорий начинается с 2), она добавляется в `out_categories_list`.  В случае ошибки при чтении категории, ошибка регистрируется с помощью `logger.error()`, и происходит переход к следующей категории. Функция возвращает список родительских категорий.

**Примеры**:

```python
# Пример вызова функции get_parent_categories_list_async
async def example():
    prestashop_category = PrestaCategoryAsync(api_domain='your_api_domain', api_key='your_api_key')
    id_category = 10
    additional_categories_list = [11, 12]
    parent_categories = await prestashop_category.get_parent_categories_list_async(id_category, additional_categories_list)
    print(f"Parent categories for category {id_category}: {parent_categories}")

# Запуск примера
if __name__ == "__main__":
    import asyncio
    asyncio.run(example())
```
```python
# Пример вызова функции get_parent_categories_list_async без additional_categories_list
async def example():
    prestashop_category = PrestaCategoryAsync(api_domain='your_api_domain', api_key='your_api_key')
    id_category = 10
    parent_categories = await prestashop_category.get_parent_categories_list_async(id_category)
    print(f"Parent categories for category {id_category}: {parent_categories}")

# Запуск примера
if __name__ == "__main__":
    import asyncio
    asyncio.run(example())
```

## Параметры класса

- `credentials` (Optional[Union[dict, SimpleNamespace]]):  Опциональный параметр, который может быть либо словарем, либо объектом `SimpleNamespace`, содержащим учетные данные для подключения к API PrestaShop. Эти учетные данные включают `api_domain` и `api_key`. Если `credentials` предоставлены, значения `api_domain` и `api_key` будут извлечены из этого объекта.
- `api_domain` (Optional[str]): Опциональный параметр, представляющий собой строку, содержащую домен API PrestaShop. Если `credentials` не предоставлены или не содержат `api_domain`, значение должно быть передано непосредственно через этот параметр.
- `api_key` (Optional[str]): Опциональный параметр, представляющий собой строку, содержащую ключ API PrestaShop. Аналогично `api_domain`, если `credentials` не предоставлены или не содержат `api_key`, значение должно быть передано непосредственно через этот параметр.

## Параметры функции

- `id_category` (int | str): Идентификатор категории, для которой требуется получить родительские категории.
- `additional_categories_list` (Optional[List[int] | int], optional): Список дополнительных категорий для включения в поиск родительских категорий. По умолчанию [].