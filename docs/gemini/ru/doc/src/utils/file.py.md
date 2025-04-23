# Модуль `src.utils.file`

## Обзор

Модуль `src.utils.file` предоставляет набор утилит для работы с файлами, включая функции для чтения, записи и поиска файлов. Он поддерживает работу с текстовыми файлами, чтение больших файлов с использованием генераторов и рекурсивный поиск файлов в директориях.

## Подробней

Модуль предназначен для упрощения операций с файлами в проекте `hypotez`. Он предоставляет удобные функции для чтения и записи текстовых файлов, а также для поиска файлов по заданным шаблонам. Использование генераторов при чтении файлов позволяет эффективно обрабатывать большие файлы, не загружая их целиком в память.

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
```

**Назначение**: Сохраняет переданные данные в текстовый файл. Поддерживает сохранение строк, списков строк и словарей в формате JSON.

**Параметры**:
- `file_path` (str | Path): Путь к файлу, в который необходимо сохранить данные.
- `data` (str | list[str] | dict): Данные, которые необходимо записать в файл. Может быть строкой, списком строк или словарем. Если передан словарь, он будет сохранен в формате JSON с отступами.
- `mode` (str, optional): Режим открытия файла. По умолчанию `'w'` (запись). Можно также использовать `'a'` для добавления данных в конец файла.

**Возвращает**:
- `bool`: `True`, если данные успешно сохранены в файл, и `False` в случае ошибки.

**Вызывает исключения**:
- `Exception`: Возникает при ошибке записи в файл.

**Как работает функция**:
1. Преобразует `file_path` в объект `Path`.
2. Создает родительские директории, если они не существуют.
3. Открывает файл в указанном режиме и кодировке UTF-8.
4. Записывает данные в файл в зависимости от их типа:
   - Если `data` - это список, записывает каждый элемент списка в отдельную строку.
   - Если `data` - это словарь, записывает его в формате JSON с отступами.
   - Если `data` - это строка, записывает строку в файл.
5. В случае возникновения исключения, логирует ошибку и возвращает `False`.

**Примеры**:

```python
from pathlib import Path
from src.utils.file import save_text_file

# Сохранение строки в файл
file_path = Path('example.txt')
data = 'Пример текста'
result = save_text_file(file_path, data)
print(result)  # Вывод: True

# Сохранение списка строк в файл
file_path = Path('example.txt')
data = ['Строка 1', 'Строка 2', 'Строка 3']
result = save_text_file(file_path, data)
print(result)  # Вывод: True

# Сохранение словаря в файл в формате JSON
file_path = Path('example.json')
data = {'ключ1': 'значение1', 'ключ2': 'значение2'}
result = save_text_file(file_path, data)
print(result)  # Вывод: True
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
            File content: Пример текста...\n
    Функция read_text_file может возвращать несколько разных типов данных в зависимости от входных параметров:\n\n    Возвращаемые значения:\n    ----------------------\n\n    - Generator[str, None, None] (Генератор строк):\n        Генератор при итерации выдаёт строки из файла(ов) по одной. Эффективно для работы с большими файлами, так как они не загружаются полностью в память.\n        - Когда:\n            file_path – это файл и as_list равен True.\n            file_path – это директория, recursive равен True и as_list равен True. При этом в генератор попадают строки из всех найденных файлов.\n            file_path – это директория, recursive равен False и as_list равен True. При этом в генератор попадают строки из всех найденных файлов в текущей директории.\n        \n    - str (Строка):\n        Содержимое файла или объединенное содержимое всех файлов в виде одной строки.\n        - Когда:\n            file_path – это файл и as_list равен False.\n            file_path – это директория, recursive равен False и as_list равен False. При этом возвращается объединенная строка, состоящая из содержимого всех файлов в директории, разделенных символами новой строки (\\n).\n            file_path – это директория, recursive равен True и as_list равен False. При этом возвращается объединенная строка, состоящая из содержимого всех файлов в директории и её поддиректориях, разделенных символами новой строки (\\n).\n \n    - list[str] (Список строк):\n        Этот тип явно не возвращается функцией, однако когда file_path – это директория, recursive равен True и as_list равен True - функция возвращает генератор, который можно преобразовать в список при помощи list()\n        - Когда:\n            file_path – не является ни файлом, ни директорией.\n            Произошла ошибка при чтении файла или директории (например, файл не найден, ошибка доступа и т.п.).\n\n\n    Note:\n        Если вы хотите прочитать содержимое файла построчно (особенно для больших файлов) используйте as_list = True. В этом случае вы получите генератор строк.\n        Если вы хотите получить всё содержимое файла в виде одной строки используйте as_list = False.\n        Если вы работаете с директорией, recursive = True будет обходить все поддиректории.\n        extensions и patterns позволят вам фильтровать файлы при работе с директорией.\n        chunk_size позволяет оптимизировать работу с большими файлами при чтении их по частям.\n        None будет возвращён в случае ошибок.\n\n    Важно помнить:\n        В случае чтения директории, если as_list=False, функция объединяет все содержимое найденных файлов в одну строку. Это может потребовать много памяти, если файлов много или они большие.\n        Функция полагается на другие функции-помощники (_read_file_lines_generator, _read_file_content, recursively_get_file_path, yield_text_from_files), которые здесь не определены и их поведение влияет на результат read_text_file.\n\n\n    """
```

**Назначение**: Читает содержимое файла или файлов в директории с использованием генератора для экономии памяти.

**Параметры**:
- `file_path` (str | Path): Путь к файлу или директории.
- `as_list` (bool, optional): Если `True`, возвращает генератор строк. По умолчанию `False`.
- `extensions` (list[str], optional): Список расширений файлов для включения при чтении директории. По умолчанию `None`.
- `chunk_size` (int, optional): Размер чанка для чтения файла в байтах. По умолчанию 8192.
- `recursive` (bool, optional): Если `True`, выполняет рекурсивный поиск файлов в директории. По умолчанию `False`.
- `patterns` (str | list[str], optional): Шаблоны для фильтрации файлов при рекурсивном поиске. По умолчанию `None`.

**Возвращает**:
- `Generator[str, None, None] | str | list[str] | None`:
    - Если `as_list` is `True` и `file_path` является файлом, возвращает генератор строк.
    - Если `as_list` is `True` и `file_path` является директорией и `recursive` is `True`, возвращает список строк.
    - Если `as_list` is `False` и `file_path` является файлом, возвращает строку.
    - Если `as_list` is `False` и `file_path` является директорией, возвращает объединенную строку.
    - Возвращает `None` в случае ошибки.

**Вызывает исключения**:
- `Exception`: Возникает при ошибке при чтении файла.

**Как работает функция**:
1. Преобразует `file_path` в объект `Path`.
2. Проверяет, является ли `file_path` файлом или директорией.
3. Если `file_path` является файлом:
   - Если `as_list` is `True`, возвращает генератор строк, используя функцию `_read_file_lines_generator`.
   - Если `as_list` is `False`, возвращает содержимое файла в виде строки, используя функцию `_read_file_content`.
4. Если `file_path` является директорией:
   - Если `recursive` is `True`:
     - Если `patterns` заданы, использует `recursively_get_file_path` для получения списка файлов, соответствующих шаблонам.
     - Иначе, использует `path.rglob('*')` для получения всех файлов в директории и её поддиректориях.
     - Если `as_list` is `True`, возвращает генератор строк, объединяющий строки из всех найденных файлов, используя функцию `yield_text_from_files`.
     - Если `as_list` is `False`, возвращает объединенную строку, состоящую из содержимого всех файлов, разделенных символами новой строки.
   - Если `recursive` is `False`:
     - Использует `path.iterdir()` для получения списка файлов в директории.
     - Если `as_list` is `True`, возвращает генератор строк, объединяющий строки из всех найденных файлов.
     - Если `as_list` is `False`, возвращает объединенную строку, состоящую из содержимого всех файлов, разделенных символами новой строки.
5. Если `file_path` не является ни файлом, ни директорией, логирует ошибку и возвращает `None`.
6. В случае возникновения исключения, логирует ошибку и возвращает `None`.

**Примеры**:

```python
from pathlib import Path
from src.utils.file import read_text_file

# Чтение содержимого файла в виде строки
file_path = Path('example.txt')
content = read_text_file(file_path)
if content:
    print(f'File content: {content[:100]}...')

# Чтение содержимого файла в виде списка строк
file_path = Path('example.txt')
content = read_text_file(file_path, as_list=True)
if content:
    for line in content:
        print(line)

# Чтение файлов из директории рекурсивно
dir_path = Path('.')
content = read_text_file(dir_path, as_list=False, recursive=True, extensions=['.txt'])
if content:
    print(f'Combined content: {content[:100]}...')
```

### `read_text_file`

```python
def read_text_file(
    file_path: Union[str, Path],
    as_list: bool = False,
    extensions: Optional[list[str]] = None,
    exc_info: bool = True,
    chunk_size: int = 8192
) -> str | list[str] | None:
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
```

**Назначение**: Читает содержимое файла и возвращает его в виде строки или списка строк.

**Параметры**:
- `file_path` (str | Path): Путь к файлу или директории.
- `as_list` (bool, optional): Если `True`, возвращает содержимое в виде списка строк. По умолчанию `False`.
- `extensions` (list[str], optional): Список расширений файлов для включения при чтении директории. По умолчанию `None`.
- `exc_info` (bool, optional): Если `True`, логирует traceback при ошибке. По умолчанию `True`.
- `chunk_size` (int, optional): Размер чанка для чтения файла в байтах. По умолчанию 8192.

**Возвращает**:
- `str | list[str] | None`: Содержимое файла в виде строки или списка строк, или `None`, если произошла ошибка.

**Как работает функция**:
1. Преобразует `file_path` в объект `Path`.
2. Проверяет, является ли `file_path` файлом или директорией.
3. Если `file_path` является файлом:
   - Открывает файл для чтения в кодировке UTF-8.
   - Читает содержимое файла.
   - Заменяет последовательности пробелов одним пробелом.
   - Экранирует двойные кавычки.
   - Возвращает список строк, если `as_list` is `True`, иначе возвращает строку.
4. Если `file_path` является директорией:
   - Получает список файлов в директории, соответствующих заданным расширениям.
   - Рекурсивно вызывает `read_text_file` для каждого файла.
   - Возвращает список содержимого файлов, если `as_list` is `True`, иначе возвращает объединенную строку.
5. Если `file_path` не является ни файлом, ни директорией, логирует предупреждение и возвращает `None`.
6. В случае возникновения исключения, логирует ошибку и возвращает `None`.

**Примеры**:

```python
from pathlib import Path
from src.utils.file import read_text_file

# Чтение содержимого файла в виде строки
file_path = Path('example.txt')
content = read_text_file(file_path)
print(content)

# Чтение содержимого файла в виде списка строк
file_path = Path('example.txt')
content = read_text_file(file_path, as_list=True)
print(content)

# Чтение файлов из директории
dir_path = Path('.')
content = read_text_file(dir_path, extensions=['.txt'])
print(content)
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
```

**Назначение**: Читает содержимое файла и возвращает его в виде генератора строк или одной строки.

**Параметры**:
- `file_path` (str | Path): Путь к файлу.
- `as_list` (bool, optional): Если `True`, возвращает генератор строк. По умолчанию `False`.
- `chunk_size` (int, optional): Размер чанка для чтения файла в байтах.

**Возвращает**:
- `Generator[str, None, None] | str | None`: Генератор строк, объединенная строка или `None` в случае ошибки.

**Yields**:
- `str`: Строки из файла, если `as_list` is `True`.

**Как работает функция**:
1. Преобразует `file_path` в объект `Path`.
2. Проверяет, является ли `file_path` файлом.
3. Если `file_path` является файлом:
   - Если `as_list` is `True`, возвращает генератор строк, используя функцию `_read_file_lines_generator`.
   - Если `as_list` is `False`, возвращает содержимое файла в виде строки, используя функцию `_read_file_content`.
4. Если `file_path` не является файлом, логирует ошибку и возвращает `None`.
5. В случае возникновения исключения, логирует ошибку и возвращает `None`.

**Примеры**:

```python
from pathlib import Path
from src.utils.file import yield_text_from_files

# Чтение файла по строкам с использованием генератора
file_path = Path('example.txt')
for line in yield_text_from_files(file_path, as_list=True):
    print(line)

# Чтение содержимого файла в виде одной строки
file_path = Path('example.txt')
content = next(yield_text_from_files(file_path))
print(content)
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
```

**Назначение**: Читает содержимое файла по частям (чанкам) и возвращает его в виде одной строки.

**Параметры**:
- `file_path` (Path): Путь к файлу, который нужно прочитать.
- `chunk_size` (int): Размер каждого чанка при чтении файла (в байтах).

**Возвращает**:
- `str`: Полное содержимое файла в виде строки.

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при чтении файла.

**Как работает функция**:

1. Открывает файл по указанному пути в режиме чтения с кодировкой UTF-8.
2. Инициализирует пустую строку `content` для хранения содержимого файла.
3. В цикле читает файл по частям размером `chunk_size` байт.
4. Добавляет каждый прочитанный чанк к строке `content`.
5. Если `chunk` пуст, это означает, что достигнут конец файла, и цикл завершается.
6. После завершения чтения заменяет все последовательности пробелов одним пробелом.
7. Экранирует все двойные кавычки.
8. Возвращает строку `content`, содержащую всё содержимое файла.

**Примеры**:

```python
from pathlib import Path
from src.utils.file import _read_file_content

# Пример использования функции
file_path = Path("example.txt")
chunk_size = 4096
content = _read_file_content(file_path, chunk_size)
print(content)
```

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
```

**Назначение**: Читает файл построчно с использованием генератора.

**Параметры**:
- `file_path` (Path): Путь к файлу для чтения.
- `chunk_size` (int): Размер чанка для чтения файла в байтах.

**Yields**:
- `str`: Строки из файла.

**Вызывает исключения**:
- `Exception`: Возникает при ошибке при чтении файла.

**Как работает функция**:

1. Открывает файл для чтения с указанием кодировки UTF-8.
2. В цикле считывает содержимое файла чанками заданного размера (`chunk_size`).
3. Разбивает каждый чанк на строки с использованием `splitlines()`.
4. Если чанк не заканчивается полной строкой (т.е. не заканчивается символом новой строки `\n`), добавляет последнюю строку из текущего чанка к следующему чанку, чтобы избежать разделения строки между чанками.
5. Перебирает полученные строки и для каждой строки:
   - Заменяет все последовательности пробелов одним пробелом.
   - Экранирует двойные кавычки.
   - Возвращает строку с использованием `yield`.

**Примеры**:

```python
from pathlib import Path
from src.utils.file import _read_file_lines_generator

# Пример использования функции
file_path = Path("example.txt")
chunk_size = 4096
for line in _read_file_lines_generator(file_path, chunk_size):
    print(line)
```

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
```

**Назначение**: Возвращает список имен файлов в указанной директории, с возможностью фильтрации по расширению.

**Параметры**:
- `directory` (str | Path): Путь к директории, в которой производится поиск файлов.
- `ext` (str | list[str], optional): Расширения файлов для фильтрации. Если указана строка `'*'`, фильтрация по расширению не производится. По умолчанию `'*'`.

**Возвращает**:
- `list[str]`: Список имен файлов, найденных в директории и соответствующих критериям фильтрации.

**Как работает функция**:

1. Проверяет, является ли указанный путь `directory` директорией. Если нет, логирует ошибку и возвращает пустой список.
2. Преобразует параметр `ext` в список расширений, если он является строкой. Если `ext` равно `'*'`, список расширений остается пустым, что означает отсутствие фильтрации по расширению.
3. Если расширения указаны без точки в начале, добавляет точку к каждому расширению.
4. Перебирает все элементы в указанной директории с использованием `directory.iterdir()`.
5. Для каждого элемента проверяет, является ли он файлом и соответствует ли его расширение одному из указанных в списке расширений (если список не пуст).
6. Если элемент является файлом и соответствует критериям фильтрации, добавляет его имя в список результатов.
7. В случае возникновения исключения, логирует ошибку и возвращает пустой список.

**Примеры**:

```python
from pathlib import Path
from src.utils.file import get_filenames_from_directory

# Получение списка имен всех файлов в текущей директории
directory = Path('.')
filenames = get_filenames_from_directory(directory)
print(filenames)

# Получение списка имен файлов с расширениями .txt и .md в текущей директории
directory = Path('.')
filenames = get_filenames_from_directory(directory, ['.txt', '.md'])
print(filenames)
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
```

**Назначение**: Рекурсивно обходит указанную директорию и возвращает пути ко всем файлам, соответствующим заданным шаблонам, в виде генератора.

**Параметры**:
- `root_dir` (str | Path): Корневая директория для поиска файлов.
- `patterns` (str | list[str], optional): Шаблоны для фильтрации файлов. Может быть как строкой (одиночный шаблон), так и списком строк (множественные шаблоны). По умолчанию `*` (все файлы).

**Yields**:
- `Path`: Путь к файлу, соответствующему заданному шаблону.

**Как работает функция**:

1. Преобразует параметр `patterns` в список, если он является строкой.
2. Перебирает все шаблоны в списке `patterns`.
3. Для каждого шаблона использует метод `rglob` объекта `Path(root_dir)` для рекурсивного поиска файлов, соответствующих шаблону.
4. Возвращает пути к файлам с использованием `yield from`, что позволяет возвращать значения из генератора `rglob`.
5. В случае возникновения исключения, логирует ошибку.

**Примеры**:

```python
from pathlib import Path
from src.utils.file import recursively_yield_file_path

# Пример использования функции
root_dir = Path('.')
patterns = ['*.txt', '*.md']
for path in recursively_yield_file_path(root_dir, patterns):
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
```

**Назначение**: Рекурсивно обходит указанную директорию и возвращает список путей ко всем файлам, соответствующим заданным шаблонам.

**Параметры**:
- `root_dir` (str | Path): Корневая директория для поиска файлов.
- `patterns` (str | list[str], optional): Шаблоны для фильтрации файлов. Может быть как строкой (одиночный шаблон), так и списком строк (множественные шаблоны). По умолчанию `*` (все файлы).

**Возвращает**:
- `list[Path]`: Список путей к файлам, соответствующим заданным шаблонам.

**Как работает функция**:

1. Инициализирует пустой список `file_paths` для хранения путей к файлам.
2. Преобразует параметр `patterns` в список, если он является строкой.
3. Перебирает все шаблоны в списке `patterns`.
4. Для каждого шаблона использует метод `rglob` объекта `Path(root_dir)` для рекурсивного поиска файлов, соответствующих шаблону.
5. Расширяет список `file_paths` путями к найденным файлам.
6. В случае возникновения исключения, логирует ошибку и возвращает пустой список.

**Примеры**:

```python
from pathlib import Path
from src.utils.file import recursively_get_file_path

# Пример использования функции
root_dir = Path('.')
patterns = ['*.txt', '*.md']
paths = recursively_get_file_path(root_dir, patterns)
print(paths)
```

### `recursively_read_text_files`

```python
def recursively_read_text_files(
    root_dir: str | Path,
    patterns: str | list[str],\
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
```

**Назначение**: Рекурсивно читает текстовые файлы из указанной корневой директории, соответствующие заданным шаблонам, и возвращает их содержимое в виде списка.

**Параметры**:
- `root_dir` (str | Path): Путь к корневой директории для поиска.
- `patterns` (str | list[str]): Шаблоны для фильтрации файлов.
- `as_list` (bool, optional): Если `True`, возвращает содержимое каждого файла в виде списка строк. По умолчанию `False`.

**Возвращает**:
- `list[str]`: Список содержимого файлов (или список строк, если `as_list=True`), соответствующих заданным шаблонам.

**Как работает функция**:
1. Инициализирует пустой список `matches` для хранения содержимого файлов.
2.