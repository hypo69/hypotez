## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода предоставляет набор функций для работы с изображениями. Он позволяет конвертировать изображения в различные форматы, проверять их типы и ориентацию, а также изменять размер и ориентацию изображений.

Шаги выполнения
-------------------------
1. **Проверка и конвертация изображения**:
   - Функция `to_image()` преобразует входное изображение в объект PIL Image. Она поддерживает различные форматы ввода, включая строки, байты и объекты PIL Image.
   - Если входное изображение является строкой, начинающейся с "data:", функция извлекает бинарные данные из строки и преобразует их в объект PIL Image.
   - Если входное изображение является байтами, функция проверяет, является ли формат файла допустимым, и преобразует его в объект PIL Image.
   - Если входное изображение является объектом PIL Image, функция просто возвращает его.
2. **Проверка расширения файла**:
   - Функция `is_allowed_extension()` проверяет, имеет ли заданное имя файла допустимое расширение.
   - Допустимые расширения файлов определены в константе `ALLOWED_EXTENSIONS`.
3. **Проверка типа данных URI**:
   - Функция `is_data_uri_an_image()` проверяет, представляет ли данный URI изображение.
   - Она проверяет, начинается ли строка с "data:image" и содержит ли она допустимый формат изображения.
4. **Проверка формата изображения**:
   - Функция `is_accepted_format()` проверяет, представляет ли данный набор байтов допустимый формат изображения.
   - Она использует специальные коды для определения формата изображения, например, `\xFF\xD8\xFF` для JPEG.
5. **Извлечение данных URI**:
   - Функция `extract_data_uri()` извлекает бинарные данные из данной строки URI.
   - Она декодирует строку base64 и возвращает бинарные данные.
6. **Получение ориентации изображения**:
   - Функция `get_orientation()` возвращает ориентацию заданного изображения.
   - Она использует EXIF-данные изображения, чтобы получить ориентацию.
7. **Обработка изображения**:
   - Функция `process_image()` обрабатывает заданное изображение путем корректировки его ориентации и изменения размера.
   - Она использует функции `transpose()` и `thumbnail()` объекта PIL Image для изменения ориентации и размера изображения.
8. **Преобразование изображения в байты**:
   - Функция `to_bytes()` преобразует заданное изображение в байты.
   - Она сохраняет изображение в объект BytesIO и возвращает его содержимое в виде байтов.
9. **Преобразование изображения в строку URI**:
   - Функция `to_data_uri()` преобразует заданное изображение в строку URI.
   - Она преобразует изображение в байты, кодирует их в base64 и создает строку URI.
10. **Классы ImageDataResponse и ImageRequest**:
   - Класс `ImageDataResponse` представляет ответ с данными изображения.
   - Класс `ImageRequest` представляет запрос изображения.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.image import to_image, to_bytes, to_data_uri

# Загружаем изображение из файла
image_path = 'path/to/image.jpg'
image = to_image(image_path)

# Изменяем размер изображения
new_width = 200
new_height = 100
processed_image = process_image(image, new_width, new_height)

# Сохраняем обработанное изображение в файл
processed_image.save('processed_image.jpg')

# Преобразуем изображение в байты
image_bytes = to_bytes(processed_image)

# Преобразуем изображение в строку URI
image_data_uri = to_data_uri(processed_image)
```