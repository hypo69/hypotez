# Модуль `src.utils.path`

## Обзор

Модуль `src.utils.path` предоставляет функцию `get_relative_path` для получения относительного пути к файлу или директории, начиная с указанного сегмента пути. 

## Подробней

Этот модуль предназначен для определения корневого пути к проекту `hypotez`. Все импорты в проекте строятся относительно этого пути.

## Функции

### `get_relative_path`

```python
def get_relative_path(full_path: str, relative_from: str) -> Optional[str]:
    """
    Возвращает часть пути начиная с указанного сегмента и до конца.

    Args:
        full_path (str): Полный путь.
        relative_from (str): Сегмент пути, с которого нужно начать извлечение.

    Returns:
        Optional[str]: Относительный путь начиная с `relative_from`, или None, если сегмент не найден.
    """
    # Преобразуем строки в объекты Path
    path = Path(full_path)
    parts = path.parts

    # Находим индекс сегмента relative_from
    if relative_from in parts:
        start_index = parts.index(relative_from)
        # Формируем путь начиная с указанного сегмента
        relative_path = Path(*parts[start_index:])
        return relative_path.as_posix()
    else:
        return None

```

**Назначение**: Функция `get_relative_path` используется для получения относительного пути к файлу или директории, начиная с указанного сегмента пути.

**Параметры**:

- `full_path` (str): Полный путь к файлу или директории.
- `relative_from` (str): Сегмент пути, с которого нужно начать извлечение относительного пути.

**Возвращает**:

- `Optional[str]`: Относительный путь, начиная с `relative_from`, или `None`, если сегмент `relative_from` не найден в полном пути.


**Как работает функция**:

- Функция преобразует строки `full_path` и `relative_from` в объекты `Path`.
- Извлекает части пути (сегменты) из объекта `full_path`.
- Проверяет, существует ли сегмент `relative_from` в списке частей пути.
- Если сегмент найден, функция определяет индекс `start_index` этого сегмента в списке частей пути.
- Используя `start_index`, функция формирует новый путь, состоящий из частей пути, начиная с `start_index`.
- Возвращает полученный относительный путь в виде строки, используя метод `as_posix`.
- Если сегмент `relative_from` не найден, функция возвращает `None`.

**Примеры**:

```python
>>> get_relative_path("/home/user/project/src/utils/path.py", "project")
'project/src/utils/path.py'

>>> get_relative_path("/home/user/project/src/utils/path.py", "src")
'src/utils/path.py'

>>> get_relative_path("/home/user/project/src/utils/path.py", "utils")
'utils/path.py'

>>> get_relative_path("/home/user/project/src/utils/path.py", "nonexistent")
None
```

**Внутренние функции**:

Функция `get_relative_path` не использует внутренних функций.