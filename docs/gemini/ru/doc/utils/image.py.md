# Модуль для обработки изображений (image.py)

## Обзор

Этот модуль предоставляет набор функций для обработки изображений, включая скачивание, сохранение, изменение размера, добавление водяных знаков и преобразование форматов изображений.

## Подробней

Модуль `src.utils.image` предназначен для упрощения задач, связанных с обработкой изображений в проекте. Он предоставляет удобный интерфейс для выполнения различных операций, таких как скачивание изображений из интернета, сохранение их на диск, изменение размеров, добавление водяных знаков и преобразование форматов. Модуль использует библиотеки `aiohttp`, `aiofiles`, `PIL (Pillow)` и модуль логирования `src.logger.logger`.

## Классы

### `ImageError`

**Описание**: Пользовательское исключение для ошибок, связанных с обработкой изображений.

```python
class ImageError(Exception):
    """Custom exception for image-related errors."""
    pass
```

**Наследует**:

-   `Exception` (базовый класс для всех исключений в Python).

## Функции

### `save_image_from_url_async`

**Назначение**: Асинхронно скачивает изображение по URL и сохраняет его локально.

```python
async def save_image_from_url_async(image_url: str, filename: Union[str, Path]) -> Optional[str]:
    """
    Downloads an image from a URL and saves it locally asynchronously.

    Args:
        image_url (str): The URL to download the image from.
        filename (Union[str, Path]): The name of the file to save the image to.

    Returns:
        Optional[str]: The path to the saved file, or None if the operation failed.

    Raises:
        ImageError: If the image download or save operation fails.
    """
    ...
```

**Параметры**:

-   `image_url` (str): URL изображения для скачивания.
-   `filename` (Union[str, Path]): Имя файла для сохранения изображения.

**Возвращает**:

-   `Optional[str]`: Путь к сохраненному файлу или `None`, если операция не удалась.

**Как работает функция**:

1.  Асинхронно скачивает изображение по указанному URL, используя `aiohttp`.
2.  Проверяет статус ответа HTTP (должен быть 200 OK).
3.  Сохраняет скачанные данные в файл, используя функцию `save_image_async`.
4.  В случае ошибки логирует ее и возвращает `None`.

### `save_image`

**Назначение**: Сохраняет данные изображения в файл в указанном формате.

```python
def save_image(image_data: bytes, file_name: str | Path, format: str = 'PNG') -> Optional[str]:
    """
    Saves image data to a file in the specified format.

    Args:
        image_data (bytes): The binary image data.
        file_name (Union[str, Path]): The name of the file to save the image to.
        format (str): The format to save the image in, default is PNG.

    Returns:
        Optional[str]: The path to the saved file, or None if the operation failed.

    Raises:
        ImageError: If the file cannot be created, saved, or if the saved file is empty.
    """
    ...
```

**Параметры**:

-   `image_data` (bytes): Бинарные данные изображения.
-   `file_name` (Union[str, Path]): Имя файла для сохранения изображения.
-   `format` (str): Формат изображения (например, "PNG", "JPEG"). По умолчанию "PNG".

**Возвращает**:

-   `Optional[str]`: Путь к сохраненному файлу или `None`, если операция не удалась.

**Как работает функция**:

1.  Создает директорию для сохранения файла, если она не существует.
2.  Использует `BytesIO` для создания буфера в памяти, в который записывает данные изображения.
3.  Открывает изображение с использованием `PIL.Image.open`.
4.  Сохраняет изображение в указанном формате в буфер.
5.  Записывает данные из буфера в файл.
6.  Проверяет, был ли создан файл и не является ли он пустым.
7.  Логирует информацию об ошибках, используя `logger.exception`.

### `save_image_async`

**Назначение**: Асинхронно сохраняет данные изображения в файл в указанном формате.

```python
async def save_image_async(image_data: bytes, file_name: str | Path, format: str = 'PNG') -> Optional[str]:
    """
    Saves image data to a file in the specified format asynchronously.

    Args:
        image_data (bytes): The binary image data.
        file_name (Union[str, Path]): The name of the file to save the image to.
        format (str): The format to save the image in, default is PNG.

    Returns:
        Optional[str]: The path to the saved file, or None if the operation failed.

    Raises:
        ImageError: If the file cannot be created, saved, or if the saved file is empty.
    """
    ...
```

**Параметры**:

-   `image_data` (bytes): Бинарные данные изображения.
-   `file_name` (Union[str, Path]): Имя файла для сохранения изображения.
-   `format` (str): Формат изображения (например, "PNG", "JPEG"). По умолчанию "PNG".

**Возвращает**:

-   `Optional[str]`: Путь к сохраненному файлу или `None`, если операция не удалась.

**Как работает функция**:

1.  Создает директорию для сохранения файла асинхронно.
2.  Использует `BytesIO` для создания буфера в памяти, в который записывает данные изображения.
3.  Открывает изображение с использованием `PIL.Image.open`.
4.  Сохраняет изображение в указанном формате в буфер.
5.  Записывает данные из буфера в файл асинхронно, используя `aiofiles`.
6.  Проверяет, был ли создан файл и не является ли он пустым асинхронно.
7.  Логирует информацию об ошибках, используя `logger.exception`.

### `get_image_bytes`

**Назначение**: Читает изображение, используя Pillow, и возвращает его байты в формате JPEG.

```python
def get_image_bytes(image_path: Path, raw: bool = True) -> Optional[BytesIO | bytes]:
    """
    Reads an image using Pillow and returns its bytes in JPEG format.

    Args:
        image_path (Path): The path to the image file.
        raw (bool): If True, returns a BytesIO object; otherwise, returns bytes. Defaults to True.

    Returns:
        Optional[Union[BytesIO, bytes]]: The bytes of the image in JPEG format, or None if an error occurs.
    """
    ...
```

**Параметры**:

-   `image_path` (Path): Путь к файлу изображения.
-   `raw` (bool): Если `True`, возвращает объект `BytesIO`; иначе возвращает `bytes`. По умолчанию `True`.

**Возвращает**:

-   `Optional[BytesIO | bytes]`: Байты изображения в формате JPEG или `None`, если произошла ошибка.

**Как работает функция**:

1.  Открывает изображение, используя `PIL.Image.open`.
2.  Создает объект `BytesIO` для хранения байтов изображения.
3.  Сохраняет изображение в формате JPEG в буфер.
4.  Возвращает буфер или его содержимое (в зависимости от значения параметра `raw`).
5.  Логирует информацию об ошибках, используя `logger.error`.

### `get_raw_image_data`

**Назначение**: Извлекает необработанные бинарные данные файла, если он существует.

```python
def get_raw_image_data(file_name: Union[str, Path]) -> Optional[bytes]:
    """
    Retrieves the raw binary data of a file if it exists.

    Args:
        file_name (Union[str, Path]): The name or path of the file to read.

    Returns:
        Optional[bytes]: The binary data of the file, or None if the file does not exist or an error occurs.
    """
    ...
```

**Параметры**:

-   `file_name` (Union[str, Path]): Имя или путь к файлу для чтения.

**Возвращает**:

-   `Optional[bytes]`: Бинарные данные файла или `None`, если файл не существует или произошла ошибка.

**Как работает функция**:

1.  Преобразует `file_name` в объект `Path`.
2.  Проверяет, существует ли файл. Если нет, логирует ошибку и возвращает `None`.
3.  Читает бинарные данные файла, используя `file_path.read_bytes()`.
4.  Логирует информацию об ошибках, используя `logger.error`.

### `random_image`

**Назначение**: Рекурсивно ищет случайное изображение в указанной директории.

```python
def random_image(root_path: Union[str, Path]) -> Optional[str]:
    """
    Recursively searches for a random image in the specified directory.

    Args:
        root_path (Union[str, Path]): The directory to search for images.

    Returns:
        Optional[str]: The path to a random image, or None if no images are found.
    """
    ...
```

**Параметры**:

-   `root_path` (Union[str, Path]): Директория для поиска изображений.

**Возвращает**:

-   `Optional[str]`: Путь к случайному изображению или `None`, если изображения не найдены.

**Как работает функция**:

1.  Определяет список поддерживаемых расширений изображений (`.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`).
2.  Рекурсивно обходит указанную директорию, используя `Path.rglob("*")`.
3.  Фильтрует список файлов, оставляя только файлы с поддерживаемыми расширениями.
4.  Если найдены изображения, выбирает случайное изображение из списка и возвращает его путь.
5.  Логирует информацию об ошибках, используя `logger.warning`.

### `add_text_watermark`

**Назначение**: Добавляет текстовый водяной знак на изображение.

```python
def add_text_watermark(image_path: str | Path, watermark_text: str, output_path: Optional[str | Path] = None) -> Optional[str]:
    """
    Adds a text watermark to an image.

    Args:
        image_path (Union[str, Path]): Path to the image file.
        watermark_text (str): Text to use as the watermark.
        output_path (Optional[Union[str, Path]]): Path to save the watermarked image.
            Defaults to overwriting the original image.

    Returns:
        Optional[str]: Path to the watermarked image, or None on failure.
    """
    ...
```

**Параметры**:

-   `image_path` (Union[str, Path]): Путь к файлу изображения.
-   `watermark_text` (str): Текст водяного знака.
-   `output_path` (Optional[Union[str, Path]]): Путь для сохранения изображения с водяным знаком. Если не указан, исходное изображение будет перезаписано.

**Возвращает**:

-   `Optional[str]`: Путь к изображению с водяным знаком или `None` в случае ошибки.

**Как работает функция**:

1.  Открывает изображение, используя `PIL.Image.open`.
2.  Создает прозрачный слой для водяного знака.
3.  Определяет размер шрифта на основе размера изображения.
4.  Определяет координаты для размещения текста водяного знака по центру изображения.
5.  Рисует текст водяного знака на прозрачном слое.
6.  Объединяет исходное изображение и слой с водяным знаком.
7.  Сохраняет изображение с водяным знаком по указанному пути.
8.  Логирует информацию об ошибках, используя `logger.error`.

### `add_image_watermark`

**Назначение**: Добавляет водяной знак (изображение) к изображению и сохраняет результат.

```python
def add_image_watermark(input_image_path: Path, watermark_image_path: Path, output_image_path: Optional[Path] = None) -> Optional[Path]:
    """
    Adds a watermark to an image and saves the result to the specified output path.

    Args:
        input_image_path (Path): Path to the input image.
        watermark_image_path (Path): Path to the watermark image.
        output_image_path (Optional[Path]): Path to save the watermarked image.
            If not provided, the image will be saved in an "output" directory.

    Returns:
        Optional[Path]: Path to the saved watermarked image, or None if the operation failed.
    """
    ...
```

**Параметры**:

-   `input_image_path` (Path): Путь к исходному изображению.
-   `watermark_image_path` (Path): Путь к изображению водяного знака.
-   `output_image_path` (Optional[Path]): Путь для сохранения изображения с водяным знаком. Если не указан, изображение будет сохранено в директории "output".

**Возвращает**:

-   `Optional[Path]`: Путь к изображению с водяным знаком или `None` в случае ошибки.

**Как работает функция**:

1.  Открывает исходное изображение и изображение водяного знака, используя `PIL.Image.open`.
2.  Изменяет размер водяного знака, чтобы он занимал 8% ширины исходного изображения.
3.  Определяет позицию для размещения водяного знака в правом нижнем углу с отступом в 20 пикселей.
4.  Создает новый прозрачный слой для объединения изображений.
5.  Вставляет исходное изображение и водяной знак на прозрачный слой.
6.  Преобразует прозрачный слой в цветовой режим исходного изображения.
7.  Сохраняет изображение с водяным знаком по указанному пути.
8.  Логирует информацию об ошибках, используя `logger.error`.

### `resize_image`

**Назначение**: Изменяет размер изображения до указанных размеров.

```python
def resize_image(image_path: Union[str, Path], size: Tuple[int, int], output_path: Optional[Union[str, Path]] = None) -> Optional[str]:
    """
    Resizes an image to the specified dimensions.

    Args:
        image_path (Union[str, Path]): Path to the image file.
        size (Tuple[int, int]): A tuple containing the desired width and height of the image.
        output_path (Optional[Union[str, Path]]): Path to save the resized image.
            Defaults to overwriting the original image.

    Returns:
        Optional[str]: Path to the resized image, or None on failure.
    """
    ...
```

**Параметры**:

-   `image_path` (Union[str, Path]): Путь к файлу изображения.
-   `size` (Tuple[int, int]): Кортеж, содержащий желаемую ширину и высоту изображения.
-   `output_path` (Optional[Union[str, Path]]): Путь для сохранения изображения измененного размера. Если не указан, исходное изображение будет перезаписано.

**Возвращает**:

-   `Optional[str]`: Путь к изображению измененного размера или `None` в случае ошибки.

**Как работает функция**:

1.  Открывает изображение, используя `PIL.Image.open`.
2.  Изменяет размер изображения до указанных размеров, используя `img.resize(size)`.
3.  Сохраняет изображение измененного размера по указанному пути.
4.  Логирует информацию об ошибках, используя `logger.error`.

### `convert_image`

**Назначение**: Преобразует изображение в указанный формат.

```python
def convert_image(image_path: Union[str, Path], format: str, output_path: Optional[Union[str, Path]] = None) -> Optional[str]:
    """
    Converts an image to the specified format.

    Args:
        image_path (Union[str, Path]): Path to the image file.
        format (str): Format to convert image to (e.g., "JPEG", "PNG").
        output_path (Optional[Union[str, Path]]): Path to save the converted image.
            Defaults to overwriting the original image.

    Returns:
        Optional[str]: Path to the converted image or None on failure.
    """
    ...
```

**Параметры**:

-   `image_path` (Union[str, Path]): Путь к файлу изображения.
-   `format` (str): Формат для преобразования изображения (например, "JPEG", "PNG").
-   `output_path` (Optional[Union[str, Path]]): Путь для сохранения преобразованного изображения. Если не указан, исходное изображение будет перезаписано.

**Возвращает**:

-   `Optional[str]`: Путь к преобразованному изображению или `None` в случае ошибки.

**Как работает функция**:

1.  Открывает изображение, используя `PIL.Image.open`.
2.  Преобразует изображение в указанный формат, используя `img.save(output_path, format=format)`.
3.  Сохраняет преобразованное изображение по указанному пути.
4.  Логирует информацию об ошибках, используя `logger.error`.

### `process_images_with_watermark`

**Назначение**: Обрабатывает все изображения в указанной папке, добавляя водяной знак и сохраняя их в директории "output".

```python
def process_images_with_watermark(folder_path: Path, watermark_path: Path) -> None:
    """
    Processes all images in the specified folder by adding a watermark and saving them in an "output" directory.

    Args:
        folder_path (Path): Path to the folder containing images.
        watermark_path (Path): Path to the watermark image.
    """
    ...
```

**Параметры**:

-   `folder_path` (Path): Путь к папке, содержащей изображения.
-   `watermark_path` (Path): Путь к изображению водяного знака.

**Как работает функция**:

1.  Проверяет, существует ли указанная папка. Если нет, логирует ошибку и завершает выполнение.
2.  Создает директорию "output" (если она не существует) в указанной папке.
3.  Перебирает все файлы в указанной папке.
4.  Для каждого файла, являющегося изображением (с расширением `.png`, `.jpg`, `.jpeg`), добавляет водяной знак, используя функцию `add_image_watermark`, и сохраняет результат в директории "output".
5.  Логирует информацию об ошибках, используя `logger.error`.

## Переменные модуля

-   В данном модуле отсутствуют глобальные переменные, за исключением констант, определенных внутри функций.

## Пример использования

```python
from src.utils.image import save_image_from_url_async, add_image_watermark, process_images_with_watermark
from pathlib import Path

# Пример асинхронного скачивания и сохранения изображения
async def main():
    image_url = "https://www.easygifanimator.net/images/samples/video-to-gif-sample.gif"
    filename = "downloaded_image.gif"
    await save_image_from_url_async(image_url, filename)

# Пример добавления водяного знака
watermark_path = Path("watermark.png")  # Укажите путь к вашему изображению водяного знака
add_image_watermark(Path("downloaded_image.gif"), watermark_path, Path("watermarked_image.png"))

# Пример обработки всех изображений в папке
folder_path = Path("images") # Укажите путь к папке с изображениями
process_images_with_watermark(folder_path, watermark_path)
```

## Взаимосвязь с другими частями проекта

-   Модуль `src.utils.image` используется другими модулями проекта для выполнения различных операций с изображениями.
-   Для логирования используется модуль `src.logger.logger`.
-   Для работы с файловой системой используется модуль `pathlib`.
-   Для асинхронных операций используются модули `aiohttp` и `aiofiles`.
-   Для обработки изображений используется библиотека `PIL (Pillow)`.