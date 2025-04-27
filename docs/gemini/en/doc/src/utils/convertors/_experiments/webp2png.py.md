# Модуль для конвертации WebP в PNG
## Обзор

Модуль `webp2png` предназначен для конвертации изображений в формате WebP в формат PNG. 

Он извлекает файлы WebP из указанного каталога и конвертирует их в формат PNG, сохраняя результат в другой каталог. Конвертация осуществляется функцией `webp2png`.

## Детали

Модуль использует функцию `webp2png`, которая принимает путь к файлу WebP и путь к файлу PNG, в который будет сохранена конвертированная версия. 

Функция `convert_images` ищет файлы WebP в указанном каталоге, конвертирует их в PNG и сохраняет результат в заданный каталог.

## Классы
### `convert_images`
**Описание**: Функция конвертирует все изображения WebP в указанном каталоге в формат PNG.

**Параметры**:
- `webp_dir` (Path): Каталог, содержащий исходные изображения WebP.
- `png_dir` (Path): Каталог для сохранения конвертированных изображений PNG.

**Пример**:
```python
convert_images(
    gs.path.google_drive / 'emil' / 'raw_images_from_openai',
    gs.path.google_drive / 'emil' / 'converted_images'
)
```

**Как работает функция**:
- Функция извлекает список файлов WebP из каталога `webp_dir` с помощью функции `get_filenames`.
- Она итерирует по каждому файлу WebP и создает имя файла PNG, добавляя к нему расширение `.png`.
- Функция `webp2png` конвертирует файл WebP в PNG и сохраняет результат в каталоге `png_dir`.

**Примеры**:
- Пример 1: `convert_images(gs.path.google_drive / 'emil' / 'raw_images_from_openai', gs.path.google_drive / 'emil' / 'converted_images')` конвертирует все изображения WebP в каталоге `gs.path.google_drive / 'emil' / 'raw_images_from_openai'` в PNG и сохраняет их в каталоге `gs.path.google_drive / 'emil' / 'converted_images'`.

## Функции
### `webp2png`
**Описание**: Функция конвертирует файл WebP в PNG.

**Параметры**:
- `webp_path` (Path): Путь к файлу WebP.
- `png_path` (Path): Путь к файлу PNG, в который будет сохранена конвертированная версия.

**Возвращает**:
- `bool`: `True` в случае успешной конвертации, `False` в случае ошибки.

**Пример**:
```python
webp_path = gs.path.google_drive / 'emil' / 'raw_images_from_openai' / 'image.webp'
png_path = gs.path.google_drive / 'emil' / 'converted_images' / 'image.png'
result = webp2png(webp_path, png_path)
```

**Как работает функция**:
- Функция использует библиотеку `Pillow` для конвертации файла WebP в PNG.
- Она сохраняет конвертированный файл PNG в указанный путь.

**Примеры**:
- Пример 1: `webp2png(gs.path.google_drive / 'emil' / 'raw_images_from_openai' / 'image.webp', gs.path.google_drive / 'emil' / 'converted_images' / 'image.png')` конвертирует файл `gs.path.google_drive / 'emil' / 'raw_images_from_openai' / 'image.webp'` в PNG и сохраняет его в `gs.path.google_drive / 'emil' / 'converted_images' / 'image.png'`.