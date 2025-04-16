### Анализ кода модуля `hypotez/src/utils/convertors/png.py`

## Обзор

Этот модуль предоставляет утилиты для работы с изображениями в формате PNG, включая функции для создания PNG-изображений из текста и наложения одного изображения на другое.

## Подробнее

Модуль содержит класс `TextToImageGenerator`, предназначенный для генерации PNG-изображений из текстовых строк, а также функции для добавления водяных знаков и преобразования изображений.

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

    def __init__(self):
        """
        Initializes the TextToImageGenerator class with default settings.
        """
        self.default_output_dir = Path("./output")
        self.default_canvas_size = (1024, 1024)
        self.default_padding = 0.10
        self.default_background = "white"
        self.default_text_color = "black"
        self.default_log_level = "WARNING"
    ...
```

**Описание**:
Класс `TextToImageGenerator` предназначен для генерации PNG-изображений из текстовых строк.

**Атрибуты**:
- `default_output_dir` (Path): Путь к директории вывода по умолчанию (./output).
- `default_canvas_size` (Tuple[int, int]): Размер холста по умолчанию (1024x1024).
- `default_padding` (float): Отступ по умолчанию (10%).
- `default_background` (str): Цвет фона по умолчанию ("white").
- `default_text_color` (str): Цвет текста по умолчанию ("black").
- `default_log_level` (str): Уровень логирования по умолчанию ("WARNING").

**Методы**:

*   `__init__(self)`: Инициализирует объект `TextToImageGenerator` со значениями по умолчанию.
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
- `webp_path` (str): Путь к входному файлу WEBP.
- `png_path` (str): Путь для сохранения преобразованного PNG-файла.

**Возвращает**:
- `bool`: True в случае успеха, False в противном случае.

**Как работает функция**:
1.  Открывает изображение в формате WEBP с использованием `Image.open`.
2.  Сохраняет изображение в формате PNG с использованием `img.save`.

**Примеры**:

```python
webp2png('image.webp', 'image.png')
```

### `generate_images`
```python
async def generate_images(
        self,
        lines: List[str],\n        output_dir: str | Path = None,\n        font: str | ImageFont.ImageFont = "sans-serif",\n        canvas_size: Tuple[int, int] = None,\n        padding: float = None,\n        background_color: str = None,\n        text_color: str = None,\n        log_level: int | str | bool = None,\n        clobber: bool = False,\n    ) -> List[Path]:
    """\n    Generates PNG images from the provided text lines.\n\n    Args:\n        lines (List[str]): A list of strings containing the text to generate images from.\n        output_dir (str | Path, optional): Directory to save the output images. Defaults to "./output".\n        font (str | ImageFont.ImageFont, optional): Font to use for the text. Defaults to "sans-serif".\n        canvas_size (Tuple[int, int], optional): Size of the canvas in pixels. Defaults to (1024, 1024).\n        padding (float, optional): Percentage of canvas size to use as a blank border. Defaults to 0.10.\n        background_color (str, optional): Background color for the images. Defaults to "white".\n        text_color (str, optional): Color of the text. Defaults to "black".\n        log_level (int | str | bool, optional): Logging verbosity level. Defaults to "WARNING".\n        clobber (bool, optional): If True, overwrites existing files. Defaults to False.\n\n    Returns:\n        List[Path]: A list of paths to the generated PNG images.\n\n    Example:\n        >>> generator = TextToImageGenerator()\n        >>> lines = ["Text 1", "Text 2", "Text 3"]\n        >>> output_dir = "./output"\n        >>> images = await generator.generate_images(lines, output_dir=output_dir)\n        >>> print(images)\n        [PosixPath(\'./output/Text 1.png\'), PosixPath(\'./output/Text 2.png\'), PosixPath(\'./output/Text 3.png\')]\n    """
```

**Назначение**:
Генерирует PNG-изображения из предоставленных текстовых строк.

**Параметры**:
-   `lines` (List[str]): Список строк, содержащих текст для создания изображений.
-   `output_dir` (str | Path, optional): Директория для сохранения выходных изображений. По умолчанию "./output".
-   `font` (str | ImageFont.ImageFont, optional): Шрифт для использования в тексте. По умолчанию "sans-serif".
-   `canvas_size` (Tuple[int, int], optional): Размер холста в пикселях. По умолчанию (1024, 1024).
-   `padding` (float, optional): Процент размера холста для использования в качестве пустой границы. По умолчанию 0.10.
-   `background_color` (str, optional): Цвет фона для изображений. По умолчанию "white".
-   `text_color` (str, optional): Цвет текста. По умолчанию "black".
-   `log_level` (int | str | bool, optional): Уровень детализации логирования. По умолчанию "WARNING".
-   `clobber` (bool, optional): Если True, перезаписывает существующие файлы. По умолчанию False.

**Возвращает**:
-   `List[Path]`: Список путей к сгенерированным PNG-изображениям.

**Как работает функция**:

1.  Определяет путь к директории вывода.
2.  Настраивает логирование.
3.  Инициализирует размеры холста и отступы.
4.  Перебирает все строки в списке `lines` и для каждой строки:
    *   Формирует имя файла для изображения.
    *   Проверяет, существует ли файл, и если существует и `clobber` равен `False`, пропускает итерацию.
    *   Вызывает `self.generate_png` для создания изображения с текущей строкой.
    *   Сохраняет изображение в указанный путь.
    *   Добавляет путь к созданному изображению в список `generated_images`.
5.  Возвращает список путей к созданным изображениям.

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

**Назначение**:
Создает PNG-изображение с указанным текстом, шрифтом и цветами.

**Параметры**:

-   `text` (str): Текст для рендеринга на изображении.
-   `canvas_size` (Tuple[int, int]): Размер холста в пикселях.
-   `padding` (float): Процент отступа, используемый в качестве границы.
-   `background_color` (str): Цвет фона изображения.
-   `text_color` (str): Цвет текста.
-   `font` (str | ImageFont.ImageFont): Шрифт для использования в тексте.

**Возвращает**:

-   `Image`: Сгенерированное PNG-изображение.

**Как работает функция**:

1.  Создает новое изображение RGB с указанным размером холста и цветом фона.
2.  Создает объект `ImageDraw` для рисования на изображении.
3.  Определяет размер шрифта на основе размера холста и отступа.
4.  Определяет позицию текста для центрирования на изображении.
5.  Рисует текст на изображении с указанными параметрами.
6.  Возвращает сгенерированное изображение.

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

**Назначение**:
Вычисляет позицию для центрирования текста на холсте.

**Параметры**:

-   `draw` (ImageDraw.Draw): Экземпляр `ImageDraw` для рисования.
-   `text` (str): Текст, который нужно отрендерить.
-   `font` (ImageFont.ImageFont): Шрифт, используемый для текста.
-   `canvas_size` (Tuple[int, int]): Размер холста в пикселях.

**Возвращает**:

-   `Tuple[int, int]`: Координаты для центрирования текста.

**Как работает функция**:

1.  Измеряет ширину и высоту текста с использованием указанного шрифта.
2.  Вычисляет координаты x и y для центрирования текста на холсте.
3.  Возвращает вычисленные координаты.

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

**Назначение**:
Накладывает одно PNG-изображение поверх другого в указанной позиции.

**Параметры**:

-   `background_path` (str | Path): Путь к фоновому PNG-изображению.
-   `overlay_path` (str | Path): Путь к PNG-изображению для наложения.
-   `position` (tuple[int, int], optional): (x, y) координаты, где будет размещено наложение. По умолчанию (0, 0).
-   `alpha` (float, optional): Уровень прозрачности наложенного изображения (0.0 - 1.0). По умолчанию 1.0.

**Возвращает**:

-   `Image`: Полученное изображение с наложением.

**Как работает функция**:

1.  Открывает фоновое и наложенное изображения с использованием `Image.open`.
2.  Преобразует наложенное изображение в формат RGBA.
3.  Изменяет размер наложенного изображения в соответствии с размером фонового, если это необходимо.
4.  Устанавливает прозрачность наложенного изображения на основе значения `alpha`.
5.  Вставляет наложенное изображение поверх фонового в указанной позиции.
6.  Возвращает результирующее изображение.

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
- `webp_path` (str): Путь к входному файлу WEBP.
- `png_path` (str): Путь для сохранения преобразованного PNG-файла.

**Возвращает**:
- `bool`: True в случае успеха, False в противном случае.

**Как работает функция**:
1.  Открывает изображение в формате WEBP с использованием `Image.open`.
2.  Сохраняет изображение в формате PNG с использованием `img.save`.

## Переменные

### `default_output_dir`

```python
self.default_output_dir = Path("./output")
```

Путь к директории вывода по умолчанию ("./output").

### `default_canvas_size`

```python
self.default_canvas_size = (1024, 1024)
```

Размер холста по умолчанию (1024x1024 пикселей).

### `default_padding`

```python
self.default_padding = 0.10
```

Отступ по умолчанию в процентах от размера холста (10%).

### `default_background`

```python
self.default_background = "white"
```

Цвет фона по умолчанию ("white").

### `default_text_color`

```python
self.default_text_color = "black"
```

Цвет текста по умолчанию ("black").

### `default_log_level`

```python
self.default_log_level = "WARNING"
```

Уровень логирования по умолчанию ("WARNING").

## Запуск

Для использования этого модуля необходимо установить библиотеку `Pillow`.

```bash
pip install Pillow
```

Пример использования:

```python
from src.utils.convertors.png import TextToImageGenerator
from pathlib import Path

async def main():
    generator = TextToImageGenerator()
    lines = ["Text 1", "Text 2", "Text 3"]
    output_dir = "./output"
    images = await generator.generate_images(lines, output_dir=output_dir)
    print(images)