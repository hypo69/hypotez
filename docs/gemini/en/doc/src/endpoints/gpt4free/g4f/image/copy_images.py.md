# Модуль для Копирования Изображений

## Обзор

Модуль предназначен для скачивания и локального сохранения изображений, обеспечивая Unicode-безопасные имена файлов. Он возвращает список относительных URL-адресов изображений.

## Подробнее

Этот модуль предоставляет функции для скачивания изображений с различных источников, включая URL-адреса и data URI, и сохранения их локально с использованием Unicode-безопасных имен файлов. Это особенно полезно для работы с изображениями, полученными из ненадежных источников, где требуется обеспечить безопасность и совместимость имен файлов.

## Функции

### `get_media_extension`

```python
def get_media_extension(media: str) -> str:
    """Извлекает расширение медиафайла из URL или имени файла.

    Args:
        media (str): URL или имя файла медиа.

    Returns:
        str: Расширение медиафайла.

    Raises:
        ValueError: Если расширение медиафайла не поддерживается.

    Example:
        >>> get_media_extension("image.png")
        '.png'
    """
    ...
```

### `ensure_images_dir`

```python
def ensure_images_dir():
    """Создает каталог для изображений, если он не существует."""
    ...
```

### `get_source_url`

```python
def get_source_url(image: str, default: str = None) -> str:
    """Извлекает исходный URL из параметра изображения, если он присутствует.

    Args:
        image (str): Параметр изображения, который может содержать URL.
        default (str, optional): Значение по умолчанию, если URL не найден. По умолчанию `None`.

    Returns:
        str: Исходный URL или значение по умолчанию.

    Example:
        >>> get_source_url("image.png?url=http://example.com/image.png")
        'http://example.com/image.png'
    """
    ...
```

### `is_valid_media_type`

```python
def is_valid_media_type(content_type: str) -> bool:
    """Проверяет, является ли тип содержимого допустимым медиатипом.

    Args:
        content_type (str): Тип содержимого для проверки.

    Returns:
        bool: `True`, если тип содержимого допустим, иначе `False`.

    Example:
        >>> is_valid_media_type("image/png")
        True
    """
    ...
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
        AsyncIterator: Объект ответа, содержащий URL медиафайла.

    Raises:
        ValueError: Если тип медиа не поддерживается.
    """
    ...
```

### `get_filename`

```python
def get_filename(tags: list[str], alt: str, extension: str, image: str) -> str:
    """Создает имя файла на основе тегов, альтернативного текста, расширения и содержимого изображения.

    Args:
        tags (list[str]): Список тегов.
        alt (str): Альтернативный текст.
        extension (str): Расширение файла.
        image (str): Содержимое изображения.

    Returns:
        str: Сгенерированное имя файла.

    Example:
        >>> get_filename(['tag1', 'tag2'], 'alt_text', '.png', 'image_content')
        '1678886400_tag1+tag2+alt_text_e5b7e3b0c6f03f28.png'
    """
    ...
```

### `copy_media`

```python
async def copy_media(
    images: list[str],\
    cookies: Optional[Cookies] = None,\
    headers: Optional[dict] = None,\
    proxy: Optional[str] = None,\
    alt: str = None,\
    tags: list[str] = None,\
    add_url: bool = True,\
    target: str = None,\
    ssl: bool = None\
) -> list[str]:
    """Загружает и сохраняет изображения локально с Unicode-безопасными именами файлов. Возвращает список относительных URL-адресов изображений.

    Args:
        images (list[str]): Список URL-адресов изображений для копирования.
        cookies (Optional[Cookies], optional): Файлы cookie для использования при запросе. По умолчанию `None`.
        headers (Optional[dict], optional): Заголовки для использования при запросе. По умолчанию `None`.
        proxy (Optional[str], optional): Прокси-сервер для использования при запросе. По умолчанию `None`.
        alt (str, optional): Альтернативный текст для использования при создании имени файла. По умолчанию `None`.
        tags (list[str], optional): Список тегов для использования при создании имени файла. По умолчанию `None`.
        add_url (bool, optional): Добавлять ли URL исходного изображения в URL локального файла. По умолчанию `True`.
        target (str, optional): Целевой путь для сохранения изображения. Если указан, имя файла генерируется не будет. По умолчанию `None`.
        ssl (bool, optional): Использовать ли SSL. По умолчанию `None`.

    Returns:
        list[str]: Список относительных URL-адресов локально сохраненных изображений.

    Example:
        >>> await copy_media(['http://example.com/image.png'], alt='example', tags=['tag1'])
        ['/media/1678886400_tag1+example_e5b7e3b0c6f03f28.png?url=http%3A%2F%2Fexample.com%2Fimage.png']
    """
    ...
```

## Принцип работы

1.  **Инициализация**:

    *   Функция `copy_media` принимает список URL-адресов изображений (`images`) и дополнительные параметры, такие как cookies, заголовки, прокси, альтернативный текст, теги и флаг для добавления URL.
    *   Она проверяет, нужно ли добавлять URL исходного изображения в URL локального файла, и создает каталог для изображений, если он не существует.

2.  **Создание сессии**:

    *   Функция создает асинхронную сессию `ClientSession` с использованием предоставленных cookies, заголовков и прокси.

3.  **Обработка каждого изображения**:

    *   Для каждого URL-адреса изображения функция `copy_image` выполняет следующие действия:
        *   Проверяет, является ли изображение локальным. Если да, возвращает его.
        *   Определяет целевой путь для сохранения изображения. Если `target` не указан, генерирует имя файла на основе тегов, альтернативного текста и расширения изображения.
        *   Обрабатывает различные типы изображений:
            *   Если изображение является data URI, извлекает данные и сохраняет их в файл.
            *   Если изображение является URL-адресом, выполняет HTTP-запрос для скачивания изображения и сохраняет его в файл.
        *   После сохранения изображения функция проверяет формат файла и, если необходимо, добавляет расширение к имени файла.
        *   Создает URL-адрес локального файла с безопасным кодированием и добавляет URL исходного изображения, если это необходимо.

4.  **Обработка ошибок**:

    *   Если во время копирования изображения возникают ошибки (например, ClientError, IOError, OSError, ValueError), функция регистрирует ошибку и пытается вернуть исходный URL изображения.

5.  **Асинхронный запуск**:

    *   Функция использует `asyncio.gather` для параллельного выполнения копирования всех изображений.

6.  **Возврат результатов**:

    *   Функция возвращает список URL-адресов локально сохраненных изображений.

## Примеры

```python
import asyncio
from src.endpoints.gpt4free.g4f.image.copy_images import copy_media

async def main():
    images = ['https://www.easygifanimator.net/images/samples/video-to-gif-sample.gif']
    result = await copy_media(images, alt='example', tags=['gif'])
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
# Expected output: ['/media/1678886400_gif+example_e5b7e3b0c6f03f28.gif?url=https%3A%2F%2Fwww.easygifanimator.net%2Fimages%2Fsamples%2Fvideo-to-gif-sample.gif']
```
```python
import asyncio
from src.endpoints.gpt4free.g4f.image.copy_images import copy_media

async def main():
    images = ['data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w+3ZgYGBiYmBlcfPycZAABd7A8gVv+MAAAAASUVORK5CYII=']
    result = await copy_media(images, alt='example', tags=['base64'])
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
# Expected output: ['/media/1678886400_base64+example_e5b7e3b0c6f03f28.png']