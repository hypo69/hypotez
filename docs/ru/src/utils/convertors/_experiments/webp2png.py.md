# Модуль для конвертации WebP изображений в PNG формат

## Обзор

Модуль предназначен для конвертации изображений из формата WebP в формат PNG. Он содержит функцию `convert_images`, которая выполняет массовую конвертацию файлов из указанной директории в другую.

## Подробней

Модуль предназначен для автоматической конвертации изображений WebP в PNG. Это может быть полезно для обеспечения совместимости с системами, которые не поддерживают формат WebP.

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
```

**Назначение**: Конвертирует все изображения в формате WebP из указанной директории в формат PNG и сохраняет их в другой директории.

**Параметры**:

-   `webp_dir` (Path): Директория, содержащая исходные изображения WebP.
-   `png_dir` (Path): Директория, в которую будут сохранены преобразованные изображения PNG.

**Возвращает**:

-   `None`: Функция ничего не возвращает.

**Как работает функция**:

1.  Функция принимает на вход пути к директориям с WebP и PNG изображениями.
2.  Использует функцию `get_filenames` для получения списка всех файлов WebP в указанной директории.
3.  Для каждого файла WebP формирует имя соответствующего PNG файла, используя метод `stem` для получения имени файла без расширения.
4.  Составляет полные пути к исходному WebP файлу и целевому PNG файлу.
5.  Вызывает функцию `webp2png` для преобразования каждого WebP файла в PNG.
6.  Выводит результат конвертации в консоль.

```
A: Получение списка WebP файлов
|
B: Для каждого WebP файла
|
C: Формирование имени PNG файла
|
D: Конвертация WebP в PNG
|
E: Вывод результата
```

**Примеры**:

```python
from pathlib import Path
from src import gs  # Предполагается, что gs определен в вашем коде

# Пример использования функции convert_images
webp_dir = gs.path.google_drive / 'kazarinov' / 'raw_images_from_openai'
png_dir = gs.path.google_drive / 'kazarinov' / 'converted_images'
convert_images(webp_dir, png_dir)