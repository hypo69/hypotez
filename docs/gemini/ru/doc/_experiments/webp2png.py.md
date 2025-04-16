### Анализ кода модуля `src/utils/convertors/_experiments/webp2png.py`

## Обзор

Этот модуль, расположенный в директории `_experiments`, предназначен для преобразования изображений из формата WebP в формат PNG.

## Подробней

Модуль `src/utils/convertors/_experiments/webp2png.py` автоматизирует процесс преобразования WebP-изображений в формат PNG, используя функцию `convert_images`. Он извлекает WebP файлы из указанной директории и сохраняет их в другой директории в формате PNG. Данный модуль предназначен для использования в экспериментальных целях и может быть нестабильным.

## Функции

### `convert_images`

**Назначение**: Преобразует все изображения WebP в указанной директории в формат PNG.

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

**Параметры**:

-   `webp_dir` (Path): Директория, содержащая исходные WebP изображения.
-   `png_dir` (Path): Директория, в которой будут сохранены преобразованные PNG изображения.

**Как работает функция**:

1.  Получает список файлов WebP в указанной директории, используя функцию `get_filenames`.
2.  Перебирает каждый WebP файл в списке.
3.  Формирует путь для сохранения PNG изображения, используя имя файла WebP без расширения и добавляя расширение `.png`.
4.  Вызывает функцию `webp2png` (из модуля `src.utils.convertors.webp2png`) для преобразования WebP в PNG.
5.  Выводит результат преобразования в консоль.

## Переменные модуля

-   В явном виде переменные модуля не определены. Используются пути, полученные из `gs.path.google_drive`.

## Пример использования

```python
from src.utils.convertors._experiments import webp2png
from pathlib import Path

# Укажите директории для WebP и PNG изображений
webp_dir = Path('/path/to/webp/images')
png_dir = Path('/path/to/png/images')

# Запустите преобразование
webp2png.convert_images(webp_dir, png_dir)
```

**Перед использованием убедитесь, что установлены необходимые библиотеки, такие как Pillow.**

## Взаимосвязь с другими частями проекта

-   Модуль зависит от `src.utils.file` для получения списка файлов.
-   Модуль использует функцию `webp2png` из `src.utils.convertors.webp2png` для преобразования WebP в PNG.
-   Модуль использует пути, полученные из `gs.path.google_drive`, что предполагает наличие конфигурации, определяющей корневые пути проекта.
-   Модуль расположен в директории `_experiments`, что указывает на его возможную нестабильность и экспериментальный характер.