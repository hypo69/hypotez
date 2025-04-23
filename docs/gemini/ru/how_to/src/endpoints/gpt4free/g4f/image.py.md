### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предоставляет набор функций для работы с изображениями, включая преобразование различных форматов изображений в PIL Image объекты, проверку форматов, извлечение данных из URI, изменение размера и ориентации изображений, а также преобразование изображений в байты или data URI.

Шаги выполнения
-------------------------
1. **Преобразование изображения в PIL Image объект:**
   - Функция `to_image` принимает изображение в различных форматах (путь к файлу, байты, PIL Image) и преобразует его в PIL Image объект.
   - Сначала проверяется, установлена ли библиотека `pillow`. Если нет, вызывается исключение `MissingRequirementsError`.
   - Если изображение представлено в виде data URI, функция `is_data_uri_an_image` проверяет его формат, а затем `extract_data_uri` извлекает бинарные данные.
   - Если изображение является SVG, используется `cairosvg` для преобразования в PNG.
   - Если изображение представлено в виде байтов, `is_accepted_format` проверяет формат изображения.
   - Если изображение не является экземпляром PIL Image, оно открывается с помощью `open_image`.

2. **Проверка расширения файла:**
   - Функция `is_allowed_extension` проверяет, имеет ли файл допустимое расширение (`png`, `jpg`, `jpeg`, `gif`, `webp`, `svg`).

3. **Проверка Data URI:**
   - Функция `is_data_uri_an_image` проверяет, является ли data URI изображением.
   - Проверяется, начинается ли URI с `data:image/` и содержит ли допустимый формат изображения.

4. **Проверка формата бинарных данных:**
   - Функция `is_accepted_format` проверяет, соответствуют ли бинарные данные допустимому формату изображения, проверяя magic bytes.

5. **Извлечение данных из Data URI:**
   - Функция `extract_data_uri` извлекает бинарные данные из data URI, декодируя base64.

6. **Получение ориентации изображения:**
   - Функция `get_orientation` извлекает информацию об ориентации изображения из EXIF-данных.

7. **Обработка изображения:**
   - Функция `process_image` корректирует ориентацию изображения на основе EXIF-данных и изменяет его размер.
   - При необходимости удаляется прозрачность (для формата RGBA) и преобразуется в формат RGB.

8. **Преобразование изображения в байты:**
   - Функция `to_bytes` преобразует изображение в байты из различных форматов (PIL Image, путь к файлу, байты, data URI).

9. **Преобразование изображения в Data URI:**
   - Функция `to_data_uri` преобразует изображение в data URI.

Пример использования
-------------------------

```python
from pathlib import Path
from PIL.Image import open as open_image
from io import BytesIO

# Пример преобразования изображения в PIL Image объект из файла
image_path = "example.jpg"
image = to_image(image_path)

# Пример преобразования изображения в PIL Image объект из байтов
image_bytes = Path(image_path).read_bytes()
image = to_image(image_bytes)

# Пример проверки расширения файла
filename = "example.png"
is_allowed = is_allowed_extension(filename)
print(f"Разрешенное расширение: {is_allowed}")

# Пример обработки изображения
new_width = 200
new_height = 200
processed_image = process_image(image, new_width, new_height)

# Пример преобразования изображения в байты
image_bytes = to_bytes(processed_image)

# Пример преобразования изображения в data URI
data_uri = to_data_uri(processed_image)

# Пример использования ImageDataResponse и ImageRequest
from typing import Union, List
class ImageDataResponse():
    def __init__(
        self,
        images: Union[str, list],
        alt: str,
    ):
        self.images = images
        self.alt = alt

    def get_list(self) -> list[str]:
        return [self.images] if isinstance(self.images, str) else self.images

class ImageRequest():
    def __init__(
        self,
        options: dict = {}
    ):
        self.options = options

    def get(self, key: str):
        return self.options.get(key)
# Создание экземпляра ImageDataResponse
image_data_response = ImageDataResponse(images=["image1.jpg", "image2.png"], alt="Примеры изображений")

# Получение списка изображений
image_list = image_data_response.get_list()
print(f"Список изображений: {image_list}")

# Создание экземпляра ImageRequest
image_request = ImageRequest(options={"width": 200, "height": 300})

# Получение значения из options
width = image_request.get("width")
print(f"Ширина: {width}")

```