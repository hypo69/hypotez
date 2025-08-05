# Модуль `create_index_rst`

## Обзор

Модуль `create_index_rst` предназначен для автоматического создания файла `index.rst` в директории `docs` проекта. Этот файл используется для генерации документации с помощью Sphinx. Модуль рекурсивно обходит все поддиректории начиная с указанной, находит все файлы с расширением `.py` и добавляет их в `index.rst` в формате `toctree`.

## Подробней

Модуль предназначен для автоматизации процесса создания документации для Python-проектов. Он облегчает навигацию по модулям проекта, генерируя файл `index.rst`, который служит отправной точкой для документации Sphinx.

## Функции

### `create_index_rst`

```python
def create_index_rst(start_dir: str) -> None:
    """
    Recursively traverses all subdirectories from the start directory, reads all *.py files,
    and creates an index.rst file in the `docs` directory that lists all these files in a toctree format. Logs the process throughout.

    Args:
        start_dir (str): The root directory to start the traversal from.

    Returns:
        None

    Example:
        >>> create_index_rst(os.getcwd())
    """
```

**Назначение**: Рекурсивно обходит все поддиректории, начиная с указанной директории, находит все файлы `.py` и создает файл `index.rst` в директории `docs`, который содержит список всех этих файлов в формате `toctree`. Процесс логируется на каждом этапе.

**Параметры**:

- `start_dir` (str): Корневая директория, с которой начинается обход.

**Возвращает**:

- `None`

**Как работает функция**:

1.  **Определение путей**: Определяет пути к начальной директории (`start_path`), директории `docs` (`docs_dir`) и файлу `index.rst` (`index_file_path`).
2.  **Создание директории `docs`**: Если директория `docs` не существует, она создается.
3.  **Запись в файл `index.rst`**: Открывает файл `index.rst` для записи и записывает в него необходимые директивы `toctree` для Sphinx.
4.  **Обход директорий**: Рекурсивно обходит все поддиректории, начиная с `start_path`.
5.  **Поиск `.py` файлов**: В каждой директории ищет файлы с расширением `.py`.
6.  **Формирование путей модулей**: Для каждого найденного `.py` файла формирует путь к модулю относительно `start_path`.
7.  **Запись путей в `index.rst`**: Записывает пути к модулям в файл `index.rst` в формате, требуемом для `toctree`.
8.  **Логирование**: Логирует все основные этапы процесса, включая создание директории `docs`, открытие файла `index.rst`, обработку директорий и добавление файлов.

**Примеры**:

```python
import os
from pathlib import Path
from src.logger import logger
def create_index_rst(start_dir: str) -> None:
    """
    Recursively traverses all subdirectories from the start directory, reads all *.py files,
    and creates an index.rst file in the `docs` directory that lists all these files in a toctree format. Logs the process throughout.

    Args:
        start_dir (str): The root directory to start the traversal from.

    Returns:
        None

    Example:
        >>> create_index_rst(os.getcwd())
    """
    start_path = Path(start_dir)
    docs_dir = start_path / 'docs'
    index_file_path = docs_dir / 'index.rst'

    # Ensure the docs directory exists
    if not docs_dir.exists():
        docs_dir.mkdir(parents=True)
        logger.info(f"Created 'docs' directory at: {docs_dir}")

    logger.info(f"Starting to create index.rst in directory: {docs_dir}")

    try:
        with index_file_path.open('w') as index_file:
            logger.debug(f"Opening file for writing: {index_file_path}")
            index_file.write('.. toctree::\n')
            index_file.write('   :maxdepth: 2\n')
            index_file.write('   :caption: Содержание:\n\n')

            found_files = False
            for root, _, files in os.walk(start_path):
                py_files = [f for f in files if f.endswith('.py') and '(' not in f and ')' not in f]

                if py_files:
                    found_files = True
                    logger.info(f"Processing directory: {root}")
                    for py_file in py_files:
                        module_path = Path(root).relative_to(start_path).with_suffix('')  # Remove .py extension
                        index_file.write(f'   {module_path}\n')
                    index_file.write('\n')
                    logger.info(f"Added {len(py_files)} Python files from {root} to index.rst")

            if not found_files:
                logger.info("No Python files found in the specified directory.")

        logger.debug(f"Successfully wrote to file: {index_file_path}")

    except Exception as e:
        logger.error(f"An error occurred while creating index.rst: {e}")
        raise
import header
# Пример использования
if __name__ == "__main__":
    create_index_rst(Path(header.__root__, 'src'))
```

## Параметры

- `start_dir` (str): Корневая директория, с которой начинается обход. Используется для определения путей к файлам и директориям.

**Примеры**:

Вызов функции с указанием текущей рабочей директории:

```python
import os
create_index_rst(os.getcwd())
```

Использование `Path` объекта для указания директории:

```python
from pathlib import Path
create_index_rst(Path('/path/to/your/project'))