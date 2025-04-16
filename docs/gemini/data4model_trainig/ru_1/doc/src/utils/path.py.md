# Модуль `src.utils.path`

## Обзор

Модуль `src.utils.path` предназначен для определения и работы с путями в проекте. Он содержит функции для получения относительных путей на основе заданного сегмента пути.

## Подробней

Этот модуль предоставляет инструменты для управления путями к файлам и каталогам в проекте. Он позволяет извлекать относительные пути, что упрощает работу с файловой системой и обеспечивает переносимость кода между различными средами.
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

Функция `get_relative_path` извлекает относительный путь из полного пути, начиная с указанного сегмента. Если указанный сегмент не найден в полном пути, функция возвращает `None`.

**Параметры**:

- `full_path` (str): Полный путь к файлу или каталогу.
- `relative_from` (str): Сегмент пути, начиная с которого необходимо извлечь относительный путь.

**Возвращает**:

- `Optional[str]`: Относительный путь, начиная с `relative_from`, или `None`, если сегмент не найден.

**Как работает функция**:

1.  Функция преобразует входные строки `full_path` и `relative_from` в объекты `Path` для удобства работы с путями.
2.  Затем она разбивает полный путь на отдельные компоненты (сегменты).
3.  Функция проверяет, содержится ли `relative_from` в списке компонентов пути.
4.  Если `relative_from` найден, определяется индекс этого сегмента.
5.  Используя этот индекс, формируется новый путь, включающий все сегменты, начиная с `relative_from` и до конца полного пути.
6.  Этот новый путь преобразуется в строку в формате POSIX и возвращается.
7.  Если `relative_from` не найден в полном пути, функция возвращает `None`.

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

```python
# Пример 1: Извлечение относительного пути
full_path = "/home/user/project/src/utils/file.txt"
relative_from = "src"
relative_path = get_relative_path(full_path, relative_from)
print(relative_path)  # Вывод: src/utils/file.txt

# Пример 2: Сегмент не найден
full_path = "/home/user/project/src/utils/file.txt"
relative_from = "config"
relative_path = get_relative_path(full_path, relative_from)
print(relative_path)  # Вывод: None

# Пример 3: relative_from находится в начале пути
full_path = "/home/user/project/src/utils/file.txt"
relative_from = "home"
relative_path = get_relative_path(full_path, relative_from)
print(relative_path)  # Вывод: home/user/project/src/utils/file.txt