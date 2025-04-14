# Модуль для работы с изображениями
==========================================

Модуль предоставляет функции для обработки, преобразования и валидации изображений. Он включает в себя методы для конвертации изображений в различные форматы, проверки допустимости форматов, извлечения данных из URI и обработки ориентации изображений.

## Обзор

Модуль предназначен для работы с изображениями различных форматов, таких как PNG, JPG, JPEG, GIF, WEBP и SVG. Он предоставляет инструменты для преобразования изображений, проверки их форматов, извлечения данных из URI и обработки ориентации. Модуль также включает классы для обработки запросов и ответов, связанных с изображениями.

## Подробнее

Модуль содержит функции для работы с изображениями, такие как `to_image`, `is_allowed_extension`, `is_data_uri_an_image`, `is_accepted_format`, `extract_data_uri`, `get_orientation`, `process_image`, `to_bytes`, `to_data_uri`, а также классы `ImageDataResponse` и `ImageRequest`.

## Классы

### `ImageDataResponse`

**Описание**: Класс для представления ответа, содержащего информацию об изображениях и их альтернативном тексте (alt).

**Атрибуты**:
- `images` (Union[str, list]): Изображение или список изображений.
- `alt` (str): Альтернативный текст для изображения.

**Методы**:
- `get_list() -> list[str]`: Возвращает список изображений.

#### `__init__`

```python
def __init__(
    self,
    images: Union[str, list],
    alt: str,
):
    """Инициализирует объект ImageDataResponse.

    Args:
        images (Union[str, list]): Изображение или список изображений.
        alt (str): Альтернативный текст для изображения.
    """
    ...
```
#### `get_list`

```python
def get_list(self) -> list[str]:
    """Возвращает список изображений. Если `images` является строкой,
    она преобразуется в список.

    Returns:
        list[str]: Список изображений.
    """
    ...
```

### `ImageRequest`

**Описание**: Класс для представления запроса изображения с опциями.

**Атрибуты**:
- `options` (dict): Словарь опций для запроса изображения.

**Методы**:
- `get(key: str)`: Возвращает значение опции по ключу.

#### `__init__`

```python
def __init__(
    self,
    options: dict = {}
):
    """Инициализирует объект ImageRequest.

    Args:
        options (dict, optional): Словарь опций для запроса изображения. По умолчанию {}.
    """
    ...
```

#### `get`

```python
def get(self, key: str):
    """Возвращает значение опции по заданному ключу.

    Args:
        key (str): Ключ опции.

    Returns:
        Any: Значение опции или None, если ключ не найден.
    """
    ...
```

## Функции

### `to_image`

```python
def to_image(image: ImageType, is_svg: bool = False) -> Image:
    """
    Преобразует входное изображение в объект PIL Image.

    Args:
        image (Union[str, bytes, Image]): Входное изображение.
        is_svg (bool): Указывает, является ли изображение SVG. По умолчанию False.

    Returns:
        Image: Преобразованный объект PIL Image.

    Raises:
        MissingRequirementsError: Если не установлены необходимые пакеты (pillow или cairosvg).
    """
    ...
```

### `is_allowed_extension`

```python
def is_allowed_extension(filename: str) -> bool:
    """
    Проверяет, имеет ли заданное имя файла допустимое расширение.

    Args:
        filename (str): Имя файла для проверки.

    Returns:
        bool: True, если расширение допустимо, False в противном случае.
    """
    ...
```

### `is_data_uri_an_image`

```python
def is_data_uri_an_image(data_uri: str) -> bool:
    """
    Проверяет, представляет ли заданный URI данных изображение.

    Args:
        data_uri (str): URI данных для проверки.

    Raises:
        ValueError: Если URI данных недействителен или формат изображения не разрешен.
    """
    ...
```

### `is_accepted_format`

```python
def is_accepted_format(binary_data: bytes) -> str:
    """
    Проверяет, представляет ли заданные двоичные данные изображение с принятым форматом.

    Args:
        binary_data (bytes): Двоичные данные для проверки.

    Raises:
        ValueError: Если формат изображения не разрешен.

    Returns:
        str: Строка, представляющая MIME-тип изображения, например "image/jpeg"
    """
    ...
```

### `extract_data_uri`

```python
def extract_data_uri(data_uri: str) -> bytes:
    """
    Извлекает двоичные данные из заданного URI данных.

    Args:
        data_uri (str): URI данных.

    Returns:
        bytes: Извлеченные двоичные данные.
    """
    ...
```

### `get_orientation`

```python
def get_orientation(image: Image) -> int:
    """
    Получает ориентацию заданного изображения.

    Args:
        image (Image): Изображение.

    Returns:
        int: Значение ориентации.
    """
    ...
```

### `process_image`

```python
def process_image(image: Image, new_width: int, new_height: int) -> Image:
    """
    Обрабатывает заданное изображение, корректируя его ориентацию и изменяя его размер.

    Args:
        image (Image): Изображение для обработки.
        new_width (int): Новая ширина изображения.
        new_height (int): Новая высота изображения.

    Returns:
        Image: Обработанное изображение.
    """
    ...
```

### `to_bytes`

```python
def to_bytes(image: ImageType) -> bytes:
    """
    Преобразует заданное изображение в байты.

    Args:
        image (ImageType): Изображение для преобразования.

    Returns:
        bytes: Изображение в виде байтов.
    """
    ...
```

### `to_data_uri`

```python
def to_data_uri(image: ImageType) -> str:
    """Преобразует заданное изображение в URI данных.

    Args:
        image (ImageType): Изображение для преобразования.

    Returns:
        str: URI данных изображения.
    """
    ...
```