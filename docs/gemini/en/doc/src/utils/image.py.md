# Image Processing Utilities

## Overview

This module provides asynchronous functions for downloading, saving, and manipulating images. It includes functionalities such as saving images from URLs, saving image data to files, retrieving image data, finding random images within directories, adding watermarks, resizing, and converting image formats.

## Details

This module is used for image processing tasks. It includes functions for:

- Downloading images from URLs asynchronously
- Saving image data to files asynchronously and synchronously
- Retrieving raw image data from files
- Finding random images within directories
- Adding text and image watermarks to images
- Resizing images to specified dimensions
- Converting images to different formats

## Classes

### `ImageError`

**Description**: Custom exception class for image-related errors.

## Functions

### `save_image_from_url_async`

**Purpose**: Downloads an image from a URL and saves it locally asynchronously.

**Parameters**:

- `image_url` (str): The URL to download the image from.
- `filename` (Union[str, Path]): The name of the file to save the image to.

**Returns**:

- `Optional[str]`: The path to the saved file, or None if the operation failed.

**Raises Exceptions**:

- `ImageError`: If the image download or save operation fails.

**How the Function Works**:

- Uses `aiohttp` to download the image from the specified URL.
- Reads the image data into a bytes object.
- Calls `save_image_async` to save the image data to the specified file.

**Examples**:

```python
async def example_save_image_from_url_async():
    image_url = "https://example.com/image.jpg"
    filename = "downloaded_image.jpg"
    saved_path = await save_image_from_url_async(image_url, filename)
    if saved_path:
        print(f"Image saved to: {saved_path}")
```

### `save_image`

**Purpose**: Saves image data to a file in the specified format.

**Parameters**:

- `image_data` (bytes): The binary image data.
- `file_name` (Union[str, Path]): The name of the file to save the image to.
- `format` (str): The format to save the image in, default is PNG.

**Returns**:

- `Optional[str]`: The path to the saved file, or None if the operation failed.

**Raises Exceptions**:

- `ImageError`: If the file cannot be created, saved, or if the saved file is empty.

**How the Function Works**:

- Creates the directory for the file if it doesn't exist.
- Uses `BytesIO` to avoid writing to disk twice.
- Opens the `BytesIO` object as an image using `Image.open`.
- Saves the image in the specified format to the `BytesIO` object.
- Writes the formatted image data to the file.
- Verifies that the file was created and is not empty.

**Examples**:

```python
image_data = b"...image data..."
file_name = "saved_image.png"
saved_path = save_image(image_data, file_name)
if saved_path:
    print(f"Image saved to: {saved_path}")
```

### `save_image_async`

**Purpose**: Saves image data to a file in the specified format asynchronously.

**Parameters**:

- `image_data` (bytes): The binary image data.
- `file_name` (Union[str, Path]): The name of the file to save the image to.
- `format` (str): The format to save the image in, default is PNG.

**Returns**:

- `Optional[str]`: The path to the saved file, or None if the operation failed.

**Raises Exceptions**:

- `ImageError`: If the file cannot be created, saved, or if the saved file is empty.

**How the Function Works**:

- Creates the directory for the file asynchronously using `asyncio.to_thread`.
- Uses `BytesIO` to avoid writing to disk twice.
- Opens the `BytesIO` object as an image using `Image.open`.
- Saves the image in the specified format to the `BytesIO` object.
- Writes the formatted image data to the file asynchronously using `aiofiles`.
- Verifies that the file was created and is not empty asynchronously using `aiofiles`.

**Examples**:

```python
async def example_save_image_async():
    image_data = b"...image data..."
    file_name = "saved_image.png"
    saved_path = await save_image_async(image_data, file_name)
    if saved_path:
        print(f"Image saved to: {saved_path}")
```

### `get_image_bytes`

**Purpose**: Reads an image using Pillow and returns its bytes in JPEG format.

**Parameters**:

- `image_path` (Path): The path to the image file.
- `raw` (bool): If True, returns a BytesIO object; otherwise, returns bytes. Defaults to True.

**Returns**:

- `Optional[Union[BytesIO, bytes]]`: The bytes of the image in JPEG format, or None if an error occurs.

**How the Function Works**:

- Opens the image using `Image.open`.
- Creates a `BytesIO` object.
- Saves the image in JPEG format to the `BytesIO` object.
- Returns the `BytesIO` object if `raw` is True, otherwise returns the bytes from the `BytesIO` object.

**Examples**:

```python
image_path = Path("image.jpg")
image_bytes = get_image_bytes(image_path)
if image_bytes:
    print(f"Image bytes: {image_bytes}")
```

### `get_raw_image_data`

**Purpose**: Retrieves the raw binary data of a file if it exists.

**Parameters**:

- `file_name` (Union[str, Path]): The name or path of the file to read.

**Returns**:

- `Optional[bytes]`: The binary data of the file, or None if the file does not exist or an error occurs.

**How the Function Works**:

- Checks if the file exists.
- Reads the file as bytes using `file_path.read_bytes`.

**Examples**:

```python
file_name = "data.bin"
data = get_raw_image_data(file_name)
if data:
    print(f"File data: {data}")
```

### `random_image`

**Purpose**: Recursively searches for a random image in the specified directory.

**Parameters**:

- `root_path` (Union[str, Path]): The directory to search for images.

**Returns**:

- `Optional[str]`: The path to a random image, or None if no images are found.

**How the Function Works**:

- Uses `root_path.rglob("*")` to recursively find all files in the directory.
- Filters the files to only include images based on the `image_extensions` list.
- Randomly selects an image from the list of image files.

**Examples**:

```python
root_path = Path("images")
random_image_path = random_image(root_path)
if random_image_path:
    print(f"Random image found: {random_image_path}")
```

### `add_text_watermark`

**Purpose**: Adds a text watermark to an image.

**Parameters**:

- `image_path` (Union[str, Path]): Path to the image file.
- `watermark_text` (str): Text to use as the watermark.
- `output_path` (Optional[Union[str, Path]]): Path to save the watermarked image. Defaults to overwriting the original image.

**Returns**:

- `Optional[str]`: Path to the watermarked image, or None on failure.

**How the Function Works**:

- Opens the image using `Image.open`.
- Creates a transparent layer for the watermark.
- Draws the watermark text on the transparent layer using `ImageDraw` and `ImageFont`.
- Combines the image and watermark using `Image.alpha_composite`.
- Saves the watermarked image to the specified output path.

**Examples**:

```python
image_path = "image.jpg"
watermark_text = "My Watermark"
watermarked_image_path = add_text_watermark(image_path, watermark_text)
if watermarked_image_path:
    print(f"Watermarked image saved to: {watermarked_image_path}")
```

### `add_image_watermark`

**Purpose**: Adds a watermark to an image and saves the result to the specified output path.

**Parameters**:

- `input_image_path` (Path): Path to the input image.
- `watermark_image_path` (Path): Path to the watermark image.
- `output_image_path` (Optional[Path]): Path to save the watermarked image. If not provided, the image will be saved in an "output" directory.

**Returns**:

- `Optional[Path]`: Path to the saved watermarked image, or None if the operation failed.

**How the Function Works**:

- Opens the input and watermark images.
- Resizes the watermark image to 8% of the width of the input image.
- Creates a new transparent layer with the same size as the input image.
- Pastes the input image onto the transparent layer.
- Pastes the watermark onto the transparent layer at the bottom-right corner with padding.
- Converts the transparent layer to the same mode as the input image.
- Saves the final image to the specified output path.

**Examples**:

```python
input_image_path = Path("image.jpg")
watermark_image_path = Path("watermark.png")
watermarked_image_path = add_image_watermark(input_image_path, watermark_image_path)
if watermarked_image_path:
    print(f"Watermarked image saved to: {watermarked_image_path}")
```

### `resize_image`

**Purpose**: Resizes an image to the specified dimensions.

**Parameters**:

- `image_path` (Union[str, Path]): Path to the image file.
- `size` (Tuple[int, int]): A tuple containing the desired width and height of the image.
- `output_path` (Optional[Union[str, Path]]): Path to save the resized image. Defaults to overwriting the original image.

**Returns**:

- `Optional[str]`: Path to the resized image, or None on failure.

**How the Function Works**:

- Opens the image using `Image.open`.
- Resizes the image using `img.resize`.
- Saves the resized image to the specified output path.

**Examples**:

```python
image_path = "image.jpg"
size = (200, 200)
resized_image_path = resize_image(image_path, size)
if resized_image_path:
    print(f"Resized image saved to: {resized_image_path}")
```

### `convert_image`

**Purpose**: Converts an image to the specified format.

**Parameters**:

- `image_path` (Union[str, Path]): Path to the image file.
- `format` (str): Format to convert image to (e.g., "JPEG", "PNG").
- `output_path` (Optional[Union[str, Path]]): Path to save the converted image. Defaults to overwriting the original image.

**Returns**:

- `Optional[str]`: Path to the converted image or None on failure.

**How the Function Works**:

- Opens the image using `Image.open`.
- Saves the image in the specified format to the specified output path.

**Examples**:

```python
image_path = "image.jpg"
format = "PNG"
converted_image_path = convert_image(image_path, format)
if converted_image_path:
    print(f"Converted image saved to: {converted_image_path}")
```

### `process_images_with_watermark`

**Purpose**: Processes all images in the specified folder by adding a watermark and saving them in an "output" directory.

**Parameters**:

- `folder_path` (Path): Path to the folder containing images.
- `watermark_path` (Path): Path to the watermark image.

**How the Function Works**:

- Checks if the folder exists.
- Creates an "output" directory if it doesn't exist.
- Iterates through each file in the folder.
- If the file is an image, it calls `add_image_watermark` to add the watermark to the image and save it to the "output" directory.

**Examples**:

```python
folder_path = Path("images")
watermark_path = Path("watermark.png")
process_images_with_watermark(folder_path, watermark_path)
```

## Example Usage

```python
if __name__ == "__main__":
    folder = Path(input("Enter Folder Path: "))  # Path to the folder containing images
    watermark = Path(input("Enter Watermark Path: "))  # Path to the watermark image

    process_images_with_watermark(folder, watermark)
```