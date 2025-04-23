# Module src.endpoints.hypo69.code_assistant.make_summary

## Обзор

Модуль собирает файл `SUMMARY.md` для компиляции средствами `mdbook`.
Подробнее: https://chatgpt.com/share/6742f054-aaa0-800d-9f84-0ab035a2a2c2

## Более подробная информация

Этот модуль предназначен для автоматического создания файла `SUMMARY.md`, который используется инструментом `mdbook` для генерации структуры книги.
Он рекурсивно обходит указанную директорию (`src_dir`), находит все файлы с расширением `.md` и добавляет их в файл `SUMMARY.md` в формате, необходимом для `mdbook`.
Также реализована фильтрация файлов по языку (`ru` или `en`) на основе суффикса в имени файла.
Файл `SUMMARY.md` создается в директории `docs`, которая является аналогом `src`, но предназначена для хранения сгенерированной документации.

## Classes

В данном модуле классы отсутствуют.

## Functions

### `make_summary`

```python
def make_summary(docs_dir: Path, lang: str = 'en') -> None:
    """
    Создает файл SUMMARY.md, рекурсивно обходя папку.

    Args:
        docs_dir (Path): Путь к исходной директории 'src'.
        lang (str): Язык фильтрации файлов. Возможные значения: 'ru' или 'en'.
    """
```

**Описание**: Создает файл `SUMMARY.md`, рекурсивно обходя указанную папку.

**Параметры**:
- `docs_dir` (Path): Путь к исходной директории `'src'`.
- `lang` (str): Язык фильтрации файлов. Возможные значения: `'ru'` или `'en'`. По умолчанию `'en'`.

**Возвращает**:
- `None`: Функция ничего не возвращает.

**Как работает функция**:
1. Функция формирует путь к файлу `SUMMARY.md`, вызывая `prepare_summary_path`.
2. Создает родительские директории для файла `SUMMARY.md`, если они не существуют.
3. Вызывает функцию `_make_summary` для фактического создания и записи содержимого в файл `SUMMARY.md`.

**Примеры**:

Пример вызова функции:
```python
from pathlib import Path
from src.endpoints.hypo69.code_assistant.make_summary import make_summary

docs_dir = Path('./src')
lang = 'ru'
make_summary(docs_dir, lang)
```

### `_make_summary`

```python
def _make_summary(src_dir: Path, summary_file: Path, lang: str = 'en') -> bool:
    """
    Рекурсивно обходит папку и создает файл SUMMARY.md с главами на основе .md файлов.

    Args:
        src_dir (Path): Путь к папке с исходниками .md.
        summary_file (Path): Путь для сохранения файла SUMMARY.md.
        lang (str): Язык фильтрации файлов. Возможные значения: 'ru' или 'en'.
    """
```

**Описание**: Рекурсивно обходит папку и создает файл `SUMMARY.md` с главами на основе `.md` файлов.

**Параметры**:
- `src_dir` (Path): Путь к папке с исходниками `.md`.
- `summary_file` (Path): Путь для сохранения файла `SUMMARY.md`.
- `lang` (str): Язык фильтрации файлов. Возможные значения: `'ru'` или `'en'`. По умолчанию `'en'`.

**Возвращает**:
- `bool`: `True`, если файл успешно создан, `False` в случае ошибки.

**Как работает функция**:
1. Проверяет, существует ли уже файл `SUMMARY.md`, и выводит сообщение, если он будет перезаписан.
2. Открывает файл `SUMMARY.md` для записи с кодировкой `utf-8`.
3. Записывает заголовок `# Summary\n\n` в файл.
4. Рекурсивно обходит все файлы с расширением `.md` в директории `src_dir`.
5. Пропускает файл `SUMMARY.md`, чтобы избежать рекурсии.
6. Фильтрует файлы по языку:
   - Если `lang == 'ru'`, пропускает файлы, не заканчивающиеся на `.ru.md`.
   - Если `lang == 'en'`, пропускает файлы, заканчивающиеся на `.ru.md`.
7. Формирует относительный путь к файлу относительно родительской директории `src_dir`.
8. Записывает строку в файл `SUMMARY.md` в формате `'- [{path.stem}]({relative_path.as_posix()})\n'`, где `path.stem` - имя файла без расширения, а `relative_path.as_posix()` - относительный путь к файлу.

**Примеры**:

Пример вызова функции:
```python
from pathlib import Path
from src.endpoints.hypo69.code_assistant.make_summary import _make_summary

src_dir = Path('./src')
summary_file = Path('./docs/SUMMARY.md')
lang = 'ru'
result = _make_summary(src_dir, summary_file, lang)
print(result)
```

### `prepare_summary_path`

```python
def prepare_summary_path(src_dir: Path, file_name: str = 'SUMMARY.md') -> Path:
    """
    Формирует путь к файлу, заменяя часть пути 'src' на 'docs' и добавляя имя файла.

    Args:
        src_dir (Path): Исходный путь с 'src'.
        file_name (str): Имя файла, который нужно создать. По умолчанию 'SUMMARY.md'.

    Returns:
        Path: Новый путь к файлу.
    """
```

**Описание**: Формирует путь к файлу, заменяя часть пути `'src'` на `'docs'` и добавляя имя файла.

**Параметры**:
- `src_dir` (Path): Исходный путь с `'src'`.
- `file_name` (str): Имя файла, который нужно создать. По умолчанию `'SUMMARY.md'`.

**Возвращает**:
- `Path`: Новый путь к файлу.

**Как работает функция**:
1. Формирует новый путь, заменяя часть пути `'src'` на `'docs'`.
2. Добавляет имя файла к новому пути.
3. Возвращает новый путь к файлу.

**Примеры**:

Пример вызова функции:
```python
from pathlib import Path
from src.endpoints.hypo69.code_assistant.make_summary import prepare_summary_path

src_dir = Path('./src')
file_name = 'SUMMARY.md'
result = prepare_summary_path(src_dir, file_name)
print(result)
```

## Class Parameters

В данном модуле нет параметров класса.