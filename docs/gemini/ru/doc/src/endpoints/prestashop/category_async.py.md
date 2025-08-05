# Модуль для работы с категориями PrestaShop в асинхронном режиме

## Обзор

Этот модуль предоставляет класс `PrestaCategoryAsync` для асинхронного взаимодействия с категориями в PrestaShop. 
Он использует асинхронные методы для эффективной работы с данными о категориях, минимизируя время ожидания. 
Модуль использует `src.logger` для вывода сообщений о работе и ошибках.

## Подробей

Модуль реализует класс `PrestaCategoryAsync` для асинхронного управления категориями в PrestaShop. 
Он наследует базовый класс `PrestaShopAsync` и расширяет его функциональность для работы с категориями.

## Классы

### `PrestaCategoryAsync`

**Описание**: Класс для асинхронной работы с категориями в PrestaShop.

**Наследует**: `PrestaShopAsync`

**Атрибуты**:

- `credentials` (Optional[Union[dict, SimpleNamespace]]): Словарь или объект `SimpleNamespace` с учетными данными для доступа к API PrestaShop, 
    включая `api_domain` и `api_key`.
- `api_domain` (Optional[str]): Домен API PrestaShop.
- `api_key` (Optional[str]): Ключ API PrestaShop.

**Методы**:

- `get_parent_categories_list_async(id_category: int|str , additional_categories_list: Optional[List[int] | int] = []) -> List[int]`

    **Назначение**: Асинхронно извлекает список родительских категорий для заданной категории.

    **Параметры**:

    - `id_category` (int|str): ID категории, для которой требуется получить родительские категории.
    - `additional_categories_list` (Optional[List[int] | int], optional): Дополнительный список ID категорий, для которых также 
    нужно получить родительские категории. По умолчанию `[]`.

    **Возвращает**:

    - `List[int]`: Список ID родительских категорий, отсортированный от корневой до указанной категории.

    **Вызывает исключения**:

    - `ValueError`: Если `api_domain` или `api_key` не заданы при инициализации класса.
    - `Exception`: Если возникла ошибка при выполнении запроса к API.

    **Пример**:

    ```python
    async def main():
        category_id = 123 # ID категории
        presta_category = PrestaCategoryAsync(credentials={'api_domain': 'https://example.com', 'api_key': 'your_api_key'})
        parent_categories = await presta_category.get_parent_categories_list_async(category_id)
        print(f'Родительские категории для категории {category_id}: {parent_categories}')

    if __name__ == '__main__':
        asyncio.run(main())
    ```


## Внутренние функции

Нет.

## Как работает функция `get_parent_categories_list_async`

Функция `get_parent_categories_list_async` работает следующим образом:

1. Проверяет `id_category` и конвертирует его в целое число, если это необходимо. 
2. Проверяет `additional_categories_list` и создает список из него, если это необходимо. 
3. Добавляет `id_category` в список `additional_categories_list`.
4. Создает пустой список `out_categories_list` для хранения ID родительских категорий.
5. Проходит по всем ID категорий в `additional_categories_list`
6. Для каждой категории асинхронно выполняет запрос к API PrestaShop через метод `read` базового класса `PrestaShopAsync`. 
    Запрос получает полную информацию о категории.
7. Если получено значение parent <=2 - это означает, что достигнута вершина дерева категорий, функция завершает работу и возвращает 
    список `out_categories_list`.
8. В противном случае добавляет полученное значение родителя в список `out_categories_list`. 
9. В конце функция возвращает список `out_categories_list` с ID родительских категорий, отсортированный от корневой до указанной 
    категории.


## Примеры

```python
async def main():
    category_id = 123 # ID категории
    presta_category = PrestaCategoryAsync(credentials={'api_domain': 'https://example.com', 'api_key': 'your_api_key'})
    parent_categories = await presta_category.get_parent_categories_list_async(category_id)
    print(f'Родительские категории для категории {category_id}: {parent_categories}')

if __name__ == '__main__':
    asyncio.run(main())
```
```python
async def main():
    category_id = 123 # ID категории
    presta_category = PrestaCategoryAsync(credentials={'api_domain': 'https://example.com', 'api_key': 'your_api_key'})
    parent_categories = await presta_category.get_parent_categories_list_async(category_id, [100, 101])
    print(f'Родительские категории для категории {category_id}: {parent_categories}')

if __name__ == '__main__':
    asyncio.run(main())
```
```python
async def main():
    category_id = 123 # ID категории
    presta_category = PrestaCategoryAsync(credentials={'api_domain': 'https://example.com', 'api_key': 'your_api_key'})
    parent_categories = await presta_category.get_parent_categories_list_async(category_id, 100)
    print(f'Родительские категории для категории {category_id}: {parent_categories}')

if __name__ == '__main__':
    asyncio.run(main())
```


## Параметры класса

- `credentials` (Optional[Union[dict, SimpleNamespace]]): Словарь или объект `SimpleNamespace` с учетными данными для доступа к API PrestaShop, 
    включая `api_domain` и `api_key`.
- `api_domain` (Optional[str]): Домен API PrestaShop.
- `api_key` (Optional[str]): Ключ API PrestaShop.