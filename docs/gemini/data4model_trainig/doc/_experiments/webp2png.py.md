### Анализ кода модуля `hypotez/src/utils/convertors/_experiments/webp2png.py`

## Обзор

Этот модуль предназначен для преобразования изображений из формата WebP в формат PNG.

## Подробнее

Модуль содержит функцию `convert_images`, которая позволяет рекурсивно обходить указанную директорию, содержащую WebP-изображения, и конвертировать их в PNG-формат, сохраняя результат в другую директорию.

## Функции

### `convert_images`

```python
def convert_images(webp_dir: Path, png_dir: Path) -> None:
    """ Convert all WebP images in the specified directory to PNG format.

    Args:
        webp_dir (Path): Directory containing the source WebP images.
        png_dir (Path): Directory to save the converted PNG images.

    Example:
        convert_images(
            gs.path.google_drive / 'emil' / 'raw_images_from_openai',
            gs.path.google_drive / 'emil' / 'converted_images'
        )
    """
    ...
```

**Назначение**:
Преобразует все WebP-изображения в указанной директории в формат PNG.

**Параметры**:
- `webp_dir` (Path): Директория, содержащая исходные WebP-изображения.
- `png_dir` (Path): Директория для сохранения преобразованных PNG-изображений.

**Возвращает**:
- None

**Как работает функция**:
1. Получает список WebP-файлов в указанной директории с помощью `get_filenames`.
2. Перебирает все найденные WebP-файлы.
3. Для каждого файла формирует путь к выходному PNG-файлу, используя имя исходного файла (без расширения) и новое расширение `.png`.
4. Вызывает функцию `webp2png` для преобразования WebP-файла в PNG.
5. Логирует результат преобразования (успех или ошибка).

## Переменные

Отсутствуют

## Запуск

Для использования этого модуля необходимо установить библиотеку `Pillow`.

```bash
pip install Pillow
```

Также, необходимо убедится что в проекте определена переменная `gs.path.google_drive`.
Пример использования:

```python
from src.utils.convertors.webp2png import convert_images
from pathlib import Path

# Необходимо определить пути к директориям
webp_dir = Path('/path/to/webp/images')
png_dir = Path('/path/to/png/images')
convert_images(webp_dir, png_dir)