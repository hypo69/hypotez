### Анализ кода `hypotez/src/utils/image.py.md`

## Обзор

Модуль предоставляет асинхронные функции для скачивания, сохранения и обработки изображений.

## Подробнее

Этот модуль содержит набор функций для выполнения различных операций с изображениями, включая загрузку из URL, сохранение на диск, изменение размеров, добавление водяных знаков и конвертацию форматов. Он использует библиотеки `aiohttp` для асинхронной загрузки, `aiofiles` для асинхронной работы с файлами и `PIL` (Pillow) для обработки изображений.

## Классы

### `ImageError`

```python
class ImageError(Exception):
    """Custom exception for image-related errors."""
    pass
```

**Описание**:
Пользовательское исключение для ошибок, связанных с изображениями.

**Наследует**:

*   `Exception`

## Функции

### `save_image_from_url_async`

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

**Назначение**:
Асинхронно скачивает изображение из URL и сохраняет его локально.

**Параметры**:

*   `image_url` (str): URL для скачивания изображения.
*   `filename` (Union[str, Path]): Имя файла для сохранения изображения.

**Возвращает**:

*   `Optional[str]`: Путь к сохраненному файлу или `None`, если операция не удалась.

**Вызывает исключения**:

*   `ImageError`: Если не удалось скачать или сохранить изображение.

**Как работает функция**:

1.  Использует `aiohttp.ClientSession` для асинхронного выполнения GET-запроса к указанному URL.
2.  Проверяет статус ответа. В случае ошибки (4xx или 5xx) вызывает исключение `HTTPError`.
3.  Асинхронно считывает данные изображения из ответа.
4.  Вызывает функцию `save_image_async` для сохранения данных изображения в файл.

### `save_image`

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

**Назначение**:
Сохраняет данные изображения в файл в указанном формате.

**Параметры**:

*   `image_data` (bytes): Бинарные данные изображения.
*   `file_name` (Union[str, Path]): Имя файла для сохранения изображения.
*   `format` (str): Формат сохранения изображения, по умолчанию 'PNG'.

**Возвращает**:

*   `Optional[str]`: Путь к сохраненному файлу или `None`, если операция не удалась.

**Вызывает исключения**:

*   `ImageError`: Если не удалось создать или сохранить файл, или если сохраненный файл пуст.

**Как работает функция**:

1.  Преобразует `file_name` в объект `Path`.
2.  Создает родительские директории, если они не существуют.
3.  Использует `BytesIO` для хранения данных изображения в памяти.
4.  Открывает изображение с помощью `Image.open`.
5.  Перематывает буфер `BytesIO` в начало.
6.  Сохраняет изображение в указанный формат.
7.  Проверяет, был ли файл создан и не является ли он пустым.
8.  Логирует ошибки, если операция сохранения не удалась.

### `save_image_async`

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

**Назначение**:
Асинхронно сохраняет данные изображения в файл в указанном формате.

**Параметры**:

*   `image_data` (bytes): Бинарные данные изображения.
*   `file_name` (Union[str, Path]): Имя файла для сохранения изображения.
*   `format` (str): Формат сохранения изображения, по умолчанию 'PNG'.

**Возвращает**:

*   `Optional[str]`: Путь к сохраненному файлу или `None`, если операция не удалась.

**Вызывает исключения**:

*   `ImageError`: Если не удалось создать или сохранить файл, или если сохраненный файл пуст.

**Как работает функция**:

1.  Преобразует `file_name` в объект `Path`.
2.  Асинхронно создает родительские директории, если они не существуют.
3.  Использует `aiofiles` для асинхронной записи данных изображения в файл.
4.  Проверяет, был ли файл создан и не является ли он пустым.
5.  Логирует ошибки, если операция сохранения не удалась.

### `get_image_bytes`

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

**Назначение**:
Читает изображение с помощью Pillow и возвращает его байты в формате JPEG.

**Параметры**:

*   `image_path` (Path): Путь к файлу изображения.
*   `raw` (bool): Если `True`, возвращает объект `BytesIO`; иначе возвращает байты. По умолчанию `True`.

**Возвращает**:

*   `Optional[BytesIO | bytes]`: Байты изображения в формате JPEG или `None`, если произошла ошибка.

**Как работает функция**:

1.  Открывает изображение с помощью `Image.open`.
2.  Создает объект `BytesIO` для хранения данных изображения в памяти.
3.  Сохраняет изображение в формате JPEG в `BytesIO` объект.
4.  Возвращает `BytesIO` объект или его значение в виде байтов, в зависимости от значения параметра `raw`.
5.  Логирует ошибки, если чтение не удалось.

### `get_raw_image_data`

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

**Назначение**:
Получает необработанные бинарные данные файла, если он существует.

**Параметры**:

*   `file_name` (Union[str, Path]): Имя или путь к файлу для чтения.

**Возвращает**:

*   `Optional[bytes]`: Бинарные данные файла или `None`, если файл не существует или произошла ошибка.

**Как работает функция**:

1.  Преобразует `file_name` в объект `Path`.
2.  Проверяет, существует ли файл. Если нет, логирует ошибку и возвращает `None`.
3.  Читает бинарные данные файла с помощью `file_path.read_bytes()`.
4.  Логирует ошибки, если чтение не удалось.

### `random_image`

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

**Назначение**:
Рекурсивно ищет случайное изображение в указанной директории.

**Параметры**:

*   `root_path` (Union[str, Path]): Директория для поиска изображений.

**Возвращает**:

*   `Optional[str]`: Путь к случайному изображению или `None`, если изображения не найдены.

**Как работает функция**:

1.  Преобразует `root_path` в объект `Path`.
2.  Определяет список поддерживаемых расширений изображений (`.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`).
3.  Рекурсивно обходит директорию, собирая список всех файлов с указанными расширениями.
4.  Если изображения не найдены, логирует предупреждение и возвращает `None`.
5.  Выбирает случайное изображение из списка и возвращает его путь.

### `add_text_watermark`

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

**Назначение**:
Добавляет текстовый водяной знак на изображение.

**Параметры**:

*   `image_path` (str | Path): Путь к файлу изображения.
*   `watermark_text` (str): Текст водяного знака.
*   `output_path` (Optional[Union[str, Path]]): Путь для сохранения изображения с водяным знаком. Если не указан, исходное изображение будет перезаписано.

**Возвращает**:

*   `Optional[str]`: Путь к изображению с водяным знаком или `None` в случае ошибки.

**Как работает функция**:

1.  Преобразует параметры `image_path` и `output_path` в объекты `Path`.
2.  Открывает изображение с помощью `Image.open` и преобразует его в формат RGBA.
3.  Создает прозрачный слой для водяного знака.
4.  Определяет размер шрифта на основе размера изображения.
5.  Загружает шрифт (Arial, если доступен, иначе шрифт по умолчанию).
6.  Вычисляет координаты для размещения текста водяного знака по центру изображения.
7.  Рисует текст водяного знака на прозрачном слое.
8.  Объединяет изображение и слой водяного знака с использованием `Image.alpha_composite`.
9.  Сохраняет изображение с водяным знаком по указанному пути.
10. Логирует ошибки с помощью модуля `src.logger.logger`.

### `add_image_watermark`

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

**Назначение**:
Добавляет водяной знак в изображение и сохраняет результат по указанному пути.

**Параметры**:

*   `input_image_path` (Path): Путь к исходному изображению.
*   `watermark_image_path` (Path): Путь к изображению водяного знака.
*   `output_image_path` (Optional[Path]): Путь для сохранения изображения с водяным знаком. Если не указан, изображение будет сохранено в директории "output".

**Возвращает**:

*   `Optional[Path]`: Путь к сохраненному изображению с водяным знаком или `None`, если операция не удалась.

**Как работает функция**:

1.  Открывает исходное изображение и изображение водяного знака с помощью `Image.open`.
2.  Преобразует водяной знак в формат RGBA.
3.  Изменяет размер водяного знака, чтобы его ширина составляла 8% от ширины исходного изображения.
4.  Вычисляет позицию для размещения водяного знака в правом нижнем углу изображения с отступом в 20 пикселей.
5.  Создает прозрачный слой для объединения изображений.
6.  Вставляет исходное изображение на прозрачный слой.
7.  Вставляет водяной знак поверх исходного изображения.
8.  Преобразует прозрачный слой в цветовой режим исходного изображения.
9.  Сохраняет итоговое изображение по указанному пути. Если путь не указан, создает директорию "output" и сохраняет изображение туда.
10. Логирует ошибки с помощью модуля `src.logger.logger`.

### `resize_image`

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

**Назначение**:
Изменяет размер изображения до указанных размеров.

**Параметры**:

*   `image_path` (Union[str, Path]): Путь к файлу изображения.
*   `size` (Tuple[int, int]): Кортеж, содержащий желаемую ширину и высоту изображения.
*   `output_path` (Optional[Union[str, Path]]): Путь для сохранения измененного размера изображения. Если не указан, исходное изображение будет перезаписано.

**Возвращает**:

*   `Optional[str]`: Путь к измененному изображению или `None` в случае ошибки.

**Как работает функция**:

1.  Преобразует параметры `image_path` и `output_path` в объекты `Path`.
2.  Открывает изображение с помощью `Image.open`.
3.  Изменяет размер изображения с помощью `img.resize(size)`.
4.  Сохраняет измененное изображение по указанному пути.
5.  Логирует ошибки с помощью модуля `src.logger.logger`.

### `convert_image`

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

**Назначение**:
Преобразует изображение в указанный формат.

**Параметры**:

*   `image_path` (Union[str, Path]): Путь к файлу изображения.
*   `format` (str): Формат, в который нужно преобразовать изображение (например, "JPEG", "PNG").
*   `output_path` (Optional[Union[str, Path]]): Путь для сохранения преобразованного изображения. Если не указан, исходное изображение будет перезаписано.

**Возвращает**:

*   `Optional[str]`: Путь к преобразованному изображению или `None` в случае ошибки.

**Как работает функция**:

1.  Преобразует параметры `image_path` и `output_path` в объекты `Path`.
2.  Открывает изображение с помощью `Image.open`.
3.  Сохраняет изображение в указанном формате по указанному пути.
4.  Логирует ошибки с помощью модуля `src.logger.logger`.

### `process_images_with_watermark`

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

**Назначение**:
Обрабатывает все изображения в указанной папке, добавляя водяной знак и сохраняя их в директории "output".

**Параметры**:

*   `folder_path` (Path): Путь к папке, содержащей изображения.
*   `watermark_path` (Path): Путь к изображению водяного знака.

**Возвращает**:

*   `None`

**Как работает функция**:

1.  Проверяет, является ли `folder_path` директорией. Если нет, логирует ошибку и завершает работу.
2.  Создает директорию "output", если она не существует.
3.  Итерируется по содержимому `folder_path`.
4.  Для каждого файла с расширением `.png`, `.jpg` или `.jpeg` вызывает функцию `add_image_watermark` для добавления водяного знака и сохранения результата в директорию "output".

## Константы

В данном коде нет констант.

## Примеры использования

```python
from src.utils.image import save_image_from_url_async, add_text_watermark
import asyncio
from pathlib import Path

async def main():
    # Пример асинхронного скачивания и сохранения изображения
    image_url = "https://www.easygifanimator.net/images/samples/video-to-gif-sample.gif"
    filename = "downloaded_image.gif"
    await save_image_from_url_async(image_url, filename)

    # Пример добавления водяного знака
    image_path = filename
    watermark_text = "hypotez"
    output_path = "watermarked_image.png"
    add_text_watermark(image_path, watermark_text, output_path)

asyncio.run(main())
```

## Зависимости

*   `aiohttp`: Для асинхронных HTTP-запросов.
*   `aiofiles`: Для асинхронной работы с файлами.
*   `asyncio`: Для асинхронного программирования.
*   `random`: Для выбора случайного изображения.
*   `pathlib.Path`: Для работы с путями к файлам.
*   `typing.Optional, typing.Union, typing.Tuple`: Для аннотаций типов.
*   `io.BytesIO`: Для работы с данными в памяти как с файлом.
*   `PIL (Pillow)`: Для обработки изображений.
*   `src.logger.logger`: Для логирования событий и ошибок.

## Взаимосвязи с другими частями проекта

Модуль `image.py` предоставляет набор утилит для работы с изображениями, которые могут использоваться в различных частях проекта `hypotez`, например, для загрузки и обработки изображений для веб-интерфейса, для создания превью изображений или для добавления водяных знаков на изображения перед публикацией.