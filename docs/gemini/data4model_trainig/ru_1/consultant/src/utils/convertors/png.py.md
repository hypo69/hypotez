### **Анализ кода модуля `png.py`**

## \file /src/utils/convertors/png.py

Модуль содержит класс `TextToImageGenerator` для генерации PNG изображений из текстовых строк, а также функцию `webp2png` для конвертации WEBP изображений в PNG формат.

**Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Хорошая структура кода, разбит на классы и функции.
  - Наличие документации к классам и методам.
  - Использование `logger` для логирования.
- **Минусы**:
  - Не все функции и методы имеют подробное описание в docstring.
  - Встречаются смешанные стили кавычек (использовать только одинарные).
  - Отсутствуют аннотации типов для переменных в `__init__`.
  - Функция `webp2png` использует `print` вместо `logger.error` для логирования ошибок.

**Рекомендации по улучшению**:

1.  **Документация**:
    *   Добавить подробные docstring для всех функций и методов, включая описание параметров и возвращаемых значений.
    *   Перевести существующие docstring на русский язык.
    *   Уточнить, что именно делают функции, избегая общих фраз вроде "получаем" или "делаем".
2.  **Форматирование**:
    *   Заменить двойные кавычки на одинарные.
    *   Добавить аннотации типов для переменных в методе `__init__`.
    *   Использовать пробелы вокруг операторов присваивания.
3.  **Логирование**:
    *   Заменить `print` на `logger.error` в функции `webp2png` для логирования ошибок.
    *   Использовать `ex` вместо `e` в блоках `except`.
4.  **Обработка исключений**:
    *   Добавить более конкретную обработку исключений в функции `webp2png`.
5.  **Типизация**:
    *   Обязательно использовать аннотации типов для всех аргументов функций и возвращаемых значений.
6.  **Комментарии**:
    *   Все комментарии должны быть на русском языке.

**Оптимизированный код**:

```python
## \file /src/utils/convertors/png.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для работы с конвертацией изображений в формат PNG.
===========================================================

Модуль содержит класс :class:`TextToImageGenerator`, который используется для генерации PNG изображений из текстовых строк,
а также функцию :func:`webp2png` для конвертации WEBP изображений в PNG формат.
"""

from pathlib import Path
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont
from src.logger.logger import logger  # Logging


class TextToImageGenerator:
    """
    Класс для генерации PNG изображений из текстовых строк.

    **Функции**:
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
        output_dir: str | Path = None,
        font: str | ImageFont.ImageFont = 'sans-serif',
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
            output_dir (str | Path, optional): Директория для сохранения выходных изображений. По умолчанию './output'.
            font (str | ImageFont.ImageFont, optional): Шрифт, используемый для текста. По умолчанию 'sans-serif'.
            canvas_size (Tuple[int, int], optional): Размер холста в пикселях. По умолчанию (1024, 1024).
            padding (float, optional): Процент от размера холста, используемый в качестве границы. По умолчанию 0.10.
            background_color (str, optional): Цвет фона для изображений. По умолчанию 'white'.
            text_color (str, optional): Цвет текста. По умолчанию 'black'.
            log_level (int | str | bool, optional): Уровень детализации логирования. По умолчанию 'WARNING'.
            clobber (bool, optional): Если True, перезаписывает существующие файлы. По умолчанию False.

        Returns:
            List[Path]: Список путей к сгенерированным PNG изображениям.

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
            img_path = output_directory / f'{line}.png'
            if img_path.exists() and not clobber:
                logger.warning(f'File {img_path} already exists. Skipping...')
                continue
            img = self.generate_png(line, canvas_size, padding, background_color, text_color, font)
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
            text (str): Текст для отображения на изображении.
            canvas_size (Tuple[int, int]): Размер холста в пикселях.
            padding (float): Процент отступа, используемый в качестве границы.
            background_color (str): Цвет фона изображения.
            text_color (str): Цвет текста.
            font (str | ImageFont.ImageFont): Шрифт, используемый для текста.

        Returns:
            Image: Сгенерированное PNG изображение.
        """
        img = Image.new('RGB', canvas_size, background_color)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font, size=self.get_font_size(canvas_size, padding))

        text_position = self.center_text_position(draw, text, font, canvas_size)
        draw.text(text_position, text, fill=text_color, font=font)

        return img

    def center_text_position(
        self, draw: ImageDraw.Draw, text: str, font: ImageFont.ImageFont, canvas_size: Tuple[int, int]
    ) -> Tuple[int, int]:
        """
        Вычисляет позицию для центрирования текста на холсте.

        Args:
            draw (ImageDraw.Draw): Экземпляр ImageDraw.
            text (str): Текст для центрирования.
            font (ImageFont.ImageFont): Шрифт, используемый для текста.
            canvas_size (Tuple[int, int]): Размер холста в пикселях.

        Returns:
            Tuple[int, int]: Координаты для центрирования текста.
        """
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
        background = Image.open(background_path).convert('RGBA')
        overlay = Image.open(overlay_path).convert('RGBA')

        # Изменяем размер накладываемого изображения, чтобы соответствовать фоновому, если необходимо
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
    Конвертирует изображение из формата WEBP в формат PNG.

    Args:
        webp_path (str): Путь к входному WEBP файлу.
        png_path (str): Путь для сохранения сконвертированного PNG файла.

    Returns:
        bool | None: True, если конвертация прошла успешно, иначе None.
    """
    try:
        # Открываем webp изображение
        with Image.open(webp_path) as img:
            # Конвертируем в PNG и сохраняем
            img.save(png_path, 'PNG')
        return True
    except Exception as ex:
        logger.error(f'Error during conversion: {ex}', exc_info=True)
        return None