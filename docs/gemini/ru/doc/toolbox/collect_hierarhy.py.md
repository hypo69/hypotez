# Модуль для сбора иерархии файлов и их копирования

## Обзор

Модуль предназначен для рекурсивного сбора иерархии файлов из указанной директории (`src/utils`) и их копирования в другую директорию (`prod`) с сохранением структуры. Он также создает JSON-файл (`file_hierarchy.json`) с иерархией файлов.

## Подробнее

Этот модуль используется для создания структуры файлов проекта и её сохранения в формате JSON. Он позволяет автоматически собрать информацию о файлах определенных типов, игнорируя при этом ненужные директории и файлы. Это полезно для организации проекта, анализа зависимостей и создания документации.

## Классы

В данном модуле нет классов.

## Функции

### `collect_and_copy_files`

**Назначение**: Рекурсивно обходит указанную директорию, собирает иерархию файлов и копирует их в целевую директорию.

```python
def collect_and_copy_files(directory: Path, target_directory: Path) -> dict:
    """
    Рекурсивно обходит указанную директорию, собирает иерархию файлов и копирует их в целевую директорию.

    Args:
        directory (Path): Путь к директории, которую необходимо обработать.
        target_directory (Path): Путь к директории, в которую будут скопированы файлы.

    Returns:
        dict: Словарь, представляющий иерархию файлов.

    """
```

**Параметры**:

- `directory` (Path): Путь к директории, которую необходимо обработать.
- `target_directory` (Path): Путь к директории, в которую будут скопированы файлы.

**Возвращает**:

- `dict`: Словарь, представляющий иерархию файлов. Ключами словаря являются имена файлов и поддиректорий, а значениями - либо `None` (для файлов), либо рекурсивно построенные словари (для директорий).

**Как работает функция**:

1.  Инициализируется пустой словарь `hierarchy`, который будет хранить структуру файлов и папок.
2.  Функция итерируется по всем элементам (файлам и поддиректориям) в указанной директории `directory` с использованием `directory.iterdir()`.
3.  Для каждого элемента проверяется, является ли он директорией (`item.is_dir()`). Если да, то выполняется проверка, чтобы исключить определенные папки (`profiles`, `__pycache__`, `_experiments`) и папки, начинающиеся с `___`, а также содержащие символ `*` в имени.
4.  Если элемент является допустимой директорией, вызывается рекурсивный вызов `collect_and_copy_files` для этой директории, и результат добавляется в словарь `hierarchy` под ключом имени директории.
5.  Если элемент не является директорией, проверяется, является ли он файлом с одним из допустимых расширений (`.py`, `.json`, `.md`, `.dot`, `.mer`) и не начинается ли его имя с `___`, не содержит ли символы `*`, `(` или `)` в имени.
6.  Если файл соответствует критериям, его имя добавляется в словарь `hierarchy` с значением `None`. Затем формируется путь к целевому файлу `target_file_path` в целевой директории `target_directory`.
7.  Создаются все необходимые родительские директории для `target_file_path` с помощью `target_file_path.parent.mkdir(parents=True, exist_ok=True)`.
8.  Файл копируется из исходной директории в целевую с использованием `copy2(item, target_file_path)`. Функция `copy2` сохраняет метаданные файла.
9.  После обработки всех элементов директории, функция возвращает словарь `hierarchy`, представляющий структуру файлов и папок.

**Примеры**:

```python
from pathlib import Path

# Пример вызова функции
directory = Path("./src/utils")
target_directory = Path("./prod")
file_hierarchy = collect_and_copy_files(directory, target_directory)
print(file_hierarchy)
```

### `main`

**Назначение**: Устанавливает исходную директорию и директорию для сохранения результатов, вызывает функцию сбора и копирования файлов и сохраняет иерархию в JSON-файл.

```python
def main():
    """
    Устанавливает исходную директорию и директорию для сохранения результатов,
    вызывает функцию сбора и копирования файлов и сохраняет иерархию в JSON-файл.
    """
```

**Как работает функция**:

1.  Определяет исходную директорию `src_directory` как `src/utils`, используя `header.__root__` для получения корневого пути проекта.
2.  Определяет директорию для сохранения результатов `project_structure_directory` как поддиректорию `prod` внутри `src_directory`.
3.  Вызывает функцию `collect_and_copy_files` для сбора иерархии файлов и их копирования из `src_directory` в `project_structure_directory`. Результат сохраняется в переменной `file_hierarchy`.
4.  Определяет путь для сохранения JSON-файла с иерархией как `file_hierarchy.json` внутри `project_structure_directory`.
5.  Использует функцию `j_dumps` (из модуля `src.utils.jjson`) для сохранения словаря `file_hierarchy` в JSON-файл по пути `json_output_path`.

**Примеры**:

```python
# Пример вызова функции main
main()
```
```python
from pathlib import Path
from shutil import copy2
from src.utils.jjson import j_dumps

def collect_and_copy_files(directory: Path, target_directory: Path) -> dict:
    hierarchy = {}
    for item in directory.iterdir():
        if item.is_dir():
            if item.name not in ['profiles', '__pycache__', '_experiments'] and not item.name.startswith('___') and '*' not in item.name:
                hierarchy[item.name] = collect_and_copy_files(item, target_directory / item.name)
        else:
            if (item.suffix in ['.py', '.json', '.md', '.dot', '.mer']) and not item.name.startswith('___') and '*' not in item.name and '(' not in item.name and ')' not in item.name:
                hierarchy[item.name] = None
                target_file_path = target_directory / item.name
                target_file_path.parent.mkdir(parents=True, exist_ok=True)
                copy2(item, target_file_path)
    return hierarchy

def main():
    src_directory = Path('./src/utils')
    project_structure_directory = Path('./prod')  # Создаем папку 'prod'
    file_hierarchy = collect_and_copy_files(src_directory, project_structure_directory)
    json_output_path = Path('./prod/file_hierarchy.json')
    j_dumps(file_hierarchy, json_output_path)

if __name__ == "__main__":
    main()
```
## Параметры класса

В данном модуле нет классов и параметров класса.

## Методы класса

В данном модуле нет классов и методов класса.