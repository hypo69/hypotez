# Модуль для конвертации PNG-изображений

## Обзор

Модуль `src.utils.convertors.png` предназначен для генерации PNG-изображений из текста, а также для наложения одного PNG-изображения на другое и конвертации изображений из формата WEBP в PNG. Он предоставляет класс `TextToImageGenerator` для создания изображений из текста и функцию `webp2png` для конвертации файлов.

## Подробнее

Модуль содержит класс `TextToImageGenerator`, который используется для создания PNG-изображений на основе предоставленных текстовых строк. Он позволяет настраивать размер холста, шрифт, цвет фона и текста, а также добавлять отступы. Также модуль включает функцию `webp2png`, которая конвертирует изображения из формата WEBP в PNG.

## Классы

### `TextToImageGenerator`

**Описание**: Класс для генерации PNG-изображений из текстовых строк.

**Атрибуты**:
- `default_output_dir` (Path): Путь к директории вывода по умолчанию (./output).
- `default_canvas_size` (Tuple[int, int]): Размер холста по умолчанию (1024, 1024).
- `default_padding` (float): Отступ по умолчанию (0.10).
- `default_background` (str): Цвет фона по умолчанию ("white").
- `default_text_color` (str): Цвет текста по умолчанию ("black").
- `default_log_level` (str): Уровень логирования по умолчанию ("WARNING").

**Методы**:
- `__init__`: Инициализирует класс `TextToImageGenerator` с настройками по умолчанию.
- `generate_images`: Генерирует PNG-изображения из предоставленных текстовых строк.
- `generate_png`: Создает PNG-изображение с указанным текстом, шрифтом и цветами.
- `center_text_position`: Вычисляет позицию для центрирования текста на холсте.
- `overlay_images`: Накладывает одно PNG-изображение на другое в указанной позиции.

**Принцип работы**:
Класс `TextToImageGenerator` предоставляет функциональность для создания PNG-изображений из текста. При инициализации класса устанавливаются значения по умолчанию для различных параметров, таких как директория вывода, размер холста, отступы, цвет фона и текста, а также уровень логирования.

Метод `generate_images` принимает список текстовых строк и генерирует PNG-изображения для каждой строки. Он создает директорию вывода, если она не существует, и сохраняет сгенерированные изображения в этой директории.

Метод `generate_png` создает PNG-изображение с указанным текстом, шрифтом и цветами. Он использует библиотеку Pillow для создания изображения и рисования текста на нем.

Метод `center_text_position` вычисляет позицию для центрирования текста на холсте.

Метод `overlay_images` накладывает одно PNG-изображение на другое в указанной позиции. Он открывает фоновое и накладываемое изображения, изменяет размер накладываемого изображения, если это необходимо, и накладывает его на фоновое изображение.

## Методы класса

### `__init__`

```python
def __init__(self):
    """
    Инициализирует класс TextToImageGenerator с настройками по умолчанию.
    """
    self.default_output_dir = Path("./output")
    self.default_canvas_size = (1024, 1024)
    self.default_padding = 0.10
    self.default_background = "white"
    self.default_text_color = "black"
    self.default_log_level = "WARNING"
```

**Назначение**: Инициализирует экземпляр класса `TextToImageGenerator` с настройками по умолчанию.

**Как работает функция**:
- Устанавливает путь к директории вывода по умолчанию как `./output`.
- Устанавливает размер холста по умолчанию как (1024, 1024).
- Устанавливает отступ по умолчанию как 0.10.
- Устанавливает цвет фона по умолчанию как "white".
- Устанавливает цвет текста по умолчанию как "black".
- Устанавливает уровень логирования по умолчанию как "WARNING".

**Примеры**:

```python
generator = TextToImageGenerator()
print(generator.default_output_dir)  # Вывод: ./output
print(generator.default_canvas_size)  # Вывод: (1024, 1024)
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
    Генерирует PNG-изображения из предоставленных текстовых строк.

    Args:
        lines (List[str]): Список строк с текстом для генерации изображений.
        output_dir (str | Path, optional): Директория для сохранения выходных изображений. По умолчанию "./output".
        font (str | ImageFont.ImageFont, optional): Шрифт для текста. По умолчанию "sans-serif".
        canvas_size (Tuple[int, int], optional): Размер холста в пикселях. По умолчанию (1024, 1024).
        padding (float, optional): Процент от размера холста для использования в качестве границы. По умолчанию 0.10.
        background_color (str, optional): Цвет фона для изображений. По умолчанию "white".
        text_color (str, optional): Цвет текста. По умолчанию "black".
        log_level (int | str | bool, optional): Уровень детализации логирования. По умолчанию "WARNING".
        clobber (bool, optional): Если True, перезаписывает существующие файлы. По умолчанию False.

    Returns:
        List[Path]: Список путей к сгенерированным PNG-изображениям.

    Example:
        >>> generator = TextToImageGenerator()
        >>> lines = ["Text 1", "Text 2", "Text 3"]
        >>> output_dir = "./output"
        >>> images = await generator.generate_images(lines, output_dir=output_dir)
        >>> print(images)
        [PosixPath('./output/Text 1.png'), PosixPath('./output/Text 2.png'), PosixPath('./output/Text 3.png')]
    """
    output_directory = Path(output_dir) if output_dir else self.default_output_dir
    self.setup_logging(level=log_level)

    if not canvas_size:
        canvas_size = self.default_canvas_size

    if not padding:
        padding = self.default_padding

    generated_images = []
    for line in lines:
        img_path = output_directory / f"{line}.png"
        if img_path.exists() and not clobber:
            logger.warning(f"File {img_path} already exists. Skipping...")
            continue
        img = self.generate_png(line, canvas_size, padding, background_color, text_color, font)
        img.save(img_path)
        generated_images.append(img_path)

    return generated_images
```

**Назначение**: Генерирует PNG-изображения из предоставленных текстовых строк.

**Параметры**:
- `lines` (List[str]): Список строк с текстом для генерации изображений.
- `output_dir` (str | Path, optional): Директория для сохранения выходных изображений. По умолчанию "./output".
- `font` (str | ImageFont.ImageFont, optional): Шрифт для текста. По умолчанию "sans-serif".
- `canvas_size` (Tuple[int, int], optional): Размер холста в пикселях. По умолчанию (1024, 1024).
- `padding` (float, optional): Процент от размера холста для использования в качестве границы. По умолчанию 0.10.
- `background_color` (str, optional): Цвет фона для изображений. По умолчанию "white".
- `text_color` (str, optional): Цвет текста. По умолчанию "black".
- `log_level` (int | str | bool, optional): Уровень детализации логирования. По умолчанию "WARNING".
- `clobber` (bool, optional): Если True, перезаписывает существующие файлы. По умолчанию False.

**Возвращает**:
- `List[Path]`: Список путей к сгенерированным PNG-изображениям.

**Как работает функция**:

1. Определяет директорию вывода для сохранения изображений, используя предоставленный `output_dir` или значение по умолчанию (`self.default_output_dir`).
2. Настраивает уровень логирования с помощью метода `self.setup_logging(level=log_level)`.
3. Определяет размер холста, используя предоставленный `canvas_size` или значение по умолчанию (`self.default_canvas_size`).
4. Определяет отступ, используя предоставленный `padding` или значение по умолчанию (`self.default_padding`).
5. Инициализирует пустой список `generated_images` для хранения путей к сгенерированным изображениям.
6. Перебирает каждую строку `line` в предоставленном списке `lines`.
7. Формирует путь `img_path` для сохранения изображения в директории вывода.
8. Проверяет, существует ли файл по пути `img_path` и не установлен ли параметр `clobber` в `False`. Если файл существует и `clobber` равен `False`, то выводит предупреждение в лог и переходит к следующей строке.
9. Если файл не существует или `clobber` равен `True`, то вызывает метод `self.generate_png` для создания PNG-изображения с текущей строкой текста и параметрами холста, отступа, цвета фона, цвета текста и шрифта.
10. Сохраняет сгенерированное изображение по пути `img_path`.
11. Добавляет путь к сгенерированному изображению в список `generated_images`.
12. После перебора всех строк возвращает список `generated_images` с путями к сгенерированным изображениям.

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
    Создает PNG-изображение с указанным текстом, шрифтом и цветами.

    Args:
        text (str): Текст для отображения на изображении.
        canvas_size (Tuple[int, int]): Размер холста в пикселях.
        padding (float): Процент отступа для использования в качестве границы.
        background_color (str): Цвет фона изображения.
        text_color (str): Цвет текста.
        font (str | ImageFont.ImageFont): Шрифт для текста.

    Returns:
        Image: Сгенерированное PNG-изображение.
    """
    img = Image.new("RGB", canvas_size, background_color)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font, size=self.get_font_size(canvas_size, padding))

    text_position = self.center_text_position(draw, text, font, canvas_size)
    draw.text(text_position, text, fill=text_color, font=font)

    return img
```

**Назначение**: Создает PNG-изображение с указанным текстом, шрифтом и цветами.

**Параметры**:
- `text` (str): Текст для отображения на изображении.
- `canvas_size` (Tuple[int, int]): Размер холста в пикселях.
- `padding` (float): Процент отступа для использования в качестве границы.
- `background_color` (str): Цвет фона изображения.
- `text_color` (str): Цвет текста.
- `font` (str | ImageFont.ImageFont): Шрифт для текста.

**Возвращает**:
- `Image`: Сгенерированное PNG-изображение.

**Как работает функция**:

1. Создает новое изображение `img` с указанным размером `canvas_size` и цветом фона `background_color` в формате RGB.
2. Создает объект `draw` для рисования на изображении.
3. Определяет размер шрифта с помощью метода `self.get_font_size(canvas_size, padding)`.
4. Определяет позицию текста на изображении с помощью метода `self.center_text_position(draw, text, font, canvas_size)`.
5. Рисует текст на изображении в указанной позиции, цветом `text_color` и шрифтом `font`.
6. Возвращает сгенерированное изображение `img`.

**Примеры**:

```python
generator = TextToImageGenerator()
text = "Пример текста"
canvas_size = (512, 512)
padding = 0.05
background_color = "lightblue"
text_color = "darkblue"
font = "arial.ttf"

img = generator.generate_png(text, canvas_size, padding, background_color, text_color, font)
img.save("example.png")
```

### `center_text_position`

```python
def center_text_position(
    self, draw: ImageDraw.Draw, text: str, font: ImageFont.ImageFont, canvas_size: Tuple[int, int]
) -> Tuple[int, int]:
    """
    Вычисляет позицию для центрирования текста на холсте.

    Args:
        draw (ImageDraw.Draw): Объект ImageDraw.
        text (str): Текст для отображения.
        font (ImageFont.ImageFont): Используемый шрифт.
        canvas_size (Tuple[int, int]): Размер холста в пикселях.

    Returns:
        Tuple[int, int]: Координаты для центрирования текста.
    """
    text_width, text_height = draw.textsize(text, font=font)
    return (canvas_size[0] - text_width) // 2, (canvas_size[1] - text_height) // 2
```

**Назначение**: Вычисляет позицию для центрирования текста на холсте.

**Параметры**:
- `draw` (ImageDraw.Draw): Объект ImageDraw.
- `text` (str): Текст для отображения.
- `font` (ImageFont.ImageFont): Используемый шрифт.
- `canvas_size` (Tuple[int, int]): Размер холста в пикселях.

**Возвращает**:
- `Tuple[int, int]`: Координаты для центрирования текста.

**Как работает функция**:

1. Вычисляет ширину и высоту текста с помощью метода `draw.textsize(text, font=font)`.
2. Вычисляет координаты для центрирования текста, вычитая ширину и высоту текста из размеров холста и деля результат на 2.
3. Возвращает вычисленные координаты.

**Примеры**:

```python
from PIL import Image, ImageDraw, ImageFont
generator = TextToImageGenerator()
img = Image.new("RGB", (512, 512), "white")
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("arial.ttf", size=32)
text = "Пример текста"
canvas_size = (512, 512)

x, y = generator.center_text_position(draw, text, font, canvas_size)
print(f"x: {x}, y: {y}")
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
    """
    Накладывает одно PNG-изображение на другое в указанной позиции.

    Args:
        background_path (str | Path): Путь к фоновому PNG-изображению.
        overlay_path (str | Path): Путь к накладываемому PNG-изображению.
        position (tuple[int, int], optional): Координаты (x, y), где будет размещено накладываемое изображение. По умолчанию (0, 0).
        alpha (float, optional): Уровень прозрачности накладываемого изображения (0.0 - 1.0). По умолчанию 1.0.

    Returns:
        Image: Результирующее изображение с наложением.

    Example:
        >>> result_image = overlay_images("background.png", "overlay.png", position=(50, 50), alpha=0.8)
        >>> result_image.save("result.png")
    """
    # Открытие фонового и накладываемого изображений
    background = Image.open(background_path).convert("RGBA")
    overlay = Image.open(overlay_path).convert("RGBA")

    # Изменение размера накладываемого изображения для соответствия фоновому, если необходимо
    if overlay.size != background.size:
        overlay = overlay.resize(background.size, Image.ANTIALIAS)

    # Настройка прозрачности накладываемого изображения
    overlay = overlay.copy()
    overlay.putalpha(int(alpha * 255))

    # Вставка накладываемого изображения на фон
    background.paste(overlay, position, overlay)

    return background
```

**Назначение**: Накладывает одно PNG-изображение на другое в указанной позиции.

**Параметры**:
- `background_path` (str | Path): Путь к фоновому PNG-изображению.
- `overlay_path` (str | Path): Путь к накладываемому PNG-изображению.
- `position` (tuple[int, int], optional): Координаты (x, y), где будет размещено накладываемое изображение. По умолчанию (0, 0).
- `alpha` (float, optional): Уровень прозрачности накладываемого изображения (0.0 - 1.0). По умолчанию 1.0.

**Возвращает**:
- `Image`: Результирующее изображение с наложением.

**Как работает функция**:

1. Открывает фоновое и накладываемое изображения, используя библиотеку Pillow, и конвертирует их в формат RGBA.
2. Если размеры накладываемого изображения не совпадают с размерами фонового изображения, изменяет размер накладываемого изображения, чтобы оно соответствовало размерам фонового изображения.
3. Устанавливает прозрачность накладываемого изображения, используя параметр `alpha`.
4. Накладывает накладываемое изображение на фоновое изображение в указанной позиции.
5. Возвращает результирующее изображение.

**Примеры**:

```python
generator = TextToImageGenerator()
background_path = "background.png"
overlay_path = "overlay.png"
position = (50, 50)
alpha = 0.8

result_image = generator.overlay_images(background_path, overlay_path, position, alpha)
result_image.save("result.png")
```

## Функции

### `webp2png`

```python
def webp2png(webp_path: str, png_path: str) -> bool:
    """
    Конвертирует WEBP-изображение в формат PNG.

    Args:
        webp_path (str): Путь к входному WEBP-файлу.
        png_path (str): Путь для сохранения конвертированного PNG-файла.

    Example:
        webp2png('image.webp', 'image.png')
    """
    try:
        # Открытие webp изображения
        with Image.open(webp_path) as img:
            # Конвертация в PNG и сохранение
            img.save(png_path, 'PNG')
        return True
    except Exception as ex:
        print(f"Error during conversion: {ex}")
        return
```

**Назначение**: Конвертирует изображение из формата WEBP в формат PNG.

**Параметры**:
- `webp_path` (str): Путь к входному WEBP-файлу.
- `png_path` (str): Путь для сохранения сконвертированного PNG-файла.

**Возвращает**:
- `bool`: `True`, если конвертация прошла успешно, иначе `None`.

**Как работает функция**:

1. Пытается открыть WEBP-изображение по указанному пути с использованием `Image.open(webp_path)`.
2. Если открытие прошло успешно, сохраняет изображение в формате PNG по указанному пути с использованием `img.save(png_path, 'PNG')`.
3. Возвращает `True`, если конвертация и сохранение прошли успешно.
4. Если в процессе возникают какие-либо исключения, перехватывает их и выводит сообщение об ошибке, используя f-строку и переменную `ex`.
5. Возвращает `None` в случае ошибки.

**Примеры**:

```python
webp2png('image.webp', 'image.png')