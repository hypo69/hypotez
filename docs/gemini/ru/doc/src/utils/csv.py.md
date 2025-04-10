# Модуль для работы с CSV и JSON файлами
=================================================

Модуль содержит функции для сохранения, чтения и преобразования файлов CSV и JSON.

Пример использования
----------------------

```python
from src.utils.csv import save_csv_file, read_csv_file, read_csv_as_json

# Сохранение данных в CSV файл
data = [{'name': 'John', 'age': '30'}, {'name': 'Jane', 'age': '25'}]
file_path = 'data.csv'
save_csv_file(data, file_path, mode='w')

# Чтение данных из CSV файла
read_data = read_csv_file(file_path)
if read_data:
    print(read_data)

# Преобразование CSV файла в JSON
csv_file_path = 'data.csv'
json_file_path = 'data.json'
read_csv_as_json(csv_file_path, json_file_path)
```

## Обзор

Модуль предоставляет набор утилит для работы с CSV и JSON файлами. Он включает функции для сохранения данных в формате CSV, чтения данных из CSV файлов, преобразования CSV в JSON, а также для чтения CSV файлов в виде словарей.

## Подробнее

Этот модуль предназначен для упрощения операций чтения и записи данных в формате CSV и JSON. Он предоставляет удобные функции, которые позволяют разработчикам легко манипулировать данными, сохранять их в файлы и загружать из файлов. Модуль использует стандартные библиотеки `csv` и `json`, а также библиотеку `pandas` для более удобной работы с данными.  Для логгирования используется модуль `logger` из `src.logger.logger`.

## Функции

### `save_csv_file`

**Назначение**: Сохраняет список словарей в CSV файл.

**Параметры**:
- `data` (List[Dict[str, str]]): Список словарей для сохранения.
- `file_path` (Union[str, Path]): Путь к CSV файлу.
- `mode` (str): Режим файла ('a' для добавления, 'w' для перезаписи). По умолчанию 'a'.
- `exc_info` (bool): Включать ли информацию об отслеживании в логи.

**Возвращает**:
- `bool`: `True`, если успешно, иначе `False`.

**Вызывает исключения**:
- `TypeError`: Если входные данные не являются списком словарей.
- `ValueError`: Если входные данные пусты.

**Как работает функция**:
Функция `save_csv_file` принимает список словарей и сохраняет их в CSV файл по указанному пути. Сначала проверяется, что входные данные являются списком словарей и не пусты. Затем создается объект `Path` для работы с путем к файлу, и создаются родительские каталоги, если они не существуют. После этого файл открывается в указанном режиме (`a` или `w`) и используется `csv.DictWriter` для записи данных в файл. Если файл открывается в режиме записи (`w`) или файл не существует, записывается строка заголовка. Наконец, данные записываются в файл построчно. В случае возникновения исключения, информация об ошибке логируется с использованием `logger.error`, и функция возвращает `False`.

**Примеры**:

```python
from pathlib import Path
from src.utils.csv import save_csv_file

# Пример 1: Сохранение данных в новый CSV файл
data = [{'name': 'John', 'age': '30'}, {'name': 'Jane', 'age': '25'}]
file_path = 'data.csv'
result = save_csv_file(data, file_path, mode='w')
print(f'Результат сохранения: {result}')  # Вывод: Результат сохранения: True

# Пример 2: Добавление данных в существующий CSV файл
data = [{'name': 'Mike', 'age': '35'}]
file_path = 'data.csv'
result = save_csv_file(data, file_path, mode='a')
print(f'Результат добавления: {result}')  # Вывод: Результат добавления: True

# Пример 3: Обработка исключения при некорректных входных данных
data = 'not a list'
file_path = 'data.csv'
try:
    result = save_csv_file(data, file_path, mode='w')
except TypeError as ex:
    print(f'Ошибка: {ex}')  # Вывод: Ошибка: Input data must be a list of dictionaries.
```

### `read_csv_file`

**Назначение**: Читает содержимое CSV файла в виде списка словарей.

**Параметры**:
- `file_path` (Union[str, Path]): Путь к CSV файлу.
- `exc_info` (bool): Включать ли информацию об отслеживании в логи.

**Возвращает**:
- `List[Dict[str, str]] | None`: Список словарей или `None`, если не удалось прочитать файл.

**Вызывает исключения**:
- `FileNotFoundError`: Если файл не найден.

**Как работает функция**:
Функция `read_csv_file` читает CSV файл, расположенный по указанному пути, и возвращает его содержимое в виде списка словарей. Функция открывает файл в режиме чтения с кодировкой UTF-8 и использует `csv.DictReader` для чтения данных. Каждая строка CSV файла преобразуется в словарь, где ключи соответствуют заголовкам столбцов. В случае, если файл не найден, логируется ошибка с использованием `logger.error`, и возвращается `None`. Если возникает какое-либо другое исключение при чтении файла, также логируется ошибка и возвращается `None`.

**Примеры**:

```python
from pathlib import Path
from src.utils.csv import read_csv_file, save_csv_file

# Подготовка: Создание CSV файла для чтения
data = [{'name': 'John', 'age': '30'}, {'name': 'Jane', 'age': '25'}]
file_path = 'data.csv'
save_csv_file(data, file_path, mode='w')

# Пример 1: Чтение данных из существующего CSV файла
read_data = read_csv_file(file_path)
if read_data:
    print(f'Прочитанные данные: {read_data}')  # Вывод: Прочитанные данные: [{'name': 'John', 'age': '30'}, {'name': 'Jane', 'age': '25'}]
else:
    print('Не удалось прочитать файл')

# Пример 2: Обработка случая, когда файл не найден
file_path = 'non_existent_file.csv'
read_data = read_csv_file(file_path)
if read_data is None:
    print('Файл не найден')  # Вывод: Файл не найден
```

### `read_csv_as_json`

**Назначение**: Преобразует CSV файл в формат JSON и сохраняет его.

**Параметры**:
- `csv_file_path` (Union[str, Path]): Путь к CSV файлу.
- `json_file_path` (Union[str, Path]): Путь для сохранения JSON файла.
- `exc_info` (bool): Включать ли информацию об отслеживании в логи.

**Возвращает**:
- `bool`: `True`, если преобразование успешно, иначе `False`.

**Как работает функция**:
Функция `read_csv_as_json` преобразует CSV файл в JSON формат и сохраняет его по указанному пути. Сначала вызывается функция `read_csv_file` для чтения данных из CSV файла. Если данные успешно прочитаны, они записываются в JSON файл с отступом в 4 пробела для удобочитаемости. Если чтение CSV файла не удалось, функция возвращает `False`. В случае возникновения исключения при записи в JSON файл, информация об ошибке логируется с использованием `logger.error`, и функция возвращает `False`.

**Примеры**:

```python
from pathlib import Path
from src.utils.csv import read_csv_as_json, save_csv_file

# Подготовка: Создание CSV файла для преобразования
data = [{'name': 'John', 'age': '30'}, {'name': 'Jane', 'age': '25'}]
csv_file_path = 'data.csv'
save_csv_file(data, csv_file_path, mode='w')

# Пример 1: Преобразование CSV в JSON
json_file_path = 'data.json'
result = read_csv_as_json(csv_file_path, json_file_path)
print(f'Результат преобразования: {result}')  # Вывод: Результат преобразования: True

# Пример 2: Обработка случая, когда CSV файл не существует
csv_file_path = 'non_existent_file.csv'
json_file_path = 'data.json'
result = read_csv_as_json(csv_file_path, json_file_path)
print(f'Результат преобразования: {result}')  # Вывод: Результат преобразования: False
```

### `read_csv_as_dict`

**Назначение**: Преобразует содержимое CSV файла в словарь.

**Параметры**:
- `csv_file` (Union[str, Path]): Путь к CSV файлу.

**Возвращает**:
- `dict | None`: Словарь, представляющий содержимое CSV файла, или `None`, если не удалось прочитать файл.

**Как работает функция**:
Функция `read_csv_as_dict` читает CSV файл и преобразует его содержимое в словарь, где ключ `"data"` содержит список словарей, представляющих строки CSV файла. Функция открывает файл в режиме чтения с кодировкой UTF-8 и использует `csv.DictReader` для чтения данных. В случае возникновения исключения при чтении файла, информация об ошибке логируется с использованием `logger.error`, и функция возвращает `None`.

**Примеры**:

```python
from pathlib import Path
from src.utils.csv import read_csv_as_dict, save_csv_file

# Подготовка: Создание CSV файла для чтения
data = [{'name': 'John', 'age': '30'}, {'name': 'Jane', 'age': '25'}]
csv_file_path = 'data.csv'
save_csv_file(data, csv_file_path, mode='w')

# Пример 1: Чтение данных из существующего CSV файла в виде словаря
read_data = read_csv_as_dict(csv_file_path)
if read_data:
    print(f'Прочитанные данные: {read_data}')
    # Вывод: Прочитанные данные: {'data': [{'name': 'John', 'age': '30'}, {'name': 'Jane', 'age': '25'}]}
else:
    print('Не удалось прочитать файл')

# Пример 2: Обработка случая, когда файл не найден
csv_file_path = 'non_existent_file.csv'
read_data = read_csv_as_dict(csv_file_path)
if read_data is None:
    print('Не удалось прочитать файл')  # Вывод: Не удалось прочитать файл
```

### `read_csv_as_ns`

**Назначение**: Загружает данные CSV в список словарей, используя Pandas.

**Параметры**:
- `file_path` (Union[str, Path]): Путь к CSV файлу.

**Возвращает**:
- `List[dict]`: Список словарей, представляющих содержимое CSV файла.

**Вызывает исключения**:
- `FileNotFoundError`: Если файл не найден.

**Как работает функция**:
Функция `read_csv_as_ns` использует библиотеку Pandas для чтения CSV файла и преобразования его содержимого в список словарей. Pandas предоставляет удобный способ работы с данными в табличном формате. Функция `pd.read_csv` читает CSV файл, а метод `to_dict(orient='records')` преобразует данные в список словарей, где каждый словарь представляет строку CSV файла. В случае, если файл не найден, логируется ошибка с использованием `logger.error`, и возвращается пустой список. Если возникает какое-либо другое исключение при чтении файла, также логируется ошибка и возвращается пустой список.

**Примеры**:

```python
from pathlib import Path
from src.utils.csv import read_csv_as_ns, save_csv_file

# Подготовка: Создание CSV файла для чтения
data = [{'name': 'John', 'age': '30'}, {'name': 'Jane', 'age': '25'}]
csv_file_path = 'data.csv'
save_csv_file(data, csv_file_path, mode='w')

# Пример 1: Чтение данных из существующего CSV файла в виде списка словарей
read_data = read_csv_as_ns(csv_file_path)
print(f'Прочитанные данные: {read_data}')
# Вывод: Прочитанные данные: [{'name': 'John', 'age': '30'}, {'name': 'Jane', 'age': '25'}]

# Пример 2: Обработка случая, когда файл не найден
csv_file_path = 'non_existent_file.csv'
read_data = read_csv_as_ns(csv_file_path)
print(f'Прочитанные данные: {read_data}')  # Вывод: Прочитанные данные: []