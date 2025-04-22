# Модуль webp2png

## Обзор

Модуль предназначен для конвертации изображений из формата WebP в формат PNG. Он выполняет поиск файлов WebP в указанной директории и сохраняет конвертированные PNG изображения в другую директорию.

## Подробней

Этот модуль предоставляет функцию `convert_images`, которая автоматизирует процесс конвертации изображений WebP в PNG. Он использует функцию `webp2png` из модуля `src.utils.convertors.webp2png` для фактического преобразования файлов. Модуль также использует функцию `get_filenames` из модуля `src.utils.file` для получения списка файлов WebP в указанной директории.

## Функции

### `convert_images`

```python
def convert_images(webp_dir: Path, png_dir: Path) -> None:
    """
    Конвертирует все WebP изображения в указанной директории в формат PNG.

    Args:
        webp_dir (Path): Директория, содержащая исходные WebP изображения.
        png_dir (Path): Директория для сохранения конвертированных PNG изображений.

    Example:
        convert_images(
            gs.path.google_drive / 'emil' / 'raw_images_from_openai',
            gs.path.google_drive / 'emil' / 'converted_images'
        )
    """
```

**Назначение**: Конвертирует все изображения в формате WebP из одной директории в формат PNG и сохраняет их в другую директорию.

**Параметры**:
- `webp_dir` (Path): Путь к директории, содержащей исходные WebP изображения.
- `png_dir` (Path): Путь к директории, в которую будут сохранены конвертированные PNG изображения.

**Возвращает**:
- `None`: Функция ничего не возвращает.

**Как работает функция**:

1.  Функция `convert_images` принимает пути к директориям с WebP изображениями (`webp_dir`) и для сохранения PNG изображений (`png_dir`).
2.  Использует `get_filenames` для получения списка всех файлов WebP в директории `webp_dir`.
3.  Для каждого файла WebP формируется путь к будущему PNG файлу в директории `png_dir`. Имя PNG файла совпадает с именем WebP файла (без расширения).
4.  Вызывает функцию `webp2png` для конвертации каждого WebP файла в PNG. Результат конвертации выводится в консоль.

**Примеры**:

```python
from pathlib import Path
from src import gs
from src.utils.convertors._experiments.webp2png import convert_images

#  Пути к директориям для WebP и PNG изображений
webp_dir = gs.path.google_drive / 'emil' / 'raw_images_from_openai'
png_dir = gs.path.google_drive / 'emil' / 'converted_images'

#  Вызов функции для конвертации изображений
convert_images(webp_dir, png_dir)