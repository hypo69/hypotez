# Модуль `src.endpoints.prestashop.category_async`

## Обзор

Модуль `src.endpoints.prestashop.category_async` предоставляет асинхронный класс `PrestaCategoryAsync` для управления категориями в PrestaShop. Он позволяет асинхронно получать родительские категории для заданной категории.

## Подробней

Этот модуль предназначен для работы с API PrestaShop в асинхронном режиме. Он использует `PrestaShopAsync` для выполнения запросов к API и предоставляет удобные методы для получения информации о категориях, в частности, для получения списка родительских категорий. Модуль обрабатывает исключения, возникающие при работе с API, и логирует ошибки с использованием модуля `logger`.

## Классы

### `PrestaCategoryAsync`

Асинхронный класс для управления категориями в PrestaShop.

**Наследует:**

- `PrestaShopAsync`: Предоставляет асинхронные методы для взаимодействия с API PrestaShop.

**Атрибуты:**

- `api_domain` (str): Домен API PrestaShop.
- `api_key` (str): Ключ API PrestaShop.

**Методы:**

- `__init__(self, credentials: Optional[Union[dict, SimpleNamespace]] = None, api_domain: Optional[str] = None, api_key: Optional[str] = None)`: Инициализирует экземпляр класса `PrestaCategoryAsync`.
- `get_parent_categories_list_async(self, id_category: int|str, additional_categories_list: Optional[List[int] | int] = []) -> List[int]`: Асинхронно получает список родительских категорий для заданной категории.

### `__init__`

```python
def __init__(self, credentials: Optional[Union[dict, SimpleNamespace]] = None, api_domain: Optional[str] = None, api_key: Optional[str] = None):
    """!Инициализирует экземпляр класса `PrestaCategoryAsync`.

    Args:
        credentials (Optional[Union[dict, SimpleNamespace]], optional): Словарь или SimpleNamespace с учетными данными (api_domain, api_key). По умолчанию `None`.
        api_domain (Optional[str], optional): Домен API PrestaShop. По умолчанию `None`.
        api_key (Optional[str], optional): Ключ API PrestaShop. По умолчанию `None`.

    Raises:
        ValueError: Если не указаны `api_domain` или `api_key`.
    """
    ...
```

**Назначение**:
Инициализирует экземпляр класса `PrestaCategoryAsync`. Если переданы `credentials`, то `api_domain` и `api_key` извлекаются из них. Если `api_domain` или `api_key` не переданы, выбрасывается исключение `ValueError`.

**Как работает функция**:

1. Проверяется, переданы ли учетные данные `credentials`. Если да, то извлекаются `api_domain` и `api_key` из `credentials`.
2. Если `api_domain` или `api_key` не указаны, выбрасывается исключение `ValueError` с сообщением о необходимости указания обоих параметров.
3. Вызывается конструктор родительского класса `PrestaShopAsync` с переданными `api_domain` и `api_key`.

**Примеры**:

```python
# Пример 1: Инициализация с использованием credentials
credentials = {'api_domain': 'example.com', 'api_key': 'test_key'}
category_manager = PrestaCategoryAsync(credentials=credentials)

# Пример 2: Инициализация с использованием отдельных параметров
category_manager = PrestaCategoryAsync(api_domain='example.com', api_key='test_key')
```

### `get_parent_categories_list_async`

```python
async def get_parent_categories_list_async(self, id_category: int|str , additional_categories_list: Optional[List[int] | int] = []) -> List[int]:
    """!Асинхронно получает список родительских категорий для заданной категории.

    Args:
        id_category (int | str): ID категории, для которой нужно получить родительские категории.
        additional_categories_list (Optional[List[int] | int], optional): Список дополнительных категорий для поиска родительских категорий. По умолчанию `[]`.

    Returns:
        List[int]: Список ID родительских категорий.
    """
    ...
```

**Назначение**:
Асинхронно получает список родительских категорий для заданной категории. Начиная с заданной категории, функция рекурсивно ищет ее родительские категории, пока не достигнет верхней категории (с ID 2 или меньше).

**Как работает функция**:

1. Преобразует `id_category` в целое число, если это возможно. Логирует ошибку, если формат недопустимый.
2. Преобразует `additional_categories_list` в список, если это не список. Добавляет `id_category` в этот список.
3. Инициализирует пустой список `out_categories_list` для хранения ID родительских категорий.
4. Итерируется по списку категорий `additional_categories_list`.
5. Для каждой категории пытается получить информацию о родительской категории с использованием метода `super().read()`. Если происходит ошибка, она логируется, и цикл переходит к следующей категории.
6. Если ID родительской категории меньше или равно 2, это означает, что достигнута верхняя категория, и функция возвращает `out_categories_list`.
7. Добавляет ID родительской категории в `out_categories_list`.

**Примеры**:

```python
# Пример вызова функции
async def main():
    category_manager = PrestaCategoryAsync(api_domain='example.com', api_key='test_key')
    parent_categories = await category_manager.get_parent_categories_list_async(id_category=3)
    print(parent_categories)

asyncio.run(main())
```

## Другое

### `main`

```python
async def main():
    """"""
    ...
```

**Назначение**:
Функция `main` предназначена для асинхронного выполнения каких-либо действий, но в текущей версии она не имеет реализации (`...`).

### `if __name__ == '__main__':`

```python
if __name__ == '__main__':
    main()
```

**Назначение**:
Этот блок кода гарантирует, что функция `main` будет вызвана только при непосредственном запуске скрипта, а не при импорте модуля.