### **Анализ кода модуля `src.utils.convertors.png`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Код хорошо структурирован и разбит на классы и функции, что облегчает понимание и поддержку.
  - Имеется базовая документация для классов и функций.
  - Используется logging для отслеживания ошибок и предупреждений.
- **Минусы**:
  - Не все функции и методы имеют подробные docstring, особенно внутренние методы классов.
  - Не хватает аннотаций типов для переменных в `__init__`.
  - Отсутствует обработка исключений для некоторых операций, например, при работе с файлами.
  - docstring написан на английском языке. Необходимо перевести на русский.
  - Есть `print` вместо `logger.error`.
  - Не везде используется `self`.

#### **Рекомендации по улучшению**:
1. **Документирование**:
   - Добавить подробные docstring для всех функций и методов, включая описание параметров, возвращаемых значений и возможных исключений.
   - Перевести существующие docstring на русский язык.
   - Добавить примеры использования в docstring.

2. **Аннотации типов**:
   - Добавить аннотации типов для всех переменных в `__init__`, чтобы улучшить читаемость и облегчить отладку.

3. **Обработка исключений**:
   - Добавить обработку исключений для всех операций, которые могут вызвать ошибки, например, при работе с файлами или при вызове сторонних библиотек.
   - Использовать `logger.error` для логирования ошибок вместо `print`.

4. **Использовать `logger` вместо `print`**:
   - Заменить все `print` на `logger.info` или `logger.error` в зависимости от ситуации.

5. **Форматирование кода**:
   - Исправить использование `self` на `cls`

6. **Общая структура**:
   - В файле отсутствует стандартный заголовок модуля, содержащий информацию о назначении модуля, авторе и т. д.
   - Добавить заголовок с информацией о модуле.

#### **Оптимизированный код**:

```python
## \file /src/utils/convertors/png.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для конвертации текста в PNG изображения.
==================================================

Модуль предоставляет класс :class:`TextToImageGenerator`, который позволяет генерировать PNG изображения из текста,
сохраненного построчно в файле или переданного в виде списка строк.

Функциональность включает настройку шрифта, размера изображения, отступов, цветов фона и текста.
Также поддерживается наложение одного изображения на другое.

Пример использования:
----------------------

>>> generator = TextToImageGenerator()
>>> lines = ["Текст 1", "Текст 2", "Текст 3"]
>>> output_dir = "./output"
>>> images = await generator.generate_images(lines, output_dir=output_dir)
>>> print(images)
[PosixPath(\'./output/Текст 1.png\'), PosixPath(\'./output/Текст 2.png\'), PosixPath(\'./output/Текст 3.png\')]

.. module:: src.utils.convertors.png
"""

from pathlib import Path
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont
from src.logger.logger import logger  # Logging


class TextToImageGenerator:
    """
    Класс для генерации PNG изображений из текста.

    **Методы**:
    - `assign_path`: Определяет корректный путь для выходных PNG файлов, создавая директорию при необходимости.
    - `center_text_position`: Вычисляет позицию для центрирования текста на холсте.
    - `generate_png`: Создает PNG изображение с заданным текстом, шрифтом, цветами и т.д.
    - `not_comment_or_blank`: Проверяет, является ли строка комментарием или пустой.
    - `which_exist`: Проверяет, какие имена файлов уже существуют в директории.
    - `get_characters`: Извлекает текстовые строки из входного файла или списка, отфильтровывая комментарии и пустые строки.
    - `parse_size`: Преобразует строку в объект `Size`.
    - `get_max_text_size`: Вычисляет максимальный размер текста на основе шрифта и текстовых строк.
    - `get_font`: Определяет размер шрифта на основе размера холста и отступов.
    - `setup_logging`: Настраивает логирование на основе заданного уровня логирования.
    - `error`: Регистрирует сообщение об ошибке и вызывает исключение.
    - `overlay_images`: Накладывает одно PNG изображение поверх другого.
    """

    def __init__(self):
        """
        Инициализирует класс TextToImageGenerator с настройками по умолчанию.
        """
        self.default_output_dir: Path = Path("./output")
        self.default_canvas_size: Tuple[int, int] = (1024, 1024)
        self.default_padding: float = 0.10
        self.default_background: str = "white"
        self.default_text_color: str = "black"
        self.default_log_level: str = "WARNING"

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
        Генерирует PNG изображения из предоставленных текстовых строк.

        Args:
            lines (List[str]): Список строк, содержащих текст для генерации изображений.
            output_dir (str | Path, optional): Директория для сохранения выходных изображений. По умолчанию "./output".
            font (str | ImageFont.ImageFont, optional): Шрифт для использования в тексте. По умолчанию "sans-serif".
            canvas_size (Tuple[int, int], optional): Размер холста в пикселях. По умолчанию (1024, 1024).
            padding (float, optional): Процент от размера холста для использования в качестве границы. По умолчанию 0.10.
            background_color (str, optional): Цвет фона для изображений. По умолчанию "white".
            text_color (str, optional): Цвет текста. По умолчанию "black".
            log_level (int | str | bool, optional): Уровень детализации логирования. По умолчанию "WARNING".
            clobber (bool, optional): Если True, перезаписывает существующие файлы. По умолчанию False.

        Returns:
            List[Path]: Список путей к сгенерированным PNG изображениям.

        Example:
            >>> generator = TextToImageGenerator()
            >>> lines = ["Текст 1", "Текст 2", "Текст 3"]
            >>> output_dir = "./output"
            >>> images = await generator.generate_images(lines, output_dir=output_dir)
            >>> print(images)
            [PosixPath(\'./output/Текст 1.png\'), PosixPath(\'./output/Текст 2.png\'), PosixPath(\'./output/Текст 3.png\')]
        """
        output_directory: Path = Path(output_dir) if output_dir else self.default_output_dir
        self.setup_logging(level=log_level)

        if not canvas_size:
            canvas_size = self.default_canvas_size

        if not padding:
            padding = self.default_padding

        generated_images: List[Path] = []
        for line in lines:
            img_path: Path = output_directory / f"{line}.png"
            if img_path.exists() and not clobber:
                logger.warning(f"File {img_path} already exists. Skipping...")
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
        Создает PNG изображение с заданным текстом, шрифтом и цветами.

        Args:
            text (str): Текст для отображения на изображении.
            canvas_size (Tuple[int, int]): Размер холста в пикселях.
            padding (float): Процент отступа для использования в качестве границы.
            background_color (str): Цвет фона изображения.
            text_color (str): Цвет текста.
            font (str | ImageFont.ImageFont): Шрифт для использования в тексте.

        Returns:
            Image: Сгенерированное PNG изображение.
        """
        img: Image = Image.new("RGB", canvas_size, background_color)
        draw: ImageDraw.Draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font, size=self.get_font_size(canvas_size, padding))

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
            text (str): Текст для отображения.
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
        """Накладывает одно PNG изображение поверх другого в указанной позиции.

        Args:
            background_path (str | Path): Путь к фоновому PNG изображению.
            overlay_path (str | Path): Путь к PNG изображению для наложения.
            position (tuple[int, int], optional): (x, y) координаты, где будет размещено наложение. По умолчанию (0, 0).
            alpha (float, optional): Уровень прозрачности накладываемого изображения (0.0 - 1.0). По умолчанию 1.0.

        Returns:
            Image: Результирующее изображение с наложением.

        Example:
            >>> result_image = overlay_images("background.png", "overlay.png", position=(50, 50), alpha=0.8)
            >>> result_image.save("result.png")
        """
        # Открываем фоновое и накладываемое изображения
        background: Image = Image.open(background_path).convert("RGBA")
        overlay: Image = Image.open(overlay_path).convert("RGBA")

        # Изменяем размер накладываемого изображения, чтобы соответствовать фоновому, если необходимо
        if overlay.size != background.size:
            overlay = overlay.resize(background.size, Image.ANTIALIAS)

        # Настраиваем прозрачность накладываемого изображения
        overlay = overlay.copy()
        overlay.putalpha(int(alpha * 255))

        # Вставляем накладываемое изображение на фон
        background.paste(overlay, position, overlay)

        return background


def webp2png(webp_path: str, png_path: str) -> bool:
    """
    Конвертирует изображение в формате WEBP в формат PNG.

    Args:
        webp_path (str): Путь к входному WEBP файлу.
        png_path (str): Путь для сохранения сконвертированного PNG файла.

    Returns:
        bool: True в случае успешной конвертации, False в случае ошибки.

    Example:
        webp2png(\'image.webp\', \'image.png\')
    """
    try:
        # Открываем webp изображение
        with Image.open(webp_path) as img:
            # Конвертируем в PNG и сохраняем
            img.save(png_path, 'PNG')
        return True
    except Exception as ex:
        logger.error(f"Error during conversion: {ex}", ex, exc_info=True)
        return False