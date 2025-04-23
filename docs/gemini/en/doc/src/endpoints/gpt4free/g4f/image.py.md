# Module for working with images
## Overview

The module provides functions for working with images, including converting images to different formats, checking their validity, and processing them. It uses the PIL (Pillow) library for image manipulation.

## More details

This module provides a set of utility functions to handle images in various formats. It supports converting images from different sources (e.g., file paths, bytes, data URIs) to PIL Image objects and vice versa. It also includes functions for validating image formats, extracting binary data from data URIs, and processing images by adjusting their orientation and size. This module is crucial for applications that require dynamic image handling, such as web services or image processing pipelines.

```rst
 .. module:: src.endpoints.gpt4free.g4f.image
```

## Classes

### `ImageDataResponse`

**Description**: This class encapsulates the response data for images, including the image list and alt text.

**Attributes**:
- `images` (Union[str, list]): Image or list of images.
- `alt` (str): Alternative text for images.

**Methods**:
- `get_list()`: Returns a list of images. If `images` is a string, it encapsulates it in a list.

```python
    class ImageDataResponse():
        """
        Класс, представляющий ответ с данными изображения.

        Attributes:
            images (Union[str, list]): Изображение или список изображений.
            alt (str): Альтернативный текст для изображений.

        Methods:
            get_list() -> list[str]: Возвращает список изображений. Если `images` является строкой, оборачивает ее в список.
        """
```

#### `__init__`

```python
    def __init__(
        self,
        images: Union[str, list],
        alt: str,
    ):
        """
        Конструктор класса ImageDataResponse.

        Args:
            images (Union[str, list]): Изображение или список изображений.
            alt (str): Альтернативный текст для изображений.
        """
```

#### `get_list`

```python
    def get_list(self) -> list[str]:
        """
        Возвращает список изображений. Если `images` является строкой, оборачивает ее в список.

        Returns:
            list[str]: Список изображений.
        """
```

### `ImageRequest`

**Description**: This class encapsulates the request data for images, including the options to be applied when processing the image.

**Attributes**:
- `options` (dict): Options to be applied when processing the image.

**Methods**:
- `get(key: str)`: Returns the value of the option with the specified key.

```python
    class ImageRequest():
        """
        Класс, представляющий запрос изображения.

        Attributes:
            options (dict): Параметры, применяемые при обработке изображения.

        Methods:
            get(key: str) -> Any: Возвращает значение параметра по указанному ключу.
        """
```

#### `__init__`

```python
    def __init__(
        self,
        options: dict = {}
    ):
        """
        Конструктор класса ImageRequest.

        Args:
            options (dict): Параметры, применяемые при обработке изображения.
        """
```

#### `get`

```python
    def get(self, key: str):
        """
        Извлекает значение параметра из словаря параметров.

        Args:
            key (str): Ключ параметра.

        Returns:
            Any: Значение параметра или None, если параметр не найден.
        """
```

## Functions

### `to_image`

**Purpose**: Converts the input image to a PIL Image object.

**Parameters**:
- `image` (ImageType): The input image.
- `is_svg` (bool, optional): Whether the image is an SVG. Defaults to False.

**Returns**:
- `Image`: The converted PIL Image object.

**Raises**:
- `MissingRequirementsError`: If the required libraries (pillow, cairosvg) are not installed.

**How the function works**:
1. Checks if the required libraries are installed. If not, raises a `MissingRequirementsError`.
2. If the image is a data URI, checks its validity and extracts the binary data.
3. If the image is an SVG, converts it to a PNG using `cairosvg`.
4. If the image is bytes, checks if it's an accepted format and opens it using PIL.
5. If the image is not already a PIL Image object, opens it using PIL.
6. Returns the PIL Image object.

**Examples**:
```python
# Пример 1: Преобразование изображения из пути к файлу
image_path = "example.jpg"
image = to_image(image_path)

# Пример 2: Преобразование изображения из байтов
with open(image_path, "rb") as f:
    image_bytes = f.read()
image = to_image(image_bytes)
```

### `is_allowed_extension`

**Purpose**: Checks if the given filename has an allowed extension.

**Parameters**:
- `filename` (str): The filename to check.

**Returns**:
- `bool`: True if the extension is allowed, False otherwise.

**How the function works**:
1. Checks if the filename contains a dot (`.`).
2. Extracts the extension from the filename.
3. Checks if the extension is in the list of allowed extensions.
4. Returns True if the extension is allowed, False otherwise.

**Examples**:
```python
# Пример 1: Проверка допустимого расширения
filename = "example.png"
is_allowed = is_allowed_extension(filename)

# Пример 2: Проверка недопустимого расширения
filename = "example.txt"
is_allowed = is_allowed_extension(filename)
```

### `is_data_uri_an_image`

**Purpose**: Checks if the given data URI represents an image.

**Parameters**:
- `data_uri` (str): The data URI to check.

**Raises**:
- `ValueError`: If the data URI is invalid or the image format is not allowed.

**How the function works**:
1. Checks if the data URI starts with `data:image` and contains an image format (e.g., jpeg, png, gif).
2. Extracts the image format from the data URI.
3. Checks if the image format is one of the allowed formats (jpg, jpeg, png, gif).
4. Raises a `ValueError` if the data URI is invalid or the image format is not allowed.

**Examples**:
```python
# Пример 1: Проверка допустимого data URI
data_uri = "data:image/png;base64,<base64_data>"
is_data_uri_an_image(data_uri)

# Пример 2: Проверка недопустимого data URI
data_uri = "data:text/plain;base64,<base64_data>"
try:
    is_data_uri_an_image(data_uri)
except ValueError as ex:
    print(f"Ошибка: {ex}")
```

### `is_accepted_format`

**Purpose**: Checks if the given binary data represents an image with an accepted format.

**Parameters**:
- `binary_data` (bytes): The binary data to check.

**Returns**:
- `str`: The image format (e.g., "image/jpeg", "image/png", "image/gif", "image/webp").

**Raises**:
- `ValueError`: If the image format is not allowed.

**How the function works**:
1. Checks the first few bytes of the binary data to identify the image format.
2. Returns the image format if it's one of the accepted formats.
3. Raises a `ValueError` if the image format is not allowed.

**Examples**:
```python
# Пример 1: Проверка допустимого формата изображения (JPEG)
with open("example.jpg", "rb") as f:
    image_bytes = f.read()
image_format = is_accepted_format(image_bytes)

# Пример 2: Проверка недопустимого формата изображения
with open("example.txt", "rb") as f:
    image_bytes = f.read()
try:
    image_format = is_accepted_format(image_bytes)
except ValueError as ex:
    print(f"Ошибка: {ex}")
```

### `extract_data_uri`

**Purpose**: Extracts the binary data from the given data URI.

**Parameters**:
- `data_uri` (str): The data URI.

**Returns**:
- `bytes`: The extracted binary data.

**How the function works**:
1. Splits the data URI by `,`.
2. Extracts the last part of the split string, which contains the base64 encoded data.
3. Decodes the base64 data.
4. Returns the binary data.

**Examples**:
```python
# Пример 1: Извлечение данных из data URI
data_uri = "data:image/png;base64,<base64_data>"
image_bytes = extract_data_uri(data_uri)
```

### `get_orientation`

**Purpose**: Gets the orientation of the given image.

**Parameters**:
- `image` (Image): The image.

**Returns**:
- `int`: The orientation value.

**How the function works**:
1. Tries to get the EXIF data from the image.
2. If EXIF data exists, extracts the orientation tag (274).
3. Returns the orientation value if it exists, otherwise returns None.

**Examples**:
```python
# Пример 1: Получение ориентации изображения
image_path = "example.jpg"
image = to_image(image_path)
orientation = get_orientation(image)

# Пример 2: Изображение без EXIF данных
image_path = "example.png"
image = to_image(image_path)
orientation = get_orientation(image)
```

### `process_image`

**Purpose**: Processes the given image by adjusting its orientation and resizing it.

**Parameters**:
- `image` (Image): The image to process.
- `new_width` (int): The new width of the image.
- `new_height` (int): The new height of the image.

**Returns**:
- `Image`: The processed image.

**How the function works**:
1. Fixes the image orientation based on the EXIF data.
2. Resizes the image to the specified dimensions using `thumbnail`.
3. Removes transparency if the image is in RGBA mode by pasting it on a white background.
4. Converts the image to RGB mode if it's not already in that mode.
5. Returns the processed image.

**Examples**:
```python
# Пример 1: Обработка изображения и изменение размера
image_path = "example.png"
image = to_image(image_path)
processed_image = process_image(image, 200, 200)

# Пример 2: Обработка JPEG изображения
image_path = "example.jpg"
image = to_image(image_path)
processed_image = process_image(image, 300, 300)
```

### `to_bytes`

**Purpose**: Converts the given image to bytes.

**Parameters**:
- `image` (ImageType): The image to convert.

**Returns**:
- `bytes`: The image as bytes.

**How the function works**:
1. Checks the type of the image and converts it to bytes accordingly.
2. If the image is already bytes, returns it.
3. If the image is a data URI, extracts the binary data from it.
4. If the image is a PIL Image object, saves it to a BytesIO buffer and returns the buffer's value.
5. If the image is a file path, reads the file and returns the bytes.

**Examples**:
```python
# Пример 1: Преобразование изображения в байты из пути к файлу
image_path = "example.png"
image_bytes = to_bytes(image_path)

# Пример 2: Преобразование изображения в байты из объекта PIL Image
image_path = "example.jpg"
image = to_image(image_path)
image_bytes = to_bytes(image)
```

### `to_data_uri`

**Purpose**: Converts the given image to a data URI.

**Parameters**:
- `image` (ImageType): The image to convert.

**Returns**:
- `str`: The image as a data URI.

**How the function works**:
1. Checks if the image is already a string. If so, returns it directly.
2. Otherwise, converts the image to bytes using `to_bytes`.
3. Base64 encodes the bytes.
4. Returns the data URI string.

**Examples**:
```python
# Пример 1: Преобразование изображения в data URI из пути к файлу
image_path = "example.png"
data_uri = to_data_uri(image_path)

# Пример 2: Преобразование изображения в data URI из объекта PIL Image
image_path = "example.jpg"
image = to_image(image_path)
data_uri = to_data_uri(image)
```