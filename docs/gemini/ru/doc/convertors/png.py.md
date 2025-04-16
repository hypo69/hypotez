# Модуль для работы с PNG изображениями (png.py)

## Обзор

Этот модуль предоставляет функции для работы с PNG изображениями, включая генерацию изображений из текста, наложение водяных знаков, изменение размеров и преобразование в другие форматы.

## Подробней

Модуль `src/utils/convertors/png.py` предназначен для упрощения задач, связанных с созданием и обработкой PNG изображений. Он предоставляет класс `TextToImageGenerator` для генерации изображений на основе текста и функции для выполнения других операций с изображениями, таких как добавление водяных знаков и изменение размеров. Модуль использует библиотеки `aiohttp`, `aiofiles`, `PIL (Pillow)` и модуль логирования `src.logger.logger`.

## Классы

### `TextToImageGenerator`

**Описание**: Класс для генерации PNG-изображений из текстовых строк.

**Атрибуты**:

-   `default_output_dir` (Path): Путь к директории для сохранения сгенерированных изображений. По умолчанию `"./output"`.
-   `default_canvas_size` (Tuple[int, int]): Размер холста для изображений (ширина, высота). По умолчанию `(1024, 1024)`.
-   `default_padding` (float): Процент от размера холста, используемый в качестве границы. По умолчанию `0.10`.
-   `default_background` (str): Цвет фона для изображений. По умолчанию `"white"`.
-   `default_text_color` (str): Цвет текста. По умолчанию `"black"`.
-   `default_log_level` (str): Уровень детализации логирования. По умолчанию `"WARNING"`.

**Методы**:

-   `__init__(self)`: Инициализирует объект `TextToImageGenerator` с настройками по умолчанию.
-   `generate_images(self, lines: List[str], output_dir: str | Path = None, font: str | ImageFont.ImageFont = "sans-serif", canvas_size: Tuple[int, int] = None, padding: float = None, background_color: str = None, text_color: str = None, log_level: int | str | bool = None, clobber: bool = False) -> List[Path]`: Генерирует PNG-изображения из предоставленных текстовых строк.
-   `generate_png(self, text: str, canvas_size: Tuple[int, int], padding: float, background_color: str, text_color: str, font: str | ImageFont.ImageFont) -> Image`: Создает PNG-изображение с указанным текстом, шрифтом и цветами.
-   `center_text_position(self, draw: ImageDraw.Draw, text: str, font: ImageFont.ImageFont, canvas_size: Tuple[int, int]) -> Tuple[int, int]`: Вычисляет позицию для центрирования текста на холсте.
-    `overlay_images(self, background_path: str | Path, overlay_path: str | Path, position: tuple[int, int] = (0, 0), alpha: float = 1.0) -> Image`: Накладывает одно PNG-изображение поверх другого в указанной позиции.

#### `__init__`

**Назначение**: Инициализирует объект `TextToImageGenerator` с настройками по умолчанию.

**Как работает функция**:

1.  Устанавливает значения по умолчанию для атрибутов, таких как выходная директория, размер холста, отступы, цвета фона и текста, а также уровень логирования.

#### `generate_images`

**Назначение**: Генерирует PNG-изображения из предоставленных текстовых строк.

```python
async def generate_images(
    self,
    lines: List[str],
    output_dir: str | Path = None,
    font: str | ImageFont.ImageFont = "sans-serif",
    canvas_size: Tuple[int, int] = None,
    padding: float = None,
    background_color: str = None,
    text_color: str = None,
    log_level: int | str | bool = None,
    clobber: bool = False,
) -> List[Path]:
    """
    Generates PNG images from the provided text lines.

    Args:
        lines (List[str]): A list of strings containing the text to generate images from.
        output_dir (str | Path, optional): Directory to save the output images. Defaults to "./output".
        font (str | ImageFont.ImageFont, optional): Font to use for the text. Defaults to "sans-serif".
        canvas_size (Tuple[int, int], optional): Size of the canvas in pixels. Defaults to (1024, 1024).
        padding (float, optional): Percentage of canvas size to use as a blank border. Defaults to 0.10.
        background_color (str, optional): Background color for the images. Defaults to "white".
        text_color (str, optional): Color of the text. Defaults to "black".
        log_level (int | str | bool, optional): Logging verbosity level. Defaults to "WARNING".
        clobber (bool, optional): If True, overwrites existing files. Defaults to False.

    Returns:
        List[Path]: A list of paths to the generated PNG images.

    Example:
        >>> generator = TextToImageGenerator()
        >>> lines = ["Text 1", "Text 2", "Text 3"]
        >>> output_dir = "./output"
        >>> images = await generator.generate_images(lines, output_dir=output_dir)
        >>> print(images)
        [PosixPath('./output/Text 1.png'), PosixPath('./output/Text 2.png'), PosixPath('./output/Text 3.png')]
    """
    ...
```

**Параметры**:

-   `lines` (List[str]): Список строк, содержащих текст для генерации изображений.
-   `output_dir` (str | Path, optional): Директория для сохранения выходных изображений. По умолчанию `"./output"`.
-   `font` (str | ImageFont.ImageFont, optional): Шрифт для использования в тексте. По умолчанию `"sans-serif"`.
-   `canvas_size` (Tuple[int, int], optional): Размер холста в пикселях. По умолчанию `(1024, 1024)`.
-   `padding` (float, optional): Процент от размера холста, используемый в качестве границы. По умолчанию `0.10`.
-   `background_color` (str, optional): Цвет фона для изображений. По умолчанию `"white"`.
-   `text_color` (str, optional): Цвет текста. По умолчанию `"black"`.
-   `log_level` (int | str | bool, optional): Уровень детализации логирования. По умолчанию `"WARNING"`.
-   `clobber` (bool, optional): Если `True`, перезаписывает существующие файлы. По умолчанию `False`.

**Возвращает**:

-   `List[Path]`: Список путей к сгенерированным PNG-изображениям.

**Как работает функция**:

1.  Инициализирует параметры на основе аргументов и значений по умолчанию.
2.  Выполняет цикл по каждой строке текста в списке `lines`.
3.  Формирует путь к выходному файлу PNG.
4.  Проверяет, существует ли файл, и если существует и `clobber` равен `False`, пропускает создание изображения.
5.  Вызывает функцию `generate_png` для создания изображения.
6.  Сохраняет изображение в файл.
7.  Добавляет путь к изображению в список `generated_images`.
8.  Возвращает список путей к сгенерированным изображениям.

#### `generate_png`

**Назначение**: Создает PNG-изображение с указанным текстом, шрифтом и цветами.

```python
def generate_png(
    self,
    text: str,
    canvas_size: Tuple[int, int],
    padding: float,
    background_color: str,
    text_color: str,
    font: str | ImageFont.ImageFont,
) -> Image:
    """
    Creates a PNG image with the specified text, font, and colors.

    Args:
        text (str): Text to render on the image.
        canvas_size (Tuple[int, int]): Size of the canvas in pixels.
        padding (float): Padding percentage to use as a border.
        background_color (str): Background color of the image.
        text_color (str): Color of the text.
        font (str | ImageFont.ImageFont): Font to use for the text.

    Returns:
        Image: The generated PNG image.
    """
    ...
```

**Параметры**:

-   `text` (str): Текст для отображения на изображении.
-   `canvas_size` (Tuple[int, int]): Размер холста в пикселях.
-   `padding` (float): Процент отступа, используемый в качестве границы.
-   `background_color` (str): Цвет фона изображения.
-   `text_color` (str): Цвет текста.
-   `font` (str | ImageFont.ImageFont): Шрифт для использования в тексте.

**Возвращает**:

-   `Image`: Сгенерированное PNG-изображение.

**Как работает функция**:

1.  Создает новое изображение с указанным размером и цветом фона.
2.  Создает объект `ImageDraw` для рисования на изображении.
3.  Определяет размер шрифта на основе размера холста и отступа.
4.  Вычисляет позицию для центрирования текста на холсте.
5.  Рисует текст на изображении с использованием указанного шрифта и цвета.
6.  Возвращает сгенерированное изображение.

#### `center_text_position`

**Назначение**: Вычисляет позицию для центрирования текста на холсте.

```python
def center_text_position(
    self, draw: ImageDraw.Draw, text: str, font: ImageFont.ImageFont, canvas_size: Tuple[int, int]
) -> Tuple[int, int]:
    """
    Calculates the position to center the text on the canvas.

    Args:
        draw (ImageDraw.Draw): The ImageDraw instance.
        text (str): Text to be rendered.
        font (ImageFont.ImageFont): Font used for the text.
        canvas_size (Tuple[int, int]): Size of the canvas in pixels.

    Returns:
        Tuple[int, int]: Coordinates for centering the text.
    """
    ...
```

**Параметры**:

-   `draw` (ImageDraw.Draw): Экземпляр `ImageDraw`.
-   `text` (str): Текст, который нужно отобразить.
-   `font` (ImageFont.ImageFont): Шрифт, используемый для текста.
-   `canvas_size` (Tuple[int, int]): Размер холста в пикселях.

**Возвращает**:

-   `Tuple[int, int]`: Координаты для центрирования текста.

**Как работает функция**:

1.  Вычисляет ширину и высоту текста с использованием `draw.textsize(text, font=font)`.
2.  Вычисляет координаты для центрирования текста на холсте и возвращает их.

#### `overlay_images`

**Назначение**: Накладывает одно PNG-изображение поверх другого в указанной позиции.

```python
def overlay_images(
    self,
    background_path: str | Path,
    overlay_path: str | Path,
    position: tuple[int, int] = (0, 0),
    alpha: float = 1.0,
) -> Image:
    """Overlays one PNG image on top of another at a specified position.

    Args:
        background_path (str | Path): Path to the background PNG image.
        overlay_path (str | Path): Path to the overlay PNG image.
        position (tuple[int, int], optional): (x, y) coordinates where the overlay will be placed. Defaults to (0, 0).
        alpha (float, optional): Transparency level of the overlay image (0.0 - 1.0). Defaults to 1.0.

    Returns:
        Image: The resulting image with the overlay.

    Example:
        >>> result_image = overlay_images("background.png", "overlay.png", position=(50, 50), alpha=0.8)
        >>> result_image.save("result.png")
    """
    ...
```

**Параметры**:

-   `background_path` (str | Path): Путь к фоновому PNG-изображению.
-   `overlay_path` (str | Path): Путь к PNG-изображению, которое будет наложено.
-   `position` (tuple[int, int], optional): (x, y) координаты, где будет размещено наложение. По умолчанию (0, 0).
-   `alpha` (float, optional): Уровень прозрачности накладываемого изображения (0.0 - 1.0). По умолчанию 1.0.

**Возвращает**:

-   `Image`: Результирующее изображение с наложением.

**Как работает функция**:

1.  Открывает фоновое и накладываемое изображения, используя `PIL.Image.open`.
2.  Изменяет размер накладываемого изображения, чтобы оно соответствовало размеру фонового, если необходимо.
3.  Регулирует прозрачность накладываемого изображения.
4.  Вставляет накладываемое изображение поверх фонового в указанной позиции.
5.  Возвращает результирующее изображение.

### `webp2png`

**Назначение**: Конвертирует WEBP изображение в формат PNG.

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

**Параметры**:

-   `webp_path` (str): Путь к исходному WEBP файлу.
-   `png_path` (str): Путь для сохранения преобразованного PNG файла.

**Возвращает**:

-   `bool`: True, если конвертация прошла успешно, False в противном случае.

**Как работает функция**:

1.  Открывает WEBP изображение, используя `Image.open`.
2.  Сохраняет изображение в формате PNG по указанному пути.
3.  Если во время процесса преобразования возникла ошибка, функция ловит исключение и возвращает False.

## Переменные модуля

-   `TEXT_COLORS` (dict): Словарь, сопоставляющий названия цветов текста с их ANSI-кодами.
-   `BG_COLORS` (dict): Словарь, сопоставляющий названия цветов фона с их ANSI-кодами.

## Пример использования

**Создание PNG-изображений из текста:**

```python
import asyncio
from src.utils.convertors.png import TextToImageGenerator

async def main():
    generator = TextToImageGenerator()
    lines = ["Hello, world!", "This is a test."]
    images = await generator.generate_images(lines, output_dir="output")
    print(f"Generated images: {images}")

if __name__ == "__main__":
    asyncio.run(main())
```

**Накладывает одно PNG-изображение поверх другого:**
```python
from pathlib import Path
from PIL import Image
from src.utils.convertors.png import TextToImageGenerator

# Пути к изображениям
background_image_path = Path("background.png")  # Замените на путь к вашему фоновому изображению
overlay_image_path = Path("overlay.png")  # Замените на путь к вашему изображению для наложения

# Проверьте, существуют ли файлы
if not background_image_path.exists() or not overlay_image_path.exists():
    print("Один из указанных файлов не существует.")
else:
    # Инициализируем TextToImageGenerator
    generator = TextToImageGenerator()

    # Накладываем изображения
    try:
        combined_image = generator.overlay_images(background_image_path, overlay_image_path, position=(50, 50), alpha=0.8)
        combined_image.save("combined_image.png")
        print("Изображение успешно создано")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
```

## Взаимосвязь с другими частями проекта

-   Модуль `src.utils.convertors.png` использует библиотеку `Pillow` для обработки изображений.
-   Модуль использует модуль `src.logger.logger` для логирования информации об ошибках.
-   Он может использоваться другими модулями проекта `hypotez` для создания, обработки и преобразования изображений.
- Требует наличия установленной библиотеки Graphviz для преобразования DOT файлов в PNG.