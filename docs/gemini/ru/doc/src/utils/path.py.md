# Модуль для работы с путями в проекте
## Обзор

Модуль `src.utils.path` предоставляет утилиты для работы с путями к файлам и директориям в проекте. Он содержит функцию `get_relative_path`, которая позволяет получить относительный путь от заданного сегмента в полном пути.

## Подорбней

Этот модуль предназначен для упрощения работы с путями в проекте, позволяя динамически определять относительные пути на основе заданных сегментов. Это полезно, когда необходимо получить часть пути от определенной точки в структуре проекта.

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

**Назначение**: Функция `get_relative_path` извлекает часть пути, начиная с указанного сегмента `relative_from` до конца полного пути `full_path`.

**Параметры**:
- `full_path` (str): Полный путь к файлу или директории.
- `relative_from` (str): Сегмент пути, начиная с которого необходимо извлечь относительный путь.

**Возвращает**:
- `Optional[str]`: Относительный путь, начиная с сегмента `relative_from`, или `None`, если сегмент не найден в полном пути.

**Как работает функция**:

1. Преобразует входные строки `full_path` в объект `Path` для удобства работы с путями.
2. Разделяет полный путь на сегменты (части) с использованием `.parts`.
3. Проверяет, содержится ли сегмент `relative_from` в списке сегментов пути.
4. Если сегмент найден, определяет его индекс и формирует новый путь, начиная с этого индекса и до конца списка сегментов.
5. Преобразует полученный относительный путь в строку в формате POSIX и возвращает его.
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

```
Пример 1:
>>> full_path = "/Users/username/Documents/project/src/utils/path.py"
>>> relative_from = "src"
>>> get_relative_path(full_path, relative_from)
'src/utils/path.py'

Пример 2:
>>> full_path = "/Users/username/Documents/project/src/utils/path.py"
>>> relative_from = "project"
>>> get_relative_path(full_path, relative_from)
'project/src/utils/path.py'

Пример 3:
>>> full_path = "/Users/username/Documents/project/src/utils/path.py"
>>> relative_from = "nonexistent"
>>> get_relative_path(full_path, relative_from) is None
True
```
```ascii
Полный путь -> Преобразование в Path -> Разделение на сегменты -> Проверка наличия relative_from
    ↓
  relative_from найден?
  /       \
 Да        Нет
  ↓         ↓
Определение индекса -> Формирование относительного пути -> Преобразование в строку POSIX -> Возврат относительного пути   Возврат None