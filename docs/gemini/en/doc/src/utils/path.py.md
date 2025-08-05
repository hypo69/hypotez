# Модуль `path`

## Обзор

Модуль `path` предоставляет функции для работы с путями к файлам и каталогам в проекте. 

## Подробности

Модуль `path` определяет корневой путь к проекту `hypotez`. Все импорты строятся относительно этого пути.

## Функции

### `get_relative_path`

**Purpose**: Эта функция извлекает часть пути к файлу или каталогу, начиная с заданного сегмента пути и до конца.

**Parameters**:

- `full_path` (str): Полный путь к файлу или каталогу.
- `relative_from` (str): Сегмент пути, с которого нужно начать извлечение.

**Returns**:

- `Optional[str]`: Относительный путь, начиная с `relative_from`, или `None`, если сегмент не найден.

**Raises Exceptions**:

- None

**How the Function Works**:

1. Функция преобразует строки `full_path` и `relative_from` в объекты `Path`.
2. Извлекает все сегменты пути из объекта `Path` для `full_path` и сохраняет их в списке `parts`.
3. Находит индекс сегмента `relative_from` в списке `parts`.
4. Если `relative_from` найден, функция создает новый объект `Path` из всех сегментов пути, начиная с `start_index` (индекс найденного сегмента) до конца списка.
5. Возвращает строковое представление нового объекта `Path` в виде относительного пути.
6. Если `relative_from` не найден, функция возвращает `None`.


**Examples**:

```python
>>> full_path = '/home/user/project/src/utils/path.py'
>>> relative_from = 'src'
>>> get_relative_path(full_path, relative_from)
'src/utils/path.py'

>>> full_path = '/home/user/project/src/utils/path.py'
>>> relative_from = 'project'
>>> get_relative_path(full_path, relative_from)
'project/src/utils/path.py'

>>> full_path = '/home/user/project/src/utils/path.py'
>>> relative_from = 'nonexistent'
>>> get_relative_path(full_path, relative_from)
None

```