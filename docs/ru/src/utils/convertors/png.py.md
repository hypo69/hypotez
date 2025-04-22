# Модуль для конвертации PNG изображений

## Обзор

Модуль предоставляет функциональность для генерации PNG изображений из текста, а также для наложения одного PNG изображения на другое. Он включает класс `TextToImageGenerator` для создания изображений из текста и функцию `webp2png` для конвертации изображений из формата WEBP в PNG.

## Подробнее

Модуль предназначен для автоматической генерации изображений на основе текстовых данных. Это может быть полезно, например, для создания превью или динамических изображений для веб-сайтов.

## Классы

### `TextToImageGenerator`

**Описание**: Класс для генерации PNG изображений из текстовых строк.

**Методы**:

- `__init__`: Инициализирует класс `TextToImageGenerator` со значениями по умолчанию для размера холста, отступов, цветов и уровня логирования.
- `generate_images`: Генерирует PNG изображения из предоставленных текстовых строк.
- `generate_png`: Создает PNG изображение с заданным текстом, шрифтом и цветами.
- `center_text_position`: Вычисляет позицию для центрирования текста на холсте.
- `overlay_images`: Накладывает одно PNG изображение на другое в указанной позиции.

### `__init__`

```python
def __init__(self):
    """
    Initializes the TextToImageGenerator class with default settings.
    """
```

**Назначение**:
Инициализирует класс `TextToImageGenerator` с настройками по умолчанию.

**Как работает функция**:
Устанавливает значения по умолчанию для атрибутов класса, таких как директория вывода, размер холста, отступы, цвет фона, цвет текста и уровень логирования.

**Атрибуты**:
- `default_output_dir` (Path): Путь к директории вывода по умолчанию (./output).
- `default_canvas_size` (Tuple[int, int]): Размер холста по умолчанию (1024x1024 пикселей).
- `default_padding` (float): Отступ по умолчанию (10% от размера холста).
- `default_background` (str): Цвет фона по умолчанию ("white").
- `default_text_color` (str): Цвет текста по умолчанию ("black").
- `default_log_level` (str): Уровень логирования по умолчанию ("WARNING").

**Примеры**:
```python
generator = TextToImageGenerator()
print(generator.default_output_dir)  # Вывод: ./output
```

### `generate_images`

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
```

**Назначение**: Генерирует PNG изображения из списка текстовых строк.

**Параметры**:
- `lines` (List[str]): Список строк, из которых будут сгенерированы изображения.
- `output_dir` (str | Path, optional): Директория для сохранения изображений. По умолчанию "./output".
- `font` (str | ImageFont.ImageFont, optional): Шрифт для текста. По умолчанию "sans-serif".
- `canvas_size` (Tuple[int, int], optional): Размер холста в пикселях. По умолчанию (1024, 1024).
- `padding` (float, optional): Отступ в процентах от размера холста. По умолчанию 0.10.
- `background_color` (str, optional): Цвет фона изображений. По умолчанию "white".
- `text_color` (str, optional): Цвет текста. По умолчанию "black".
- `log_level` (int | str | bool, optional): Уровень детализации логирования. По умолчанию "WARNING".
- `clobber` (bool, optional): Если `True`, перезаписывает существующие файлы. По умолчанию `False`.

**Возвращает**:
- `List[Path]`: Список путей к сгенерированным PNG изображениям.

**Как работает функция**:

1. Определяет директорию вывода, используя предоставленный параметр `output_dir` или значение по умолчанию.
2. Устанавливает уровень логирования с помощью метода `setup_logging`.
3. Перебирает каждую строку текста в списке `lines`.
4. Формирует путь к файлу изображения на основе текста строки.
5. Проверяет, существует ли файл и нужно ли его перезаписывать.
6. Вызывает метод `generate_png` для создания изображения.
7. Сохраняет изображение в указанный путь.
8. Добавляет путь к изображению в список `generated_images`.
9. Возвращает список путей к сгенерированным изображениям.

**Примеры**:

```python
generator = TextToImageGenerator()
lines = ["Text 1", "Text 2", "Text 3"]
output_dir = "./output"
images = await generator.generate_images(lines, output_dir=output_dir)
print(images)
# Вывод: [PosixPath('./output/Text 1.png'), PosixPath('./output/Text 2.png'), PosixPath('./output/Text 3.png')]
```

### `generate_png`

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
```

**Назначение**: Создает PNG изображение с заданным текстом, шрифтом и цветами.

**Параметры**:
- `text` (str): Текст для отрисовки на изображении.
- `canvas_size` (Tuple[int, int]): Размер холста в пикселях.
- `padding` (float): Отступ в процентах от размера холста.
- `background_color` (str): Цвет фона изображения.
- `text_color` (str): Цвет текста.
- `font` (str | ImageFont.ImageFont): Шрифт для текста.

**Возвращает**:
- `Image`: Сгенерированное PNG изображение.

**Как работает функция**:

1. Создает новое изображение с заданным размером и цветом фона.
2. Создает объект `ImageDraw` для рисования на изображении.
3. Определяет размер шрифта с помощью метода `get_font_size`.
4. Вычисляет позицию для центрирования текста с помощью метода `center_text_position`.
5. Отрисовывает текст на изображении с заданным цветом и шрифтом.
6. Возвращает сгенерированное изображение.

**Примеры**:

```python
generator = TextToImageGenerator()
text = "Hello, World!"
canvas_size = (512, 512)
padding = 0.05
background_color = "white"
text_color = "black"
font = "arial.ttf"
image = generator.generate_png(text, canvas_size, padding, background_color, text_color, font)
image.save("hello_world.png")
```

### `center_text_position`

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
```

**Назначение**: Вычисляет позицию для центрирования текста на холсте.

**Параметры**:
- `draw` (ImageDraw.Draw): Объект `ImageDraw` для рисования.
- `text` (str): Текст для центрирования.
- `font` (ImageFont.ImageFont): Шрифт текста.
- `canvas_size` (Tuple[int, int]): Размер холста в пикселях.

**Возвращает**:
- `Tuple[int, int]`: Координаты (x, y) для центрирования текста.

**Как работает функция**:

1. Измеряет ширину и высоту текста с помощью метода `draw.textsize`.
2. Вычисляет координаты для центрирования текста, вычитая ширину и высоту текста из размера холста и деля результат на 2.
3. Возвращает вычисленные координаты.

**Примеры**:

```python
from PIL import Image, ImageDraw, ImageFont

generator = TextToImageGenerator()
image = Image.new("RGB", (512, 512), "white")
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("arial.ttf", size=32)
text = "Centered Text"
canvas_size = (512, 512)
x, y = generator.center_text_position(draw, text, font, canvas_size)
print(f"x={x}, y={y}")
```

### `overlay_images`

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
```

**Назначение**: Накладывает одно PNG изображение на другое в указанной позиции.

**Параметры**:
- `background_path` (str | Path): Путь к фоновому PNG изображению.
- `overlay_path` (str | Path): Путь к накладываемому PNG изображению.
- `position` (tuple[int, int], optional): Координаты (x, y), где будет размещено накладываемое изображение. По умолчанию (0, 0).
- `alpha` (float, optional): Уровень прозрачности накладываемого изображения (0.0 - 1.0). По умолчанию 1.0.

**Возвращает**:
- `Image`: Результирующее изображение с наложенным изображением.

**Как работает функция**:

1. Открывает фоновое и накладываемое изображения, преобразуя их в формат RGBA.
2. Изменяет размер накладываемого изображения, чтобы он соответствовал размеру фонового изображения, если это необходимо.
3. Регулирует прозрачность накладываемого изображения на основе параметра `alpha`.
4. Накладывает изображение на фон в указанной позиции.
5. Возвращает результирующее изображение.

**Примеры**:

```python
generator = TextToImageGenerator()
result_image = generator.overlay_images("background.png", "overlay.png", position=(50, 50), alpha=0.8)
result_image.save("result.png")
```

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
```

**Назначение**: Конвертирует изображение из формата WEBP в формат PNG.

**Параметры**:
- `webp_path` (str): Путь к исходному WEBP файлу.
- `png_path` (str): Путь для сохранения сконвертированного PNG файла.

**Возвращает**:
- `bool`: `True`, если конвертация прошла успешно, иначе `False`.

**Как работает функция**:

1. Открывает WEBP изображение с использованием `PIL.Image.open`.
2. Сохраняет изображение в формате PNG по указанному пути.
3. Возвращает `True` в случае успеха.
4. В случае возникновения исключения выводит сообщение об ошибке и возвращает `False`.

**Примеры**:

```python
result = webp2png('image.webp', 'image.png')
if result:
    print("Conversion successful!")
else:
    print("Conversion failed.")