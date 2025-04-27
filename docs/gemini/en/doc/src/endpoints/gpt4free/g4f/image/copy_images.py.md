# Module for copying and storing images from URLs
## Overview
This module provides functions and tools for downloading and storing images from various sources, including URLs, data URIs, and local files. It ensures the creation of safe and Unicode-compatible filenames and supports handling different image types.

## Details
The module utilizes `aiohttp` library for asynchronous HTTP requests, and `hashlib` for generating unique identifiers for each image. 

The main function of the module is `copy_media`, which downloads and stores images locally, returning a list of relative image URLs for further use. The module also provides auxiliary functions like `get_media_extension`, `ensure_images_dir`, and `get_filename` that support the main function. 

## Functions
### `get_media_extension`
**Purpose**:  Извлечение расширения файла из URL или имени файла.

**Parameters**:
- `media` (str): URL или имя файла, из которого необходимо извлечь расширение.

**Returns**:
- `str`:  Расширение файла без точки.

**Raises Exceptions**:
- `ValueError`:  Если расширение файла не поддерживается.

**How the Function Works**:
- The function first attempts to extract the extension from the path of the URL using `urllib.parse.urlparse`.
- If no extension is found, it extracts the extension from the original `media` string.
- It then checks if the extension is supported and returns it.
- If the extension is not supported, it raises a `ValueError`.

**Examples**:
```python
>>> get_media_extension("https://example.com/image.jpg")
'jpg'

>>> get_media_extension("image.png")
'png'

>>> get_media_extension("https://example.com/image")
''
```

### `ensure_images_dir`
**Purpose**: Создание директории для хранения изображений, если она не существует.

**Parameters**: None

**Returns**: None

**Raises Exceptions**: None

**How the Function Works**:
- The function uses `os.makedirs` to create the directory `./generated_images` if it does not already exist. The `exist_ok=True` argument ensures that the function does not raise an error if the directory already exists.

**Examples**:
```python
>>> ensure_images_dir()
# Creates the directory ./generated_images if it does not exist.
```

### `get_source_url`
**Purpose**: Извлечение исходного URL из параметра `image`, если он присутствует.

**Parameters**:
- `image` (str): Строка, содержащая параметр `image`.
- `default` (str): Значение по умолчанию, которое будет возвращено, если исходный URL не найден.

**Returns**:
- `str`: Исходный URL, если он найден; в противном случае возвращается значение по умолчанию.

**Raises Exceptions**: None

**How the Function Works**:
- The function checks if the `image` string contains the substring `url=`. If it does, it extracts the decoded URL from the string and returns it.
- If the `url=` substring is not found, the function returns the `default` value.

**Examples**:
```python
>>> get_source_url("image.jpg?url=https://example.com/image.jpg")
'https://example.com/image.jpg'

>>> get_source_url("image.jpg")
None

>>> get_source_url("image.jpg", "https://example.com/default.jpg")
'https://example.com/default.jpg'
```

### `is_valid_media_type`
**Purpose**: Проверка типа контента на допустимость.

**Parameters**:
- `content_type` (str): Тип контента, который необходимо проверить.

**Returns**:
- `bool`: `True`, если тип контента допустим; в противном случае `False`.

**Raises Exceptions**: None

**How the Function Works**:
- The function checks if the `content_type` is in the `MEDIA_TYPE_MAP` dictionary or starts with `audio/` or `video/`.
- If the content type is valid, the function returns `True`.
- Otherwise, it returns `False`.

**Examples**:
```python
>>> is_valid_media_type("image/jpeg")
True

>>> is_valid_media_type("audio/mpeg")
True

>>> is_valid_media_type("text/plain")
False
```

### `save_response_media`
**Purpose**:  Сохранение медиафайла из ответа на запрос в локальный файл и возвращение URL.

**Parameters**:
- `response` (StreamResponse): Ответ на запрос, содержащий медиафайл.
- `prompt` (str): Текст запроса, использованный для генерации медиафайла.
- `tags` (list[str]):  Список тегов, связанных с медиафайлом.

**Returns**:
- `AsyncIterator`: Генератор, возвращающий объект `ImageResponse`, `AudioResponse` или `VideoResponse`, содержащий URL медиафайла.

**Raises Exceptions**:
- `ValueError`:  Если тип контента не поддерживается.

**How the Function Works**:
- The function first extracts the content type from the response headers.
- Then it determines the file extension based on the content type and generates a unique filename using the `get_filename` function.
- The function opens the file in write-binary mode (`'wb'`) and writes the content of the response to the file.
- Finally, it builds the URL of the saved media file and yields an appropriate response object: `ImageResponse`, `AudioResponse`, or `VideoResponse`.

**Examples**:
```python
>>> response = ... # assume a response object
>>> prompt = "Generate a picture of a cat"
>>> tags = ["cat", "animal"]
>>> async for media_response in save_response_media(response, prompt, tags):
...     print(media_response.url)
...
/media/1679401195_cat+animal_f56007666574_jpg
```

### `get_filename`
**Purpose**:  Создание уникального имени файла для медиафайла.

**Parameters**:
- `tags` (list[str]): Список тегов, связанных с медиафайлом.
- `alt` (str):  Альтернативный текст для медиафайла.
- `extension` (str): Расширение файла.
- `image` (str):  URL или имя файла, из которого был получен медиафайл.

**Returns**:
- `str`:  Уникальное имя файла с расширением.

**Raises Exceptions**: None

**How the Function Works**:
- The function generates a filename based on the current timestamp, tags, alternative text, a 16-character hash of the `image` string, and the provided extension.
- It uses `secure_filename` to sanitize the input strings and ensure that the filename is safe for use in the filesystem.

**Examples**:
```python
>>> get_filename(["cat", "animal"], "A cute cat", ".jpg", "https://example.com/image.jpg")
'1679401195_cat+animal_A+cute+cat_f56007666574_jpg'

>>> get_filename([], "A beautiful landscape", ".png", "data:image/png;base64,...")
'1679401195_A+beautiful+landscape_456789012345_png'
```

### `copy_media`
**Purpose**:  Загрузка и сохранение медиафайлов локально с Unicode-безопасными именами файлов.

**Parameters**:
- `images` (list[str]):  Список URL или имен файлов медиафайлов.
- `cookies` (Optional[Cookies]):  Словарь с куки, которые должны быть отправлены с запросом.
- `headers` (Optional[dict]):  Словарь с заголовками запроса.
- `proxy` (Optional[str]):  Адрес прокси-сервера.
- `alt` (str): Альтернативный текст для медиафайла.
- `tags` (list[str]): Список тегов, связанных с медиафайлом.
- `add_url` (bool): Флаг, определяющий, нужно ли добавлять исходный URL к имени файла.
- `target` (str): Путь к целевому файлу.
- `ssl` (bool): Флаг, определяющий, нужно ли использовать SSL для запроса.

**Returns**:
- `list[str]`: Список относительных URL сохраненных медиафайлов.

**Raises Exceptions**: None

**How the Function Works**:
- The function iterates through the list of `images` and downloads each one using the `copy_image` function.
- It creates a unique filename for each image using the `get_filename` function.
- The function supports downloading from URLs, data URIs, and local files.
- It also supports using a proxy server and sending custom cookies and headers with requests.
- If `add_url` is set to `True`, the function adds the source URL to the filename.
- The function handles different image types, including images, audio files, and videos.

**Examples**:
```python
>>> await copy_media(["https://example.com/image1.jpg", "https://example.com/image2.png"], tags=["cat", "animal"], alt="A cute cat")
['/media/1679401195_cat+animal_A+cute+cat_f56007666574_jpg?url=https%3A%2F%2Fexample.com%2Fimage1.jpg', '/media/1679401195_cat+animal_A+cute+cat_f56007666574_png?url=https%3A%2F%2Fexample.com%2Fimage2.png']

>>> await copy_media(["data:image/jpeg;base64,..."], alt="A beautiful landscape")
['/media/1679401195_A+beautiful+landscape_456789012345_jpg']

>>> await copy_media(["/local/image.jpg"], target="/path/to/target/image.jpg")
['/path/to/target/image.jpg']
```

### `copy_image`
**Purpose**:  Обработка отдельного изображения и возврат его локального URL.

**Parameters**:
- `image` (str): URL или имя файла изображения.
- `target` (str): Путь к целевому файлу.

**Returns**:
- `str`: Локальный URL изображения.

**Raises Exceptions**:
- `ClientError`:  Если возникает ошибка при выполнении HTTP-запроса.
- `IOError`:  Если возникает ошибка при чтении или записи в файл.
- `OSError`:  Если возникает ошибка при работе с файловой системой.
- `ValueError`:  Если тип контента не поддерживается.

**How the Function Works**:
- The function checks if the `image` is already a local file. If it is, it returns the `image` as is.
- If `target` is not provided, the function generates a unique filename using `get_filename` and saves the image to the `./generated_images` directory.
- If `target` is provided, the function saves the image to the specified location.
- The function supports downloading from URLs, data URIs, and local files.
- It also supports using custom headers and SSL for requests.
- If the image type is not recognized, the function attempts to guess the type based on the file header.
- If the download fails, the function logs an error message and returns the original `image` URL.

**Examples**:
```python
>>> await copy_image("https://example.com/image.jpg")
'/media/1679401195_A+cute+cat_f56007666574_jpg?url=https%3A%2F%2Fexample.com%2Fimage.jpg'

>>> await copy_image("data:image/jpeg;base64,...", target="/path/to/target/image.jpg")
'/path/to/target/image.jpg'

>>> await copy_image("/local/image.jpg")
'/local/image.jpg'
```

## Parameter Details
- `media` (str): URL or filename from which to extract the file extension.
- `default` (str): Default value to return if the source URL is not found.
- `content_type` (str): Content type to validate.
- `response` (StreamResponse): Response object containing the media file.
- `prompt` (str): Prompt text used to generate the media file.
- `tags` (list[str]): List of tags associated with the media file.
- `alt` (str): Alternative text for the media file.
- `extension` (str): File extension.
- `image` (str): URL or filename of the media file.
- `cookies` (Optional[Cookies]): Dictionary of cookies to send with the request.
- `headers` (Optional[dict]): Dictionary of request headers.
- `proxy` (Optional[str]): Proxy server address.
- `add_url` (bool): Flag indicating whether to add the source URL to the filename.
- `target` (str): Path to the target file.
- `ssl` (bool): Flag indicating whether to use SSL for the request.

## Examples

**Example 1: Downloading images from URLs:**
```python
>>> import asyncio
>>> from hypotez.src.endpoints.gpt4free.g4f.image.copy_images import copy_media
>>> async def main():
...     image_urls = ["https://example.com/image1.jpg", "https://example.com/image2.png"]
...     image_paths = await copy_media(image_urls, tags=["cat", "animal"], alt="A cute cat")
...     print(image_paths)
>>> asyncio.run(main())
['/media/1679401195_cat+animal_A+cute+cat_f56007666574_jpg?url=https%3A%2F%2Fexample.com%2Fimage1.jpg', '/media/1679401195_cat+animal_A+cute+cat_f56007666574_png?url=https%3A%2F%2Fexample.com%2Fimage2.png']
```

**Example 2: Downloading images from data URIs:**
```python
>>> import asyncio
>>> from hypotez.src.endpoints.gpt4free.g4f.image.copy_images import copy_media
>>> async def main():
...     data_uri = "data:image/jpeg;base64,...".encode('utf-8')
...     image_paths = await copy_media([data_uri.decode('utf-8')], alt="A beautiful landscape")
...     print(image_paths)
>>> asyncio.run(main())
['/media/1679401195_A+beautiful+landscape_456789012345_jpg']
```

**Example 3: Saving images to a specific location:**
```python
>>> import asyncio
>>> from hypotez.src.endpoints.gpt4free.g4f.image.copy_images import copy_media
>>> async def main():
...     image_urls = ["https://example.com/image1.jpg"]
...     target_path = "/path/to/target/image1.jpg"
...     image_paths = await copy_media(image_urls, target=target_path)
...     print(image_paths)
>>> asyncio.run(main())
['/path/to/target/image1.jpg']
```