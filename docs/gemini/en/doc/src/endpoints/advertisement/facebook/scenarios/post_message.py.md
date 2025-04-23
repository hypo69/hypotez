# Module for Posting Messages on Facebook

## Overview

This module provides functionality for posting messages, including text and media, to Facebook using a Selenium WebDriver. It includes functions to handle the posting process, media uploads, and caption updates.

## More details

This module is designed to automate the process of posting content to Facebook. It uses locators defined in a JSON file to interact with the Facebook webpage. The module provides functions for posting a title and description, uploading media files, updating captions, and publishing the post. It handles different scenarios, such as single image posts and posts with multiple media files.

## Table of Contents

- [Classes](#classes)
- [Functions](#functions)
    - [post_title](#post_title)
    - [upload_media](#upload_media)
    - [update_images_captions](#update_images_captions)
        - [handle_product](#handle_product)
    - [publish](#publish)
    - [promote_post](#promote_post)
    - [post_message](#post_message)

## Classes

There are no classes in this module.

## Functions

### `post_title`

```python
def post_title(d: Driver, message: SimpleNamespace | str) -> bool:
    """ Sends the title and description of a campaign to the post message box.

    Args:
        d (Driver): The driver instance used for interacting with the webpage.
        message (SimpleNamespace): The message containing the title and description to be sent.

    Returns:
        bool: `True` if the title and description were sent successfully, otherwise `None`.

    Examples:
        >>> driver = Driver(...)
        >>> category = SimpleNamespace(title="Campaign Title", description="Campaign Description")
        >>> post_title(driver, category)
        True
    """
```

**Purpose**: Sends the title and description of a campaign to the post message box on Facebook.

**Parameters**:
- `d` (Driver): The WebDriver instance used to interact with the webpage.
- `message` (SimpleNamespace | str): The message object containing the title and description to be sent.

**Returns**:
- `bool`: `True` if the title and description were sent successfully; otherwise, returns `None`.

**How the function works**:
1. Scrolls backward on the page to ensure the post box is visible.
2. Opens the 'add post' box using a locator.
3. Constructs the message string `m` from the `message` object's `title` and `description` attributes.
4. Adds the message to the post box using a locator.

**Examples**:
```python
driver = Driver(Chrome)
message = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
post_title(driver, message)
```

### `upload_media`

```python
def upload_media(d: Driver, media: SimpleNamespace | List[SimpleNamespace] | str | list[str],   no_video: bool = False, without_captions:bool = False) -> bool:
    """ Uploads media files to the images section and updates captions.

    Args:
        d (Driver): The driver instance used for interacting with the webpage.
        products (List[SimpleNamespace]): List of products containing media file paths.

    Returns:
        bool: `True` if media files were uploaded successfully, otherwise `None`.

    Raises:
        Exception: If there is an error during media upload or caption update.

    Examples:
        >>> driver = Driver(...)
        >>> products = [SimpleNamespace(local_image_path='path/to/image.jpg', ...)]
        >>> upload_media(driver, products)
        True
    """
```

**Purpose**: Uploads media files to the image section on Facebook and updates the captions for the uploaded media.

**Parameters**:
- `d` (Driver): The WebDriver instance used to interact with the webpage.
- `media` (SimpleNamespace | List[SimpleNamespace] | str | list[str]): Media object containing media file paths.
- `no_video` (bool): Flag indicating whether to avoid uploading video files. Defaults to `False`.
- `without_captions` (bool): Flag indicating whether to skip updating captions. Defaults to `False`.

**Returns**:
- `bool`: `True` if the media files were uploaded successfully; otherwise, returns `None`.

**How the function works**:
1. Opens the 'add media' form using a locator.
2. Converts the media to a list if it is not already a list.
3. Iterates over the list of media files and uploads each one.
4. Updates the captions for the uploaded media.

**Examples**:
```python
driver = Driver(Chrome)
products = [SimpleNamespace(local_image_path='путь/к/изображению.jpg')]
upload_media(driver, products)
```

### `update_images_captions`

```python
def update_images_captions(d: Driver, media: List[SimpleNamespace], textarea_list: List[WebElement]) -> None:
    """ Adds descriptions to uploaded media files.

    Args:
        d (Driver): The driver instance used for interacting with the webpage.
        products (List[SimpleNamespace]): List of products with details to update.
        textarea_list (List[WebElement]): List of textareas where captions are added.

    Raises:
        Exception: If there's an error updating the media captions.
    """
```

**Purpose**: Adds descriptions to uploaded media files by sending text to the corresponding textareas.

**Parameters**:
- `d` (Driver): The WebDriver instance used to interact with the webpage.
- `media` (List[SimpleNamespace]): A list of product objects with details to update.
- `textarea_list` (List[WebElement]): A list of textareas where captions are added.

**How the function works**:
1. Loads local units from a JSON file for translation.
2. Iterates through the `media` list (products) and calls `handle_product` for each item.

#### `handle_product`

```python
def handle_product(product: SimpleNamespace, textarea_list: List[WebElement], i: int) -> None:
    """ Handles the update of media captions for a single product.

    Args:
        product (SimpleNamespace): The product to update.
        textarea_list (List[WebElement]): List of textareas where captions are added.
        i (int): Index of the product in the list.
    """
```

**Purpose**: Handles the update of media captions for a single product.

**Parameters**:
- `product` (SimpleNamespace): The product object containing details to update.
- `textarea_list` (List[WebElement]): List of textareas where captions are added.
- `i` (int): Index of the product in the list.

**How the internal function works**:
1. Retrieves language and direction (LTR or RTL) based on the product's `language` attribute.
2. Constructs a message string based on the direction and product details.
3. Sends the message to the appropriate textarea element.

**Examples**:
```python
local_units = j_loads_ns(Path(gs.path.src / 'advertisement' / 'facebook' / 'scenarios' / 'translations.json'))

def handle_product(product: SimpleNamespace, textarea_list: List[WebElement], i: int) -> None:
    lang = product.language.upper()
    direction = getattr(local_units.LOCALE, lang, "LTR")
    message = ""
```

### `publish`

```python
def publish(d:Driver, attempts = 5) -> bool:
    """"""
```

**Purpose**: Publishes the post to Facebook, handling potential pop-up windows or errors during the process.

**Parameters**:
- `d` (Driver): The WebDriver instance used to interact with the webpage.
- `attempts` (int): The number of attempts to publish the post. Defaults to 5.

**Returns**:
- `bool`: `True` if the post was published successfully; otherwise, returns `None`.

**How the function works**:
1. Attempts to click the "finish editing" button.
2. Attempts to click the "publish" button.
3. If publishing fails, it checks for pop-up windows and attempts to close them.
4. Retries publishing the post up to the specified number of attempts.

### `promote_post`

```python
def promote_post(d: Driver, category: SimpleNamespace, products: List[SimpleNamespace], no_video: bool = False) -> bool:
    """ Manages the process of promoting a post with a title, description, and media files.

    Args:
        d (Driver): The driver instance used for interacting with the webpage.
        category (SimpleNamespace): The category details used for the post title and description.
        products (List[SimpleNamespace]): List of products containing media and details to be posted.

    Examples:
        >>> driver = Driver(...)
        >>> category = SimpleNamespace(title="Campaign Title", description="Campaign Description")
        >>> products = [SimpleNamespace(local_image_path='path/to/image.jpg', ...)]
        >>> promote_post(driver, category, products)
    """
```

**Purpose**: Manages the process of promoting a post with a title, description, and media files.

**Parameters**:
- `d` (Driver): The WebDriver instance used to interact with the webpage.
- `category` (SimpleNamespace): The category details used for the post title and description.
- `products` (List[SimpleNamespace]): List of products containing media and details to be posted.
- `no_video` (bool): Flag indicating whether to avoid uploading video files. Defaults to `False`.

**Returns**:
- `bool`: `True` if the post was promoted successfully; otherwise, returns `None`.

**How the function works**:
1. Calls `post_title` to add the title and description to the post.
2. Calls `upload_media` to upload the media files.
3. Clicks the "finish editing" button.
4. Clicks the "publish" button.

**Examples**:
```python
driver = Driver(Chrome)
category = SimpleNamespace(title="Заголовок кампании", description="Описание кампании")
products = [SimpleNamespace(local_image_path='путь/к/изображению.jpg')]
promote_post(driver, category, products)
```

### `post_message`

```python
def post_message(d: Driver, message: SimpleNamespace,  no_video: bool = False,  images:Optional[str | list[str]] = None, without_captions:bool = False) -> bool:
    """ Manages the process of promoting a post with a title, description, and media files.

    Args:
        d (Driver): The driver instance used for interacting with the webpage.
        message (SimpleNamespace): The message details used for the post title and description.
        products (List[SimpleNamespace]): List of products containing media and details to be posted.

    Examples:
        >>> driver = Driver(...)
        >>> category = SimpleNamespace(title="Campaign Title", description="Campaign Description")
        >>> products = [SimpleNamespace(local_image_path='path/to/image.jpg', ...)]
        >>> promote_post(driver, category, products)
    """
```

**Purpose**: Manages the process of posting a message with a title, description, and media files to Facebook.

**Parameters**:
- `d` (Driver): The WebDriver instance used to interact with the webpage.
- `message` (SimpleNamespace): The message object containing the title, description, and media details.
- `no_video` (bool): Flag indicating whether to avoid uploading video files. Defaults to `False`.
- `images` (Optional[str | list[str]]): Optional list of image paths. Defaults to `None`.
- `without_captions` (bool): Flag indicating whether to skip updating captions. Defaults to `False`.

**Returns**:
- `bool`: `True` if the post was created successfully; otherwise, returns `None`.

**How the function works**:
1. Calls `post_title` to add the title and description to the post.
2. Calls `upload_media` to upload the media files.
3. If there is only one image, clicks the "send" button.
4. Clicks the "finish editing" button.
5. Calls `publish` to publish the post.

**Examples**:
```python
driver = Driver(Chrome)
message = SimpleNamespace(title="Заголовок сообщения", description="Описание сообщения", products=[SimpleNamespace(local_image_path='путь/к/изображению.jpg')])
post_message(driver, message)
```