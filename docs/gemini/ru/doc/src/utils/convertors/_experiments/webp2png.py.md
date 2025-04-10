# Модуль `webp2png`

## Обзор

Модуль предназначен для конвертации изображений из формата WebP в формат PNG. Он выполняет поиск файлов WebP в указанной директории и сохраняет сконвертированные PNG-изображения в другую директорию.

## Подробнее

Модуль `webp2png` предоставляет функцию `convert_images`, которая автоматизирует процесс конвертации изображений WebP в PNG. Он использует функцию `webp2png` из модуля `src.utils.convertors.webp2png` для фактической конвертации каждого файла. Модуль также использует функцию `get_filenames` из модуля `src.utils.file` для получения списка файлов WebP из заданной директории.
Внутри `if __name__ == '__main__'` определены пути к директориям с исходными изображениями WebP и директории, куда будут сохранены сконвертированные PNG-изображения. Затем вызывается функция `convert_images` для выполнения конвертации.

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

**Назначение**: Конвертирует все WebP изображения в указанной директории в формат PNG.

**Параметры**:
- `webp_dir` (Path): Директория, содержащая исходные WebP изображения.
- `png_dir` (Path): Директория для сохранения сконвертированных PNG изображений.

**Возвращает**:
- `None`: Функция ничего не возвращает.

**Как работает функция**:
1. Функция `convert_images` принимает на вход две директории: `webp_dir`, откуда будут взяты WebP файлы, и `png_dir`, куда будут сохранены сконвертированные PNG файлы.
2. С помощью функции `get_filenames(webp_dir)` получается список всех WebP файлов в директории `webp_dir`.
3. Затем для каждого WebP файла формируется имя для соответствующего PNG файла, используя метод `stem` для получения имени файла без расширения.
4. Далее формируется полный путь к исходному WebP файлу и к целевому PNG файлу.
5. Вызывается функция `webp2png(webp_path, png)` для выполнения конвертации каждого WebP файла в PNG.
6. Результат конвертации выводится в консоль.

**Примеры**:

```python
from pathlib import Path
#Путь к директории webp
webp_dir = Path('/path/to/webp_images')
#Путь к директории png
png_dir = Path('/path/to/png_images')
convert_images(webp_dir, png_dir)
```

### `__main__`

```python
if __name__ == '__main__':
    # Define the directories for WebP and PNG images
    webp_dir = gs.path.google_drive / 'kazarinov' / 'raw_images_from_openai'
    png_dir = gs.path.google_drive / 'kazarinov' / 'converted_images'
    print(f"from: {webp_dir=}\nto:{png_dir=}")
    # Run the conversion
    convert_images(webp_dir, png_dir)
```

**Назначение**: Определяет директории для WebP и PNG изображений и запускает процесс конвертации.

**Как работает**:
1. Определяются пути к директориям, содержащим WebP изображения и в которые будут сохранены PNG изображения.
2. Выводит в консоль пути к директориям WebP и PNG изображений.
3. Вызывается функция `convert_images` с указанными директориями для выполнения конвертации.

**Примеры**:
Данный блок кода выполняется только при запуске скрипта напрямую.

```python
python your_script_name.py