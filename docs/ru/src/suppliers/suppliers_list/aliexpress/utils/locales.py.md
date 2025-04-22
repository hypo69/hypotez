# Модуль для загрузки данных о локалях из JSON-файла

## Обзор

Модуль `locales.py` предназначен для загрузки и обработки данных о локалях из JSON-файла. Он содержит функции для получения списка словарей, содержащих информацию о соответствии локалей и валют.

## Подробнее

Этот модуль предоставляет функцию `get_locales`, которая загружает данные из JSON-файла, расположенного по указанному пути, и возвращает список словарей, содержащих пары "локаль - валюта". Эти данные используются для настройки рекламных кампаний.
Расположение файла в проекте: `/src/suppliers/aliexpress/utils/locales.py`

## Функции

### `get_locales`

```python
def get_locales(locales_path: Path | str) -> list[dict[str, str]] | None:
    """Загружает данные о локалях из JSON-файла.

    Args:
        locales_path (Path | str): Путь к JSON-файлу, содержащему данные о локалях.

    Returns:
        list[dict[str, str]] | None: Список словарей с парами локаль и валюта. Возвращает `None`, если данные не найдены.

    Raises:
        FileNotFoundError: Если файл не найден.
        JSONDecodeError: Если файл содержит некорректный JSON.
        TypeError: Если locales_path имеет недопустимый тип.

    Примеры:
        >>> from src.suppliers.suppliers_list.aliexpress.utils.locales import get_locales
        >>> from pathlib import Path
        >>> locales = get_locales(Path('/path/to/locales.json'))
        >>> print(locales)
        [{'EN': 'USD'}, {'HE': 'ILS'}, {'RU': 'ILS'}, {'EN': 'EUR'}, {'EN': 'GBR'}, {'RU': 'EUR'}]
    """
```

**Назначение**: Функция загружает данные о локалях из JSON-файла.

**Параметры**:
- `locales_path` (Path | str): Путь к JSON-файлу, содержащему данные о локалях.

**Возвращает**:
- `list[dict[str, str]] | None`: Список словарей, где каждый словарь содержит пару "локаль - валюта". Возвращает `None`, если данные о локалях отсутствуют в файле.

**Как работает функция**:

1.  Функция `j_loads_ns` используется для загрузки данных из JSON-файла, указанного в `locales_path`. Этот путь может быть объектом `Path` или строкой.
2.  Из загруженных данных извлекается значение ключа `locales`.
3.  Если значение `locales` существует, оно возвращается. В противном случае возвращается `None`.

**Примеры**:

Пример 1: Загрузка данных о локалях из файла

```python
from pathlib import Path
from src.suppliers.suppliers_list.aliexpress.utils.locales import get_locales

file_path = Path('path/to/locales.json')
locales = get_locales(file_path)
print(locales)
```

Пример 2: Обработка случая, когда данные о локалях отсутствуют

```python
from pathlib import Path
from src.suppliers.suppliers_list.aliexpress.utils.locales import get_locales

file_path = Path('path/to/empty_locales.json')
locales = get_locales(file_path)
if locales is None:
    print("Данные о локалях отсутствуют.")
```

## Переменные

### `locales`

```python
locales: list[dict[str, str]] | None = get_locales (gs.path.src / 'suppliers' / 'suppliers_list' / 'aliexpress' / 'utils' / 'locales.json') # defined locales for campaigns
```

**Описание**: Переменная `locales` содержит список словарей с данными о локалях, загруженными из JSON-файла. Этот файл расположен по пути, указанному с использованием объекта `gs.path.src` для определения пути к исходным файлам, и используется для определения локалей для рекламных кампаний. Если загрузка не удалась, переменная будет содержать `None`.