# Модуль для подготовки кода для ввода в AI

## Обзор

Модуль предназначен для сбора содержимого определенных файлов в директории `src`, сохранения их в один текстовый файл для использования в качестве входных данных для моделей машинного обучения. Он исключает определенные директории и файлы, и включает только файлы с расширениями `.py`, `.json`, `.md`, `.dot` и `.mer`.

## Подробнее

Этот модуль автоматизирует процесс сбора и подготовки данных из различных файлов проекта для использования в задачах машинного обучения. Он позволяет рекурсивно обходить директории, читать содержимое файлов, фильтровать их по расширению и имени, а затем объединять все содержимое в один выходной файл.

## Функции

### `collect_file_contents`

```python
def collect_file_contents(directory: Path, target_directory: Path) -> dict:
    """ Recursively collects the content of specific files.

    Traverses the specified `directory`, filters out unwanted directories and files,
    and collects the content of remaining files with specific extensions.

    Args:
        directory (Path): Path to the source directory to scan.
        target_directory (Path): Path to save the final text file for ML input.

    Returns:
        dict: A dictionary where keys are file paths and values are file contents.

    """
    ...
```

**Назначение**:
Рекурсивно собирает содержимое файлов с определенными расширениями из указанной директории и ее поддиректорий.

**Параметры**:

-   `directory` (Path): Путь к исходной директории для сканирования.
-   `target_directory` (Path): Путь к целевой директории для сохранения итогового текстового файла для ввода в модель машинного обучения.

**Возвращает**:

-   `dict`: Словарь, где ключами являются пути к файлам, а значениями - содержимое этих файлов.

**Как работает функция**:

1.  Инициализирует пустой словарь `contents` для хранения содержимого файлов.
2.  Перебирает все элементы (файлы и поддиректории) в указанной директории.
3.  Если элемент является директорией:

    *   Проверяет, не является ли имя директории одним из исключенных (`profiles`, `__pycache__`, `_experiments`), не начинается ли с `___`, и не содержит ли символ `*`.
    *   Если директория не исключена, рекурсивно вызывает `collect_file_contents` для этой директории и обновляет словарь `contents` результатами рекурсивного вызова.
4.  Если элемент является файлом:

    *   Проверяет, имеет ли файл одно из разрешенных расширений (`.py`, `.json`, `.md`, `.dot`, `.mer`), не начинается ли его имя с `___`, и не содержит ли символы `*`, `(` или `)`.
    *   Если файл соответствует условиям, открывает его в кодировке `utf-8`, читает содержимое и добавляет его в словарь `contents` под ключом, соответствующим пути к файлу.
5.  Возвращает словарь `contents`.

### `save_contents_to_text`

```python
def save_contents_to_text(contents: dict, output_file: Path):
    """ Saves collected file contents to a single text file.

    Args:
        contents (dict): Dictionary with file paths as keys and file contents as values.
        output_file (Path): Path to the output text file for ML input.

    """
    ...
```

**Назначение**:
Сохраняет собранное содержимое файлов в один текстовый файл.

**Параметры**:

-   `contents` (dict): Словарь, где ключами являются пути к файлам, а значениями - содержимое этих файлов.
-   `output_file` (Path): Путь к выходному текстовому файлу для ввода в модель машинного обучения.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Открывает файл, указанный в `output_file`, в режиме записи и кодировке `utf-8`.
2.  Перебирает все элементы в словаре `contents`.
3.  Для каждого элемента (путь к файлу и содержимое):

    *   Записывает в файл строку `File: {path}\n`, где `path` - путь к файлу.
    *   Записывает в файл содержимое файла.
    *   Записывает в файл разделитель `\n" + "="*80 + "\\n\\n"` для отделения содержимого одного файла от другого.

### `main`

```python
def main():
    """ Main function to initiate content collection and save to a text file."""
    ...
```

**Назначение**:
Основная функция, запускающая процесс сбора содержимого файлов и сохранения его в текстовый файл.

**Параметры**:

-   Отсутствуют.

**Возвращает**:

-   `None`

**Как работает функция**:

1.  Определяет путь к исходной директории (`src/utils`) и сохраняет его в переменной `src_directory`.
2.  Определяет путь к целевой директории (`src/utils/prod`) и сохраняет его в переменной `project_structure_directory`.
3.  Создает директорию `prod`, если она не существует.
4.  Вызывает функцию `collect_file_contents` для сбора содержимого файлов из исходной директории.
5.  Определяет путь к выходному файлу (`all_file_contents.txt`) и сохраняет его в переменной `output_file_path`.
6.  Вызывает функцию `save_contents_to_text` для сохранения содержимого файлов в выходной файл.

## Примеры

### Пример использования модуля

```python
from pathlib import Path
from dev_utils.prepare_code_for_ai_input import collect_file_contents, save_contents_to_text
import header

if __name__ == "__main__":
    src_directory = Path(header.__root__, 'src', 'utils')
    project_structure_directory = Path(src_directory, 'prod')
    project_structure_directory.mkdir(parents=True, exist_ok=True)  # Ensure the 'prod' folder exists

    # Collect contents of files
    file_contents = collect_file_contents(src_directory, project_structure_directory)
    
    # Save all contents to a single text file for ML
    output_file_path = Path(project_structure_directory, 'all_file_contents.txt')
    save_contents_to_text(file_contents, output_file_path)
```

Этот код выполняет следующие действия:

1.  Импортирует необходимые модули и функции.
2.  Определяет пути к исходной и целевой директориям.
3.  Создает целевую директорию, если она не существует.
4.  Вызывает функцию `collect_file_contents` для сбора содержимого файлов из исходной директории.
5.  Вызывает функцию `save_contents_to_text` для сохранения содержимого файлов в выходной файл.