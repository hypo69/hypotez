# Список картинок, сгенерированный ИИ

## Обзор

Модуль предназначен для получения списка изображений, сгенерированных ИИ. Он выполняет поиск файлов изображений в указанной директории и выводит список найденных путей.

## Подробнее

Данный код является частью экспериментов Kazarinov и предназначен для работы с изображениями, сгенерированными ИИ. Он использует функции для рекурсивного поиска файлов изображений в заданной директории и их вывода.

## Модули

В данном файле используются следующие модули:

- `header`: Импортируется модуль `header`. (Предположительно, содержит общие настройки или определения для проекта)
- `src`: Импортируется модуль `gs` из пакета `src`.
- `src.utils.file`: Импортируются функции `read_text_file`, `save_text_file`, и `recursively_get_filepath` из модуля `src.utils.file`.
- `src.utils.printer`: Импортируется функция `pprint` из модуля `src.utils.printer`.

## Переменные

- `images_path`: содержит список путей к файлам изображений, полученный с помощью функции `recursively_get_filepath`.

## Функции

### `recursively_get_filepath`

```python
from src.utils.file import recursively_get_filepath

def recursively_get_filepath(
    root_dir: Path,
    patterns: List[str],
    exclude_patterns: Optional[List[str]] = None,
    max_depth: Optional[int] = None,
) -> List[Path]:
    """
    Рекурсивно получает список путей к файлам, соответствующим заданным шаблонам, начиная с указанной корневой директории.

    Args:
        root_dir (Path): Корневая директория для поиска файлов.
        patterns (List[str]): Список шаблонов файлов для включения в поиск (например, ['*.txt', '*.pdf']).
        exclude_patterns (Optional[List[str]], optional): Список шаблонов файлов для исключения из поиска. По умолчанию None.
        max_depth (Optional[int], optional): Максимальная глубина поиска. По умолчанию None (без ограничений).

    Returns:
        List[Path]: Список путей к файлам, соответствующим заданным шаблонам.

    Raises:
        OSError: Если возникают проблемы при доступе к директории или файлу.
        ValueError: Если предоставлены некорректные аргументы, например, если root_dir не является директорией.

    Example:
        >>> from pathlib import Path
        >>> root_dir = Path("./")  # Текущая директория
        >>> patterns = ["*.txt"]
        >>> file_paths = recursively_get_filepath(root_dir, patterns)
        >>> for path in file_paths:
        ...     print(path)  # Вывод путей к файлам с расширением .txt в текущей директории и поддиректориях.
    """
    ...
```

**Назначение**:
Рекурсивно получает список путей к файлам, соответствующим заданным шаблонам, начиная с указанной корневой директории.

**Параметры**:
- `root_dir` (Path): Корневая директория для поиска файлов.
- `patterns` (List[str]): Список шаблонов файлов для включения в поиск (например, `['*.txt', '*.pdf']`).
- `exclude_patterns` (Optional[List[str]], optional): Список шаблонов файлов для исключения из поиска. По умолчанию `None`.
- `max_depth` (Optional[int], optional): Максимальная глубина поиска. По умолчанию `None` (без ограничений).

**Возвращает**:
- `List[Path]`: Список путей к файлам, соответствующим заданным шаблонам.

**Вызывает исключения**:
- `OSError`: Если возникают проблемы при доступе к директории или файлу.
- `ValueError`: Если предоставлены некорректные аргументы, например, если `root_dir` не является директорией.

**Как работает функция**:
Функция выполняет рекурсивный поиск файлов в указанной директории `root_dir`, фильтруя их по заданным шаблонам `patterns`. При необходимости можно исключить файлы, соответствующие шаблонам в `exclude_patterns`, и ограничить глубину поиска с помощью `max_depth`. Возвращает список объектов `Path`, представляющих пути к найденным файлам.

**Примеры**:
```python
from pathlib import Path
root_dir = Path("./")  # Текущая директория
patterns = ["*.txt"]
file_paths = recursively_get_filepath(root_dir, patterns)
for path in file_paths:
    print(path)  # Вывод путей к файлам с расширением .txt в текущей директории и поддиректориях.
```

### `pprint`

```python
from src.utils.printer import pprint

def pprint(print_data: Any = None, text_color: str = "white", bg_color: str = "", font_style: str = "") -> None:
    """Pretty prints the given data with optional color, background, and font style.

    This function formats the input data based on its type and prints it to the console. The data is printed with optional 
    text color, background color, and font style based on the specified parameters. The function can handle dictionaries, 
    lists, strings, and file paths.

    :param print_data: The data to be printed. Can be of type ``None``, ``dict``, ``list``, ``str``, or ``Path``.
    :param text_color: The color to apply to the text. Default is 'white'. See :ref:`TEXT_COLORS`.
    :param bg_color: The background color to apply to the text. Default is '' (no background color). See :ref:`BG_COLORS`.
    :param font_style: The font style to apply to the text. Default is '' (no font style). See :ref:`FONT_STYLES`.
    :return: None

    :raises: Exception if the data type is unsupported or an error occurs during printing.

    :example:
        >>> pprint({"name": "Alice", "age": 30}, text_color="green")

        >>> pprint(["apple", "banana", "cherry"], text_color="blue", font_style="bold")

        >>> pprint("text example", text_color="yellow", bg_color="bg_red", font_style="underline")
    """
    ...
```

**Назначение**:
Красиво выводит предоставленные данные с возможностью настройки цвета текста, фона и стиля шрифта.

**Параметры**:
- `print_data` (Any, optional): Данные для вывода. Может быть `None`, `dict`, `list`, `str` или `Path`. По умолчанию `None`.
- `text_color` (str, optional): Цвет текста. По умолчанию "white".
- `bg_color` (str, optional): Цвет фона. По умолчанию "".
- `font_style` (str, optional): Стиль шрифта. По умолчанию "".

**Возвращает**:
- `None`

**Вызывает исключения**:
- `Exception`: Если тип данных не поддерживается или возникает ошибка во время вывода.

**Как работает функция**:
Функция принимает данные различных типов (словарь, список, строка, путь к файлу) и выводит их в консоль с применением указанных стилей текста, фона и шрифта. Она использует ANSI escape-коды для форматирования текста.

**Примеры**:
```python
pprint({"name": "Alice", "age": 30}, text_color="green")
pprint(["apple", "banana", "cherry"], text_color="blue", font_style="bold")
pprint("text example", text_color="yellow", bg_color="bg_red", font_style="underline")
```

## Логика кода

1.  **Определение пути к директории с изображениями**:

    -   Переменная `images_path` инициализируется результатом вызова функции `recursively_get_filepath`.
    -   В качестве аргументов передаются:
        -   `gs.path.external_data / 'kazarinov' / 'converted_images' / 'pastel'` - путь к директории, где хранятся изображения. `gs.path.external_data` - это, вероятно, путь к внешним данным проекта.
        -   `['*.jpeg','*.jpg','*.png']` - список шаблонов файлов, которые необходимо найти (JPEG, JPG, PNG).

2.  **Вывод списка путей к изображениям**:

    -   Функция `pprint(images_path)` выводит список путей к найденным изображениям. Это позволяет разработчику увидеть, какие файлы были найдены и где они расположены.

## Примеры

```python
import header
from src import gs
from src.utils.file import read_text_file, save_text_file, recursively_get_filepath
from src.utils.printer import pprint

images_path = recursively_get_filepath(gs.path.external_data / 'kazarinov' / 'converted_images' / 'pastel', ['*.jpeg','*.jpg','*.png'])
pprint(images_path)