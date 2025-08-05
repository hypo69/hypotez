# Модуль для получения списка картинок

## Обзор

Этот модуль отвечает за получение списка картинок, сгенерированных ИИ, из определенной директории. 

## Детали

Модуль использует функцию `recursively_get_filepath` из модуля `src.utils.file` для рекурсивного поиска файлов с определенными расширениями в указанной директории. 

## Функции

### `recursively_get_filepath`

**Назначение**: Функция рекурсивно ищет файлы с определенными расширениями в указанной директории.

**Параметры**:
- `path` (Path): Путь к директории.
- `extensions` (List[str]): Список расширений файлов, которые нужно найти.

**Возвращает**:
- List[Path]: Список найденных файлов.

**Пример**:
```python
from pathlib import Path
from src.utils.file import recursively_get_filepath

images_path = recursively_get_filepath(Path('/path/to/images'), ['.jpeg', '.jpg', '.png'])
pprint(images_path)
```

## Примеры

```python
# Пример использования модуля
from src import gs
from src.utils.file import read_text_file, save_text_file, recursively_get_filepath
from src.utils.printer import pprint

images_path = recursively_get_filepath(gs.path.external_data / 'kazarinov' / 'converted_images' / 'pastel', ['.jpeg', '.jpg', '.png'])
pprint(images_path)
```