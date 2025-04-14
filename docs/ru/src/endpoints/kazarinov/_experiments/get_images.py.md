# Модуль для работы со списком изображений, сгенерированных ИИ
## Обзор

Модуль предназначен для получения списка изображений, сгенерированных ИИ, из указанной директории. Он использует функции для рекурсивного поиска файлов с определенными расширениями и вывода списка найденных файлов.

## Подробней

Данный код является частью проекта `hypotez` и отвечает за сбор списка изображений, находящихся в определенной директории (`external_data / 'kazarinov' / 'converted_images' / 'pastel'`). Эти изображения, вероятно, были сгенерированы с использованием искусственного интеллекта и преобразованы в формат, пригодный для дальнейшей обработки или использования. Модуль использует утилиты для рекурсивного поиска файлов и вывода списка найденных путей к файлам.

## Функции

### `recursively_get_filepath`

```python
from src.utils.file import read_text_file, save_text_file, recursively_get_filepath
from src.utils.printer import pprint

images_path = recursively_get_filepath(gs.path.external_data / 'kazarinov' / 'converted_images' / 'pastel', ['*.jpeg','*.jpg','*.png'])
pprint(images_path)
...
```

**Назначение**: Получение списка путей к файлам, рекурсивно находящимся в указанной директории и соответствующих заданным расширениям.

**Параметры**:
- `gs.path.external_data / 'kazarinov' / 'converted_images' / 'pastel'` (Path): Путь к директории, в которой производится поиск файлов.
- `['*.jpeg','*.jpg','*.png']` (List[str]): Список расширений файлов, которые необходимо найти.

**Возвращает**:
- `List[str]`: Список путей к найденным файлам.

**Вызывает исключения**:
- Отсутствуют явные указания на вызываемые исключения.

**Как работает функция**:

1. Функция `recursively_get_filepath` рекурсивно просматривает указанную директорию и все ее поддиректории.
2. Для каждого файла проверяется, соответствует ли его расширение одному из указанных в списке расширений.
3. Если файл соответствует, его путь добавляется в список результатов.
4. Функция возвращает список путей ко всем найденным файлам.

**Примеры**:

```python
from pathlib import Path
from src.utils.file import recursively_get_filepath
# Пример использования функции
# Предположим, что в директории 'data' есть файлы 'image1.jpg', 'image2.png' и 'text.txt'
# Путь к директории data
data_path = Path('data')

# Получение списка путей к файлам с расширениями .jpg и .png
image_paths = recursively_get_filepath(data_path, ['*.jpg', '*.png'])
print(image_paths)
```

### `pprint`

```python
from src.utils.file import read_text_file, save_text_file, recursively_get_filepath
from src.utils.printer import pprint

images_path = recursively_get_filepath(gs.path.external_data / 'kazarinov' / 'converted_images' / 'pastel', ['*.jpeg','*.jpg','*.png'])
pprint(images_path)
...
```

**Назначение**: Вывод списка путей к изображениям в удобочитаемом формате.

**Параметры**:
- `images_path` (List[str]): Список путей к файлам изображений, полученный из функции `recursively_get_filepath`.

**Возвращает**:
- Отсутствует явное возвращаемое значение (функция выполняет вывод в консоль).

**Вызывает исключения**:
- Отсутствуют явные указания на вызываемые исключения.

**Как работает функция**:

1. Функция `pprint` принимает список путей к изображениям.
2. Она форматирует этот список и выводит его в консоль в удобном для чтения виде.

**Примеры**:

```python
from src.utils.printer import pprint

# Пример использования функции
image_paths = ['path/to/image1.jpg', 'path/to/image2.png']
pprint(image_paths)
```

## Как работает модуль:

1.  Импортируются необходимые модули и функции: `header`, `gs`, `read_text_file`, `save_text_file`, `recursively_get_filepath`, `pprint`.
2.  Функция `recursively_get_filepath` вызывается для получения списка путей к файлам изображений с расширениями `.jpeg`, `.jpg`, `.png` из директории `gs.path.external_data / 'kazarinov' / 'converted_images' / 'pastel'`.
3.  Полученный список путей к изображениям сохраняется в переменной `images_path`.
4.  Функция `pprint` вызывается для вывода списка `images_path` в консоль.