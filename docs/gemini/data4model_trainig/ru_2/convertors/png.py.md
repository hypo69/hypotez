### Анализ кода `hypotez/src/utils/convertors/png.py.md`

## Обзор

Модуль предоставляет утилиты для работы с PNG-изображениями, включая генерацию изображений из текста и наложение водяных знаков.

## Подробнее

Этот модуль содержит класс `TextToImageGenerator`, который предоставляет методы для генерации PNG-изображений из текста, а также функции для наложения изображений друг на друга и преобразования изображений из формата WebP в PNG. Он использует библиотеки `aiohttp` для асинхронной загрузки, `aiofiles` для асинхронной работы с файлами и `PIL` (Pillow) для обработки изображений.

## Классы

### `TextToImageGenerator`

```python
class TextToImageGenerator:
    """
    A class for generating PNG images from text lines.

    **Functions**:
    - `assign_path`: Determines the correct path for output PNG files, creating the directory if necessary.
    - `center_text_position`: Calculates the position to center text on the canvas.
    - `generate_png`: Creates a PNG image with the specified text, font, colors, etc.
    - `not_comment_or_blank`: Checks if a line is neither a comment nor blank.
    - `which_exist`: Checks which file names already exist in the directory.
    - `get_characters`: Extracts text lines from the input file or list, filtering out comments and blank lines.
    - `parse_size`: Parses a string into a `Size` object.
    - `get_max_text_size`: Computes the maximum text size based on the font and text lines.
    - `get_font`: Determines the font size based on canvas size and padding.
    - `setup_logging`: Configures logging based on the specified logging level.
    - `error`: Logs an error message and raises an exception.
    - `overlay_images`: Overlays one PNG image on top of another.
    """
    ...
```

**Описание**:
Класс для генерации PNG-изображений из текстовых строк.

**Методы**:

*   `__init__(self)`: Инициализирует класс `TextToImageGenerator` с настройками по умолчанию.
*   `generate_images(self, lines: List[str], output_dir: str | Path = None, font: str | ImageFont.ImageFont = "sans-serif", canvas_size: Tuple[int, int] = None, padding: float = None, background_color: str = None, text_color: str = None, log_level: int | str | bool = None, clobber: bool = False) -> List[Path]`: Генерирует PNG-изображения из предоставленных текстовых строк.
*   `generate_png(self, text: str, canvas_size: Tuple[int, int], padding: float, background_color: str, text_color: str, font: str | ImageFont.ImageFont) -> Image`: Создает PNG-изображение с указанным текстом, шрифтом и цветами.
*   `center_text_position(self, draw: ImageDraw.Draw, text: str, font: ImageFont.ImageFont, canvas_size: Tuple[int, int]) -> Tuple[int, int]`: Вычисляет позицию для центрирования текста на холсте.
*   `overlay_images(self, background_path: str | Path, overlay_path: str | Path, position: tuple[int, int] = (0, 0), alpha: float = 1.0) -> Image`: Накладывает одно PNG-изображение поверх другого в указанной позиции.

## Функции

### `webp2png`

```python
def webp2png(webp_path: str, png_path: str) -> bool:
    """
    Converts a WEBP image to PNG format.

    Args:
        webp_path (str): Path to the input WEBP file.
        png_path (str): Path to save the converted PNG file.

    Example:
        webp2png('image.webp', 'image.png')
    """
    ...
```

**Назначение**:
Преобразует изображение в формате WEBP в формат PNG.

**Параметры**:

*   `webp_path` (str): Путь к входному WEBP-файлу.
*   `png_path` (str): Путь для сохранения преобразованного PNG-файла.

**Возвращает**:

*   `bool`: `True`, если преобразование прошло успешно, None в противном случае.

**Как работает функция**:

1.  Открывает изображение в формате WebP с помощью `Image.open`.
2.  Сохраняет изображение в формате PNG с помощью `img.save`.
3.  Возвращает `True` в случае успеха.
4.  В случае ошибки выводит сообщение и завершает работу.

## Переменные

Отсутствуют.

## Примеры использования

```python
from src.utils.convertors.png import TextToImageGenerator, webp2png
from pathlib import Path

# Создание генератора изображений
generator = TextToImageGenerator()

# Пример наложения изображений
background_path = "background.png"  # Замените на путь к вашему фоновому изображению
overlay_path = "overlay.png"  # Замените на путь к вашему изображению наложения
result_image = generator.overlay_images(background_path, overlay_path, position=(50, 50), alpha=0.8)
result_image.save("result.png")

# Пример преобразования WebP в PNG
webp_path = "image.webp"
png_path = "image.png"
if webp2png(webp_path, png_path):
    print(f"Successfully converted {webp_path} to {png_path}")
```

## Зависимости

*   `aiohttp`: Для асинхронных HTTP-запросов.
*   `aiofiles`: Для асинхронной работы с файлами.
*   `asyncio`: Для асинхронного программирования.
*   `random`: Для выбора случайного изображения.
*   `pathlib.Path`: Для работы с путями к файлам.
*   `typing.Optional, typing.Union, typing.Tuple, typing.List`: Для аннотаций типов.
*   `io.BytesIO`: Для работы с данными в памяти как с файлом.
*   `PIL (Pillow)`: Для обработки изображений.
*   `src.logger.logger`: Для логирования событий и ошибок.

## Взаимосвязи с другими частями проекта

Модуль `png.py` предоставляет утилиты для работы с изображениями и может использоваться в других частях проекта `hypotez`, где требуется генерация изображений, наложение водяных знаков, изменение размеров или преобразование форматов.