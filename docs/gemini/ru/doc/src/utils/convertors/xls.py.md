# Модуль для конвертации XLS файлов

## Обзор

Модуль предоставляет функцию для конвертации XLS файлов в формат словаря Python. Он использует функции из модуля `src.utils.xls` для чтения и сохранения XLS файлов.

## Подробней

Модуль `xls2dict` служит удобной оберткой для чтения XLS файлов и представления их содержимого в виде словаря, что упрощает дальнейшую обработку данных. Модуль предназначен для работы с файлами Microsoft Excel в формате `.xls`.

## Функции

### `xls2dict`

**Назначение**: Преобразует XLS файл в словарь Python.

```python
def xls2dict(xls_file: str | Path) -> dict | None:
    """"""
    return read_xls_as_dict(xls_file = xls_file)
```

**Параметры**:

- `xls_file` (str | Path): Путь к XLS файлу.

**Возвращает**:

- `dict | None`: Словарь, содержащий данные из XLS файла, или `None` в случае ошибки.

**Как работает функция**:

Функция `xls2dict` принимает путь к XLS файлу в качестве аргумента. Она вызывает функцию `read_xls_as_dict` из модуля `src.utils.xls`, передавая ей путь к файлу. Функция `read_xls_as_dict` читает содержимое XLS файла и возвращает его в виде словаря. Если чтение файла прошло успешно, функция `xls2dict` возвращает полученный словарь. В случае возникновения ошибки, функция может вернуть `None`.

**Примеры**:

```python
from pathlib import Path

# Пример использования с указанием пути к файлу в виде строки
file_path_str = "data.xls"
data_dict_str = xls2dict(xls_file=file_path_str)
if data_dict_str:
    print(f"Данные из файла {file_path_str}: {data_dict_str}")

# Пример использования с указанием пути к файлу в виде объекта Path
file_path_path = Path("data.xls")
data_dict_path = xls2dict(xls_file=file_path_path)
if data_dict_path:
    print(f"Данные из файла {file_path_path}: {data_dict_path}")