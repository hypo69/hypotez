### Анализ кода модуля `hypotez/src/utils/image.py`

## Обзор

Этот модуль предоставляет набор асинхронных функций для скачивания, сохранения и обработки изображений. Включает функциональность для сохранения изображений по URL-адресам, сохранения данных изображений в файлы, извлечения данных изображений, поиска случайных изображений в директориях, добавления водяных знаков, изменения размера и преобразования форматов изображений.

## Подробнее

Модуль предназначен для выполнения различных операций с изображениями, таких как скачивание, сохранение, изменение размера, добавление водяных знаков и преобразование форматов. Он предоставляет как синхронные, так и асинхронные функции для выполнения этих задач.

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
- `Exception`

**Атрибуты**:
- Нет

**Методы**:
- Нет

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
Асинхронно скачивает изображение по URL и сохраняет его локально.

**Параметры**:
- `image_url` (str): URL-адрес изображения для скачивания.
- `filename` (Union[str, Path]): Имя файла для сохранения изображения.

**Возвращает**:
- `Optional[str]`: Путь к сохраненному файлу или `None`, если операция не удалась.

**Вызывает исключения**:
- `ImageError`: Если скачивание или сохранение изображения не удалось.

**Как работает функция**:
1. Отправляет асинхронный GET-запрос к `image_url` с использованием `aiohttp.ClientSession`.
2. Если ответ успешен, читает данные изображения из ответа.
3. Вызывает `save_image_async` для сохранения данных изображения в файл.

**Примеры**:

```python
import asyncio
from pathlib import Path
from src.utils.image import save_image_from_url_async

async def main():
    image_url = "https://www.easygifanimator.net/images/samples/video-to-gif-sample.gif"
    filename = "downloaded_image.gif"
    result = await save_image_from_url_async(image_url, filename)
    if result:
        print(f"Image saved to {result}")
    else:
        print("Failed to download and save image")

asyncio.run(main())
```

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
- `image_data` (bytes): Двоичные данные изображения.
- `file_name` (Union[str, Path]): Имя файла для сохранения изображения.
- `format` (str, optional): Формат сохранения изображения, по умолчанию 'PNG'.

**Возвращает**:
- `Optional[str]`: Путь к сохраненному файлу или `None`, если операция не удалась.

**Вызывает исключения**:
- `ImageError`: Если файл не может быть создан, сохранен, или если сохраненный файл пуст.

**Как работает функция**:
1.  Создает объект `Path` из `file_name`.
2.  Создает родительские директории для файла, если они не существуют.
3.  Использует `BytesIO` для создания буфера в памяти.
4.  Открывает изображение из `image_data` с помощью `Image.open`.
5.  Сохраняет изображение в буфер `BytesIO` в указанном формате.
6.  Записывает данные из буфера в файл.
7.  Проверяет, был ли создан файл и не является ли он пустым.

**Примеры**:

```python
from pathlib import Path
from PIL import Image
from io import BytesIO
from src.utils.image import save_image

# Создаем тестовые данные изображения
img = Image.new('RGB', (60, 30), color='red')
img_byte_arr = BytesIO()
img.save(img_byte_arr, format='PNG')
img_byte_arr = img_byte_arr.getvalue()

file_name = "test_image.png"
result = save_image(img_byte_arr, file_name)
if result:
    print(f"Image saved to {result}")
```

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
- `image_data` (bytes): Двоичные данные изображения.
- `file_name` (Union[str, Path]): Имя файла для сохранения изображения.
- `format` (str, optional): Формат сохранения изображения, по умолчанию 'PNG'.

**Возвращает**:
- `Optional[str]`: Путь к сохраненному файлу или `None`, если операция не удалась.

**Вызывает исключения**:
- `ImageError`: Если файл не может быть создан, сохранен, или если сохраненный файл пуст.

**Как работает функция**:
1.  Создает объект `Path` из `file_name`.
2.  Асинхронно создает родительские директории для файла, если они не существуют.
3.  Асинхронно записывает данные изображения в файл, используя `aiofiles`.
4.  (Закомментированная часть) преобразует изображение с помощью Pillow

**Примеры**:

```python
import asyncio
from pathlib import Path
from PIL import Image
from io import BytesIO
from src.utils.image import save_image_async

async def main():
    # Создаем тестовые данные изображения
    img = Image.new('RGB', (60, 30), color='blue')
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    file_name = "test_image_async.png"
    result = await save_image_async(img_byte_arr, file_name)
    if result:
        print(f"Image saved asynchronously to {result}")

asyncio.run(main())
```

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
Читает изображение, используя Pillow, и возвращает его байты в формате JPEG.

**Параметры**:
- `image_path` (Path): Путь к файлу изображения.
- `raw` (bool, optional): Если True, возвращает объект BytesIO, иначе возвращает bytes. По умолчанию True.

**Возвращает**:
- `Optional[BytesIO | bytes]`: Байты изображения в формате JPEG, или None, если произошла ошибка.

**Как работает функция**:
1.  Открывает изображение с помощью `Image.open`.
2.  Создает объект `BytesIO`.
3.  Сохраняет изображение в `BytesIO` в формате JPEG.
4.  Если `raw` равно True, возвращает объект `BytesIO`, иначе возвращает байты из `BytesIO`.

**Примеры**:

```python
from pathlib import Path
from src.utils.image import get_image_bytes

image_path = Path("test_image.png")  # Замените на путь к существующему изображению
image_bytes = get_image_bytes(image_path)
if image_bytes:
    print(f"Image read successfully. Size: {len(image_bytes.getvalue())} bytes")
```

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
Извлекает необработанные двоичные данные файла, если он существует.

**Параметры**:
- `file_name` (Union[str, Path]): Имя или путь к файлу для чтения.

**Возвращает**:
- `Optional[bytes]`: Двоичные данные файла или None, если файл не существует или произошла ошибка.

**Как работает функция**:
1. Создает объект `Path` из `file_name`.
2. Проверяет существование файла. Если файл не существует, логирует ошибку и возвращает `None`.
3. В противном случае, читает содержимое файла как двоичные данные и возвращает их.

**Примеры**:

```python
from pathlib import Path
from src.utils.image import get_raw_image_data

file_name = "test_image.png"  # Замените на путь к существующему файлу
raw_data = get_raw_image_data(file_name)
if raw_data:
    print(f"File read successfully. Size: {len(raw_data)} bytes")
```

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
- `root_path` (Union[str, Path]): Директория для поиска изображений.

**Возвращает**:
- `Optional[str]`: Путь к случайному изображению или None, если изображения не найдены.

**Как работает функция**:
1. Создает объект `Path` из `root_path`.
2. Определяет список поддерживаемых расширений изображений.
3. Рекурсивно обходит директорию, ища файлы с указанными расширениями.
4. Если найдены изображения, возвращает путь к случайному изображению.
5. Если изображения не найдены, логирует предупреждение и возвращает None.

**Примеры**:

```python
from pathlib import Path
from src.utils.image import random_image

root_path = Path(".")
random_image_path = random_image(root_path)
if random_image_path:
    print(f"Random image found: {random_image_path}")
```

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
Добавляет текстовый водяной знак к изображению.

**Параметры**:
- `image_path` (Union[str, Path]): Путь к файлу изображения.
- `watermark_text` (str): Текст для использования в качестве водяного знака.
- `output_path` (Optional[Union[str, Path]], optional): Путь для сохранения изображения с водяным знаком. Если не указан, исходное изображение будет перезаписано.

**Возвращает**:
- `Optional[str]`: Путь к изображению с водяным знаком или None в случае ошибки.

**Как работает функция**:
1. Создает объекты `Path` из `image_path` и `output_path`.
2. Открывает изображение с помощью `Image.open`.
3. Создает прозрачный слой для водяного знака.
4. Определяет размер шрифта на основе размера изображения.
5. Загружает шрифт (Arial, если доступен, иначе шрифт по умолчанию).
6. Вычисляет позицию для размещения текста водяного знака.
7. Рисует текст на прозрачном слое.
8. Объединяет изображение и водяной знак.
9. Сохраняет изображение с водяным знаком в указанный файл.

**Примеры**:

```python
from pathlib import Path
from src.utils.image import add_text_watermark

image_path = Path("test_image.png")  # Замените на путь к существующему изображению
watermark_text = "Hypotez"
output_path = Path("watermarked_image.png")
result = add_text_watermark(image_path, watermark_text, output_path)
if result:
    print(f"Watermarked image saved to {result}")
```

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
Добавляет изображение водяного знака на другое изображение.

**Параметры**:
- `input_image_path` (Path): Путь к исходному изображению.
- `watermark_image_path` (Path): Путь к изображению водяного знака.
- `output_image_path` (Optional[Path], optional): Путь для сохранения изображения с водяным знаком. Если не указан, изображение будет сохранено в директории "output" в той же директории, что и исходное изображение.

**Возвращает**:
- `Optional[Path]`: Путь к сохраненному изображению с водяным знаком или None в случае ошибки.

**Как работает функция**:
1. Открывает исходное изображение и изображение водяного знака с помощью `Image.open`.
2. Преобразует водяной знак в формат RGBA.
3. Изменяет размер водяного знака в зависимости от размеров исходного изображения.
4. Вычисляет позицию для размещения водяного знака (в правом нижнем углу с отступом 20 пикселей).
5. Создает новый прозрачный слой и вставляет на него исходное изображение и водяной знак.
6. Преобразует прозрачный слой в формат исходного изображения.
7. Сохраняет конечное изображение в указанном пути.

**Примеры**:

```python
from pathlib import Path
from src.utils.image import add_image_watermark

input_image_path = Path("test_image.png")  # Замените на путь к существующему изображению
watermark_image_path = Path("watermark.png")  # Замените на путь к существующему изображению водяного знака
output_image_path = Path("watermarked_image.png")
result = add_image_watermark(input_image_path, watermark_image_path, output_image_path)
if result:
    print(f"Watermarked image saved to {result}")
```

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
- `image_path` (Union[str, Path]): Путь к файлу изображения.
- `size` (Tuple[int, int]): Кортеж, содержащий желаемую ширину и высоту изображения.
- `output_path` (Optional[Union[str, Path]], optional): Путь для сохранения изображения измененного размера. Если не указан, исходное изображение будет перезаписано.

**Возвращает**:
- `Optional[str]`: Путь к изображению измененного размера или None в случае ошибки.

**Как работает функция**:
1. Открывает изображение с помощью `Image.open`.
2. Изменяет размер изображения с помощью `img.resize(size)`.
3. Сохраняет изображение измененного размера в указанный файл.

**Примеры**:

```python
from pathlib import Path
from src.utils.image import resize_image

image_path = Path("test_image.png")  # Замените на путь к существующему изображению
size = (128, 128)
output_path = Path("resized_image.png")
result = resize_image(image_path, size, output_path)
if result:
    print(f"Resized image saved to {result}")
```

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
- `image_path` (Union[str, Path]): Путь к файлу изображения.
- `format` (str): Формат для преобразования изображения (например, "JPEG", "PNG").
- `output_path` (Optional[Union[str, Path]], optional): Путь для сохранения преобразованного изображения. Если не указан, исходное изображение будет перезаписано.

**Возвращает**:
- `Optional[str]`: Путь к преобразованному изображению или None в случае ошибки.

**Как работает функция**:
1. Открывает изображение с помощью `Image.open`.
2. Сохраняет изображение в указанном формате в указанный файл.

**Примеры**:

```python
from pathlib import Path
from src.utils.image import convert_image

image_path = Path("test_image.png")  # Замените на путь к существующему изображению
format = "JPEG"
output_path = Path("converted_image.jpg")
result = convert_image(image_path, format, output_path)
if result:
    print(f"Converted image saved to {result}")
```

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
- `folder_path` (Path): Путь к папке, содержащей изображения.
- `watermark_path` (Path): Путь к изображению водяного знака.

**Возвращает**:
- None

**Как работает функция**:
1. Проверяет, существует ли указанная папка.
2. Создает директорию "output", если она не существует.
3. Перебирает все файлы в указанной папке.
4. Если файл является изображением (с расширением `.png`, `.jpg`, `.jpeg`), вызывает функцию `add_image_watermark` для добавления водяного знака и сохранения изображения в директории "output".

**Примеры**:

```python
from pathlib import Path
from src.utils.image import process_images_with_watermark

folder = Path("images")  # Замените на путь к папке с изображениями
watermark = Path("watermark.png")  # Замените на путь к изображению водяного знака
process_images_with_watermark(folder, watermark)
```

## Переменные

Отсутствуют

## Запуск

Для использования данного модуля необходимо установить библиотеку `Pillow` и `aiohttp`.

```bash
pip install Pillow aiohttp aiofiles
```

```python
import asyncio
from pathlib import Path
from src.utils.image import save_image_from_url_async, random_image

async def main():
    image_url = "https://www.easygifanimator.net/images/samples/video-to-gif-sample.gif"
    filename = "downloaded_image.gif"
    result = await save_image_from_url_async(image_url, filename)
    if result:
        print(f"Image saved to {result}")

    root_path = Path(".")
    random_image_path = random_image(root_path)
    if random_image_path:
        print(f"Random image found: {random_image_path}")
asyncio.run(main())