# Модуль: src.utils.image

## Обзор

Модуль предоставляет асинхронные функции для загрузки, сохранения и обработки изображений. Он включает в себя функциональность, такую как сохранение изображений из URL-адресов, сохранение данных изображения в файлы, извлечение данных изображения, поиск случайных изображений в каталогах, добавление водяных знаков, изменение размера и преобразование форматов изображений.

## Подробнее

Этот модуль предоставляет набор инструментов для асинхронной работы с изображениями, что позволяет эффективно выполнять операции, такие как загрузка, сохранение и изменение изображений. Он также включает функции для добавления водяных знаков и преобразования форматов изображений.

## Классы

### `ImageError`

**Описание**: Пользовательское исключение для ошибок, связанных с изображениями.

**Наследует**:
  - `Exception`: Стандартный класс исключений Python.

**Атрибуты**:
  - Отсутствуют.

**Методы**:
  - Отсутствуют.

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
```

**Назначение**: Асинхронно загружает изображение по URL-адресу и сохраняет его локально.

**Параметры**:
- `image_url` (str): URL-адрес изображения для загрузки.
- `filename` (Union[str, Path]): Имя файла для сохранения изображения.

**Возвращает**:
- `Optional[str]`: Путь к сохраненному файлу или `None`, если операция не удалась.

**Вызывает**:
- `ImageError`: Если загрузка или сохранение изображения не удались.

**Как работает**:
1. Пытается асинхронно загрузить изображение по указанному URL-адресу.
2. Если загрузка прошла успешно, вызывает функцию `save_image_async` для сохранения данных изображения в файл.
3. В случае ошибки логирует ошибку и возвращает `None`.

**Примеры**:
```python
image_url = "https://example.com/image.png"
filename = "path/to/save/image.png"
result = await save_image_from_url_async(image_url, filename)
if result:
    print(f"Image saved to {result}")
else:
    print("Failed to save image")
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
```

**Назначение**: Сохраняет данные изображения в файл в указанном формате.

**Параметры**:
- `image_data` (bytes): Бинарные данные изображения.
- `file_name` (Union[str, Path]): Имя файла для сохранения изображения.
- `format` (str): Формат сохранения изображения, по умолчанию 'PNG'.

**Возвращает**:
- `Optional[str]`: Путь к сохраненному файлу или `None`, если операция не удалась.

**Вызывает**:
- `ImageError`: Если файл не может быть создан, сохранен, или если сохраненный файл пуст.

**Как работает**:
1. Создает путь к файлу на основе переданного имени файла.
2. Создает родительские каталоги, если они не существуют.
3. Использует `BytesIO` для работы с данными изображения в памяти.
4. Открывает изображение с помощью `PIL.Image.open`.
5. Сохраняет изображение в указанном формате.
6. Записывает отформатированные данные изображения в файл.
7. Проверяет, был ли создан файл и не является ли он пустым.
8. Логирует ошибки, если файл не был создан или имеет нулевой размер.
9. Возвращает путь к сохраненному файлу или `None` в случае ошибки.

**Примеры**:
```python
image_data = b"..."  # some image data
filename = "path/to/save/image.png"
result = save_image(image_data, filename)
if result:
    print(f"Image saved to {result}")
else:
    print("Failed to save image")
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
```

**Назначение**: Асинхронно сохраняет данные изображения в файл в указанном формате.

**Параметры**:
- `image_data` (bytes): Бинарные данные изображения.
- `file_name` (Union[str, Path]): Имя файла для сохранения изображения.
- `format` (str): Формат сохранения изображения, по умолчанию 'PNG'.

**Возвращает**:
- `Optional[str]`: Путь к сохраненному файлу или `None`, если операция не удалась.

**Вызывает**:
- `ImageError`: Если файл не может быть создан, сохранен, или если сохраненный файл пуст.

**Как работает**:
1. Создает путь к файлу на основе переданного имени файла.
2. Асинхронно создает родительские каталоги, если они не существуют.
3. Использует `aiofiles` для асинхронной записи данных изображения в файл.
4. Проверяет, был ли создан файл и не является ли он пустым.
5. Логирует ошибки, если файл не был создан или имеет нулевой размер.
6. Возвращает путь к сохраненному файлу или `None` в случае ошибки.

**Примеры**:
```python
image_data = b"..."  # some image data
filename = "path/to/save/image.png"
result = await save_image_async(image_data, filename)
if result:
    print(f"Image saved to {result}")
else:
    print("Failed to save image")
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
```

**Назначение**: Читает изображение с помощью Pillow и возвращает его байты в формате JPEG.

**Параметры**:
- `image_path` (Path): Путь к файлу изображения.
- `raw` (bool): Если `True`, возвращает объект `BytesIO`; в противном случае возвращает байты. По умолчанию `True`.

**Возвращает**:
- `Optional[Union[BytesIO, bytes]]`: Байты изображения в формате JPEG или `None`, если произошла ошибка.

**Как работает**:
1. Открывает изображение с помощью `PIL.Image.open`.
2. Создает объект `BytesIO`.
3. Сохраняет изображение в формате JPEG в объект `BytesIO`.
4. Возвращает объект `BytesIO` или байты изображения в зависимости от значения параметра `raw`.
5. В случае ошибки логирует ошибку и возвращает `None`.

**Примеры**:
```python
image_path = Path("path/to/image.png")
image_bytes = get_image_bytes(image_path)
if image_bytes:
    print("Image bytes retrieved")
else:
    print("Failed to retrieve image bytes")
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
```

**Назначение**: Извлекает необработанные бинарные данные файла, если он существует.

**Параметры**:
- `file_name` (Union[str, Path]): Имя или путь к файлу для чтения.

**Возвращает**:
- `Optional[bytes]`: Бинарные данные файла или `None`, если файл не существует или произошла ошибка.

**Как работает**:
1. Создает путь к файлу на основе переданного имени файла.
2. Проверяет, существует ли файл.
3. Если файл существует, читает его байты и возвращает их.
4. Если файл не существует или произошла ошибка, логирует ошибку и возвращает `None`.

**Примеры**:
```python
filename = "path/to/file.txt"
file_data = get_raw_image_data(filename)
if file_data:
    print("File data retrieved")
else:
    print("Failed to retrieve file data")
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
```

**Назначение**: Рекурсивно ищет случайное изображение в указанном каталоге.

**Параметры**:
- `root_path` (Union[str, Path]): Каталог для поиска изображений.

**Возвращает**:
- `Optional[str]`: Путь к случайному изображению или `None`, если изображения не найдены.

**Как работает**:
1. Создает путь к каталогу на основе переданного пути.
2. Определяет список расширений файлов изображений.
3. Рекурсивно ищет все файлы с указанными расширениями в каталоге.
4. Если изображения не найдены, логирует предупреждение и возвращает `None`.
5. Если изображения найдены, выбирает случайное изображение и возвращает его путь.

**Примеры**:
```python
root_path = "path/to/images"
random_image_path = random_image(root_path)
if random_image_path:
    print(f"Random image found: {random_image_path}")
else:
    print("No images found")
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
```

**Назначение**: Добавляет текстовый водяной знак на изображение.

**Параметры**:
- `image_path` (Union[str, Path]): Путь к файлу изображения.
- `watermark_text` (str): Текст для использования в качестве водяного знака.
- `output_path` (Optional[Union[str, Path]]): Путь для сохранения изображения с водяным знаком. По умолчанию перезаписывает исходное изображение.

**Возвращает**:
- `Optional[str]`: Путь к изображению с водяным знаком или `None` в случае неудачи.

**Как работает**:
1. Открывает изображение с помощью `PIL.Image.open` и преобразует его в формат RGBA.
2. Создает прозрачный слой для водяного знака.
3. Определяет размер шрифта на основе размера изображения.
4. Загружает шрифт arial.ttf, если он доступен, в противном случае использует шрифт по умолчанию.
5. Определяет размеры текста водяного знака.
6. Вычисляет координаты для размещения текста по центру изображения.
7. Рисует текст на прозрачном слое.
8. Объединяет изображение и водяной знак.
9. Сохраняет изображение с водяным знаком.
10. Возвращает путь к изображению с водяным знаком или `None` в случае ошибки.

**Примеры**:
```python
image_path = "path/to/image.png"
watermark_text = "Watermark"
output_path = "path/to/watermarked_image.png"
result = add_text_watermark(image_path, watermark_text, output_path)
if result:
    print(f"Watermark added to {result}")
else:
    print("Failed to add watermark")
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
```

**Назначение**: Добавляет изображение в качестве водяного знака на другое изображение и сохраняет результат в указанный путь вывода.

**Параметры**:
- `input_image_path` (Path): Путь к входному изображению.
- `watermark_image_path` (Path): Путь к изображению водяного знака.
- `output_image_path` (Optional[Path]): Путь для сохранения изображения с водяным знаком. Если не указан, изображение будет сохранено в каталоге "output".

**Возвращает**:
- `Optional[Path]`: Путь к сохраненному изображению с водяным знаком или `None`, если операция не удалась.

**Как работает**:
1. Открывает базовое изображение.
2. Открывает изображение водяного знака и преобразует его в формат RGBA.
3. Устанавливает размер водяного знака (8% от ширины базового изображения).
4. Определяет позицию для размещения водяного знака (нижний правый угол с отступом 20px).
5. Создает новый прозрачный слой для объединения изображений.
6. Вставляет базовое изображение на новый слой.
7. Вставляет водяной знак поверх базового изображения.
8. Проверяет режим изображения и преобразует прозрачный слой в исходный режим.
9. Сохраняет окончательное изображение в указанный путь вывода с оптимизированным качеством.
10. Возвращает путь к сохраненному изображению с водяным знаком или `None` в случае ошибки.

**Примеры**:
```python
input_image_path = Path("path/to/image.png")
watermark_image_path = Path("path/to/watermark.png")
output_image_path = Path("path/to/watermarked_image.png")
result = add_image_watermark(input_image_path, watermark_image_path, output_image_path)
if result:
    print(f"Watermark added to {result}")
else:
    print("Failed to add watermark")
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
```

**Назначение**: Изменяет размер изображения до указанных размеров.

**Параметры**:
- `image_path` (Union[str, Path]): Путь к файлу изображения.
- `size` (Tuple[int, int]): Кортеж, содержащий желаемую ширину и высоту изображения.
- `output_path` (Optional[Union[str, Path]]): Путь для сохранения измененного изображения. По умолчанию перезаписывает исходное изображение.

**Возвращает**:
- `Optional[str]`: Путь к измененному изображению или `None` в случае неудачи.

**Как работает**:
1. Открывает изображение с помощью `PIL.Image.open`.
2. Изменяет размер изображения до указанных размеров.
3. Сохраняет измененное изображение.
4. Возвращает путь к измененному изображению или `None` в случае ошибки.

**Примеры**:
```python
image_path = "path/to/image.png"
size = (800, 600)
output_path = "path/to/resized_image.png"
result = resize_image(image_path, size, output_path)
if result:
    print(f"Image resized to {result}")
else:
    print("Failed to resize image")
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
```

**Назначение**: Преобразует изображение в указанный формат.

**Параметры**:
- `image_path` (Union[str, Path]): Путь к файлу изображения.
- `format` (str): Формат для преобразования изображения (например, "JPEG", "PNG").
- `output_path` (Optional[Union[str, Path]]): Путь для сохранения преобразованного изображения. По умолчанию перезаписывает исходное изображение.

**Возвращает**:
- `Optional[str]`: Путь к преобразованному изображению или `None` в случае неудачи.

**Как работает**:
1. Открывает изображение с помощью `PIL.Image.open`.
2. Сохраняет изображение в указанном формате.
3. Возвращает путь к преобразованному изображению или `None` в случае ошибки.

**Примеры**:
```python
image_path = "path/to/image.png"
format = "JPEG"
output_path = "path/to/converted_image.jpg"
result = convert_image(image_path, format, output_path)
if result:
    print(f"Image converted to {result}")
else:
    print("Failed to convert image")
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
```

**Назначение**: Обрабатывает все изображения в указанной папке, добавляя водяной знак и сохраняя их в каталоге "output".

**Параметры**:
- `folder_path` (Path): Путь к папке, содержащей изображения.
- `watermark_path` (Path): Путь к изображению водяного знака.

**Как работает**:
1. Проверяет, существует ли указанная папка.
2. Создает каталог "output", если он не существует.
3. Перебирает все файлы в папке.
4. Если файл является изображением (с расширением .png, .jpg, .jpeg), добавляет водяной знак и сохраняет его в каталоге "output".

**Примеры**:
```python
folder_path = Path("path/to/images")
watermark_path = Path("path/to/watermark.png")
process_images_with_watermark(folder_path, watermark_path)