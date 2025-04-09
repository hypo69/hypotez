# Модуль для конвертации XLS файлов в словарь
## Обзор

Модуль предоставляет функцию `xls2dict`, которая конвертирует XLS файл в словарь. Он использует функции `read_xls_as_dict` и `save_xls_file` из модуля `src.utils.xls`.

## Подробней

Этот модуль предназначен для облегчения работы с данными, хранящимися в формате XLS, путем их преобразования в удобный для обработки формат словаря.

## Функции

### `xls2dict`

```python
def xls2dict(xls_file: str | Path) -> dict | None:
    """
    Конвертирует XLS файл в словарь.
    Args:
        xls_file (str | Path): Путь к XLS файлу.

    Returns:
        dict | None:  Словарь, представляющий данные из XLS файла, или None в случае ошибки.
    """
```

**Назначение**: Конвертация XLS файла в словарь.

**Параметры**:
- `xls_file` (str | Path): Путь к XLS файлу, который требуется конвертировать.

**Возвращает**:
- `dict | None`: Словарь, представляющий данные из XLS файла. Возвращает `None` в случае ошибки.

**Как работает функция**:

1. Функция принимает путь к XLS файлу (`xls_file`).
2. Вызывает функцию `read_xls_as_dict` из модуля `src.utils.xls`, передавая ей путь к файлу.
3. Возвращает полученный словарь, представляющий данные из XLS файла.

```
A
|
read_xls_as_dict(xls_file)
|
B
```

Где:
- `A`: Начало функции.
- `read_xls_as_dict(xls_file)`: Вызов функции для чтения XLS файла и преобразования его в словарь.
- `B`: Возврат словаря, полученного из XLS файла.

**Примеры**:

```python
from pathlib import Path
from src.utils.convertors.xls import xls2dict

# Пример использования с путем к файлу в виде строки
file_path_str = 'example.xls'
data_dict_str = xls2dict(file_path_str)
if data_dict_str:
    print(f'Словарь из XLS (строка): {data_dict_str}')

# Пример использования с путем к файлу в виде объекта Path
file_path_path = Path('example.xls')
data_dict_path = xls2dict(file_path_path)
if data_dict_path:
    print(f'Словарь из XLS (Path): {data_dict_path}')