# Модуль `src.utils.path`

## Обзор

Модуль определяет корневой путь к проекту. Все импорты строятся относительно этого пути. Это обеспечивает удобство и консистентность при работе с путями в рамках проекта.

## Подробней

Этот модуль содержит функцию `get_relative_path`, которая позволяет получить относительный путь, начиная с определенного сегмента полного пути.
Это полезно, когда необходимо выделить часть пути, основываясь на известном сегменте (например, корневой директории проекта).

## Функции

### `get_relative_path`

**Назначение**: Возвращает часть пути начиная с указанного сегмента и до конца.

**Параметры**:
- `full_path` (str): Полный путь к файлу или директории.
- `relative_from` (str): Сегмент пути, с которого нужно начать извлечение относительного пути.

**Возвращает**:
- `Optional[str]`: Относительный путь, начиная с сегмента `relative_from`, или `None`, если сегмент не найден.

**Как работает функция**:
1. Функция принимает полный путь `full_path` и сегмент `relative_from`, начиная с которого необходимо извлечь относительный путь.
2. Полный путь преобразуется в объект `Path` для удобства работы.
3. Путь разбивается на сегменты (части).
4. Проверяется, содержится ли сегмент `relative_from` в списке сегментов пути.
5. Если сегмент найден, определяется его индекс.
6. Формируется новый путь, начиная с найденного индекса и до конца списка сегментов.
7. Полученный относительный путь преобразуется в строку в формате POSIX и возвращается.
8. Если сегмент `relative_from` не найден, функция возвращает `None`.

**Примеры**:

```python
from pathlib import Path
from typing import Optional

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

**Пример 1**:
```python
full_path = "/home/user/project/src/utils/file.txt"
relative_from = "src"
result = get_relative_path(full_path, relative_from)
print(result)  # Вывод: src/utils/file.txt
```

**Пример 2**:
```python
full_path = "/home/user/project/src/utils/file.txt"
relative_from = "project"
result = get_relative_path(full_path, relative_from)
print(result)  # Вывод: project/src/utils/file.txt
```

**Пример 3**:
```python
full_path = "/home/user/project/src/utils/file.txt"
relative_from = "nonexistent"
result = get_relative_path(full_path, relative_from)
print(result)  # Вывод: None