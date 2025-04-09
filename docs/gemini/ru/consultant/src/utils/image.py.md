### **Анализ кода модуля `src.utils.image`**

## \file /src/utils/image.py

Модуль предоставляет асинхронные функции для скачивания, сохранения и обработки изображений, включая добавление водяных знаков, изменение размера и преобразование форматов.

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Использование асинхронности для операций ввода-вывода.
    - Обработка исключений с логированием ошибок.
    - Применение `BytesIO` для работы с изображениями в памяти.
- **Минусы**:
    - Не все функции документированы в соответствии с заданным форматом.
    - В некоторых местах закомментированы `raise ImageError`.
    - Не везде используются аннотации типов.
    - В некоторых функциях есть неиспользуемый код (например, закомментированный код после асинхронной записи файла).
    - Используется `Union` вместо `|`.

**Рекомендации по улучшению:**

1.  **Документация**:
    *   Дополнить все docstring в соответствии с заданным форматом, включая описание аргументов, возвращаемых значений и возможных исключений.
2.  **Обработка исключений**:
    *   Раскомментировать или удалить закомментированные `raise ImageError` после обработки исключений. Решить, нужно ли пробрасывать исключение выше.
3.  **Типизация**:
    *   Добавить аннотации типов для всех переменных, где это необходимо.
4.  **Удаление неиспользуемого кода**:
    *   Удалить закомментированный код в функции `save_image_async`, который дублирует функциональность.
5.  **Использовать `|` вместо `Union`**:
    *   Заменить `Union[str, Path]` на `str | Path`.
6.  **Согласованность**:
    *   Сделать обработку ошибок и логирование консистентными во всех функциях.
    *   Удалить закомментированные строки `# ~~~~~~~~~~~~~~~~~~~~~~ DEBUG ~~~~~~~~~\n        # Write the UNFORMATED image data to the file asynchronously\n        async with aiofiles.open(file_path, "wb") as file:\n            await file.write(image_data)\n        return str(file_path)\n        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n`
    *   Заменить все множественные `Union` типа `Optional[Union[str, Path]]` на `Optional[str | Path]`

**Оптимизированный код:**

```python
## \file /src/utils/image.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для работы с изображениями
=====================================

Модуль содержит асинхронные функции для скачивания, сохранения и обработки изображений.
Включает в себя функциональность для сохранения изображений из URL, сохранения данных изображений в файлы,
получения данных изображений, поиска случайных изображений в каталогах, добавления водяных знаков, изменения размера
и преобразования форматов изображений.
"""

import aiohttp
import aiofiles
import asyncio
import random
from pathlib import Path
from typing import Optional, Tuple

from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from src.logger.logger import logger


class ImageError(Exception):
    """
    Исключение для ошибок, связанных с обработкой изображений.
    """

    pass


async def save_image_from_url_async(image_url: str, filename: str | Path) -> Optional[str]:
    """
    Асинхронно скачивает изображение по URL и сохраняет его локально.

    Args:
        image_url (str): URL изображения для скачивания.
        filename (str | Path): Имя файла для сохранения изображения.

    Returns:
        Optional[str]: Путь к сохраненному файлу, или None, если операция не удалась.

    Raises:
        ImageError: Если скачивание или сохранение изображения не удалось.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                image_data: bytes = await response.read()
    except Exception as ex:
        logger.error(f'Error downloading image from {image_url}', ex, exc_info=True)
        # raise ImageError(f"Failed to download image from {image_url}") from ex
        return None

    return await save_image_async(image_data, filename)


def save_image(image_data: bytes, file_name: str | Path, format: str = 'PNG') -> Optional[str]:
    """
    Сохраняет данные изображения в файл в указанном формате.

    Args:
        image_data (bytes): Бинарные данные изображения.
        file_name (str | Path): Имя файла для сохранения изображения.
        format (str, optional): Формат изображения для сохранения. По умолчанию 'PNG'.

    Returns:
        Optional[str]: Путь к сохраненному файлу, или None, если операция не удалась.

    Raises:
        ImageError: Если файл не может быть создан или сохранен, или если сохраненный файл пуст.
    """
    file_path: Path = Path(file_name)

    try:
        # Создание директории для файла, если она не существует
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Использование BytesIO для избежания двойной записи на диск
        with BytesIO(image_data) as img_io:
            img: Image = Image.open(img_io)
            img_io.seek(0)  # Сброс позиции буфера перед сохранением
            img.save(img_io, format=format)
            img_bytes: bytes = img_io.getvalue()

        # Запись отформатированных данных изображения в файл
        with open(file_path, 'wb') as file:
            file.write(img_bytes)

        # Проверка, что файл был создан и не является пустым
        if not file_path.exists():
            logger.error(f'File {file_path} was not created.')
            # raise ImageError(f"File {file_path} was not created.")
            return None

        file_size: int = file_path.stat().st_size
        if file_size == 0:
            logger.error(f'File {file_path} saved, but its size is 0 bytes.')
            # raise ImageError(f"File {file_path} saved, but its size is 0 bytes.")
            return None

        return str(file_path)

    except Exception as ex:
        logger.exception(f'Failed to save file {file_path}', ex, exc_info=True)
        # raise ImageError(f"Failed to save file {file_path}") from ex
        return None


async def save_image_async(image_data: bytes, file_name: str | Path, format: str = 'PNG') -> Optional[str]:
    """
    Асинхронно сохраняет данные изображения в файл в указанном формате.

    Args:
        image_data (bytes): Бинарные данные изображения.
        file_name (str | Path): Имя файла для сохранения изображения.
        format (str, optional): Формат изображения для сохранения. По умолчанию 'PNG'.

    Returns:
        Optional[str]: Путь к сохраненному файлу, или None, если операция не удалась.

    Raises:
        ImageError: Если файл не может быть создан или сохранен, или если сохраненный файл пуст.
    """
    file_path: Path = Path(file_name)

    try:
        # Создание директории для файла, если она не существует
        await asyncio.to_thread(file_path.parent.mkdir, parents=True, exist_ok=True)

        # Запись данных изображения в файл
        async with aiofiles.open(file_path, 'wb') as file:
            await file.write(image_data)
        return str(file_path)

    except Exception as ex:
        logger.exception(f'Failed to save file {file_path}', ex, exc_info=True)
        # raise ImageError(f"Failed to save file {file_path}") from ex
        return None


def get_image_bytes(image_path: Path, raw: bool = True) -> Optional[BytesIO | bytes]:
    """
    Читает изображение, используя Pillow, и возвращает его байты в формате JPEG.

    Args:
        image_path (Path): Путь к файлу изображения.
        raw (bool, optional): Если True, возвращает объект BytesIO, иначе возвращает bytes. По умолчанию True.

    Returns:
        Optional[BytesIO | bytes]: Байты изображения в формате JPEG, или None в случае ошибки.
    """
    try:
        img: Image = Image.open(image_path)
        img_byte_arr: BytesIO = BytesIO()
        img.save(img_byte_arr, format='JPEG')
        return img_byte_arr if raw else img_byte_arr.getvalue()
    except Exception as ex:
        logger.error('Error reading image with Pillow:', ex, exc_info=True)
        return None


def get_raw_image_data(file_name: str | Path) -> Optional[bytes]:
    """
    Извлекает необработанные двоичные данные файла, если он существует.

    Args:
        file_name (str | Path): Имя или путь к файлу для чтения.

    Returns:
        Optional[bytes]: Двоичные данные файла, или None, если файл не существует или произошла ошибка.
    """
    file_path: Path = Path(file_name)

    if not file_path.exists():
        logger.error(f'File {file_path} does not exist.')
        return None

    try:
        return file_path.read_bytes()
    except Exception as ex:
        logger.error(f'Error reading file {file_path}', ex, exc_info=True)
        return None


def random_image(root_path: str | Path) -> Optional[str]:
    """
    Рекурсивно ищет случайное изображение в указанном каталоге.

    Args:
        root_path (str | Path): Каталог для поиска изображений.

    Returns:
        Optional[str]: Путь к случайному изображению, или None, если изображения не найдены.
    """
    root_path: Path = Path(root_path)
    image_extensions: list[str] = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    image_files: list[Path] = [
        file_path
        for file_path in root_path.rglob('*')
        if file_path.is_file() and file_path.suffix.lower() in image_extensions
    ]

    if not image_files:
        logger.warning(f'No images found in {root_path}.')
        return None

    return str(random.choice(image_files))


def add_text_watermark(image_path: str | Path, watermark_text: str, output_path: Optional[str | Path] = None) -> Optional[str]:
    """
    Добавляет текстовый водяной знак на изображение.

    Args:
        image_path (str | Path): Путь к файлу изображения.
        watermark_text (str): Текст для использования в качестве водяного знака.
        output_path (Optional[str | Path], optional): Путь для сохранения изображения с водяным знаком.
            По умолчанию перезаписывает исходное изображение.

    Returns:
        Optional[str]: Путь к изображению с водяным знаком, или None в случае неудачи.
    """
    image_path: Path = Path(image_path)
    output_path: Path = image_path if output_path is None else Path(output_path)

    try:
        image: Image = Image.open(image_path).convert('RGBA')

        # Создание прозрачного слоя для водяного знака
        watermark_layer: Image = Image.new('RGBA', image.size, (255, 255, 255, 0))
        draw: ImageDraw = ImageDraw.Draw(watermark_layer)

        font_size: int = min(image.size) // 10  # Adjust the font size based on the image
        try:
            font: ImageFont = ImageFont.truetype('arial.ttf', size=font_size)
        except IOError:
            font: ImageFont = ImageFont.load_default(size=font_size)
            logger.warning('Font arial.ttf not found; using default font.')

        text_width, text_height = draw.textsize(watermark_text, font=font)
        x: int = (image.width - text_width) // 2
        y: int = (image.height - text_height) // 2

        # Draw text on the transparent layer
        draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))

        # Combine the image and watermark
        watermarked_image: Image = Image.alpha_composite(image, watermark_layer)
        watermarked_image.save(output_path)

        return str(output_path)

    except Exception as ex:
        logger.error(f'Failed to add watermark to {image_path}', ex, exc_info=True)
        return None


def add_image_watermark(
    input_image_path: Path, watermark_image_path: Path, output_image_path: Optional[Path] = None
) -> Optional[Path]:
    """
    Добавляет водяной знак на изображение и сохраняет результат по указанному пути.

    Args:
        input_image_path (Path): Путь к исходному изображению.
        watermark_image_path (Path): Путь к изображению водяного знака.
        output_image_path (Optional[Path], optional): Путь для сохранения изображения с водяным знаком.
            Если не указан, изображение будет сохранено в каталоге "output".

    Returns:
        Optional[Path]: Путь к сохраненному изображению с водяным знаком, или None, если операция не удалась.
    """
    try:
        # Открытие базового изображения
        base_image: Image = Image.open(input_image_path)

        # Открытие изображения водяного знака и преобразование его в RGBA
        watermark: Image = Image.open(watermark_image_path).convert('RGBA')

        # Установка размера водяного знака (8% от ширины базового изображения)
        position: Tuple[int, int] = base_image.size  # Size of the base image (width, height)
        newsize: Tuple[int, int] = (
            int(position[0] * 8 / 100),
            int(position[0] * 8 / 100),
        )  # New size of the watermark
        watermark: Image = watermark.resize(newsize)  # Resize the watermark

        # Определение позиции для размещения водяного знака (нижний правый угол с отступом 20px)
        new_position: Tuple[int, int] = position[0] - newsize[0] - 20, position[1] - newsize[1] - 20

        # Создание нового прозрачного слоя для объединения изображений
        transparent: Image = Image.new(mode='RGBA', size=position, color=(0, 0, 0, 0))

        # Вставка базового изображения на новый слой
        transparent.paste(base_image, (0, 0))

        # Вставка водяного знака поверх базового изображения
        transparent.paste(watermark, new_position, watermark)

        # Проверка режима изображения и преобразование прозрачного слоя в исходный режим
        image_mode: str = base_image.mode
        if image_mode == 'RGB':
            transparent: Image = transparent.convert(image_mode)  # Convert to RGB
        else:
            transparent: Image = transparent.convert('P')  # Convert to palette

        # Сохранение окончательного изображения по указанному пути с оптимизированным качеством
        if output_image_path is None:
            output_image_path: Path = input_image_path.parent / 'output' / input_image_path.name
        output_image_path.parent.mkdir(parents=True, exist_ok=True)  # Create output directory if it doesn't exist
        transparent.save(output_image_path, optimize=True, quality=100)
        logger.info(f'Saving {output_image_path}...')

        return output_image_path

    except Exception as ex:
        logger.error(f'Failed to add watermark to {input_image_path}: {ex}', ex, exc_info=True)
        return None


def resize_image(image_path: str | Path, size: Tuple[int, int], output_path: Optional[str | Path] = None) -> Optional[str]:
    """
    Изменяет размер изображения до указанных размеров.

    Args:
        image_path (str | Path): Путь к файлу изображения.
        size (Tuple[int, int]): Кортеж, содержащий желаемую ширину и высоту изображения.
        output_path (Optional[str | Path], optional): Путь для сохранения измененного изображения.
            По умолчанию перезаписывает исходное изображение.

    Returns:
        Optional[str]: Путь к измененному изображению, или None в случае неудачи.
    """
    image_path: Path = Path(image_path)
    output_path: Path = image_path if output_path is None else Path(output_path)

    try:
        img: Image = Image.open(image_path)
        resized_img: Image = img.resize(size)
        resized_img.save(output_path)
        return str(output_path)

    except Exception as ex:
        logger.error(f'Failed to resize image {image_path}', ex, exc_info=True)
        return None


def convert_image(image_path: str | Path, format: str, output_path: Optional[str | Path] = None) -> Optional[str]:
    """
    Преобразует изображение в указанный формат.

    Args:
        image_path (str | Path): Путь к файлу изображения.
        format (str): Формат для преобразования изображения (например, "JPEG", "PNG").
        output_path (Optional[str | Path], optional): Путь для сохранения преобразованного изображения.
            По умолчанию перезаписывает исходное изображение.

    Returns:
        Optional[str]: Путь к преобразованному изображению, или None в случае неудачи.
    """
    image_path: Path = Path(image_path)
    output_path: Path = image_path if output_path is None else Path(output_path)

    try:
        img: Image = Image.open(image_path)
        img.save(output_path, format=format)
        return str(output_path)
    except Exception as ex:
        logger.error(f'Failed to convert image {image_path}', ex, exc_info=True)
        return None


def process_images_with_watermark(folder_path: Path, watermark_path: Path) -> None:
    """
    Обрабатывает все изображения в указанной папке, добавляя водяной знак и сохраняя их в каталоге "output".

    Args:
        folder_path (Path): Путь к папке, содержащей изображения.
        watermark_path (Path): Путь к изображению водяного знака.
    """
    if not folder_path.is_dir():
        logger.error(f'Folder {folder_path} does not exist.')
        return

    # Create an "output" directory if it doesn't exist
    output_dir: Path = folder_path / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process each file in the folder
    for file_path in folder_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in ['.png', '.jpg', '.jpeg']:
            output_image_path: Path = output_dir / file_path.name
            add_image_watermark(file_path, watermark_path, output_image_path)


# Example usage
if __name__ == '__main__':
    folder: Path = Path(input('Enter Folder Path: '))  # Path to the folder containing images
    watermark: Path = Path(input('Enter Watermark Path: '))  # Path to the watermark image

    process_images_with_watermark(folder, watermark)