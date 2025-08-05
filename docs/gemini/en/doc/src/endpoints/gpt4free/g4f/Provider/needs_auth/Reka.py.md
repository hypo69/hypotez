# Provider Reka

## Overview

This module provides the `Reka` class, which implements the `AbstractProvider` interface and represents a provider for the `gpt4free` endpoint.  The `Reka` class handles communication with the `reka.ai` API for generating text completions, handling image uploads, and acquiring access tokens.

## Details

The `Reka` provider is designed to interact with the `reka.ai` service for generating text completions and managing image uploads. It leverages the `requests` library for HTTP communication and handles authentication with access tokens obtained from the `reka.ai` platform.

## Classes

### `Reka`

**Description**: This class represents the `reka.ai` provider for the `gpt4free` endpoint, inheriting from the `AbstractProvider` class. It handles authentication, image uploads, and text completion requests using the `reka.ai` API.

**Inherits**: `AbstractProvider`

**Attributes**:

- `domain` (str): The domain name for the `reka.ai` API.
- `url` (str): The base URL for the `reka.ai` API.
- `working` (bool): Indicates whether the provider is currently functional.
- `needs_auth` (bool): Indicates whether the provider requires authentication.
- `supports_stream` (bool): Indicates whether the provider supports streaming responses.
- `default_vision_model` (str): The default vision model to use for image uploads.
- `cookies` (dict): A dictionary containing cookies for authentication with the `reka.ai` API.

**Methods**:

- `create_completion(model: str, messages: Messages, stream: bool, proxy: str = None, api_key: str = None, image: ImageType = None, **kwargs) -> CreateResult`: This method generates a text completion response from the `reka.ai` API, handling authentication, image uploads, and streaming responses.
- `upload_image(cls, access_token, image: ImageType) -> str`: This method uploads an image to the `reka.ai` API and returns the URL of the uploaded image.
- `get_access_token(cls)`: This method retrieves an access token from the `reka.ai` API, using the provided cookies for authentication.

## Class Methods

### `create_completion`

```python
    def create_completion(
        cls,
        model: str,
        messages: Messages,
        stream: bool,
        proxy: str = None,
        api_key: str = None,
        image: ImageType = None,
        **kwargs
    ) -> CreateResult:
        """ 
        Генерирует завершение текста с помощью API reka.ai.
        Обрабатывает аутентификацию, загрузку изображений и потоковую передачу ответов.

        Args:
            model (str): Название модели, которую нужно использовать для генерации текста.
            messages (Messages): Список сообщений, которые должны быть отправлены в модель для генерации текста.
            stream (bool):  Включает потоковую передачу текста.
            proxy (str, optional):  Прокси-сервер для использования. Defaults to `None`.
            api_key (str, optional):  Ключ API для аутентификации. Defaults to `None`.
            image (ImageType, optional):  Изображение для загрузки. Defaults to `None`.

        Returns:
            CreateResult:  Результат генерации текста.
        """
        cls.proxy = proxy

        if not api_key:
            cls.cookies = get_cookies(cls.domain)
            if not cls.cookies:
                raise ValueError(f"No cookies found for {cls.domain}")
            elif "appSession" not in cls.cookies:
                raise ValueError(f"No appSession found in cookies for {cls.domain}, log in or provide bearer_auth")
            api_key = cls.get_access_token(cls)

        conversation = []
        for message in messages:
            conversation.append({
                "type": "human",
                "text": message["content"],
            })

        if image:
            image_url = cls.upload_image(cls, api_key, image)
            conversation[-1]["image_url"] = image_url
            conversation[-1]["media_type"] = "image"

        headers = {
            'accept': '*/*',
            'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
            'authorization': f'Bearer {api_key}',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': cls.url,
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

        json_data = {
            'conversation_history': conversation,
            'stream': True,
            'use_search_engine': False,
            'use_code_interpreter': False,
            'model_name': 'reka-core',
            'random_seed': int(time.time() * 1000),
        }

        tokens = ''

        response = requests.post(f'{cls.url}/api/chat', 
                                cookies=cls.cookies, headers=headers, json=json_data, proxies=cls.proxy, stream=True)

        for completion in response.iter_lines():
            if b'data' in completion:
                token_data = json.loads(completion.decode('utf-8')[5:])['text']

                yield (token_data.replace(tokens, ''))

                tokens = token_data
```

**Purpose**: This method sends a request to the `reka.ai` API to generate a text completion response, handling authentication, image uploads, and streaming.

**Parameters**:

- `model` (str): The name of the model to use for text generation.
- `messages` (Messages): A list of messages to be sent to the model for text generation.
- `stream` (bool): Flag to enable streaming of the text response.
- `proxy` (str, optional): A proxy server to use for the request. Defaults to `None`.
- `api_key` (str, optional): The API key for authentication. Defaults to `None`.
- `image` (ImageType, optional): An image to be uploaded. Defaults to `None`.

**Returns**:

- `CreateResult`: The result of the text generation process.

**Raises Exceptions**:

- `ValueError`: If no cookies are found or if the `appSession` cookie is missing.

**How the Function Works**:

1. **Authentication**: The function checks if an API key is provided. If not, it retrieves cookies for the `reka.ai` domain. If no cookies are found or the `appSession` cookie is missing, it raises a `ValueError`. Otherwise, it retrieves an access token using the `get_access_token` method.
2. **Conversation History**: The function assembles the conversation history from the provided messages, adding the "type" and "text" fields to each message.
3. **Image Upload**: If an image is provided, it uploads the image using the `upload_image` method and adds the image URL and media type to the last message in the conversation history.
4. **API Request**: The function builds the JSON data with the conversation history, streaming flag, and other parameters. It sets up the request headers, including the authorization header with the API key, and then sends a POST request to the `reka.ai` API endpoint for chat.
5. **Streaming Response**: The function iterates over the streamed lines from the response and yields the text data, replacing any existing tokens with the new data.

**Examples**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.Reka import Reka
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Example 1: Simple text generation
messages = [
    {"role": "user", "content": "Hello, how are you?"}
]
response = Reka.create_completion(model="reka", messages=messages, stream=True)
for completion in response:
    print(completion)

# Example 2: Text generation with image upload
messages = [
    {"role": "user", "content": "Describe this image:"}
]
image_data = ... # Your image data
response = Reka.create_completion(model="reka", messages=messages, stream=True, image=image_data)
for completion in response:
    print(completion)
```

### `upload_image`

```python
    def upload_image(cls, access_token, image: ImageType) -> str:
        """ 
        Загружает изображение на API reka.ai и возвращает URL загруженного изображения.

        Args:
            access_token (str):  Токен доступа для аутентификации.
            image (ImageType):  Изображение для загрузки.

        Returns:
            str:  URL загруженного изображения.
        """
        boundary_token = os.urandom(8).hex()

        headers = {
            'accept': '*/*',
            'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
            'cache-control': 'no-cache',
            'authorization': f'Bearer {access_token}',
            'content-type': f'multipart/form-data; boundary=----WebKitFormBoundary{boundary_token}',
            'origin': cls.url,
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': f'{cls.url}/chat/hPReZExtDOPvUfF8vCPC',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

        image_data = to_bytes(image)

        boundary = f'----WebKitFormBoundary{boundary_token}'
        data = f'--{boundary}\r\nContent-Disposition: form-data; name="image"; filename="image.png"\r\nContent-Type: image/png\r\n\r\n'
        data += image_data.decode('latin-1')
        data += f'\r\n--{boundary}--\r\n'

        response = requests.post(f'{cls.url}/api/upload-image', 
                                    cookies=cls.cookies, headers=headers, proxies=cls.proxy, data=data.encode('latin-1'))

        return response.json()['media_url']
```

**Purpose**: This method uploads an image to the `reka.ai` API and returns the URL of the uploaded image.

**Parameters**:

- `access_token` (str): The access token for authentication.
- `image` (ImageType): The image to be uploaded.

**Returns**:

- `str`: The URL of the uploaded image.

**How the Function Works**:

1. **Generate Boundary Token**: The function generates a random boundary token for the multipart form data.
2. **Build Request Data**: The function builds the multipart form data with the boundary token, the image data, and the content type.
3. **Send Request**: The function sends a POST request to the `reka.ai` API endpoint for image upload with the prepared data, cookies, headers, and proxy settings.
4. **Return Media URL**: The function extracts the media URL from the JSON response and returns it.

**Examples**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.Reka import Reka

access_token = ... # Your access token
image_data = ... # Your image data
image_url = Reka.upload_image(access_token, image_data)
print(f"Uploaded image URL: {image_url}")
```

### `get_access_token`

```python
    def get_access_token(cls):
        """
        Извлекает токен доступа из API reka.ai, используя предоставленные cookie для аутентификации.

        Args:
            None

        Returns:
            str: Токен доступа.
        """
        headers = {
            'accept': '*/*',
            'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': f'{cls.url}/chat',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

        try:
            response = requests.get(f'{cls.url}/bff/auth/access_token', 
                                    cookies=cls.cookies, headers=headers, proxies=cls.proxy)

            return response.json()['accessToken']

        except Exception as e:
            raise ValueError(f"Failed to get access token: {e}, refresh your cookies / log in into {cls.domain}")
```

**Purpose**: This method retrieves an access token from the `reka.ai` API using the provided cookies for authentication.

**Parameters**:

- None

**Returns**:

- `str`: The access token.

**Raises Exceptions**:

- `ValueError`: If an error occurs while retrieving the access token.

**How the Function Works**:

1. **Set Headers**: The function sets up the request headers, including the cookies and proxy settings.
2. **Send Request**: The function sends a GET request to the `reka.ai` API endpoint for access tokens.
3. **Extract Access Token**: The function extracts the access token from the JSON response and returns it.
4. **Handle Errors**: If an error occurs while retrieving the access token, the function raises a `ValueError` with the error message.

**Examples**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.Reka import Reka

access_token = Reka.get_access_token()
print(f"Access token: {access_token}")
```