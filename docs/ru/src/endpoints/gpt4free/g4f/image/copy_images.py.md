# Модуль для копирования изображений

## Обзор

Модуль `copy_images.py` предназначен для скачивания и сохранения изображений с использованием Unicode-безопасных имен файлов. Он предоставляет функции для обработки изображений различных типов (например, из URL или data URI) и сохранения их в локальную директорию. Модуль также включает проверку формата файла и создание URL для доступа к сохраненным изображениям.

## Подробней

Этот модуль играет важную роль в проекте `hypotez`, обеспечивая возможность локального хранения и обработки изображений, полученных из различных источников. Он обрабатывает случаи, когда изображения предоставляются в виде URL-адресов или data URI, а также обеспечивает безопасное именование файлов для предотвращения проблем с Unicode.

## Функции

### `get_media_extension`

```python
def get_media_extension(media: str) -> str:
    """Извлекает расширение медиафайла из URL или имени файла.

    Args:
        media (str): URL или имя файла.

    Returns:
        str: Расширение файла (например, ".jpg").

    Raises:
        ValueError: Если расширение файла не поддерживается.

    
    - Функция извлекает расширение файла из предоставленного URL или имени файла.
    - Проверяет, поддерживается ли расширение в `EXTENSIONS_MAP`.
    - Возвращает расширение или вызывает исключение, если оно не поддерживается.

    Примеры:
        >>> get_media_extension("image.jpg")
        '.jpg'
        >>> get_media_extension("http://example.com/image.png")
        '.png'
    """
```

### `ensure_images_dir`

```python
def ensure_images_dir():
    """Создает директорию для изображений, если она не существует.

    
    - Функция проверяет, существует ли директория `images_dir`.
    - Если директория не существует, она создает ее.

    Примеры:
        >>> ensure_images_dir()
    """
```

### `get_source_url`

```python
def get_source_url(image: str, default: str = None) -> str:
    """Извлекает оригинальный URL из параметра image, если он присутствует.

    Args:
        image (str): Строка, содержащая URL изображения.
        default (str, optional): Значение по умолчанию, если URL не найден. По умолчанию `None`.

    Returns:
        str: Оригинальный URL или значение по умолчанию.

    
    - Функция проверяет, содержит ли параметр `image` URL, закодированный в формате `url=...`.
    - Если URL найден, он декодируется и возвращается.
    - Если URL не найден, возвращается значение по умолчанию.

    Примеры:
        >>> get_source_url("image.jpg?url=http://example.com/image.jpg")
        'http://example.com/image.jpg'
        >>> get_source_url("image.jpg", default="http://example.com/default.jpg")
        'http://example.com/default.jpg'
    """
```

### `is_valid_media_type`

```python
def is_valid_media_type(content_type: str) -> bool:
    """Проверяет, является ли указанный Content-Type допустимым типом медиа.

    Args:
        content_type (str): Content-Type для проверки.

    Returns:
        bool: `True`, если Content-Type является допустимым, иначе `False`.

    
    - Функция проверяет, содержится ли `content_type` в `MEDIA_TYPE_MAP` или начинается ли он с "audio/" или "video/".
    - Возвращает `True`, если условие выполнено, иначе `False`.

    Примеры:
        >>> is_valid_media_type("image/jpeg")
        True
        >>> is_valid_media_type("audio/mpeg")
        True
        >>> is_valid_media_type("text/html")
        False
    """
```

### `save_response_media`

```python
async def save_response_media(response: StreamResponse, prompt: str, tags: list[str]) -> AsyncIterator:
    """Сохраняет медиа из ответа в локальный файл и возвращает URL.

    Args:
        response (StreamResponse): Объект ответа с медиаданными.
        prompt (str): Описание изображения.
        tags (list[str]): Список тегов для изображения.

    Yields:
        AsyncIterator: Объект `ImageResponse`, `AudioResponse` или `VideoResponse` с URL сохраненного файла.

    Raises:
        ValueError: Если тип медиа не поддерживается.

    
    - Функция извлекает `content-type` из заголовков ответа.
    - Определяет расширение файла на основе `content-type`.
    - Генерирует имя файла с использованием тегов, описания и хэша содержимого.
    - Сохраняет содержимое ответа в локальный файл.
    - Создает и возвращает объект ответа (ImageResponse, AudioResponse или VideoResponse) с URL сохраненного файла.

    Примеры:
        >>> # Пример использования требует реального объекта StreamResponse
        >>> # и асинхронного контекста.
        >>> # await save_response_media(response, "example prompt", ["tag1", "tag2"])
    """
```

### `get_filename`

```python
def get_filename(tags: list[str], alt: str, extension: str, image: str) -> str:
    """Генерирует имя файла на основе тегов, альтернативного текста, расширения и содержимого изображения.

    Args:
        tags (list[str]): Список тегов.
        alt (str): Альтернативный текст.
        extension (str): Расширение файла.
        image (str): Содержимое изображения.

    Returns:
        str: Сгенерированное имя файла.

    
    - Функция генерирует имя файла, включающее текущее время, теги, альтернативный текст и хэш содержимого изображения.
    - Использует `secure_filename` для обеспечения безопасности имени файла.
    - Возвращает сгенерированное имя файла.

    Примеры:
        >>> get_filename(["tag1", "tag2"], "alt text", ".jpg", "image content")
        '1678886400_tag1+tag2+alt text_e5b7e4b6_secure.jpg'
    """
```

### `copy_media`

```python
async def copy_media(
    images: list[str],
    cookies: Optional[Cookies] = None,
    headers: Optional[dict] = None,
    proxy: Optional[str] = None,
    alt: str = None,
    tags: list[str] = None,
    add_url: bool = True,
    target: str = None,
    ssl: bool = None
) -> list[str]:
    """Загружает и сохраняет изображения локально с Unicode-безопасными именами файлов.

    Args:
        images (list[str]): Список URL изображений для загрузки.
        cookies (Optional[Cookies], optional): Куки для использования при загрузке. По умолчанию `None`.
        headers (Optional[dict], optional): Заголовки для использования при загрузке. По умолчанию `None`.
        proxy (Optional[str], optional): Прокси для использования при загрузке. По умолчанию `None`.
        alt (str, optional): Альтернативный текст для изображений. По умолчанию `None`.
        tags (list[str], optional): Список тегов для изображений. По умолчанию `None`.
        add_url (bool, optional): Добавлять ли оригинальный URL в параметры запроса. По умолчанию `True`.
        target (str, optional): Целевой путь для сохранения изображения. По умолчанию `None`.
        ssl (bool, optional): Использовать ли SSL. По умолчанию `None`.

    Returns:
        list[str]: Список относительных URL изображений.

    
    - Функция принимает список URL изображений и параметры для их загрузки и сохранения.
    - Для каждого изображения выполняется загрузка и сохранение в локальную директорию.
    - Возвращает список относительных URL сохраненных изображений.

    Внутренние функции:

    `copy_image`

    ```python
    async def copy_image(image: str, target: str = None) -> str:
        """Обрабатывает отдельное изображение и возвращает его локальный URL.

        Args:
            image (str): URL изображения.
            target (str, optional): Целевой путь для сохранения изображения. По умолчанию `None`.

        Returns:
            str: Локальный URL изображения.

        
        - Функция проверяет, является ли изображение локальным.
        - Если изображение не локальное, оно загружается и сохраняется в локальную директорию.
        - Возвращает локальный URL изображения.
        """
    ```

    Примеры:
        >>> # Пример использования требует реального асинхронного контекста.
        >>> # await copy_media(["http://example.com/image.jpg"], alt="example", tags=["tag1"])
    """