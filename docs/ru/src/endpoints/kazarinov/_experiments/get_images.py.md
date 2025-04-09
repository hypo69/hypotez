# Модуль для получения списка изображений, сгенерированных ИИ
## Обзор
Модуль предназначен для получения списка изображений, которые были сгенерированы искусственным интеллектом. Он сканирует указанную директорию, извлекает пути к файлам изображений и предоставляет их для дальнейшего использования.

## Подробнее
Этот модуль используется для поиска изображений, сгенерированных ИИ, в определенной директории. Он использует функции `recursively_get_filepath` для рекурсивного обхода директорий и поиска файлов с указанными расширениями (`*.jpeg`, `*.jpg`, `*.png`). Затем он выводит список найденных изображений, используя функцию `pprint`.

## Функции

### `recursively_get_filepath`

```python
from src.utils.file import read_text_file, save_text_file, recursively_get_filepath
from src.utils.printer import pprint

def recursively_get_filepath(
    root_dir: str | Path,
    patterns: str | List[str],
    ignore_hidden: bool = True,
    only_names: bool = False
) -> list[str]:
    """
    Рекурсивно получает список путей к файлам, соответствующим заданным шаблонам, в указанной директории.

    Args:
        root_dir (str | Path): Корневая директория для поиска файлов.
        patterns (str | List[str]): Шаблоны файлов для поиска (например, ['*.txt', '*.pdf']).
        ignore_hidden (bool): Игнорировать скрытые файлы и директории. По умолчанию `True`.
        only_names (bool): Возвращать только имена файлов вместо полных путей. По умолчанию `False`.

    Returns:
        list[str]: Список путей к файлам, соответствующим заданным шаблонам.
    """
    ...
```

**Параметры**:
- `root_dir` (str | Path): Корневая директория, в которой будет производиться поиск файлов.
- `patterns` (str | List[str]): Шаблоны файлов для поиска (например, `*.txt`, `*.pdf`).
- `ignore_hidden` (bool): Игнорировать скрытые файлы и директории. По умолчанию `True`.
- `only_names` (bool): Возвращать только имена файлов вместо полных путей. По умолчанию `False`.

**Возвращает**:
- `list[str]`: Список путей к файлам, соответствующим заданным шаблонам.

**Как работает функция**:

1.  Функция `recursively_get_filepath` рекурсивно обходит указанную корневую директорию (`root_dir`).
2.  Для каждого файла и директории проверяется, нужно ли игнорировать скрытые элементы (`ignore_hidden`).
3.  Если элемент не скрытый, проверяется, соответствует ли имя файла одному из заданных шаблонов (`patterns`).
4.  Если файл соответствует шаблону, его путь (или имя, если `only_names` равно `True`) добавляется в список результатов.
5.  Если встречается директория, функция рекурсивно вызывается для этой директории.
6.  В конце функция возвращает список всех найденных путей к файлам, соответствующих заданным шаблонам.

```
recursively_get_filepath
│
├── root_dir, patterns, ignore_hidden, only_names
│
├─── Проверка: файл соответствует шаблону?
│    │
│    └─── Да: добавить путь/имя файла в список результатов
│
└─── Проверка: это директория?
     │
     └─── Да: рекурсивный вызов для этой директории
```

**Примеры**:
```python
from pathlib import Path
from src.utils.file import recursively_get_filepath

# Пример 1: Получение полных путей к файлам с расширением .txt в указанной директории
root_dir = Path("./test_dir")
patterns = ["*.txt"]
files = recursively_get_filepath(root_dir, patterns)
print(files)
# Output: ['./test_dir/file1.txt', './test_dir/subdir/file2.txt']

# Пример 2: Получение только имен файлов с расширением .txt в указанной директории
root_dir = Path("./test_dir")
patterns = ["*.txt"]
files = recursively_get_filepath(root_dir, patterns, only_names=True)
print(files)
# Output: ['file1.txt', 'file2.txt']

# Пример 3: Получение файлов с расширениями .txt и .pdf
root_dir = Path("./test_dir")
patterns = ["*.txt", "*.pdf"]
files = recursively_get_filepath(root_dir, patterns)
print(files)
# Output: ['./test_dir/file1.txt', './test_dir/file3.pdf', './test_dir/subdir/file2.txt']
```

### `pprint`

```python
from src.utils.printer import pprint

def pprint(*args, **kwargs):
    """
    Печатает переданные аргументы в консоль, используя `rich.print`.

    Args:
        *args: Позиционные аргументы для печати.
        **kwargs: Именованные аргументы для `rich.print`.
    """
    ...
```

**Параметры**:
- `*args`: Позиционные аргументы, которые необходимо напечатать.
- `**kwargs`: Именованные аргументы, которые передаются в функцию `rich.print`.

**Как работает функция**:
1. Функция `pprint` принимает произвольное количество позиционных и именованных аргументов.
2. Она вызывает функцию `rich.print` с переданными аргументами, что позволяет печатать данные в консоль с использованием расширенного форматирования, предоставляемого библиотекой `rich`.

**Примеры**:
```python
from src.utils.printer import pprint

# Пример 1: Печать строки
pprint("Hello, world!")

# Пример 2: Печать списка
my_list = [1, 2, 3, 4, 5]
pprint(my_list)

# Пример 3: Печать словаря с отступами
my_dict = {"a": 1, "b": 2, "c": 3}
pprint(my_dict, indent=4)

# Пример 4: Печать с выделением цветом
pprint("[bold blue]This is a blue text[/bold blue]")
```
### Использование в коде

```python
import header
from src import gs
from src.utils.file import read_text_file, save_text_file, recursively_get_filepath
from src.utils.printer import pprint

images_path = recursively_get_filepath(gs.path.external_data / 'kazarinov' / 'converted_images' / 'pastel', ['*.jpeg','*.jpg','*.png'])
pprint(images_path)
...
```

**Описание**:
1.  Импортируются необходимые модули и функции.
2.  Формируется путь к директории с изображениями, используя переменные из модуля `gs`.
3.  Вызывается функция `recursively_get_filepath` для получения списка путей к изображениям с расширениями `.jpeg`, `.jpg` и `.png` в указанной директории.
4.  Полученный список путей выводится в консоль с использованием функции `pprint`.

```
Получение списка изображений
│
├── Формирование пути к директории с изображениями
│
├─── Получение списка путей к изображениям с помощью `recursively_get_filepath`
│
└─── Вывод списка путей к изображениям с помощью `pprint`