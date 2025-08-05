# Модуль `webp2png`

## Обзор

Модуль предназначен для конвертации изображений из формата WebP в формат PNG. Он содержит функцию `convert_images`, которая выполняет конвертацию всех WebP-изображений из указанной директории в PNG-изображения и сохраняет их в другую директорию.

## Подробней

Данный модуль является частью пакета `src.utils.convertors._experiments` и предоставляет функциональность для пакетной конвертации изображений WebP в PNG. Это может быть полезно для работы с изображениями, полученными из различных источников, таких как API OpenAI, где формат WebP может быть предпочтительным, но требуется совместимость с другими системами, поддерживающими только PNG.

## Функции

### `convert_images`

**Назначение**: Конвертирует все WebP-изображения из указанной директории в формат PNG и сохраняет их в другую директорию.

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
```

**Параметры**:
- `webp_dir` (Path): Объект `Path`, представляющий директорию, содержащую исходные WebP-изображения.
- `png_dir` (Path): Объект `Path`, представляющий директорию, в которую будут сохранены конвертированные PNG-изображения.

**Возвращает**:
- `None`: Функция ничего не возвращает.

**Как работает функция**:
1. Функция извлекает список имен файлов WebP из указанной директории `webp_dir`, используя функцию `get_filenames`.
2. Для каждого файла WebP формируется путь к файлу PNG в директории `png_dir`. Имя файла PNG формируется на основе имени файла WebP (без расширения), к которому добавляется расширение ".png".
3. Для каждого WebP файла формируются полные пути к исходному WebP файлу и итоговому PNG файлу.
4. Вызывается функция `webp2png` для выполнения конвертации.
5. Результат конвертации выводится в консоль.

**Примеры**:

Пример вызова функции:
```python
from pathlib import Path
from src.utils.convertors._experiments.webp2png import convert_images
from src import gs

webp_dir = gs.path.google_drive / 'kazarinov' / 'raw_images_from_openai'
png_dir = gs.path.google_drive / 'kazarinov' / 'converted_images'
convert_images(webp_dir, png_dir)
```
В этом примере функция `convert_images` вызывается с путями к директориям, содержащим WebP-изображения и предназначенным для сохранения PNG-изображений. Функция конвертирует все WebP-изображения из `webp_dir` в PNG-изображения и сохраняет их в `png_dir`.

### `get_filenames`

Эта функция не объявлена в этом файле.

### `webp2png`

Эта функция не объявлена в этом файле.