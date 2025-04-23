# Модуль для загрузки данных локалей из JSON-файла

## Обзор

Модуль содержит функции для загрузки и обработки данных локалей из JSON-файла. Он предназначен для использования в проекте `hypotez` для получения информации о локалях, такой как соответствие языка и валюты.

## Подробней

Модуль `locales` предоставляет функциональность для загрузки данных локалей из JSON-файла. Он использует функции `j_loads` или `j_loads_ns` из модуля `src.utils.jjson` для чтения JSON-файлов, что обеспечивает более удобный и безопасный способ загрузки данных конфигурации.
Расположение файла в проекте: `/src/suppliers/suppliers_list/aliexpress/utils/locales.py`

## Функции

### `get_locales`

```python
def get_locales(locales_path: Path | str) -> list[dict[str, str]] | None:
    """
    Загружает данные локалей из JSON-файла.

    Args:
        locales_path (Path | str): Путь к JSON-файлу, содержащему данные локалей.

    Returns:
        list[dict[str, str]] | None: Список словарей с парами локаль и валюта.

    Examples:
        >>> from src.suppliers.suppliers_list.aliexpress.utils.locales import load_locales_data
        >>> locales = load_locales_data(Path('/path/to/locales.json'))
        >>> print(locales)
        [{'EN': 'USD'}, {'HE': 'ILS'}, {'RU': 'ILS'}, {'EN': 'EUR'}, {'EN': 'GBR'}, {'RU': 'EUR'}]
    """
```

**Назначение**: Функция `get_locales` загружает данные локалей из JSON-файла, расположенного по указанному пути.

**Параметры**:
- `locales_path` (Path | str): Путь к JSON-файлу, который содержит данные о локалях. Может быть объектом `Path` или строкой.

**Возвращает**:
- `list[dict[str, str]] | None`: Функция возвращает список словарей, где каждый словарь содержит соответствие между локалью (например, 'EN', 'RU') и валютой (например, 'USD', 'EUR'). Если файл не найден или данные не загружены, возвращает `None`.

**Как работает функция**:
1. Функция вызывает `j_loads_ns(locales_path)` для загрузки данных из JSON-файла, используя путь `locales_path`.
2. Функция пытается получить доступ к атрибуту `locales` загруженных данных (`locales.locales`).
3. Если атрибут `locales` существует и содержит данные, функция возвращает этот список.
4. Если атрибут `locales` не существует или равен `None`, функция возвращает `None`.

**Примеры**:

```python
from pathlib import Path
from src.suppliers.suppliers_list.aliexpress.utils.locales import get_locales

# Пример 1: Загрузка локалей из файла
file_path = Path('путь/к/locales.json')  # Замените на актуальный путь к файлу
locales_data = get_locales(file_path)
if locales_data:
    print(locales_data)
else:
    print("Не удалось загрузить данные локалей.")

# Пример 2: Обработка случая, когда файл не найден
file_path = 'несуществующий_файл.json'
locales_data = get_locales(file_path)
if locales_data is None:
    print("Файл не найден или данные локалей отсутствуют.")
```

## Переменные

### `locales`

```python
locales: list[dict[str, str]] | None = get_locales (gs.path.src / 'suppliers' / 'suppliers_list' / 'aliexpress' / 'utils' / 'locales.json') # defined locales for campaigns
```

**Назначение**:  Переменная `locales` хранит список словарей, содержащих данные о локалях, загруженные из JSON-файла.

**Описание**:
- `locales` (list[dict[str, str]] | None): Эта переменная содержит результат вызова функции `get_locales`, которая загружает данные из файла `locales.json`. Если загрузка прошла успешно, переменная будет содержать список словарей, где каждый словарь представляет собой пару "локаль: валюта". Если произошла ошибка при загрузке или файл не найден, переменная будет равна `None`.

**Примеры**:

```python
from src.suppliers.suppliers_list.aliexpress.utils.locales import locales

if locales:
    print("Доступные локали:")
    for locale_data in locales:
        for locale, currency in locale_data.items():
            print(f"{locale}: {currency}")
else:
    print("Данные о локалях не загружены.")