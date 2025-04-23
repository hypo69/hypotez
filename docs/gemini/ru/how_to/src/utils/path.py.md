### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Функция `get_relative_path` извлекает относительный путь из полного пути, начиная с указанного сегмента. Это полезно, когда необходимо получить часть пути от определенной точки в иерархии файловой системы.

Шаги выполнения
-------------------------
1. **Преобразование в Path:** Функция преобразует входные строки `full_path` и `relative_from` в объекты `Path` для удобства манипуляций с путями.
2. **Разбиение пути на части:** Полный путь разбивается на отдельные компоненты (сегменты), которые хранятся в списке `parts`.
3. **Поиск индекса начала:** Функция ищет индекс сегмента `relative_from` в списке `parts`. Если сегмент найден, определяется индекс, с которого нужно начать формирование относительного пути.
4. **Формирование относительного пути:** Если `relative_from` найден в списке `parts`, создается новый объект `Path` из сегментов, начиная с найденного индекса.
5. **Возврат относительного пути:** Относительный путь преобразуется в строку в формате POSIX и возвращается. Если `relative_from` не найден, функция возвращает `None`.

Пример использования
-------------------------

```python
from pathlib import Path
from typing import Optional

def get_relative_path(full_path: str, relative_from: str) -> Optional[str]:
    """
    Функция извлекает относительный путь из полного пути, начиная с указанного сегмента.

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

# Пример использования
full_path = "/home/user/project/src/module/file.py"
relative_from = "src"
relative_path = get_relative_path(full_path, relative_from)

if relative_path:
    print(f"Относительный путь от '{relative_from}': {relative_path}")
else:
    print(f"Сегмент '{relative_from}' не найден в пути '{full_path}'")

# Вывод:
# Относительный путь от 'src': src/module/file.py
```
```python