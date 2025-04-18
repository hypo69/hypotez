# Модуль `png.py`

## Обзор

Модуль предоставляет функциональность для преобразования текста в изображения формата PNG. Он включает класс `TextToImageGenerator`, который позволяет генерировать изображения PNG на основе заданных строк текста, шрифта, цветов и других параметров. Также модуль содержит функцию `webp2png` для конвертации изображений из формата WEBP в формат PNG.

## Подробней

Модуль `png.py` предоставляет инструменты для автоматической генерации изображений из текстовых данных. Это может быть полезно для создания превью, водяных знаков или динамически генерируемых изображений для веб-сайтов и приложений. Модуль использует библиотеку Pillow (PIL) для работы с изображениями и шрифтами.

## Классы

### `TextToImageGenerator`

**Описание**: Класс предназначен для генерации PNG изображений из текста.

**Принцип работы**:
Класс инициализируется с настройками по умолчанию для размера холста, отступов, цветов фона и текста. Он предоставляет методы для генерации изображений на основе заданных параметров, центрирования текста на холсте и наложения изображений друг на друга.

**Аттрибуты**:
- `default_output_dir` (Path): Путь к директории вывода по умолчанию ("./output").
- `default_canvas_size` (Tuple[int, int]): Размер холста по умолчанию (1024, 1024).
- `default_padding` (float): Отступ от границ холста по умолчанию (0.10).
- `default_background` (str): Цвет фона по умолчанию ("white").
- `default_text_color` (str): Цвет текста по умолчанию ("black").
- `default_log_level` (str): Уровень логирования по умолчанию ("WARNING").

**Методы**:
- `__init__`: Инициализирует экземпляр класса `TextToImageGenerator` значениями по умолчанию.
- `generate_images`: Генерирует PNG изображения из предоставленных строк текста.
- `generate_png`: Создает PNG изображение с заданным текстом, шрифтом и цветами.
- `center_text_position`: Вычисляет позицию для центрирования текста на холсте.
- `overlay_images`: Накладывает одно PNG изображение на другое в заданной позиции.

### `TextToImageGenerator.__init__`

**Описание**: Инициализирует класс `TextToImageGenerator` значениями по умолчанию.

**Параметры**:
- Нет

**Возвращает**:
- Нет

**Примеры**:
```python
generator = TextToImageGenerator()
```

### `TextToImageGenerator.generate_images`

**Описание**: Генерирует PNG изображения из предоставленных строк текста.

**Параметры**:
- `lines` (List[str]): Список строк, содержащих текст для генерации изображений.
- `output_dir` (str | Path, optional): Директория для сохранения выходных изображений. По умолчанию "./output".
- `font` (str | ImageFont.ImageFont, optional): Шрифт для использования в тексте. По умолчанию "sans-serif".
- `canvas_size` (Tuple[int, int], optional): Размер холста в пикселях. По умолчанию (1024, 1024).
- `padding` (float, optional): Процент размера холста для использования в качестве пустой границы. По умолчанию 0.10.
- `background_color` (str, optional): Цвет фона для изображений. По умолчанию "white".
- `text_color` (str, optional): Цвет текста. По умолчанию "black".
- `log_level` (int | str | bool, optional): Уровень детализации логирования. По умолчанию "WARNING".
- `clobber` (bool, optional): Если `True`, перезаписывает существующие файлы. По умолчанию `False`.

**Возвращает**:
- `List[Path]`: Список путей к сгенерированным PNG изображениям.

**Как работает функция**:

1. **Инициализация**:
   - Устанавливает директорию вывода, уровень логирования.
   - Если размер холста или отступ не заданы, использует значения по умолчанию.
2. **Генерация изображений**:
   - Проходит по каждой строке текста в списке `lines`.
   - Формирует путь к файлу изображения на основе текста строки.
   - Проверяет, существует ли файл изображения и нужно ли его перезаписывать. Если файл существует и перезапись не разрешена, пропускает и переходит к следующей строке.
   - Генерирует PNG изображение с помощью метода `self.generate_png`.
   - Сохраняет изображение по указанному пути.
   - Добавляет путь к сгенерированному изображению в список `generated_images`.
3. **Возврат**:
   - Возвращает список путей к сгенерированным изображениям.

```
A: Установка параметров
|
B: Перебор строк текста
|
C: Проверка существования файла
|
D: Генерация PNG изображения
|
E: Сохранение изображения
|
F: Возврат списка путей
```

**Примеры**:

```python
generator = TextToImageGenerator()
lines = ["Текст 1", "Текст 2", "Текст 3"]
output_dir = "./output"
images = await generator.generate_images(lines, output_dir=output_dir)
print(images)
# [PosixPath('./output/Текст 1.png'), PosixPath('./output/Текст 2.png'), PosixPath('./output/Текст 3.png')]
```

### `TextToImageGenerator.generate_png`

**Описание**: Создает PNG изображение с заданным текстом, шрифтом и цветами.

**Параметры**:
- `text` (str): Текст для отображения на изображении.
- `canvas_size` (Tuple[int, int]): Размер холста в пикселях.
- `padding` (float): Процент отступа для использования в качестве границы.
- `background_color` (str): Цвет фона изображения.
- `text_color` (str): Цвет текста.
- `font` (str | ImageFont.ImageFont): Шрифт для использования в тексте.

**Возвращает**:
- `Image`: Сгенерированное PNG изображение.

**Как работает функция**:

1. **Создание изображения**:
   - Создает новое RGB изображение с заданным размером холста и цветом фона.
2. **Подготовка к рисованию**:
   - Создает объект `ImageDraw` для рисования на изображении.
   - Определяет шрифт и размер шрифта с помощью метода `self.get_font_size`.
3. **Определение позиции текста**:
   - Вычисляет позицию для центрирования текста на холсте с помощью метода `self.center_text_position`.
4. **Отрисовка текста**:
   - Рисует текст на изображении с заданным цветом и шрифтом.
5. **Возврат изображения**:
   - Возвращает сгенерированное изображение.

```
A: Создание изображения
|
B: Подготовка к рисованию
|
C: Определение позиции текста
|
D: Отрисовка текста
|
E: Возврат изображения
```

**Примеры**:

```python
generator = TextToImageGenerator()
text = "Пример текста"
canvas_size = (512, 512)
padding = 0.05
background_color = "lightblue"
text_color = "darkblue"
font = "arial.ttf"
image = generator.generate_png(text, canvas_size, padding, background_color, text_color, font)
image.save("example.png")
```

### `TextToImageGenerator.center_text_position`

**Описание**: Вычисляет позицию для центрирования текста на холсте.

**Параметры**:
- `draw` (ImageDraw.Draw): Экземпляр `ImageDraw`.
- `text` (str): Текст для отображения.
- `font` (ImageFont.ImageFont): Шрифт, используемый для текста.
- `canvas_size` (Tuple[int, int]): Размер холста в пикселях.

**Возвращает**:
- `Tuple[int, int]`: Координаты для центрирования текста.

**Как работает функция**:

1. **Измерение размера текста**:
   - Вычисляет ширину и высоту текста с использованием заданного шрифта.
2. **Вычисление позиции**:
   - Вычисляет позицию для центрирования текста по горизонтали и вертикали.
3. **Возврат позиции**:
   - Возвращает кортеж с координатами x и y для центрирования текста.

```
A: Измерение размера текста
|
B: Вычисление позиции
|
C: Возврат позиции
```

**Примеры**:

```python
from PIL import Image, ImageDraw, ImageFont
generator = TextToImageGenerator()
image = Image.new("RGB", (512, 512), "white")
draw = ImageDraw.Draw(image)
text = "Пример текста"
font = ImageFont.truetype("arial.ttf", size=24)
canvas_size = (512, 512)
x, y = generator.center_text_position(draw, text, font, canvas_size)
print(f"Координаты центрирования: x={x}, y={y}")
```

### `TextToImageGenerator.overlay_images`

**Описание**: Накладывает одно PNG изображение на другое в заданной позиции.

**Параметры**:
- `background_path` (str | Path): Путь к фоновому PNG изображению.
- `overlay_path` (str | Path): Путь к накладываемому PNG изображению.
- `position` (tuple[int, int], optional): Координаты (x, y), где будет размещено накладываемое изображение. По умолчанию (0, 0).
- `alpha` (float, optional): Уровень прозрачности накладываемого изображения (0.0 - 1.0). По умолчанию 1.0.

**Возвращает**:
- `Image`: Результирующее изображение с наложенным изображением.

**Как работает функция**:

1. **Открытие изображений**:
   - Открывает фоновое и накладываемое изображения, преобразует их в формат RGBA.
2. **Изменение размера накладываемого изображения**:
   - Если размеры накладываемого изображения не совпадают с размерами фонового изображения, изменяет размер накладываемого изображения, чтобы оно соответствовало размерам фонового изображения.
3. **Настройка прозрачности**:
   - Устанавливает прозрачность накладываемого изображения в соответствии с заданным уровнем `alpha`.
4. **Накладывание изображений**:
   - Накладывает накладываемое изображение на фоновое изображение в заданной позиции.
5. **Возврат результирующего изображения**:
   - Возвращает результирующее изображение.

```
A: Открытие изображений
|
B: Изменение размера накладываемого изображения
|
C: Настройка прозрачности
|
D: Накладывание изображений
|
E: Возврат результирующего изображения
```

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
        webp2png(\'image.webp\', \'image.png\')
    """
    try:
        # Open the webp image
        with Image.open(webp_path) as img:
            # Convert to PNG and save
            img.save(png_path, \'PNG\')
        return True
    except Exception as e:
        print(f"Error during conversion: {e}")
        return
```

**Назначение**: Преобразует изображение из формата WEBP в формат PNG.

**Параметры**:
- `webp_path` (str): Путь к входному WEBP файлу.
- `png_path` (str): Путь для сохранения сконвертированного PNG файла.

**Возвращает**:
- `bool`: `True`, если конвертация прошла успешно, в противном случае возвращает `None`.

**Вызывает исключения**:
- `Exception`: Возникает, если во время конвертации произошла ошибка.

**Как работает функция**:

1. **Открытие WEBP изображения**:
   - Открывает WEBP изображение, используя библиотеку PIL.
2. **Конвертация и сохранение**:
   - Конвертирует изображение в формат PNG и сохраняет его по указанному пути.
3. **Обработка исключений**:
   - Если во время конвертации происходит ошибка, печатает сообщение об ошибке и возвращает `None`.
4. **Возврат значения**:
   - Возвращает `True`, если конвертация выполнена успешно.

```
A: Открытие WEBP изображения
|
B: Конвертация и сохранение
|
C: Обработка исключений
|
D: Возврат значения
```

**Примеры**:

```python
webp2png('image.webp', 'image.png')