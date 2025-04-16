### Анализ кода модуля `hypotez/src/utils/path.py`

## Обзор

Этот модуль предназначен для определения корневого пути к проекту и предоставляет функцию для получения относительного пути. Все импорты строятся относительно корневого пути.

## Подробнее

Модуль содержит функцию `get_relative_path`, которая позволяет извлекать часть пути, начиная с указанного сегмента. Это полезно для работы с файловой системой и формирования путей относительно корня проекта.

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
    ...
```

**Назначение**:
Возвращает часть пути, начиная с указанного сегмента и до конца.

**Параметры**:
- `full_path` (str): Полный путь.
- `relative_from` (str): Сегмент пути, с которого нужно начать извлечение.

**Возвращает**:
- `Optional[str]`: Относительный путь, начиная с `relative_from`, или None, если сегмент не найден.

**Как работает функция**:
1. Преобразует строки `full_path` и `relative_from` в объекты `Path`.
2. Получает части пути с помощью `path.parts`.
3. Находит индекс сегмента `relative_from` в частях пути.
4. Если сегмент найден, формирует новый путь, начиная с указанного сегмента, и возвращает его в формате POSIX.
5. Если сегмент не найден, возвращает None.

**Примеры**:

```python
from pathlib import Path
full_path = "/path/to/my/project/src/module.py"
relative_from = "src"
relative_path = get_relative_path(full_path, relative_from)
print(relative_path)  # Вывод: src/module.py
```

## Переменные

Отсутствуют

## Запуск

Для использования данного модуля необходимо импортировать функцию `get_relative_path` из модуля `src.utils.path`.

```python
from src.utils.path import get_relative_path
from pathlib import Path

full_path = "/path/to/my/project/src/module.py"
relative_from = "src"
relative_path = get_relative_path(full_path, relative_from)
print(relative_path)
```