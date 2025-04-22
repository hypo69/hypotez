# Модуль `prepare_code_for_ai_input.py`

## Обзор

Модуль предназначен для сбора содержимого определенных файлов в директории `src`, сохранения их в один текстовый файл для использования в моделях машинного обучения. Исключаются определенные директории и файлы, включаются только файлы с расширениями `.py`, `.json`, `.md`, `.dot` и `.mer`.

## Подробней

Модуль выполняет рекурсивный обход указанной директории, фильтрует нежелательные директории и файлы, а затем собирает содержимое оставшихся файлов с указанными расширениями. Собранные данные сохраняются в один текстовый файл, который может быть использован в качестве входных данных для моделей машинного обучения.
Расположение файла в проекте: `/dev_utils/prepare_code_for_ai_input.py`.

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
```

**Назначение**: Рекурсивно собирает содержимое определенных файлов в указанной директории.

**Параметры**:

-   `directory` (Path): Путь к исходной директории для сканирования.
-   `target_directory` (Path): Путь к директории, в которой будет сохранен финальный текстовый файл для входных данных машинного обучения.

**Возвращает**:

-   `dict`: Словарь, где ключами являются пути к файлам, а значениями - содержимое файлов.

**Как работает функция**:

1.  Функция `collect_file_contents` рекурсивно обходит все элементы в указанной директории `directory`.
2.  Если элемент является директорией, проверяется, не входит ли её имя в список исключений (`profiles`, `__pycache__`, `_experiments`) и не начинается ли оно с `___`, а также не содержит ли символ `*`. Если директория не исключена, функция рекурсивно вызывает саму себя для этой директории.
3.  Если элемент является файлом, проверяется, имеет ли он одно из допустимых расширений (`.py`, `.json`, `.md`, `.dot`, `.mer`), не начинается ли его имя с `___`, не содержит ли символ `*` и символы `(` и `)`. Если файл соответствует критериям, его содержимое считывается и сохраняется в словаре `contents`, где ключом является путь к файлу.
4.  В конце функция возвращает словарь `contents`, содержащий пути к файлам и их содержимое.

```python
def save_contents_to_text(contents: dict, output_file: Path):
    """ Saves collected file contents to a single text file.

    Args:
        contents (dict): Dictionary with file paths as keys and file contents as values.
        output_file (Path): Path to the output text file for ML input.

    """
```

**Назначение**: Сохраняет собранное содержимое файлов в один текстовый файл.

**Параметры**:

-   `contents` (dict): Словарь, где ключами являются пути к файлам, а значениями - содержимое файлов.
-   `output_file` (Path): Путь к выходному текстовому файлу для входных данных машинного обучения.

**Как работает функция**:

1.  Функция `save_contents_to_text` открывает файл, указанный в параметре `output_file`, для записи.
2.  Перебирает элементы словаря `contents`, где ключом является путь к файлу, а значением - его содержимое.
3.  Для каждого файла записывает в выходной файл строку `File: {path}\n`, затем содержимое файла, и, наконец, разделитель в виде 80 символов `=`.

```python
def main():
    """ Main function to initiate content collection and save to a text file."""
```

**Назначение**: Главная функция, инициирующая сбор содержимого и сохранение в текстовый файл.

**Как работает функция**:

1.  Определяет путь к исходной директории `src_directory` и директории для сохранения результатов `project_structure_directory`.
2.  Создает директорию `prod` внутри `src_directory`, если она не существует.
3.  Вызывает функцию `collect_file_contents` для сбора содержимого файлов из `src_directory`.
4.  Определяет путь к выходному файлу `output_file_path`.
5.  Вызывает функцию `save_contents_to_text` для сохранения собранного содержимого в текстовый файл.

### Внутренние функции:

В данном модуле нет внутренних функций.

**Примеры**:

```python
# Пример использования функций
from pathlib import Path

# Определение путей к директориям и файлам
src_directory = Path("./src")
target_directory = Path("./target")
output_file = Path("./output.txt")

# Сбор содержимого файлов
contents = collect_file_contents(src_directory, target_directory)

# Сохранение содержимого в файл
save_contents_to_text(contents, output_file)

# Пример структуры содержимого файлов
# contents = {
#     "file1.py": "Содержимое file1.py",
#     "file2.json": "Содержимое file2.json"
# }