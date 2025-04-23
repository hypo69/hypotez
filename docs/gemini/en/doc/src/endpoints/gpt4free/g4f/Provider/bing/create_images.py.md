# Module for Creating Images Using Bing Service

## Overview

This module provides functionality to generate images based on a given text prompt using the Bing image creation service. It handles session creation, request submission, polling for results, and extraction of image URLs from the response.

## More details

This module is a part of the `hypotez` project and allows users to programmatically generate images using the Bing image creation service. It is used to automate the process of creating images from text prompts. The module ensures that the necessary requirements are installed, handles potential errors such as rate limits and blocked prompts, and extracts the generated image URLs for further use.

## Classes

### `create_session`

**Description**: Creates a new client session with specified cookies and headers.

**Parameters**:
- `cookies` (Dict[str, str]): Cookies to be used for the session.
- `proxy` (str, optional): Proxy configuration.
- `connector` (BaseConnector, optional): The connector to use for the session.

**Working principle**:
The function initializes a client session with custom headers and cookies. It configures the session to mimic a browser request, setting headers such as `accept`, `accept-encoding`, `accept-language`, and `user-agent`. If cookies are provided, they are added to the headers. The session also uses a connector, which can be customized using `get_connector` for proxy support.

**Methods**:
- None

```python
def create_session(cookies: Dict[str, str], proxy: str = None, connector: BaseConnector = None) -> ClientSession:
    """
    Creates a new client session with specified cookies and headers.

    Args:
        cookies (Dict[str, str]): Cookies to be used for the session.
        proxy (str, optional): Proxy configuration.
        connector (BaseConnector, optional): The connector to use for the session.

    Returns:
        ClientSession: The created client session.
    """
```

### `create_images`

**Description**: Creates images based on a given prompt using Bing's service.

**Parameters**:
- `session` (ClientSession): Active client session.
- `prompt` (str): Prompt to generate images.
- `timeout` (int, optional): Timeout for the request. Defaults to `TIMEOUT_IMAGE_CREATION`.

**Working principle**:
This function takes an active client session and a prompt to generate images using Bing's image creation service. It first checks if the `beautifulsoup4` package is installed and raises an error if it is not. The function then URL-encodes the prompt and sends a POST request to the Bing image creation endpoint. It handles potential errors such as rate limits, blocked prompts, and timeouts. Upon success, it extracts the redirect URL and request ID, and polls the image creation service until the images are generated. Finally, it calls the `read_images` function to extract the image URLs from the HTML content.

**Internal functions**:
- None

```python
async def create_images(session: ClientSession, prompt: str, timeout: int = TIMEOUT_IMAGE_CREATION) -> List[str]:
    """
    Creates images based on a given prompt using Bing's service.

    Args:
        session (ClientSession): Active client session.
        prompt (str): Prompt to generate images.
        timeout (int): Timeout for the request.

    Returns:
        List[str]: A list of URLs to the created images.

    Raises:
        RuntimeError: If image creation fails or times out.
    """
```

### `read_images`

**Description**: Extracts image URLs from the HTML content.

**Parameters**:
- `html_content` (str): HTML content containing image URLs.

**Working principle**:
This function parses the HTML content using BeautifulSoup to extract image URLs. It searches for `img` tags with specific classes (`mimg` or `gir_mmimg`) and extracts the `src` attribute, which contains the image URL. The function also checks for bad images and raises an error if any are found.

**Internal functions**:
- None

```python
def read_images(html_content: str) -> List[str]:
    """
    Extracts image URLs from the HTML content.

    Args:
        html_content (str): HTML content containing image URLs.

    Returns:
        List[str]: A list of image URLs.
    """
```

## Functions

### `create_session`

**Purpose**: Creates a new client session with specified cookies and headers.

**Parameters**:
- `cookies` (Dict[str, str]): Cookies to be used for the session.
- `proxy` (str, optional): Proxy configuration.
- `connector` (BaseConnector, optional): The connector to use for the session.

**Returns**:
- `ClientSession`: The created client session.

**Raises**:
- None

**How the function works**:
The function initializes an `aiohttp.ClientSession` with custom headers and cookies. It sets headers such as `accept`, `accept-encoding`, `accept-language`, and `user-agent` to mimic a browser request. If cookies are provided, they are added to the headers. The session also uses a connector, which can be customized for proxy support.

**Examples**:

```python
# Пример использования функции create_session
cookies = {"cookie1": "value1", "cookie2": "value2"}
session = create_session(cookies=cookies)
```

### `create_images`

**Purpose**: Creates images based on a given prompt using Bing's service.

**Parameters**:
- `session` (ClientSession): Active client session.
- `prompt` (str): Prompt to generate images.
- `timeout` (int, optional): Timeout for the request. Defaults to `TIMEOUT_IMAGE_CREATION`.

**Returns**:
- `List[str]`: A list of URLs to the created images.

**Raises**:
- `MissingRequirementsError`: If the `beautifulsoup4` package is not installed.
- `RateLimitError`: If there are no coins left to create images.
- `RuntimeError`: If image creation fails or times out.

**How the function works**:
The function takes an active client session and a prompt to generate images using Bing's image creation service. It first checks if the `beautifulsoup4` package is installed and raises an error if it is not. The function then URL-encodes the prompt and sends a POST request to the Bing image creation endpoint. It handles potential errors such as rate limits, blocked prompts, and timeouts. Upon success, it extracts the redirect URL and request ID, and polls the image creation service until the images are generated. Finally, it calls the `read_images` function to extract the image URLs from the HTML content.

**Internal functions**:
- None

**Examples**:

```python
# Пример использования функции create_images
import asyncio
from aiohttp import ClientSession

async def main():
    cookies = {"cookie1": "value1", "cookie2": "value2"}
    prompt = "A futuristic cityscape"
    async with ClientSession() as session:
        image_urls = await create_images(session, prompt)
        print(image_urls)

if __name__ == "__main__":
    asyncio.run(main())
```

### `read_images`

**Purpose**: Extracts image URLs from the HTML content.

**Parameters**:
- `html_content` (str): HTML content containing image URLs.

**Returns**:
- `List[str]`: A list of image URLs.

**Raises**:
- `RuntimeError`: If no images are found or if bad images are found.

**How the function works**:
This function parses the HTML content using BeautifulSoup to extract image URLs. It searches for `img` tags with specific classes (`mimg` or `gir_mmimg`) and extracts the `src` attribute, which contains the image URL. The function also checks for bad images and raises an error if any are found.

**Examples**:

```python
# Пример использования функции read_images
html_content = """
<img class="mimg" src="https://example.com/image1.jpg?w=300">
<img class="mimg" src="https://example.com/image2.jpg?w=300">
"""
image_urls = read_images(html_content)
print(image_urls) # Output: ['https://example.com/image1.jpg', 'https://example.com/image2.jpg']
```