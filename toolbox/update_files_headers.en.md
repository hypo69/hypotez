# Модуль для обновления заголовков файлов в проекте "hypotez"

## Обзор

Этот скрипт предназначен для обработки Python-файлов в проекте "hypotez". Он добавляет или заменяет заголовки, строки интерпретатора и документацию модуля в исходном коде. Скрипт обходит все файлы в проекте и обновляет их, добавляя информацию о проекте, детали интерпретатора и метаданные.

## Подробнее

Скрипт выполняет следующие задачи:

- Определяет корневую папку проекта.
- Находит и добавляет строку кодировки.
- Добавляет строки интерпретатора для Windows и Linux.
- Добавляет строку документации модуля.
- Устанавливает значение режима для проекта.

## Использование

### Стандартный запуск

Обрабатывает все файлы в проекте:

```bash
python update_files_headers.py
```

### Принудительное обновление файлов

Принудительно обновляет файлы, даже если заголовки уже существуют:

```bash
python update_files_headers.py --force-update
```

### Указание конкретного каталога проекта

Обрабатывает файлы в указанном каталоге проекта:

```bash
python update_files_headers.py -p /путь/к/проекту
```

### Исключение каталога "venv"

Исключает каталог `venv` из обработки:

```bash
python update_files_headers.py --exclude-venv
```

## Принцип работы скрипта

1. **Поиск корня проекта**
   Скрипт ищет корень проекта, начиная с текущего каталога. Если корень проекта не найден, возникает ошибка.

2. **Добавление/замена заголовков**
   Для каждого Python-файла скрипт:
   - Добавляет строку кодировки `# -*- coding: utf-8 -*-`, если она отсутствует.
   - Добавляет строки интерпретатора для Windows и Linux (в зависимости от операционной системы).
   - Добавляет строку документации модуля, если она отсутствует.
   - Устанавливает переменную `MODE`, если она отсутствует.

3. **Режимы обновления**
   - В обычном режиме обновления (когда `force-update` не установлен), заголовки добавляются только если они отсутствуют.
   - В режиме `--force-update`, заголовки и строки интерпретатора обновляются, даже если они уже существуют в файле.

4. **Исключение папок**
   Папки, такие как `venv`, `tmp`, `docs`, `data` и другие каталоги, указанные в переменной `EXCLUDE_DIRS`, исключаются из обработки.

## Зависимости

Скрипт использует стандартные библиотеки Python:

- `os`
- `argparse`
- `pathlib`
- `sys`
- `platform`

Убедитесь, что Python и зависимости установлены, если это требуется для вашей среды.

## Пример кода

Вот пример Python-кода для добавления/замены заголовков:

```python
def add_or_replace_file_header(file_path: str, project_root: Path, force_update: bool):
    """Добавляет или заменяет заголовок, строки интерпретатора и docstring модуля в указанном Python-файле."""
    # Логика для добавления заголовков и интерпретаторов...
```

Этот скрипт полезен для автоматической настройки заголовков файлов в крупных проектах, обеспечивая стандартизированную структуру и метаданные в исходных файлах.

## Функции

### `add_or_replace_file_header`

```python
def add_or_replace_file_header(file_path: str, project_root: Path, force_update: bool):
    """Добавляет или заменяет заголовок, строки интерпретатора и docstring модуля в указанном Python-файле."""
    # Логика для добавления заголовков и интерпретаторов...
```

**Назначение**: Добавляет или заменяет заголовок, строки интерпретатора и docstring модуля в указанном Python-файле.

**Параметры**:
- `file_path` (str): Путь к файлу, в котором нужно добавить или заменить заголовок.
- `project_root` (Path): Корневой путь проекта.
- `force_update` (bool): Флаг, указывающий, следует ли принудительно обновить заголовок, даже если он уже существует.

**Возвращает**:
- `None`

**Как работает функция**:
- Функция выполняет добавление или замену заголовка файла, строк интерпретатора и docstring модуля в Python-файле.

**Примеры**:

```python
file_path = 'example.py'
project_root = Path('.')
force_update = True
add_or_replace_file_header(file_path, project_root, force_update)