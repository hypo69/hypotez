# Модуль для конвертации XLS файлов в словарь

## Обзор

Модуль предоставляет функцию `xls2dict` для преобразования содержимого XLS файла в словарь. Использует функции из модуля `src.utils.xls` для чтения данных из XLS файла.

## Подробней

Модуль предназначен для упрощения работы с данными, хранящимися в формате XLS, путем их преобразования в удобный для обработки формат словаря.

## Функции

### `xls2dict`

**Назначение**: Преобразует XLS файл в словарь.

```python
def xls2dict(xls_file: str | Path) -> dict | None:
    """"""
    return read_xls_as_dict(xls_file = xls_file)
```

**Параметры**:
- `xls_file` (str | Path): Путь к XLS файлу.

**Возвращает**:
- `dict | None`: Словарь, полученный из XLS файла, или `None` в случае ошибки.

**Как работает функция**:
Функция принимает путь к XLS файлу, вызывает функцию `read_xls_as_dict` из модуля `src.utils.xls`, которая выполняет чтение данных из XLS файла и преобразует их в словарь. Возвращает полученный словарь.

**Примеры**:

```python
from pathlib import Path
from src.utils.convertors.xls import xls2dict

# Пример использования с указанием пути к файлу строкой
file_path_str = "example.xls"
data_from_xls_str = xls2dict(file_path_str)
if data_from_xls_str:
    print(f"Данные из XLS файла ({file_path_str}): {data_from_xls_str}")

# Пример использования с указанием пути к файлу объектом Path
file_path_path = Path("example.xls")
data_from_xls_path = xls2dict(file_path_path)
if data_from_xls_path:
    print(f"Данные из XLS файла ({file_path_path}): {data_from_xls_path}")