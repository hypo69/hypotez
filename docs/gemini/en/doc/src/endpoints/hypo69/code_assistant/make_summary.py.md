# Модуль `make_summary`

## Обзор

Модуль `make_summary` предназначен для создания файла `SUMMARY.md`, который используется для компиляции документации проекта с помощью `mdbook`. Модуль рекурсивно обходит заданную директорию, собирая информацию о .md файлах и формируя список глав для документации.

## Детали

Модуль `make_summary` позволяет создавать файлы `SUMMARY.md` для разных языков, фильтруя .md файлы по суффиксу (`.ru.md` для русского языка). 

##  Функции

### `make_summary(docs_dir: Path, lang: str = 'en') -> None`

**Описание:**

Функция создает файл `SUMMARY.md` в директории `docs` проекта, рекурсивно обходя заданную директорию `docs_dir` и формируя список глав на основе .md файлов. 

**Параметры:**

- `docs_dir` (Path): Путь к исходной директории `src` проекта.
- `lang` (str): Язык фильтрации файлов. Возможные значения: `ru` или `en`. 

**Возвращает:**

- `None`

**Пример:**

```python
from pathlib import Path
from src.endpoints.hypo69.code_assistant.make_summary import make_summary

docs_dir = Path('./src')  # Задаем путь к директории `src` 
make_summary(docs_dir, lang='en')  # Создаем файл `SUMMARY.md` для английской документации 
```

### `_make_summary(src_dir: Path, summary_file: Path, lang: str = 'en') -> bool`

**Описание:**

Рекурсивно обходит заданную директорию `src_dir`, формируя список глав для документации и записывая его в файл `summary_file`.

**Параметры:**

- `src_dir` (Path): Путь к папке с .md файлами.
- `summary_file` (Path): Путь к файлу `SUMMARY.md` для записи.
- `lang` (str): Язык фильтрации файлов. Возможные значения: `ru` или `en`.

**Возвращает:**

- `bool`: `True`, если файл `SUMMARY.md` создан успешно, `False` в случае ошибки.

**Пример:**

```python
from pathlib import Path
from src.endpoints.hypo69.code_assistant.make_summary import _make_summary

src_dir = Path('./src')  # Задаем путь к директории `src` 
summary_file = Path('./docs/SUMMARY.md')  # Задаем путь к файлу `SUMMARY.md`
_make_summary(src_dir, summary_file, lang='en')  # Создаем файл `SUMMARY.md` для английской документации 
```

### `prepare_summary_path(src_dir: Path, file_name: str = 'SUMMARY.md') -> Path`

**Описание:**

Формирует путь к файлу `SUMMARY.md` в директории `docs`, заменяя часть пути `src` на `docs` и добавляя имя файла.

**Параметры:**

- `src_dir` (Path): Исходный путь с `src`.
- `file_name` (str): Имя файла, которое нужно создать. По умолчанию `SUMMARY.md`.

**Возвращает:**

- `Path`: Новый путь к файлу.

**Пример:**

```python
from pathlib import Path
from src.endpoints.hypo69.code_assistant.make_summary import prepare_summary_path

src_dir = Path('./src')  # Задаем путь к директории `src` 
file_name = 'SUMMARY.md'  # Задаем имя файла
prepare_summary_path(src_dir, file_name)  # Формируем путь к файлу `SUMMARY.md` 
```

## Примеры

**Пример 1: Создание файла `SUMMARY.md` для русской документации**

```python
from src.endpoints.hypo69.code_assistant.make_summary import make_summary

docs_dir = Path('./src')
make_summary(docs_dir, lang='ru')  # Создаем файл `SUMMARY.md` для русской документации
```

**Пример 2: Создание файла `SUMMARY.md` для английской документации с использованием `_make_summary`**

```python
from pathlib import Path
from src.endpoints.hypo69.code_assistant.make_summary import _make_summary

src_dir = Path('./src')
summary_file = Path('./docs/SUMMARY.md')
_make_summary(src_dir, summary_file, lang='en')  # Создаем файл `SUMMARY.md` для английской документации 
```

## Дополнительная информация

- Модуль использует модуль `header` для определения корневого пути проекта.
- Функция `_make_summary` выполняет рекурсивный обход директории с помощью `src_dir.rglob('*.md')`.
- Фильтрация файлов по языку осуществляется с помощью проверки имени файла на наличие суффикса `.ru.md`.

**Важно:**

- Используйте этот модуль для создания файлов `SUMMARY.md` для разных языков документации.
- Проверьте, что пути к исходным директориям и к файлу `SUMMARY.md` заданы верно.