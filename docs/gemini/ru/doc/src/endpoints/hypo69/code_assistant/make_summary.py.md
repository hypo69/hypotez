# Модуль для создания файла SUMMARY.md 

## Обзор

Модуль `make_summary`  собирает файл `summary.md` для компиляции средствами `mdbook`.  Он рекурсивно обходит папку с исходными `.md`-файлами и создает файл `SUMMARY.md` с главами на основе найденных `.md`-файлов.

## Подробнее

Модуль предназначен для удобства создания оглавления (файла `SUMMARY.md`)  для проекта `hypotez`,  который использует инструмент `mdbook` для генерации документации.  

Файл `SUMMARY.md`  используется  `mdbook` для формирования оглавления проекта.  Он содержит  список глав документации,  каждая из которых соответствует  `md`-файлу  в исходной директории проекта.  

## Классы
**Классы в модуле отсутствуют.**

## Функции

### `make_summary`

**Назначение**:
- Создает файл `SUMMARY.md` с  относительными  путями  к  файлам  в  папке `src`  с учетом языка.

**Параметры**:
- `docs_dir` (Path): Путь к  директории `src`  в проекте `hypotez`.
- `lang` (str): Язык фильтрации файлов.  Возможные  значения:  `ru`  или `en`.  По умолчанию  `en`.

**Возвращает**:
- `None`:  Функция  не  возвращает  значения.

**Как работает функция**:
- Функция `make_summary`  использует  вспомогательную  функцию `prepare_summary_path`  для  формирования  пути  к  файлу `SUMMARY.md` в  директории `docs`  проекта.
- Далее,  функция  `_make_summary`  рекурсивно  обходит  папку  `docs_dir`  и  записывает  в  `summary_file`  список  глав  в  формате `mdbook`.
- Для  каждого  `.md`-файла  в  папке  `docs_dir`  функция  записывает  строку  в  `summary_file`.
- Формат  строки  в  `summary_file`: `- [Название главы](Относительный путь к файлу.md)`.

**Примеры**:
```python
from pathlib import Path
import make_summary

# Создаем файл SUMMARY.md  для  русских  файлов
make_summary.make_summary(docs_dir=Path('/path/to/hypotez/src'), lang='ru')

# Создаем файл SUMMARY.md  для  английских  файлов
make_summary.make_summary(docs_dir=Path('/path/to/hypotez/src'), lang='en')

```
### `_make_summary`

**Назначение**:
- Рекурсивно обходит папку и создает файл `SUMMARY.md` с  главами  на  основе  `.md`  файлов,  с учетом языка.

**Параметры**:
- `src_dir` (Path): Путь к  папке  с  исходниками  `.md`.
- `summary_file` (Path): Путь  для  сохранения  файла  `SUMMARY.md`.
- `lang` (str): Язык  фильтрации  файлов.  Возможные  значения:  `ru`  или `en`.  По умолчанию `en`.

**Возвращает**:
- `bool`:  `True`,  если  файл  `SUMMARY.md`  был  создан  успешно,  `False`  в  случае  ошибки.

**Как работает функция**:
- Функция  `_make_summary`  рекурсивно  обходит  папку  `src_dir`  и  записывает  в  `summary_file`  список  глав  в  формате  `mdbook`.
- Для  каждого  `.md`-файла  в  папке  `src_dir`  функция  записывает  строку  в  `summary_file`.
- Формат  строки  в  `summary_file`: `- [Название главы](Относительный путь к файлу.md)`.
- Функция  использует  условие  `if lang == 'ru' and not path.name.endswith('.ru.md'):`  для  фильтрации  файлов  по  языку.
-  Функция  использует  условие  `if lang == 'en' and path.name.endswith('.ru.md'):`  для  фильтрации  файлов  по  языку.
- Функция  использует  `summary.write(f'- [{path.stem}]({relative_path.as_posix()})\\n\')`  для  записи  строки  в  файл  `summary_file`.

**Примеры**:
```python
from pathlib import Path
import make_summary

# Создаем файл SUMMARY.md  для  русских  файлов
make_summary._make_summary(src_dir=Path('/path/to/hypotez/src'), summary_file=Path('/path/to/hypotez/docs/SUMMARY.md'), lang='ru')

# Создаем файл SUMMARY.md  для  английских  файлов
make_summary._make_summary(src_dir=Path('/path/to/hypotez/src'), summary_file=Path('/path/to/hypotez/docs/SUMMARY.md'), lang='en')

```
### `prepare_summary_path`

**Назначение**:
- Формирует  путь  к  файлу,  заменяя  часть  пути  `src`  на  `docs`  и  добавляя  имя  файла.

**Параметры**:
- `src_dir` (Path):  Исходный  путь  с `src`.
- `file_name` (str):  Имя  файла,  который  нужно  создать.  По  умолчанию  `SUMMARY.md`.

**Возвращает**:
- `Path`:  Новый  путь  к  файлу.

**Как работает функция**:
- Функция  `prepare_summary_path`  получает  в  качестве  аргумента  путь  к  папке `src`  и  имя  файла.
- Далее  она  заменяет  `src`  на  `docs`  в  пути  и  добавляет  имя  файла.
-  Результат  возвращается  в  виде  объекта  `Path`.


**Примеры**:
```python
from pathlib import Path
import make_summary

# Формируем  путь  к  файлу  SUMMARY.md  в  директории  docs
summary_file = make_summary.prepare_summary_path(src_dir=Path('/path/to/hypotez/src'), file_name='SUMMARY.md')

# Вывод  пути  к  файлу
print(summary_file)

```

## Параметры класса
**В модуле нет классов, поэтому параметров класса нет.**

## Примеры

**Примеры вызова функции `make_summary`**:
```python
from pathlib import Path
import make_summary

# Создаем  файл  SUMMARY.md  для  русских  файлов
make_summary.make_summary(docs_dir=Path('/path/to/hypotez/src'), lang='ru')

# Создаем  файл  SUMMARY.md  для  английских  файлов
make_summary.make_summary(docs_dir=Path('/path/to/hypotez/src'), lang='en')
```
```markdown