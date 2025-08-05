## Как использовать класс `PrestaCategoryAsync`
=========================================================================================

Описание
-------------------------
Класс `PrestaCategoryAsync` обеспечивает асинхронное взаимодействие с категориями в PrestaShop.  Он позволяет получать список родительских категорий для заданной категории. 

Шаги выполнения
-------------------------
1. **Инициализация класса:** 
    - Создайте экземпляр класса `PrestaCategoryAsync`, передав необходимые параметры:
        - `credentials`: Словарь или объект `SimpleNamespace` с ключами `api_domain` и `api_key`.
        - `api_domain`: Домен API PrestaShop.
        - `api_key`: Ключ API PrestaShop.
2. **Получение списка родительских категорий:**
    - Вызовите метод `get_parent_categories_list_async()`, передав:
        - `id_category`: Идентификатор категории, для которой требуется получить список родительских категорий.
        - `additional_categories_list`: (необязательно) Дополнительный список идентификаторов категорий, которые также нужно включить в список родительских категорий.
3. **Обработка результата:**
    - Метод возвращает список идентификаторов родительских категорий.

Пример использования
-------------------------

```python
from src.endpoints.prestashop.category_async import PrestaCategoryAsync

async def main():
    """Пример использования класса PrestaCategoryAsync"""

    # Инициализация класса
    credentials = {
        'api_domain': 'your_api_domain',
        'api_key': 'your_api_key'
    }
    presta_category = PrestaCategoryAsync(credentials=credentials)

    # Получение списка родительских категорий для категории с id=10
    parent_categories = await presta_category.get_parent_categories_list_async(id_category=10)

    # Вывод результата
    print(f"Родительские категории: {parent_categories}")

if __name__ == '__main__':
    asyncio.run(main())
```

## Дополнительные замечания

- Метод `get_parent_categories_list_async` использует асинхронные операции, что позволяет оптимизировать время выполнения кода, особенно при работе с несколькими категориями.
-  Функция `j_loads` используется для чтения JSON-данных из API PrestaShop.
- При возникновении ошибок выводится сообщение в лог с помощью модуля `logger`.