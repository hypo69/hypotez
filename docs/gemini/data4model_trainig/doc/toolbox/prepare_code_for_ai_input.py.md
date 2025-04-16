# Модуль для подготовки кода к вводу в AI

## Обзор

Этот модуль предназначен для сбора содержимого определенных файлов в директории `src`, сохранения их в единый текстовый файл для использования в качестве входных данных для моделей машинного обучения.

## Подробнее

Модуль предоставляет функциональность для рекурсивного обхода указанной директории, исключения нежелательных директорий и файлов, сбора содержимого оставшихся файлов с определенными расширениями и сохранения этого содержимого в один текстовый файл.

## Функции

### `collect_file_contents`

```python
def collect_file_contents(directory: Path, target_directory: Path) -> dict:
    """Рекурсивно собирает содержимое указанных файлов.

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
Рекурсивно собирает содержимое файлов из указанной директории и ее поддиректорий, фильтруя нежелательные файлы и директории.

**Параметры**:
- `directory` (Path): Путь к исходной директории для сканирования.
- `target_directory` (Path): Путь к директории для сохранения конечного текстового файла, предназначенного для ввода в модель машинного обучения.

**Возвращает**:
- `dict`: Словарь, где ключами являются пути к файлам, а значениями - содержимое файлов.

**Как работает функция**:
1. Создает пустой словарь `contents` для хранения содержимого файлов.
2. Перебирает все элементы (файлы и поддиректории) в указанной директории.
3. Если элемент является директорией:
    - Проверяет, не является ли имя директории одним из исключенных (`profiles`, `__pycache__`, `_experiments`) и не начинается ли с `___`, а также не содержит ли символ `*`.
    - Если директория не исключена, рекурсивно вызывает `collect_file_contents` для этой директории и обновляет словарь `contents` результатами рекурсивного вызова.
4. Если элемент является файлом:
    - Проверяет, имеет ли файл одно из разрешенных расширений (`.py`, `.json`, `.md`, `.dot`, `.mer`), не начинается ли его имя с `___`, и не содержит ли символ `*`, `(` или `)`.
    - Если файл соответствует условиям, открывает его, читает содержимое и сохраняет в словаре `contents` под ключом, соответствующим пути к файлу.
5. Возвращает словарь `contents`.

**Примеры**:

```python
from pathlib import Path

source_dir = Path("src")
target_dir = Path("output")
file_contents = collect_file_contents(source_dir, target_dir)
print(file_contents)
```

### `save_contents_to_text`

```python
def save_contents_to_text(contents: dict, output_file: Path):
    """Saves collected file contents to a single text file.

    Args:
        contents (dict): Dictionary with file paths as keys and file contents as values.
        output_file (Path): Path to the output text file for ML input.
    """
    ...
```

**Назначение**:
Сохраняет собранное содержимое файлов в один текстовый файл.

**Параметры**:
- `contents` (dict): Словарь, где ключами являются пути к файлам, а значениями - содержимое файлов.
- `output_file` (Path): Путь к выходному текстовому файлу для ввода в модель машинного обучения.

**Возвращает**:
- None

**Как работает функция**:
1. Открывает указанный файл `output_file` для записи.
2. Перебирает все элементы словаря `contents`.
3. Для каждого элемента записывает в файл путь к файлу, содержимое файла и разделитель (`"="*80`).

**Примеры**:

```python
from pathlib import Path

file_contents = {"file1.txt": "content of file1", "file2.txt": "content of file2"}
output_file = Path("output.txt")
save_contents_to_text(file_contents, output_file)
```

### `main`

```python
def main():
    """Main function to initiate content collection and save to a text file."""
    ...
```

**Назначение**:
Основная функция, которая запускает процесс сбора содержимого файлов и сохранения его в текстовый файл.

**Параметры**:
- None

**Возвращает**:
- None

**Как работает функция**:
1. Определяет путь к исходной директории (`src_directory`) как `src/utils` внутри корневого каталога проекта.
2. Определяет путь к директории для сохранения результата (`project_structure_directory`) как `prod` внутри исходной директории.
3. Создает директорию `prod`, если она не существует.
4. Вызывает функцию `collect_file_contents` для сбора содержимого файлов из исходной директории.
5. Определяет путь к выходному файлу (`output_file_path`) как `all_file_contents.txt` внутри директории для сохранения результата.
6. Вызывает функцию `save_contents_to_text` для сохранения собранного содержимого в текстовый файл.

**Примеры**:

```python
if __name__ == "__main__":
    main()
```

## Запуск

```python
if __name__ == "__main__":
    main()
```

При запуске этого скрипта будет вызвана функция `main`, которая соберет содержимое файлов из директории `src/utils`, сохранит их в файле `all_file_contents.txt` в директории `prod`.