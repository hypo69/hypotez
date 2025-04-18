# Модуль `png`

## Обзор

Модуль `png` предоставляет инструменты для конвертации текста в PNG-изображения. Он включает класс `TextToImageGenerator`, который позволяет генерировать изображения на основе заданных параметров, таких как текст, шрифт, размер холста, цвет фона и цвет текста.

## Подробнее

Этот модуль предназначен для автоматического создания PNG-изображений из текстовых строк. Он использует библиотеку Pillow (PIL) для работы с изображениями и шрифтами. Модуль может быть использован для создания превью текста, генерации изображений для водяных знаков и других задач, требующих преобразования текста в изображения.

## Классы

### `TextToImageGenerator`

**Описание**: Класс для генерации PNG-изображений из текстовых строк.

**Атрибуты**:
- `default_output_dir` (Path): Путь к директории вывода по умолчанию (`./output`).
- `default_canvas_size` (Tuple[int, int]): Размер холста по умолчанию (1024x1024).
- `default_padding` (float): Отступ от края холста по умолчанию (10%).
- `default_background` (str): Цвет фона по умолчанию ("white").
- `default_text_color` (str): Цвет текста по умолчанию ("black").
- `default_log_level` (str): Уровень логирования по умолчанию ("WARNING").

**Методы**:

- `__init__`: Инициализирует класс `TextToImageGenerator` с настройками по умолчанию.
- `generate_images`: Генерирует PNG-изображения из списка текстовых строк.
- `generate_png`: Создает PNG-изображение с заданным текстом, шрифтом и цветами.
- `center_text_position`: Вычисляет позицию для центрирования текста на холсте.
- `overlay_images`: Накладывает одно PNG-изображение поверх другого в заданной позиции.

**Принцип работы**:
Класс `TextToImageGenerator` предоставляет функциональность для генерации PNG-изображений из текста. При инициализации устанавливаются параметры по умолчанию, такие как размер холста, цвет фона и уровень логирования. Метод `generate_images` принимает список текстовых строк и генерирует PNG-изображения для каждой строки, сохраняя их в указанной директории. Метод `generate_png` создает изображение на основе заданных параметров, таких как текст, шрифт и цвет.

## Методы класса

### `__init__`

```python
def __init__(self):
    """
    Initializes the TextToImageGenerator class with default settings.
    """
    ...
```

**Назначение**: Инициализирует экземпляр класса `TextToImageGenerator` с настройками по умолчанию.
Устанавливает значения по умолчанию для директории вывода, размера холста, отступа, цвета фона, цвета текста и уровня логирования.

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
        [PosixPath(\'./output/Text 1.png\'), PosixPath(\'./output/Text 2.png\'), PosixPath(\'./output/Text 3.png\')]
    """
    ...
```

**Назначение**: Генерирует PNG-изображения из списка текстовых строк.

**Параметры**:
- `lines` (List[str]): Список строк, содержащих текст для генерации изображений.
- `output_dir` (str | Path, optional): Директория для сохранения выходных изображений. По умолчанию "./output".
- `font` (str | ImageFont.ImageFont, optional): Шрифт для использования в тексте. По умолчанию "sans-serif".
- `canvas_size` (Tuple[int, int], optional): Размер холста в пикселях. По умолчанию (1024, 1024).
- `padding` (float, optional): Процент от размера холста для использования в качестве пустой границы. По умолчанию 0.10.
- `background_color` (str, optional): Цвет фона для изображений. По умолчанию "white".
- `text_color` (str, optional): Цвет текста. По умолчанию "black".
- `log_level` (int | str | bool, optional): Уровень детализации логирования. По умолчанию "WARNING".
- `clobber` (bool, optional): Если `True`, перезаписывает существующие файлы. По умолчанию `False`.

**Возвращает**:
- `List[Path]`: Список путей к сгенерированным PNG-изображениям.

**Как работает функция**:
Функция принимает список текстовых строк и генерирует PNG-изображения для каждой строки. Сначала она настраивает логирование и определяет параметры, такие как размер холста и отступ. Затем для каждой строки генерируется PNG-изображение с помощью метода `generate_png`. Если файл уже существует и параметр `clobber` установлен в `False`, изображение не генерируется, и выводится предупреждение. Сгенерированные изображения сохраняются в указанной директории, и их пути добавляются в список, который возвращается в конце.

**Примеры**:
```python
generator = TextToImageGenerator()
lines = ["Текст 1", "Текст 2", "Текст 3"]
output_dir = "./output"
images = await generator.generate_images(lines, output_dir=output_dir)
print(images)
# Ожидаемый результат:
# [PosixPath('./output/Текст 1.png'), PosixPath('./output/Текст 2.png'), PosixPath('./output/Текст 3.png')]
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
    ...
```

**Назначение**: Создает PNG-изображение с заданным текстом, шрифтом и цветами.

**Параметры**:
- `text` (str): Текст для отображения на изображении.
- `canvas_size` (Tuple[int, int]): Размер холста в пикселях.
- `padding` (float): Процент отступа для использования в качестве границы.
- `background_color` (str): Цвет фона изображения.
- `text_color` (str): Цвет текста.
- `font` (str | ImageFont.ImageFont): Шрифт для использования в тексте.

**Возвращает**:
- `Image`: Сгенерированное PNG-изображение.

**Как работает функция**:
Функция создает новое изображение с заданным размером и цветом фона. Затем она использует библиотеку Pillow для рисования текста на изображении с заданным шрифтом и цветом. Функция вычисляет позицию текста, чтобы центрировать его на холсте, и возвращает сгенерированное изображение.

**Примеры**:
```python
generator = TextToImageGenerator()
text = "Пример текста"
canvas_size = (512, 512)
padding = 0.05
background_color = "lightgray"
text_color = "darkblue"
font = "arial.ttf"
image = generator.generate_png(text, canvas_size, padding, background_color, text_color, font)
image.save("example.png")
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
    ...
```

**Назначение**: Вычисляет позицию для центрирования текста на холсте.

**Параметры**:
- `draw` (ImageDraw.Draw): Экземпляр `ImageDraw`.
- `text` (str): Текст для отображения.
- `font` (ImageFont.ImageFont): Шрифт, используемый для текста.
- `canvas_size` (Tuple[int, int]): Размер холста в пикселях.

**Возвращает**:
- `Tuple[int, int]`: Координаты для центрирования текста.

**Как работает функция**:
Функция вычисляет ширину и высоту текста с использованием заданного шрифта. Затем она вычисляет координаты для центрирования текста на холсте, вычитая половину ширины и высоты текста из половины ширины и высоты холста соответственно. Возвращает полученные координаты.

**Примеры**:
```python
from PIL import Image, ImageDraw, ImageFont

generator = TextToImageGenerator()
image = Image.new("RGB", (512, 512), "white")
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("arial.ttf", size=32)
text = "Пример текста"
canvas_size = (512, 512)
x, y = generator.center_text_position(draw, text, font, canvas_size)
print(f"Координаты для центрирования текста: x={x}, y={y}")
# Ожидаемый результат: Координаты будут зависеть от размера текста и шрифта.
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
    ...
```

**Назначение**: Накладывает одно PNG-изображение поверх другого в заданной позиции.

**Параметры**:
- `background_path` (str | Path): Путь к фоновому PNG-изображению.
- `overlay_path` (str | Path): Путь к накладываемому PNG-изображению.
- `position` (tuple[int, int], optional): Координаты (x, y), где будет размещено накладываемое изображение. По умолчанию (0, 0).
- `alpha` (float, optional): Уровень прозрачности накладываемого изображения (0.0 - 1.0). По умолчанию 1.0.

**Возвращает**:
- `Image`: Результирующее изображение с наложенным изображением.

**Как работает функция**:
Функция открывает фоновое и накладываемое изображения, преобразуя их в формат RGBA. Если размеры накладываемого изображения не совпадают с размерами фонового изображения, оно изменяется до размеров фонового изображения. Затем функция изменяет прозрачность накладываемого изображения в соответствии с заданным уровнем прозрачности (`alpha`) и накладывает его на фоновое изображение в указанной позиции.

**Примеры**:
```python
generator = TextToImageGenerator()
background_path = "background.png"
overlay_path = "overlay.png"
result_image = generator.overlay_images(background_path, overlay_path, position=(50, 50), alpha=0.8)
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
        webp2png(\'image.webp\', \'image.png\')
    """
    ...
```

**Назначение**: Конвертирует изображение в формате WEBP в формат PNG.

**Параметры**:
- `webp_path` (str): Путь к входному файлу WEBP.
- `png_path` (str): Путь для сохранения конвертированного файла PNG.

**Возвращает**:
- `bool`: `True`, если конвертация прошла успешно, иначе `False`.

**Как работает функция**:
Функция открывает изображение в формате WEBP, используя библиотеку Pillow. Затем она сохраняет изображение в формате PNG по указанному пути. Если в процессе конвертации возникает ошибка, функция выводит сообщение об ошибке и возвращает `False`.

**Примеры**:
```python
webp2png('image.webp', 'image.png')