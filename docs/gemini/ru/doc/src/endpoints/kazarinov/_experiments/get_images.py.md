# Список картинок, сгенерированный ИИ

## Обзор

Этот модуль содержит код для получения списка картинок, сгенерированных ИИ. Он работает с папкой `converted_images`,  расположенной в `gs.path.external_data/kazarinov/converted_images`.
## Подробней

Модуль выполняет следующие действия:

1. **Загружает путь к папке `converted_images`:** 
  - Используется функция `recursively_get_filepath` из модуля `src.utils.file` для получения списка файлов, сгенерированных ИИ.
  - Указанный путь к папке  -  `gs.path.external_data / 'kazarinov' / 'converted_images' / 'pastel'`. 
2. **Ищет изображения:**
  - Функция `recursively_get_filepath` отбирает только изображения с расширениями `.jpeg`, `.jpg`, `.png`.
  - Функция `pprint` из модуля `src.utils.printer` красиво выводит полученный список файлов.
3. **Дополнительные действия:**
  -  В коде присутствует `...`.  На данном этапе  в коде  не реализованы  другие действия с полученными изображениями.

## Функции

### `recursively_get_filepath`

**Назначение**: Функция получает список файлов, сгенерированных ИИ.

**Параметры**:

- `path (Path)`: Путь к папке, в которой нужно искать файлы.
- `extensions (List[str])`: Список расширений файлов для поиска.

**Возвращает**:

- `List[Path]`: Список файлов с указанными расширениями, найденных в папке и подпапках.

**Пример**:

```python
from src.utils.file import recursively_get_filepath
from pathlib import Path

# Пример: 
path = Path('/path/to/your/folder')
extensions = ['.jpg', '.png']
files = recursively_get_filepath(path, extensions)
print(files) 
```

### `pprint`

**Назначение**: Функция выводит полученный список файлов в читабельном формате.

**Параметры**:

- `print_data (Any)`: Данные, которые нужно вывести.

**Возвращает**:

- `None`

**Пример**:

```python
from src.utils.printer import pprint
files = ['file1.jpg', 'file2.png', 'file3.jpeg']
pprint(files)
```

## Параметры

- `images_path (List[Path])`: Список файлов с указанными расширениями, найденных в папке и подпапках.

## Примеры

```python
import header
from src import gs
from src.utils.file import read_text_file, save_text_file, recursively_get_filepath
from src.utils.printer import pprint

images_path = recursively_get_filepath(gs.path.external_data / 'kazarinov' / 'converted_images' / 'pastel', ['.jpeg', '.jpg', '.png'])
pprint(images_path)