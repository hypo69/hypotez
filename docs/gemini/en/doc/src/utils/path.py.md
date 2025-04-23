# Модуль `src.utils.path`

## Обзор

Модуль `src.utils.path` предназначен для работы с путями в файловой системе. Он определяет функцию `get_relative_path`, которая позволяет получить относительный путь от заданного полного пути, начиная с определенного сегмента.

## Более подробно

Этот модуль упрощает работу с путями, особенно когда необходимо получить часть пути относительно известного сегмента. Это может быть полезно, например, для работы с конфигурационными файлами или при построении путей к ресурсам в проекте.

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
```

**Назначение**:
Функция `get_relative_path` извлекает относительный путь из полного пути, начиная с указанного сегмента.

**Параметры**:
- `full_path` (str): Полный путь к файлу или директории.
- `relative_from` (str): Сегмент пути, начиная с которого необходимо получить относительный путь.

**Возвращает**:
- `Optional[str]`: Относительный путь в виде строки, начиная с сегмента `relative_from`. Если сегмент `relative_from` не найден в `full_path`, возвращает `None`.

**Как работает функция**:
1. Преобразует входные строки `full_path` в объект `Path`.
2. Разбивает путь на отдельные сегменты.
3. Ищет индекс сегмента `relative_from` в списке сегментов.
4. Если сегмент `relative_from` найден, формирует новый путь, начиная с этого сегмента и до конца.
5. Возвращает полученный относительный путь в виде строки.
6. Если сегмент `relative_from` не найден, возвращает `None`.

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

Пример 1:
```python
full_path = "/home/user/project/src/utils/file.py"
relative_from = "src"
result = get_relative_path(full_path, relative_from)
print(result)  # Вывод: src/utils/file.py
```

Пример 2:
```python
full_path = "/home/user/project/src/utils/file.py"
relative_from = "project"
result = get_relative_path(full_path, relative_from)
print(result)  # Вывод: project/src/utils/file.py
```

Пример 3:
```python
full_path = "/home/user/project/src/utils/file.py"
relative_from = "nonexistent"
result = get_relative_path(full_path, relative_from)
print(result)  # Вывод: None
```
```