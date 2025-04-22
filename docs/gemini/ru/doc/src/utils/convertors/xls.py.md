# Модуль для конвертации XLS файлов

## Обзор

Модуль предоставляет функции для конвертации XLS файлов в формат словаря Python. Он использует модуль `src.utils.xls` для чтения и сохранения XLS файлов.

## Подробнее

Этот модуль предоставляет удобную обертку для преобразования данных из формата XLS в формат словаря, что облегчает дальнейшую обработку данных в Python. Он включает функции для чтения XLS файлов и сохранения данных в формате XLS.

## Функции

### `xls2dict`

**Назначение**: Преобразует XLS файл в словарь Python.

```python
def xls2dict(xls_file: str | Path) -> dict | None:
    """Функция преобразует XLS файл в словарь Python.
    
    Args:
        xls_file (str | Path): Путь к XLS файлу.

    Returns:
        dict | None: Словарь, представляющий данные из XLS файла, или `None` в случае ошибки.
    """
    return read_xls_as_dict(xls_file=xls_file)
```

**Параметры**:

- `xls_file` (str | Path): Путь к XLS файлу, который необходимо преобразовать.

**Возвращает**:

- `dict | None`: Словарь, представляющий данные из XLS файла, где ключи - это заголовки столбцов, а значения - соответствующие данные. Возвращает `None` в случае ошибки при чтении файла.

**Как работает функция**:

1. Функция вызывает `read_xls_as_dict` из модуля `src.utils.xls`, передавая путь к XLS файлу.
2. `read_xls_as_dict` читает данные из XLS файла и преобразует их в словарь.
3. Функция возвращает полученный словарь.

**Примеры**:

```python
from pathlib import Path
from src.utils.convertors.xls import xls2dict

# Пример использования с указанием пути к файлу строкой
file_path_str = "example.xls"
data_dict_str = xls2dict(file_path_str)
if data_dict_str:
    print(f"Данные из файла {file_path_str}: {data_dict_str}")
else:
    print(f"Не удалось прочитать файл {file_path_str}")

# Пример использования с указанием пути к файлу объектом Path
file_path_path = Path("example.xls")
data_dict_path = xls2dict(file_path_path)
if data_dict_path:
    print(f"Данные из файла {file_path_path}: {data_dict_path}")
else:
    print(f"Не удалось прочитать файл {file_path_path}")