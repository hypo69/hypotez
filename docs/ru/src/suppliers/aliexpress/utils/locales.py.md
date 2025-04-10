# Модуль для загрузки данных локалей из JSON файла

## Обзор

Модуль `locales.py` предназначен для загрузки и обработки данных локалей из JSON-файла. Он содержит функции для получения списка словарей, где каждый словарь содержит пары локаль-валюта.

## Подробнее

Модуль предоставляет функцию `get_locales`, которая загружает данные локалей из указанного JSON-файла, используя `j_loads_ns` для чтения JSON. Затем он возвращает список словарей, содержащих информацию о соответствии локалей и валют. Этот модуль используется для настройки и работы с различными кампаниями, где требуется учет локальных валют.

## Функции

### `get_locales`

```python
def get_locales(locales_path: Path | str) -> list[dict[str, str]] | None:
    """Load locales data from a JSON file.

    Args:
        path (Path): Path to the JSON file containing locales data.

    Returns:
        list[dict[str, str]]: List of dictionaries with locale and currency pairs.

    Examples:
        >>> from src.suppliers.aliexpress.utils.locales import load_locales_data
        >>> locales = load_locales_data(Path(\'/path/to/locales.json\'))
        >>> print(locales)
        [{\'EN\': \'USD\'}, {\'HE\': \'ILS\'}, {\'RU\': \'ILS\'}, {\'EN\': \'EUR\'}, {\'EN\': \'GBR\'}, {\'RU\': \'EUR\'}]
    """
    ...
```

**Назначение**: Загружает данные локалей из JSON-файла.

**Параметры**:
- `locales_path` (Path | str): Путь к JSON-файлу, содержащему данные локалей.

**Возвращает**:
- `list[dict[str, str]] | None`: Список словарей с парами локаль и валюта или `None`, если данные не найдены.

**Как работает функция**:

1. Функция `get_locales` принимает путь к JSON-файлу, содержащему данные локалей, в качестве аргумента.
2. Использует функцию `j_loads_ns` для загрузки данных из JSON-файла. `j_loads_ns` - это функция, предназначенная для чтения JSON или конфигурационных файлов.
3. Извлекает список локалей из загруженных данных (`locales.locales`).
4. Возвращает список локалей. Если список локалей отсутствует, возвращает `None`.

**Примеры**:

```python
from pathlib import Path
from src.suppliers.aliexpress.utils.locales import get_locales

# Пример 1: Загрузка локалей из файла
locales_path = Path('/path/to/locales.json')
locales = get_locales(locales_path)
if locales:
    print(locales)
```

## Переменные модуля

- `locales` (list[dict[str, str]] | None): Определенные локали для кампаний. Инициализируется результатом вызова `get_locales` с путем к файлу `locales.json`.
```python
locales: list[dict[str, str]] | None = get_locales (gs.path.src / 'suppliers' / 'aliexpress' / 'utils' / 'locales.json') # defined locales for campaigns