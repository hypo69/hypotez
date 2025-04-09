### **Анализ кода модуля `png.py`**

## \file /src/utils/convertors/png.py

Модуль содержит класс `TextToImageGenerator` для генерации PNG изображений из текста, а также функцию `webp2png` для конвертации изображений из формата WEBP в PNG.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Хорошая структура класса `TextToImageGenerator`, разделение функциональности на отдельные методы.
    - Использование аннотаций типов.
    - Наличие docstring для большинства методов.
    - Использование `logger` для логирования.
- **Минусы**:
    - Не все методы имеют docstring.
    - Отсутствуют проверки типов для входных параметров (например, проверка, что `canvas_size` - это кортеж целых чисел).
    - В функции `webp2png` используется `print` вместо `logger.error` для логирования ошибок.
    - docstring на английском языке.
    - Не везде добавлены аннотации типа.
    - Не используется `j_loads` или `j_loads_ns`.

**Рекомендации по улучшению:**

1.  **Добавить docstring для всех методов и классов**, включая описание параметров, возвращаемых значений и возможных исключений.
2.  **Перевести все docstring на русский язык.**
3.  **Добавить проверки типов** для входных параметров, чтобы убедиться, что они соответствуют ожидаемым типам.
4.  **Использовать `logger.error` вместо `print`** для логирования ошибок в функции `webp2png`.
5.  **Добавить аннотации типов** для всех переменных и параметров функций.
6.  **Улучшить обработку исключений** в функции `webp2png`, чтобы логировать более подробную информацию об ошибке.
7.  **Добавить примеры использования** для всех функций и методов.
8.  **Использовать одинарные кавычки** вместо двойных.
9.  **Для всех путей использовать `Path`** из `pathlib`.

**Оптимизированный код:**

```python
## \file /src/utils/convertors/png.py
# -*- coding: utf-8 -*

#! .pyenv/bin/python3

"""
Модуль для работы с конвертацией изображений в формат PNG
=========================================================

Модуль содержит класс :class:`TextToImageGenerator`, который используется для генерации PNG изображений из текста,
а также функцию :func:`webp2png` для конвертации изображений из формата WEBP в PNG.

Пример использования
----------------------

>>> generator = TextToImageGenerator()
>>> lines = ["Текст 1", "Текст 2", "Текст 3"]
>>> output_dir = "./output"
>>> images = await generator.generate_images(lines, output_dir=output_dir)
>>> print(images)
[PosixPath('./output/Текст 1.png'), PosixPath('./output/Текст 2.png'), PosixPath('./output/Текст 3.png')]
"""

from pathlib import Path
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont
from src.logger.logger import logger  # Logging


class TextToImageGenerator:
    """
    Класс для генерации PNG изображений из текста.

    **Методы**:\n
    - `assign_path`: Определяет корректный путь для выходных PNG файлов, создавая директорию при необходимости.
    - `center_text_position`: Вычисляет позицию для центрирования текста на холсте.
    - `generate_png`: Создает PNG изображение с указанным текстом, шрифтом, цветами и т.д.
    - `not_comment_or_blank`: Проверяет, является ли строка комментарием или пустой.
    - `which_exist`: Проверяет, какие имена файлов уже существуют в директории.
    - `get_characters`: Извлекает текстовые строки из входного файла или списка, фильтруя комментарии и пустые строки.
    - `parse_size`: Преобразует строку в объект `Size`.
    - `get_max_text_size`: Вычисляет максимальный размер текста на основе шрифта и текстовых строк.
    - `get_font`: Определяет размер шрифта на основе размера холста и отступов.
    - `setup_logging`: Настраивает логирование на основе указанного уровня логирования.
    - `error`: Логирует сообщение об ошибке и вызывает исключение.
    - `overlay_images`: Накладывает одно PNG изображение поверх другого.
    """

    def __init__(self) -> None:
        """
        Инициализирует класс TextToImageGenerator с настройками по умолчанию.
        """
        self.default_output_dir: Path = Path('./output')
        self.default_canvas_size: Tuple[int, int] = (1024, 1024)
        self.default_padding: float = 0.10
        self.default_background: str = 'white'
        self.default_text_color: str = 'black'
        self.default_log_level: str = 'WARNING'

    async def generate_images(
        self,
        lines: List[str],
        output_dir: str | Path | None = None,
        font: str | ImageFont.ImageFont = 'sans-serif',
        canvas_size: Tuple[int, int] | None = None,
        padding: float | None = None,
        background_color: str | None = None,
        text_color: str | None = None,
        log_level: int | str | bool | None = None,
        clobber: bool = False,
    ) -> List[Path]:
        """
        Генерирует PNG изображения из предоставленных текстовых строк.

        Args:
            lines (List[str]): Список строк, содержащих текст для генерации изображений.
            output_dir (str | Path | None, optional): Директория для сохранения выходных изображений. По умолчанию './output'.
            font (str | ImageFont.ImageFont, optional): Шрифт для использования в тексте. По умолчанию 'sans-serif'.
            canvas_size (Tuple[int, int] | None, optional): Размер холста в пикселях. По умолчанию (1024, 1024).
            padding (float | None, optional): Процент от размера холста, используемый в качестве пустой границы. По умолчанию 0.10.
            background_color (str | None, optional): Цвет фона для изображений. По умолчанию 'white'.
            text_color (str | None, optional): Цвет текста. По умолчанию 'black'.
            log_level (int | str | bool | None, optional): Уровень детализации логирования. По умолчанию 'WARNING'.
            clobber (bool, optional): Если True, перезаписывает существующие файлы. По умолчанию False.

        Returns:
            List[Path]: Список путей к сгенерированным PNG изображениям.

        Example:
            >>> generator = TextToImageGenerator()
            >>> lines = ["Текст 1", "Текст 2", "Текст 3"]
            >>> output_dir = "./output"
            >>> images = await generator.generate_images(lines, output_dir=output_dir)
            >>> print(images)
            [PosixPath('./output/Текст 1.png'), PosixPath('./output/Текст 2.png'), PosixPath('./output/Текст 3.png')]
        """
        output_directory: Path = Path(output_dir) if output_dir else self.default_output_dir
        self.setup_logging(level=log_level)

        if not canvas_size:
            canvas_size = self.default_canvas_size

        if not padding:
            padding = self.default_padding

        generated_images: List[Path] = []
        for line in lines:
            img_path: Path = output_directory / f'{line}.png'
            if img_path.exists() and not clobber:
                logger.warning(f'Файл {img_path} уже существует. Пропускаем...')
                continue
            img: Image = self.generate_png(line, canvas_size, padding, background_color, text_color, font)
            img.save(img_path)
            generated_images.append(img_path)

        return generated_images

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
        Создает PNG изображение с указанным текстом, шрифтом и цветами.

        Args:
            text (str): Текст для рендеринга на изображении.
            canvas_size (Tuple[int, int]): Размер холста в пикселях.
            padding (float): Процент отступа, используемый в качестве границы.
            background_color (str): Цвет фона изображения.
            text_color (str): Цвет текста.
            font (str | ImageFont.ImageFont): Шрифт для использования в тексте.

        Returns:
            Image: Сгенерированное PNG изображение.
        """
        img: Image = Image.new('RGB', canvas_size, background_color)
        draw: ImageDraw.Draw = ImageDraw.Draw(img)
        font: ImageFont.ImageFont = ImageFont.truetype(font, size=self.get_font_size(canvas_size, padding))

        text_position: Tuple[int, int] = self.center_text_position(draw, text, font, canvas_size)
        draw.text(text_position, text, fill=text_color, font=font)

        return img

    def center_text_position(
        self, draw: ImageDraw.Draw, text: str, font: ImageFont.ImageFont, canvas_size: Tuple[int, int]
    ) -> Tuple[int, int]:
        """
        Вычисляет позицию для центрирования текста на холсте.

        Args:
            draw (ImageDraw.Draw): Экземпляр ImageDraw.
            text (str): Текст, который нужно отобразить.
            font (ImageFont.ImageFont): Шрифт, используемый для текста.
            canvas_size (Tuple[int, int]): Размер холста в пикселях.

        Returns:
            Tuple[int, int]: Координаты для центрирования текста.
        """
        text_width: int
        text_height: int
        text_width, text_height = draw.textsize(text, font=font)
        return (canvas_size[0] - text_width) // 2, (canvas_size[1] - text_height) // 2

    def overlay_images(
        self,
        background_path: str | Path,
        overlay_path: str | Path,
        position: tuple[int, int] = (0, 0),
        alpha: float = 1.0,
    ) -> Image:
        """
        Накладывает одно PNG изображение поверх другого в указанной позиции.

        Args:
            background_path (str | Path): Путь к фоновому PNG изображению.
            overlay_path (str | Path): Путь к накладываемому PNG изображению.
            position (tuple[int, int], optional): (x, y) координаты, где будет размещено наложение. По умолчанию (0, 0).
            alpha (float, optional): Уровень прозрачности накладываемого изображения (0.0 - 1.0). По умолчанию 1.0.

        Returns:
            Image: Результирующее изображение с наложением.

        Example:
            >>> result_image = overlay_images("background.png", "overlay.png", position=(50, 50), alpha=0.8)
            >>> result_image.save("result.png")
        """
        # Открываем фоновое и накладываемое изображения
        background: Image = Image.open(background_path).convert('RGBA')
        overlay: Image = Image.open(overlay_path).convert('RGBA')

        # Изменяем размер накладываемого изображения, чтобы соответствовать фоновому, если это необходимо
        if overlay.size != background.size:
            overlay = overlay.resize(background.size, Image.ANTIALIAS)

        # Настраиваем прозрачность накладываемого изображения
        overlay = overlay.copy()
        overlay.putalpha(int(alpha * 255))

        # Вставляем накладываемое изображение на фон
        background.paste(overlay, position, overlay)

        return background


def webp2png(webp_path: str, png_path: str) -> bool | None:
    """
    Конвертирует изображение из формата WEBP в PNG.

    Args:
        webp_path (str): Путь к входному WEBP файлу.
        png_path (str): Путь для сохранения конвертированного PNG файла.

    Returns:
        bool | None: True, если конвертация прошла успешно, None в случае ошибки.

    Example:
        webp2png('image.webp', 'image.png')
    """
    try:
        # Открываем WEBP изображение
        with Image.open(webp_path) as img:
            # Конвертируем в PNG и сохраняем
            img.save(png_path, 'PNG')
        return True
    except Exception as ex:
        logger.error('Ошибка во время конвертации', ex, exc_info=True)
        return None