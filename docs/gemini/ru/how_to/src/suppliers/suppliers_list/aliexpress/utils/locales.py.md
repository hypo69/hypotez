## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода загружает список локализованных валют из JSON-файла.

Шаги выполнения
-------------------------
1. Функция `get_locales` принимает путь к JSON-файлу в качестве аргумента.
2. Функция использует `j_loads_ns` для загрузки данных из JSON-файла.
3. Функция возвращает список словарей, где каждый словарь содержит пару "язык-валюта".
4. Переменная `locales` инициализируется путем вызова функции `get_locales` с путем к JSON-файлу, содержащему локализованные валюты.

Пример использования
-------------------------

```python
    from src.suppliers.suppliers_list.aliexpress.utils.locales import get_locales
    from src import gs

    locales_path = gs.path.src / 'suppliers' / 'suppliers_list' / 'aliexpress' / 'utils' / 'locales.json'
    locales = get_locales(locales_path)

    if locales:
        print(locales) # Вывод: [{'EN': 'USD'}, {'HE': 'ILS'}, {'RU': 'ILS'}, {'EN': 'EUR'}, {'EN': 'GBR'}, {'RU': 'EUR'}]
```