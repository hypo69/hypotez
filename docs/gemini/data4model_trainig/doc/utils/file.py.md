### Анализ кода модуля `hypotez/src/utils/file.py`

## Обзор

Модуль предоставляет набор утилит для работы с файлами, включая функции для сохранения, чтения и поиска текстовых файлов. Модуль поддерживает обработку больших файлов с использованием генераторов для экономии памяти.

## Подробнее

Модуль содержит функции, упрощающие выполнение операций с файлами, такими как чтение и запись текстовых данных, а также рекурсивный поиск файлов в директориях с фильтрацией по расширениям.

## Функции

### `save_text_file`

```python
def save_text_file(
    data: str | list[str] | dict,
    file_path: str | Path,
    mode: str = 'w'
) -> bool:
    """
    Сохраняет данные в текстовый файл.

    Args:
        file_path (str | Path): Путь к файлу для сохранения.
        data (str | list[str] | dict): Данные для записи. Могут быть строкой, списком строк или словарем.
        mode (str, optional): Режим записи файла ('w' для записи, 'a' для добавления).
    Returns:
        bool: `True`, если файл успешно сохранен, `False` в противном случае.
    Raises:
        Exception: При возникновении ошибки при записи в файл.

    Example:
        >>> from pathlib import Path
        >>> file_path = Path('example.txt')
        >>> data = 'Пример текста'
        >>> result = save_text_file(file_path, data)
        >>> print(result)
        True
    """
    ...
```

**Назначение**:
Сохраняет данные в текстовый файл.

**Параметры**:
- `file_path` (str | Path): Путь к файлу для сохранения.
- `data` (str | list[str] | dict): Данные для записи. Могут быть строкой, списком строк или словарем.
- `mode` (str, optional): Режим записи файла ('w' для записи, 'a' для добавления). По умолчанию 'w'.

**Возвращает**:
- `bool`: `True`, если файл успешно сохранен, `False` в противном случае.

**Вызывает исключения**:
- `Exception`: При возникновении ошибки при записи в файл.

**Как работает функция**:
1. Преобразует `file_path` в объект `Path`.
2. Создает родительские директории для файла, если они не существуют.
3. Открывает файл в указанном режиме и кодировке UTF-8.
4. В зависимости от типа данных (`str`, `list`, `dict`):
    - Если данные - список, записывает каждую строку из списка в файл, добавляя символ новой строки.
    - Если данные - словарь, записывает их в файл в формате JSON с отступами.
    - Если данные - строка, записывает строку в файл.
5. Возвращает `True` в случае успеха, `False` в случае ошибки.

**Примеры**:

```python
from pathlib import Path
file_path = Path('example.txt')
data = 'Пример текста'
result = save_text_file(file_path, data)
print(result)
```

### `read_text_file_generator`

```python
def read_text_file_generator(
    file_path: str | Path,
    as_list: bool = False,
    extensions: Optional[list[str]] = None,
    chunk_size: int = 8192,
    recursive: bool = False,
    patterns: Optional[str | list[str]] = None,
) -> Generator[str, None, None] | str | list[str] | None:
    """
    Читает содержимое файла(ов) или директории.

        Args:
            file_path (str | Path): Путь к файлу или директории.
            as_list (bool, optional): Если `True`, то возвращает генератор строк или список строк, в зависимости от типа вывода.
            extensions (list[str], optional): Список расширений файлов для включения при чтении директории.
            chunk_size (int, optional): Размер чанка для чтения файла в байтах.
            recursive (bool, optional): Если `True`, то поиск файлов выполняется рекурсивно.
            patterns (str | list[str], optional): Шаблоны для фильтрации файлов при рекурсивном поиске.

        Returns:
            Generator[str, None, None] | str | list[str] | None:
            - Если `as_list` is True и `file_path` является файлом, возвращает генератор строк.
            - Если `as_list` is True и `file_path` является директорией и `recursive` is True, возвращает список строк.
            - Если `as_list` is False и `file_path` является файлом, возвращает строку.
            - Если `as_list` is False и `file_path` является директорией, возвращает объединенную строку.
            - Возвращает `None` в случае ошибки.
        Raises:
            Exception: При возникновении ошибки при чтении файла.

        Example:
            >>> from pathlib import Path
            >>> file_path = Path('example.txt')
            >>> content = read_text_file(file_path)
            >>> if content:
            ...    print(f'File content: {content[:100]}...')
            File content: Пример текста...
    Функция read_text_file может возвращать несколько разных типов данных в зависимости от входных параметров:

    Возвращаемые значения:
    ----------------------

    - Generator[str, None, None] (Генератор строк):
        Генератор при итерации выдаёт строки из файла(ов) по одной. Эффективно для работы с большими файлами, так как они не загружаются полностью в память.
        - Когда:
            file_path – это файл и as_list равен True.
            file_path – это директория, recursive равен True и as_list равен True. При этом в генератор попадают строки из всех найденных файлов.
            file_path – это директория, recursive равен False и as_list равен True. При этом в генератор попадают строки из всех найденных файлов в текущей директории.
        
    - str (Строка):
        Содержимое файла или объединенное содержимое всех файлов в виде одной строки.
        - Когда:
            file_path – это файл и as_list равен False.
            file_path – это директория, recursive равен False и as_list равен False. При этом возвращается объединенная строка, состоящая из содержимого всех файлов в директории, разделенных символами новой строки (\n).
            file_path – это директория, recursive равен True и as_list равен False. При этом возвращается объединенная строка, состоящая из содержимого всех файлов в директории и её поддиректориях, разделенных символами новой строки (\n).
 
    - list[str] (Список строк):
        Этот тип явно не возвращается функцией, однако когда file_path – это директория, recursive равен True и as_list равен True - функция возвращает генератор, который можно преобразовать в список при помощи list()
        - Когда:
            file_path – не является ни файлом, ни директорией.
            Произошла ошибка при чтении файла или директории (например, файл не найден, ошибка доступа и т.п.).


    Note:
        Если вы хотите прочитать содержимое файла построчно (особенно для больших файлов) используйте as_list = True. В этом случае вы получите генератор строк.
        Если вы хотите получить всё содержимое файла в виде одной строки используйте as_list = False.
        Если вы работаете с директорией, recursive = True будет обходить все поддиректории.
        extensions и patterns позволят вам фильтровать файлы при работе с директорией.
        chunk_size позволяет оптимизировать работу с большими файлами при чтении их по частям.
        None будет возвращён в случае ошибок.

    Важно помнить:
        В случае чтения директории, если as_list=False, функция объединяет все содержимое найденных файлов в одну строку. Это может потребовать много памяти, если файлов много или они большие.
        Функция полагается на другие функции-помощники (_read_file_lines_generator, _read_file_content, recursively_get_file_path, yield_text_from_files), которые здесь не определены и их поведение влияет на результат read_text_file.


    """
    ...
```

**Назначение**:
Читает содержимое файла(ов) или директории с использованием генератора.

**Параметры**:
- `file_path` (str | Path): Путь к файлу или директории.
- `as_list` (bool, optional): Если `True`, то возвращает генератор строк или список строк, в зависимости от типа вывода.
- `extensions` (list[str], optional): Список расширений файлов для включения при чтении директории.
- `chunk_size` (int, optional): Размер чанка для чтения файла в байтах.
- `recursive` (bool, optional): Если `True`, то поиск файлов выполняется рекурсивно.
- `patterns` (str | list[str], optional): Шаблоны для фильтрации файлов при рекурсивном поиске.

**Возвращает**:
- `Generator[str, None, None] | str | list[str] | None`:
    - Если `as_list` is True и `file_path` является файлом, возвращает генератор строк.
    - Если `as_list` is True и `file_path` является директорией и `recursive` is True, возвращает список строк.
    - Если `as_list` is False и `file_path` является файлом, возвращает строку.
    - Если `as_list` is False и `file_path` является директорией, возвращает объединенную строку.
    - Возвращает `None` в случае ошибки.

**Вызывает исключения**:
- `Exception`: При возникновении ошибки при чтении файла.

**Как работает функция**:
1. Преобразует `file_path` в объект `Path`.
2. Проверяет, является ли `file_path` файлом или директорией.
3. В зависимости от типа `file_path` и значения `as_list` вызывает соответствующие функции для чтения содержимого файла или директории с использованием генераторов.
4. Логирует ошибки при чтении файла или директории.

**Примеры**:

```python
from pathlib import Path
file_path = Path('example.txt')
content = read_text_file(file_path)
if content:
    print(f'File content: {content[:100]}...')
```

### `read_text_file`

```python
def read_text_file(
    file_path: Union[str, Path],\n    as_list: bool = False,\n    extensions: Optional[list[str]] = None,\n    exc_info: bool = True,\n) -> str | list[str] | None:
    """
    Read the contents of a file.

    Args:
        file_path (str | Path): Path to the file or directory.
        as_list (bool, optional): If True, returns content as list of lines. Defaults to False.
        extensions (list[str], optional): List of file extensions to include if reading a directory. Defaults to None.
        exc_info (bool, optional): If True, logs traceback on error. Defaults to True.

    Returns:
        str | list[str] | None: File content as a string or list of lines, or None if an error occurs.
    """
    ...
```

**Назначение**:
Читает содержимое файла.

**Параметры**:
- `file_path` (Union[str, Path]): Путь к файлу или директории.
- `as_list` (bool, optional): Если True, возвращает содержимое в виде списка строк. По умолчанию False.
- `extensions` (list[str], optional): Список расширений файлов для включения при чтении директории. По умолчанию None.
- `exc_info` (bool, optional): Если True, логирует информацию об ошибке. По умолчанию True.

**Возвращает**:
- `str | list[str] | None`: Содержимое файла в виде строки или списка строк, или None, если произошла ошибка.

**Как работает функция**:
1. Преобразует `file_path` в объект `Path`.
2. Если `file_path` является файлом, открывает файл для чтения в кодировке UTF-8 и возвращает либо список строк, либо всю строку целиком.
3. Если `file_path` является директорией, рекурсивно читает все файлы в директории с указанными расширениями и возвращает либо список строк, либо объединенную строку.
4. В случае ошибки логирует информацию об ошибке и возвращает None.

**Примеры**:

```python
from pathlib import Path
file_path = Path('example.txt')
content = read_text_file(file_path)
if content:
    print(f'File content: {content[:100]}...')
```

### `yield_text_from_files`

```python
def yield_text_from_files(
    file_path: str | Path,
    as_list: bool = False,
    chunk_size: int = 8192
) -> Generator[str, None, None] | str | None:
    """
    Читает содержимое файла и возвращает его в виде генератора строк или одной строки.

    Args:
        file_path (str | Path): Путь к файлу.
        as_list (bool, optional): Если True, возвращает генератор строк. По умолчанию False.
        chunk_size (int, optional): Размер чанка для чтения файла в байтах.

    Returns:
        Generator[str, None, None] | str | None: Генератор строк, объединенная строка или None в случае ошибки.

    Yields:
       str: Строки из файла, если as_list is True.

    Example:
        >>> from pathlib import Path
        >>> file_path = Path('example.txt')
        >>> for line in yield_text_from_files(file_path, as_list=True):
        ...     print(line)
        Первая строка файла
        Вторая строка файла
    """
    ...
```

**Назначение**:
Читает содержимое файла и возвращает его в виде генератора строк или одной строки.

**Параметры**:
- `file_path` (str | Path): Путь к файлу.
- `as_list` (bool, optional): Если True, возвращает генератор строк. По умолчанию False.
- `chunk_size` (int, optional): Размер чанка для чтения файла в байтах.

**Возвращает**:
- `Generator[str, None, None] | str | None`: Генератор строк, объединенная строка или None в случае ошибки.

**Как работает функция**:
1. Преобразует `file_path` в объект `Path`.
2. Проверяет, является ли `file_path` файлом.
3. Если `file_path` является файлом:
    - Если `as_list` равен True, возвращает генератор строк, читая файл построчно.
    - Если `as_list` равен False, возвращает содержимое файла как одну строку.
4. В случае ошибки логирует информацию об ошибке и возвращает None.

**Примеры**:

```python
from pathlib import Path
file_path = Path('example.txt')
for line in yield_text_from_files(file_path, as_list=True):
    print(line)
```

### `_read_file_content`

```python
def _read_file_content(file_path: Path, chunk_size: int) -> str:
    """
    Читает содержимое файла по чанкам и возвращает как строку.

    Args:
        file_path (Path): Путь к файлу для чтения.
        chunk_size (int): Размер чанка для чтения файла в байтах.
    Returns:
        str: Содержимое файла в виде строки.
    Raises:
        Exception: При возникновении ошибки при чтении файла.
    """
    ...
```

**Назначение**:
Читает содержимое файла по частям (чанкам) и возвращает как строку.

**Параметры**:
- `file_path` (Path): Путь к файлу для чтения.
- `chunk_size` (int): Размер чанка для чтения файла в байтах.

**Возвращает**:
- `str`: Содержимое файла в виде строки.

**Вызывает исключения**:
- `Exception`: При возникновении ошибки при чтении файла.

**Как работает функция**:
1. Открывает файл для чтения в кодировке UTF-8.
2. Читает файл по частям размером `chunk_size` байт.
3. Добавляет каждый чанк к общей строке.
4. Возвращает строку, содержащую всё содержимое файла.

### `_read_file_lines_generator`

```python
def _read_file_lines_generator(file_path: Path, chunk_size: int) -> Generator[str, None, None]:
    """
    Читает файл по строкам с помощью генератора.

    Args:
        file_path (Path): Путь к файлу для чтения.
        chunk_size (int): Размер чанка для чтения файла в байтах.
    Yields:
        str: Строки из файла.
    Raises:
        Exception: При возникновении ошибки при чтении файла.
    """
    ...
```

**Назначение**:
Читает файл построчно с использованием генератора.

**Параметры**:
- `file_path` (Path): Путь к файлу для чтения.
- `chunk_size` (int): Размер чанка для чтения файла в байтах.

**Возвращает**:
- `Generator[str, None, None]`: Генератор, выдающий строки из файла.

**Вызывает исключения**:
- `Exception`: При возникновении ошибки при чтении файла.

**Как работает функция**:
1. Открывает файл для чтения в кодировке UTF-8.
2. Читает файл по частям размером `chunk_size` байт.
3. Разделяет каждый чанк на строки.
4. Если чанк не заканчивается полной строкой, добавляет последнюю строку к следующему чанку.
5. Использует `yield from` для выдачи строк из чанка.

### `get_filenames_from_directory`

```python
def get_filenames_from_directory(
    directory: str | Path, ext: str | list[str] = '*'
) -> list[str]:
    """
    Возвращает список имен файлов в директории, опционально отфильтрованных по расширению.

    Args:
        directory (str | Path): Путь к директории для поиска.
        ext (str | list[str], optional): Расширения для фильтрации.
            По умолчанию '*'.

    Returns:
        list[str]: Список имен файлов, найденных в директории.

    Example:
        >>> from pathlib import Path
        >>> directory = Path('.')
        >>> get_filenames_from_directory(directory, ['.txt', '.md'])
        ['example.txt', 'readme.md']
    """
    ...
```

**Назначение**:
Возвращает список имен файлов в указанной директории, опционально отфильтрованных по расширению.

**Параметры**:
- `directory` (str | Path): Путь к директории для поиска.
- `ext` (str | list[str], optional): Расширения для фильтрации. По умолчанию '\*'.

**Возвращает**:
- `list[str]`: Список имен файлов, найденных в директории.

**Как работает функция**:
1. Проверяет, является ли указанный путь директорией.
2. Преобразует расширения в список, если они переданы как строка.
3. Перебирает все элементы в директории.
4. Фильтрует элементы, оставляя только файлы с указанными расширениями.
5. Возвращает список имен файлов.

**Примеры**:

```python
from pathlib import Path
directory = Path('.')
get_filenames_from_directory(directory, ['.txt', '.md'])
```

### `recursively_yield_file_path`

```python
def recursively_yield_file_path(
    root_dir: str | Path, patterns: str | list[str] = '*'
) -> Generator[Path, None, None]:
    """
    Рекурсивно возвращает пути ко всем файлам, соответствующим заданным шаблонам, в указанной директории.

    Args:
        root_dir (str | Path): Корневая директория для поиска.
        patterns (str | list[str]): Шаблоны для фильтрации файлов.

    Yields:
        Path: Путь к файлу, соответствующему шаблону.

    Example:
        >>> from pathlib import Path
        >>> root_dir = Path('.')
        >>> for path in recursively_yield_file_path(root_dir, ['*.txt', '*.md']):
        ...    print(path)
        ./example.txt
        ./readme.md
    """
    ...
```

**Назначение**:
Рекурсивно возвращает пути ко всем файлам, соответствующим заданным шаблонам, в указанной директории, используя генератор.

**Параметры**:
- `root_dir` (str | Path): Корневая директория для поиска.
- `patterns` (str | list[str], optional): Шаблоны для фильтрации файлов. По умолчанию '\*'.

**Возвращает**:
- `Generator[Path, None, None]`: Генератор, выдающий пути к файлам, соответствующим шаблону.

**Как работает функция**:
1. Преобразует шаблоны в список, если они переданы как строка.
2. Перебирает все шаблоны.
3. Использует `Path(root_dir).rglob(pattern)` для рекурсивного поиска файлов, соответствующих шаблону.
4. Использует `yield from` для выдачи путей к файлам из генератора.

**Примеры**:

```python
from pathlib import Path
root_dir = Path('.')
for path in recursively_yield_file_path(root_dir, ['*.txt', '*.md']):
    print(path)
```

### `recursively_get_file_path`

```python
def recursively_get_file_path(
    root_dir: str | Path,
    patterns: str | list[str] = '*'
) -> list[Path]:
    """
    Рекурсивно возвращает список путей ко всем файлам, соответствующим заданным шаблонам, в указанной директории.

    Args:
        root_dir (str | Path): Корневая директория для поиска.
        patterns (str | list[str]): Шаблоны для фильтрации файлов.

    Returns:
        list[Path]: Список путей к файлам, соответствующим шаблонам.

    Example:
        >>> from pathlib import Path
        >>> root_dir = Path('.')
        >>> paths = recursively_get_file_path(root_dir, ['*.txt', '*.md'])
        >>> print(paths)
        [Path('./example.txt'), Path('./readme.md')]
    """
    ...
```

**Назначение**:
Рекурсивно возвращает список путей ко всем файлам, соответствующим заданным шаблонам, в указанной директории.

**Параметры**:
- `root_dir` (str | Path): Корневая директория для поиска.
- `patterns` (str | list[str], optional): Шаблоны для фильтрации файлов. По умолчанию '\*'.

**Возвращает**:
- `list[Path]`: Список путей к файлам, соответствующим шаблонам.

**Как работает функция**:
1. Создает пустой список `file_paths`.
2. Преобразует шаблоны в список, если они переданы как строка.
3. Перебирает все шаблоны.
4. Использует `Path(root_dir).rglob(pattern)` для рекурсивного поиска файлов, соответствующих шаблону.
5. Добавляет все найденные пути в список `file_paths`.
6. Возвращает список `file_paths`.

**Примеры**:

```python
from pathlib import Path
root_dir = Path('.')
paths = recursively_get_file_path(root_dir, ['*.txt', '*.md'])
print(paths)
```

### `recursively_read_text_files`

```python
def recursively_read_text_files(
    root_dir: str | Path,
    patterns: str | list[str],
    as_list: bool = False
) -> list[str]:
    """
    Рекурсивно читает текстовые файлы из указанной корневой директории, соответствующие заданным шаблонам.

    Args:
        root_dir (str | Path): Путь к корневой директории для поиска.
        patterns (str | list[str]): Шаблон(ы) имени файла для фильтрации.
             Может быть как одиночным шаблоном (например, '*.txt'), так и списком.
        as_list (bool, optional): Если True, то возвращает содержимое файла как список строк.
             По умолчанию `False`.

    Returns:
        list[str]: Список содержимого файлов (или список строк, если `as_list=True`),
         соответствующих заданным шаблонам.

    Example:
        >>> from pathlib import Path
        >>> root_dir = Path('.')
        >>> contents = recursively_read_text_files(root_dir, ['*.txt', '*.md'], as_list=True)
        >>> for line in contents:
        ...     print(line)
        Содержимое example.txt
        Первая строка readme.md
        Вторая строка readme.md
    """
    ...
```

**Назначение**:
Рекурсивно читает текстовые файлы из указанной корневой директории, соответствующие заданным шаблонам.

**Параметры**:
- `root_dir` (str | Path): Путь к корневой директории для поиска.
- `patterns` (str | list[str]): Шаблон(ы) имени файла для фильтрации. Может быть как одиночным шаблоном (например, '\*.txt'), так и списком.
- `as_list` (bool, optional): Если True, то возвращает содержимое файла как список строк. По умолчанию `False`.

**Возвращает**:
- `list[str]`: Список содержимого файлов (или список строк, если `as_list=True`), соответствующих заданным шаблонам.

**Как работает функция**:
1. Создает пустой список `matches` для хранения содержимого файлов.
2. Преобразует `root_dir` в объект `Path`.
3. Проверяет, является ли `root_path` директорией. Если нет, возвращает пустой список.
4. Преобразует `patterns` в список, если передан строкой.
5. Рекурсивно обходит директорию `root_path` и для каждого файла проверяет соответствие имени файла одному из шаблонов.
6. Если имя файла соответствует шаблону, открывает файл для чтения в кодировке UTF-8 и добавляет его содержимое в список `matches` (либо как одну строку, либо как список строк, в зависимости от значения `as_list`).
7. Возвращает список `matches`.

**Примеры**:

```python
from pathlib import Path
root_dir = Path('.')
contents = recursively_read_text_files(root_dir, ['*.txt', '*.md'], as_list=True)
for line in contents:
    print(line)
```

### `get_directory_names`

```python
def get_directory_names(directory: str | Path) -> list[str]:
    """
    Возвращает список имен директорий из указанной директории.

    Args:
        directory (str | Path): Путь к директории, из которой нужно получить имена.

    Returns:
        list[str]: Список имен директорий, найденных в указанной директории.

    Example:
        >>> from pathlib import Path
        >>> directory = Path('.')
        >>> get_directory_names(directory)
        ['dir1', 'dir2']
    """
    ...
```

**Назначение**:
Возвращает список имен директорий из указанной директории.

**Параметры**:
- `directory` (str | Path): Путь к директории, из которой нужно получить имена.

**Возвращает**:
- `list[str]`: Список имен директорий, найденных в указанной директории.

**Как работает функция**:
1. Преобразует `directory` в объект `Path`.
2. Перебирает все элементы в директории.
3. Фильтрует элементы, оставляя только директории.
4. Возвращает список имен директорий.

**Примеры**:

```python
from pathlib import Path
directory = Path('.')
get_directory_names(directory)
```

### `remove_bom`

```python
def remove_bom(path: str | Path) -> None:
    """
    Удаляет BOM из текстового файла или из всех файлов Python в директории.

    Args:
        path (str | Path): Путь к файлу или директории.

    Example:
        >>> from pathlib import Path
        >>> file_path = Path('example.txt')
        >>> with open(file_path, 'w', encoding='utf-8') as f:
        ...     f.write('\\ufeffПример текста с BOM')
        >>> remove_bom(file_path)
        >>> with open(file_path, 'r', encoding='utf-8') as f:
        ...     print(f.read())
        Пример текста с BOM
    """
    ...
```

**Назначение**:
Удаляет BOM (Byte Order Mark) из текстового файла или из всех файлов Python в указанной директории.

**Параметры**:
- `path` (str | Path): Путь к файлу или директории.

**Возвращает**:
- None

**Как работает функция**:
1. Преобразует `path` в объект `Path`.
2. Если `path` является файлом:
    - Открывает файл для чтения и записи в кодировке UTF-8.
    - Читает содержимое файла, заменяя все BOM на пустую строку.
    - Перемещает указатель в начало файла и записывает очищенное содержимое.
    - Обрезает файл до длины нового содержимого.
3. Если `path` является директорией:
    - Рекурсивно обходит все файлы в директории.
    - Для каждого файла Python (с расширением `.py`) выполняет те же действия, что и для отдельного файла.
4. Если `path` не является ни файлом, ни директорией, логирует сообщение об ошибке.

**Примеры**:

```python
from pathlib import Path
file_path = Path('example.txt')
with open(file_path, 'w', encoding='utf-8') as f:
    f.write('\ufeffПример текста с BOM')
remove_bom(file_path)
with open(file_path, 'r', encoding='utf-8') as f:
    print(f.read())
```

## Переменные

Отсутствуют

## Запуск

Этот модуль предоставляет набор функций для работы с файлами. Для использования этих функций необходимо импортировать их из модуля `src.utils.file`.

```python
from src.utils.file import read_text_file, save_text_file

file_path = 'example.txt'
content = read_text_file(file_path)
if content:
    print(f'File content: {content[:100]}...')

save_text_file(file_path, 'Новый текст')