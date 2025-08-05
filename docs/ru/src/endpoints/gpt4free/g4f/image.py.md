# Модуль для работы с изображениями

## Обзор

Модуль `image.py` предназначен для обработки изображений, включая конвертацию, проверку формата, извлечение данных из URI и изменение размера. Он использует библиотеку PIL (Pillow) для работы с изображениями. Модуль также включает классы `ImageDataResponse` и `ImageRequest` для управления данными изображений и запросами.

## Подробнее

Этот модуль предоставляет набор функций для работы с изображениями различных форматов, таких как PNG, JPG, JPEG, GIF, WEBP и SVG. Он позволяет конвертировать изображения между различными форматами, проверять их допустимые расширения и извлекать данные из URI. Кроме того, модуль содержит функции для изменения размера изображений, обработки ориентации и удаления прозрачности.

## Классы

### `ImageDataResponse`

**Описание**: Класс `ImageDataResponse` предназначен для хранения данных об изображении, включая список изображений и альтернативный текст.

**Атрибуты**:

- `images` (Union[str, list]): Список изображений или одно изображение в виде строки.
- `alt` (str): Альтернативный текст для изображения.

**Методы**:

#### `__init__(images: Union[str, list], alt: str)`

**Назначение**: Конструктор класса `ImageDataResponse`.

**Параметры**:

- `images` (Union[str, list]): Список изображений или одно изображение в виде строки.
- `alt` (str): Альтернативный текст для изображения.

**Пример**:

```python
data = ImageDataResponse(images=["image1.png", "image2.jpg"], alt="Пример изображений")
```

#### `get_list() -> list[str]`

**Назначение**: Возвращает список изображений. Если `self.images` является строкой, метод преобразует ее в список.

**Возвращает**:

- `list[str]`: Список строк, представляющих изображения.

**Пример**:

```python
data = ImageDataResponse(images="image1.png", alt="Пример изображения")
image_list = data.get_list()
print(image_list)  # Вывод: ['image1.png']
```

### `ImageRequest`

**Описание**: Класс `ImageRequest` используется для представления запроса изображения с опциями.

**Атрибуты**:

- `options` (dict): Словарь с опциями запроса.

**Методы**:

#### `__init__(options: dict = {})`

**Назначение**: Конструктор класса `ImageRequest`.

**Параметры**:

- `options` (dict, optional): Словарь с опциями запроса. По умолчанию `{}`.

**Пример**:

```python
request = ImageRequest(options={"width": 100, "height": 200})
```

#### `get(key: str)`

**Назначение**: Возвращает значение опции по ключу.

**Параметры**:

- `key` (str): Ключ опции.

**Возвращает**:

- Значение опции по ключу, или `None`, если ключ не найден.

**Пример**:

```python
request = ImageRequest(options={"width": 100, "height": 200})
width = request.get("width")
print(width)  # Вывод: 100
```

## Функции

### `to_image(image: ImageType, is_svg: bool = False) -> Image`

**Назначение**: Преобразует входное изображение в объект `PIL Image`.

**Параметры**:

- `image` (ImageType): Входное изображение (строка, байты или объект `Image`).
- `is_svg` (bool, optional): Флаг, указывающий, является ли изображение SVG. По умолчанию `False`.

**Возвращает**:

- `Image`: Преобразованный объект `PIL Image`.

**Вызывает исключения**:

- `MissingRequirementsError`: Если отсутствует пакет `pillow` или `cairosvg` (для SVG).
- `ValueError`: Если data URI или формат изображения недействителен.

**Как работает функция**:

1. Проверяет наличие необходимых зависимостей (pillow).
2. Если изображение является строкой и начинается с "data:", извлекает данные из URI.
3. Если `is_svg` равен `True`, использует `cairosvg` для преобразования SVG в PNG.
4. Если изображение является байтами, проверяет формат и открывает как `PIL Image`.
5. Если изображение не является объектом `PIL Image`, открывает его с помощью `open_image` и загружает.

**Пример**:

```python
from PIL.Image import Image
image_path = "example.jpg"  # замените на имя файла изображения
image = to_image(image_path)
print(type(image))
```

### `is_allowed_extension(filename: str) -> bool`

**Назначение**: Проверяет, имеет ли заданное имя файла допустимое расширение.

**Параметры**:

- `filename` (str): Имя файла для проверки.

**Возвращает**:

- `bool`: `True`, если расширение допустимо, `False` в противном случае.

**Как работает функция**:

Функция проверяет, содержит ли имя файла точку (`.`) и входит ли расширение файла (после последней точки) в список разрешенных расширений `ALLOWED_EXTENSIONS`.

**Пример**:

```python
filename = "example.png"
is_allowed = is_allowed_extension(filename)
print(is_allowed)  # Вывод: True

filename = "example.txt"
is_allowed = is_allowed_extension(filename)
print(is_allowed)  # Вывод: False
```

### `is_data_uri_an_image(data_uri: str) -> bool`

**Назначение**: Проверяет, представляет ли заданный data URI изображение.

**Параметры**:

- `data_uri` (str): Data URI для проверки.

**Вызывает исключения**:

- `ValueError`: Если data URI недействителен или формат изображения не разрешен.

**Как работает функция**:

Функция проверяет, соответствует ли data URI формату `data:image/<формат>;base64,...` и входит ли формат изображения в список разрешенных форматов (`ALLOWED_EXTENSIONS`).

**Пример**:

```python
data_uri = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w+rAIYcFnQAEcIDExEQAAAABJRU5ErkJggg=="
try:
    is_valid = is_data_uri_an_image(data_uri)
    print(is_valid)
except ValueError as ex:
    print(f"Ошибка: {ex}")
```

### `is_accepted_format(binary_data: bytes) -> str`

**Назначение**: Проверяет, представляет ли заданные двоичные данные изображение с допустимым форматом.

**Параметры**:

- `binary_data` (bytes): Двоичные данные для проверки.

**Возвращает**:

- `str`: MIME-тип изображения (например, `"image/jpeg"`).

**Вызывает исключения**:

- `ValueError`: Если формат изображения не разрешен.

**Как работает функция**:

Функция проверяет начальные байты двоичных данных, чтобы определить формат изображения (JPEG, PNG, GIF, WEBP).

**Пример**:

```python
with open("example.png", "rb") as f:
    binary_data = f.read()
try:
    image_format = is_accepted_format(binary_data)
    print(image_format)  # Вывод: image/png
except ValueError as ex:
    print(f"Ошибка: {ex}")
```

### `extract_data_uri(data_uri: str) -> bytes`

**Назначение**: Извлекает двоичные данные из заданного data URI.

**Параметры**:

- `data_uri` (str): Data URI.

**Возвращает**:

- `bytes`: Извлеченные двоичные данные.

**Как работает функция**:

Функция разделяет data URI по запятой, декодирует данные в формате Base64 и возвращает их.

**Пример**:

```python
data_uri = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w+rAIYcFnQAEcIDExEQAAAABJRU5ErkJggg=="
binary_data = extract_data_uri(data_uri)
print(type(binary_data))  # Вывод: <class 'bytes'>
```

### `get_orientation(image: Image) -> int`

**Назначение**: Получает ориентацию заданного изображения из метаданных EXIF.

**Параметры**:

- `image` (Image): Изображение.

**Возвращает**:

- `int`: Значение ориентации (если доступно).

**Как работает функция**:

Функция пытается получить данные EXIF из изображения и возвращает значение тега ориентации (274).

**Пример**:

```python
from PIL import Image as PILImage
image_path = "example.jpg"
image = PILImage.open(image_path)
orientation = get_orientation(image)
print(orientation)
```

### `process_image(image: Image, new_width: int, new_height: int) -> Image`

**Назначение**: Обрабатывает заданное изображение, корректируя его ориентацию и изменяя размер.

**Параметры**:

- `image` (Image): Изображение для обработки.
- `new_width` (int): Новая ширина изображения.
- `new_height` (int): Новая высота изображения.

**Возвращает**:

- `Image`: Обработанное изображение.

**Как работает функция**:

1. Корректирует ориентацию изображения на основе данных EXIF.
2. Изменяет размер изображения до заданных ширины и высоты.
3. Удаляет прозрачность (если есть) и преобразует в формат RGB.

**Пример**:

```python
from PIL import Image as PILImage
image_path = "example.png"
image = PILImage.open(image_path)
processed_image = process_image(image, 100, 100)
processed_image.save("processed_example.png")
```

### `to_bytes(image: ImageType) -> bytes`

**Назначение**: Преобразует заданное изображение в байты.

**Параметры**:

- `image` (ImageType): Изображение для преобразования.

**Возвращает**:

- `bytes`: Изображение в виде байтов.

**Как работает функция**:

Функция обрабатывает различные типы входных данных (байты, data URI, `PIL Image`, путь к файлу) и возвращает изображение в виде байтов.

**Пример**:

```python
from PIL import Image as PILImage
image_path = "example.png"
image = PILImage.open(image_path)
image_bytes = to_bytes(image)
print(type(image_bytes))  # Вывод: <class 'bytes'>
```

### `to_data_uri(image: ImageType) -> str`

**Назначение**: Преобразует заданное изображение в data URI.

**Параметры**:

- `image` (ImageType): Изображение для преобразования.

**Возвращает**:

- `str`: Изображение в виде data URI.

**Как работает функция**:

Функция преобразует изображение в байты, кодирует их в Base64 и формирует data URI.

**Пример**:

```python
from PIL import Image as PILImage
image_path = "example.png"
image = PILImage.open(image_path)
data_uri = to_data_uri(image)
print(data_uri[:50])  # Вывод: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA