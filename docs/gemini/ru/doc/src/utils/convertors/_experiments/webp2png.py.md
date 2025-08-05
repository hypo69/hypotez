# Модуль `src.utils.convertors._experiments.webp2png`

## Обзор

Модуль содержит функции для преобразования изображений в формате WebP в PNG. 
Он предназначен для обработки изображений, полученных из различных источников. 

## Подробней

Модуль содержит функцию `convert_images()`, которая рекурсивно обходит заданную директорию, 
находит все файлы WebP и преобразует их в PNG. Преобразованные изображения сохраняются в 
отдельную директорию.

## Функции

### `convert_images`

**Назначение**: Преобразует все изображения WebP в указанной директории в PNG.

**Параметры**:
- `webp_dir` (Path): Директория, содержащая исходные изображения WebP.
- `png_dir` (Path): Директория для сохранения преобразованных изображений PNG.

**Возвращает**:
- `None`

**Пример**:
```python
from src.utils.convertors._experiments.webp2png import convert_images
from src import gs

# Пример использования функции:
convert_images(
    gs.path.google_drive / 'emil' / 'raw_images_from_openai',
    gs.path.google_drive / 'emil' / 'converted_images'
)
```

**Как работает функция**:
1. Использует функцию `get_filenames` из `src.utils.file`, чтобы получить список всех файлов WebP в указанной директории.
2. Перебирает все файлы WebP в списке.
3. Для каждого файла WebP:
   - Формирует путь к файлу PNG с использованием имени исходного файла WebP, удаляя расширение и добавляя `.png`.
   - Вызывает функцию `webp2png` из `src.utils.convertors.webp2png`, передавая пути к файлам WebP и PNG.
   - Выводит результат работы функции `webp2png`.


## Примеры

```python
from src import gs
from src.utils.convertors._experiments.webp2png import convert_images

# Пример использования функции:
convert_images(
    gs.path.google_drive / 'kazarinov' / 'raw_images_from_openai',
    gs.path.google_drive / 'kazarinov' / 'converted_images'
)
```

## Внутренние функции

### `webp2png`

**Назначение**: Преобразует изображение WebP в PNG с использованием библиотеки Pillow.

**Параметры**:
- `webp_path` (Path): Путь к исходному файлу WebP.
- `png_path` (Path): Путь к файлу PNG для сохранения результата преобразования.

**Возвращает**:
- `str`: Сообщение о результатах преобразования, если оно успешно выполнено, или сообщение об ошибке, если преобразование не удалось.

**Как работает функция**:
1. Импортирует библиотеку `PIL` (Pillow).
2. Открывает файл WebP с помощью `PIL.Image.open`.
3. Преобразует изображение WebP в формат RGB, если исходное изображение было в формате RGBA.
4. Сохраняет преобразованное изображение в PNG-файл с помощью `PIL.Image.save`.
5. Возвращает сообщение о результатах преобразования.


## Параметры

### `gs`

- Модуль `gs` - это точка входа в проект `hypotez`. В этом модуле хранятся все константы, которые используются в проекте. В том числе константы для работы с Google Drive.

### `webp_dir`

- Директория, содержащая исходные изображения WebP.

### `png_dir`

- Директория для сохранения преобразованных изображений PNG.

## Примеры

```python
from src import gs
from src.utils.convertors._experiments.webp2png import convert_images

# Пример использования функции:
convert_images(
    gs.path.google_drive / 'kazarinov' / 'raw_images_from_openai',
    gs.path.google_drive / 'kazarinov' / 'converted_images'
)
```