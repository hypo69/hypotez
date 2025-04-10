# Модуль для работы с изображениями

## Обзор

Модуль `image.py` предоставляет набор функций и классов для обработки изображений, включая преобразование форматов, изменение размера, проверку формата и извлечение данных из URI. Он также содержит классы для представления запросов и ответов, связанных с изображениями.

## Подробнее

Модуль предназначен для работы с изображениями различных форматов, таких как `PNG`, `JPG`, `JPEG`, `GIF`, `WEBP` и `SVG`. Он включает функции для проверки допустимости расширений файлов, преобразования изображений в различные форматы и извлечения данных из URI.  Для работы с изображениями используется библиотека `Pillow` (PIL). Если библиотека отсутствует, выбрасывается исключение `MissingRequirementsError`.

## Классы

### `ImageDataResponse`

**Описание**: Класс для представления ответа, содержащего данные об изображении.

**Атрибуты**:
- `images` (Union[str, list]): Изображение или список изображений.
- `alt` (str): Альтернативный текст для изображения.

**Методы**:
- `get_list()`: Возвращает список изображений.

### `ImageRequest`

**Описание**: Класс для представления запроса, связанного с изображением.

**Атрибуты**:
- `options` (dict): Словарь с опциями запроса.

**Методы**:
- `get(key: str)`: Возвращает значение опции запроса по ключу.

## Функции

### `to_image`

```python
def to_image(image: ImageType, is_svg: bool = False) -> Image:
    """
    Converts the input image to a PIL Image object.

    Args:
        image (Union[str, bytes, Image]): The input image.

    Returns:
        Image: The converted PIL Image object.
    """
```

**Назначение**: Преобразует входное изображение в объект `PIL Image`.

**Параметры**:
- `image` (ImageType): Входное изображение. Может быть строкой (путь к файлу или URI), байтами или объектом `PIL Image`.
- `is_svg` (bool, optional): Флаг, указывающий, является ли изображение в формате `SVG`. По умолчанию `False`.

**Возвращает**:
- `Image`: Преобразованный объект `PIL Image`.

**Вызывает исключения**:
- `MissingRequirementsError`: Если не установлена библиотека `pillow` или `cairosvg` для работы с `SVG`.

**Как работает функция**:
1. Проверяет, установлена ли библиотека `pillow`. Если нет, вызывает исключение `MissingRequirementsError`.
2. Если `image` - строка, начинающаяся с `data:`, то проверяет, является ли `data URI` изображением, и извлекает данные из `URI`.
3. Если `is_svg` - `True`, пытается импортировать библиотеку `cairosvg`. Если библиотека не установлена, вызывает исключение `MissingRequirementsError`. Если `image` не байты, то считывает содержимое `image`. Конвертирует `svg` в `png`, используя `cairosvg.svg2png`.
4. Если `image` - байты, то проверяет, является ли формат изображения допустимым, и открывает изображение из байтов.
5. Если `image` не является экземпляром `PIL Image`, то открывает изображение из файла и загружает его.
6. Возвращает объект `PIL Image`.

**Примеры**:
```python
from PIL.Image import Image
from pathlib import Path

# Пример 1: Преобразование изображения из пути к файлу
image_path = "path/to/image.jpg"  # Замените на существующий путь к файлу
image = to_image(image_path)
print(type(image))  # Выведет: <class 'PIL.Image.Image'>

# Пример 2: Преобразование изображения из байтов
with open(image_path, "rb") as f:  # Замените на существующий путь к файлу
    image_bytes = f.read()
image = to_image(image_bytes)
print(type(image))  # Выведет: <class 'PIL.Image.Image'>

# Пример 3: Преобразование изображения из объекта PIL Image
image = Image.new("RGB", (60, 30), color="red")
image = to_image(image)
print(type(image))  # Выведет: <class 'PIL.Image.Image'>

# Пример 4: Преобразование SVG изображения
svg_path = "path/to/image.svg"  # Замените на существующий путь к файлу SVG
with open(svg_path, "rb") as f:
    svg_data = f.read()
image = to_image(svg_data, is_svg=True)
print(type(image))
```

### `is_allowed_extension`

```python
def is_allowed_extension(filename: str) -> bool:
    """
    Checks if the given filename has an allowed extension.

    Args:
        filename (str): The filename to check.

    Returns:
        bool: True if the extension is allowed, False otherwise.
    """
```

**Назначение**: Проверяет, имеет ли указанное имя файла допустимое расширение.

**Параметры**:
- `filename` (str): Имя файла для проверки.

**Возвращает**:
- `bool`: `True`, если расширение допустимо, `False` в противном случае.

**Как работает функция**:
1. Проверяет, содержит ли имя файла точку (`.`).
2. Разделяет имя файла по последней точке, чтобы получить расширение.
3. Приводит расширение к нижнему регистру и проверяет, входит ли оно в список допустимых расширений (`ALLOWED_EXTENSIONS`).
4. Возвращает `True`, если расширение допустимо, `False` в противном случае.

**Примеры**:
```python
# Пример 1: Проверка имени файла с допустимым расширением
filename = "image.png"
is_allowed = is_allowed_extension(filename)
print(is_allowed)  # Выведет: True

# Пример 2: Проверка имени файла с недопустимым расширением
filename = "document.txt"
is_allowed = is_allowed_extension(filename)
print(is_allowed)  # Выведет: False

# Пример 3: Проверка имени файла без расширения
filename = "image"
is_allowed = is_allowed_extension(filename)
print(is_allowed)  # Выведет: False
```

### `is_data_uri_an_image`

```python
def is_data_uri_an_image(data_uri: str) -> bool:
    """
    Checks if the given data URI represents an image.

    Args:
        data_uri (str): The data URI to check.

    Raises:
        ValueError: If the data URI is invalid or the image format is not allowed.
    """
```

**Назначение**: Проверяет, представляет ли указанный `data URI` изображение.

**Параметры**:
- `data_uri` (str): `Data URI` для проверки.

**Вызывает исключения**:
- `ValueError`: Если `data URI` недействителен или формат изображения не разрешен.

**Как работает функция**:
1. Проверяет, начинается ли `data URI` с `data:image` и содержит ли формат изображения (например, `jpeg`, `png`, `gif`).
2. Извлекает формат изображения из `data URI`.
3. Проверяет, входит ли формат изображения в список допустимых форматов (`ALLOWED_EXTENSIONS`) или является `svg+xml`.
4. Вызывает исключение `ValueError`, если `data URI` недействителен или формат изображения не разрешен.

**Примеры**:
```python
# Пример 1: Проверка допустимого data URI
data_uri = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w+n8AwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA